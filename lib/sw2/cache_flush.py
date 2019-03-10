"""
"""
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Flush cache file according to the provided key
See query cache_info to get existing keys"""

    def __init__(self, config, **kwargs):

        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'key': {
                'description': 'The key of the cache to flush',
                'required': True,
            },
        }
        parameters = {
            'key': '/tmp/.sw2.cache.export.6adf97f83acf6453d4a6a4b1070f3754',
        }
        self.add_example('To flush the cache {key}', parameters)

    def query(self):
        cache_file = self.get('key')
        assert(cache_file.startswith(self.cache_prefix))
        assert(os.path.isfile(cache_file))
        os.remove(cache_file)
        return f'Cache file {cache_file} successfully flushed'

