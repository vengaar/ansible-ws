import logging
import unittest
import pprint

import sys
sys.path.append('.')
import tests
from ansible_ws import AnsibleWebServiceConfig


class TestAnsibleWebServiceConfig(unittest.TestCase):

    def test(self):
        config = AnsibleWebServiceConfig()
        value = config.get('unittest.unittest.unittest')
        self.assertEqual(value, 'unittest')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
