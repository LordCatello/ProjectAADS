Problem3

# Solution
In order to implement the DFS iteratively, we have changed the structure of graph's vertex. 
We have added two variables:

1. **dfs_predecessor** that represents the vertex from which we reached the current vertex.

2. **edges_to_visit** that memorizes the iterator-generator of the incident edges of the current vertex.

The implementation is composed by two functions that are in the **iterative_dfs.py** module.

The **dfs_complete** that takes as input a graph instance of the Graph class present in the **graph.py** module.
It looks for each not yet visited connected component of the graph and calls the **dfs** function on that connected component. If the graph is connected this result in only one call to the dfs(g,s) function.

The **dfs** function that takes as input the graph and a vertex representing the starting point of the dfs visit.
For each vertex of the connected component the algorithm saves the iterator-generator of the incident edges of the vertex in edges_to_visit, then it starts the visit of the adjacent vertices.
For each of these vertices the algorithm checks if it has already been visited by inspecting the value of the edges_to_visit variable. If it has not been visited then the current vertex is set as his predecessor and that vertex becomes the current one. 



## Complexity
The complexity of the algorithm is the same of the recursive one O(n+m).

