import os
import unittest
import pprint

import  re, ansible
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.helpers import get_group_vars

ANSIBLE_WS_PATH_TEST = os.path.dirname(os.path.realpath(__file__))
sources = [
    os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_database'),
    os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts_webserver')
]

loader = DataLoader()
inventory = InventoryManager(
    loader=loader,
    sources=sources
)
inventory.reconcile_inventory()
# inventory.reconcile_inventory()
# variable_manager = VariableManager()
# variable_manager.set_inventory(inventory)


#pprint.pprint(dir(inventory))
pprint.pprint(inventory.list_groups())
pprint.pprint(inventory.groups)

for group_name in inventory.groups:
    group = inventory.groups[group_name]
    print(type(group))
    print( group.get_vars() )

groups_dict = inventory.get_groups_dict()
pprint.pprint(groups_dict)

inventory_asg_groups = filter(lambda g: 'database' in g, inventory.groups)

print(get_group_vars(inventory.groups.values()))

#pprint.pprint(inventory.get_vars())