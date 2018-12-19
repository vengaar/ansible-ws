import pprint
import re

import ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

def request_ansible_inventory(query, sources):

    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=sources)
    groups_dict = inventory.get_groups_dict()

    if ',' in query:
        response = dict(
            (group_name, groups_dict[group_name])
            for group_name in inventory.groups
            if group_name in query.split(',')
        )
    else:
        response = dict(
            (group_name, groups_dict[group_name])
            for group_name in inventory.groups
            if re.match(query, group_name)
        )
    return response
