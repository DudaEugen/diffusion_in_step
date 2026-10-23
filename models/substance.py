from typing import NamedTuple

avogadro_constant = 6.02214076 * 10**23

class Substance(NamedTuple):
    name: str
    density: float
    atomic_weight: float

    @property
    def concentration(self) -> float:
        return avogadro_constant * self.density / self.atomic_weight
