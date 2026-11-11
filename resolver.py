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

        # Keep the outside face on each side as a one-cell halo.  Its
        # concentrations remain unchanged, but its coefficient is needed to
        # calculate the active endpoint's flux.
        face_fluxes = []
        first_face = start - 1
        last_face = end
        for left_index in range(first_face, last_face + 1):
            if left_index < 0 or left_index >= node_count - 1:
                face_fluxes.append(0.0)
            else:
                diffusion = self._harmonic_mean(
                    coefficients[left_index], coefficients[left_index + 1]
                )
                face_fluxes.append(
                    diffusion
                    * (concentration[left_index + 1] - concentration[left_index])
                    / self.state.delta
                )

        new_values = []
        for offset, index in enumerate(range(start, end + 1)):
            new_values.append(
                concentration[index]
                + self.timer.step()
                * self._flux_divergence(
                    face_fluxes[offset], face_fluxes[offset + 1], index, node_count
                )
            )
        return new_values

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
            self.state.concentration1[active_start : active_end + 1] = new_concentration1
            self.state.concentration2[active_start : active_end + 1] = new_concentration2
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
