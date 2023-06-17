from contextlib import contextmanager
from abc import ABC, abstractmethods
from .connector import DBConnector

class DatabaseEntity(ABC):
    obj : object
    types : dict[str, type]

    @abstractmethod
    def get_entity(self, id) -> obj:
        values = DBConnector.get_entity_values(obj.db_table_name, id)
        if not self.validate_values(values):
            DBConnector.create_db_object(self, name, id)

        return self.obj(values)

    @abstractmethod
    def delete_entity(self, id: int) -> bool:
        return DBConnector.delete_db_object(obj.db_table_name, id)

    @abstractmethod
    def create_entity(self, values: dict[str, ...]) -> bool:
        if not self.validate_values(values):
            return False

        return DBConnector.create_db_object(name, values)

    @abstractmethod
    def update_entity(self, id: int, diff: dict[str, ...]) -> bool:
        if not self.validate_values(diff):
            return False

        return DBConnector.update_db_object(obj.db_table_name, id ) 

    @abstractmethod
    def validate_values(self, values: dict[str, ...]) -> bool:
        for key, val in values.items():
            if not isinstance(val, self.types[key]):
                return False

        return True

