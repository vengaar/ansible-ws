import os
import unittest
import pprint
import shutil

import sys
sys.path.append('.')
import tests as ansible_ws_tests
import ansible_ws
from ansible_ws.playbooks_ws import PlaybookContextLaunch, PlaybookContext
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig

class TestAnsibleLaunch(unittest.TestCase):

    RUNS_DIR = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'runs')

    @classmethod
    def tearDownClass(cls):
        super(TestAnsibleLaunch, cls).tearDownClass()
        shutil.rmtree(cls.RUNS_DIR)

    def test_run(self):

      playbook = os.path.join(ansible_ws_tests.ANSIBLE_WS_PATH_TEST, 'data', 'playbooks', 'tags.yml') 
#     print(playbook)
      ansible_ws_config = AnsibleWebServiceConfig()
      ansible_ws_config.config['runs_dir'] = self.RUNS_DIR
      context = dict(
        playbook=playbook,
        cmdline=f'ansible-playbook {playbook} -v',
        ansible_ws_config=ansible_ws_config
      )
      pcl =PlaybookContextLaunch(**context)
#     print(pcl.runid)
      pc = PlaybookContext(pcl.runid, ansible_ws_config=ansible_ws_config)
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
#     pprint.pprint(pc.out)
      self.assertIsNotNone(pc.out)
      status = pc.status
#     pprint.pprint(status)
      self.assertEqual(status['status'], pc.STATUS_FINISHED)
      self.assertIsInstance(status['begin'], float)
      self.assertIsInstance(status['end'], float)
      self.assertIsInstance(status['pid'], int)
      self.assertEqual(status['return_code'], 0)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    unittest.main()