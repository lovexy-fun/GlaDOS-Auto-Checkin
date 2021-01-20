import os
import configparser

class Config:
    '''
    参数配置
    '''

    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError('Not Found File:' + config_file)
        self._config = configparser.RawConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

config = Config()