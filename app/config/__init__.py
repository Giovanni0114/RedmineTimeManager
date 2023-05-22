from loguru import logger
from helpers import exit_program
from redminelib import Redmine
from pydantic import BaseSettings, Field
from datetime import datetime, time

class RTMSettings(BaseSettings):
    ADDRESS: str
    API_KEY: str
    DAILY: time

    def __init__(self):
        config = configparser.ConfigParser()
    
        absolute_path = os.path.abspath(__file__)
        config.read(os.path.dirname(absolute_path) + "config/config.ini")
    
        try:
            self.ADDRESS = config['REDMINE']['ADDRESS']
            self.API_KEY = config['REDMINE']['API_KEY']
            self.DAILY = datetime.strptime(config['REDMINE']['DAILY'], "%H:%M:%S") 
        except KeyError:
            logger.error("Error occured during parsing config.ini")
    
            raise Exception("The configuration file is corrupted or has not been properly filled out")
            exit_program(1)
    

