from typing import List, Callable
import json
import os

class Plugin:
    label: str
    symbol: str
    action: Callable

    def __init__(self, json_obj):
        self.label = self.get_manifest()[plg]["description"]
        self.symbol = self.get_manifest()[plg]["symbol"]
        path_to_actions = self.get_manifest()[plg]["path"]
        self.action = __import__(path_to_actions).action

class PluginFactory:
    registered_plugins : List[str]

    def __init__(self):
        self.manifest = self.get_manifest()
        self.register_plugins_from_manifest()

    def get_plugins(self) -> List[Plugin]:
        return [Plugin(self.manifest()[plg]) for plg in self.registered_plugins]

    def register_plugins_from_manifest(self):
        self.registered_plugins = [plugin["name"] for plugin in self.manifest()] 

    def get_manifest(self) -> json:
        absolute_path = os.path.abspath(__file__)
        with open(os.path.dirname(absolute_path) + "manifest.json") as manifest_file:
            return json.load(manifest_file)  
