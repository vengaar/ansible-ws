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
        self.name = 'tasks'
        self.__usages()
        self._is_valid = 'demo1' in self.parameters

    def __usages(self):
        self.parameters_description = {
            'demo1': {
                'description': 'A value',
                'required': True,
            },
            'demo2': {
                'description': 'The playbook to gather tags',
                'required': False,
                'format': 'A list of values with coma separator',
            },
        }
        demo1 = 'test'
        demo2 = 'foo,bar'
        self.examples.append({
            'desc': f'To have list ended with p1 + p2',
            'url': f'/sw2/query?query={self.name}&demo1={demo1}&demo2={demo2}'
        })

    def query(self):
        p1 = self.parameters.get('demo1')
        p2 = self.parameters.get('demo2', [])
        if isinstance(p2, str):
            p2 = p2.split(',')
        
        values = ['I', 'love ', 'wapi', p1] + p2
        return self.format_to_semantic_ui_dropdown(values)
