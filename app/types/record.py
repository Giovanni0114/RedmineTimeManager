from ..database.database import DatabaseEntity
from ..database.connector import DBConnector
from datetime import datetime, date
from .issue import Issue, IssueDatabaseEntity
from .float_time import FloatTime

class Record:
    id: int
    timeSpend: FloatTime
    issue: Issue
    comment : str

    def __init__(self, values: dict[str, ...]):
        self.id = values["id"]
        self.timeSpend = values["timeSpend"]
        self.issue = IssueDatabaseEntity.get_entity(values["Issues.id"])    
        self.comment = values["comment"]
    
    def get_value(self) -> dict[str, ...]:
        return {
            "id": self.id,
            "timeSpend" : self.timeSpend.value,
            "issueId" : self.issue.id,
            "comment" : self.comment
        }

    def __repr__(self):
        return f"Record id: {self.id}, time: {self.time:r}, Issue: [{self.issue:r}]"

class RecordDatabaseEntity(DatabaseEntity):
    obj = Record
    types = {
        "id": int,
        "issueId": int,
        "timeSpend": float,
        "comment": str,
    }



