from test_functions import build_tree
from test_functions import check_tree
from btree import BTree
import btree
from node import Node
import numpy as np

# Configure BTree class for testing
btree.BLOCK_DIM = 90  # ensures order of 5

# Create integer to integer mapping B-tree
tree = BTree(int, int)

print(tree.order)

# EMPTY TREE
# Test root, should be None
root = tree.root
assert root is None
# Test len, should be zero
result = len(tree)
assert result == 0
# Test is_root
result = tree.is_root(None)
assert result is False
# Test inorder visit with empty tree
tree.inorder_vist()
# Test level dump with empty tree
tree.dump_level()
# Test is_empty, should be true
result = tree.is_empty()
assert result is True
# Test check_tree, should return true
result = check_tree(tree)
assert result is True
# Test __getitem__, should raise KeyError
try:
    x = tree[5]
except KeyError:
    pass
# Test __delitem__, should raise KeyError
try:
    del tree[1050]
except KeyError:
    pass
# Test iter
i = 0
for x in tree:
    i += 1
assert i == 0

# Add some elements
tree[50] = 1
tree[60] = 1
tree[70] = 1
tree[80] = 1
tree.dump_level()
# Check tree
assert check_tree(tree)
# Now should cause overflow
tree[90] = 1
tree.dump_level()
# Check tree
assert check_tree(tree)

# Insert some other elements
tree[97] = 1
tree[102] = 1
tree[40] = 1
tree[29] = 1
tree[20] = 1
tree[87] = 150
tree[32] = 1
tree[37] = 1
tree[53] = 1
tree[58] = 1000
tree[83] = 1
tree[85] = 1
tree[91] = 1
tree[110] = 1

"""
##################FALLISCE#############
# Test root
tree.dump_level()  # RIMUOVERE
# Check tree
assert check_tree(tree)
root = tree.root
root_node = [40, 70, 90]
i = 0
for element in root.elements:  # elements è l'intero array, non un iteratore
    print(element["key"])
    assert element["key"] == root_node[i]
    i += 1
result = tree.is_root(root)
assert result
"""

# Test root
tree.dump_level()  # RIMUOVERE
# Check tree
assert check_tree(tree)
root = tree.root
result = tree.is_root(root)
assert result

# Now should have an overflow
tree[95] = 1
tree[93] = 1
tree[96] = 1
tree[105] = 1
tree[120] = 1

tree.dump_level()
result = check_tree(tree)
assert result

# Try inorder visit
tree.inorder_vist()

# Test root
root = tree.root
root_node = [40, 70, 90, 97]
i = 0
for element in tree.root.elements:
    assert element["key"] == root_node[i]
    i += 1
result = tree.is_root(root)
assert result
pair_type = np.dtype(tree._key_type, tree._value_type)
node = Node(pair_type, tree.order)
result = tree.is_root(node)
assert not result

# NON CANCELLARE 58 E 87. AGGIORNA IL TEST DELLA LEN SOTTO

# Should cause an overflow that propagates to the root
tree[94] = 1
tree.dump_level()
result = check_tree(tree)
assert result

# Should cause an underflow solved with transfer from right sibling
del tree[93]
del tree[91]
tree.dump_level()
result = check_tree(tree)
assert result

# should cause a fusion with right child
del tree[94]
tree.dump_level()
result = check_tree(tree)
assert result

# Should cause an underflow propagating to the root, solved with fusion (both left and right fusion)
del tree[95]
del tree[96]
del tree[97]
del tree[102]
del tree[105]
tree.dump_level()
result = check_tree(tree)
assert result  # FAILS

# Should cause underflow with transfer from left sibling
del tree[110]
del tree[120]
tree.dump_level()
result = check_tree(tree)
assert result  # PROBABLY FAILS

# Test __getitem__ and __setitem__
x = tree[58]
assert x == 1000
x = tree[87]
assert x == 150
try:
    x = tree[1209]  # raises KeyError when given key is not in the tree
except KeyError:
    pass
try:
    tree[87] = None  # raises TypeError when setting key to None
except TypeError:
    pass
x = tree[87]
assert x == 150
try:
    x = tree[None]
except TypeError:
    pass

# Test len
result = len(tree)
assert result == 15

# Test is_empty
result = tree.is_empty()
assert not result


