from btree import BTree
from node import Node
from test_functions import random_int
from test_functions import build_tree
from test_functions import check_tree
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
element2.add_element("ciccio", 69)
element1._struct[0]["children"][1] = element2
element2.parent = element1

element3 = Node(pair_type, tree._order)
element3.add_element("a", 1)
element3.add_element("b", 2)
element3.add_element("c", 3)
element1._struct[0]["children"][0] = element3
element3.parent = element1

element4 = Node(pair_type, tree._order)
element4.add_element("zi", 1)
element4.add_element("zo", 2)
element4.add_element("zu", 3)
element1._struct[0]["children"][3] = element4
element4.parent = element1

tree._root = element1
tree._size += 4

print(tree.__getitem__("cecilia"))
# tree.inorder_vist()

for el in tree.__iter__():
    print(el)

print(check_tree(tree))
print(tree.after(element1, 0))
print(tree.after(element3, 1))
print(tree.after(element1, 2))

print(tree.before(element1, 0))
print(tree.before(element1, 1))
print(tree.before(element3, 1))
# use this function to build a tree
# build_tree(100, int, int, random_int, random_int)
