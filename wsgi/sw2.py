import traceback
import json
import logging
from cgi import parse_qs

import ansible_ws
import sw2
from sw2 import ScriptWebServiceWrapper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def application(environ, start_response):

    try:
        method = environ['REQUEST_METHOD']
        print("==========>", method)
        if method == 'GET':
            query_strings = parse_qs(environ['QUERY_STRING'])
            parameters = {
                key: value[0]
                for key, value in query_strings.items()
            }
        elif method == 'POST':
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            parameters =  dict(
                (key.decode("utf-8") , value[0].decode("utf-8"))
                for key, value in parse_qs(request_body).items()
            )
        print("==========>", parameters)
        service = ScriptWebServiceWrapper(parameters)
        response = service.get_result()
        if service.is_valid():
            status = ansible_ws.HTTP_200
        else:
            status = ansible_ws.HTTP_400
        response_headers, output = ansible_ws.get_json_response(response)
    except:
        status, response_headers, output = ansible_ws.get_500_response()
#     cache = ('Cache-Control', 'max-age=60')
#     response_headers.append(cache)
    start_response(status, response_headers)
    return [output]
