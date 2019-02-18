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

