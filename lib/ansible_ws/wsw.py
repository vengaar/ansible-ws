"""
@test
"""
import importlib
import json

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService

class WebServiceWrapper(AnsibleWebService):
    """
    """
    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        query = self.get_param('query')
        s_parameters = self.query_strings.get('parameters')[0]
        print(s_parameters)
        try :
            parameters = json.loads(s_parameters)
        except Exception as e:
            self.logger.error(f'Fail to load parameters for {query}')
            self.logger.error(str(e))
            parameters = {}
        print(parameters)
        plugin = importlib.import_module(f'wsw_plugins.{query}')
        response=  plugin.query(**parameters)
        return response
