import pprint
import re

import ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

def get_ansible_host_by_group(query, sources):

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

# if __name__ == '__main__':
#
#     sources = ['/etc/ansible/hosts']
#
#     query = 'database_app1_prod,database_app3_prod'
#     response = get_ansible_host_by_group(query, sources)
#     pprint.pprint(response)
#
#     query = '^database_.*_prod$'
#     response = get_ansible_host_by_group(query, sources)
#     pprint.pprint(response)
