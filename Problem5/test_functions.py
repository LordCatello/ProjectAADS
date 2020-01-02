# 28/12/2019

from graph import Graph
import random
import time

"""
This module contains functions used for testing the solution of the vertex cover function
"""


def is_vertex_cover_correct(graph: Graph) -> bool:
    """
    It returns True if the vertex cover is evaluated correctly on the graph passed as parameter.

    It returns True if, for every pair of vertices connected by an edge, at least one of them is in the vertex cover.

    :param graph:   the graph on which the function evaluates if the vertex cover is evaluated correctly or not.

    :return:        True if the vertex cover is evaluated correctly.
                    False otherwise.
    """

    for edge in graph.edges():
        (u, v) = edge.endpoints()
        # if none of the two vertices is in the vertex cover, then the vertex cover is not evaluated correctly
        if not (u.element() or v.element()):
            return False

    return True


def build_random_graph(number_vertices: int = 100, take_edge_prob: float = 0.5) -> Graph:
    """
    It builds a graph in a random way

    It builds a graph with the number of vertices passed as parameter.
    The edges are chosen randomly using the probability passed as parameter.
    The graph returned is not necessarily connected.

    :param number_vertices:     it is the number of vertices to add to the graph
    :param take_edge_prob:      it is the probability of taking an edge between two vertices

    :return:                    A graph
    """

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


def evaluate_performances(functions, number_graphs: int = 100, take_edge_prob: int = -1) -> [(bool, float, float)]:
    """
    It evaluates the performances of a list of vertex cover functions passed as parameter.

    The performance is evaluated os a set of randomly generated graphs with different probabilities.
    The set of graph is the same for every function.

    :param functions:       A list of functions on which it evaluates the performances

    :param number_graphs:   The number of graphs used for testing the functions.

    :param take_edge_prob:  it is the probability of taking an edge between two vertices.
                            It is used for building the graphs used during the test.
                            If -1 is passed, a random probability is chosen for each graph

    :return:                A list of tuples. Each tuple is related to a function.
                            Each tuple consists of 3 elements.
                            The first element is a boolean and it's True if the function evaluates a correct vertex_cover for all
                            the graphs used as tests. It's false otherwise.
                            The second element is a float and it's the average of the number of vertex included in the vertex cover.
                            The second element is a float and it's the average time, in nanoseconds, needed to evaluate the results.
    """

    performances = []
    graphs = []

    # build the graphs
    take_prob = take_edge_prob
    for i in range(number_graphs):
        if take_edge_prob == -1:
            take_prob = random.random()

        graphs.append(build_random_graph(100, take_prob))

    for function in functions:
        # reset the counters
        verified = True
        sum_count = 0
        sum_total_time = 0

        for graph in graphs:
            before_time_ns = time.time_ns()
            count = function(graph)
            after_time_ns = time.time_ns()

            if not is_vertex_cover_correct(graph):
                verified = False
                break

            total_time_ns = after_time_ns - before_time_ns

            sum_count += count
            sum_total_time += total_time_ns

        average_count = sum_count / len(graphs)
        average_time = sum_total_time / len(graphs)

        performances.append((verified, average_count, average_time))

        # I have reset all the graphs
        for graph in graphs:
            for vertex in graph.vertices():
                vertex.set_element(None)

            for edge in graph.edges():
                edge.set_element(1)

    return performances
