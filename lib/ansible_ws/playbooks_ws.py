import re
import os
import time
import subprocess

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService, AnsibleWebServiceConfig, json_file_cache
from ansible_ws.launch import PlaybookContextLaunch, PlaybookContext


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
        return run


class AnsibleWebServiceLaunch(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        pcl = PlaybookContextLaunch(**self.query_strings)
        pcl.launch()
        return pcl.status


class AnsibleWebServiceTags(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        playbook = self.get_param('playbook')
        return self.get_tags(playbook)

    def cache_get_key(self, discriminant):
        playbook = os.path.basename(discriminant)
        key = f'/tmp/.ansible-ws.cache.tags.{playbook}'
        return key

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            stat_cache = os.stat(key)
            stat_playbook = os.stat(self.get_param('playbook'))
            return stat_cache.st_mtime > stat_playbook.st_mtime
        else:
            return False

    @json_file_cache
    def get_tags(self, playbook):
        ansible_cmd = AnsibleWebServiceConfig().get('ansible_cmd.playbook')
        command = [ansible_cmd, '--list-tags', playbook]
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
        self.debug['line_refused'] = line_refused
        self.debug['line_accepted'] = line_accepted
        sorted(tags)
        return tags


class AnsibleWebServiceTasks(AnsibleWebService):

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        playbook = self.get_param('playbook')
        return self.get_tasks(playbook)

    def cache_get_key(self, discriminant):
        playbook = os.path.basename(discriminant)
        key = f'/tmp/.ansible-ws.cache.tasks.{playbook}'
        return key

    def cache_is_valid(self, key):
        if os.path.isfile(key):
            stat_cache = os.stat(key)
            stat_playbook = os.stat(self.get_param('playbook'))
            return stat_cache.st_mtime > stat_playbook.st_mtime
        else:
            return False

    @json_file_cache
    def get_tasks(self, playbook):
        ansible_cmd = AnsibleWebServiceConfig().get('ansible_cmd.playbook')
        command = [ansible_cmd, '--list-tasks', playbook]
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

        self.debug['line_refused'] = line_refused
        self.debug['line_accepted'] = line_accepted
        return tasks







# def file_cache_test(type='undefined'):
#     """
#     """
#     logger = logging.getLogger('file_cache')
# 
#     def decorated(func):
#         """
#         """
# 
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             """
#             """
#             logger.info(f'Enter cache for type {type}')
#             def update_cache(cache_path):
#                 result = func(*args, **kwargs)
#                 logger.info(f'Write cache {cache_path}')
#                 with open(cache_path, 'w') as stream:
#                     json.dump(result, stream)
#                 return result
# 
#             playbook_path = args[1]
#             logger.debug(f'playbook_path={playbook_path}')
#             playbook = os.path.basename(playbook_path)
#             logger.debug(f'playbook={playbook}')
#             dir = os.path.dirname(playbook_path)
#             cache_filename = f'.cached.{type}.{playbook}'
#             cache_path = os.path.join(dir, cache_filename)
#             print(f'cache_path={cache_path}')
#             if os.path.isfile(cache_path):
#                 logger.info(f'Cache found {cache_path}')
#                 stat_cache = os.stat(cache_path)
#                 stat_playbook = os.stat(playbook_path)
#                 if stat_cache.st_mtime > stat_playbook.st_mtime:
#                     logger.info('Cache younger than playbook -> use cache')
#                     try:
#                         with open(cache_path) as stream:
#                             data = stream.read()
#                         result = json.loads(data)
#                     except Exception as e:
#                         logger.error(f'Failed to read cache {cache_path}')
#                         logger.error(str(e))
#                         result = update_cache(cache_path)
#                 else:
#                     logger.info('Cache older than playbook -> update cache')
#                     result = update_cache(cache_path)
#             else:
#                 logger.info(f'Cache not found {cache_path}')
#                 result = update_cache(cache_path)
#             return result
# 
#         return wrapper
# 
#     return decorated

