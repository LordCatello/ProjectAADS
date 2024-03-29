import numpy as np
import copy
from typing import Optional

UINT = np.uint32


class Node:
    def __init__(self, pair_type, max_number_of_children, parent=None):
        """
        Note:
        If you want to use a string, you have to use a dtype, str does not work, bceause you have to specify the dim
        of the str
        for example you can specify np.dtype('U16') for a 16 char string.
        In general, If you want to use an object, you have to define a dtype object, for the same reason of the str
        (Node need to know the dimension of the memory to allocate).
        """

        # defines the "node" type
        # I have to do this If I want that all the node is stored in a contiguous block of memory
        node_type = np.dtype([("size", UINT), ("elements", pair_type, max_number_of_children - 1),
                              ("children", Node, max_number_of_children), ("parent", Node)])

        # It creates a contiguous memory block (an array). The array is of one element, because we have
        # previously defined a dtype that is a struct, containing the size, the elements (array), the children (
        # array), the parent.
        self._struct = np.empty(shape=1, dtype=node_type)

        # size is the number of elements in the 'elements' array
        self._struct[0]['size'] = 0

        # 'parent' should be None because np.empty should return already None

    @property
    def size(self) -> UINT:
        return self._struct[0]["size"]

    @size.setter
    def size(self, value: UINT):
        self._struct[0]["size"] = value

    @property
    def parent(self) -> "Node":
        return self._struct[0]["parent"]

    @parent.setter
    def parent(self, value: "Node"):
        self._struct[0]["parent"] = value

    @property
    def children(self):
        return self._struct[0]["children"]

    @property
    def elements(self):
        return self._struct[0]["elements"]

    def is_full(self) -> bool:
        return self.size == len(self._struct[0]["elements"])

    def is_empty(self) -> bool:
        return self.size == 0

    def is_leaf(self) -> bool:
        leaf = True
        for child in self.children:
            if child is not None:
                leaf = False
        return leaf

    def is_root(self) -> bool:
        return self.parent is None

    def remove_element(self, key):

        if self.is_empty():
            return None
        else:
            index = self.find_element_index(key)
            if self.elements[index]["key"] != key:
                return None
            else:
                return self.remove_element_by_index(index)

    def remove_element_by_index(self, index):

        removed = copy.deepcopy(self.elements[index])
        for i in range(index, self.size - 1):
            self.elements[i] = self.elements[i + 1]

        self.size = self.size - 1
        return removed

    def add_element(self, key, value):
        """
        Adds an element (pair key,value), to the node.
        If key is already present the new value is stored.
        Takes O(n) because the elements are ordered and the order have to be preserved.

        :param key:         The key of the element
        :param value:       The value of the element

        :raise IndexError   Raise an exception if the node if full
        """

        # Insert an element in an ordered array
        # Search the position where to insert the element
        # index = np.searchsorted(self._struct[0]["elements"], key)
        index = self.find_element_index(key)

        self.add_element_by_index(index, key, value)


    def find_element_index(self, key) -> int:
        """
        Find the index of the element using binary search.

        :param key:     The key of the element

        :return:        If the element is found returns the index of the element,
                        otherwise returns the index where the element should be stored.
        """

        left = 0
        right = self.size

        while left < right:
            middle = (left + right) // 2
            middle_key = self.get_element_by_index(middle)["key"]
            if middle_key < key:
                left = middle + 1
            elif middle_key > key:
                right = middle
            else:
                return middle

        # if the element is not found, i return the index at which the element should be inserted
        return left

    def get_element_by_index(self, index: int):
        """
        Returns an element given the index as a deep copy.

        :param index:       The index of the element

        :return:            Returns the element stored in index position.
        :raise IndexError   Raise an exception if the index is out of bounds of the logical size of the array.
        """
        if index >= self.size or index < 0:
            raise IndexError

        return copy.deepcopy(self.elements[index])

    """
    def ceil_in_node(self, key):
        # returns the index of the smallest node element that has a key > to
        # the given one, or node.size if all the elements in the node have key
        # <= to the given key
        elements = self.elements
        i = 0
        for i in range(self.size):
            if elements[i]["key"] > key:
                return i
        return i + 1
    """

    def get_child_by_index(self, index: int) -> "Node":
        """
        Returns a child given the index.

        :param index:       The index of the child.

        :return:            Returns the child stored in index position.
        :raise IndexError   Raise an exception if the index is out of bounds of the logical size of the array.
        """

        if index >= self.size + 1 or index < 0:
            raise IndexError

        return self._struct[0]["children"][index]

    def get_index_from_parent(self) -> Optional[int]:
        """
        :return: the index of the parent's children array which points to this node or None if it has no
                 parent - i.e. it is the root.
        """
        key = self.get_element_by_index(0)["key"]  # arbitrary key choice
        parent = self.parent
        if parent is not None:
            return parent.find_element_index(key)
        else:
            return None

    def update_child(self, index: int, node: "Node"):
        self._struct[0]["children"][index] = node

        if node is not None:
            node.parent = self

    def print_node(self):

        for i in range(self.size):
            print(self.elements[i],end='')
        print()


    def add_element_by_index(self, index: int, key, value):
        if index >= len(self._struct[0]["elements"]):
            raise IndexError

        # If the key is not present, I have to shift all the elements
        if index == self.size or self._struct[0]["elements"][index]["key"] != key:
            # Move all the elements greater than key and add the element to the index position.
            for i in range(index, self.size):
                self._struct[0]["elements"][self.size + index - i] = self._struct[0]["elements"][self.size + index - i - 1]
            self.size = self.size + 1

        # if the key is presents
        self._struct[0]["elements"][index] = (key, value)

