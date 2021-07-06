import datetime
from redminelib import Redmine
import redminelib.exceptions
import calendar
import time
from datetime import date
import os
import sqlite3
from rich import print as print
from rich.panel import Panel
from rich.text import Text
from rich.color import Color
from rich.console import Console
from rich.table import Table
import configparser
from deep_translator import GoogleTranslator

stop = ""
choose = 0
info = False
console = Console()


def throw_403():
    print("")
    print(Panel(Text(f"\n403 - Brak dostępu do wybranego zadania!\n", justify="center", style="bold #ff4242"),
                title="[bold orange3]CZASOINATOR"))
    return


def invalid_time_value():
    print("")
    print(Panel(Text(f"\nNieprawidłowa wartość dla pola: Spędzony czas\n", justify="center", style="bold #ff4242"),
                title="[bold orange3]CZASOINATOR"))
    return


def throw_404():
    print("")
    print(Panel(Text(f"\n404 - Wybrane zadanie nie istnieje!\n", justify="center", style="bold #ff4242"),
                title="[bold orange3]CZASOINATOR"))
    return


def get_time():
    # Get and format current date
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Check if today is monday - used for valid "yesterday" when it's weekend:
    if now.weekday() == 0:
        yesterday = now - datetime.timedelta(days=3)
        yesterday = str(yesterday).split(" ")[0]
    else:
        # If today is monday, yesterday is friday.
        yesterday = now - datetime.timedelta(days=1)
        yesterday = str(yesterday).split(" ")[0]

    # Split current time from 2021-12-10 22:32:52 to 2021-12-10
    today = current_time.split(" ")[0]

    return current_time, yesterday, today


def init():
    # Set configparser, read config and setup redmine_conf variable
    config = configparser.ConfigParser()
    config.read("config.ini")
    redmine_conf = config['REDMINE']

    return redmine_conf


def get_started(redmine_conf):
    global choose
    global info
    # Info variable is being used to show user a legend of possible options.
    if not info:
        # Show rich panel
        print(Panel(Text("\nWybierz co chcesz zrobić:\n"
                         "\n1. Uruchom zliczanie czasu"
                         "\n2. Sprawdź dzisiejsze postępy"
                         "\n3. Sprawdź wczorajsze postępy"
                         "\n4. Dorzuć ręcznie czas do zadania"
                         "\n5. Dorzuć ręcznie czas do bazy - własne zadanie"
                         "\n6. Statystyki"
                         "\n7. Wyjście\n", justify="center"), title="[bold orange3]CZASOINATOR"))

        # Turn off info after showing legend once.
        info = True

    # Ask user to choose a module
    choose = input("\nWybór > ")
    # Make a connection to Redmine.
    redmine = Redmine(redmine_conf["ADDRESS"], key=redmine_conf["API_KEY"])
    # Set up sqlite
    conn = sqlite3.connect(f"czasoinator.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS BAZA_DANYCH (DATA TEXT, NUMER_ZADANIA TEXT, "
        "NAZWA_ZADANIA TEXT, SPEDZONY_CZAS TEXT, KOMENTARZ TEXT);")
    return redmine, cursor, choose, conn


