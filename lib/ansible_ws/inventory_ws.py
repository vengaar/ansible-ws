"""
"""

import  re, ansible
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
        self.result = response
