"""
"""
import subprocess
import re
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on coomand [ansible-playbook --list-tasks].
The tags are put in cache."""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.name = 'tasks'
        self.__usages()
        self._is_valid = 'playbook' in self.parameters
        if self._is_valid:
            playbook = self.parameters.get('playbook')
            self.playbook = os.path.expanduser(playbook)

    def __usages(self):
        self.parameters_description = {
            'playbook': {
                'description': 'The playbook to gather tags',
                'required': True,
            },
        }
        playbook = '~/ansible-ws/tests/data/playbooks/tags.yml'
        self.examples.append({
            'desc': f'To get tags of playbook {playbook}',
            'url': f'/sw2/query?query={self.name}&playbook={playbook}'
        })

    def query(self):
        """
        """
        self.cache_config = {
            'discriminant': self.playbook,
            'category': 'tasks'
        }
        tasks = self.get_cached_resource(self.get_tasks)
        response = self.format_to_semantic_ui_dropdown(tasks)
        return response

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            stat_cache = os.stat(key)
            stat_playbook = os.stat(self.playbook)
            return stat_cache.st_mtime > stat_playbook.st_mtime
        else:
            return False

    def get_tasks(self, playbook):
        command = ['ansible-playbook', '--list-tasks', playbook]
        p = subprocess.run(command, stdout=subprocess.PIPE)
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

        self.logger.debug(f'line_refused={line_refused}')
        self.logger.debug(f'line_accepted={line_accepted}')
        return tasks
