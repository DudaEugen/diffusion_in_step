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

        start = border_coordinate - initial_destribution.inner_offset
        end = border_coordinate + initial_destribution.outer_offset
        self.initial_active_start = max(0, min(node_count - 1, math.floor(start / delta)))
        self.initial_active_end = max(0, min(node_count - 1, math.ceil(end / delta)))

        concentration1 = initial_destribution.generate(node_count, delta, border_coordinate)
        concentration2 = initial_destribution.generate(node_count, delta, border_coordinate, reversed=True)

        inner_concentration = inner_substance.concentration(temperature)
        outer_concentration = outer_substance.concentration(temperature)
        self.concentration1 = [c * inner_concentration for c in concentration1]
        self.concentration2 = [c * outer_concentration for c in concentration2]
