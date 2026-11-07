from constants.substance_names import SubstanceName
from models.substance import Substance
from models.diffusion_coefficient import DiffusionCoefficient

temperature = 300

aluminium = Substance(name=SubstanceName.ALUMINIUM, density=2699, atomic_weight=27*1e-3)
copper = Substance(name=SubstanceName.COPPER, density=8944, atomic_weight=64*1e-3)

aluminum_self = DiffusionCoefficient(
    solvent=SubstanceName.ALUMINIUM,
    solute=SubstanceName.ALUMINIUM,
    factor=6.5e-5,
    activation_energy=142e3,
    temperature=temperature
)
copper_self = DiffusionCoefficient(
    solvent=SubstanceName.COPPER,
    solute=SubstanceName.COPPER,
    factor=7.8e-5,
    activation_energy=196e3,
    temperature=temperature
)
aluminum_in_copper = DiffusionCoefficient(
    solvent=SubstanceName.ALUMINIUM,
    solute=SubstanceName.COPPER,
    factor=1.31e-5,
    activation_energy=185.2e3,
    temperature=temperature
)
copper_in_aluminum = DiffusionCoefficient(
    solvent=SubstanceName.COPPER,
    solute=SubstanceName.ALUMINIUM,
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
