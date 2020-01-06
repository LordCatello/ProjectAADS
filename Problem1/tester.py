from test_functions import build_tree
from test_functions import check_tree
from btree import BTree

# Create integer to integer mapping B-tree
tree = BTree(int, int)

# EMPTY TREE
# Test root, should be None
root = tree.root
assert root is None
# Test len, should be zero
len = len(tree)
assert len == 0
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
