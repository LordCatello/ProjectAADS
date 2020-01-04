import numpy as np
import platform
from node import Node
from collections import MutableMapping
from math import floor

BLOCK_DIM = 1024
UINT = np.uint32
POINTER_DIM = int(platform.architecture()[0][:2]) // 8

class BTree(MutableMapping):
    __slots__ = "_root", "_size", "_key_type", "_value_type", "_order", "_min_internal_num_children"

    def __init__(self, key_type, value_type):
        """
        size:   Number of elements

        """

        self._root = None
        self._size = 0
        self._key_type = key_type
        self._value_type = value_type

        # note that an internal node
        self._order = self._compute_order()
        self._min_internal_num_children = self._order // 2

    def __delitem__(self, key):
        pass

    def __getitem__(self, key):
        current_node = self._root

        while current_node is not None:
            index = current_node.find_element_index(key)
            # if index >= current_node.size the key is surely not in the current node (maybe is in the rightmost child)
            if index < current_node.size:
                element = current_node.get_element_by_index(index)
                if element["key"] == key:
                    return element["value"]

            try:
                current_node = current_node.get_child_by_index(index)
            except IndexError:
                break

        return None

    def __len__(self) -> int:
        return self._size

    # what type of visit I have to perform? Inorder?
    def __iter__(self):
        pass

    def __setitem__(self, k, v) -> None:
        pass

    def is_empty(self) -> bool:
        return self._size == 0

    def _compute_order(self) -> int:
        """
        Evaluates the maximum number of children (d) allowed for the node.

        :return:            Returns the maximum number of children allowed for the node.
        """

        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])

        size_dim = UINT(0).itemsize
        node_dim = POINTER_DIM
        pair_dim = pair_type.itemsize

        # block_dim - numpy_array_overhead - size_dim - parent_dim (node_dim)
        remaining_dim = BLOCK_DIM - size_dim - node_dim

        order = (remaining_dim + pair_dim) // (pair_dim + node_dim)
        return order

    def insert_item(self, key, value):
        if self.is_empty():
            # create new node
            self._insert_new(key, value)
        else:
            # have to insert in proper position
            self._insert_existing(key, value)

    def _insert_new(self, key, value):
        # create new node
        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
        new_node = Node(pair_type, self._order)
        # add element to new node
        new_node.add_element(key, value)
        # set new node as root
        self._root = new_node
        # increase size
        self._size += 1

    def _insert_existing(self, key, value):
        inserted = False
        start = self._root
        while True:
            i = start.ceil_in_node(key, start)
            elements = start.elements
            children = start.children
            if i == 0 or elements[i - 1] < key:
                if children[i] is None:
                    break
                start = children[i]
            else:
                # previous element in node has same key
                elements[i - 1]["value"] = value
                inserted = True
                break
            
        if inserted:
            return
        # otherwise, in start there's a reference to the node to insert
        # the element into
        if start.is_full():
            # call split
            self._split_and_insert(key, value, start)
        else:
            start.add_element(key, value)
            start._size += 1

    def _split_and_insert(self, key, value, node):
        median = floor(node.size/2)






    """
    def _add_root(self, k, v) -> _Node:
        list = list[self.order_d*None]
        list = np.ascontiguousarray(list)
        root = _Node.__init__(list[self.order_d*None], None)
    """

tree = BTree(np.dtype('U16'), int)

pair_type = np.dtype([("key", tree._key_type), ("value", tree._value_type)])

element1 = Node(pair_type, tree._order)
element1.add_element("carmine", 3)
element1.add_element("pippo", 58)
element1.add_element("zelda", 3)

tree._root = element1
tree._size += 3

print(element1._struct.itemsize)
print(tree.__getitem__("pippo"))
