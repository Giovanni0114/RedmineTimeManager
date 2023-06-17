from loguru import logger
from contextlib import contextmanager
from abc import ABC, abstractmethods
import sqlite3
import os

class SqliteDatabase:
    conn : sqlite3.Connection
    cursor : sqlite3.Cursor

    def __init__(self):
        absolute_path = os.path.abspath(__file__)
        self.conn = sqlite3.connect(os.path.dirname(absolute_path) + "db.sqlite")
        self.cursor = conn.cursor()
    
    def close_db(self):
        self.conn.close()

    def execute(self, querry, args):
        self.cursor.execute(querry, args)
        data = self.cursor.fetchall()
        return data[0] if len(data) == 1 else len(data)

    def create_structure(self):
        queries = [
            "PRAGMA foreign_keys = ON;",   
            "CREATE TABLE IF NOT EXISTS Issues "
            "(id INTEGER, issueName TEXT);", 

            "CREATE TABLE IF NOT EXISTS Records "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, timeSpend REAL, issueId INT, comment TEXT, FOREIGN KEY (issueId) REFERENCES Issues (id));", 

            "CREATE TABLE IF NOT EXISTS Storage "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, recordId INT, date TIMESTAMP, FOREIGN KEY (recordId) REFERENCES Records (id))" 
        ]

@contextmanager
def db_connection():
    db = SqliteDatabase()
    try:
        yield db
    finally:
        db.close_db()

