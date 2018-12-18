import unittest
import pprint

import sys, os
ANSIBLE_WS_PATH_TEST = os.path.dirname(os.path.realpath(__file__))
ANSIBLE_WS_PATH_ROOT = os.path.dirname(ANSIBLE_WS_PATH_TEST)
ANSIBLE_WS_PATH_LIB = os.path.join(ANSIBLE_WS_PATH_ROOT, 'bin')
sys.path.append(ANSIBLE_WS_PATH_LIB)
from ansible_inventory_helper import get_ansible_host_by_group

class TestAnsibleHostsRequest(unittest.TestCase):

    sources = [
        os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'hosts')
    ]

    def test_list(self):
        expected = dict(
            database_app1_prod=['server_prod_11', 'server_prod_12', 'server_prod_13'],
            database_app2_dev=['server_dev_21', 'server_dev_22', 'server_dev_23']
        )
        query = ','.join(expected.keys())
        response = get_ansible_host_by_group(query, self.sources)
        # pprint.pprint(response)
        self.assertEqual(response, expected)

    def test_regex(self):
        expected = dict(
            database_app1_prod=['server_prod_11', 'server_prod_12', 'server_prod_13'],
            database_app2_prod=['server_prod_21', 'server_prod_22', 'server_prod_23'],
        )
        query = 'database_.*_prod'
        response = get_ansible_host_by_group(query, self.sources)
        # pprint.pprint(response)
        self.assertEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
