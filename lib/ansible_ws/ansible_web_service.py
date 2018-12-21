import yaml, logging, re, subprocess, ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

def get_parameters(qs, config_parameters):
    validation = True
    parameters = dict()
    type = None
    for name, desc in config_parameters.items():
        print(name, desc)
        type = 'text'
        default = None
        attributes = desc.get('attributes', [])
        if 'multiple' in attributes:
            type = 'list'
            default = []
        if 'default' in desc:
            default = desc.get('default')
            if isinstance(default, list):
                type = 'list'
        print(name, default, type)
        if type == 'list':
            value = qs.get(name, default)
            if 'choices' in desc:
                if not set(value).issubset(set(choices)):
                    validation = False
            if 'required' in attributes:
                if value == []:
                    validation = False
        else:
            value = qs.get(name, [default])[0]
            if 'choices' in desc:
                if value not in desc['choices']:
                    validation = False
            if 'required' in attributes:
                if value is None:
                    validation = False
        parameters[name] = value
        print(name, value)

    return (validation, parameters)


class AnsibleWebService(object):

    def __init__(self, config_file, query_strings):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_file = config_file
        self.query_strings = query_strings
        try:
            with open(self.config_file) as (f):
                self.config = yaml.load(f)
                self.logger.info(f'''Configuration file {(self.config_file)} LOADED''')
        except Exception:
            self.logger.error(f'''Not possible to load configuration file {config_file}''')

        self.mode_debug = query_strings.get('debug', ['false'])[0] == 'true'
        parameters_valid, parameters = get_parameters(self.query_strings, self.config['parameters'])
        self.parameters = parameters
        self.parameters_valid = parameters_valid
        self.debug = dict()
        self.result = dict()
        self.meta = dict(config_file=self.config_file,
          config=self.config,
          query_stringq=self.query_strings,
          parameters=self.parameters,
          parameters_valid=self.parameters_valid)
        self.run()

    def get_param(self, name):
        return self.parameters.get(name)

    def run(self):
        pass

    def get_result(self):
        output = dict(results=self.result)
        if self.mode_debug:
            output['meta'] = self.meta
            output['debug'] = self.debug
        return output


class AnsibleWebServiceHosts(AnsibleWebService):
    TYPE_LIST = 'list'
    TYPE_REGEX = 'regex'

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        type = self.parameters['type']
        sources = self.parameters['sources']
        if type == self.TYPE_LIST:
            groups = self.query_strings.get('groups', None)
        else:
            if type == self.TYPE_REGEX:
                groups = self.query_strings.get('groups', [None])[0]
        loader = DataLoader()
        inventory = InventoryManager(loader=loader,
          sources=sources)
        groups_dict = inventory.get_groups_dict()
        if type == self.TYPE_LIST:
            response = dict(((group_name, groups_dict[group_name]) for group_name in inventory.groups if group_name in groups))
        else:
            pattern = re.compile(groups)
            response = dict(((group_name, groups_dict[group_name]) for group_name in inventory.groups if re.match(pattern, group_name)))
        self.result = response


class AnsibleWebServiceTags(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        playbook = self.get_param('playbook')
        command = ['ansible-playbook', '--list-tags', playbook]
        p = subprocess.run(command, capture_output=True)
        out = p.stdout.decode('utf-8')
        tags = []
        line_refused = []
        line_accepted = []
        pattern = re.compile('^.*\\[(?P<string_tags>.+)\\].*$')
        for line in out.split('\n'):
            match = re.match(pattern, line)
            if match is not None:
                line_accepted.append(line)
                string_tags = match.group('string_tags')
                for tag in string_tags.split(','):
                    tag = tag.strip()
                    if tag not in tags:
                        tags.append(tag)

            else:
                line_refused.append(line)

        self.debug['line_refused'] = line_refused
        self.debug['line_accepted'] = line_accepted
        sorted(tags)
        self.result = tags
# okay decompiling ansible_web_service.cpython-37.pyc
