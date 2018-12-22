import os
import unittest
import pprint

import path_test
from path_test import ANSIBLE_WS_PATH_TEST

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceTags

class TestAnsibleHostsRequest(unittest.TestCase):

    playbook_tags   = os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'tags.yml')
    playbook_notags = os.path.join(ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'notags.yml')
    config_file = '/etc/ansible-ws/playbook_tags.yml'

    def test_tags(self):
        expected = ['tag1', 'tag2', 'tag22', 'tag3']
        query_strings = dict(
            playbook=[self.playbook_tags],
            debug=['true']
        )
        service = AnsibleWebServiceTags(self.config_file, query_strings)
        data = service.get_result()
        # pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_tags(self):
        expected = []
        query_strings = dict(
            playbook=[self.playbook_notags],
            debug=['true']
        )
        service = AnsibleWebServiceTags(self.config_file, query_strings)
        data = service.get_result()
        # pprint.pprint(data)
        self.assertEqual(data['results'], expected)



if __name__ == '__main__':
    unittest.main()
