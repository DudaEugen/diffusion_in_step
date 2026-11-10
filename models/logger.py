from typing import List

from models.state import State
from models.timer import Timer

class PeriodicLogger:
    _period: float
    _last_log_time: float
    _log_points: int
    _sample_indices: List[int]

    def __init__(self, period: float, log_points: int):
        self._period = period
        self._last_log_time = self._period
        self._log_points = log_points
        self._sample_indices = []

    def _prepare(self, state: State):
        pass

    def info(self, timer: Timer, state: State) -> None:
        if not self._sample_indices:
            node_count = len(state.concentration1)
            if len(state.concentration2) != node_count:
                raise ValueError("Concentration arrays must have equal lengths")
            if self._log_points > node_count:
                raise ValueError(
                    f"log_points ({self._log_points}) exceeds node count ({node_count})"
                )
            if self._log_points == 1:
                self._sample_indices = [0]
            else:
                self._sample_indices = [    
                    round(i * (node_count - 1) / (self._log_points - 1))
                    for i in range(self._log_points)
                ]
            self._prepare(state)
        if timer.time() - self._last_log_time > self._period:
            self._last_log_time = timer.time()
            self._log(state)

    def _log(self, state: State) -> None:
        raise NotImplementedError()

class FileLogger(PeriodicLogger):
    def __init__(self, period: float, log_points: int, filename: str, header: str):
        if log_points < 1:
            raise ValueError("log_points must be at least 1")
        super().__init__(period, log_points)
        self._filename = filename
        with open(f'{self._filename}.tsv', 'w') as f:
            print(header, file=f, end="\n")

    def _prepare(self, state: State):
        with open(f'{self._filename}.tsv', 'a') as f:
            values = [i * state.delta for i in self._sample_indices]
            print("time", "substance", *values, file=f, sep='\t', end="\n")

    def _log(self, state: State):
        with open(f'{self._filename}.tsv', 'a') as f:
             points1 = [state.concentration1[i] for i in self._sample_indices]
             print(self._last_log_time, state.substance1, *points1, file=f, sep="\t", end="\n")
             points2 = [state.concentration2[i] for i in self._sample_indices]
             print(self._last_log_time, state.substance2, *points2, file=f, sep="\t", end="\n")
