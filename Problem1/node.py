import numpy as np
import platform
from sys import getsizeof

UINT = np.uint32
POINTER_SIZE = int(platform.architecture()[0][:2]) // 8

class Node:
    def __init__(self, pair_type, max_number_of_children, parent = None):
        """
        Note:
        If you want to use a string, you have to use a dtype, str does not work, bceause you have to specify the dim of the str
        for example you can specify np.dtype('U16') for a 16 char string.
        In general, If you want to use an object, you have to define a dtype object, for the same reason of the str
        (Node need to know the dimension of the memory to allocate).
        """

        # defines the "node" type
        # I have to do this If I want that all the node is stored in a contiguous block of memory
        node_type = np.dtype([("size", UINT), ("elements", pair_type, max_number_of_children - 1), ("children", Node, max_number_of_children), ("parent", Node)])

        # It creates a contiguous memory block (an array). The array is of one element, because we have
        # previously defined a dtype that is a struct, containing the size, the elements (array), the children (array), the parent.
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

    def add_element(self, key, value):
        """
        Adds an element (pair key,value), to the node.
        If key is already present the new value is stored.
        Takes O(n) because the elements are ordered.

        :param key:         The key of the element
        :param value:       The value of the element

        :raise IndexError   Raise an exception if the node if full
        """

        if self.is_full():
            raise IndexError

        # Insert an element in an ordered array
        # Search the position where to insert the element
        # index = np.searchsorted(self._struct[0]["elements"], key)
        # It's better to use a binary search
        index = self.find_element_index(key)

        # If the key is not present, I have to shift all the elements
        if self._struct[0]["elements"][index]["key"] != key:
            # Move all the elements greater than key and add the element to the index position.
            for i in range(index, self.size):
                self._struct[0]["elements"][self.size + index - i] = self._struct[0]["elements"][self.size + index - i - 1]
            self.size = self.size + 1

        # Insert the element in index
        self._struct[0]["elements"][index] = (key, value)


    def find_element_index(self, key) -> int:
        # we have to implement a binary search, not a linear search
        found = False
        i = 0
        index = None

        while not found:
            if i == self.size or self._struct[0]["elements"][i]["key"] >= key:
                index = i
                found = True

            i += 1

        return index

    def get_element_by_index(self, index):
        if index >= self.size or index < 0:
            raise IndexError

        return self._struct[0]["elements"][index]

    def get_child_by_index(self, index):
        if index >= self.size + 1 or index < 0:
            raise IndexError

        return self._struct[0]["children"][index]




# peppe = Node(np.dtype('U16'), np.dtype(np.int32), 1024)
# element1 = Node(np.dtype(np.int64), np.dtype(np.int64), 256)
pair_type = np.dtype([("key", np.dtype('U16')), ("value", int)])

element1 = Node(pair_type, 5)

element1.add_element("carmine", 3)
element1.add_element("pippo", 3)
element1.add_element("zelda", 5)
element1.add_element("camillo", 9)

print(element1._struct)

"""
print(element1._struct.itemsize)
print(element1._struct[0]["size"].itemsize)
print(element1._struct[0]["elements"].itemsize)
print(element1._struct[0]["children"].itemsize)
# print(element1._struct[0]["parent"].itemsize)
"""