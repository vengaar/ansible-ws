import sys
import traceback
import json
import yaml
import logging
from cgi import parse_qs
from http import HTTPStatus

from ansible_inventory_helper import request_ansible_inventory

HTTP_200 = f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}'
HTTP_500 = f'{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'
HTTP_400 = f'{HTTPStatus.BAD_REQUEST.value} {HTTPStatus.BAD_REQUEST.phrase}'

def application(environ, start_response):

    try:
        logger = logging.getLogger(__name__)
        try:
            config_file = '/etc/ansible-ws/config.yml'
            with open(config_file) as f:
                ansible_ws_config = yaml.load(f)
                logger.info(f'Configuration file {config_file} LOADED')
        except Exception:
            logger.error(f'Not possible to load configuration file {config_file}')

        examples = ansible_ws_config['examples']
        config_parameters = ansible_ws_config['parameters']

        qs = parse_qs(environ['QUERY_STRING'])
        debug = dict(
            config_file=config_file,
            config=ansible_ws_config,
            qs=qs,
        )
        debug_mode = qs.get('debug', ['false'])[0] == 'true'

        output = dict()
        if debug_mode:
            output['debug'] = debug

        # Write generic function to provide dict from qs and config_parameters
        groups = qs.get('groups', [None])[0]
        default_sources = config_parameters['sources']['default']
        sources = qs.get('sources', default_sources)

        if groups is None:
            status = HTTP_400
            content_type = 'application/json'
            output['usage'] = debug
            output = json.dumps(output)
            output = output.encode('utf-8')
        else:
            logger.error(sources)
            output['result'] = request_ansible_inventory(groups, sources)
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
