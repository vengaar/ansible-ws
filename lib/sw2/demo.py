"""
"""
import logging
import subprocess
import json
import re
from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def query(self):
        p1 = self.parameters.get('demo1')
        p2 = self.parameters.get('demo2', [])
        values = ['Ha', 'que ', 'coucou', '!!!', p1] + p2
        return self.format_to_semantic_ui_dropdown(values)
