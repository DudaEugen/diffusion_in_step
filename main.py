import math
import sys
from models.initial_destribution import CilindricDestribution, PlainDestribution, SphericalDestribution
from models.state import State
from utils.substances import aluminium, copper

border_coordinate = 0.1
inner_offset = 0.01
outer_offset = 0.011
inner_substance = aluminium
outer_substance = copper

size = 2*border_coordinate

delta_r = 0.00001
delta_t = 0.00001

if 'plain' in sys.argv:
    initial_destribution = PlainDestribution(
        inner_offset=inner_offset,
        outer_offset=outer_offset
    )
elif 'cilindric' in sys.argv:
    initial_destribution = CilindricDestribution(
        inner_offset=inner_offset,
        outer_offset=outer_offset
    )
elif 'spherical' in sys.argv:
    initial_destribution = SphericalDestribution(
        inner_offset=inner_offset,
        outer_offset=outer_offset
    )
else:
    print('ran default configiration: cilindric')
    initial_destribution = CilindricDestribution(
        inner_offset=inner_offset,
        outer_offset=outer_offset
    )

state = State(
    inner_substance=inner_substance,
    outer_substance=outer_substance,
    delta=delta_r,
    node_count=math.floor(size/delta_r) + 1,
    border_coordinate=border_coordinate,
    initial_destribution=initial_destribution
)
