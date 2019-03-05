"""
"""
import re
import os

from ansible_ws.launch import PlaybookContext
from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Return the run according to the runid provided"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.name = 'run'
        self.__usages()
        self._is_valid = ('runid' in self.parameters)

    def __usages(self):
        self.parameters_description = {
            'runid': {
                'description': 'The runid to get',
                'required': True
            }
        }
        runid = 'f14529a2-cd83-4d2c-b885-a6184b83f7bc'
        self.examples.append({
            'desc': f'To get run {runid}',
            'url': f'/sw2/query?query={self.name}&runid={runid}'
        })

    def query(self):
        """
        """
        runid = self.parameters.get('runid')
        pc = PlaybookContext(runid)
        response = dict(
            status=pc.status,
            output=pc.out
        )
        return response
