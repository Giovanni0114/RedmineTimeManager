from .config import settings
from interface import MainMenu

def main():
    menu = MainMenu() 

    while True:
        if info is True:
            menu.write_menu()
            info = False
    
        symbol = input("\nWybór > ")
        menu.choose(symbol)       

