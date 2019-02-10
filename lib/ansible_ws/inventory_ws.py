"""
"""
import  os
import json, yaml
import re
import ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService

class AnsibleWebServiceHosts(AnsibleWebService):
    """
    """

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        sources = self.parameters['sources']
        loader = DataLoader()
        inventory = InventoryManager(
            loader=loader,
            sources=sources
        )
        groups_dict = inventory.get_groups_dict()
        groups = self.get_param('groups')
        pattern = re.compile(groups)
        response = dict(
            (group_name, sorted(groups_dict[group_name]))
            for group_name in inventory.groups
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

