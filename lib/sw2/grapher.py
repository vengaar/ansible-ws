"""
"""
import subprocess
import os

from . import ScriptWrapper
from sys import stdout


class ScriptWrapperQuery(ScriptWrapper):
    """Wrapper on ansible-inventory-grapher."""

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.name = 'grapher'
        self.default_format = self.config.get('grapher.format')
        self.__usages()
        self._is_valid = ('host' in self.parameters)
        if self._is_valid:
            self.host = self.parameters.get('host')
            self.format = self.parameters.get('format', self.default_format)
            self.output_folder = config.get('grapher.output')

    def __usages(self):
        pass
        self.parameters_description = {
            'host': {
                'description': 'The ansible host to graph dependencies.',
                'required': True,
            },
            'format': {
                'description': 'The ansible host to graph dependencies.',
                'required': False,
                'default': self.default_format
            },
            'inventory': {
                'description': 'The ansible host to graph dependencies.',
                'required': False,
            },
        }
        host = 'db_prod_11'
        inventory = '~/ansible-ws/tests/data/inventories'
        self.examples.append({
            'desc': f'To generate graph of host {host}',
            'url': f'/sw2/query?query={self.name}&host={host}&inventory={inventory}'
        })

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
            subprocess.run(command, stdout=subprocess.PIPE, check=True, shell=True)
        return img_file
