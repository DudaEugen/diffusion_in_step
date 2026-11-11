import math
from typing import List
from models.diffusion_coefficient import DiffusionCoefficient
from models.initial_destribution import InitialDestribution
from models.substance import Substance

class State:
    substance1: Substance
    concentration1: List[float]
    substance2: Substance
    concentration2: List[float]
    delta: float
    initial_active_start: int
    initial_active_end: int

    def __init__(
        self,
        inner_substance: Substance,
        outer_substance: Substance,
        delta: float,
        node_count: int,
        border_coordinate: float,
        initial_destribution: InitialDestribution,
        temperature: float
    ):
        self.substance1 = inner_substance
        self.substance2 = outer_substance
        self.delta = delta

        self.initial_active_start = round(
            (border_coordinate - initial_destribution.inner_offset) / delta
        )
        transition_intervals = math.floor(
            (initial_destribution.inner_offset + initial_destribution.outer_offset) / delta
        )
        self.initial_active_end = min(node_count - 1, self.initial_active_start + transition_intervals)

        # Build complementary composition profiles, then convert fractions to number concentrations.
        concentration1 = [1. for _ in range(self.initial_active_start)]
        concentration1.extend(initial_destribution.generate(delta=self.delta, border_coordinate=border_coordinate))
        concentration1.extend([.0 for _ in range(node_count - len(concentration1))])

        concentration2 = [.0 for _ in range(self.initial_active_start)]
        concentration2.extend(initial_destribution.generate_reversed(self.delta, border_coordinate))
        concentration2.extend([1. for _ in range(node_count - len(concentration2))])
        
        self.concentration1 = list(map(lambda c: c*inner_substance.concentration(temperature), concentration1))
        self.concentration2 = list(map(lambda c: c*outer_substance.concentration(temperature), concentration2))
