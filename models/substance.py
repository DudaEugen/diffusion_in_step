import math

from typing import NamedTuple
from constants.substance_names import SubstanceName

avogadro_constant = 6.02214076 * math.pow(10, 23)
referenced_temperature = 273.15

class Substance(NamedTuple):
    name: SubstanceName
    atomic_weight: float
    density_at_zero_celcius: float
    volumetric_thermal_expansion: float

    def concentration(self, temperature: float) -> float:
        return avogadro_constant * self.density_at_zero_celcius / (\
                1 + (temperature - referenced_temperature)*self.volumetric_thermal_expansion
            ) / self.atomic_weight

    def __str__(self) -> str:
        return str(self.name)
