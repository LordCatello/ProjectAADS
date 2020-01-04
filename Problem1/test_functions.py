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

    return randint(0, 100)