"""
"""
from . import ScriptWrapper
from ansible_ws.ssh_agent import SshAgent

class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper to kill a SSH agent"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'id': {
                'description': 'The agent ID to kill',
                'required': True,
            },
        }
        parameters ={
            'id': 'ansible-ws-test',
            'action': 'kill'
        }
        self.add_example('To kill ssh-agent {id}', parameters)

    def query(self):
        id = self.get('id')
        agent = SshAgent(id)
        agent.kill()
        response = {
           'agent': agent.env_agent,
           'keys': agent.keys,
           'action': 'kill',
        }
        return response
