"""
"""
import glob
import json

from . import ScriptWrapper
from symbol import except_clause


class ScriptWrapperQuery(ScriptWrapper):
    """To list all data in cache.
This query has no parameter."""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

    def query(self):
        response = []
        for file in sorted(glob.glob(f'{self.cache_prefix}*')):
            file_split = file.split('.')
            data = None
            try:
                with open(file, 'r') as stream:
                    cache = stream.read()
                    data = json.loads(cache)
                    metadata = data['metadata']
            except json.decoder.JSONDecodeError:
                self.logger.error(f'Invalid JSON for cache {file}')
                self.logger.error(data)
                metadata = {'error': 'INVALID CACHE FORMAT'}
            except Exception:
                self.logger.error(f'Unexpected error during cache read {file}')
            info = {
                'key': file,
                'metadata': metadata
            }
            response.append(info)
        return response

