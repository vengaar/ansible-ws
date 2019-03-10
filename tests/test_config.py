import logging
import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig


class TestAnsibleWebServiceConfig(unittest.TestCase):

    def test(self):
        config = AnsibleWebServiceConfig()
#         print(config.get('runs_dir'))
#         print(config.get('ansible_cmd.playbook'))
        value = config.get('unittest.unittest.unittest')
        self.assertEqual(value, 'unittest')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
