from .config import RTMSettings

from interface import MainMenu
from redminer import Redminer


from helpers.get_today_or_yesterday import get_time
from modules.days_off import show_days_off
from modules.issue_stopwatch import start_issue_stopwatch
from modules.show_today_or_yesterday_work import show_work
from modules.add_work_to_redmine import add_manually_to_redmine
from modules.show_work import show_assigned_to_user
from modules.stats import show_stats
from helpers.greet_user import welcome

def main():
    settings = RTMSettings()
    menu = MainMenu() 
    redmine = Redminer(settings.ADDRESS, settings.API_KEY)

    welcome()

    # Main loop of script. Here we have "info" variable, which store True/False about showing options to choose.
    while True:
        if info is True:
            menu.write_menu()
            info = False
    
        choose = input("\nWybór > ")
        
        #1  start_issue_stopwatch()
        #2   show_work(day)
        #3   show_work(yesterday)
        #4   add_manually_to_redmine()
        #5   show_assigned_to_user()
        #6   show_days_off()
        #7   show_stats()
        #8   exit_program()
        #?   info = True

if __name__ == "__main__":
    main()
