from .config import settings

from writer import writer
from interface import MainMenu
from redminer import redminer

def main():
    redminer.init(settings.ADDRESS, settings.API_KEY)

    menu = MainMenu() 

    while True:
        if info is True:
            menu.write_menu()
            info = False
    
        symbol = input("\nWybór > ")
        menu.choose(symbol)       

if __name__ == "__main__":
    main()
