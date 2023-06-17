from ..database.database import DatabaseEntity
from datetime import datetime, date
from .record import Record
from .float_time import FloatTime

class Storage:
    id: int
    date: datetime
    records: list[Record]

    def __init__(self, values: dict[str, ...]):
        self.id = values["id"]
        self.date = datetime.fromtimestamp(values["date"])
        
        print(f"Created: {self}")
    
    def get_values(self) -> dict[str, ...]:
        return {
            "id" : self.id,
            "date": self.data,
            "recordId": self.records[0].id if len(self.records) > 0 else -1
        }

    def get_summary_timespend(self) -> FloatTime:
        return sum([r.timeSpend for r in self.records])

    def get_all_comments(self) -> list[str]:
        return [r.comment for r in self.records]

    def __repr__(self):
        return f"Storage id: {self.id}, date: {self.date}, time spend: {self.get_summary_timespend()}, no. commments: {len(self.get_all_comments())} Issue: [{self.issue}]"


class StorageDatabaseEntity(DatabaseEntity):
    obj = Storage
    types = {
        "id": int,
        "date": int,
        "recordId": int
    }

