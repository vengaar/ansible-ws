
import logging
from cgi import parse_qs

import ansible_ws
from ansible_ws.inventory_ws import AnsibleWebServiceHosts

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        query_strings = parse_qs(environ['QUERY_STRING'])
        config_file = '/etc/ansible-ws/ansible_hosts.yml'
        service = AnsibleWebServiceHosts(config_file, query_strings)
        response = service.get_result()
        if service.parameters_valid:
            status = ansible_ws.HTTP_200
            format = service.get_param('format')
            if format == 'sui':
                disabled = service.get_param('groups_selection') == 'no'
                sui_result = []
                for name, hosts in response['results'].items():
                    group = dict(name=f'<i class="orange sitemap icon"></i> {name}', value=name, disabled=disabled)
                    sui_result.append(group)
                    sui_result += [
                        dict(name=f'<i class="hdd icon"></i> {host}', value=host)
                        for host in hosts
                    ]
                response['results'] = sui_result
        else:
            status = ansible_ws.HTTP_400
        response_headers, output = ansible_ws.get_json_response(response)

    except:
        status, response_headers, output = ansible_ws.get_500_response()

    start_response(status, response_headers)
    return [output]
