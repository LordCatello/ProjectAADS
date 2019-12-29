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
Our algorith could provide the solution of the second image, that is not optimal.

![optimal_solution.png](../../_resources/c8e8c2474bbe4fdba546a0ebc4148d94.png)   ![our_solution.png](../../_resources/e1bd753a8a3d4925ac9662c475593170.png)
    
## How to test the script
