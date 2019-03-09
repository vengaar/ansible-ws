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
    sources = [
        os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_database'),
        os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_webserver'),
    ]
    query = 'groups'

    def test_default(self):
        parameters = {
            'pattern': 'all',
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertIsInstance(response['results'], list)

    def test_groups_pattern(self):
        parameters = {
            'pattern': 'database',
            'sources': self.sources
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        values = [
            option['value']
            for option in response['results']
        ]
        expected = [
            'database_app1_dev',
            'server_dev_x1',
            'server_dev_x2',
            'database_app1_prod',
            'db_prod_11',
            'db_prod_12',
            'db_prod_13',
            'database_app2_dev',
            'server_dev_x1',
            'server_dev_x2',
            'database_app2_prod',
            'db_prod_21',
            'db_prod_22',
            'db_prod_23',
        ]
#         pprint.pprint(values)
        self.assertEqual(values, expected)

    def test_groups_list(self):
        parameters = {
            'pattern': '(database_app1_dev|database_app2_prod)',
            'groups_selection': 'yes',
            'sources': self.sources
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        values = [
            option['value']
            for option in response['results']
        ]
        expected = [
            'database_app1_dev',
            'server_dev_x1',
            'server_dev_x2',
            'database_app2_prod',
            'db_prod_21',
            'db_prod_22',
            'db_prod_23',
        ]
#         pprint.pprint(values)
        self.assertEqual(values, expected)
        self.assertEqual(response['results'][0]['disabled'], 'yes')
        self.assertEqual(response['results'][3]['disabled'], 'yes')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
