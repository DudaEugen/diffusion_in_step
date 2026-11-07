from typing import Dict, List

from constants.substance_names import SubstanceName
from models.effective_diffusion_coefficient import EffectiveDiffusionCoefficient
from models.logger import PeriodicLogger
from models.state import State
from models.timer import Timer


class Resolver:
    state: State
    timer: Timer
    diffusion_coefficient: EffectiveDiffusionCoefficient
    logger: PeriodicLogger

    def __init__(
        self,
        state: State,
        timer: Timer,
        diffusion_coefficient_resolver: EffectiveDiffusionCoefficient,
        logger: PeriodicLogger,
    ):
        self.state = state
        self.timer = timer
        self.diffusion_coefficient = diffusion_coefficient_resolver
        self.logger = logger

    def _calculate_new_concentrations(
        self, concentrations: Dict[SubstanceName, List[float]], sub: SubstanceName
    ) -> List[float]:
        concentration = concentrations[sub]
        coefficients = [
            self.diffusion_coefficient.calculate(
                {name: values[i] for name, values in concentrations.items()}, sub
            )
            for i in range(len(concentration))
        ]
        face_fluxes = self._face_fluxes(concentration, coefficients)
        return [
            value + self.timer.step() * self._flux_divergence(face_fluxes, i)
            for i, value in enumerate(concentration)
        ]

    def _face_fluxes(self, concentration: List[float], coefficients: List[float]) -> List[float]:
        delta = self.state.delta
        return [
            # Zero flux at the isolated boundaries.
            0.0,
            *(
                self._harmonic_mean(coefficients[i], coefficients[i + 1])
                * (concentration[i + 1] - concentration[i]) / delta
                for i in range(len(concentration) - 1)
            ),
            0.0,
        ]

    @staticmethod
    def _harmonic_mean(left: float, right: float) -> float:
        # Represents the combined diffusion resistance across a face.
        return 2 * left * right / (left + right)

    def _flux_divergence(self, face_fluxes: List[float], index: int) -> float:
        raise NotImplementedError()

    def run(self) -> None:
        while self.timer.next():
            self.logger.info(self.timer, self.state)
            concentrations = {
                self.state.substance1.name: self.state.concentration1,
                self.state.substance2.name: self.state.concentration2,
            }
            new_concentration1 = self._calculate_new_concentrations(
                concentrations, self.state.substance1.name
            )
            new_concentration2 = self._calculate_new_concentrations(
                concentrations, self.state.substance2.name
            )
            self.state.concentration1[:] = new_concentration1
            self.state.concentration2[:] = new_concentration2


class PlainResolver(Resolver):
    def _flux_divergence(self, face_fluxes: List[float], index: int) -> float:
        delta = self.state.delta
        # Boundary nodes have half-width control volumes.
        volume_width = delta / 2 if index in (0, len(face_fluxes) - 2) else delta
        return (face_fluxes[index + 1] - face_fluxes[index]) / volume_width


class _RadialResolver(Resolver):
    radial_power: int

    def _flux_divergence(self, face_fluxes: List[float], index: int) -> float:
        delta = self.state.delta
        radius = index * delta
        left_radius = max(0.0, radius - delta / 2)
        # The last node lies on the physical outer boundary, so its control
        # volume ends at that radius instead of extending half a step outward.
        right_radius = radius if index == len(face_fluxes) - 2 else radius + delta / 2
        power = self.radial_power
        shell_measure = right_radius ** (power + 1) - left_radius ** (power + 1)
        # Surface-area factors give the radial form of div(D grad(C)).
        return (power + 1) * (
            right_radius**power * face_fluxes[index + 1]
            - left_radius**power * face_fluxes[index]
        ) / shell_measure


class CilindricResolver(_RadialResolver):
    radial_power = 1


class SphericalResolver(_RadialResolver):
    radial_power = 2
