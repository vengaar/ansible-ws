import logging
import os
import unittest
import pprint
import sys

sys.path.append('.')
import tests
import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestSWSW(unittest.TestCase):

    config = AnsibleWebServiceConfig()
    inventory = os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'inventories')
    query = 'grapher'

    def test_grapher(self):
        grapher_output = '/tmp'
        self.config.config['grapher']['output'] = grapher_output
        expected_file = '/tmp/db_prod_11.png'
        if os.path.isfile(expected_file):
            os.remove(expected_file)
        parameters = {
            'host': 'db_prod_11',
            'inventory': self.inventory
        }
        request = tests.get_sw2_request(self.query, parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertTrue(os.path.isfile(expected_file))
        os.remove(expected_file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
