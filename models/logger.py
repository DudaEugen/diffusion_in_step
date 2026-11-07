from models.state import State
from models.timer import Timer

class PeriodicLogger:
    _period: float
    _last_log_time: float

    def __init__(self, period: float):
        self._period = period
        self._last_log_time = self._period

    def info(self, timer: Timer, state: State) -> None:
        if timer.time() - self._last_log_time > self._period:
            self._last_log_time = timer.time()
            self._log(state)

    def _log(self, state: State) -> None:
        raise NotImplementedError()

class FileLogger(PeriodicLogger):
    def __init__(self, period: float, filename: str):
        super().__init__(period)
        self._filename = filename

    def _log(self, state: State):
        with open(f'{self._filename}_time={self._last_log_time}.txt', 'w') as f:
            print(self._last_log_time, state, file=f, sep="\t", end="\n")
