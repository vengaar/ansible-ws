import  re, ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService

class AnsibleWebServiceHosts(AnsibleWebService):
    TYPE_LIST = 'list'
    TYPE_REGEX = 'regex'

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        type = self.parameters['type']
        sources = self.parameters['sources']
        if type == self.TYPE_LIST:
            groups = self.query_strings.get('groups', None)
        else:
            if type == self.TYPE_REGEX:
                groups = self.query_strings.get('groups', [None])[0]
        loader = DataLoader()
        inventory = InventoryManager(loader=loader,
          sources=sources)
        groups_dict = inventory.get_groups_dict()
        if type == self.TYPE_LIST:
            response = dict(((group_name, groups_dict[group_name]) for group_name in inventory.groups if group_name in groups))
        else:
            pattern = re.compile(groups)
            response = dict(((group_name, groups_dict[group_name]) for group_name in inventory.groups if re.match(pattern, group_name)))
        self.result = response
