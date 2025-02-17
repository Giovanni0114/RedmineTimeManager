import re
import logger

# File imports
from config.setup_config_and_connection import redmine, frame_title
from database.setup_db import cursor, conn
from helpers.get_today_or_yesterday import get_time
from helpers.colors import get_color
from helpers.error_handler import display_error

def add_manually_to_redmine():
    current_time, _, today = get_time()
    issue_id = input("\nPodaj numer zadania > ")

    console.print("",
                  Panel(Text(f"\nWybrano zadanie: {issue_name}\n", justify="center", style="white"),
                        style=get_color("light_blue"), title=frame_title))

    question = input("\nKontynuować? T/n > ")

    if question.lower() == "t" or question == "":

        # This variable is used in database.
        time_elapsed = input("\nPodaj czas spędzony nad zadaniem w formacie H:MM - np 2:13 > ")

        # Check if user pass time in correct format.
        if not bool(re.match(r"\d:\d\d", time_elapsed)):
            display_error("Nieprawidłowa wartość dla pola: Spędzony czas")
            return

        # Convert H:MM to float - eg 0:45 -> 0.80
        hours, minutes = time_elapsed.split(":")
        float_time_elapsed = round((int(hours) + float(minutes) / 60), 2)

        comment = input("Dodaj komentarz > ")
        # Catch problems with connection, permissions etc.
        try:
            redmine.time_entry.create(issue_id=issue_id, spent_on=today,
                                      hours=float_time_elapsed, activity_id=8, comments=comment)
        except Exception as e:
            console.print(f"Wystąpił błąd przy dodawaniu czasu do redmine - {e}")

        logger.info(
            f"Dodano manualnie przepracowany czas do redmine pod zadaniem #{issue_id} - {time_elapsed} godzin.")
        # Insert user work to database.
        cursor.execute("INSERT INTO BAZA_DANYCH (DATA, NUMER_ZADANIA, NAZWA_ZADANIA, SPEDZONY_CZAS, KOMENTARZ) VALUES "
                       "(?, ?, ?, ?, ?)", (current_time, issue_id, issue_name, float_time_elapsed, comment,))
        logger.info(
            f"Umieszczono w bazie danych dodany manualnie przepracowany czas pod zadaniem "
            f"#{issue_id} - {float_time_elapsed} godzin.")

        # Apply changes and close connection to sqlite database.
        conn.commit()
        logger.info("Zakommitowano zmiany w bazie danych.")

        console.print("", Panel(Text(f"\nDodano!"
                                     f"\n\nSpędzony czas: {hours} godzin, {minutes} minut."
                                     f"\nKomentarz: {comment}\n", justify="center", style="white"),
                                style=get_color("green"),
                                title=frame_title))
