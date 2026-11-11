from constants.substance_names import SubstanceName
from models.substance import Substance
from models.diffusion_coefficient import DiffusionCoefficient

temperature = 300

aluminium = Substance(
    name=SubstanceName.ALUMINIUM,
    atomic_weight=27*1e-3,
    density_at_zero_celcius=2700,
    volumetric_thermal_expansion=69e-6
)
copper = Substance(
    name=SubstanceName.COPPER,
    atomic_weight=64*1e-3,
    density_at_zero_celcius=8960,
    volumetric_thermal_expansion=51e-6
)

aluminum_self = DiffusionCoefficient(
    solute=SubstanceName.ALUMINIUM,
    solvent=SubstanceName.ALUMINIUM,
    factor=6.5e-5,
    activation_energy=142e3,
    temperature=temperature
)
copper_self = DiffusionCoefficient(
    solute=SubstanceName.COPPER,
    solvent=SubstanceName.COPPER,
    factor=7.8e-5,
    activation_energy=196e3,
    temperature=temperature
)
aluminum_in_copper = DiffusionCoefficient(
    solute=SubstanceName.ALUMINIUM,
    solvent=SubstanceName.COPPER,
    factor=1.31e-5,
    activation_energy=185.2e3,
    temperature=temperature
)
copper_in_aluminum = DiffusionCoefficient(
    solute=SubstanceName.COPPER,
    solvent=SubstanceName.ALUMINIUM,
    factor=2.9e-5,
    activation_energy=130.2e3,
    temperature=temperature
)

diffusion_coefficients = [
    aluminum_self,
    copper_self,
    aluminum_in_copper,
    copper_in_aluminum
]
