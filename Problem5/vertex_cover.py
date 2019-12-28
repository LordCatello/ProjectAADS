# 28/12/2019

from graph import Graph

"""
It evaluates a vertex cover for the graph using the approx_vertex_algorithm.

The approx_vertex_algorithm is a simple 2-approximation algorithm.
It is linear.

:param graph:   the graph on which the vertex cover is evaluated.

:return         the number of vertex included in the vertex cover.
"""
def approx_vertex_cover(graph: Graph) -> int:
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


"""
It evaluates a vertex cover for the graph using our algorithm

:param graph:   the graph on which the vertex cover is evaluated.

:return         the number of vertex included in the vertex cover.
"""
def degree(graph,v) -> int:
    count = 0
    for edge in graph.incident_edges(v):
        if edge.element() == 'removed':
            continue
        count+=1
    return count

def vertex_cover(graph: Graph) -> int:
    count = 0
    for v in graph.vertices():
        current_degree = degree(graph,v)
        for edge in graph.incident_edges(v):
            u = edge.opposite(v)
            if(degree(graph,u) > current_degree):
                u.set_element(True)
                count+=1
                for e in graph.incident_edges(u):
                    e.set_element('removed')
            else:
                v.set_element(True)
                count+=1
                for e in graph.incident_edges(v):
                    e.set_element('removed')
    return count







