from redminelib import Redmine
from redminelib import exceptions
from loguru import logger
from .issue import Issue

class Redminer:
    redmine: Redmine

    def init(self, addr: str, key: str, n: int = 0):
        logger.info(f"Connecting to server {addr}...")
        try:
            self.redmine = Redmine(addr, key)
        except exceptions.BaseRedmineError:
            if n == 3:
                print("App is unable to connect with Redmine server. Check your internet connection")
                sys.exit(1)
            print("Connection seems to be failed. Trying again")
            self.init(addr, key, n+1)

    def get_issue(id: int) -> Issue:
        try:
            issue_name = str(self.issue.get(issue_id))
        except exceptions.ForbiddenError:
            display_error("403 - Issue Forbidden!")
            return

        except exceptions.ResourceNotFoundError:
            display_error("404 - Issue Not Found!")
            return

        return Issue(id, issue_name)

