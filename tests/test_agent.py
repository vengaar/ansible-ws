import logging
import unittest
import pprint
import os

import sys
sys.path.append('.')
import tests
from ansible_ws import AnsibleWebServiceConfig
from ansible_ws.ssh_agent import SshAgent
from sw2 import ScriptWebServiceWrapper


class TestSshAgent(unittest.TestCase):

    key1 = os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'key1')
    key2 = os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'agent', 'key2')
    config = AnsibleWebServiceConfig()

    def get_public_key(self, file):
        with open(f'{file}.pub') as fstream:
            raw = fstream.read()
        pub_key = raw.split(os.linesep)[0]
        return pub_key

    def test(self):
      ssh_agent = SshAgent('ansible-ws-unittest')
      ssh_auth_sock = ssh_agent.env["SSH_AUTH_SOCK"]
#       print(ssh_auth_sock)
      ssh_agent = SshAgent('ansible-ws-unittest')
      ssh_auth_sock2 = ssh_agent.env["SSH_AUTH_SOCK"]
#       print(ssh_auth_sock2)
      self.assertEqual(ssh_auth_sock, ssh_auth_sock2)
      rc, output = ssh_agent.kill()
      self.assertEqual(rc, 0)

      # sure to have new agent without key
      ssh_agent = SshAgent('ansible-ws-unittest')
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
      rc, output = ssh_agent.kill()
      self.assertEqual(rc, 0)

    def test_sw2(self):
        id = 'ansible-ws-unittest'

        # KILL
        parameters = {
            'id': id,
        }
        request = tests.get_sw2_request('SSHAgentKill', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results']['keys'], None)
        self.assertEqual(response['results']['action'], 'kill')
        self.assertEqual(response['results']['rc'], 0)

        # INFO
        parameters = {
            'id': id,
        }
        request = tests.get_sw2_request('SSHAgent', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results']['keys'], [])
        self.assertEqual(response['results']['action'], 'init')

        # ADD
        parameters = {
            'id': id,
            'private_key': self.key1,
            'passphrase': 'key1',
        }
        request = tests.get_sw2_request('SSHAgentAdd', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results']['action'], 'add')
        self.assertTrue(response['results']['keys'][0].startswith('ssh-rsa '))

        # KILL
        parameters = {
            'id': id,
        }
        request = tests.get_sw2_request('SSHAgentKill', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results']['keys'], None)
        self.assertEqual(response['results']['action'], 'kill')
        self.assertEqual(response['results']['rc'], 0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
