"""
Performs a DFS traversal of a graph, in an iterative way.

:param g: the graph to traverse.
:param s: source node of the DFS traversal.
"""

def dfs(g, s):
    # visit the root of the DFS tree
    s.edges_to_visit = 0
    # the root has no predecessor
    s.dfs_predecessor = None
    while True:
        while True:
            if s.edges_to_visit < len(g.incident_edges(s)):
                e = g.incident_edges(s)[s.edges_to_visit]
                s.edges_to_visit += 1
            else:
                break
            # DEBUG
            print('elemento in s: ', s.element())
            x = e.endpoints()
            print('arco incide in: ', x[0].element(), ' ', x[1].element())
            # FINE DEBUG
            v = e.opposite(s)
            if v.edges_to_visit == -1:
                v.edges_to_visit = 0
                v.dfs_predecessor = s
                s = v

        if s.dfs_predecessor is not None:
            # go back to the previous node in the DFS tree, to continue
            # the inspection of its incident edges
            s = s.dfs_predecessor
        else:
            # all the incident edges for the root have been "relaxed",
            # so all the nodes which are reachable from the root have
            # have been visited, hence the algorithm can stop
            break

