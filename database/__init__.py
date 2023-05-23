from .setup import setup_connection_and_cursor, create_structure
from loguru import logger

cursor = None
conn = None

def close_db():
    logger.info("DB closed")
    conn.close()

def db_init():
    conn, cursor = setup_connection_and_cursor()
    create_structure(cursor)

