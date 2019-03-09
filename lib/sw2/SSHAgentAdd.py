"""
"""
import os
from . import ScriptWrapper
from ansible_ws.ssh_agent import SshAgent

class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on SSH agent to add key"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'id': {
                'description': 'The agent ID',
                'required': True,
            },
            'private_key': {
                'description': 'The path of the private key to add',
                'required': True,
            },
            'passphrase': {
                'description': 'The passphrase to the private key',
                'required': True,
            },
        }
        parameters ={
            'id': 'ansible-ws-test',
            'action': 'add',
            'private_key': '~/ansible-ws/tests/data/agent/key1',
            'passphrase': 'key1'
        }
        self.add_example('To add {private_key} to ssh-agent {id}', parameters)

    def query(self):
        id = self.get('id')
        agent = SshAgent(id)
        _private_key = self.parameters.get('private_key')
        private_key = os.path.expanduser(_private_key)
        passphrase = self.parameters.get('passphrase')
        agent.load_key(private_key, passphrase)
        response = {
           'agent': agent.env_agent,
           'keys': agent.keys,
           'action': 'add',
        }
        return response
