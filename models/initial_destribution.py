import math
from typing import Callable, List

class InitialDestribution:
    inner_offset: float
    outer_offset: float

    def __init__(
        self,
        inner_offset: float,
        outer_offset: float
    ):
        self.inner_offset = inner_offset
        self.outer_offset = outer_offset

    def _calculate_coefficients(
        self, 
        border_coordinate: float,
        inner_offset: float,
        outer_offset: float
    ) -> List[float]:
        raise Exception('Not implemented')
    
    def _value(self, coef: List[float]) -> Callable[[float], float]:
        def implementation(coord: float) -> float:
            return sum(map(lambda c, i: c*coord**i, coef, range(len(coef))))
        return implementation

    def _calculate_destribution(
        self,
        delta: float, 
        border_coordinate: float,
        inner_offset: float,
        outer_offset: float
    ):
        coef = self._calculate_coefficients(
            border_coordinate=border_coordinate,
            inner_offset=inner_offset,
            outer_offset=outer_offset
        )
        nodes_count = math.floor((inner_offset + outer_offset) / delta)
        return list(map(self._value(coef), [delta*i for i in range(nodes_count + 1)]))

    def generate(
        self,
        delta: float,
        border_coordinate: float,
    ) -> List[float]:
        return self._calculate_destribution(
            delta=delta, 
            border_coordinate=border_coordinate,
            inner_offset=self.inner_offset,
            outer_offset=self.outer_offset
        )

    def generate_reversed(
        self,
        delta: float,
        border_coordinate: float,
    ) -> List[float]:
        return reversed(self._calculate_destribution(
            delta=delta, 
            border_coordinate=border_coordinate,
            inner_offset=self.outer_offset,
            outer_offset=self.inner_offset
        ))
    

class PlainDestribution(InitialDestribution):
    def _calculate_coefficients(
        self,
        border_coordinate: float,
        inner_offset: float,
        outer_offset: float
    ) -> List[float]:
        summary_offset = inner_offset + outer_offset
        return [
            1,
            0,
            -6*(3*outer_offset - 2*inner_offset)/pow(summary_offset, 3),
            4*(8*outer_offset - 7*inner_offset)/pow(summary_offset, 4),
            15*(inner_offset - outer_offset)/pow(summary_offset, 5),
        ]

class CilindricDestribution(InitialDestribution):
    def _calculate_coefficients(
        self,
        border_coordinate: float,
        inner_offset: float,
        outer_offset: float
    ) -> List[float]:
        R = border_coordinate
        r1 = border_coordinate - inner_offset
        d = inner_offset + outer_offset
        factor = 2/(d**4 + 2*d**3*r1)
        return [
            1,
            0,
            -3*factor*(2*d**2+6*d*r1-5*R**2+5*r1**2),
            2*factor*(5*d**2+16*d*r1-15*R**2+15*r1**2)/d,
            15*factor*(-0.3*d**2-d*r1+R**2-r1**2)/d**2
        ]

class SphericalDestribution(InitialDestribution):
    def _calculate_coefficients(
        self,
        border_coordinate: float,
        inner_offset: float,
        outer_offset: float
    ) -> List[float]:
        R = border_coordinate
        r1 = border_coordinate - inner_offset
        d = inner_offset + outer_offset
        factor = 1/(2*d**2+7*d*r1+7*r1**2)/d**3
        return [
            1,
            0,
            -factor*(20*d**3+84*d**2*r1+126*r1**2*d-70*(R**3-r1**3)),
            2*factor*(16*d**3+70*d**2*r1+112*r1**2*d-70*(R**3-r1**3))/d,
            7*factor*(10*(R**3-r1**3)-2*d**3-9*r1*d**2-15*r1**2*d)/d**2
        ]       
