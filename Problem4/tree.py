
class Tree():

    __slots__ = '_element', '_children'

    def __init__(self,element=None):
        self._children = []
        self._element=element

    def element(self):
        return self._element

    def num_children(self):
        return len(self._children)

    def children(self):
        for p in self._children:
            yield p

    def add_child(self,child):
        self._children.append(child)

    def update_element(self,new_element):
        self._element=new_element