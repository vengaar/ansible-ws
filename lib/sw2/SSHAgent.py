"""
"""
from . import ScriptWrapper
from ansible_ws.ssh_agent import SshAgent

class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on SSH agent to create it"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'id': {
                'description': 'The agent ID to use. Create the agent it is not present.',
                'required': True,
            }
        }
        parameters = {
            'id': 'ansible-ws-test',
        }
        self.add_example('To get info of ssh-agent {id}', parameters)

    def query(self):
        id = self.parameters.get('id')
        agent = SshAgent(id)
        response = {
           'agent': agent.env_agent,
           'keys': agent.keys,
           'action': 'init',
        }
        return response
