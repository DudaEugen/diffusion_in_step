from parameters.substances import aluminium, copper

border_coordinate = 0.1e-3
inner_offset = 1.1e-8
outer_offset = 1e-8
inner_substance = aluminium
outer_substance = copper

temperature = 500

size = 2*border_coordinate

delta_coordinate = 1e-9
delta_time = 1e8

stop_time = 1e12

log_period = 1e10
log_points = 100
file_prefix='results/state'
