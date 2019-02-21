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

    def test_tags(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/notags.yml')
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
        expected = []
        self.assertEqual(response['results'], expected)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
