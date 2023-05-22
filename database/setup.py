from loguru import logger

import sqlite3
import os

def setup_connection_and_cursor():
    absolute_path = os.path.abspath(__file__)
    conn = sqlite3.connect(os.path.dirname(absolute_path) + "database/db.sqlite")
    cursor = conn.cursor()

    # make sure foreign keys is active
    cursor.execute(
        "PRAGMA foreign_keys = ON;"
    ) 

    # create Isuues table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS"
        "Issues (id INTEGER, issueName TEXT);"
    )

    # create Storage table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS"
        "Storage (id INTEGER PRIMARY KEY AUTOINCREMENT, issueId INTEGER , data TIMESTAMP, timeSpend TEXT, comment TEXT, "
            "FOREIGN KEY (issueId) REFERENCES) Issues (id);"
    )
    logger.info("Database created")
    return conn, cursor
