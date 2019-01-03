import re, subprocess

import uuid
import os
import json
import time
import daemon
import lockfile
import threading

class PlaybookContext(object):

    STATUS_READY = 'ready'
    STATUS_STARTED = 'started'
    STATUS_FINISHED = 'finished'
    DIR_RUNS = '/home/vengaar/wapi_runs'

    def __init__(self, runid):

        self.runid = runid
        self.folder = os.path.join(self.DIR_RUNS, self.runid)
        print(self.folder)
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
        status = json.load(run_status)
      return status

class PlaybookContextLaunch(PlaybookContext):

    def __init__(self, **kwargs):
        print("PCL INIT")
        print(kwargs)
        self.return_code = None
        self.pid = None
        self.begin = None
        self.end = None
        if 'runid' not in kwargs:
            self.uuiid = uuid.uuid4()
            self.runid = str(self.uuiid)
            super().__init__(self.runid)
            if not os.path.isdir(self.DIR_RUNS):
              os.mkdir(self.DIR_RUNS)
            os.mkdir(self.folder)
            self.__write_description(kwargs)
            self.write_status(self.STATUS_READY)
        else:
            runid = kwargs['runid']
            print(runid)
            super().__init__(runid)

    def write_status(self, status):
        self.__status = status
        status = dict(
            pid=self.pid,
            runid=self.runid,
            status=self.__status,
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
        # folder = self.folder
        # fpid = os.path.join(folder, 'run.pid')
        # fpid_out = os.path.join(folder, 'pid.out')
        # fpid_err = os.path.join(folder, 'pid.err')
        # with open(fpid_out, 'w+') as pid_out, open(fpid_err, 'w+') as pid_err:
        #     with daemon.DaemonContext(
        #         working_directory=folder,
        #         # pidfile=lockfile.LockFile(fpid),
        #         stdout=pid_out,
        #         stderr=pid_err,
        #     ) as ctx:
        #         run(folder, self.runid)
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print('=== start playbook ===')
        print(self.description['cmdline'])
        command = [
          self.description['cmdline']
        ]
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
        print("=== end playbook ===")

if __name__ == '__main__':
    import pprint
    context = dict(
      playbook='/home/vengaar/ansible-ws/test/data/playbooks/tags.yml',
    )
    pcl =PlaybookContextLaunch(**context)
    pcl.launch()
    pcr = PlaybookContext(pcl.runid)    
    # while pcr.status["return_code"] is None:
    #   time.sleep(1)
    #   print ('wait')
    # pprint.pprint(pcr.out)
    # pprint.pprint(pcr.description)
    # pprint.pprint(pcr.status)

