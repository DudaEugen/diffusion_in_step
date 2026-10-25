import math
import sys
from constants.geometry import Geometry
from models.initial_destribution import CilindricDestribution, PlainDestribution, SphericalDestribution
from models.state import State
from models.time_stepper import StaticTimeStepper
from parameters.substances import diffusion_coefficients
from parameters.values import (
    border_coordinate,
    inner_offset,
    outer_offset,
    inner_substance,
    outer_substance,
    size,
    delta_coordinate,
    delta_time,
    temperature
)
from resolver import PlainResolver, CilindricResolver, SphericalResolver


time_stepper = StaticTimeStepper(delta_time)

geometry: Geometry = Geometry.CILINDRIC

if Geometry.PLAIN.value in sys.argv:
    geometry = Geometry.PLAIN
elif Geometry.CILINDRIC.value in sys.argv:
    geometry = Geometry.CILINDRIC
elif Geometry.SPHERICAL.value in sys.argv:
    geometry = Geometry.SPHERICAL
else:
    print(f'ran default configiration: {geometry}')

match geometry:
    case Geometry.PLAIN:
        initial_destribution = PlainDestribution(
            inner_offset=inner_offset,
            outer_offset=outer_offset
        )
    case Geometry.CILINDRIC:
        initial_destribution = CilindricDestribution(
            inner_offset=inner_offset,
            outer_offset=outer_offset
        )
    case Geometry.SPHERICAL:
        initial_destribution = SphericalDestribution(
            inner_offset=inner_offset,
            outer_offset=outer_offset
        )

state = State(
    inner_substance=inner_substance,
    outer_substance=outer_substance,
    delta=delta_coordinate,
    node_count=math.floor(size/delta_coordinate) + 1,
    border_coordinate=border_coordinate,
    initial_destribution=initial_destribution,
    diffusion_coefficients=diffusion_coefficients,
    temperature=temperature
)

match geometry:
    case Geometry.PLAIN:
        resolver = PlainResolver(state=state, time_stepper=time_stepper)
    case Geometry.CILINDRIC:
        resolver = CilindricResolver(state=state, time_stepper=time_stepper)
    case Geometry.SPHERICAL:
        resolver = SphericalResolver(state=state, time_stepper=time_stepper)

resolver.run()
