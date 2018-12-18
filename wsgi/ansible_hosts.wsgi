import sys
import traceback
import json
from cgi import parse_qs
from http import HTTPStatus

from ansible_inventory_helper import get_ansible_host_by_group

HTTP_200 = f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}'
HTTP_500 = f'{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'
HTTP_400 = f'{HTTPStatus.BAD_REQUEST.value} {HTTPStatus.BAD_REQUEST.phrase}'

def application(environ, start_response):

    try:
        qs = parse_qs(environ['QUERY_STRING'])
        debug = dict(
            qs=qs
        )
        debug_mode = qs.get('debug', ['false'])[0]
        protocol = environ['REQUEST_SCHEME']
        server = environ['SERVER_NAME']
        _port = environ['SERVER_PORT']
        debug['_port'] = str(type(_port))
        port = '' if _port == '80' else f':{_port}'
        path = environ['SCRIPT_NAME']
        uri = f'{protocol}://{server}{port}{path}'

        parameters = dict(
            groups = dict(
                desc = 'The ansible groups to used to select hosts',
                require = True,
                format = 'List of groups separated by comma or group pattern'
            ),
            sources = dict(
                desc = 'The folder or to use as ansible inventory',
                require = False,
                default = '/etc/ansible/hosts',
                format = 'List of path separated by comma'
            )
        )
        examples = [
            dict(
                desc = 'To get hosts in groups database_app1_prod and database_app2_dev',
                url = f'{uri}?groups=database_app1_prod,database_app3_prod'
            ),
            dict(
                desc = 'To get hosts wich name groups match pattern database_.*_prod',
                url = f'{uri}?groups=database_.*_prod'
            )
        ]

        output = dict()
        if debug_mode:
            output['debug'] = debug
            output['examples'] = examples

        groups = qs.get('groups', [None])[0]
        sources = qs.get('source', ['/etc/ansible/hosts'])[0]

        if groups is None:
            status = HTTP_400
            content_type = 'application/json'
            output['usage'] = dict(
                parameters=parameters,
                examples=examples
            )
            output = json.dumps(output)
            output = output.encode('utf-8')
        else:
            output['result'] = get_ansible_host_by_group(groups, sources)
            status = HTTP_200
            content_type = 'application/json'
            output = json.dumps(output)
            output = output.encode('utf-8')
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
