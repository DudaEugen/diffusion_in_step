from typing import List
from models.substance import Substance
from models.initial_destribution import InitialDestribution

class State:
    substance1: Substance
    concentration1: List[float]
    substance2: Substance
    concentration2: List[float]
    delta: float

    def __init__(
        self,
        inner_substance: Substance,
        outer_substance: Substance,
        delta: float,
        node_count: int,
        border_coordinate: float,
        initial_destribution: InitialDestribution
    ):
        self.substance1 = inner_substance
        self.substance2 = outer_substance
        self.delta = delta

        concentration1 = [1 for _ in range(round((border_coordinate - initial_destribution.inner_offset)/self.delta))]
        concentration1.extend(initial_destribution.generate(delta=self.delta, border_coordinate=border_coordinate))
        concentration1.extend([0 for _ in range(node_count - len(concentration1))])

        concentration2 = [0 for _ in range(round((border_coordinate - initial_destribution.inner_offset)/self.delta))]
        concentration2.extend(initial_destribution.generate_reversed(self.delta, border_coordinate))
        concentration2.extend([1 for _ in range(node_count - len(concentration2))])
        
        self.concentration1 = list(map(lambda c: c*inner_substance.concentration, concentration1))
        self.concentration2 = list(map(lambda c: c*outer_substance.concentration, concentration2))
        