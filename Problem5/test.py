# 28/12/2019

from graph import Graph
from test_functions import is_vertex_cover_correct
from test_functions import build_random_graph
import vertex_cover


"""
It tests if the function "is_vertex_cover_correct" is correct.

:return True if the return value of the "is_vertex_cover_correct" is correct.
        False otherwise.
"""
def test_is_vertex_cover_correct() -> bool:
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

"""
# test is_vertex_cover_correct function
print(test_is_vertex_cover_correct())

# test build_random_graph function
graph = build_random_graph(100, 0.5)
graph.dump()
"""

# test approx_vertex_cover
graph = build_random_graph(3, 1)
graph.dump()
vertex_cover.approx_vertex_cover(graph)
graph.dump()
print(is_vertex_cover_correct(graph))
