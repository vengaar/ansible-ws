"""
"""
import  subprocess

import ansible_ws
from ansible_ws.ansible_web_service import AnsibleWebService, AnsibleWebServiceConfig

class AnsibleWebServiceInvnetoryGrapher(AnsibleWebService):
    """
    """

    def __init__(self, config_file, query_strings):
        super().__init__(config_file, query_strings)

    def run(self):
        
        inventory = self.get_param('inventory')
        target = self.get_param('target')
        grapher_dir = AnsibleWebServiceConfig().get('grapher_dir')
        svg = f'{grapher_dir}/{target}.svg'
        try:
            cmd = f'ansible-inventory-grapher -i {inventory} {target} | dot -Tsvg'
            self.logger.debug(cmd)
            with open(svg, 'w') as output: 
                with subprocess.Popen(cmd, stdout=output, shell=True) as p:
                    p.wait()
        except:
            self.logger.debug(f'Imposible to generate graph for {target} with {inventory}')
        self.result = svg
