import math

from typing import NamedTuple
from constants.substance_names import SubstanceName

avogadro_constant = 6.02214076 * math.pow(10, 23)

class Substance(NamedTuple):
    name: SubstanceName
    atomic_weight: float
    density_at_reference_temperature: float
    volumetric_thermal_expansion: float
    reference_temperature: float

    def concentration(self, temperature: float) -> float:
        return avogadro_constant * self.density_at_reference_temperature / (\
                1 + (temperature - self.reference_temperature)*self.volumetric_thermal_expansion
            ) / self.atomic_weight

    def __str__(self) -> str:
        return str(self.name)
