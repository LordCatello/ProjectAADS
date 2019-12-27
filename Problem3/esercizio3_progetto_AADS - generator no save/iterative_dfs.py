"""
Performs a DFS traversal of a graph, in an iterative way.

:param g: the graph to traverse.
:param s: source node of the DFS traversal.
"""


def dfs(g, s):
    # visit the root of the DFS tree
    s.visited = True
    # the root has no predecessor
    s.dfs_predecessor = None

    while True:
        # Get an iterator over the incident edges in the node
        edges_to_visit = g.incident_edges(s)
        while True:
            try:
                e = next(edges_to_visit)
            except StopIteration:
                break
            # DEBUG
            print('elemento in s: ', s.element())
            x = e.endpoints()
            print('arco incide in: ', x[0].element(), ' ', x[1].element())
            # END DEBUG
            v = e.opposite(s)
            if not v.visited:
                # Visit the node on the opposite side of the edge
                v.visited = True
                v.dfs_predecessor = s
                # Move on it
                s = v
                edges_to_visit = g.incident_edges(s)

        if s.dfs_predecessor is not None:
            # go back to the previous node in the DFS tree, to continue
            # the inspection of its incident edges
            s = s.dfs_predecessor
        else:
            # all the incident edges for the root have been "relaxed",
            # so all the nodes which are reachable from the root have
            # have been visited, hence the algorithm can stop
            break

