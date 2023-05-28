from ..database.database import DatabaseEntity, DatabaseObject
from ..database.connector import DBConnector
from datetime import datetime, date
from .issue import Issue, IssueDatabaseEntity

class RecordDatabaseEntity(DatabaseEntity):
    def get_entity(self, id):
        return DBConnector

    def create_entity(self, values: dict[str, ...]) -> Record:
        if not self.validate_values(values):
            raise Exception("Validaition for records failed!")
        
        return Record(values)

    def validate_values(self, values: dict[str, ...]) -> bool:
        if not isinstance(values["id"], int):
            return False

        if not isinstance(values["issueId"], int):
            return False

        if not isinstance(values["timeSpend"], float):
            return False

        if not isinstance(values["comment"], str):
            return False

        return True

class Record(DatabaseObject):
    id: int
    time: date
    issue: Issue
    comment : str

    def __init__(self, values: dict[str, ...]):
        self.id = values["id"]
        self.timeSpend = values["timeSpend"]
        self.issue = IssueDatabaseEntity
        self.comment = values["comment"]

    def __repr__(self):
        return f"Record id: {self.id}, time: {self.time:r}, Issue: [{self.issue:r}]"



