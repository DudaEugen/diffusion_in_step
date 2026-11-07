from typing import Dict, List
from constants.substance_names import SubstanceName
from models.diffusion_coefficient import DiffusionCoefficient

class EffectiveDiffusionCoefficient:
    _coefficients: Dict[SubstanceName, Dict[SubstanceName, float]]

    def __init__(self, coefficients: List[DiffusionCoefficient], temperature: float):
        # Index coefficients by diffusing substance, then by host substance.
        self._coefficients = {}
        for coefficient in coefficients:
            coefficient.set_temperature(temperature)
            if coefficient.solute not in self._coefficients:
                self._coefficients[coefficient.solute] = {}
            self._coefficients[coefficient.solute][coefficient.solvent] = coefficient.value

    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        raise NotImplementedError()

class StaticDiffusionCoefficient(EffectiveDiffusionCoefficient):
    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        # Use the coefficient for the locally most abundant host substance.
        max_concentartion_sub = max(concentrations, key=lambda k: concentrations[k])
        return self._coefficients[substance][max_concentartion_sub]

class WeightedAverageDiffusionCoefficient(EffectiveDiffusionCoefficient):
    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        summary = sum(concentrations.values())
        # Mix host-specific coefficients in proportion to local concentrations.
        weighted = sum(map(lambda item: self._coefficients[substance][item[0]]*item[1], concentrations.items()))
        return weighted / summary
