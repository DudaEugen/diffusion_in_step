class Timer:
    def next(self) -> bool:
        raise NotImplementedError()

    def time(self) -> float:
        raise NotImplementedError()

    def step(self) -> float:
        raise NotImplementedError()

class StaticTimer(Timer):
    def __init__(self, step: float, stop_time: float):
        self._time: float = 0
        self._step = step
        self._stop_time = stop_time

    def time(self) -> float:
        return self._time

    def next(self) -> bool:
        self._time += self._step
        return self._stop_time >= self._time

    def step(self) -> float:
        return self._step

    def __str__(self) -> str:
        return str(self._time)
