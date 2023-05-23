from .redminer import Redminer
from dataclasses import dataclass

import sys

redminer = None

class FloatTime:
    value: float

    def __repr__(self):
        return f"{int(self.value)}:{(self.value * 60 % 60):02}"

@dataclass
class Issue:
    id: int
    name: str
    time_total: FloatTime
    
    def add_time(self, delta: float):
        self.time_total.value += delta

    def commit(self):
        ...

def redmine_init(addr, key):
    redminer = Redminer(addr, key)

