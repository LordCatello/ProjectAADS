# 28/12/2019

from graph import Graph


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

        current_degree = compute_degree(graph,v)

        for edge in graph.incident_edges(v):
            u = edge.opposite(v)
            # if my neighboour is already in the vertex cover then skip this iteration
            if u.element():
                continue
            # if my neighboour has a degree bigger then mine put him in the solution
            # and "remove" all is incident edges.
            if(compute_degree(graph,u) > current_degree):
                u.set_element(True)
                count+=1
                current_degree-=1
                for e in graph.incident_edges(u):
                    e.set_element("removed")
            # if i have a degree bigger then my neighboour put me in the solution
            # and "remove" all my incident edges, then break so go to the next vertex
            else:
                v.set_element(True)
                count+=1
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

