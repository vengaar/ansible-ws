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

    def get_public_key(self, file):
        with open(f'{file}.pub') as fstream:
            raw = fstream.read()
        pub_key = raw.split(os.linesep)[0]
        return pub_key

    def test(self):

      ssh_agent = SshAgent('ansible-ws-unittest')
#       pprint.pprint(ssh_agent.env)
      ssh_agent.load_key(self.key1, 'key1')
#       pprint.pprint(ssh_agent.keys)
      pub_key1 = self.get_public_key(self.key1) 
#       pprint.pprint(pub_key1)
      self.assertEqual(len(ssh_agent.keys), 1)
      self.assertIn(pub_key1, ssh_agent.keys)
      ssh_agent = SshAgent('ansible-ws-unittest')
      self.assertEqual(len(ssh_agent.keys), 1)
      self.assertIn(pub_key1, ssh_agent.keys)
      ssh_agent.load_key(self.key2, 'key2')
      pub_key2 = self.get_public_key(self.key2)
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
        pub_key1 = self.get_public_key(self.key1)
        self.assertIn(pub_key1, response['results']['keys'])
        ssh_agent = SshAgent('ansible-ws-unittest')
        ssh_agent.kill()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
