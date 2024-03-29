import numpy as np
import platform
from node import Node
from collections import MutableMapping
from math import ceil
from math import floor
from typing import Tuple, Optional

from queue import Queue


BLOCK_DIM = 0

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

        # The order should be at least 4
        if self._order < 4:
            self._order = 4

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
        """
        deletes the item with that key
        :param key:
        :return:
        """
        if self.is_empty():
            raise KeyError
        else:
            current_node, index, current_index_from_parent = self._get_node_and_index(key)

            if current_node is None:
                raise KeyError

            elif self.is_root(current_node):
                self._size = self._size - 1
                if current_node.is_leaf():
                    current_node.remove_element_by_index(index)
                else:
                    after_node, after_index, successor_index_from_parent = self._swap_with_successor(current_node, index)
                    return self.remove_item(after_node, after_index, successor_index_from_parent)
            else:
                self._size = self._size - 1
                if current_node.is_leaf():
                    if current_node.size > self.min_internal_num_children - 1:
                        return current_node.remove_element_by_index(index)
                    else:
                        return self._delete_underflow(current_node,index, current_node.get_index_from_parent())
                else:
                    after_node,after_index, successor_index_from_parent =self._swap_with_successor(current_node,index)
                    return self.remove_item(after_node,after_index, successor_index_from_parent)

    def _swap_with_successor(self,current_node,index):
        """
        swap the element current_node[index] with its successor

        :param current_node: the current node that contains the element to be swapped
        :param index: the index of the element that have to be swapped
        :return:
        """
        after_node, after_index, successor_index_from_parent = self.after_node_index(current_node, index)
        to_remove = current_node.get_element_by_index(index)
        current_node.elements[index] = after_node.get_element_by_index(after_index)
        after_node.elements[after_index] = to_remove
        return (after_node,after_index, successor_index_from_parent)

    def _delete_underflow(self, node: Node, index_to_delete, index_from_parent):
        """
        Deletes the element if it's not a naive case.
        It firstly tries to make a transfer, otherwise it makes a fusion of nodes.
        In this case, it then restores the tree after an underflow by going upwards.
        """
        # can a transfer be executed?
        parent = node.parent

        if index_from_parent is None:
            # node is the root
            if node.size > 1:
                node.remove_element_by_index(index_to_delete)
                return
            else:
                # in this case the root is empty and has only one child
                # so the child becomes the new root
                self._root = node.children[0]
                self._root.parent = None
                return

        right_sibling, left_sibling = None, None

        if index_from_parent - 1 >= 0:
            left_sibling = parent.children[index_from_parent - 1]
        if index_from_parent + 1 < parent.size + 1:
            right_sibling = parent.children[index_from_parent + 1]

        if left_sibling is not None and left_sibling.size >= self._min_internal_num_children:
            return self.transfer_left(parent, index_from_parent - 1, node, index_to_delete, left_sibling)

        if right_sibling is not None and right_sibling.size >= self._min_internal_num_children:
            return self.transfer_right(parent, index_from_parent, node, index_to_delete, right_sibling)

        # no! a fusion is necessary
        if left_sibling is not None:
            self.fusion_left(parent, index_from_parent - 1, node, index_to_delete, left_sibling)
            self.remove_item(parent, index_from_parent - 1, parent.get_index_from_parent())
        elif right_sibling is not None:
            self.fusion_right(parent, index_from_parent, node, index_to_delete, right_sibling)
            self.remove_item(parent,index_from_parent, parent.get_index_from_parent())

    def fusion_left(self,parent, middle_index, current_node, index_to_remove, left_node):
        """
        performs a fusion with the left sibiling of the current_node

        :param parent: parent of the current node
        :param middle_index: index of the parent in which there is the element to take
        :param current_node: current node that is in underflow
        :param index_to_remove: index of the element to remove
        :param left_node: the left sibling that has to be merged with the current node
        :return:
        """
        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
        new_node = Node(pair_type, self.order)
        counter = 0
        for i in range(left_node.size):
            new_node.add_element(left_node.get_element_by_index(i)["key"],left_node.get_element_by_index(i)["value"])
            new_node.children[counter] = left_node.children[i]
            counter += 1
        new_node.children[counter] = left_node.children[left_node.size]
        counter += 1

        new_node.add_element(parent.get_element_by_index(middle_index)["key"],parent.get_element_by_index(middle_index)["value"])

        for i in range(current_node.size):
            element = current_node.get_element_by_index(i)
            if not (element['key'] == current_node.get_element_by_index(index_to_remove)['key']):
                new_node.add_element(element["key"],element["value"])
            new_node.children[counter]=current_node.children[i]
            counter += 1

        new_node.children[counter] = current_node.children[current_node.size]

        new_node.parent = parent
        parent.children[middle_index] = new_node
        for i in range(middle_index + 1, parent.size):
            parent.children[i] = parent.children[i + 1]

        parent.children[parent.size] = None

    def fusion_right(self,parent, middle_index, current_node, index_to_remove, right_node):
        """
        performs a fusion with the right sibiling of the current_node

        :param parent: parent of the current node
        :param middle_index: index of the parent in which there is the element to take
        :param current_node: current node that is in underflow
        :param index_to_remove: index of the element to remove
        :param right_node: the right sibling that has to be merged with the current node
        :return:
        """
        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
        new_node = Node(pair_type, self.order)
        counter = 0

        for i in range(current_node.size):
            element = current_node.get_element_by_index(i)
            if not (element['key'] == current_node.get_element_by_index(index_to_remove)['key']):
                new_node.add_element(element["key"],element["value"])
            new_node.children[counter] = current_node.children[i]
            counter += 1

        new_node.children[counter] = current_node.children[current_node.size]
        counter += 1
        new_node.add_element(parent.get_element_by_index(middle_index)["key"],parent.get_element_by_index(middle_index)["value"])

        for i in range(right_node.size):
            new_node.add_element(right_node.get_element_by_index(i)["key"],right_node.get_element_by_index(i)["value"])
            new_node.children[counter]=right_node.children[i]
            counter +=1

        new_node.children[i] =right_node.children[right_node.size]

        new_node.parent = parent
        parent.children[middle_index] = new_node
        for i in range(middle_index + 1, parent.size):
            parent.children[i] = parent.children[i + 1]
        parent.children[parent.size] = None


    def remove_item(self, node, index, index_from_parent):
        if node.size > self.min_internal_num_children - 1:
            return node.remove_element_by_index(index)
        else:
            return self._delete_underflow(node,index, index_from_parent)


    def transfer_left(self, parent, middle_index, current_node, index_to_remove, left_node):
        """
        performs a transfer to the left
        :param parent: parent of the node that is in underflow
        :param middle_index: the index of the element of the father that mast be swapped
        :param current_node: the current node that is in underflow
        :param index_to_remove: the index of the element to remove
        :param left_node: the left sibling of the node of that is in underflow
        :return:
        """
        middle_element = parent.get_element_by_index(middle_index)
        max_left_element = left_node.remove_element_by_index(left_node.size - 1)

        max_left_children = left_node.children[left_node.size + 1]
        parent.elements[middle_index]=max_left_element
        current_node.children[index_to_remove - 1] = max_left_children

        removed = current_node.remove_element_by_index(index_to_remove)
        current_node.add_element(middle_element["key"], middle_element["value"])
        return removed

    def transfer_right(self, parent, middle_index, current_node, index_to_remove, right_node):
        """
           performs a transfer to the right
           :param parent: parent of the node that is in underflow
           :param middle_index: the index of the element of the father that mast be swapped
           :param current_node: the current node that is in underflow
           :param index_to_remove: the index of the element to remove
           :param right_node: the right sibling of the node of that is in underflow
           :return:
           """
        middle_element = parent.get_element_by_index(middle_index)

        min_right_element = right_node.remove_element_by_index(0)
        min_right_children = right_node.children[0]

        current_node.children[index_to_remove+1] = min_right_children
        parent.elements[middle_index] = min_right_element
        removed = current_node.remove_element_by_index(index_to_remove)
        current_node.add_element(middle_element["key"],middle_element["value"])

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

        if key is None:
            raise TypeError("Key can't be none")

        if self.root is None:
          raise KeyError


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
        if node is None:
            return False

        return node == self._root and node.is_root()

    def _get_node_and_index(self, key) -> Tuple[Optional[Node], Optional[int], Optional[int]]:
        """
        :param key:     The key of the element.
        :return:        The node and the index of the array corresponding to the key, if the key is found,
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


    def graphic_dump(self):
        self._dump(self.root)


    def _dump(self,node):
        if node is not None:
            node.print_node()
            for child in node.children:
                self._dump(child)

    def dump_level(self):
        """
         Dumps the tree.

         Dumps the tree in the standard output.

         A new level is placed on a new line.

         The collection of children of two different nodes in the same line are divided by more space
         respects to the space used for the children of the same node.

         For each node, the size of the node and the array of elements are printed.
        """

        if self.is_empty():
            return

        queue = Queue()
        queue.put(self._root)

        while not queue.empty():
            print()
            count = queue.qsize()

            for i in range(0, count):
                queue_element = queue.get()
                if queue_element == "tab":
                    print(end="\t")
                else:
                    # print size
                    print("size:", queue_element.size, end=" - ")

                    elements = queue_element.elements
                    for j in range(queue_element.size):
                        print(elements[j], end=" ")

                    for child in queue_element.children:
                        if child is not None:
                            queue.put(child)
                    queue.put("tab")

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
        """
        Insert a new element in the tree.

        Insert a new element in the tree if the tree does not contain the key k.
        Otherwise update the element with the new value passed as parameter.

        :param k:   the key of the element.
        :param v:   the value of the element.
        """

        self._insert_item(k, v)

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

    def _insert_item(self, key, value):
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

    def _insertion_point(self, key, value):
        """
        If the given key is already in the tree, it substitutes its value with the given one. Otherwise,
        it returns the node in which the (key,value) pair must be inserted.

        :param key:         the key to be inserted as new element in the tree.
        :param value:       the value to be associated with the given key.
        :return:            None if the key is already in the tree, or the node in which it must be inserted.
        """
        node = self._root

        while True:
            i = node.find_element_index(key)

            if i < node.size:
                element = node.get_element_by_index(i)

                # If I found the element
                if element["key"] == key:
                    node.add_element(key, value)
                    return None

            # If I am here, I didnt' find the element
            # If the correct child is not None, I have to explore the child
            # Otherwise I have to return the current node
            child = node.children[i]
            if child is None:
                return node

            node = child


    def _insert_existing(self, key, value):
        insert_at = self._insertion_point(key, value)

        # I don't have to increment the size, because I update a previous value
        if insert_at is None:
            return

        # otherwise, in start there's a reference to the node to insert
        # the element into
        # otherwise I have to insert the element in a leaf
        # we use this array because we can't append a new child to the children of a node if is full,
        # because the array is static
        children = []
        # I add another child, because the node will contain another element
        for i in range(insert_at.size + 2):
            # the node is a leaf, so the children are all None
            children.append(None)

        self._insert_new_element_in_a_node(key, value, insert_at, children)

        self._size += 1


    def _insert_new_element_in_a_node(self, key, value, node: "Node", children: ["Node"]):
        """
        Insert (key, value) in a node.
        """
        # if node is None, I have to create a new root
        if node is None:
            # creating the new root
            pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])
            self._root = Node(pair_type, self._order)

            # add the new element
            self._root.add_element(key, value)

            # update the children
            self._root.update_child(0, children[0])
            self._root.update_child(1, children[1])
        elif node.is_full():
            self._overflow(key, value, node, children)
        else:
            node.add_element(key, value)

            # update the children
            for i in range(len(children)):
                node.update_child(i, children[i])


    def _overflow(self, key, value, node: "Node", children: ["Node"]):
        """
        Manages the overflow that happens in a node
        """

        # if the node is the root, we have to pay attention

        # evaluating the index of the median
        # floor is equivalent, it will chose a different but valid interval in the case
        # the array plus the new element is even.
        median_index = ceil(node.size / 2)

        # evaluating the index where to insert the new element
        new_element_index = node.find_element_index(key)

        # evaluating the element associated to the median index
        # we have to pay attention because we have not inserted yet the new element
        # so we have to use some if to get the correct median
        if median_index < new_element_index:
            median_element = node.get_element_by_index(median_index)
        elif median_index == new_element_index:
            median_element = (key, value)
        else:
            # I consider median_index - 1 because if I add the element in the array I have to shift to the right
            # all the previous elements
            # so in the starting array, the element is in the left
            median_element = node.get_element_by_index(median_index - 1)


        # creating two new Nodes
        pair_type = np.dtype([("key", self._key_type), ("value", self._value_type)])

        left_node = Node(pair_type, self._order)
        right_node = Node(pair_type, self._order)

        # insert the elements starting from 0 to median_index - 1 to the left_node and median_index + 1 to size to the right node
        # the elements array in node is not updated with the insertion of the new element, because we don't have space
        # se we have to use some if to assign the correct element
        for i in range(node.size + 1):
            if i < median_index:
                node_to_add = left_node
            elif i > median_index:
                node_to_add = right_node
            else:
                continue

            # we are sure that add is O(1) because we insert at the end of array
            # so we don't have to search the element and we don't have to shift the elements
            if i < new_element_index:
                element = node.get_element_by_index(i)
                node_to_add.add_element_by_index(node_to_add.size, element["key"], element["value"])
            elif i == new_element_index:
                node_to_add.add_element_by_index(node_to_add.size, key, value)
            else:
                element = node.get_element_by_index(i - 1)
                node_to_add.add_element_by_index(node_to_add.size, element["key"], element["value"])


        # I add the right children to the new nodes using the children array passed as parameter
        # I have to add children from index 0 to median_index to the left node
        # and children from index median_index + 1 to old_size to the right node
        left_counter = 0
        right_counter = 0
        for i in range(len(children)):
            if i <= median_index:
                left_node.update_child(left_counter, children[i])
                left_counter += 1
            else:
                right_node.update_child(right_counter, children[i])
                right_counter += 1

        # set the parent of the two nodes
        parent = node.parent

        # probably this is not useful. This should be already done in the next call of the function.
        left_node.parent = parent
        right_node.parent = parent

        # the creation of the two nodes is completed
        # all the reference to the old node in the children are already been deleted
        # I do this in the update_child for all the children
        # the reference in the parent node, will be updated in the next call to the _insert_new_element_in_a_node function

        # Now I have to evaluate the new array of children of the parent
        new_children = []

        if parent is not None:
            parent_children = parent.children
            node_index_in_parent = node.get_index_from_parent()
            for i in range(parent.size + 1):
                if i == node_index_in_parent:
                    new_children.append(left_node)
                    new_children.append(right_node)
                else:
                    new_children.append(parent_children[i])
        else:
            # if parent is None
            # node is the root
            # so the new children will be only the left and the right child
            new_children.append(left_node)
            new_children.append(right_node)


        self._insert_new_element_in_a_node(median_element[0], median_element[1], parent, new_children)








