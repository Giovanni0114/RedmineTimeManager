from ..database.database import DatabaseEntity, DatabaseObject
from datetime import datetime, date
from .record import Record, RecordDatabaseEntity

class StorageDatabaseEntity(DatabaseEntity):
    def get_entity(self, id):
        return Storage({})

    def create_entity(self, values: dict[str, ...]) -> Storage:
        if not self.validate_values(values):
            raise Exception("Validaition for records failed!")
        
        return Storage(values)

    def validate_values(self, values: dict[str, ...]) -> bool:
        if not isinstance(values["id"], int):
            return false

        if not isinstance(values["recordId"], int):
            return false

        try:
            datetime.fromtimestamp(values["data"])
        except TypeError:
            return false
        
        return true

class Storage(DatabaseObject):
    id: int
    datatime: datetime
    record: Record


    def __init__(self, values: dict[str, ...]):
        self.id = values["id"]
        self.timeSpend = values["timeSpend"]
        self.issue = IssueDatabaseEntity
        self.comment = values["comment"]

    def __repr__(self):
        return f"Storage id: {self.id}, time: {self.time:r}, Issue: [{self.issue:r}]"



