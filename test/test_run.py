import logging
import os
import unittest
import pprint

import path_test
from path_test import ANSIBLE_WS_PATH_TEST

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceRun

class TestAnsibleHostsRequest(unittest.TestCase):

    playbook_tags   = os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'tags.yml')
    playbook_notags = os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'notags.yml')
    config_file = '/etc/ansible-ws/playbook_run.yml'

    def test_run(self):
        expected = ['tag1', 'tag2', 'tag22', 'tag3']
        query_strings = dict(
            runid=['935629ee-edd1-4dbe-ae5f-ebf6df75e306'],
        )
        service = AnsibleWebServiceRun(self.config_file, query_strings)
        data = service.get_result()
        pprint.pprint(data)
        self.assertEqual(data['results'], expected)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
