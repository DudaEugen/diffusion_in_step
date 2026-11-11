import math
import sys
from constants.geometry import Geometry
from constants.diffusion_coefficient import DIFFUSION_COEFFICIENT
from models.effective_diffusion_coefficient import (
    EffectiveDiffusionCoefficient,
    StaticDiffusionCoefficient,
    WeightedAverageDiffusionCoefficient
)
from models.initial_destribution import (
    CilindricDestribution,
    PlainDestribution,
    SphericalDestribution,
    InitialDestribution
)
from models.logger import FileLogger
from models.state import State
from models.timer import StaticTimer
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
    stop_time,
    temperature,
    log_period,
    file_prefix,
    log_points
)
from resolver import (
    Resolver,
    PlainResolver,
    CilindricResolver,
    SphericalResolver
)

timer = StaticTimer(step=delta_time, stop_time=stop_time)

geometry: Geometry = Geometry.CILINDRIC
diffusion_coefficient_resolver_type: DIFFUSION_COEFFICIENT = DIFFUSION_COEFFICIENT.STATIC

initial_destribution: InitialDestribution
resolver: Resolver
diffusion_coefficient_resolver: EffectiveDiffusionCoefficient

if f'-g={Geometry.PLAIN.value}' in sys.argv:
    geometry = Geometry.PLAIN
elif f'-g={Geometry.CILINDRIC.value}' in sys.argv:
    geometry = Geometry.CILINDRIC
elif f'-g={Geometry.SPHERICAL.value}' in sys.argv:
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

if f'-dc={DIFFUSION_COEFFICIENT.STATIC.value}' in sys.argv:
    diffusion_coefficient_resolver_type = DIFFUSION_COEFFICIENT.STATIC
elif f'-dc={DIFFUSION_COEFFICIENT.WEIGHTED_AVERAGE.value}' in sys.argv:
    diffusion_coefficient_resolver_type = DIFFUSION_COEFFICIENT.WEIGHTED_AVERAGE
else:
    print(f'ran default effective diffusion coefficient: {diffusion_coefficient_resolver_type}')

match diffusion_coefficient_resolver_type:
    case DIFFUSION_COEFFICIENT.STATIC:
        diffusion_coefficient_resolver = StaticDiffusionCoefficient(diffusion_coefficients, temperature)
    case DIFFUSION_COEFFICIENT.WEIGHTED_AVERAGE:
        diffusion_coefficient_resolver = WeightedAverageDiffusionCoefficient(diffusion_coefficients, temperature)

state = State(
    inner_substance=inner_substance,
    outer_substance=outer_substance,
    delta=delta_coordinate,
    node_count=math.floor(size/delta_coordinate) + 1,
    border_coordinate=border_coordinate,
    initial_destribution=initial_destribution,
    temperature=temperature
)

config = [
    f'T={temperature}',
    f'R={border_coordinate}',
    f'r1={inner_offset}',
    f'r2={outer_offset}',
    f'inner={inner_substance}',
    f'outer={outer_substance}',
    f'g={geometry.value}',
    f'dc={diffusion_coefficient_resolver_type.value}'
]
filename = '_'.join([
    file_prefix,
    *config,
])

logger = FileLogger(
    period=log_period,
    log_points=log_points,
    filename=filename,
    header='\t'.join(["" , *config])
)

match geometry:
    case Geometry.PLAIN:
        resolver = PlainResolver(
            state=state,
            timer=timer,
            logger=logger,
            diffusion_coefficient_resolver=diffusion_coefficient_resolver
        )
    case Geometry.CILINDRIC:
        resolver = CilindricResolver(
            state=state,
            timer=timer,
            logger=logger,
            diffusion_coefficient_resolver=diffusion_coefficient_resolver
        )
    case Geometry.SPHERICAL:
        resolver = SphericalResolver(
            state=state,
            timer=timer,
            logger=logger,
            diffusion_coefficient_resolver=diffusion_coefficient_resolver
        )

resolver.run()
