from loguru import logger
from pydantic import BaseSettings, Field
from datetime import datetime, time
from configparser import ConfigParser
import os

class RTMSettings:
    ADDRESS: str
    API_KEY: str
    DAILY: time

    def __init__(self):
        config = self.get_config_parser('REDMINE')
        try:
            self.ADDRESS = config['ADDRESS']
            self.API_KEY = config['API_KEY']
            self.DAILY = datetime.strptime(config['DAILY'], "%H:%M:%S") 
        except KeyError:
            ERROR("Error occured during parsing config.ini")
    
    def get_config_parser(self, context: str):
        config = ConfigParser()

        absolute_path = os.path.abspath(__file__)
        config.read(os.path.dirname(absolute_path) + "/config.ini")
        return config[context]
