"""
"""
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.cache_file = self.parameters.get('key')

    def query(self):
        assert(self.cache_file.startswith(self.cache_prefix))
        assert(os.path.isfile(self.cache_file))
        os.remove(self.cache_file)
        return f'Cache file {self.cache_file} successfully flushed'

