import sys
import traceback
import json
import logging
from cgi import parse_qs
from http import HTTPStatus

HTTP_200 = f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}'
HTTP_500 = f'{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'
HTTP_400 = f'{HTTPStatus.BAD_REQUEST.value} {HTTPStatus.BAD_REQUEST.phrase}'

import ansible_ws
from ansible_ws.playbooks_ws import AnsibleWebServiceLaunch

def application(environ, start_response):

    try:
        query_strings = parse_qs(environ['QUERY_STRING'])
        print("qs", query_strings)
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        print("request_body_size", query_strings)
        request_body = environ['wsgi.input'].read(request_body_size)
        print("request_body", request_body)
        query_strings = parse_qs(request_body)
        print("qs", query_strings)
        print("qs", query_strings.keys())
        config_file = '/etc/ansible-ws/playbook_launch.yml'
        service = AnsibleWebServiceLaunch(config_file, query_strings)
        if service.parameters_valid:
            status = HTTP_200
        else:
            status = HTTP_400
        output = service.get_result()
        output = json.dumps(output)
        output = output.encode('utf-8')
        content_type = 'application/json'
    except:
        status = HTTP_500
        content_type = 'text/plain'
        trace = traceback.format_exc()
        output = trace.encode('utf-8')

    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
