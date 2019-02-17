import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.inventory_ws2 import AnsibleWebServiceHosts, AnsibleWebServiceGroupVars

class TestAnsibleHostsRequest(unittest.TestCase):

    hosts_dir = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories')
    hosts_database = os.path.join(hosts_dir, 'hosts_database') 
    sources = [
        hosts_database
    ]
    config_file = '/etc/ansible-ws/ansible_hosts.yml'

    def test_default(self):
        expected = dict(
            all=[
                'db_prod_11',
                'db_prod_12',
                'db_prod_13',
                'db_prod_21',
                'db_prod_22',
                'db_prod_23',
                'server_dev_x1',
                'server_dev_x2',
            ],
        )
        query_strings = dict(
            sources=self.sources,
        )
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

        query_strings['cache'] = ['flush']
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)


    def test_regex(self):
        expected = dict(
            database_app1_prod=['db_prod_11', 'db_prod_12', 'db_prod_13'],
            database_app2_prod=['db_prod_21', 'db_prod_22', 'db_prod_23'],
        )
        query_strings = dict(
            sources=self.sources,
            groups=['^database_.*_prod$'],
        )
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_list(self):
        expected = dict(
            database_app1_dev=['server_dev_x1', 'server_dev_x2'],
            database_app2_prod=['db_prod_21', 'db_prod_22', 'db_prod_23'],
        )
        query_strings = dict(
            sources=self.sources,
            groups=['^(database_app1_dev|database_app2_prod)$'],
        )
        service = AnsibleWebServiceHosts(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_groupvars(self):
        expected = ['es', 'fr', 'it']
        query_strings = dict(
            group=['database_app1_prod'],
            key=['countries.dict'],
            inventory=[self.hosts_dir]
        )
        config_file = '/etc/ansible-ws/groupvars.yml'
        service = AnsibleWebServiceGroupVars(config_file, query_strings)
#         print(service.parameters)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
