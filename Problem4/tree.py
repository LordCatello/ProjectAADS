# 27/12/2019

from queue import Queue


class Tree:
    __slots__ = '__children', '__included', '__count'

    def __init__(self, included: bool = None, count: int = 0):
        """
        It builds a new instance of Tree

        :param included:    It indicates if the node is included or not in the vertex cover.
                            It can be:
                            None: Vertex cover not evaluated yet for this node
                            True: Included in the vertex cover
                            False: Not included in the vertex cover

        :param count:       It indicates the number of nodes of the tree included in the vertex cover.
        """

        self.__children = []
        self.__included = included
        self.__count = count

    def get_children(self) -> 'Tree':
        for c in self.__children:
            yield c

    def get_num_children(self) -> int:
        return len(self.__children)

    def add_child(self, child: 'Tree'):
        self.__children.append(child)

    def is_included(self) -> bool:
        return self.__included

    def add_to_vertex_cover(self, count: int):
        """
        It adds the current node to the vertex cover

        It adds the current node to the vertex cover,
        setting "included" to True and "count" to "count".

        :param count: it is the number of nodes of this tree added to the vertex cover, including this node.
        """

        self.__included = True
        self.__count = count

    def remove_from_vertex_cover(self, count: int):
        """
        It removes the current node to the vertex cover

        It removes the current node to the vertex cover,
        setting "included" to False and "count" to "count".

        :param count: it is the number of nodes of this tree added to the vertex cover, including this node.
        """

        self.__included = False
        self.__count = count

    def get_count(self):
        return self.__count

    def is_vertex_cover_evaluated(self) -> bool:
        """
        It returns a boolean indicating if the vertex cover for this node has already been evaluated

        :return true if the vertex cover for this node has already been evaluated
                false otherwise
        """

        return self.is_included() is not None

    def dump(self):
        """
         Dumps the tree

         dump() prints the tree in the standard output.
         A new level is placed on a new line.
         The collection of children of two different nodes in the same line are divided by more space
         respects to the space used for the children of the same node.
         For each node, the "included" value and the "count" are printed.
        """

        queue = Queue()
        queue.put(self)

        while not queue.empty():
            print()
            count = queue.qsize()

            for i in range(0, count):
                element = queue.get()
                if element == "tab":
                    print(end="\t")
                else:
                    print(element.is_included(), " - ", element.get_count(), end="\t")

                    for child in element.get_children():
                        queue.put(child)
                    queue.put("tab")


