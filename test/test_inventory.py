import os
import unittest
import pprint

import path_test
from path_test import ANSIBLE_WS_PATH_TEST

import ansible_ws
from ansible_ws.inventory_ws import AnsibleWebServiceHosts

class TestAnsibleHostsRequest(unittest.TestCase):

    sources = [
        os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'inventories', 'hosts')
    ]
    config_file = '/etc/ansible-ws/ansible_hosts.yml'

    def test_list(self):
        expected = dict(
            database_app1_prod=['server_prod_11', 'server_prod_12', 'server_prod_13'],
            database_app2_dev=['server_dev_21', 'server_dev_22', 'server_dev_23']
        )
        query_strings = dict(
            sources=self.sources,
            type=['list'],
            groups=['database_app1_prod', 'database_app2_dev'],
        )
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
        # pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_regex(self):
        expected = dict(
            database_app1_prod=['server_prod_11', 'server_prod_12', 'server_prod_13'],
            database_app2_prod=['server_prod_21', 'server_prod_22', 'server_prod_23'],
        )
        query_strings = dict(
            sources=self.sources,
            type=['regex'],
            groups=['database_.*_prod'],
        )
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
        # pprint.pprint(data)
        self.assertEqual(data['results'], expected)

if __name__ == '__main__':
    unittest.main()
