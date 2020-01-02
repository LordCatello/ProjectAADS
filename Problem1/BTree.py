from typing import TypeVar, _KT, _VT, Iterator
import numpy as np
from _collections import MutableMapping
import sys

BLOCK_SIZE = 1024

class BTree(MutableMapping[_KT, _VT]):

    class _Node:

        def __init__(self, list, parent=None):
            self._list = list
            self._parent = parent

    def __init__(self):
        key_size = np.dtype(_KT).itemsize
        value_size = np.dtype(_VT).itemsize
        references_size = 64
        order_d = int((BLOCK_SIZE - references_size)/(key_size + value_size + references_size*2))
        a = int(order_d/2)
        self.root = None
        self.size = 0

    def __delitem__(self, v: _KT) -> None:
        pass

    def __getitem__(self, k: _KT) -> _VT:
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator[_KT]:
        pass

    def __setitem__(self, k: _KT, v: _VT) -> None:
        pass

    def search_item(self):
        pass

    def _add_root(self, k: _KT, v: _VT) -> _Node:
        list = list[self.order_d*None]
        list = np.ascontiguousarray(list)
        root = _Node.__init__(list[self.order_d*None], None)

