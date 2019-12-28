# 28/12/2019

from graph import Graph
import random

"""
This module contains functions used for testing the solution of the vertex cover function
"""

"""
It returns True if the vertex cover is evaluated correctly on the graph passed as parameter.

It returns True if, for every pair of vertices connected by an edge, at least one of them is in the vertex cover.

:param graph:   the graph on which the function evaluates if the vertex cover is evaluated correctly or not.

:return         True if the vertex cover is evaluated correctly.
                False otherwise.
"""
def is_vertex_cover_correct(graph: Graph) -> bool:
    for edge in graph.edges():
        (u, v) = edge.endpoints()
        # if none of the two vertices is in the vertex cover, then the vertex cover is not evaluated correctly
        if not (u.element() or v.element()):
            return False

    return True


"""
It builds a graph in a random way

It builds a graph with the number of vertices passed as parameter.
The edges are chosen randomly using the probability passed as parameter.
The graph returned is not necessarily connected.

:param number_vertices:     it is the number of vertices to add to the graph
:param take_edge_prob:      it is the probability of taking an edge between two vertices

:return                     A graph
"""
def build_random_graph(number_vertices: int = 100, take_edge_prob: float = 0.5) -> Graph:
    graph = Graph()
    vertices = []
    # I add number_vertices vertices to the graph
    for i in range(number_vertices):
        vertices.append(graph.insert_vertex())

    # for each vertex, for each possible edge, I decide if to add it or not
    for i in range(number_vertices):
        for j in range(i + 1, number_vertices):
            choice = random.random()
            if choice <= take_edge_prob:
                graph.insert_edge(vertices[i], vertices[j])

    return graph
