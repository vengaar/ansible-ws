import logging
import os
import importlib
import json
import hashlib
import time
from math import fabs

class ScriptWebServiceWrapper():

    def __init__(self, query_strings):
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
            self.output['usages'] = 'Missing query parameter'
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
            parameters['cache'] = self.query_strings.get('cache')
            self.logger.debug(parameters)
            if self._is_valid:
                PluginClass = getattr(importlib.import_module(f'sw2.{query}'), 'ScriptWrapperQuery')
                self.logger.debug(PluginClass)
                self.plugin = PluginClass(**parameters)
                self.logger.debug(self.plugin)
                if self.plugin.is_valid():
                    self.output['results'] = self.plugin.query()
                else:
                    self.output["usages"] = self.plugin.usages

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
        key = f'/tmp/.sw2.cache.{category}.{md5}'
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
            ttl = 180
            return cache_age < ttl
        else:
            return False

    def get_cached_resource(self, func):
        discrimimant = self.cache_config['discriminant']
        category = self.cache_config['category']
        cache_action = self.parameters.get('cache', 'read')
        self.cache_config['action'] = cache_action
        self.logger.debug(f'cache > get {cache_action} > {self.cache_config}')
        if cache_action == 'pass':
            data = func(discrimimant)
        else:
            key = self.__build_key_cache(discrimimant, category)
            if cache_action == 'flush':
                self.__cache_flush_data(key)
            if self.cache_is_valid(key):
                data = self.__cache_get_data(key)
                if data is None:
                    data = func(discrimimant)
            else:
                data = func(discrimimant)
                self.__cache_store_data(key, data)
        return data

    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parameters = kwargs
        self.logger.debug(self.parameters)
        self._is_valid = True
        if self.__doc__ is None:
            self.usages = ["No usages defines"]
        else:
            self.usages = self.__doc__.split(os.linesep)

    def is_valid(self):
        return self._is_valid

    def format_to_semantic_ui_dropdown(self, values):
        return [
            dict(name=value, value=value)
            for value in values
        ]