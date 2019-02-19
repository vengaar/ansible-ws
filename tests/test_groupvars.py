import logging
import os
import unittest
import pprint
import json
import sys
sys.path.append('.')
import tests

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestSWSW(unittest.TestCase):

    config = AnsibleWebServiceConfig()

    def test_groupvars(self):
        parameters = {
            'group': 'database_app1_prod',
            'key': 'countries.dict',
            'inventories': [
                '~/ansible-ws/tests/data/inventories/hosts_database',
                '~/ansible-ws/tests/data/inventories/hosts_webserver',
            ]
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            query='groupvars',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['es', 'fr', 'it']
        ]
        self.assertEqual(response['results'], expected)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()