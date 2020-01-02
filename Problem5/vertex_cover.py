# 28/12/2019

from graph import Graph


def vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph.

    It starts from a random vertex, computes its degree (number of adjacent vertices not in the
    vertex cover), then for each adjacent vertex not already in the vertex cover, compares the two
    degrees. The vertex with the greatest degree is added to the vertex cover and
    all its edges are set as "removed" from the graph.
    This is repeated on every vertex of the graph.

    This function assumes that all the vertices are initialized with "None"
    and all the edges are initialized with 1.
    If this is not True the algorithm could not work.

    The complexity of this algorithm is linear.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return:        the number of vertex included in the vertex cover.
    """

    count = 0
    for v in graph.vertices():
        # if the vertex is already in the vertex cover then skip this iteration
        if v.element():
            continue

        current_degree = sum(graph.incident_edges_element(v))

        for u in graph.neighbour_vertices(v):
            # if my neighbour is already in the vertex cover then skip this iteration
            if u.element():
                continue

            count += 1
            # if my neighbour has a degree bigger then mine put him in the solution
            # and "remove" all is incident edges.
            if sum(graph.incident_edges_element(u)) > current_degree:
                current_degree -= 1
                u.set_element(True)
                for e in graph.incident_edges(u):
                    e.set_element(0)

            # if i have a degree bigger then my neighbour put me in the solution
            # and "remove" all my incident edges, then break so go to the next vertex
            else:
                v.set_element(True)
                for e in graph.incident_edges(v):
                    e.set_element(0)
                break
    return count
