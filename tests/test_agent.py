import logging
import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.ssh_agent import AnsibleWebServiceSshAgent, SshAgent

class TestSshAgent(unittest.TestCase):

    private_key = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'ansible-ws')
    public_key = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'ansible-ws.pub')

    def test(self):

      ssh_agent = SshAgent()
#       pprint.pprint(ssh_agent.env)
      ssh_agent.load_key(self.private_key, 'ansible-ws')
#       pprint.pprint(ssh_agent.keys)
      with open(self.public_key) as fstream:
        expected_key = fstream.read() 
#       pprint.pprint(expected_key)
      self.assertEqual(ssh_agent.keys, expected_key)
      ssh_agent = SshAgent()
      self.assertEqual(ssh_agent.keys, expected_key)
      ssh_agent.kill()

    def test_ws(self):
        config_file = '/etc/ansible-ws/ssh_agent.yml'
        query_strings = dict(
            action=['add'],
            private_key=[self.private_key],
            passphrase=['ansible-ws']
        )
        service = AnsibleWebServiceSshAgent(config_file, query_strings)
        response = service.get_result()
#         pprint.pprint(response)
        ssh_agent = SshAgent()
        ssh_agent.kill()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
