import logging
import unittest
import pprint
import os

import sys
sys.path.append('.')
import tests
from ansible_ws import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestTags(unittest.TestCase):

    config = AnsibleWebServiceConfig()

    def test_tasks(self):
        playbook = os.path.expanduser('~/ansible-ws/tests/data/playbooks/tags.yml')
        parameters = {
            'playbook': playbook,
        }
        request = tests.get_sw2_request('tasks', parameters)
#         pprint.pprint(request)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
