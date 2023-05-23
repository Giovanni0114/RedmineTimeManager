from loguru import logger

import sqlite3
import os

def setup_connection_and_cursor():
    absolute_path = os.path.abspath(__file__)
    conn = sqlite3.connect(os.path.dirname(absolute_path) + "db.sqlite")
    cursor = conn.cursor()

    return conn, cursor

def create_structure(cursor: sqlite3.Cursor):
    cursor.execute( "PRAGMA foreign_keys = ON;" ) 

    # create Isuues table
    cursor.execute( "CREATE TABLE IF NOT EXISTS Issues "
                    "(id INTEGER, issueName TEXT);")

    # create Records table
    cursor.execute( "CREATE TABLE IF NOT EXISTS Records "
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, timeSpend REAL, issueId INT, comment TEXT, "
                     "FOREIGN KEY (issueId) REFERENCES Issues (id));")

    # create Storage table
    cursor.execute( "CREATE TABLE IF NOT EXISTS Storage"
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, recordId INT, data TIMESTAMP,"
                    "FOREIGN KEY (recordId) REFERENCES Records (id))")

