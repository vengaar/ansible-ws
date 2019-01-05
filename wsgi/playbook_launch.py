import traceback
import json
import logging
from cgi import parse_qs

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceLaunch

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        query_strings =  dict(
            (key.decode("utf-8") , value[0].decode("utf-8"))
            for key, value in parse_qs(request_body).items()
        ) 
        config_file = '/etc/ansible-ws/playbook_launch.yml'
        service = AnsibleWebServiceLaunch(config_file, query_strings)
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