def issue_stopwatch(redmine, cursor, conn):
    # stop variable is used to stop the stopwatch.
    stop = ""

    issue_id = input("\nPodaj numer zadania > ")

    # Start stopwatch
    start_timestamp = int(calendar.timegm(time.gmtime()))

    # Get issue name
    try:
        issue_name = str(redmine.issue.get(issue_id))
    except redminelib.exceptions.ForbiddenError:
        throw_403()
        return
    except redminelib.exceptions.ResourceNotFoundError:
        throw_404()
        return

    # Show rich panel
    print("", Panel(Text(f"\nWybrano zadanie: {issue_name}\n", justify="center"), title="[bold orange3]CZASOINATOR"),
          "")

    # Wait for input
    while stop != "k":
        stop = console.input(
            '[bold #25ba14]Rozpoczęto mierzenie czasu![/bold #25ba14] \n\nGdy zakończysz pracę nad zadaniem wpisz [bold #25ba14]k[/bold #25ba14], lub [bold #e81313]x[/bold #e81313] aby anulować > ')
        if stop.lower() == "x":
            return

    # Stop stopwatch and calculate timestamp to hours eg. 2.63
    stop_timestamp = int(calendar.timegm(time.gmtime()))
    time_elapsed = round(((stop_timestamp - start_timestamp) / 60 / 60), 2)

    # Show rich panel
    print("", Panel(
        Text(f"\nZakończono pracę nad #{issue_id}!\n Spędzony czas: {time_elapsed} godzin.\n ", justify="center"),
        title="[bold orange3]CZASOINATOR"))

    comment = input("\nDodaj komentarz > ")

    if input("Dodać czas do zadania w redmine? t/n > ").lower() == "t":

        # Catch problems with connection, permissions etc.
        try:
            redmine.time_entry.create(issue_id=issue_id, spent_on=date.today(),
                                      hours=time_elapsed, activity_id=8, comments=comment)

            # Translate comment from user input above
            translated_comment = GoogleTranslator(source="auto", target="en").translate(comment)

            # Show rich panel
            print("", Panel(Text(f"\nDodano!"
                                 f"\n\nSpędzony czas: {time_elapsed}"
                                 f"\nKomentarz: {comment}\n"
                                 f"\nPamiętaj o git commit -m \"TASK#{issue_id}: {translated_comment}\" && git push",
                                 justify="center"), title="[bold orange3]CZASOINATOR"))
        except Exception as e:
            print(f"Wystąpił błąd przy dodawaniu czasu do redmine - {e}")

    current_time, _, _ = get_time()

    # Insert user work to database
    cursor.execute(f"INSERT INTO BAZA_DANYCH (DATA, NUMER_ZADANIA, NAZWA_ZADANIA, SPEDZONY_CZAS, KOMENTARZ) VALUES "
                   f"(?, ?, ?, ?, ?)", (current_time, issue_id, issue_name, time_elapsed, comment))

    # Apply changes and close connection to sqlite database
    conn.commit()


def show_work(cursor, redmine_conf, day):
    """
    Some magic happeened here!
    With user input from get_started() day variable is set to today or yesterday.
    It's set by choosing in "if __name__ == __main__" by get_time function
    which returns current time, yesterday and today.
    """
    # This variable store information about doing anything before daily
    info_daily = False
    # Replace 11:00:00 from config.ini to 110000
    daily = redmine_conf["DAILY"].replace(":", "")

    # Send query to get data from today
    cursor.execute("SELECT * FROM BAZA_DANYCH WHERE DATA LIKE ?", (f"%{day}%",))

    # Fetch data from query above
    rows = cursor.fetchall()

    # Empty rows variable means there's no SQL entries.
    if not rows:
        # Show rich panel
        print("", Panel(Text("\n Brak postępów! \n", justify="center"), title="[bold orange3]CZASOINATOR"))

        return

    # Generate column to show data from sql
    table = Table(show_header=True, header_style='bold #c071f5',
                  title=f'[bold #2070b2]POSTĘPY DNIA {day}', show_lines=True)
    table.add_column("Data rozpoczęcia", justify="center")
    table.add_column("Nazwa zadania", justify="center")
    table.add_column("Spędzony czas", justify="center")
    table.add_column("Komentarz", justify="center")
    table.add_column("Numer zadania", justify="center")

    for row in rows:

        # Set up colors for spent time.
        # 00:00-02:00 - Green
        # 02:00-04:00 - Orange
        # 04:00+ - Red
        if float(row[3]) <= 2.00:
            color = "bold #25ba14"  # Green
        elif float(row[3]) <= 4.00:
            color = "bold #d99011"  # Orange
        else:
            color = "bold #ff4242"  # Red

        # Split row with date: 24-11-2021 14:20:52 -> 14:20:52
        # Drop ":" from splitted data above, and compare it with daily variable
        # Also check if "daily lines" are displayed before
        if row[0].split(" ")[1].replace(":", "") > daily and info_daily is False:
            table.add_row(f'{day} {redmine_conf["DAILY"]}', '[bold #ff00ee]Daily![/bold #ff00ee]', '', '',
                          f'')
            info_daily = True

        # row_1 = row[1] is for text-formatting purposes. eg # 20000 or "Empty issue number"
        row_1 = row[1]

        # Same as above, eg 4.86 -> 04:51.
        time = float(row[3])
        minutes = 60 * (time % 1)
        time = "0%d:%02d" % (time, minutes)

        # Append row to table with recognizing that info about work has issue number
        if row_1 is None:
            table.add_row(row[0], row[2], f"[{color}]{time}[/{color}]", row[4], f"[bold #ff4242]Brak![/bold #ff4242]")
        else:
            table.add_row(row[0], row[2], f"[{color}]{time}[/{color}]", row[4],
                          f"[#6bb0c9][link={redmine_conf['ADDRESS']}/issues/{row[1]}]#{row[1]}[/link][/#6bb0c9]")

    # Show table with work time
    console.print(table)

    # Close connection to database
    conn.close()


