import os
ANSIBLE_WS_PATH_TEST = os.path.dirname(os.path.realpath(__file__))
ANSIBLE_WS_PATH_ROOT = os.path.dirname(ANSIBLE_WS_PATH_TEST)
ANSIBLE_WS_PATH_LIB = os.path.join(ANSIBLE_WS_PATH_ROOT, 'lib')

import sys
sys.path.append(ANSIBLE_WS_PATH_LIB)

def get_sw2_request(query, parameters={}, debug=True, cache='bypass'):
    return {
        'sw2': {
            'query': query,
            'debug': debug,
            'cache': cache,
        },
        'parameters': parameters
    }