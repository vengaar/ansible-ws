"""
"""
import subprocess

from . import ScriptWrapper
from sys import stderr


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on 'ansible -m setup {host} to update facts."""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'host': {
                'description': 'The target host for setup module',
                'required': True,
            },
            'inventories': {
                'description': 'The list inventories to used'
            }
        }
        parameters = {'host': 'db_prod_11'}
        self.add_example('To update facts of {host}', parameters)

    def query(self):
        """
        """
        host = self.get('host')
        command = ['ansible', '-m', 'setup', host]
        inventories = self.get('inventories')
        if inventories is not None:
            for inventory in inventories:
               command.append('-i') 
               command.append(inventory) 
        self.logger.debug(' '.join(command))
        p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.check_returncode()
        return {
            'returncode': p.returncode,
            'stderr': p.stderr.decode('utf-8'),
        }