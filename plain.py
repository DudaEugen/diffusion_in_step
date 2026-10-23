from typing import Callable, List

R = 0.1
d1 = 0.01
d2 = 0.011
C1_init = 1.2
C2_init = 1.18

R_max = 2*R
d_sum = d1 + d2

delta_r = 0.00001
delta_t = 0.00001

B_factors = [
    1,
    0,
    -6*(3*d2 - 2*d1)/pow(d_sum, 3),
    4*(8*d2 - 7*d1)/pow(d_sum, 4),
    15*(d1 - d2)/pow(d_sum, 5),
]

B1 = list(map(lambda b: b*C1_init, B_factors))
B2 = list(map(lambda b: b*C2_init, B_factors))

def concentarion_initial(B: List[float]) -> Callable[[float], float]:
    def implementation(r: float) -> float:
        return sum(map(lambda b, i: b*r**i, B, range(len(B))))
    return implementation

C1 = [1 for _ in range(round((R-d1)/delta_r) + 1)]
C1.extend(map(concentarion_initial(B1), [delta_r*i for i in range(round(d_sum/delta_r) + 1)]))
C1.extend([0 for _ in range(round((R_max-R-d2)/delta_r) + 1)])

C2 = [0 for _ in range(round((R-d1)/delta_r) + 1)]
C2.extend(map(concentarion_initial(B2), reversed([delta_r*i for i in range(round(d_sum/delta_r) + 1)])))
C2.extend([1 for _ in range(round((R_max-R-d2)/delta_r) + 1)])
