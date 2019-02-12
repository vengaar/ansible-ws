"""
"""
import os
import json
import yaml
import re
import subprocess

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService, json_file_cache

class AnsibleWebServiceHosts(AnsibleWebService):
    """
    """

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    @json_file_cache
    def get_groups(self, sources):
        """
        """
        command = [
            'ansible',
            '-m',
            'debug',
            '-a',
            'var=groups',
            'localhost',
        ]
        if len(sources) > 0:
            inventories = []
            for source in sources:
                inventories.append('-i')
                inventories.append(source)
            command.extend(inventories)
        self.logger.debug(f'get groups command {command}')
        p = subprocess.run(command, stdout=subprocess.PIPE)
        out = p.stdout.decode('utf-8')
        lines = out.splitlines()
        lines[0] = '{'
        inventory = json.loads(''.join(lines))
        groups = inventory['groups']
        self.logger.debug(groups)
        return groups

    def use_cache(self):
        return True

    def run(self):
        
        sources = self.parameters['sources']
        groups = self.get_groups(sources)
        param_groups = self.get_param('groups')
        pattern = re.compile(param_groups)
        response = dict(
            (group_name, sorted(groups[group_name]))
            for group_name in groups.keys()
            if re.match(pattern, group_name) is not None
        )
        return response

class AnsibleWebServiceGroupVars(AnsibleWebService):
    """
    """
    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        group = self.get_param('group')
        key = self.get_param('key')
        inventory_raw = self.get_param('inventory')
        inventory = os.path.expanduser(inventory_raw)
        self.logger.error(inventory)

        if os.path.isdir(inventory):
            group_path = os.path.join(inventory, 'group_vars', group)
        else:
            group_path = os.path.join(os.path.dirname(inventory), 'group_vars', group)

        expected_files = [
            f'{group_path}{ext}'
            for ext in ('', '.yml', '.yaml', '.json')
        ]
        self.logger.debug(expected_files)

        for path in expected_files:
            if os.path.isfile(path):
                self.logger.debug(f'read group vars {path}')
                try:
                    with open(path) as stream:
                        data = yaml.load(stream)
                except yaml.parser.ParserError:
                    try:
                        with open(path, 'r') as stream:
                            data = json.loads(stream.read())
                    except json.decoder.JSONDecodeError as e:
                        data = dict()
                        self.logger.error(e)
                break

        for sub_key in key.split('.'):
            data = data[sub_key]

        return sorted(data.keys()) if isinstance(data, dict) else data

