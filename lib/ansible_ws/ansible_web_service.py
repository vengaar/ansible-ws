import logging
import os
import yaml
import json


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


class AnsibleWebServiceConfig(object):

    CONFIG_FILE = '/etc/ansible-ws/ansible-ws.yml'

    def __init__(self, config_file=CONFIG_FILE):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            with open(self.CONFIG_FILE) as configfile:
                self.config = yaml.load(configfile)
                self.logger.debug(self.config)
                self.logger.info(f'Configuration file {self.CONFIG_FILE} LOADED')
        except Exception:
            self.logger.error(f'Not possible to load configuration file {self.CONFIG_FILE}')

    def get(self, keys):
        value = self.config
        for key in keys.split('.'):
            value= value[key]
        return value

class AnsibleWebService(object):
    """
    """
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
          query_string=self.query_strings,
          parameters=self.parameters,
          parameters_valid=self.parameters_valid
        )

        if self.parameters_valid:
          cache = self.config.get('cache')
          if cache:
              resource = self.get_param(cache['resource'])
              type = cache['type']
              self.result = self.get_result_from_cache(type, resource)
          else:
              self.result = self.run()

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

    def get_result_from_cache(self, type, resource):
        """
        """
        self.logger.info(f'Try using cache for {type} on {resource}')
        
        def update_cache(cache_path):
            self.run()
            self.logger.info(f'Write cache {cache_path}')
            with open(cache_path, 'w') as stream:
                json.dump(self.result, stream)
            return self.result

        self.logger.debug(f'resource={resource}')
        resource_name = os.path.basename(resource)
        self.logger.debug(f'resource_name={resource_name}')
        dir = os.path.dirname(resource)
        cache_filename = f'.cached.{type}.{resource_name}'
        cache_path = os.path.join(dir, cache_filename)
        print(f'cache_path={cache_path}')
        if os.path.isfile(cache_path):
            self.logger.info(f'Cache found {cache_path}')
            stat_cache = os.stat(cache_path)
            stat_resource = os.stat(resource)
            if stat_cache.st_mtime > stat_resource.st_mtime:
                self.logger.info('Cache younger than resource -> use cache')
                try:
                    with open(cache_path) as stream:
                        data = stream.read()
                    result = json.loads(data)
                except Exception as e:
                    self.logger.error(f'Failed to read cache {cache_path}')
                    self.logger.error(str(e))
                    result = update_cache(cache_path)
            else:
                self.logger.info('Cache older than resource -> update cache')
                result = update_cache(cache_path)
        else:
            self.logger.info(f'Cache not found {cache_path}')
            result = update_cache(cache_path)
        return result

















