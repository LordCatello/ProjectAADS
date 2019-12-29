# 27/12/2019

from tree import Tree


def vertex_cover_tree(tree: Tree) -> int:
    """
    It evaluates the minimum vertex cover of a tree.

    It evaluates the minimum vertex cover of the tree passed as parameter

    :param tree: the tree on wich the vertex cover is performed.

    :return      the number of nodes added to the vertex cover.
    """

    if tree is None:
        return 0

    if tree.get_num_children() == 0:
        tree.remove_from_vertex_cover(0)
        return 0

    vc_include_count = 1
    for child in tree.get_children():
        if child.is_vertex_cover_evaluated():
            vc_include_count += child.get_count()
        else:
            vc_include_count += vertex_cover_tree(child)

    vc_not_include_count = tree.get_num_children()
    for child in tree.get_children():
        for grandchild in child.get_children():
            if grandchild.is_vertex_cover_evaluated():
                vc_not_include_count += grandchild.get_count()
            else:
                vc_not_include_count += vertex_cover_tree(grandchild)

    if vc_include_count <= vc_not_include_count:
        tree.add_to_vertex_cover(vc_include_count)
    else:
        tree.remove_from_vertex_cover(vc_not_include_count)
        # if the current node is not included all the children have to be included
        for child in tree.get_children():
            # at this point is_include is certainly not None because the children are been
            # previously evaluated
            # in this case we are explictly inserting children in the vertex cover
            # in case they were not in the vertex cover we sum 1 to their vertex cover (themselves)
            if not child.is_included():
                child.add_to_vertex_cover(child.get_count()+1)

    return tree.get_count()


'''
def VertexCoverv2(r,vertex_cover):
    if (r == None):
        return 0
    if (r.num_children() == 0):
        vertex_cover[r]=0
        return 0

    VCin = 1
    for child in r.children():
        if(child in vertex_cover):
            VCin+=vertex_cover[child]
            continue
        VCin += VertexCoverv2(child,vertex_cover)

    VCout = r.num_children()

    for child in r.children():
        for grandchild in child.children():
            if(grandchild in vertex_cover):
                VCout+=vertex_cover[grandchild]
                continue
            VCout += VertexCoverv2(grandchild,vertex_cover)

    vc = min(VCin, VCout)
    vertex_cover[r]=vc
    if (vc == VCin):
        r.change_label('in')

    return vc
'''

