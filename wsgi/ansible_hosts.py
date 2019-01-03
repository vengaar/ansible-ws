import traceback
import json
import logging
from cgi import parse_qs

import ansible_ws
from ansible_ws.inventory_ws import AnsibleWebServiceHosts

logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        query_strings = parse_qs(environ['QUERY_STRING'])
        config_file = '/etc/ansible-ws/ansible_hosts.yml'
        service = AnsibleWebServiceHosts(config_file, query_strings)
        if service.parameters_valid:
            status = ansible_ws.HTTP_200
        else:
            status = ansible_ws.HTTP_400

        output = service.get_result()
        format = service.get_param('format')
        if format == 'sui':
            disabled = service.get_param('groups_selection') == 'no'
            sui_result = []
            for name, hosts in output['results'].items():
                sui_result.append(dict(name=f'<i class="orange sitemap icon"></i> {name}', value=name, disabled=disabled))
                sui_result += [
                    dict(name=f'<i class="hdd icon"></i> {host}', value=host)
                    for host in hosts
                    ]
            output['results'] = sui_result

        content_type = 'application/json'
        output = json.dumps(output)
        output = output.encode('utf-8')
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
