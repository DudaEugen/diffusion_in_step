from typing import Dict, List
from constants.substance_names import SubstanceName
from models.diffusion_coefficient import DiffusionCoefficient

class EffectiveDiffusionCoefficient:
    _coefficients: Dict[SubstanceName, Dict[SubstanceName, float]]

    def __init__(self, coefficients: List[DiffusionCoefficient], temperature: float):
        self._coefficients = {}
        for coefficient in coefficients:
            coefficient.set_temperature(temperature)
            if coefficient.solute not in self._coefficients:
                self._coefficients[coefficient.solute] = {}
            self._coefficients[coefficient.solute][coefficient.solvent] = coefficient.value

    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        raise NotImplementedError()

    def is_static(self) -> bool:
        raise NotImplementedError()

class StaticDiffusionCoefficient(EffectiveDiffusionCoefficient):
    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        max_concentartion_sub = max(concentrations, key=lambda k: concentrations[k])
        return self._coefficients[substance][max_concentartion_sub]

    def is_static(self) -> bool:
        return True

class WeightedAverageDiffusionCoefficient(EffectiveDiffusionCoefficient):
    def calculate(self, concentrations: Dict[SubstanceName, float], substance: SubstanceName) -> float:
        summary = sum(concentrations.values())
        weighted = sum(map(lambda item: self._coefficients[substance][item[0]]*item[1], concentrations.items()))
        return weighted / summary

    def is_static(self) -> bool:
        return False