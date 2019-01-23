
import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService

class AnsibleWebServiceSshAgent(AnsibleWebService):
    """
    """
    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        self.result = dict()
        action = self.get_param('action')
        self.logger.error(self.parameters)
        self.logger.error(action)
        agent = SshAgent()
        if action == 'add':
            _private_key = self.get_param('private_key')
            private_key = os.path.expanduser(_private_key)
            passphrase = self.get_param('passphrase')
            self.logger.error(private_key)
            self.logger.error(passphrase)
            agent.load_key(private_key, passphrase)
        result = dict(
          agent=agent.env_agent,
          keys=agent.keys
        )
        self.result = result

import os
import subprocess
import pprint
from typing import Dict, List
import re
# dnf install python3-pexpect.noarch
import pexpect
import getpass
import pathlib
import json
import logging
import copy
import psutil

def parse_output(output: bytes) -> Dict[str, str]:
    result = {}
    for name, value in re.findall(r'([A-Z_]+)=([^;]+);', output.decode('ascii')):
        result[name] = value
    return result

class SshAgent():

    user = getpass.getuser()
    home = str(pathlib.Path.home())
    file_agent = os.path.join(home, '.ssh', 'wapi.agent')

    def __init__(self) -> None:

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(self.user)
        self.logger.debug(self.home)
        self.logger.debug(self.file_agent)
        try:
            with open(self.file_agent) as fstream:
              self.env_agent = json.load(fstream)
              self.logger.info(f'USE AGENT {self.env_agent}')
        except:
          self.logger.info('NEW AGENT')
          output = subprocess.check_output(['ssh-agent', '-s'])
          self.env_agent = parse_output(output)
          self.logger.debug(self.env_agent)
          with open(self.file_agent, 'w+') as fstream:
            json.dump(self.env_agent, fstream)
        self.env = copy.deepcopy(os.environ)
        self.env.update(self.env_agent)
        self.pid = int(self.env['SSH_AGENT_PID'])
        self.socket = self.env['SSH_AUTH_SOCK']

    def kill(self) -> None:
        if psutil.pid_exists(self.pid) and os.path.exists(self.socket):
            self.logger.info(f'Killing ssh-agent {self.pid}')
            p = psutil.Process(self.pid)
            p.terminate()
            p.wait()
            os.remove(self.file_agent)

    def load_key(self, private_key, passphrase):
        self.logger.info(f'Load key {private_key}')
        child = pexpect.spawn(f'ssh-add {private_key}', env=self.env)
        child.expect(f'Enter passphrase for {private_key}:')
        child.sendline(passphrase)
        case = child.expect([b'.*Identity added', b'.*Bad passphrase'])
        child.close()
        if case != 0:
            raise Exception('Bad passphrase')

    @property
    def keys(self):
      process = subprocess.run(
          ['ssh-add', '-L'],
          env=self.env,
          capture_output=True,
          text=True,
      )
      if process.returncode == 0:
        keys = process.stdout
      else:
        keys = ''
      self.logger.debug(keys)
      return keys
