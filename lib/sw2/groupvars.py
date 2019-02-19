"""
"""
import os
import json
import subprocess

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Below expected parameters
[required,string] group, the name of group to get vars.
[required,string] key, the keys to follow with dot notation.
[optional,list] inventories, the inventories files to used."""

    def __init__(self,config,  **kwargs):
        super().__init__(config, **kwargs)
        required = set(['group', 'key'])
        if not required.issubset(set(self.parameters.keys())):
            self._is_valid = False
        self.group = self.parameters.get('group')
        self.key = self.parameters.get('key')
        self.inventories = self.parameters.get('inventories')

    def query(self):

        self.cache_config = {
            'discriminant': self.inventories,
            'category': 'export'
        }
        inventory = self.get_cached_resource(self.get_export)
        vars = inventory[self.group]['vars']

        for sub_key in self.key.split('.'):
            vars = vars[sub_key]

        values = sorted(vars.keys()) if isinstance(vars, dict) else vars
        response = self.format_to_semantic_ui_dropdown(values)
        return response

    def get_export(self, inventories):
        cmdline = [
            'ansible-inventory',
            '--list',
            '--export',
        ]
        if self.inventories is not None:
            for inventory in self.inventories:
                cmdline.append('-i')
                cmdline.append(inventory)
        self.logger.debug(cmdline)
        p = subprocess.run(cmdline, stdout=subprocess.PIPE)
        out = p.stdout.decode('utf-8')
        inventory = json.loads(out)
        return inventory
