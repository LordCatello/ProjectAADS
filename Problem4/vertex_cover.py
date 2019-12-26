from tree import Tree

def VertexCover(r):

    if (r == None):
        return 0
    if (r.num_children() == 0):
        r.update_vertex_count(0)
        return 0

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