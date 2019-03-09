import logging
import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestRuns(unittest.TestCase):

    RUNS_DIR = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'runs')
    ansible_ws_config = AnsibleWebServiceConfig()

    def test_search_basic(self):
        self.ansible_ws_config.config['ansible']['runs_dir'] = self.RUNS_DIR
        request = {
            'debug': 'true',
            'query': 'runs',
            'from': 'January 1, 2019',
        }
        sw2 = ScriptWebServiceWrapper(request, self.ansible_ws_config)
        response = sw2.get_result()
#         pprint.pprint(response)
#         print(len(response['results']))
        self.assertEqual(len(response['results']), 6)

    def test_search_state(self):
        self.ansible_ws_config.config['ansible']['runs_dir'] = self.RUNS_DIR
        request = {
            'debug': 'true',
            'query': 'runs',
            'from': 'January 1, 2019',
            'states': 'failed'
        }
        sw2 = ScriptWebServiceWrapper(request, self.ansible_ws_config)
        response = sw2.get_result()
#         pprint.pprint(response)
#         print(len(response['results']))
        self.assertEqual(response['results'][0]['runid'], 'f14529a2-cd83-4d2c-b885-a6184b83f7bc')
        self.assertEqual(response['results'][1]['runid'], 'f61aef56-9700-48a8-ab1e-f049df76ec0b')
        self.assertEqual(len(response['results']), 2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
