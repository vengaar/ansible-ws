import subprocess
import uuid
import os
import json, yaml
import time
import threading
import logging

from ansible_ws import AnsibleWebServiceConfig
from ansible_ws.ssh_agent import SshAgent

class PlaybookContext(object):

    STATUS_READY = 'ready'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'

    STATE_RUNNING = 'running'
    STATE_SUCCEEDED = 'succeeded'
    STATE_FAILED = 'failed'
#     STATE_ABORTED = 'aborted'
#     STATE_KILLED = 'killed'
    STATES = (STATE_RUNNING, STATE_SUCCEEDED, STATE_FAILED)

    def __init__(self, runid: str, ansible_ws_config: AnsibleWebServiceConfig=None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ansible_ws_config = AnsibleWebServiceConfig() if ansible_ws_config is None else ansible_ws_config 
        self.runs_dir = self.ansible_ws_config.get('ansible.runs_dir')
        self.runid = runid
        self.folder = os.path.join(self.runs_dir, self.runid)
        self.logger.debug(self.folder)
        self.file_output = os.path.join(self.folder, 'run.out')
        self.file_error = os.path.join(self.folder, 'run.err')
        self.file_desc = os.path.join(self.folder, 'run.desc')
        self.file_status = os.path.join(self.folder, 'run.status')
        self._description = None

    @property
    def description(self):
        if self._description is None:
          with open(self.file_desc) as run_desc:
            self._description = json.load(run_desc)
        return self._description

    @property
    def out(self):
        if os.path.isfile(self.file_output):
            with open(self.file_output) as out:
              run_out = out.read()
        else:
            run_out = None
        return run_out

    @property
    def status(self):
      with open(self.file_status) as run_status:
        # self.logger.debug(f'read {self.file_status}')
        status = json.load(run_status)
      return status

class PlaybookContextLaunch(PlaybookContext):

    def __init__(self, **kwargs):
        self.return_code = None
        self.pid = None
        self.begin = None
        self.end = None
        if 'runid' not in kwargs:
            self.uuiid = uuid.uuid4()
            self.runid = str(self.uuiid)
            ansible_ws_config = kwargs.pop('ansible_ws_config', None)
            super().__init__(self.runid, ansible_ws_config=ansible_ws_config)
            if not os.path.isdir(self.runs_dir):
              os.mkdir(self.runs_dir)
            os.mkdir(self.folder)
            self.__write_description(kwargs)
            self.write_status(self.STATUS_READY)
        else:
            runid = kwargs['runid']
            super().__init__(runid)

    def write_status(self, status):
        self.__status = status
        if self.return_code is None:
            state = self.STATE_RUNNING
        elif self.return_code == 0:
            state = self.STATE_SUCCEEDED
        else:
            state = self.STATE_FAILED
        status = dict(
            pid=self.pid,
            runid=self.runid,
            status=self.__status,
            state=state,
            begin=self.begin,
            end=self.end,
            return_code=self.return_code,
            description=self.description
        )
        with open(self.file_status, 'w') as run_status:
          json.dump(status, run_status)

    def __write_description(self, parameters):
        playbook = parameters['playbook']
        assert os.path.isfile(playbook)
        self._description = parameters
        with open(self.file_desc, 'w') as run_desc:
          json.dump(self._description, run_desc)

    def launch(self):
        # Solution where playbook run alays link to httpd process
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        # os.system(f'python3 {os.path.realpath(__file__)} --runid {self.runid}')

    def run(self):
        self.logger.debug('=== start playbook ===')
        self.logger.debug(self.description['cmdline'])
        command = [
          self.description['cmdline']
        ]
        agent = SshAgent()
        os.environ.update(agent.env_agent)
        os.environ['ANSIBLE_FORCE_COLOR'] = 'true'
        with open(self.file_output, 'w+') as out, open(self.file_error, 'w+') as err:
            with subprocess.Popen(
                command,
                shell=True,
                stdout=out,
                stderr=err,
            ) as proc:
                self.pid = proc.pid
                self.begin = time.time()
                self.write_status(self.STATUS_STARTED)
                self.return_code = proc.wait()
            self.end = time.time()
            self.write_status(self.STATUS_FINISHED)
        self.logger.debug("=== end playbook ===")

