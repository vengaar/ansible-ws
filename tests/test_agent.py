import logging
import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests
import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
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

    def test_sw2(self):
        id = 'ansible-ws-unittest'

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

        # ALL
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
        self.assertEqual(response['results']['keys'], [])
        self.assertEqual(response['results']['action'], 'kill')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
