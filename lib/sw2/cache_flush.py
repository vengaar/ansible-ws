"""
"""
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Flush cache file according to the provided key
See query cache_info to get existing keys"""

    def __init__(self, config, **kwargs):
        
        super().__init__(config, **kwargs)
        self.name = 'cache_flush'
        self.__usages()
        self._is_valid = ('key' in self.parameters)
        if self._is_valid:
            self.cache_file = self.parameters.get('key')

    def __usages(self):
        self.parameters_description = {
            'key': {
                'description': 'The key of the cache to flush',
                'required': True,
            },
        }
        key = '/tmp/.sw2.cache.export.6adf97f83acf6453d4a6a4b1070f3754'
        self.examples.append({
            'desc': f'To flush the cache {key}',
            'url': f'/sw2/query?query={self.name}&key={key}'
        })

    def query(self):
        assert(self.cache_file.startswith(self.cache_prefix))
        assert(os.path.isfile(self.cache_file))
        os.remove(self.cache_file)
        return f'Cache file {self.cache_file} successfully flushed'

