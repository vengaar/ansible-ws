import re, subprocess

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService
from ansible_ws.launch import PlaybookContextLaunch, PlaybookContext
    
import uuid
import os
import json


class AnsibleWebServiceRun(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        runid = self.get_param("runid")
        pcr = PlaybookContext(runid)
        run = dict(
            status=pcr.status,
            output=pcr.out
        )
        self.result = run


class AnsibleWebServiceLaunch(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        context = dict(
            playbook='/home/vengaar/ansible-ws/test/data/playbooks/tags.yml',
            # extra_vars=dict(
            # toto='toto',
            # foo='bar'
            # ),
            # options=['-v', '--diff'],
            # inventorie= [
            #   '/tmp/toto',
            #   '/tmp/titi'
            # ],
            # task='plop',
            # tags=dict(
            #   to_apply=['foo', 'bar']
            # )
        )
        print("AnsibleWebServiceLaunch", self.parameters)
        print("AnsibleWebServiceLaunch", self.query_strings)
        context = dict(
            (key.decode("utf-8") , value[0].decode("utf-8"))
            for key, value in self.query_strings.items()
        )
        print(context)

        pcl = PlaybookContextLaunch(**context)
        pcr = PlaybookContext(pcl.runid)
        pcl.launch()
        self.result = pcr.status

class AnsibleWebServiceTags(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        playbook = self.get_param('playbook')
        command = ['ansible-playbook', '--list-tags', playbook]
        p = subprocess.run(command, capture_output=True)
        out = p.stdout.decode('utf-8')
        tags = []
        line_refused = []
        line_accepted = []
        pattern = re.compile('^.*\\[(?P<string_tags>.+)\\].*$')
        for line in out.split('\n'):
            match = re.match(pattern, line)
            if match is not None:
                line_accepted.append(line)
                string_tags = match.group('string_tags')
                for tag in string_tags.split(','):
                    tag = tag.strip()
                    if tag not in tags:
                        tags.append(tag)

            else:
                line_refused.append(line)

        self.debug['line_refused'] = line_refused
        self.debug['line_accepted'] = line_accepted
        sorted(tags)
        self.result = tags


class AnsibleWebServiceTasks(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        playbook = self.get_param('playbook')
        command = ['ansible-playbook', '--list-tasks', playbook]
        p = subprocess.run(command, capture_output=True)
        out = p.stdout.decode('utf-8')
        tasks = []
        line_refused = []
        line_accepted = []
        pattern = re.compile('^(?P<task_name>.*)TAGS.*$')
        for line in out.split('\n'):
            # re.MULTILINE
            match = re.match(pattern, line)
            if match is not None:
                task_name = match.group('task_name').strip()
                if not task_name.startswith('play #'):
                  line_accepted.append(line)                    
                  tasks.append(task_name)
                else:
                  line_refused.append(line)
            else:
                line_refused.append(line)

        self.debug['line_refused'] = line_refused
        self.debug['line_accepted'] = line_accepted
        self.result = tasks
