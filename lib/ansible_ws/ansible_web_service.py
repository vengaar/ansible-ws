import yaml, logging, re, subprocess, ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

def get_parameters(qs, config_parameters):
    validation = True
    parameters = dict()
    type = None
    for name, desc in config_parameters.items():
        # print(name, desc)
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
        # print(name, default, type)
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
        # print(name, value)

    return (validation, parameters)


class AnsibleWebService(object):

    def __init__(self, config_file, query_strings):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_file = config_file
        self.query_strings = query_strings
        try:
            with open(self.config_file) as (f):
                self.config = yaml.load(f)
                self.logger.info(f'Configuration file {self.config_file} LOADED')
        except Exception:
            self.logger.error(f'Not possible to load configuration file {config_file}')

        self.mode_debug = query_strings.get('debug', ['false'])[0] == 'true'
        parameters_valid, parameters = get_parameters(self.query_strings, self.config['parameters'])
        self.parameters = parameters
        self.parameters_valid = parameters_valid
        self.debug = dict()
        self.result = dict()
        self.meta = dict(
          config_file=self.config_file,
          config=self.config,
          query_stringq=self.query_strings,
          parameters=self.parameters,
          parameters_valid=self.parameters_valid
        )

        if self.parameters_valid:
          self.run()

    def get_param(self, name):
        return self.parameters.get(name)

    def run(self):
        pass

    def get_result(self):
        output = dict(results=self.result)
        if not self.parameters_valid or self.mode_debug:
          output['meta'] = self.meta
        if self.mode_debug:
            output['debug'] = self.debug
        return output
