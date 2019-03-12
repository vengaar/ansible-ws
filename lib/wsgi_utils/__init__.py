import http
import traceback
import json

HTTP_200 = f'{http.HTTPStatus.OK.value} {http.HTTPStatus.OK.phrase}'
HTTP_500 = f'{http.HTTPStatus.INTERNAL_SERVER_ERROR.value} {http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'
HTTP_400 = f'{http.HTTPStatus.BAD_REQUEST.value} {http.HTTPStatus.BAD_REQUEST.phrase}'
HTTP_415 = f'{http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value} {http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase}'

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_TEXT = 'text/plain'


def get_500_response():
    status = HTTP_500
    content_type = CONTENT_TYPE_TEXT
    trace = traceback.format_exc()
    output = trace.encode('utf-8')
    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    return status, response_headers, output


def get_json_response(data):
    json_data = json.dumps(data, indent=2)
    output = json_data.encode('utf-8')
    response_headers = [
        ('Content-type', CONTENT_TYPE_JSON),
        ('Content-Length', str(len(output)))
    ]
    return response_headers, output
