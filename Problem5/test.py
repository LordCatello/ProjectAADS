# 28/12/2019

from graph import Graph
from test_functions import is_vertex_cover_correct
from test_functions import build_random_graph
import test_functions
import vertex_cover


def test_is_vertex_cover_correct() -> bool:
    """
    It tests if the function "is_vertex_cover_correct" is correct.

    :return True if the return value of the "is_vertex_cover_correct" is correct.
            False otherwise.
    """

    # I have to build a bunch of graphs for testing the function
    graph1 = Graph()
    output1 = True
    a = graph1.insert_vertex(True)
    b = graph1.insert_vertex(True)
    c = graph1.insert_vertex(False)

    graph1.insert_edge(a, b)
    graph1.insert_edge(a, c)
    graph1.insert_edge(b, c)

    # graph1.dump()

    graph2 = Graph()
    output2 = False
    a = graph2.insert_vertex(True)
    b = graph2.insert_vertex(False)
    c = graph2.insert_vertex(False)

    graph2.insert_edge(a, b)
    graph2.insert_edge(a, c)
    graph2.insert_edge(b, c)

    # graph2.dump()

    if is_vertex_cover_correct(graph1) != output1 or is_vertex_cover_correct(graph2) != output2:
        return False
    else:
        return True


# evaluates the performances for all the algorithms
functions_names = ["local_max_vertex_cover", "optimized_local_max_vertex_cover"]
functions = [vertex_cover.local_max_vertex_cover, vertex_cover.optimized_local_max_vertex_cover]

results = test_functions.evaluate_performances(functions, 100, 0.5)

print("function name - correct - performance - time_ns - time_ms")
for i in range(len(functions)):
    print(functions_names[i], " - ", results[i][0], " - ", results[i][1], " - ", results[i][2], " - ", results[i][2] / 1000000 )


"""
graph = build_random_graph(3, 1)
count = vertex_cover.optimized_local_max_vertex_cover(graph)
print(count)
graph.graphic_dump()
"""