# 27/12/2019


"""
It evaluates the minimum vertex cover of a tree.

It evaluates the minimum vertex cover of the tree passed as parameter

:param tree: the tree on wich the vertex cover is performed.

:return      the number of nodes added to the vertex cover.
"""
def vertex_cover_tree(tree):
    if tree is None:
        return 0

    if tree.get_num_children() == 0:
        tree.remove_from_vertex_cover(0)
        return 0

    if tree.is_included() is not None:
        return tree.get_count()

    vc_include_count = 1
    for child in tree.get_children():
        vc_include_count += vertex_cover_tree(child)

    vc_not_include_count = tree.get_num_children()
    for child in tree.get_children():
        for grandchild in child.get_children():
            vc_not_include_count += vertex_cover_tree(grandchild)

    if vc_include_count <= vc_not_include_count:
        tree.add_to_vertex_cover(vc_include_count)
    else:
        tree.remove_from_vertex_cover(vc_not_include_count)

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

