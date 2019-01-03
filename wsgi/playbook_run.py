import traceback
import json
import logging
from cgi import parse_qs

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceRun

logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        query_strings = parse_qs(environ['QUERY_STRING'])
        config_file = '/etc/ansible-ws/playbook_run.yml'
        service = AnsibleWebServiceRun(config_file, query_strings)
        response = service.get_result()
        if service.parameters_valid:
            status = ansible_ws.HTTP_200
        else:
            status = ansible_ws.HTTP_400
        response_headers, output = ansible_ws.get_json_response(response)

    except:
        status, response_headers, output = ansible_ws.get_500_response()

    start_response(status, response_headers)
    return [output]
