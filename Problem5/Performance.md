Performance

# Performance

Performance comparison on the following algorithms, with 100 graphs of 100 nodes with 0.5 prob.

function name - correct - performance - time_ns - time_ms
approx_vertex_cover  -  True  -  98.36  -  12672191.0  -  12.672191
add_max_vertex_cover  -  True  -  92.6  -  184546027.0  -  184.546027
local_max_vertex_cover  -  True  -  92.49  -  4277755.0  -  4.277755

local_max_vertex_cover is the best

Performance comparison with the probability randomly chosen for every graph

function name - correct - performance - time_ns - time_ms
approx_vertex_cover  -  True  -  96.54  -  12122427.0  -  12.122427
add_max_vertex_cover  -  True  -  88.22  -  177751524.0  -  177.751524
local_max_vertex_cover  -  True  -  88.32  -  4158627.0  -  4.158627

add_max is slightly better is a lot of cases, but it takes too much time. If we can optimize a lot this function we can use it, but probably we can't do it because the complexity is at least quadratic.
Local max is linear.

local_max_vertex_cover  -  True  -  92.64  -  4137359.0  -  4.137359
boolean True instead of "removed" in the edge

optimized_local_max_vertex_cover  -  True  -  92.36  -  3919518.0  -  3.919518
optimized the compute_degree function, using sum built-in function
edges are inizialized to 1
when they are removed, they are set to 0
