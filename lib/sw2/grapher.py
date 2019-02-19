"""
"""
import subprocess
import os

from . import ScriptWrapper


class ScriptWrapperQuery(ScriptWrapper):
    """Below expected parameters
[required,string] host, the ansible host to graph dependencies.
[optional,string] format, [png,svg] the graph output format."""

    def __init__(self,config,  **kwargs):
        super().__init__(config, **kwargs)
        self.host = self.parameters.get('host')
        if self.host is None:
            self._is_valid = False
        self.format = self.parameters.get('format', self.config.get('grapher.format'))
        self.output_folder = config.get('grapher.output')
    def query(self):
        """
        """
        if 'inventory' in self.parameters:
            inventory = f' -i {self.parameters["inventory"]}'
        else:
            inventory = ''
        img_file = f'{self.output_folder}/{self.host}.{self.format}'
        command = [f'ansible-inventory-grapher {self.host}{inventory} | dot -T{self.format} > {img_file}']
        self.logger.debug(command)
        with open(img_file, 'wb+') as out:
            subprocess.run(command, capture_output=True, check=True, shell=True)
        return img_file
