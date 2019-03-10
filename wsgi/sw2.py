import traceback
import json
import logging
import urllib
from cgi import parse_qs

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebServiceConfig
import sw2
from sw2 import ScriptWebServiceWrapper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
config = AnsibleWebServiceConfig()

def application(environ, start_response):

    try:
        method = environ['REQUEST_METHOD']
        content_type = environ.get('CONTENT_TYPE')
        if content_type in (ansible_ws.CONTENT_TYPE_JSON, None):
            if method == 'GET':
                raw_qs = environ.get('QUERY_STRING')
                if raw_qs == '':
                    raw_qs = '{}'
                qs =  urllib.parse.unquote_plus(raw_qs, encoding='utf-8')
                parameters = json.loads(qs)
            elif method == 'POST':
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                request_body = environ['wsgi.input'].read(request_body_size)
                parameters = json.loads(request_body)
            service = ScriptWebServiceWrapper(parameters, config)
            response = service.get_result()
            if content_type is None:
                response['warnings'] = [
                    f'No content-type found in request. Assume content-type was {ansible_ws.CONTENT_TYPE_JSON}'
                ]
            if service.is_valid():
                status = ansible_ws.HTTP_200
            else:
                status = ansible_ws.HTTP_400
        else:
            status = ansible_ws.HTTP_415
            response = {
                'errors': [
                    f'Unexpected content-type, {content_type} found instead {ansible_ws.CONTENT_TYPE_JSON}'
                ]
            }
        response_headers, output = ansible_ws.get_json_response(response)
    except:
        status, response_headers, output = ansible_ws.get_500_response()
    start_response(status, response_headers)
    return [output]
