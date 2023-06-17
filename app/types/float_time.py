class FloatTime:
    value: float

    def __init__(self, value: float):
        self.value = value

    def __repr__(self) -> str:
        return f"{int(self.value)}:{(self.value * 60 % 60):02}"
    
    def __add__(self, other):
        if isinstance(other, FloatTime):
            return FloatTime(self.value + other.value)
        if isinstance(other, float):
            return FloatTime(self.value + other)

    def __radd__(self, other):
        if isinstance(other, FloatTime):
            return FloatTime(self.value + other.value)
        if isinstance(other, float):
            return FloatTime(self.value + other)
