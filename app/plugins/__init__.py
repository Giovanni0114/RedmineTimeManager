from typing import List, Callable
import json
import os
import sys


class Plugin:
    label: str
    symbol: str
    action: Callable

    def __init__(self, json_obj):
        self.label = json_obj["description"]
        self.symbol = json_obj["symbol"]
        module = json_obj["module"]

        sys.path.append(os.path.dirname(__file__) + "/src")
    
        self.action = __import__(module).action

class PluginFactory:
    def __init__(self):
        self.manifest = self.get_manifest()

    def get_plugins(self) -> List[Plugin]:
        return [Plugin(plg) for plg in self.manifest.values()]

    def get_manifest(self) -> json:
        absolute_path = os.path.abspath(__file__)
        with open(os.path.dirname(absolute_path) + "/manifest.json") as manifest_file:
            return json.load(manifest_file)  
