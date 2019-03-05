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
    inventories = [
        os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_database'),
        os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_webserver')
    ]

    def test_list(self):
        request = {
            'debug': True,
            'query': 'groupvars',
            'group': 'database_app1_prod',
            'key': 'countries.list',
            'inventories': ','.join(self.inventories)
        }
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['fr', 'it', 'es']
        ]
        self.assertEqual(response['results'], expected)

    def test_json_parameters(self):
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