def add_manually_to_database(redmine, cursor):
    current_time, _, today = get_time()
    issue_id = input("\nPodaj numer zadania > ")

    # Get issue name
    try:
        issue_name = str(redmine.issue.get(issue_id))

    except redminelib.exceptions.ForbiddenError:
        throw_403()
        return

    except redminelib.exceptions.ResourceNotFoundError:
        throw_404()
        return

    # Show rich panel
    print("",
          Panel(Text(f"\nWybrano zadanie: {issue_name}\n", justify="center"), title="[bold orange3]CZASOINATOR"))

    question = input("\nKontynuować? t/n > ")

    if question.lower() == "t":

        try:
            time_elapsed = float(input("\nPodaj czas spędzony nad zadaniem - oddzielony kropką np 2.13 > "))
        except ValueError:
            invalid_time_value()
            return

        comment = input("Dodaj komentarz > ")
        # Catch problems with connection, permissions etc.
        try:
            redmine.time_entry.create(issue_id=issue_id, spent_on=today,
                                      hours=time_elapsed, activity_id=8, comments=comment)
        except Exception as e:
            print(f"Wystąpił błąd przy dodawaniu czasu do redmine - {e}")

        # Insert user work to database.
        cursor.execute(f"INSERT INTO BAZA_DANYCH (DATA, NUMER_ZADANIA, NAZWA_ZADANIA, SPEDZONY_CZAS, KOMENTARZ) VALUES "
                       f"(?, ?, ?, ?, ?)", (current_time, issue_id, issue_name, time_elapsed, comment,))

        # Apply changes and close connection to sqlite database.
        conn.commit()
        conn.close()

        # Show rich panel
        print("", Panel(Text(f"\nDodano!"
                             f"\n\nSpędzony czas: {time_elapsed}"
                             f"\nKomentarz: {comment}\n", justify="center"), title="[bold orange3]CZASOINATOR"))


def add_own_to_database(cursor):
    current_time, _, _ = get_time()

    issue_name = input("\nPodaj nazwę zadania > ")
    try:
        time_elapsed = float(input("\nPodaj czas spędzony nad zadaniem - oddzielony kropką np 2.13 > "))
    except ValueError:
        invalid_time_value()
        return
    # Insert user work to database.
    cursor.execute(f"INSERT INTO BAZA_DANYCH (DATA, NAZWA_ZADANIA, SPEDZONY_CZAS) VALUES "
                   f"(?, ?, ?)", (current_time, issue_name, time_elapsed,))

    # Apply changes and close connection to sqlite database.
    conn.commit()
    conn.close()

    # Show rich panel
    print("", Panel(Text(f"\nDodano!"
                         f"\n\nNazwa Zadania: {issue_name}"
                         f"\nSpędzony czas: {time_elapsed}\n", justify="center"), title="[bold orange3]CZASOINATOR"))


def stats(cursor):
    cursor.execute("SELECT SPEDZONY_CZAS FROM BAZA_DANYCH")
    rows = cursor.fetchall()
    total_hours = 0

    for row in rows:
        total_hours += float(row[0])
    total_hours = round(total_hours, 2)

    # Show rich panel
    print("", Panel(Text(f"\n Czas spędzony z CZASOINATOREM: {total_hours} \n", justify="center"),
                    title="[bold orange3]CZASOINATOR"))


if __name__ == "__main__":
    redmine_conf = init()
    while choose != str(7):
        redmine, cursor, choose, conn = get_started(redmine_conf)
        if choose == str(1):
            issue_stopwatch(redmine, cursor, conn)
        if choose == str(2):
            _, _, day = get_time()
            show_work(cursor, redmine_conf, day)
        if choose == str(3):
            _, day, _ = get_time()
            show_work(cursor, redmine_conf, day)
        if choose == str(4):
            add_manually_to_database(redmine, cursor)
        if choose == str(5):
            add_own_to_database(cursor)
        if choose == str(6):
            stats(cursor)
        if choose == "?":
            info = False
