from math import exp
from constants.substance_names import SubstanceName

universal_gas_constant = 8.314

class DiffusionCoefficient:
    def __init__(
        self,
        solvent: SubstanceName,
        solute: SubstanceName,
        factor: float,
        activation_energy: float,
        temperature: float,
    ):
        self.solvent = solvent
        self.solute = solute
        self._factor = factor
        self._activation_energy = activation_energy
        self._temperature = temperature
        self._value = self._calculate_value()

    def _calculate_value(self) -> float:
        return self._factor*exp(
            -self._activation_energy/(universal_gas_constant*self.temperature)
        )
    
    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def value(self) -> float:
        return self._value

    def set_temperature(self, temperature: float) -> None:
        self._temperature = temperature
        self._value = self._calculate_value()
    