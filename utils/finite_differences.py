def first_derivative_central(state: list[float], index: int, delta: float) -> float:
    return (state[index+1] - state[index-1])/(2*delta)

def first_derivative_forward(state: list[float], index: int, delta: float) -> float:
    return (state[index+1] - state[index])/delta

def first_derivative_backward(state: list[float], index: int, delta: float) -> float:
    return (state[index] - state[index-1])/delta

def first_derivative_forward_order2(state: list[float], index: int, delta: float) -> float:
    return (-state[index+2] + 4*state[index+1] - 3*state[index])/(2*delta)

def first_derivative_backward_order2(state: list[float], index: int, delta: float) -> float:
    return (3*state[index] - 4*state[index-1] + state[index-2])/(2*delta)

def second_derivative_central(state: list[float], index: int, delta: float) -> float:
    return (state[index+1] - 2*state[index] + state[index-1])/pow(delta, 2)

def second_derivative_forward(state: list[float], index: int, delta: float) -> float:
    return (state[index+2] - 2*state[index+1] + state[index])/pow(delta, 2)

def second_derivative_backward(state: list[float], index: int, delta: float) -> float:
    return (state[index] - 2*state[index-1] + state[index-2])/pow(delta, 2)
