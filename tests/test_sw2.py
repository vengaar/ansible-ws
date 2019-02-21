import logging
import os
import unittest
import pprint
import json
import sys
sys.path.append('.')
import tests

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestSWSW(unittest.TestCase):

    config = AnsibleWebServiceConfig()

    def test_demo(self):
        parameters = {
            'demo1': 'value1',
            'demo2': ['foo', 'bar']
        }
        json_parameters = json.dumps(parameters)
#         print(json_parameters)
        request = dict(
            debug='true',
            query='demo',
            parameters=json_parameters
        )
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results'][5]['name'], 'foo')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
