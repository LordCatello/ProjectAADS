# 27/12/2019


def VertexCover(tree):

    if tree is None:
        return 0

    if tree.num_children() == 0:
        tree.set_element('out')
        return 0

    if

    VCin = 1
    for child in r.children():
        VCin += VertexCover(child)

    VCout = r.num_children()

    for child in r.children():
        for grandchild in child.children():
            VCout += VertexCover(grandchild)

    vertex_cover= min(VCin,VCout)
    r.update_vertex_count(vertex_cover)
    if(vertex_cover==VCin):
        r.change_label('in')

    return vertex_cover

i=0

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


