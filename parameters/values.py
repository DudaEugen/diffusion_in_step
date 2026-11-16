from parameters.environment import setting
from parameters.substances import aluminium, copper

border_coordinate = setting("BORDER_COORDINATE", float)
inner_offset = setting("INNER_OFFSET", float)
outer_offset = setting("OUTER_OFFSET", float)
inner_substance = aluminium
outer_substance = copper

temperature = setting("TEMPERATURE", float)

size = setting("SIZE_MULTIPLIER", float) * border_coordinate

delta_coordinate = setting("DELTA_COORDINATE", float)
delta_time = setting("DELTA_TIME", float)

stop_time = setting("STOP_TIME", float)

log_period = setting("LOG_PERIOD_STEPS", float) * delta_time
log_points = setting("LOG_POINTS", int, default=None)
file_prefix = setting("FILE_PREFIX", str)
