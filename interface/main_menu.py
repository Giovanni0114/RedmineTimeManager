from .option import Option
from typing import Dict
from writer import writer
from plugins import PluginFactory


class MainMenu:
    options: Dict[str, Option]

    def __init__(self):
        factory = PluginFactory()
        for plugin in factory.get_plugins():
            self.options[plugin.symbol] = Option(plugin)

    def generate_list():
        header = "\nChoose action to perform: \n"
        return header + "\n".join(self.options)

    def write_menu():
        writer.write_panel(self.generate_list(), "light_blue")

