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
    query = 'groupvars'

    def test_list(self):
        parameters = {
            'group': 'database_app1_prod',
            'key': 'countries.list',
            'inventories': self.inventories
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['fr', 'it', 'es']
        ]
        self.assertEqual(response['results'], expected)

    def test_dict(self):
        parameters = {
            'group': 'database_app1_prod',
            'key': 'countries.dict',
            'inventories': self.inventories
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['es', 'fr', 'it']
        ]
        self.assertEqual(response['results'], expected)

    def test_default(self):
        parameters = {
            'group': 'foo',
            'key': 'foo.barr',
        }
        request = tests.get_sw2_request(self.query, parameters)
        pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
        pprint.pprint(response)
        expected = []
        self.assertEqual(response['results'], expected)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
