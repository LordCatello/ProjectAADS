from collections import MutableMapping


class ArrayMap(MutableMapping):
    """An implementation of a map using a 'static' array. Keys are directly used as indexes of the underlying array,
    so they must be integers.
    This was created in order to be more in control of the occupied memory in cases in which the size of the map is
    known.

    In the future, this class might be implemented with a true static array, maybe using libraries such as numpy.
    """
    __slots__ = '_array', '_size'

    def __init__(self, size: int):
        self._array = [None] * size
        self._size = size

    def __getitem__(self, key: int):
        try:
            return self._array[key]
        except IndexError as index_error:
            raise KeyError from index_error

    def __setitem__(self, key: int, value):
        try:
            self._array[key] = value
        except IndexError as index_error:
            raise KeyError from index_error

    def __delitem__(self, key: int):
        try:
            self._array[key] = None
        except IndexError as index_error:
            raise KeyError from index_error

    def __iter__(self):
        for index, _ in enumerate(self._array):
            yield index

    def __len__(self) -> int:
        """Returns the length of the underlying static array, and not the actual amount of elements."""
        return self._size
