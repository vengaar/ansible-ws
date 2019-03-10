"""
"""
import logging
import subprocess
import json
import re
from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.__usages()
        self.check_parameters()

    def __usages(self):
        self.parameters_description = {
            'demo1': {
                'description': 'A value',
                'required': True,
            },
            'demo2': {
                'description': 'A list of values',
                'required': False,
                'default': [],
            },
        }
        parameters = {
            'demo1': 'test',
            'demo2': 'foo,bar',
        }
        self.add_example('To have list ended with {demo1} + {demo2}', parameters)

    def query(self):
        p1 = self.get('demo1')
        p2 = self.get('demo2')
        values = ['I', 'love ', 'wapi', p1] + p2
        return self.format_to_semantic_ui_dropdown(values)
