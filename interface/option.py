from typing import Callable

class Option:
    text: str
    index: int
    action : Callable

    def __init__(self, index: int, text: str):
        self.text = text
        self.index = index
    
    def assign_action(self, action: Callable) -> None:
        self.action = action

    def __repr__(self) -> str:
        return f"[{self.index}] {self.text}"


