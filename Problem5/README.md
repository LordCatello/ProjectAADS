README

README

# Problem 5

## Introduction
The problem is an example of the **vertex cover problem** on a graph. So ,for simplicity, in this and in all the documents and files related to the problem number 5, we will refer to the vertex cover problem and not to the bacefook problem.

## The algorithm
The algorithm that we have designed is greedy and consists of the following steps:
- for each vertex of the graph that has not been already added to the vertex cover, call it v, consider all its neighbour vertices that are not in the vertex cover.
- for v and for each neighbour, call it u, compute the degree. The degree is the score assigned to each vertex and it is the number of adjacent vertices not in the vertex cover.
- for each couple (v, u), add to the vertex cover the vertex with the highest degree. If v is added to the vertex cover, stop the iteration for the remaining couples (all the couples (v, u) are satisfied).

## Complexity
The complexity of this algorithm is O(n + m) where n is the number of vertices and m is the number of edges.

## Does the algorithm return an optimal solution?
The algorithm does not return always an optimal solution.

For example the optimal solution for this graph is the one in the first image.
Our algorithm could provide the solution of the second image, that is not optimal.

![optimal_solution.png](../../_resources/c8e8c2474bbe4fdba546a0ebc4148d94.png)   ![our_solution.png](../../_resources/e1bd753a8a3d4925ac9662c475593170.png)
    
## How to test the script
Our algorithm is a function called vertex_cover in the **vertex_cover.py** module, it takes in input a graph istance of the class Graph present in the module **graph.py** module. It evaluates the vertex cover on the graph and labels the vertices as **True** or **False**, if a vertex is True it is in the vertex cover otherwise not.

### The test.py
In this module, we just call a function that we made in order to evaluate the performances of different solutions the **evaluate_performances** present in the **test_functions.py** module.

This function takes as input:

1. An array of functions, that contains the functions for which the performances must be evaluated.
2. The number of graphs on which the performances must be evaluated (They are made of 100 vertices for default).
3. The probability that a vertex has and edge linking it with any other vertices.

This function creates as random graphs as specified in the second parameter using the function **build_random_graph** in the **test_functions.py** that takes in input the number of vertices and the probability specified in the third parameter.
Then each function is runned on each graph, calculating the time it takes and the value of the vertex cover that it returns.
For each graph the correcteness of the result is tested using the **is_vertex_cover_correct**.
At the end a mean of this values is calculated and returned.

If you dont want to use this function, all you have to do is creating a graph instance of the Graph class, with the default values of elements for vertices and edges, and pass it to the vertex_cover.
