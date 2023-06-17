from .database import db_connection

class DBConnector:
    def get_entity_values(self, name: str, id: int):
        with db_connection() as db:
            querry = "SELECT * FROM ? where id = ?"
            return db.execute(querry, [name, id])
        
    def create_empty_db_object(self, name: str) -> int:
        with db_connection() as db:
            querry = "INSERT INTO ? ;"

    def delete_db_object(self, name: str, id: int):
        with db_connection() as db:
            querry = "DELETE FROM ? WHERE id = ?;"
            return db.execute(querry, [id])

    def update_db_object(self, name: str, id: int,  diff: dict[str, ...]):
        with db_connection() as db:
            querry = "UPDATE ? SET ? WHERE id = ?;"
            values = ",".join(["=".join([str(i) for i in item]) for item in diff.items()])
            return db.execute(querry, [name, values, id])

    def create_db_object(self, name: str, values: dict[str, ...]):
        with db_connection() as db:
            querry = "INSERT INTO ? (?) VALUES ?;"
            keys = values.keys()
            vals = values.values()
            return db.execute(querry, [name, keys, vals])

