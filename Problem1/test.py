import numpy as np
from btree import BTree
from node import Node
from test_functions import check_tree
from test_functions import build_tree
from test_functions import random_int

"""
Test file

"""

"""
tree = BTree(np.dtype('U16'), int)
pair_type = np.dtype([("key", tree._key_type), ("value", tree._value_type)])

element1 = Node(pair_type, tree._order)
element1.add_element("carmine", 3)
element1.add_element("pippo", 58)
#element1.add_element("zelda", 3)

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
element1._struct[0]["children"][2] = element4
element4.parent = element1

tree._root = element1
tree._size += 4
#tree.inorder_vist()
#print(tree._order)
ret_val = tree._insertion_point('pio', 12)
for i in ret_val.elements:
    print(i["key"])

# print(tree.__getitem__("cecilia"))
# # tree.inorder_visit()
#
# for el in tree:
#     print(el)
#
# print(check_tree(tree))

"""

"""
for node in element2.children:
    print(node)
"""

# print(element2.is_leaf())



"""
print(tree.after(element1, 0))
print(tree.after(element3, 1))
print(tree.after(element1, 2))

print(tree.before(element1, 0))
print(tree.before(element1, 1))
print(tree.before(element3, 1))
"""

"""
# use this function to build a tree

"""

"""
tree = build_tree(10, int, int, random_int, random_int)

print(tree.order)
tree.inorder_vist()
print(check_tree(tree))
"""

# TEST TRANSFER RIGHT
tree = BTree(int, int)
pair_type = np.dtype([("key", tree._key_type), ("value", tree._value_type)])
print("a = ", tree._min_internal_num_children)

root = Node(pair_type, tree._order)
root.add_element(25, 3)
tree._root = root

left_child = Node(pair_type, tree._order)
left_child.add_element(10, 66)
left_child.add_element(15, 69)
left_child.add_element(21, 69)
root._struct[0]["children"][0] = left_child
left_child.parent = root

right_child = Node(pair_type, tree.order)
right_child.add_element(28, 66)
root._struct[0]["children"][1] = right_child
right_child.parent = root

left_grandchild1 = Node(pair_type, tree.order)
left_grandchild1.add_element(7, 66)
left_grandchild1.add_element(9, 66)
left_child._struct[0]["children"][0] = left_grandchild1
left_grandchild1.parent = left_child

left_grandchild2 = Node(pair_type, tree.order)
left_grandchild2.add_element(12, 66)
left_child._struct[0]["children"][1] = left_grandchild2
left_grandchild2.parent = left_child

left_grandchild3 = Node(pair_type, tree.order)
left_grandchild3.add_element(16, 66)
left_child._struct[0]["children"][2] = left_grandchild3
left_grandchild3.parent = left_child

left_grandchild4 = Node(pair_type, tree.order)
left_grandchild4.add_element(22, 66)
left_grandchild4.add_element(23, 66)
left_child._struct[0]["children"][3] = left_grandchild4
left_grandchild4.parent = left_child

tree._size += 11

tree.dump_level()

print(check_tree(tree))

#del tree[16]

"""

tree = BTree(int, int)

for i in range(20):
    tree[i] = i + 1

tree.inorder_vist()
print(len(tree))
print(check_tree(tree))
tree.dump_level()


"""
"""
tree = BTree(int,int)

print(tree.order)
print(tree.min_internal_num_children)
print(len(tree))


for i in range(50):
    tree[i]=i+1

print(check_tree(tree))

tree.graphic_dump()

del(tree[1])
del(tree[12])
del(tree[23])
del(tree[13])



tree.graphic_dump()
"""

