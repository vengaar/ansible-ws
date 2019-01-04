import os
import unittest
import pprint

import path_test
from path_test import ANSIBLE_WS_PATH_TEST

import ansible_ws
from ansible_ws.playbooks_ws import PlaybookContextLaunch, PlaybookContext

class TestAnsibleLaunch(unittest.TestCase):


    def _test_context_read(self):
      pcl =PlaybookContextRead('fcba34a1-f20c-4f30-b89f-7b19bab99610')
      pprint.pprint(pcl.id)
      pprint.pprint(pcl.description)

    def test_context_new(self):
    #   context = dict(
    #     playbook='/home/vengaar/ansible-ws/test/data/playbooks/wait.yml',
    #     extra_vars=dict(
    #       toto='toto',
    #       foo='bar'
    #     ),
    #     options=['-v', '--diff'],
    #     # inventorie= [
    #     #   '/tmp/toto',
    #     #   '/tmp/titi'
    #     # ],
    #     # task='plop',
    #     # tags=dict(
    #     #   to_apply=['foo', 'bar']
    #     # )
    #   )
      context = dict(
        playbook='/home/vengaar/ansible-ws/test/data/playbooks/wait.yml',
      )
      pcl =PlaybookContextLaunch(**context)
      print(pcl.id)
      pcl.launch()
      pcr = PlaybookContextRead(pcl.id)
      pprint.pprint(pcr.out)
      pprint.pprint(pcr.description)
      pprint.pprint(pcr.status)



if __name__ == '__main__':
    #   unittest.main()
      playbook = '/home/vengaar/ansible-ws/test/data/playbooks/wait.yml'
      context = dict(
        playbook=playbook,
        cmdline=f'ansible-playbook {playbook} -vvv'

      )
      pcl =PlaybookContextLaunch(**context)
      runid = pcl.runid
      print(runid)
      pcl.launch()
      pc = PlaybookContext(runid)
      print(pc)
      pprint.pprint(pc.out)
      pprint.pprint(pc.description)
      pprint.pprint(pc.status)