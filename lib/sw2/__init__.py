import logging
import os
import importlib
import json
import hashlib
import time
import glob
import urllib
import re


class ScriptWebServiceWrapper():

    def get_usage(self):
        modules = [
            os.path.splitext(file)[0]
            for file in os.listdir(os.path.dirname(__file__))
            if not os.path.basename(file).startswith('__')
        ]
        usage = dict(
            error=f'query parameter is missing. The available queries are {sorted(modules)}',
            usage='/sw2/query?query={query}&{query_parameters}',
            help=[
                'To have the detail of each query, call a query with parameter help',
                'example: /sw2/query?query=run&help=true'
            ]
        )
        return usage

    def __init__(self, query_strings, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.query_strings = query_strings
        self.mode_debug = query_strings.get('debug', 'false') == 'true'
        self.debug = dict()
        self.meta = dict(
            query_string=self.query_strings,
        )
        self.output = dict()
        self._is_valid = True
        if self.mode_debug:
            self.output['debug'] = self.debug
            self.output['meta'] = self.meta

        if 'query' not in self.query_strings:
            self._is_valid = False
            self.output['usages'] = self.get_usage()
        else:
            parameters = {}
            query = self.query_strings.get('query')
            self.logger.debug(query)
            if 'parameters' in self.query_strings:
                s_parameters = self.query_strings.get('parameters')
                self.logger.debug(s_parameters)
                try :
                    parameters = json.loads(s_parameters)
                except Exception as e:
                    self.logger.error(f'Fail to load parameters for {query}')
                    self.logger.error(str(e))
                    self._is_valid = False
                    self.output['usages'] = 'Parameter parameters must be a valid JSON'
            query_strings.update(parameters)
            self.logger.debug(query_strings)
            if self._is_valid:
                PluginClass = getattr(importlib.import_module(f'sw2.{query}'), 'ScriptWrapperQuery')
                self.logger.debug(PluginClass)
                self.plugin = PluginClass(config, **query_strings)
                self.logger.debug(self.plugin)
                if 'help' in query_strings:
                    self.output["usages"] = self.plugin.usages
                elif self.plugin.is_valid() :
                    self.output['results'] = self.plugin.query()
                else:
                    self.output["usages"] = self.plugin.usages
                    self.output["errors"] = self.plugin.errors

    def is_valid(self):
        return self._is_valid and self.plugin.is_valid()

    def get_result(self):
        return self.output


class ScriptWrapper():
    """
        No usage defined
    """

    def __build_key_cache(self, discriminant, category):
        id = str(discriminant).encode('utf-8')
        md5 = hashlib.md5(id).hexdigest()
        key = f'{self.cache_prefix}{category}.{md5}'
        return key

    def __cache_get_data(self, key):
        try:
            with open(key) as stream:
                data = stream.read()
            result = json.loads(data)
        except Exception as e:
            logger.error(f'Failed to get cache {key}')
            logger.error(str(e))
        return result['data']

    def __cache_store_data(self, key, data):
        self.logger.info(f'cache > store : {key}')
        to_cache = {
            'metadata': self.cache_config,
            'data': data
        }
        try:
            with open(key, 'w') as stream:
                json.dump(to_cache, stream)
        except Exception as e:
            logger.error(f'Failed to write cache {key}')
            logger.error(str(e))

    def __cache_flush_data(self, key):
        self.logger.info(f'cache > flush : {key}')
        if os.path.isfile(key):
            try:
                os.remove(key)
            except Exception as e:
                logger.error(f'Failed to flush cache {key}')
                logger.error(str(e))

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            cache_stat = os.stat(key)
            cache_age = time.time() - cache_stat.st_mtime
            return cache_age < self.cache_ttl
        else:
            return False

    def get_cached_resource(self, func):
        discrimimant = self.cache_config['discriminant']
        category = self.cache_config['category']
        cache_action = self.parameters.get('cache', 'read')
        self.cache_config['action'] = cache_action
        self.logger.debug(f'cache > get {cache_action} > {self.cache_config}')
        if cache_action == 'bypass':
            data = func(discrimimant)
        else:
            key = self.__build_key_cache(discrimimant, category)
            if cache_action == 'refresh':
                self.__cache_flush_data(key)
            if self.cache_is_valid(key):
                data = self.__cache_get_data(key)
                if data is None:
                    data = func(discrimimant)
            else:
                data = func(discrimimant)
                self.__cache_store_data(key, data)
        return data

    def __init__(self, config, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.cache_prefix = self.config.get('cache.prefix')
        self.cache_ttl = self.config.get('cache.ttl')
        self.parameters = kwargs
        self.logger.debug(self.parameters)
        self._is_valid = True
        self.parameters_description = dict()
        self.examples = []
        self.errors = []
        self.query_name = self.parameters['query']

    def add_example(self, description, parameters):
        qs = urllib.parse.urlencode(parameters)
        self.examples.append({
            'parameters': parameters,
            'desc': description.format(**parameters),
            'url': f'/sw2/query?query={self.query_name}&{qs}'
        })

    @property
    def usages(self):
        usages = {
            'parameters': self.parameters_description,
            'examples': self.examples
        }
        if self.__doc__ is None:
            usages['description'] = ["No usages defines"]
        else:
            usages['description'] = self.__doc__.split(os.linesep),
        return usages

    def get(self, name):
        return self.parameters[name]

    def check_parameters(self):
        """
        """
        for name, parameter in self.parameters_description.items():
            if parameter.get('required', False):
                if name not in self.parameters:
                    self._is_valid = False
                    self.errors.append(f'Required parameter {name} is missing')
            if 'values' in parameter:
                if name in self.parameters:
                    values = parameter['values']
                    if self.parameters[name] not in values:
                        self._is_valid = False
                        self.errors.append(f'The value of {name} is not in expected values {values}')
            if 'regex' in parameter:
                if name in self.parameters:
                    regex = parameter['regex']
                    value = self.parameters[name]
                    re.match(regex, value)
                    if re.match(regex, value) is None:
                        self._is_valid = False
                        self.errors.append(f"The command line [{value}] don't match expected regex {regex}")

    def is_valid(self):
        return self._is_valid

    def format_to_semantic_ui_dropdown(self, values):
        return [
            dict(name=value, value=value)
            for value in values
        ]
