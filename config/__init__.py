from loguru import logger
from helpers import exit_program
from redminelib import Redmine
from pydantic import BaseSettings, Field
from datetime import datetime


class RTMSettings(BaseSettings):
    ADDRESS: str
    API_KEY: str
    DAILY: datetime.timestamp

def parse_config():
    logger.info("Parsing config.ini started")
    config = configparser.ConfigParser()

    absolute_path = os.path.abspath(__file__)
    config.read(os.path.dirname(absolute_path) + "config/config.ini")

    # Check if config.ini is valid.
    try:
        redmine_conf = config['REDMINE']
        redmine_conf['ADDRESS']
        redmine_conf['API_KEY']
        redmine_conf['DAILY']
        redmine_conf['EXCLUDE']
    except KeyError:
        logger.error("Error occured during parsing config.ini")

        raise Exception("Plik konfiguracyjny jest uszkodzony lub nie został poprawnie wypełniony.")
        exit_program(1)

    logger.info("Parsowanie ukończone.")

    # Setup frame title: display <orange>CZASOINATOR <white>- <red>{split address from config}

    # Make a connection to Redmine.
    logger.info(f"Próba połączenia z serwerem {redmine_conf['ADDRESS']}...")
    redmine = Redmine(redmine_conf["ADDRESS"], key=redmine_conf["API_KEY"])

    return redmine, redmine_conf, frame_title


redmine, redmine_conf, frame_title = parse_config()
