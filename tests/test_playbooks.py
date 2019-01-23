import logging
import os
import unittest
import pprint

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceTags, AnsibleWebServiceTasks

class TestAnsibleHostsRequest(unittest.TestCase):

    playbook_tags   = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'tags.yml')
    playbook_notags = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'notags.yml')
    config_file = '/etc/ansible-ws/playbook_tags.yml'

    def test_tags(self):
        expected = ['tag1', 'tag2', 'tag22', 'tag3']
        query_strings = dict(
            playbook=[self.playbook_tags],
            debug=['true']
        )
        service = AnsibleWebServiceTags(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_tags_no(self):
        expected = []
        query_strings = dict(
            playbook=[self.playbook_notags],
            debug=['true']
        )
        service = AnsibleWebServiceTags(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)

    def test_tasks(self):
        expected = ['task11', 'task12 with long name', 'task13', 'debug', 'task21', 'task22']
        query_strings = dict(
            playbook=[self.playbook_tags],
            debug=['true']
        )
        service = AnsibleWebServiceTasks(self.config_file, query_strings)
        data = service.get_result()
#         pprint.pprint(data)
        self.assertEqual(data['results'], expected)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
