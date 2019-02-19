"""
"""
import subprocess
import re
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Below expected parameters
[required,string] playbook, the playbook to list tags."""

    def __init__(self,config,  **kwargs):
        super().__init__(config, **kwargs)
        if 'playbook' not in self.parameters:
            self._is_valid = False
        self.playbook = self.parameters.get('playbook')

    def query(self):
        """
        """
        self.cache_config = {
            'discriminant': self.playbook,
            'category': 'tags'
        }
        tags = self.get_cached_resource(self.get_tags)
        response = self.format_to_semantic_ui_dropdown(tags)
        return response

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            stat_cache = os.stat(key)
            stat_playbook = os.stat(self.playbook)
            return stat_cache.st_mtime > stat_playbook.st_mtime
        else:
            return False

    def get_tags(self, playbook):
        command = ['ansible-playbook', '--list-tags', playbook]
        p = subprocess.run(command, stdout=subprocess.PIPE)
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
        self.logger.debug(f'line_refused={line_refused}')
        self.logger.debug(f'line_accepted={line_accepted}')
        sorted(tags)
        self.logger.debug(tags)
        return tags
