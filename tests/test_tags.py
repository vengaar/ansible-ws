import logging
import unittest
import pprint
import os

import sys
sys.path.append('.')
import tests
from ansible_ws import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestSWSW(unittest.TestCase):

    config = AnsibleWebServiceConfig()

    def test_tags(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/tags.yml')
        parameters = {
            'playbook': playbook,
        }
        request = tests.get_sw2_request('tags', parameters, cache='refresh')
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = [
            {'name': value, 'value': value}
            for value in ['tag1', 'tag2', 'tag22', 'tag3']
        ]
        self.assertEqual(response['results'], expected)

        # with cache
        request['sw2'].pop('cache')
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
        self.assertEqual(response['results'], expected)

    def test_no_tags(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/notags.yml')
        parameters = {
            'playbook': playbook,
        }
        request = tests.get_sw2_request('tags', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        expected = []
        self.assertEqual(response['results'], expected)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
