from typing import Dict, List
from constants.substance_names import SubstanceName
from models.effective_diffusion_coefficient import EffectiveDiffusionCoefficient
from models.logger import PeriodicLogger
from models.state import State
from models.timer import Timer
from utils.finite_differences import (
    FiniteDerivative,
    first_derivative_backward_order2,
    first_derivative_central,
    first_derivative_forward_order2,
    second_derivative_backward_order2,
    second_derivative_forward_order2,
    second_derivative_central,
)

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
        logger: PeriodicLogger
    ):
        self.state = state
        self.timer = timer
        self.diffusion_coefficient = diffusion_coefficient_resolver
        self.logger = logger

    def _calculate_new_concentrations(self, concentrations: Dict[SubstanceName, List[float]], sub: SubstanceName) -> List[float]:
        raise NotImplementedError()

    def run(self) -> None:
        while self.timer.next():
            self.logger.info(self.timer, self.state)

            new_concentration1: List[float] = []
            new_concentration2: List[float] = []
            concentrations = [
                (self.state.concentration1, self.state.concentration2, new_concentration1, self.state.substance1, self.state.substance2),
                (self.state.concentration2, self.state.concentration1, new_concentration2, self.state.substance2, self.state.substance1)
            ]
            for concentration, other, new, substance, other_substance in concentrations:
                updated = self._calculate_new_concentrations(
                    {
                        substance.name: concentration,
                        other_substance.name: other,
                    },
                    sub=substance.name
                )
                new.clear()
                new.extend(updated)
            self.state.concentration1.clear()
            self.state.concentration1.extend(new_concentration1)
            self.state.concentration2.clear()
            self.state.concentration2.extend(new_concentration2)

class PlainResolver(Resolver):
    def _calculate_new_concentrations(self, concentrations: Dict[SubstanceName, List[float]], sub: SubstanceName) -> List[float]:
        result: List[float] = []
        local_concentration = concentrations[sub]
        diffusion_coefficients: List[float] = []
        for i in range(len(local_concentration)):
            local_concentrations = { name: v[i] for name, v in concentrations.items()}
            diffusion_coefficients.append(self.diffusion_coefficient.calculate(local_concentrations, sub))
        for i in range(len(local_concentration)):
            growth = .0 

            first_derivative: FiniteDerivative = first_derivative_central
            second_derivative: FiniteDerivative = second_derivative_central
            if i == len(local_concentration) - 1:
                first_derivative = first_derivative_backward_order2
                second_derivative = second_derivative_backward_order2
            elif i == 0:
                first_derivative = first_derivative_forward_order2
                second_derivative = second_derivative_forward_order2
            growth += diffusion_coefficients[i] * self.timer.step()*second_derivative(local_concentration, i, self.state.delta)

            if not self.diffusion_coefficient.is_static():
                growth += self.timer.step()*\
                    first_derivative(local_concentration, i, self.state.delta)*\
                    first_derivative(diffusion_coefficients, i, self.state.delta)

            result.append(growth + local_concentration[i])
        return result

class CilindricResolver(Resolver):
    def _calculate_new_concentrations(self, concentrations: Dict[SubstanceName, List[float]], sub: SubstanceName) -> List[float]:
        result: List[float] = []
        local_concentration = concentrations[sub]
        diffusion_coefficients: List[float] = []
        for i in range(len(local_concentration)):
            local_concentrations = { name: v[i] for name, v in concentrations.items()}
            diffusion_coefficients.append(self.diffusion_coefficient.calculate(local_concentrations, sub))
        for i in range(len(local_concentration)):
            growth = .0
            first_derivative: FiniteDerivative = first_derivative_central
            second_derivative: FiniteDerivative = second_derivative_central
            if i == len(local_concentration) - 1:
                first_derivative = first_derivative_backward_order2
                second_derivative = second_derivative_backward_order2
            elif i == 0:
                second_derivative = lambda c, i, d: 4*(c[i + 1] - c[i])/pow(d, 2)

            if i != 0:
                growth += first_derivative(local_concentration, i, self.state.delta)/(i*self.state.delta)
            growth += second_derivative(local_concentration, i, self.state.delta)
            growth *= diffusion_coefficients[i] * self.timer.step()

            if not self.diffusion_coefficient.is_static() and i !=0:
                growth += self.timer.step()*\
                    first_derivative(local_concentration, i, self.state.delta)*\
                    first_derivative(diffusion_coefficients, i, self.state.delta)

            result.append(growth + local_concentration[i])
        return result

class SphericalResolver(Resolver):
    def _calculate_new_concentrations(self, concentrations: Dict[SubstanceName, List[float]], sub: SubstanceName) -> List[float]:
        result: List[float] = []
        local_concentration = concentrations[sub]
        diffusion_coefficients: List[float] = []
        for i in range(len(local_concentration)):
                local_concentrations = { name: v[i] for name, v in concentrations.items()}
                diffusion_coefficients.append(self.diffusion_coefficient.calculate(local_concentrations, sub))
        for i in range(len(local_concentration)):
            growth = .0        
            first_derivative: FiniteDerivative = first_derivative_central
            second_derivative: FiniteDerivative = second_derivative_central
            if i == len(local_concentration) - 1:
                first_derivative = first_derivative_backward_order2
                second_derivative = second_derivative_backward_order2
            elif i == 0:
                second_derivative = lambda c, i, d: 6*(c[i + 1] - c[i])/pow(d, 2)

            if i != 0:
                growth += 2*first_derivative(local_concentration, i, self.state.delta)/(i*self.state.delta)
            growth += second_derivative(local_concentration, i, self.state.delta)
            growth *= diffusion_coefficients[i] * self.timer.step()

            if not self.diffusion_coefficient.is_static() and i != 0:
                growth += self.timer.step()*\
                    first_derivative(local_concentration, i, self.state.delta)*\
                    first_derivative(diffusion_coefficients, i, self.state.delta)

            result.append(growth + local_concentration[i])
        return result