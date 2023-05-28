from .database import Database

class DBConnector:
    db : Database

    def __init__(self):
       self.db = Database()
    
    def get_entity_values(self, id: int, name: str):
        querry = "SELECT * FROM ? where id = ?"
        return self.db.execute(querry, [name, id])
        

