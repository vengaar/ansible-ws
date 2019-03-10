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


class TestSW2(unittest.TestCase):

    config = AnsibleWebServiceConfig()

    def test(self):
        sw2 = ScriptWebServiceWrapper({}, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertIsInstance(response['errors'], list)
        self.assertIsInstance(response['errors'][0], str)

    def test_demo(self):
        parameters = {
            'demo1': 'test',
            'demo2': ['foo', 'bar']
        }
        request = tests.get_sw2_request('demo', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        self.assertEqual(response['results'][3]['name'], 'test')
        self.assertEqual(response['results'][4]['name'], 'foo')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
