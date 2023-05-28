
from ..database.database import DatabaseObject, DatabaseEntity
from dataclasses import dataclass
from .float_time import FloatTime

class IssueDatabaseEntity(DatabaseEntity):
    def get_entity(self, id):
        return Issue({})

    def create_entity(self, values: dict[str, ...]) -> Record:
        if not self.validate_values(values):
            raise Exception("Validaition for records failed!")
        return Issue(values)

    def validate_values(self, values: dict[str, ...]) -> bool:
        if not isinstance(values["id"], int):
            return False

        if not isinstance(values["name"], str):
            return False

        return True


@dataclass
class Issue:
    id: int
    name: str
    time_total: FloatTime
 
    def __init__(self, values : dict[str, ...]):
        self.id = values["id"]
        self.name = values["name"]


    def add_time(self, delta: float):
        self.time_total.value += delta
