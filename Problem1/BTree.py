import numpy as np
import platform
from node import Node
from collections import MutableMapping

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
        pass

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        pass

    def __setitem__(self, k, v) -> None:
        pass

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

    """
    def _add_root(self, k, v) -> _Node:
        list = list[self.order_d*None]
        list = np.ascontiguousarray(list)
        root = _Node.__init__(list[self.order_d*None], None)
    """

tree = BTree(np.dtype('U16'), int)

pair_type = np.dtype([("key", tree._key_type), ("value", tree._value_type)])

element1 = Node(pair_type, tree._order)

print(element1._struct.itemsize)
