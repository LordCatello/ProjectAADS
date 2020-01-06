from btree import BTree
from node import Node
from random import randint

def build_tree(elements_count: int, key_type, value_type, random_key_function, random_value_function) -> BTree:
    """
    Builds a tree.

    Builds a tree with elements_count elements, with random elements.

    :param elements_count           The total number of elements to put in to the tree (key, value)
    :param key_type                 The type of the key.
    :param value_type               The type of the value.
    :param random_key_function      A function that returns a random value of the specified key_type
    :param random_value_function    A function that returns a random value of the specified value_type
    :return:                        Returns a random generated tree with elements_count elements.
    """

    tree = BTree(key_type, value_type)

    for i in range(elements_count):
        tree.__setitem__(random_key_function(), random_value_function())

    return tree


def random_int() -> int:
    """
    Returns a random int.

    :return:    A random int value.
    """

    return randint(0, 1000)


def check_tree(tree: BTree) -> bool:
    """
    Checks if the tree is a BTree.
    The tree is a BTree if:
    1) the tree is ordered (the in-order visit is correct)
    2) the keys are unique
    3) the size of the tree is correct
    4) each internal node has at most order children and at least min_number_children
    
    :param tree:    The tree on which the check is performed.
    :return:        Return true if the tree is a BTree.
                    False otherwise.
    """

    is_btree = True

    # in-order check
    # and
    # check if the keys are unique
    test_size = 0
    prec = None
    for el in tree.__iter__():
        if prec is not None:
            # the in-order visit is not correct if
            if prec > el["key"]:
                print("in-order not true")
                return False
            if prec == el["key"]:
                print("keys not unique")
                return False

        prec = el["key"]

        test_size += 1

    # check the size
    if len(tree) != test_size:
        print("size not correct")
        return False

    # children check
    b = tree.order
    a = tree.min_internal_num_children

    # add also a check on the size

    return _check_a_b_property(a, b, tree.root)


def _check_a_b_property(a: int, b: int, node: "Node") -> bool:
    """
    Returns True if the a b property is verified.
    """
    if node is None:
        return True

    if node.size > (b - 1):
        print("b property not respected")
        return False

    # if the node is not the root
    if node.parent is not None:
        if node.size < (a - 1):
            print("a property not respected")
            return False

    # check the property for all the children
    for child in node.children:
        if not _check_a_b_property(a, b, child):
            return False

    return True

