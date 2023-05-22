from .option import Option
from typing import Dict
from writer import Writer

class MainMenu:
    options: Dict[int, Option]
    color: str = "light_blue"

    def __init__(self):
        self.options.update({1: Option("Start timer on ceratin issue")})
        self.options.update({2: Option("Check today progress")})
        self.options.update({3: Option("Check yesterday progress")})
        self.options.update({4: Option("Add time to issue manually")})
        self.options.update({5: Option("Check issuess assigned to you")})
        self.options.update({6: Option("Stats")})
        self.options.update({7: Option("Exit")})

    def generate_list():
        header = "\nChoose action to perform: \n"
        return header + "\n".join(self.options)

    def write_menu():
        Writer.write_panel(self.generate_list(), color)


