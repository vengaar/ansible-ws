"""
"""
import logging
import subprocess
import json
import re

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Below expected parameters
[required,string] pattern, the pattern of groups name to search.
[optional,list] sources, the inventory files to used."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'pattern' not in self.parameters:
            self._is_valid = False

    def query(self):
        """
        """
        sources = self.parameters.get('sources', [])
        self.cache_config = {
            'discriminant': sources,
            'category': 'inventory'
        }
        inventory = self.get_cached_resource(self.get_inventory)
        groups = inventory['groups']
        pattern = self.parameters['pattern']
        re_pattern = re.compile(pattern)
        selected_groups = dict(
            (group_name, sorted(groups[group_name]))
            for group_name in groups.keys()
            if re.match(re_pattern, group_name) is not None
        )
        disabled = self.parameters.get('groups_selection', 'no')
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
            'ansible',
            '-m',
            'debug',
            '-a',
            'var=groups',
            'localhost',
        ]
        for source in sources:
            command.append('-i')
            command.append(source)
        self.logger.debug(f'get groups command {command}')
        p = subprocess.run(command, stdout=subprocess.PIPE)
        out = p.stdout.decode('utf-8')
        lines = out.splitlines()
        lines[0] = '{'
        inventory = json.loads(''.join(lines))
        self.logger.debug(inventory)
        return inventory
