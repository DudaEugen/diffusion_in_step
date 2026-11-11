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
        self,
        concentrations: Dict[SubstanceName, List[float]],
        sub: SubstanceName,
        start: int,
        end: int,
    ) -> List[float]:
        concentration = concentrations[sub]
        result = concentration.copy()
        node_count = len(concentration)
        coefficient_start = max(0, start - 1)
        coefficient_end = min(node_count - 1, end + 1)
        coefficients = {}
        for index in range(coefficient_start, coefficient_end + 1):
            local_concentrations = {
                name: values[index] for name, values in concentrations.items()
            }
            coefficients[index] = self.diffusion_coefficient.calculate(
                local_concentrations, sub
            )

        def face_flux(left_index: int) -> float:
            if left_index < 0 or left_index >= node_count - 1:
                return 0.0
            diffusion = self._harmonic_mean(
                coefficients[left_index], coefficients[left_index + 1]
            )
            return (
                diffusion
                * (concentration[left_index + 1] - concentration[left_index])
                / self.state.delta
            )

        for index in range(start, end + 1):
            result[index] += self.timer.step() * self._flux_divergence(
                face_flux(index - 1), face_flux(index), index, node_count
            )
        return result

    @staticmethod
    def _harmonic_mean(left: float, right: float) -> float:
        # Represents the combined diffusion resistance across a face.
        return 2 * left * right / (left + right)

    def _flux_divergence(
        self, left_flux: float, right_flux: float, index: int, node_count: int
    ) -> float:
        raise NotImplementedError()

    def run(self) -> None:
        if len(self.state.concentration1) != len(self.state.concentration2):
            raise ValueError("Concentration arrays must have equal lengths")
        self.logger.info(self.timer, self.state)
        step_index = 0
        while self.timer.next():
            step_index += 1
            active_start = max(0, self.state.initial_active_start - step_index)
            active_end = min(
                len(self.state.concentration1) - 1,
                self.state.initial_active_end + step_index,
            )
            concentrations = {
                self.state.substance1.name: self.state.concentration1,
                self.state.substance2.name: self.state.concentration2,
            }
            new_concentration1 = self._calculate_new_concentrations(
                concentrations, self.state.substance1.name, active_start, active_end
            )
            new_concentration2 = self._calculate_new_concentrations(
                concentrations, self.state.substance2.name, active_start, active_end
            )
            self.state.concentration1[:] = new_concentration1
            self.state.concentration2[:] = new_concentration2
            self.logger.info(self.timer, self.state)


class PlainResolver(Resolver):
    def _flux_divergence(
        self, left_flux: float, right_flux: float, index: int, node_count: int
    ) -> float:
        delta = self.state.delta
        # Boundary nodes have half-width control volumes.
        volume_width = delta / 2 if index in (0, node_count - 1) else delta
        return (right_flux - left_flux) / volume_width


class _RadialResolver(Resolver):
    radial_power: int

    def _flux_divergence(
        self, left_flux: float, right_flux: float, index: int, node_count: int
    ) -> float:
        delta = self.state.delta
        radius = index * delta
        left_radius = max(0.0, radius - delta / 2)
        # The last node lies on the physical outer boundary, so its control
        # volume ends at that radius instead of extending half a step outward.
        right_radius = radius if index == node_count - 1 else radius + delta / 2
        power = self.radial_power
        shell_measure = right_radius ** (power + 1) - left_radius ** (power + 1)
        # Surface-area factors give the radial form of div(D grad(C)).
        return (power + 1) * (
            right_radius**power * right_flux
            - left_radius**power * left_flux
        ) / shell_measure


class CilindricResolver(_RadialResolver):
    radial_power = 1


class SphericalResolver(_RadialResolver):
    radial_power = 2
