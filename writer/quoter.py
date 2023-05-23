from .writer import quote
from random import choice

class Quoter:
    def __init__(self):
        self.path = "path/to/file"
    
    def get_quote(self):
        with open(path, 'r') as file:
            lines = file.readlines()
            lines = [l.rstrip() for l in lines]
            return choice(lines)

    def update_quote(self):
        quote = self.get_quote()


