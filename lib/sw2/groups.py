"""
"""
import logging
import subprocess
import json
import re

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on [ansible-inventory --list] to get groups.
The groups are cached.
The output is formmated for semantic ui dropdown"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.default_groups_selection = 'no'
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'pattern': {
                'description': 'The pattern of groups name to search',
                'required': True,
            },
            'sources': {
                'description': 'The inventory files to used',
                'required': False,
                'format': 'List of inventories separated by coma'
            },
            'groups_selection': {
                'description': 'The inventory files to used',
                'required': False,
                'default': self.default_groups_selection,
                'values': ['no', 'yes'],
            },
        }
        parameters = {
            'pattern': '.*database',
            'sources': '~/ansible-ws/tests/data/inventories/hosts_database',
        }
        self.add_example('To get hosts in group.s matching regex {pattern}', parameters)

    def query(self):
        """
        """
        sources = self.get('sources')
        self.cache_config = {
            'discriminant': sources,
            'category': 'inventory'
        }
        groups = self.get_cached_resource(self.get_inventory)
        pattern = self.get('pattern')
        if pattern == 'all':
            pattern = ".*"
        re_pattern = re.compile(pattern)
        selected_groups = {
            group_name: sorted(groups[group_name]['hosts'])
            for group_name in groups.keys()
            if re.match(re_pattern, group_name) is not None
        }
        disabled = self.get('groups_selection') == 'no'
        response = []
        for name, hosts in selected_groups.items():
            group = dict(name=f'<i class="orange sitemap icon"></i> {name}', value=name, disabled=disabled)
            response.append(group)
            response += [
                dict(name=f'<i class="hdd icon"></i> {host}', value=host)
                for host in hosts
            ]
        return response

    def get_inventory(self, sources):
        command = [
            'ansible-inventory',
            '--list',
        ]
        if sources is not None:
            for source in sources:
                command.append('-i')
                command.append(source)
        self.logger.debug(f'get groups command {command}')
        p = subprocess.run(command, stdout=subprocess.PIPE)
        out = p.stdout.decode('utf-8')
        inventory = json.loads(out)
        inventory.pop('_meta')
        inventory.pop('all')
        return inventory
