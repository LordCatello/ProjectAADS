from random import randint
from tree import Tree
# max_height is the maximum height of the tree, max_num_children is the maximum number of children
# that each tree can have

def build_tree(max_height,max_num_children):
    height = randint(1,max_height)
    queue = []
    tree = Tree()
    queue.append(tree)

    for i in height-1:
        num_children=randint(max_num_children)
        for j in num_children:
            queue.