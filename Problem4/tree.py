
class Tree():

    __slots__ = '_vertex_cover_count', '_children','_label'

    def __init__(self,element=None,label='out'):
        self._children = []
        self._vertex_cover_count=element
        self._label=label

    def element(self):
        return self._vertex_cover_count

    def num_children(self):
        return len(self._children)

    def children(self):
        if len(self._children)==0:
            return None
        for p in self._children:
            yield p

    def change_label(self,new_label):
        self._label=new_label

    def add_child(self,child):
        self._children.append(child)

    def update_vertex_count(self,new_vertex_count):
        self._vertex_cover_count=new_vertex_count