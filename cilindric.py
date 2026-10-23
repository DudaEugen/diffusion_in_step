R = 0.1
d1 = 0.01
d2 = 0.011
C1_init = 1.2

r1 = R - d1
r2 = R - d2
d = d1 + d2

M = 2*C1_init/(d**4 + 2*d**3*r1)
B = [
    C1_init,
    0,
    -3*M*(2*d**2+6*d*r1-5*R**2+5*r1**2),
    2*M*(5*d**2+16*d*r1-15*R**2+15*r1**2)/d,
    15*M*(-0.3*d**2-d*r1+R**2-r1**2)/d**2
]

def concentarion_initial(r):
    return sum(map(lambda C, i: C*r**i, B, range(len(B))))

N = 800
delta = d / N

C1 = list(map(concentarion_initial, [delta*i for i in range(N + 1)]))

# TODO: start with r = 0


print(B, C1[:5], delta, sep='\n')