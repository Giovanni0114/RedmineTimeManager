from .setup import setup_connection_and_cursor
from loguru import logger

conn, cursor = setup_connection_and_cursor()

def close_db():
    logger.info("DB closed")
    conn.close()


