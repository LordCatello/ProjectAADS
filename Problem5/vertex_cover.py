# 28/12/2019

from graph import Graph
import random


def approx_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using the approx_vertex_algorithm.

    The approx_vertex_algorithm is a simple 2-approximation algorithm.
    It is linear in time.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    edges = graph.edges()
    count = 0

    while len(edges) > 0:
        edge = edges.pop()
        (u, v) = edge.endpoints()
        u.set_element(True)
        v.set_element(True)
        count += 2

        # remove edges
        for remove_edge in graph.incident_edges(u):
            try:
                edges.remove(remove_edge)
            except:
                pass

        for remove_edge in graph.incident_edges(v):
            try:
                edges.remove(remove_edge)
            except:
                pass

    return count


def local_max_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using our algorithm.

    It starts from a random vertex, computes its degree = number of adjacent vertices not in the
    vertex cover, then for each adjacent vertex not already in the vertex cover compare the two
    degrees, the vertex with the greatest degree is added to the vertex cover
    all its edges are "removed" from the graph and the degree of the current vertex
    is updated. This is repeated on every vertex of the graph.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    count = 0
    for v in graph.vertices():
        # if the vertex is already in the vertex cover then skip this iteration
        if v.element():
            continue

        current_degree = compute_degree(graph, v)

        for edge in graph.incident_edges(v):
            u = edge.opposite(v)
            # if my neighbour is already in the vertex cover then skip this iteration
            if u.element():
                continue
            # if my neighbour has a degree bigger then mine put him in the solution
            # and "remove" all is incident edges.
            if compute_degree(graph, u) > current_degree:
                u.set_element(True)
                count += 1
                current_degree -= 1
                for e in graph.incident_edges(u):
                    e.set_element("removed")

            # if i have a degree bigger then my neighbour put me in the solution
            # and "remove" all my incident edges, then break so go to the next vertex
            else:
                v.set_element(True)
                count += 1
                for e in graph.incident_edges(v):
                    e.set_element("removed")
                break
    return count


def add_max_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using the remove_max_vertex_cover algorithm

    The remove_max_vertex_cover algorithm is a simple log(n)-approximation algorithm.
    It adds to the vertex cover always the vertex with the highest degree.
    The complexity is quadratic.


    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    vertices = graph.vertices()
    count = 0

    for i in range(len(vertices)):
        # take the vertex with the max degree
        max_degree = -1
        max_vertex = None
        for vertex in vertices:
            degree = compute_degree(graph, vertex)
            if degree > max_degree:
                max_degree = degree
                max_vertex = vertex

        # add this vertex to the vertex cover if his degree is greater than 0 (is connected to other vertices)
        if max_degree > 0:
            max_vertex.set_element(True)
            count += 1

        # set the label of all the incident edges as "removed"
        for edge in graph.incident_edges(max_vertex):
            edge.set_element("removed")

    return count


def random_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using the random_vertex_cover algorithm

    The random_vertex_cover algorithm is a very simple O(n) algorithm.
    For every pair of vertices that are not yet in the vertex cover,
    one of them is included in the vertex cover. The choice is random with the same probability.

    An evolution of this algorithm can be an algorithm that uses a weighted probability.
    The weight can be the degree of the vertex.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    count = 0

    for v in graph.vertices():
        # if the vertex is not in the vertex cover
        if not v.element():
            for edge in graph.incident_edges(v):
                u = edge.opposite(v)
                # if the vertex is not in the vertex cover
                if not u.element():
                    # I increment the count because I will add v or u to the vertex cover
                    count += 1
                    if bool(random.getrandbits(1)):
                        v.set_element(True)
                        # If I add v to the vertex cover I have to stop the iteration
                        break
                    else:
                        u.set_element(True)

    return count


def weighted_random_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using the weighted_random_vertex_cover algorithm

    The weighted_random_vertex_cover algorithm unify the random and local_max vertex cover algorithms.
    For every pair of vertices that are not yet in the vertex cover,
    one of them is included in the vertex cover.
    The choice is random with the probabilities weighted with the degrees of the vertices.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    count = 0
    for v in graph.vertices():
        # if the vertex is already in the vertex cover then skip this iteration
        if v.element():
            continue

        current_degree = compute_degree(graph, v)

        for edge in graph.incident_edges(v):
            u = edge.opposite(v)
            # if my neighbour is already in the vertex cover then skip this iteration
            if u.element():
                continue

            degree = compute_degree(graph, u)

            prob = current_degree / (current_degree + degree)

            choice = random.random()

            if choice > prob:
                u.set_element(True)
                count += 1
                current_degree -= 1
                for e in graph.incident_edges(u):
                    e.set_element("removed")
            else:
                v.set_element(True)
                count += 1
                for e in graph.incident_edges(v):
                    e.set_element("removed")
                break
    return count


def improved_local_max_vertex_cover(graph: Graph) -> int:
    """
    It evaluates a vertex cover for the graph using the improved_local_max_vertex_cover algorithm.

    For each vertex not yet in the vertex cover, compute the degree of this vertex and of all his neighbours not yet
    in the vertex cover.
    Add to the vertex cover, the vertices in order of max degree. If the starting vertex is added, stop the iteration,
    because all the pairs between this vertex and all other vertices are satisfied.

    :param graph:   the graph on which the vertex cover is evaluated.

    :return         the number of vertex included in the vertex cover.
    """

    count = 0

    for v in graph.vertices():
        # if the vertex is not in the vertex cover
        if not v.element():
            degrees_to_vertices = []
            degrees_to_vertices.append([v, compute_degree(graph, v)])
            for edge in graph.incident_edges(v):
                u = edge.opposite(v)
                # if the vertex is not in the vertex cover
                if not u.element():
                    degrees_to_vertices.append([u, compute_degree(graph, u)])

            while len(degrees_to_vertices) > 1:
                # take the vertex with the max degree
                max_element = (None, -1)
                for element in degrees_to_vertices:
                    if element[1] > max_element[1]:
                        max_element = element

                # add the vertex to the vertex cover
                max_element[0].set_element(True)

                # Remove all the incident edges
                for e in graph.incident_edges(max_element[0]):
                    e.set_element("removed")

                # update the counter
                count += 1

                # if the vertex added to the vertex cover is v, break
                if max_element[0] == v:
                    break

                # remove the element fro degrees_to_vertices
                degrees_to_vertices.remove(max_element)

                # update the degree of all the vertices
                for i in range(len(degrees_to_vertices)):
                    degrees_to_vertices[i][1] = compute_degree(graph, degrees_to_vertices[i][0])

            # Remove all the incident edges of v
            for e in graph.incident_edges(v):
                e.set_element("removed")


    return count


def compute_degree(graph: Graph, vertex) -> int:
    """
    It computes the degree of a vertex

    It computes the degree considering only the edges that are labeled as not removed.

    :param graph:   the vertex of the graph
    :param vertex   the vertex on which compute the degree

    :return         the degree of the vertex
    """

    count = 0
    for edge in graph.incident_edges(vertex):
        if edge.element() != "removed":
            count += 1

    return count

