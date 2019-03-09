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
        self.name = 'runs'
        self.date_pattern = '%B %d, %Y'
        self.today = datetime.datetime.now()
        tomorow = self.today + datetime.timedelta(days=1)
        self.default_from = self.today.strftime(self.date_pattern)
        self.default_to   = tomorow.strftime(self.date_pattern)
        self.__usages()

        states = self.parameters.get('states', self.parameters_description['states']['default'])
        self.states = states.split(',')
        self.playbook = self.parameters.get('playbook', self.parameters_description['playbook']['default'])
        self.regex = re.compile(self.playbook)

        start_txt = self.parameters.get('from', self.parameters_description['from']['default'])
        start_date = datetime.datetime.strptime(start_txt, self.date_pattern)
        self.start = datetime.datetime.timestamp(start_date)

        end_txt = self.parameters.get('to', self.parameters_description['to']['default'])
        end_date = datetime.datetime.strptime(end_txt, self.date_pattern)
        self.end = datetime.datetime.timestamp(end_date)

    def __usages(self):
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
                'default': self.default_from,
                'format': self.date_pattern
            },
            'to': {
                'description': 'The maximal date when the runs must have started. By default tommorow.',
                'default': self.default_to,
                'format': self.date_pattern
            }
        }
        parameters = {}
        self.add_example('To get daily runs', parameters)
        date_from = self.today + datetime.timedelta(days=-7)
        date_txt = date_from.strftime(self.date_pattern)
        parameters = {
            'from': date_txt,
        }
        self.add_example('To get runs of the previous week', parameters)


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
