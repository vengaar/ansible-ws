import logging
import os
import unittest
import pprint
import json
import sys
sys.path.append('.')
import tests
from sw2 import ScriptWebServiceWrapper


class TestSWSW(unittest.TestCase):

    def test_demo(self):
        parameters = {
            'demo1': 'value1',
            'demo2': ['foo', 'bar']
        }
        json_parameters = json.dumps(parameters)
        print(json_parameters)
        request = dict(
            debug='true',
            query='demo',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request)
        response = sw2.get_result()
        pprint.pprint(response)
        self.assertEqual(response['results'][5]['name'], 'foo')

    def test_groups(self):
        parameters = {
            'pattern': '.*prod',
            'sources': [
                '~/ansible-ws/tests/data/inventories/hosts_database',
                '~/ansible-ws/tests/data/inventories/hosts_webserver',
            ]
        }
        json_parameters = json.dumps(parameters)
        print(json_parameters)
        request = dict(
            debug='true',
            query='groups',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request)
        response = sw2.get_result()
        pprint.pprint(response)

    def test_tags(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/tags.yml')
        parameters = {
            'playbook': playbook,
        }
        json_parameters = json.dumps(parameters)
        print(json_parameters)
        request = dict(
            debug='true',
            query='tags',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request)
        response = sw2.get_result()
        pprint.pprint(response)
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
        print(json_parameters)
        request = dict(
            debug='true',
            cache='flush',
            query='tasks',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request)
        response = sw2.get_result()
        pprint.pprint(response)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
