import http

HTTP_200 = f'{http.HTTPStatus.OK.value} {http.HTTPStatus.OK.phrase}'
HTTP_500 = f'{http.HTTPStatus.INTERNAL_SERVER_ERROR.value} {http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'
HTTP_400 = f'{http.HTTPStatus.BAD_REQUEST.value} {http.HTTPStatus.BAD_REQUEST.phrase}'
