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
        Builds an instance of a BTree.
        d (the maximum number of children), is not a parameter. It depends on the dimension of a memory block.
        It is assumed, for this exercise, that the dimension of the memory block is BLOCK_DIM bytes.

        :param key_type:         The type of the key.
        :param value_type:       The type of the value.
        """

        self._root = None
        self._size = 0
        self._key_type = key_type
        self._value_type = value_type
        self._order = self._compute_order()
        self._min_internal_num_children = self._order // 2

    def __delitem__(self, key):
        pass

    def __getitem__(self, key):
        """
        Returns the value given the key.
        The time complexity of this function is ( f(d) / (log(d-1) ) * log (n)
        where:
        n is the number of elements
        d the maximum number of children
        f(d) the time needed to search an item in a node. It's log(d) if the binary search algorithm is used.

        :param key      The key of the element.
        :return:        The value corresponding to the key, if the key is found,
                        None otherwise.
        """

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

    def inorder_vist(self):
        """
        In-Order visit of the tree.
        The visit takes O(n).

        Prints to the standard output all the element of the tree visited in-order (crescent order of the key).
        """

        self._inorder_visit_recursive(self._root)


    def _inorder_visit_recursive(self, node):
        # I have to define a new function, because I need to pass as parameter the node
        # I can't do this in inorder_visit because the function is public and the user should
        # not pass the node as parameter.

        if node is None:
            return

        if node.size <= 0:
            return

        elements = node.elements
        children = node.children

        for i in range(node.size):
            self._inorder_visit_recursive(children[i])
            print(elements[i])

        self._inorder_visit_recursive(children[node.size])


    def __iter__(self):
        """
        Returns an iterator over the elements the tree.

        The elements are returned in a crescent order (in-order visit).

        :return:    an iterator over the elements of the tree.
        """

        return self._iter_inorder(self._root)


    def _iter_inorder(self, node):
        if node is None:
            return

        if node.size <= 0:
            return

        elements = node.elements
        children = node.children

        for i in range(node.size):
            yield from self._iter_inorder(children[i])
            yield elements[i]

        yield from self._iter_inorder(children[node.size])


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
        # Create new node
        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
        new_node = Node(pair_type, self._order)
        # Move some elements to new node

        """
        Problemi:
        - Devo spostare elementi da node a quello nuovo, quindi mi serve un modo per "mettere a null" gli elementi
        rimossi nel vecchio nodo
        - devo spostare i child, solo che non c'è la add_child in Node
        - Devo gestire la propagazione dell'overflow
        """







