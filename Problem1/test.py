import numpy as np
from btree import BTree
from node import Node
from test_functions import check_tree
from test_functions import build_tree
from test_functions import random_int

"""
Test file

"""
tree = BTree(int, int)

for i in range(21):
    tree[i]=i+1

print(check_tree(tree))
print(tree.order)
print(tree.min_internal_num_children)
tree.dump_level()

del tree[12]
del tree[13]

tree.dump_level()


