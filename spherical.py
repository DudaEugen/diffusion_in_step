R = 0.1
d1 = 0.01
d2 = 0.011
C1_init = 1.2

r1 = R - d1
r2 = R - d2
d = d1 + d2

M = C1_init/(2*d**2+7*d*r1+7*r1**2)/d**3
B = [
    C1_init,
    0,
    -M*(20*d**3+84*d**2*r1+126*r1**2*d-70*(R**3-r1**3)),
    2*M*(16*d**3+70*d**2*r1+112*r1**2*d-70*(R**3-r1**3))/d,
    7*M*(10*(R**3-r1**3)-2*d**3-9*r1*d**2-15*r1**2*d)/d**2
]

def concentarion_initial(r):
    return sum(map(lambda C, i: C*r**i, B, range(len(B))))

N = 800
delta = d / N

C1 = list(map(concentarion_initial, [delta*i for i in range(N + 1)]))

# TODO: start with r = 0


print(B, C1[:5], delta, sep='\n')