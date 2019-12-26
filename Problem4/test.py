from random import randint
from tree import Tree
import vertex_cover
# max_height is the maximum height of the tree, max_num_children is the maximum number of children
# that each tree can have
from vertex_cover import VertexCover

def print_tree(t):
    queue = [t]
    num_children = 0
    accumulator = 0
    i=0
    while len(queue) > 0 :
        current = queue.pop(0)
        print("     ", current.get_label(), "   ", end=" ")
        num_children -= 1
        for child in current.children():
            queue.append(child)

        if(num_children!=0):
            accumulator+= current.num_children()

        if(num_children==0):
            num_children = accumulator
            accumulator=0
            print('')
        if(i==0):
            i=1
            num_children=current.num_children()
            print('')



def build_tree():
    tree= Tree()
    child1 = Tree()
    child2 = Tree()
    child3= Tree()
    child4 = Tree()
    child5 = Tree()
    child6= Tree()
    child7 = Tree()
    child8= Tree()

    tree.add_child(child1)
    tree.add_child(child2)
    tree.add_child(child3)
    child1.add_child(child4)
    child1.add_child(child5)
    child2.add_child(child6)
    child3.add_child(child7)
    child3.add_child(child8)
    return tree

tree=build_tree()
print_tree(tree)
print(VertexCover(tree))
print_tree(tree)



