"""
"""
import time
import datetime
import re
import os

from ansible_ws.launch import PlaybookContextLaunch, PlaybookContext
from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Return a list of run according to parameters"""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.date_pattern = '%B %d, %Y'
        self.__usages()

    def __usages(self):
        today = datetime.datetime.now()
        tomorow = today + datetime.timedelta(days=1)
        default_from = today.strftime(self.date_pattern)
        default_to   = tomorow.strftime(self.date_pattern)
        self.parameters_description = {
            'states': {
                'description': 'The states of the runs searched',
                'default': ','.join(list(PlaybookContext.STATES)),
                'values': PlaybookContext.STATES,
                'format': 'List of sate separated by coma'
            },
            'playbook': {
                'description': 'The name of playbook used for the run',
                'default': '',
                'format': 'regex'
            },
            'from': {
                'description': 'The minimal date when the runs must have started. By default current day.',
                'default': default_from,
                'format': self.date_pattern
            },
            'to': {
                'description': 'The maximal date when the runs must have started. By default tommorow.',
                'default': default_to,
                'format': self.date_pattern
            }
        }
        self.add_example('To get daily runs')
        date_from = today + datetime.timedelta(days=-7)
        date_txt = date_from.strftime(self.date_pattern)
        parameters = {
            'from': date_txt,
        }
        self.add_example('To get runs of the previous week', parameters)


    def query(self):
        """
        """
        states = self.get('states').split(',')
        playbook = self.get('playbook')
        regex = re.compile(playbook)
        start_txt = self.get('from')
        start_date = datetime.datetime.strptime(start_txt, self.date_pattern)
        start = datetime.datetime.timestamp(start_date)
        end_txt = self.get('to')
        end_date = datetime.datetime.strptime(end_txt, self.date_pattern)
        end = datetime.datetime.timestamp(end_date)
        runs_dir = self.config.get('ansible.runs_dir')
        runid_list = os.listdir(runs_dir)
        runs = []
        for runid in runid_list:
            path = os.path.join(runs_dir, runid)
            stat = os.stat(path)
            self.logger.debug([start, stat.st_ctime, end])
            if stat.st_ctime >= start and stat.st_ctime <= end:
                self.logger.debug('run time valid')
                pc = PlaybookContext(runid, ansible_ws_config=self.config)
                run_status = pc.status
                if self.__match(run_status, states, regex):
                    runs.append(run_status)
            else:
                self.logger.debug('run time NOT valid')
        response = sorted(runs, key=lambda run: run['begin'], reverse=True)
        return response

    def __match(self, run, states, regex):
        match = True
        if run['state'] not in states:
            match = False
        playbook = os.path.basename(run['description']['playbook'])
        if regex.match(playbook) is None:
            match = False
        return match
