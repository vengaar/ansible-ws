import traceback
import json
import logging
from cgi import parse_qs

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceTasks

logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        query_strings = parse_qs(environ['QUERY_STRING'])
        config_file = '/etc/ansible-ws/playbook_tasks.yml'
        service = AnsibleWebServiceTasks(config_file, query_strings)
        if service.parameters_valid:
            status = ansible_ws.HTTP_200
        else:
            status = ansible_ws.HTTP_400

        output = service.get_result()
        format = service.get_param('format')
        if format == 'sui':
            sui_results = [
                dict(name=tag, value=tag)
                for tag in output['results']
            ]
            output['results'] = sui_results

        output = json.dumps(output)
        output = output.encode('utf-8')
        content_type = 'application/json'
    except:
        status = ansible_ws.HTTP_500
        content_type = 'text/plain'
        trace = traceback.format_exc()
        output = trace.encode('utf-8')

    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]