Problem3

Problem3

# Solution
In order to implement the DFS iteratively, we have changed the structure of the Vertex class.
We have added two variables:

1. **dfs_predecessor**, that represents the vertex from which we reached the current one, set by default to None.

2. **edges_to_visit**, that memorizes the iterator-generator of the incident edges of the current vertex, set by default to None.

The implementation is composed by two functions, **dfs_complete(g)** and **dfs(g,s)** that are in the **iterative_dfs.py** module.

The **dfs_complete(g)** function takes as input a graph, instance of the Graph class present in the **graph.py** module.
It looks for each not yet visited connected component of the graph received as an argument, and calls the *dfs(g,s)* function on each of these connected components. If the graph is connected, this results in only one call to the *dfs(g,s)* function.

The **dfs(g,s)** function takes as input the graph and a vertex representing the starting point of the dfs visit (the *source*).
Starting from the source, the visit consists in saving the iterator-generator for the incident edges in *edges_to_visit*, setting the *dfs_predecessor* to None, and considering the vertices adjacent to it.
For each adjacent vertex, the algorithm checks if it has already been visited, by inspecting the value of the *edges_to_visit* attribute (finding it set to None means the vertex has not been visited yet), and, if it's not the case, it sets the source as its *dfs_predecessor*, and makes this vertex the current one. The process then proceeds as for the source.
When all the vertices adjacent to a certain one have been visited, the algorithm "goes back" to the *dfs_predecessor* of the current node, by setting it as the new current one.
The algorithm terminates when the predecessor of the current node is None, because this indicates that this node is the source of the visit.

## Alternative implementations


# Time complexity
The time complexity of the algorithm is the same of the recursive one, $O(n + m)$.
We can prove this by analizing separately the two functions in the **iterative_dfs.py** module.
The **dfs_complete(g)** function performs a constant-time `if` statement on every node of the graph `g`, and a call to **dfs(g, s)**, on a certain source node, for each of its connected component.
In the **dfs(g, s)** function, the inner `while` performs constant-time operations on each of the edges adjacent to a current one (named `s`), and it's exectued, toghether with a constant-time `if` statement, for each vertex in the connected component of `g` that contains `s` (outer `while`). So this functions' complexity is $O(\sum_{s \in G(s)}deg(s))$, where *G(s)* is the connected component of `g` that contains `s`.
Since this function is called by **dfs_complete(g)** on each of the connected components of `g`, and the connected components are disjoint sets of vertices, this results in a total complexity of $O( \sum_{G(s) \in g}(\sum_{s \in G(s)}deg(s)))$, that is $O(\sum_{v \in g}deg(v))$, that is $O(n + m)$.

# Usage instructions