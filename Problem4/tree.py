# 27/12/2019


class Tree:
    __slots__ = '__children', '__element'

    def __init__(self, element=None):
        self.__children = []
        self.__element = element

    def get_children(self):
        for c in self.__children:
            yield c

    def get_num_children(self):
        return len(self.__children)

    def add_child(self, child):
        self.__children.append(child)

    def get_element(self):
        return self.__element

    def set_element(self, element):
        self.__element = element
