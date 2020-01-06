import numpy as np
from btree import BTree
from node import Node
from test_functions import check_tree
from test_functions import build_tree
from test_functions import random_int
from test_functions import test_delete

"""
Test file

"""

"""
=======
>>>>>>> e005e18acf1da57f4d642ca34ee3ef3674ae082a
tree = BTree(int, int)

for i in range(21):
    tree[i] = i+1

print(check_tree(tree))
tree.dump_level()

<<<<<<< HEAD
print("delete 0")
del tree[0]
print(check_tree(tree))
print(len(tree))
tree.dump_level()

print("delete 11")
del tree[11]
print(check_tree(tree))
print(len(tree))
tree.dump_level()

print("delete 12")
del tree[12]
print(check_tree(tree))
print(len(tree))
tree.dump_level()
"""

tree = BTree(int, int)

for i in range(20):
    tree[i] = i + 1

print(check_tree(tree))

print(test_delete(tree, 30))



