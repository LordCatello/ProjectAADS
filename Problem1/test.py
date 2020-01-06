import numpy as np
from btree import BTree
from node import Node
from test_functions import check_tree
from test_functions import build_tree
from test_functions import random_int

"""
Test file

"""

STANDARD_DIMENSION = 21


def set_up(dim):
    tree = create_tree(dim)
    print("start tree:")
    tree.dump_level()
    return tree


def tear_down(tree):
    if check_tree(tree):
        print("The tree is a correct B-Tree.")
    else:
        print("The tree is NOT a correct B-Tree!")


def delete_and_print_list(tree, key_list):
    for key in key_list:
        delete_and_print(tree, key)


def delete_and_print(tree, key):
    del tree[key]
    print("Deleted {}:".format(key))
    tree.dump_level()


def create_tree(dim):
    tree = BTree(int, int)

    for i in range(dim):
        tree[i] = i + 1

    print(check_tree(tree))
    print(tree.order)
    print(tree.min_internal_num_children)

    return tree


def delete_transfer_right_case():
    tree = set_up(STANDARD_DIMENSION)
    delete_and_print_list(tree, [0, 1])
    tear_down(tree)


def delete_transfer_left_case():
    # il transfer si genera indirettamente per uno swap del successore che genera underflow
    tree = set_up(STANDARD_DIMENSION)
    delete_and_print_list(tree, [0, 11, 12])
    tear_down(tree)


def delete_fusion_right_case():
    tree = set_up(STANDARD_DIMENSION)
    delete_and_print_list(tree, [0, 3, 1])
    tear_down(tree)


def delete_fusion_left_case():
    tree = set_up(STANDARD_DIMENSION)
    delete_and_print_list(tree, [3, 6, 7])
    tear_down(tree)


def delete_fusion_new_root():
    tree = set_up(4)
    delete_and_print_list(tree, [1, 3])
    tear_down(tree)


delete_fusion_new_root()
delete_fusion_right_case()
delete_transfer_right_case()
delete_fusion_left_case()
delete_transfer_left_case()

