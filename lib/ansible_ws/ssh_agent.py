from typing import Dict, List
import logging
import os
import re
import getpass
import pathlib
import json
import copy
import subprocess
import psutil
import pexpect


class SshAgent():
    """
    """

    @staticmethod
    def parse_output(output: bytes) -> Dict[str, str]:
        result = {}
        for name, value in re.findall(r'([A-Z_]+)=([^;]+);', output.decode('ascii')):
            result[name] = value
        return result

    def __init__(self, id=None, path=None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user = getpass.getuser()
        self.logger.debug(self.user)
        self.id = self.user if id is None else id
        if path is None or not os.path.isdir(path):
            home = str(pathlib.Path.home())
            path = os.path.join(home, '.ssh')
        self.file_agent = os.path.join(path, f'{self.id}.agent')
        self.logger.debug(self.file_agent)
        self.env = copy.deepcopy(os.environ)
        try:
            with open(self.file_agent) as fstream:
                self.env_agent = json.load(fstream)
            self.logger.info(f'USE AGENT {self.env_agent}')
            self.env.update(self.env_agent)
            self.pid = int(self.env['SSH_AGENT_PID'])
            self.socket = self.env['SSH_AUTH_SOCK']
            if not self.__exist():
                self.__create()
        except:
            self.__create()

    def __exist(self):
        return psutil.pid_exists(self.pid) and os.path.exists(self.socket)

    def __create(self):
        self.logger.info('NEW AGENT')
        output = subprocess.check_output(['ssh-agent', '-s'])
        self.env_agent = self.parse_output(output)
        self.logger.debug(self.env_agent)
        with open(self.file_agent, 'w+') as fstream:
          json.dump(self.env_agent, fstream)
        self.env.update(self.env_agent)
        self.pid = int(self.env['SSH_AGENT_PID'])
        self.socket = self.env['SSH_AUTH_SOCK']

    def kill(self) -> None:
        if self.__exist():
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
          stdout=subprocess.PIPE
      )
      if process.returncode == 0:
        output = str(process.stdout, 'utf-8')
        keys = [
            key
            for key in output.split(os.linesep)
            if key != ''
        ]
      else:
        keys = []
      self.logger.debug(keys)
      return keys
