import graph
import iterative_dfs

g = graph.Graph()
# insert vertices
v1 = g.insert_vertex(x=1)
v2 = g.insert_vertex(x=2)
v3 = g.insert_vertex(x=3)
v4 = g.insert_vertex(x=4)
v5 = g.insert_vertex(x=5)
v6 = g.insert_vertex(x=6)
v7 = g.insert_vertex(x=7)
v8 = g.insert_vertex(x=8)
v9 = g.insert_vertex(x=9)
v10 = g.insert_vertex(x=10)
v11 = g.insert_vertex(x=11)
# insert edges
e1_10 = g.insert_edge(v1, v10, None)
e1_2 = g.insert_edge(v1, v2, None)
e1_3 = g.insert_edge(v1, v3, None)
e1_4 = g.insert_edge(v1, v4, None)
e2_6 = g.insert_edge(v2, v6, None)
e3_4 = g.insert_edge(v3, v4, None)
e3_9 = g.insert_edge(v3, v9, None)
e3_5 = g.insert_edge(v3, v5, None)
e4_8 = g.insert_edge(v4, v8, None)
e4_6 = g.insert_edge(v4, v6, None)
e6_7 = g.insert_edge(v6, v7, None)

# write code to call dfs method
iterative_dfs.dfs_complete(g)
