from models.state import State
from models.time_stepper import TimeStepper

class Resolver:
    state: State
    timer: TimeStepper

    def update_state(self):
        raise NotImplementedError()

    def run(self):
        pass # TODO

class PlainResolver(Resolver):
    def __init__(self, state: State, time_stepper: TimeStepper):
        self.state = state
        self.time_stepper = time_stepper

    def update_state(self):
        pass # TODO

class CilindricResolver(Resolver):
    def __init__(self, state: State, time_stepper: TimeStepper):
        self.state = state
        self.timer = time_stepper

    def update_state(self):
        pass # TODO

class SphericalResolver(Resolver):
    def __init__(self, state: State, time_stepper: TimeStepper):
        self.state = state
        self.time_stepper = time_stepper

    def update_state(self):
        pass # TODO