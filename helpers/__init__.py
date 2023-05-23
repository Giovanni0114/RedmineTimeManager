import sys
from database import close_db
from loguru import logger
from .get_time import *
from writer import writer

def EXIT(exit_code : int = 0 ) -> None:
    close_db()
    logger.info("App closed")
    sys.exit(exit_code)

def ERROR(text):
    writer.panel_write(text, "red") 
    logging.error(text)

