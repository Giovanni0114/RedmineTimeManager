from .main_menu import MainMenu
from .writer import Writer
from .plugins import PluginFactory
from dataclasses import dataclass

@dataclass
class Interface:
    menu: MainMenu
    writer: Writer

    def __init__(self):
        self.menu = MainMenu()
        

