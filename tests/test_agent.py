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

    key1 = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'key1')
    key2 = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'key2')

    def test(self):

      ssh_agent = SshAgent('ansible-ws-unittest')
#       pprint.pprint(ssh_agent.env)
      ssh_agent.load_key(self.key1, 'key1')
#       pprint.pprint(ssh_agent.keys)
      with open(f'{self.key1}.pub') as fstream:
        pub_key1 = fstream.read() 
#       pprint.pprint(expected_key)
      self.assertEqual(ssh_agent.keys, pub_key1)
      ssh_agent = SshAgent('ansible-ws-unittest')
      self.assertEqual(ssh_agent.keys, pub_key1)
      ssh_agent.load_key(self.key2, 'key2')
      with open(f'{self.key2}.pub') as fstream:
        pub_key2 = fstream.read()
#       pprint.pprint(ssh_agent.keys)
      self.assertIn(pub_key1, ssh_agent.keys)
      self.assertIn(pub_key2, ssh_agent.keys)
      ssh_agent.kill()

    def test_ws(self):
        config_file = '/etc/ansible-ws/ssh_agent_add.yml'
        query_strings = dict(
            action=['add'],
            private_key=[self.key1],
            passphrase=['key1'],
            id=['ansible-ws-unittest']
        )
        service = AnsibleWebServiceSshAgent(config_file, query_strings)
        response = service.get_result()
#         pprint.pprint(response)
        with open(f'{self.key1}.pub') as fstream:
            pub_key1 = fstream.read() 
        self.assertIn(pub_key1, response['results']['keys'])
        ssh_agent = SshAgent('ansible-ws-unittest')
        ssh_agent.kill()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
