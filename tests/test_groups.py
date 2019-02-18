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
    parameters = {
        'sources': [
            '~/ansible-ws/tests/data/inventories/hosts_database',
            '~/ansible-ws/tests/data/inventories/hosts_webserver',
        ]
    }
    json_parameters = json.dumps(parameters)

    def test_groups_pattern(self):
        request = dict(
            debug='true',
            query='groups',
            pattern='.*database',
            parameters=self.json_parameters
        )
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
        request = dict(
            debug='true',
            query='groups',
            pattern='(database_app1_dev|database_app2_prod)',
            groups_selection='yes',
            parameters=self.json_parameters
        )
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
