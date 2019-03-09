import logging
import os
import unittest
import pprint
import shutil
import time

import sys
sys.path.append('.')
import tests
import ansible_ws
from ansible_ws.playbooks_ws import PlaybookContextLaunch, PlaybookContext
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
from sw2 import ScriptWebServiceWrapper


class TestAnsibleLaunch(unittest.TestCase):

    RUNS_DIR = os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'runs_tmp')
    playbook = os.path.join(tests.ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'tags.yml')
    config = AnsibleWebServiceConfig()
    config.config['ansible']['runs_dir'] = RUNS_DIR

    @classmethod
    def tearDownClass(cls):
        super(TestAnsibleLaunch, cls).tearDownClass()
        shutil.rmtree(cls.RUNS_DIR)

    def test_run(self):
        context = {
            'playbook': self.playbook,
            'cmdline': f'ansible-playbook {self.playbook} -v',
            'ansible_ws_config': self.config
        }
        pcl = PlaybookContextLaunch(**context)
#         print(pcl.runid)
        pc = PlaybookContext(pcl.runid, ansible_ws_config=self.config)
        self.assertIsNone(pc.out)
        context.pop('ansible_ws_config')
        self.assertEqual(pc.description, context)
        status = pc.status
        runid = status['runid']
        self.assertEqual(len(runid.split('-')), 5)
        self.assertEqual(status['status'], pc.STATUS_READY)
        self.assertIsNone(status['begin'])
        self.assertIsNone(status['end'])
        self.assertIsNone(status['pid'])
        self.assertIsNone(status['return_code'])
        pcl.run()
#         pprint.pprint(pc.out)
        self.assertIsNotNone(pc.out)
        status = pc.status
#         pprint.pprint(status)
        self.assertEqual(status['status'], pc.STATUS_FINISHED)
        self.assertIsInstance(status['begin'], float)
        self.assertIsInstance(status['end'], float)
        self.assertIsInstance(status['pid'], int)
        self.assertEqual(status['return_code'], 0)

    def test_sw2(self):
        parameters = {
            'cmdline': f'ansible-playbook  {self.playbook} -v',
            'playbook': self.playbook,
        }
        request = tests.get_sw2_request('launch', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        results = response['results']
#         pprint.pprint(results)
        self.assertIsNone(results['return_code'])
        self.assertEqual(results['state'], PlaybookContext.STATE_RUNNING)
        self.assertEqual(results['status'], PlaybookContext.STATUS_READY)
        runid = results['runid']

        parameters = {
            'runid': runid
        }
        request = tests.get_sw2_request('run', parameters)
#         pprint.pprint(request)
        sw2 = ScriptWebServiceWrapper(request, self.config)
        response = sw2.get_result()
#         pprint.pprint(response)
        status = response['results']['status']
#         pprint.pprint(status)
        self.assertEqual(status['runid'], runid)
        while status['status'] != PlaybookContext.STATUS_FINISHED:
            time.sleep(5)
            sw2 = ScriptWebServiceWrapper(request, self.config)
            response = sw2.get_result()
#             pprint.pprint(response)
            status = response['results']['status']
        self.assertEqual(status['return_code'], 0)
        self.assertEqual(status['state'], PlaybookContext.STATE_SUCCEEDED)
        self.assertEqual(status['status'], PlaybookContext.STATUS_FINISHED)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
