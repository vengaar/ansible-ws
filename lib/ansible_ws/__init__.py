import logging
import yaml


class AnsibleWebServiceConfig(object):

    CONFIG_FILE = '/etc/ansible-ws/ansible-ws.yml'

    def __init__(self, config_file=CONFIG_FILE):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            with open(self.CONFIG_FILE) as configfile:
                self.config = yaml.load(configfile)
                self.logger.debug(self.config)
                self.logger.info(f'Configuration file {self.CONFIG_FILE} LOADED')
        except Exception:
            self.logger.error(f'Not possible to load configuration file {self.CONFIG_FILE}')

    def get(self, keys):
        value = self.config
        for key in keys.split('.'):
            value = value[key]
        return value
