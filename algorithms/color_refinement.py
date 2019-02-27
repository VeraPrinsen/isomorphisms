from supporting_components.graph import Graph, Vertex
from typing import List


def color_refinement(G: "Graph"):
    """
    Assuming there is no initial coloring
    :param G: Graph to be colored
    :return: Colored graph
    """

    colors, max_colornum = __initialize_colors(G)

    has_changed = True
    while has_changed:
        for color_num, vertices in colors.copy().items():
            if has_changed:
                max_colornum += 1
                has_changed = False

            if len(vertices) == 1:
                continue

            has_changed = __colorgroup_refinement(colors, vertices, max_colornum)
    return G


def __initialize_colors(G: "Graph"):
    colors = {}
    max_colornum = 0
    for v in G.vertices:
        v.colornum = v.degree
        if v.degree > max_colornum:
            max_colornum = v.degree
        colors.setdefault(v.degree, []).append(v)
    return colors, max_colornum


def __colorgroup_refinement(colors, vertices: List["Vertex"], max_colornum):
    """

    :param vertices:
    :param max_colornum:
    :return:
    """
    v0 = vertices[0]
    v0_colors = []
    for v in v0.neighbours:
        v0_colors.append(v.colornum)
    has_changed = False
    for v in vertices[1:]:
        if not __neighbours_equal(v0_colors.copy(), v):
            v.colornum = max_colornum
            colors.setdefault(max_colornum, []).append(v)
            colors[v0.colornum].remove(v)
            has_changed = True
    return has_changed


def __neighbours_equal(v0_colors: List[int], v: Vertex):
    """
    Assumes degree of vertex 1 and 2 are the same
    """
    for n in v.neighbours:
        if n.colornum in v0_colors:
            v0_colors.remove(n.colornum)
        else:
            return False
    return True