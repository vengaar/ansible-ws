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

    def get_usages(self):
        data = {
            'sw2': {
                'query': f'The query todo // A value in {self.queries}',
                'debug': 'true/false // To add debug information in response',
                'cache': 'The cache action todo // See each query to now cache policy',
                'help': 'true/false // The display help',
            },
            'parameters': 'A dict with query parameters // See each query for details'
        }
        json.dumps(data)
        examples = [
            {
                'desc': 'Ask help for query tasks',
                'data': {
                    'sw2': {
                        'query': 'tasks',
                        'help': True
                    },
                }
            }
        ]
        usages = {
            'usages': 'provide to /sw2/query? with json data',
            'data': data,
            'examples': examples,
        }
        return usages

    def __init__(self, request, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(request)
        self.debug = dict()
        self.meta = dict(
            request=request,
        )
        self.errors = []
        self.output = dict()
        self._is_valid = True
        if 'parameters' not in request:
            request['parameters'] = {}
        if 'sw2' not in request:
            self._is_valid = False
            self.errors.append('No sw2 description found')
        sw2 = request.get('sw2', {})
        self.logger.debug(sw2)
        self.mode_debug = sw2.get('debug', 'false') == 'true'
        if self.mode_debug:
            self.output['debug'] = self.debug
            self.output['meta'] = self.meta
        query = sw2.get('query')
        
        self.queries = sorted([
            os.path.splitext(file)[0]
            for file in os.listdir(os.path.dirname(__file__))
            if not os.path.basename(file).startswith('__')
        ])
        
        if query not in self.queries: 
            self._is_valid = False
            self.errors.append(f'Unexpected sw2 query. {query} not in {self.queries}')

        if not self._is_valid:
            self.output['usages'] = self.get_usages()
            self.output["errors"] = self.errors
        else:
            query = sw2.get('query')
            self.logger.debug(query)
            PluginClass = getattr(importlib.import_module(f'sw2.{query}'), 'ScriptWrapperQuery')
            self.logger.debug(PluginClass)
            self.plugin = PluginClass(config, **request)
            self.logger.debug(self.plugin)
            if 'help' in sw2:
                self.output["usages"] = self.plugin.usages
            elif self.plugin.is_valid() :
                self.output['results'] = self.plugin.query()
            else:
                self.output["usages"] = self.plugin.usages
                self.output["errors"] = self.plugin.errors

    def get_result(self):
        return self.output

    def is_valid(self):
        return self._is_valid and self.plugin.is_valid()

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

    def cache_is_valid(self, key, cache_ttl):
        if os.path.isfile(key):
            cache_stat = os.stat(key)
            cache_age = time.time() - cache_stat.st_mtime
            if cache_ttl is not None:
                ttl = min(cache_ttl, self.cache_confing_ttl)
            else:
                ttl = self.cache_confing_ttl
            self.logger.debug(f'cache_age={cache_age}')
            return cache_age < ttl
        else:
            return False

    def _cache_is_valid_mtime(self, key, cache_ttl):
        if os.path.isfile(key):
            stat_cache = os.stat(key)
            stat_playbook = os.stat(self.playbook)
            cache_more_recent = stat_cache.st_mtime > stat_playbook.st_mtime
            if cache_ttl is None:
                return cache_more_recent
            else:
                cache_age = time.time() - stat_cache.st_mtime
            return cache_more_recent and (cache_age < cache_ttl)
        else:
            return False

    def get_cached_resource(self, func):
        discrimimant = self.cache_config['discriminant']
        category = self.cache_config['category']
        cache_action = self.sw2.get('cache', 'read')
        cache_ttl = self.sw2.get('cache_ttl')
        self.cache_config['action'] = cache_action
        self.logger.debug(f'cache > {cache_action} > {self.cache_config}')
        if cache_action == 'bypass':
            data = func(discrimimant)
        else:
            key = self.__build_key_cache(discrimimant, category)
            self.logger.debug(f'cache > key {key}')
            if cache_action == 'refresh':
                self.__cache_flush_data(key)
            if self.cache_is_valid(key, cache_ttl):
                data = self.__cache_get_data(key)
                if data is None:
                    data = func(discrimimant)
            else:
                data = func(discrimimant)
                self.__cache_store_data(key, data)
        return data

    def __init__(self, config, **request):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.cache_prefix = self.config.get('cache.prefix')
        self.cache_confing_ttl = self.config.get('cache.ttl')
        self.sw2 = request['sw2']
        self.query_name = self.sw2['query']
        self._parameters = request['parameters']
        self.logger.debug(self._parameters)
        self._is_valid = True
        self.parameters_description = dict()
        self.examples = []
        self.errors = []

    def add_example(self, description, parameters={}):
        data = {
            'sw2': {
                'query': self.query_name
            },
            'parameters': parameters
        }
        json.dumps(data)
        self.examples.append({
            'desc': description.format(**parameters),
            'url': '/sw2/query?{data}',
            'data': data,
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
            usages['description'] = self.__doc__.split(os.linesep)
        return usages

    def get(self, name):
        default = self.parameters_description[name].get('default')
        return self._parameters.get(name, default)

    def check_parameters(self):
        """
        """
        for name, parameter in self.parameters_description.items():
            if parameter.get('required', False):
                if name not in self._parameters:
                    self._is_valid = False
                    self.errors.append(f'Required parameter {name} is missing')
            if 'values' in parameter:
                if name in self._parameters:
                    values = parameter['values']
                    if self._parameters[name] not in values:
                        self._is_valid = False
                        self.errors.append(f'The value of {name} is not in expected values {values}')
            if 'regex' in parameter:
                if name in self._parameters:
                    regex = parameter['regex']
                    value = self._parameters[name]
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
