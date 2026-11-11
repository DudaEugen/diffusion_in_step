from parameters.substances import aluminium, copper

border_coordinate = 0.1e-3
inner_offset = 1.1e-7
outer_offset = 1e-7
inner_substance = aluminium
outer_substance = copper

temperature = 800

size = 2*border_coordinate

delta_coordinate = 1e-8
delta_time = 1e-4

stop_time = 1e12

log_period = 1e4 * delta_time
log_points = 100
file_prefix='results/state'
