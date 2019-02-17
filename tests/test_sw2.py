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

    def test_demo(self):
        parameters = {
            'demo1': 'value1',
            'demo2': ['foo', 'bar']
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            query='demo',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results'][5]['name'], 'foo')

    def test_groups(self):
        parameters = {
            'pattern': '.*database',
            'sources': [
                '~/ansible-ws/tests/data/inventories/hosts_database',
                '~/ansible-ws/tests/data/inventories/hosts_webserver',
            ]
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            query='groups',
            parameters=json_parameters
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
        
    def test_tags(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/tags.yml')
        parameters = {
            'playbook': playbook,
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            query='tags',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['tag1', 'tag2', 'tag22', 'tag3']
        ]
        self.assertEqual(response['results'], expected)

    def test_tasks(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/tags.yml')
        parameters = {
            'playbook': playbook,
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            cache='refresh',
            query='tasks',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in [
                'task11',
                'task12 with long name',
                'task13',
                'debug',
                'task21',
                'task22',
            ]
        ]
        self.assertEqual(response['results'], expected)

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
#     logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.ERROR)
    unittest.main()
