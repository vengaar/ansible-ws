"""
"""
import subprocess
import re

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Below expected parameters
[required,string] playbook, the playbook to gather tags."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'playbook' not in self.parameters:
            self._is_valid = False

    def query(self):
        """
        """
        playbook = self.parameters.get('playbook',)
        self.cache_config = {
            'discriminant': playbook,
            'category': 'tasks'
        }
        tasks = self.get_cached_resource(self.get_tasks)
        response = self.format_to_semantic_ui_dropdown(tasks)
        return response

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
