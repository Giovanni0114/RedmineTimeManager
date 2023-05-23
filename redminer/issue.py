from dataclasses import dataclass
from .float_time import FloatTime

@dataclass
class Issue:
    id: int
    name: str
    time_total: FloatTime
    
    def add_time(self, delta: float):
        self.time_total.value += delta
