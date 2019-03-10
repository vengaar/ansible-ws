"""
"""
import os
from . import ScriptWrapper
from ansible_ws.launch import PlaybookContextLaunch


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper launch playbook"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()
        if self._is_valid:
            _playbook = self.get('playbook')
            playbook = os.path.expanduser(_playbook)
            self._parameters['playbook'] = playbook
            if not os.path.isfile(playbook):
                self._is_valid = False
                self.errors.append(f'{playbook} is not a valid file')
            

    def __usages(self):
        self.parameters_description = {
            'cmdline': {
                'description': 'The command line to use to launch a playbook.',
                'required': True,
                'regex': '^ansible-playbook.*',
            },
            'playbook': {
                'description': 'The path of playbook to launch.',
                'required': True,
            },
        }
        parameters = {
            'cmdline': 'ansible-playbook ~/ansible-ws/tests/data/playbooks/tags.yml',
            'playbook': '~/ansible-ws/tests/data/playbooks/tags.yml',
        }
        self.add_example('To launch {cmdline}', parameters)

    def query(self):
        self._parameters['ansible_ws_config'] = self.config
        pcl = PlaybookContextLaunch(**self._parameters)
        pcl.launch()
        return pcl.status
