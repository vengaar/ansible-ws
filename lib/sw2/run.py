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
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'runid': {
                'description': 'The runid to get',
                'required': True
            }
        }
        runid = 'f14529a2-cd83-4d2c-b885-a6184b83f7bc'
        parameters = {
            'runid': runid,
        }
        self.add_example('To get run {runid}', parameters)

    def query(self):
        """
        """
        runid = self.parameters.get('runid')
        pc = PlaybookContext(runid, self.config)
        response = dict(
            status=pc.status,
            output=pc.out
        )
        return response
