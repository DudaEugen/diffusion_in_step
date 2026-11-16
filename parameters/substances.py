from parameters.environment import setting

from constants.substance_names import SubstanceName
from models.substance import Substance
from models.diffusion_coefficient import DiffusionCoefficient

reference_temperature = setting("REFERENCE_TEMPERATURE", float)

aluminium = Substance(
    name=SubstanceName.ALUMINIUM,
    atomic_weight=27e-3,  # kg/mol
    density_at_reference_temperature=setting("ALUMINIUM_DENSITY_AT_REFERENCE_TEMPERATURE", float),
    volumetric_thermal_expansion=setting("ALUMINIUM_VOLUMETRIC_THERMAL_EXPANSION", float),
    reference_temperature=reference_temperature
)
copper = Substance(
    name=SubstanceName.COPPER,
    atomic_weight=64e-3,  # kg/mol
    density_at_reference_temperature=setting("COPPER_DENSITY_AT_REFERENCE_TEMPERATURE", float),
    volumetric_thermal_expansion=setting("COPPER_VOLUMETRIC_THERMAL_EXPANSION", float),
    reference_temperature=reference_temperature
)

aluminum_self = DiffusionCoefficient(
    solute=SubstanceName.ALUMINIUM,
    solvent=SubstanceName.ALUMINIUM,
    factor=setting("ALUMINIUM_SELF_FACTOR", float),
    activation_energy=setting("ALUMINIUM_SELF_ACTIVATION_ENERGY", float),
    temperature=reference_temperature
)
copper_self = DiffusionCoefficient(
    solute=SubstanceName.COPPER,
    solvent=SubstanceName.COPPER,
    factor=setting("COPPER_SELF_FACTOR", float),
    activation_energy=setting("COPPER_SELF_ACTIVATION_ENERGY", float),
    temperature=reference_temperature
)
aluminum_in_copper = DiffusionCoefficient(
    solute=SubstanceName.ALUMINIUM,
    solvent=SubstanceName.COPPER,
    factor=setting("ALUMINIUM_IN_COPPER_FACTOR", float),
    activation_energy=setting("ALUMINIUM_IN_COPPER_ACTIVATION_ENERGY", float),
    temperature=reference_temperature
)
copper_in_aluminum = DiffusionCoefficient(
    solute=SubstanceName.COPPER,
    solvent=SubstanceName.ALUMINIUM,
    factor=setting("COPPER_IN_ALUMINIUM_FACTOR", float),
    activation_energy=setting("COPPER_IN_ALUMINIUM_ACTIVATION_ENERGY", float),
    temperature=reference_temperature
)

diffusion_coefficients = [
    aluminum_self,
    copper_self,
    aluminum_in_copper,
    copper_in_aluminum
]
