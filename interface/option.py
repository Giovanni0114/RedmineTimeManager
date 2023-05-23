from typing import Callable
from plugins import Plugin, PluginFactory

class Option:
    plugin: Plugin
        
    def __init__(self, plugin: Plugin):
        self.plugin = plugin

    @property
    def action(self):
        return self.plugin.action

    def __repr__(self) -> str:
        return f"[{self.plugin.symbol}] {self.plugin.label}"


