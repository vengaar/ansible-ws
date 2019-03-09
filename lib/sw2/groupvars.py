"""
"""
import os
import json
import subprocess

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on command [ansible-inventory --list --export] to get group variables.
The exported inventory is put in cache."""

    def __init__(self,config,  **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        required = set(['group', 'key'])
        self._is_valid = required.issubset(set(self.parameters.keys()))
        if self._is_valid:
            self.group = self.parameters.get('group')
            self.key = self.parameters.get('key')
            self.inventories = []
            if 'parameters' in self.parameters:
                self.inventories = self.parameters.get('inventories')
            else:
                inventories = self.parameters.get('inventories')
                if inventories is not None:
                    self.inventories = inventories.split(',')

    def __usages(self):
        self.parameters_description = {
            'group': {
                'description': 'The name of group to get var',
                'required': 'true',
            },
            'playbook': {
                'description': 'The keys to follow with dot notation',
                'required': 'true',
            },
            'inventories': {
                'description': 'The inventories files to used. If nothing is defined the default ansible inventories are used',
                'required': 'false',
                'format': 'List of inventory separated by coma'
            },
        }
        
        group = 'database_app1_prod'
        key = 'countries.list'
        inventories = '~/ansible-ws/tests/data/inventories/hosts_database'
        self.examples.append({
            'desc': f'The get list defined in the group {group} under the key {key} and defined in the inventories {inventories}',
            'url': f'/sw2/query?query=groupvars&group={group}&key={key}&inventories={inventories}'
        })

    def query(self):

        self.cache_config = {
            'discriminant': self.inventories,
            'category': 'export'
        }
        inventory = self.get_cached_resource(self.get_export)
        
        values = []
        if self.group in inventory:
            if 'vars' in inventory[self.group]:
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
