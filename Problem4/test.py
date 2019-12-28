# 27/12/2019

from random import randint
from queue import Queue

from tree import Tree
from vertex_cover_tree import vertex_cover_tree


"""
It builds a tree randomly
    
It builds a tree with as many nodes as specified in the parameters.
The number of childs of a node is chosen randomly between 1 and max_number_children
    
:param  number_nodes:           The number of nodes that the tree must have.

:param  max_number_children     The maximum number of children that a node can have

:return                         A tree built in according to the parameters.

"""
def build_random_tree(number_nodes: int = 10, max_number_children: int = 5) -> Tree:
    tree = Tree()
    queue = Queue()

    nodes_count = 1
    queue.put(tree)

    while nodes_count < number_nodes:
        element = queue.get()
        number_children = randint(1, max_number_children)
        children_count = 0

        while nodes_count < number_nodes and children_count < number_children:
            child = Tree()
            element.add_child(child)
            queue.put(child)
            children_count += 1
            nodes_count += 1
    return tree


tree = build_random_tree(30, 5)
tree.dump()
print(vertex_cover_tree(tree))
tree.dump()


# vertex_cover = {}
# print(VertexCoverv2(tree, vertex_cover))
# print(vertex_cover)
