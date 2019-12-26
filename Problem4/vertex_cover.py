
def VertexCover(t):

    if (r == None):
        return
    if (r.num_children() == 0):
        return 0
    VCin = 1
    for child in r.children():
        VCin += VertexCover(child)

    VCout = r.num_children()

    for child in r.children():
        for grandchild in child.children():
            VCout += VertexCover(grandchild)