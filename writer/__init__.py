from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from .colors import get_color

writer = None

frame_title = f"[{get_color('bold_orange')}]CZASOINATOR [{get_color('white')}]" \
              f"- [{get_color('bold_red')}]{redmine_conf['ADDRESS'].split('://')[1]}"
class Writer:
    console : Console

    def __init__(self):
        self.console = Console()

    def write_panel(*, text: str, color: str):
        self.console.print(
            Panel(
                Text(f"\n{text}\n", justify="center", style="white"), 
                style=get_color(color), title=frame_title)
            )

def writer_init():
    writer = Writer()
