from loguru import logger
from abc import ABC,  abstractmethod
import sqlite3
import os

class Database:
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
            "CREATE TABLE IF NOT EXISTS Issues (id INTEGER, issueName TEXT);", 
            "CREATE TABLE IF NOT EXISTS Records (id INTEGER PRIMARY KEY AUTOINCREMENT, timeSpend REAL, issueId INT, comment TEXT, FOREIGN KEY (issueId) REFERENCES Issues (id));", 
            "CREATE TABLE IF NOT EXISTS Storage (id INTEGER PRIMARY KEY AUTOINCREMENT, recordId INT, data TIMESTAMP,FOREIGN KEY (recordId) REFERENCES Records (id))" 
        ]

class DatabaseEntity(ABC):
    @abstractmethod
    def get_entity(self, id: int) -> DatabaseObject:
        pass

    @abstractmethod
    def delete_entity(self, id: int) -> bool:
        pass

    @abstractmethod
    def create_entity(self, values: dict[str, ...]) -> DatabaseObject:
        pass

    @abstractmethod
    def update_entity(self, changes : dict):
        pass
    
    @abstractmethod
    def validate_values(self, values: dict[str, ...]) -> bool:
        pass

class DatabaseObject(ABC):
    entity: DatabaseEntity

    @abstractmethod
    def __repr__(self):
        pass







