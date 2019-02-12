import logging
import os
import yaml
import json
import hashlib
import time
import functools

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
    if 'help' in qs:
        validation = False

    return (validation, parameters)


def json_file_cache(func):
    #print(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        """
        #print(args, kwargs)
        self = args[0]
        discrimimant = args[1]
        if self.use_cache():
            self.logger.debug(f'discrimimant for cache={discrimimant}')
            key = self.cache_get_key(discrimimant)
            cache_action = self.get_param('cache')
            if cache_action == 'flush':
                self.cache_flush_data(key)
            if self.cache_is_valid(key):
                result = self.cache_get_data(key)
                if result is None:
                    result = func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                self.cache_store_data(key, result)
        else:
            result = func(*args, **kwargs)
        return result

    return wrapper


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
            value = value[key]
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



#############
### CACHE ###
#############

    def use_cache(self):
        cache_config = self.config.get('cache')
        cache_action = self.get_param('cache')
        use_cache = cache_config is not None and cache_action in ('use', 'flush')
        self.logger.debug(f'use_cache {use_cache} -> {cache_action}, {cache_config}')
        return use_cache

    def cache_get_key(self, discriminant):
        id = str(discriminant).encode('utf-8')
        md5 = hashlib.md5(id).hexdigest()
        key = f'/tmp/.ansible-ws.cache.{md5}'
        return key

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            cache_stat = os.stat(key)
            cache_age = time.time() - cache_stat.st_mtime
            ttl = 60
            return cache_age < ttl
        else:
            return False

    def cache_get_data(self, key):
        try:
            with open(key) as stream:
                data = stream.read()
            result = json.loads(data)
        except Exception as e:
            logger.error(f'Failed to get cache {key}')
            logger.error(str(e))
        return result

    def cache_store_data(self, key, data):
        self.logger.info(f'cache > store : {key}')
        try:
            with open(key, 'w') as stream:
                json.dump(data, stream)
        except Exception as e:
            logger.error(f'Failed to write cache {key}')
            logger.error(str(e))

    def cache_flush_data(self, key):
        self.logger.info(f'cache > flush : {key}')
        if os.path.isfile(key):
            try:
                os.remove(key)
            except Exception as e:
                logger.error(f'Failed to flush cache {key}')
                logger.error(str(e))


