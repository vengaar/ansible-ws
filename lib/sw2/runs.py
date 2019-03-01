"""
"""
import time
import datetime
import re
import os

from ansible_ws.launch import PlaybookContextLaunch, PlaybookContext
from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        date_pattern = '%B %d, %Y'

        self.states = self.parameters.get('states', PlaybookContext.STATES)
        self.playbook = self.parameters.get('playbook', '')
        self.regex = re.compile(self.playbook)

        start_txt = self.parameters.get('from')
        if start_txt is None:
            self.start = 0
        else:
            start_date = datetime.datetime.strptime(start_txt, date_pattern)
            self.start = datetime.datetime.timestamp(start_date)

        end_txt = self.parameters.get('to')
        if end_txt is None:
            self.end = time.time()
        else:
            end_date = datetime.datetime.strptime(end_txt, date_pattern)
            self.end = datetime.datetime.timestamp(end_date)

    def query(self):
        """
        """
        runs_dir = self.config.get('ansible.runs_dir')
        runid_list = os.listdir(runs_dir)
        runs = []
        for runid in runid_list:
            path = os.path.join(runs_dir, runid)
            stat = os.stat(path)
            self.logger.debug([self.start, stat.st_ctime, self.end])
            if stat.st_ctime >= self.start and stat.st_ctime <= self.end:
                self.logger.debug('run time valid')
                pc = PlaybookContext(runid, ansible_ws_config=self.config)
                run_status = pc.status
                if self.__match(run_status):
                    runs.append(run_status)
            else:
                self.logger.debug('run time NOT valid')
        response = sorted(runs, key=lambda run: run['begin'], reverse=True)
        return response

    def __match(self, run):
        match = True
        if run['state'] not in self.states:
            match = False
        playbook = os.path.basename(run['description']['playbook'])
        if self.regex.match(playbook) is None:
            match = False
        return match
