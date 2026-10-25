class TimeStepper:
    def step(self):
        raise NotImplementedError()

class StaticTimeStepper:
    def __init__(self, delta: float):
        self._delta = delta

    def step(self):
        return self._delta
