# 28/12/2019

import test_functions
import vertex_cover

# evaluates the performances of the algorithm
# you need python >= 3.7 to run this code because test_functions.evaluate_performanecs() uses time.time_ns that requires python 3.7
functions_names = ["vertex_cover"]
functions = [vertex_cover.vertex_cover]

results = test_functions.evaluate_performances(functions, 100, 0.5)

print("function name - correct - performance - time_ns - time_ms")
for i in range(len(functions)):
    print(functions_names[i], " - ", results[i][0], " - ", results[i][1], " - ", results[i][2], " - ", results[i][2] / 1000000 )