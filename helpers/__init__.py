import sys
from database import close_db
from loguru import logger
from .colors import COLORS

def exit_program(exit_code : int = 0 ) -> None:
    close_db()
    logger.info("App closed")
    sys.exit(exit_code)


