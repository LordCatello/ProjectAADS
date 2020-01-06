from btree import BTree
from node import Node
from random import randint
from copy import deepcopy

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
    4) each internal node has at most "order" children and at least min_number_children
    5) the depth property is correct. All the leaves are at the same level.
    
    :param tree:    The tree on which the check is performed.
    :return:        Return true if the tree is a BTree.
                    False otherwise.
    """

    if tree is None:
        return True

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

    # check the depth property
    is_correct = _check_depth(tree)

    if not is_correct:
        print("depth property not respected")
        return False

    return _check_a_b_property(a, b, tree.root)


def _check_depth(tree: BTree) -> bool:
    """
    Check the depth property of a tree.

    Check if all the leaves are at the same level.

    :param tree     The tree.

    :return         True if the depth property is correct.
                    False otherwise.
    """

    node = tree.root

    # if the tree has got no nodes, the property is correct
    if node is None:
        return True

    # find the level of a leaf
    level = 0
    is_leaf = False

    while not is_leaf:
        # if all the children are None node is a leaf
        # otherwise I continue to search in another child
        children = node.children
        is_leaf = True

        # for all the children
        for i in range(node.size + 1):
            if children[i] is not None:
                level += 1
                node = children[i]
                is_leaf = False
                break

    # now I found the level of a leaf
    # I have to check if all the leaves are on the same level that I found
    return _check_depth_recursive(tree.root, level, 0)


def _check_depth_recursive(node: Node, threshold: int, level: int) -> bool:
    """

    """
    if node is None:
        return True

    # if level > threshold I can stop here even if the node is not a leaf
    # because surely all the leaves that are children of this node
    # will not respect the property
    if level > threshold:
        return False

    is_leaf = True
    children = node.children

    for i in range(node.size + 1):
        if children[i] is not None:
            is_leaf = False
            is_correct = _check_depth_recursive(children[i], threshold, level + 1)
            if not is_correct:
                return False

    if is_leaf and threshold != level:
            return False

    return True




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


def test_delete(tree: BTree, number_of_deletes: int, debug: bool) -> bool:
    """
    Tests number_of_deletes "deletes" in the tree.
    The elements to delete are chosen randomly.

    A check is done after every delete.
    The check_tree() function is used in order to check if the tree is still a btree.
    and
    The __getitem__ function is used in order to check if the element has been effectively removed from the tree.

    If the tree has less elements than number_of_deletes
    all the elements are deleted.

    :param tree                 Tree.
    :param number_of_deletes    Number of elements to delete.
    :param debug                If debug is True, some debug prints are made
                                Otherwise only the failure cause will be printed.

    :return:                    True if all the deletes are correct (i.e. all the specified elements have been removed and check_tree() is True)
                                False otherwise
    """

    if len(tree) < number_of_deletes:
        total_elements_to_remove = len(tree)
    else:
        total_elements_to_remove = number_of_deletes

    # append all the elements to a temporary list
    elements = []
    for element in tree.__iter__():
        elements.append(element)

    for i in range(total_elements_to_remove):
        # change a random element from the list
        index = randint(0, len(elements) - 1)
        element = deepcopy(elements.pop(index))

        # delete element from tree
        if debug:
            print("Deleting item with key: ", element["key"])
        tree.__delitem__(element["key"])

        # check if the item has been effectively removed
        try:
            tree.__getitem__(element["key"])
            print("the item associated to key: ", element["key"], " has not been deleted")
            # If the key is found, return false
            return False
        except:
            pass

        # check the tree
        if not check_tree(tree):
            return False

    return True




