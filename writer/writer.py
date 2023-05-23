from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .colors import get_color

quote = ""
frame_title = f"[{get_color('bold_orange')}] RedmineTimeManager [{get_color('white')}]" \
              f"- [{get_color('bold_red')}]{quote}"

class Writer:
    console : Console

    def __init__(self):
        self.console = Console()

    def write_panel(*, text: str, color: str):
        self.console.print(
            Panel( Text(f"\n{text}\n", justify="center", style="white"), 
                style=get_color(color), title=frame_title))

