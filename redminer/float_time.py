class FloatTime:
    value: float

    def __repr__(self):
        return f"{int(self.value)}:{(self.value * 60 % 60):02}"

