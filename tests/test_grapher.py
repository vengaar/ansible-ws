import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.grapher import AnsibleWebServiceInvnetoryGrapher

class TestGrapher(unittest.TestCase):

    sources = [
        os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts')
    ]
    config_file = '/etc/ansible-ws/inventory_grapher.yml'
    query_strings = dict(
        target=['server_prod_11'],
        inventory=[os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts')]
    )
    service = AnsibleWebServiceInvnetoryGrapher(config_file, query_strings)
    print(service.parameters)
    data = service.get_result()
    pprint.pprint(data)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
