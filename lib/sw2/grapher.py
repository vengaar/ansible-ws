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
        self.default_format = self.config.get('grapher.format')
        self.output_folder = config.get('grapher.output')
        self.__usages()
        self.check_parameters()

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
        parameters = {
            'host': 'db_prod_11',
            'inventory': '~/ansible-ws/tests/data/inventories',
        }
        self.add_example('To generate graph of host {host}', parameters)

    def query(self):
        """
        """
        host = self.get('host')
        format = self.get('format')
        p_inventory = self.get('inventory')
        inventory = '' if p_inventory is None else f' -i {p_inventory}'
        img_file = f'{self.output_folder}/{host}.{format}'
        command = [f'ansible-inventory-grapher {host}{inventory} | dot -T{format} > {img_file}']
        self.logger.debug(command)
        with open(img_file, 'wb+') as out:
            subprocess.run(command, stdout=subprocess.PIPE, check=True, shell=True)
        return img_file
