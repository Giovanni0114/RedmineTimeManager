from redminelib import Redmine
from redminelib import exceptions
import sys


class Redminer(Redmine):
    def __init__(self, addr: str, key: str, n: int = 0):
        logger.info(f"Connecting to server {addr}...")
        try:
            self = Redmine(addr, key)
        except exceptions.BaseRedmineError:
            if n == 3:
                print("App is unable to connect with Redmine server. Check your internet connection")
                sys.exit(1)
            print("Connection seems to be failed. Trying again")
            self = Redminer(addr, key, n+1)
