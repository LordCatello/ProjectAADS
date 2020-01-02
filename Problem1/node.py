import numpy as np
from sys import getsizeof

UINT = np.uint32
ARRAY_OVERHEAD = 48  # bytes
WORD_SIZE = 8  # 64 bit

class Node:
    def __init__(self, key_dtype, value_dtype, block_dim):
        self._size = UINT(0)  # actual number of elements in the node

        pair_type = np.dtype([("key", key_dtype), ("value", value_dtype)])

        # print(pair_type.itemsize)
        order = Node._compute_order(pair_type, block_dim)
        print(order)
        # self._elements = np.dtype(pair_type, (order - 1,))
        self._elements = np.empty(shape=order-1, dtype=pair_type)
        self._children = np.empty(shape=order, dtype=np.int64)
        print(self._elements)
        # print(self._elements.itemsize)
        # self._elements = np.ascontiguousarray([(3.6, 5.3), (6.4, 6.7)], pair_type)

    @staticmethod
    def _compute_order(pair_type, block_dim) -> int:
        int_size = getsizeof(UINT(0))
        parent_size = getsizeof(np.int64(0))

        pointer_node_size = WORD_SIZE
        pair_element_size = pair_type.itemsize
        # we declares 2 array, one for the pair [key, value], and one for the children
        arrays_overhead_size = 2 * ARRAY_OVERHEAD

        # block_dim - dim(size) - dim(parent) - overhead(arrays)
        remaining_dim = block_dim - int_size - parent_size - arrays_overhead_size
        # print(remaining_dim)

        # This way I waste a pair
        return remaining_dim // (pair_element_size + pointer_node_size)


# peppe = Node(np.dtype('U16'), np.dtype(np.int32), 1024)
element = Node(np.dtype(np.float64), np.dtype(np.float64), 1024)

"""
print(np.dtype(np.int32).itemsize)
print(np.dtype(np.int16).itemsize)
print(getsizeof(element._elements))
"""