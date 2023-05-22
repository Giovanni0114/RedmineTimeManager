from typing import List, Callable
from writer import Writer

class Option:
    text: str
    index: int
    callout : Callable

    def __init__(self, index: int, text: str):
        self.text = text
        self.index = index
    
    def __repr__(self):
        return f"[{self.index}] {self.text}"


class MainMenu:
    options: List[str]
    color : str = "light_blue"
    
    def __init__(self):
        self.options.append(Option(1, "Start timer on ceratin issue"))
        self.options.append(Option(2, "Check today progress"))
        self.options.append(Option(3, "Check yesterday progress"))
        self.options.append(Option(4, "Add time to issue manually"))
        self.options.append(Option(5, "Check issuess assigned to you"))
        self.options.append(Option(6, "Stats"))
        self.options.append(Option(7, "Exit"))

    def generate_list():
        header = "\nChoose action to perform: \n"
        return header + "\n".join(self.options)

    def write_menu():
        Writer.write_panel(self.generate_list(), color)



