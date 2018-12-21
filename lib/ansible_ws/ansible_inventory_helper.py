import pprint
import re

import ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

TYPE_LIST = "list"
TYPE_REGEX = "regex"

def request_ansible_inventory(query, type, sources):

    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=sources)
    groups_dict = inventory.get_groups_dict()

    if type == TYPE_LIST:
        response = dict(
            (group_name, groups_dict[group_name])
            for group_name in inventory.groups
            if group_name in query
        )
    else:
        response = dict(
            (group_name, groups_dict[group_name])
            for group_name in inventory.groups
            if re.match(query, group_name)
        )
    return response
