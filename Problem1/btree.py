import numpy as np
import platform
from .node import Node
from collections import MutableMapping
from math import ceil
from math import floor
from typing import Tuple, Optional
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
        self._min_internal_num_children = int(ceil((self._order - 1) / 2))

    @property
    def order(self) -> int:
        return self._order

    @property
    def min_internal_num_children(self) -> int:
        return self._min_internal_num_children

    @property
    def root(self) -> Node:
        return self._root

    def __delitem__(self, key):
        if self.is_empty():
            raise KeyError
        else:
            current_node, index, current_index_from_parent = self._get_node_and_index(key)

            if current_node is None:
                return current_node
            else:
                if self.is_root(current_node) or current_node.size > self._min_internal_num_children - 1:
                    after_node, after_index, index_from_parent = self.after_node_index(current_node, index)
                    if after_node is None:
                        return current_node.remove_element_by_index(index)
                    else:
                        to_remove = current_node.get_element_by_index(index)
                        current_node.elements[index] = after_node.get_element_by_index(0)
                        after_node.elements[0] = to_remove
                        return self.remove_item(after_node, 0, index_from_parent)
                else:
                    self.remove_item(current_node, index, current_index_from_parent)

    def _delete_underflow(self, node: Node, index_to_delete):
        """
        Deletes the element if it's not a naive case.
        It firstly tries to make a transfer, otherwise it makes a fusion of nodes.
        In this case, it then restores the tree after an underflow by going upwards.
        """

        if node.size >= self._min_internal_num_children - 1:  # tree restored
            return

        # can a transfer be executed?
        parent = node.parent
        index_from_parent = node.get_index_from_parent()

        right_sibling, left_sibling = None, None

        if index_from_parent - 1 > 0:
            left_sibling = parent.children[index_from_parent - 1]
        if index_from_parent + 1 < parent.size:
            right_sibling = parent.children[index_from_parent + 1]

        if left_sibling is not None and left_sibling.size >= self._min_internal_num_children:
            return self.transfer_left(parent, index_from_parent, node, index_to_delete, left_sibling)

        if right_sibling is not None and right_sibling.size >= self._min_internal_num_children:
            return self.transfer_right(parent, index_from_parent, node, index_to_delete, right_sibling)

        # no! a fusion is necessary
        if left_sibling is not None:
            # fusion left
            pass





    def remove_item(self, node, index, index_from_parent):
        if node.size > self.min_internal_num_children - 1:
            return node.remove_element_by_index(index)
        else:
            parent = node.parent

            if index_from_parent != 0 and parent.chidren[index_from_parent - 1].size > self._min_internal_num_children - 1:

                middle_element_index = index_from_parent - 1
                left_node = parent.chidren[index_from_parent - 1]
                return self.transfer_left(parent, middle_element_index, node, index, left_node)

            elif parent.chidren[index_from_parent + 1].size > self._min_internal_num_children - 1:
                middle_element_index = index_from_parent
                right_node = parent.chidren[index_from_parent + 1]
                return self.transfer_right(parent, middle_element_index, node, index, right_node)

            else:
                middle_element_index = index_from_parent - 1
                left_node = parent.chidren[index_from_parent - 1]
                pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
                new_node = Node(pair_type, self.order)
                for i in range(left_node.size):
                    new_node.add_element(left_node.get_element_by_index(i))
                new_node.add_element(parent.get_element_by_index(middle_element_index))
                for i in range(node.size):
                    element = node.get_element_by_index(i)
                    if not(element['key'] == node.get_element_by_index(index)['key']):
                        new_node.add_element(element)
                new_node.parent = parent
                # parent.update_children()
                for i in range(middle_element_index, parent.size):
                    if i == middle_element_index:
                        parent.chidren[i] = new_node
                    else:
                        parent.chidren[i] = parent.chidren[i+1]

    def transfer_left(self, parent, middle_index, current_node, index_to_remove, left_node):
        middle_element = parent.elements[middle_index]
        removed = current_node.remove_element_by_index(index_to_remove)
        parent.elements[middle_index - 1] = left_node.remove_element_by_index(left_node.size - 1)
        current_node.add_element(middle_element['key'], middle_element['value'])
        return removed

    def transfer_right(self, parent, middle_index, current_node, index_to_remove, right_node):
        middle_element = parent.elements[middle_index]
        removed = current_node.remove_element_by_index(index_to_remove)
        parent.elements[middle_index] = right_node.remove_element_by_index(0)
        current_node.add_element(middle_element['key'], middle_element['value'])  # Maybe necessary do a add element at last position
        return removed

    def __getitem__(self, key):
        """
        Returns the value given the key.
        The time complexity of this function is ( f(d) / (log(d-1) ) * log (n)
        where:
        n is the number of elements
        d the maximum number of children
        f(d) the time needed to search an item in a node. It's log(d) if the binary search algorithm is used.

        :param key      The key of the element.
        :return:        The value corresponding to the key, if the key is found.
        :raise:         KeyError if the value is not found.
        """
        node, index, _ = self._get_node_and_index(key)
        if node is None or index is None:
            raise KeyError
        value = node.elements[index]['value']
        if value is None:
            raise KeyError

        return value

    def __len__(self) -> int:
        return self._size

    def is_root(self, node: Node) -> bool:
        return node == self._root and node.is_root()

    def _get_node_and_index(self, key) -> Tuple[Optional[Node], Optional[int], Optional[int]]:
        """
        :param key: The key of the element.
        :return: The node and the index of the array corresponding to the key, if the key is found,
                 None otherwise.
        """
        current_node = self._root
        index_from_parent = None

        while current_node is not None:
            index = current_node.find_element_index(key)
            # if index >= current_node.size the key is surely not in the current node (maybe is in the rightmost child)
            if index < current_node.size:
                element = current_node.get_element_by_index(index)
                if element["key"] == key:
                    return current_node, index, index_from_parent

            try:
                index_from_parent = index
                current_node = current_node.get_child_by_index(index)
            except IndexError:
                break

        return None, None, None

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

    @staticmethod
    def after_node_index(node: Node, index: int) -> Tuple[Optional[Node], Optional[int], Optional[int]]:
        """
        Finds the successor to the element specified by node and index.
        :return:
            Returns a tuple containing the node and the index of the successor element, and the index of this node
            in the parent's array of children.
            If everything is None, no successor was found.
        """
        current_node = node
        after_node = current_node.get_child_by_index(index + 1)

        if after_node is None:
            # if the node has no children greater than this key, i check in the node
            if index + 1 < current_node.size:
                # if there are other items, the successor is the next one
                return current_node, index + 1, current_node.get_index_from_parent()
            else:
                # if this is the last key in the node, i go upwards in the tree
                key = current_node.get_element_by_index(index)["key"]
                current_node = current_node.parent
                while current_node is not None:
                    parent_key_index = current_node.find_element_index(key)
                    if parent_key_index < current_node.size:
                        return current_node, parent_key_index, current_node.get_index_from_parent()
                    current_node = current_node.parent
                # there is no successor to this key
                return None, None, None
        else:
            # the node has children greater than this key, so i take the smallest child on the right
            while after_node is not None:
                if after_node.get_child_by_index(0) is None:
                    index_from_parent = index + 1
                    return after_node, 0, index_from_parent
                else:
                    after_node = after_node.get_child_by_index(0)
                    index = -1

        return None, None, None

    @staticmethod
    def after(node, index):
        """
        :return: The element successor to the element in the specified node at the specified index.
        """
        after_node, after_index, _ = BTree.after_node_index(node, index)
        if after_node is None:
            return None
        else:
            return after_node.elements[after_index]

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
            return  # consider moving this in the else branch of if statement

        # otherwise, in start there's a reference to the node to insert
        # the element into
        if start.is_full():
            # call split
            self._split_and_insert(key, value, start)
        else:
            # note that here I'm sure that the node I'm inserting
            # the pair into has no children
            start.add_element(key, value)
            # The size of the node is incremented in Node.add_element

        # I have to increase only the size of this tree
        self._size += 1

    def _split_and_insert(self, key, value, node: Node, left_child: Node, right_child: Node, pos: UINT):
        # Check that both children are specified or none is
        if (not left_child and (right_child or pos)) or (not right_child and (left_child or pos)):
            raise TypeError("left_child, right_child and pos must be all None or all specified")

            # Remove the node from parent's children, saving the index -> DO THIS WHEN INSERTING INSTEAD
            parent = node.parent()
            parent_children = parent.chidren()
            index_in_parent = 0
            for child in parent_children:
                if child is node:
                    child = None
                    break
                index_in_parent += 1
            # Remove median from node
            median_index = floor(node.size()/2)
            elements = node.elements()
            median = elements[median_index]  # it's pair_type
            # Create new node
            pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
            new_right_child = Node(pair_type, self._order)
            # If new element's key is greater than median's key, insert it
            # as first element of the new node
            if key > node.children()[median_index]["key"]:
                new_right_child.add_element(key, value)
            # Move elements greater than the median to new node
            for i in range(median_index + 1, node.size()):
                new_right_child.add_element(elements[i]["key"], elements[i]["value"])
                node._struct[0]["size"] -= 1
            # If new element's key is smaller than median's key, insert it
            # in place of the median
            if key < node.children()[median_index]["key"]:
                node.children()[median_index]["key"] = key
                node.children()[median_index]["value"] = value


            if key > node.children()[median_index]["key"]:
                # accounts for median removal
                node._struct[0]["size"] -= 1
            # insert a call to a function that inserts an element and associated left and right child and pos
            # into the tree (pos in index_in_parent)




        """
        Problemi:
        - Devo spostare elementi da node a quello nuovo, quindi mi serve un modo per "mettere a null" gli elementi
        rimossi nel vecchio nodo
        - devo spostare i child, solo che non c'è la add_child in Node
        - Devo gestire la propagazione dell'overflow
        """







