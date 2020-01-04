from btree import BTree
from node import Node
from test_functions import random_int
from test_functions import build_tree
import numpy as np

"""
Test file

"""

tree = BTree(np.dtype('U16'), int)
pair_type = np.dtype([("key", tree._key_type), ("value", tree._value_type)])

element1 = Node(pair_type, tree._order)
element1.add_element("carmine", 3)
element1.add_element("pippo", 58)
element1.add_element("zelda", 3)

element2 = Node(pair_type, tree._order)
element2.add_element("cecilia", 66)
element1._struct[0]["children"][1] = element2

tree._root = element1
tree._size += 4

print(tree.__getitem__("cecilia"))
tree.inorder_vist()

for el in tree.__iter__():
    print(el)

# use this function to build a tree
# build_tree(100, int, int, random_int, random_int)
