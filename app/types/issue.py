from ..database.database import DatabaseEntity
from dataclasses import dataclass
from .float_time import FloatTime
from ..database.connector import DBConnector

@dataclass
class Issue:
    db_table_name: str = "Issues"
    id: int
    name: str
    time_total: FloatTime 

    def __init__(self, values : dict[str, ...]):
        self.id = values["id"]
        self.name = values["name"]

    def add_time(self, delta: float):
        self.time_total.value += delta

class IssueDatabaseEntity(DatabaseEntity):
    obj = Issue
    types = {
        "id" : int, 
        "name" : str, 
        "time_total": float
    }

