from supporting_components.graph import Graph, Vertex
from typing import List


def color_refinement(G: "Graph"):
    """
    Given a graph G, this method changes the colornum property of the vertices in the graph to be unique for every vertex
    that could not be mapped to other vertices of the same colornum.
    :param G: Graph to be colored
    :return: Colored graph
    """

    colors, max_colornum = __initialize_colors(G)

    has_changed = True
    while has_changed:
        has_changed = False
        for colornum, vertices in colors.copy().items():
            max_colornum += 1

            if len(vertices) == 1:
                continue

            if __colorgroup_refinement(colors, colornum, vertices, max_colornum):
                has_changed = True
    return G


def __initialize_colors(G: "Graph"):
    """
    Initializes the colornum properties of all vertices in graph G.
    :param G: Graph to be initialized
    :return colors: Dictionary with colornums as keys and vertices as values
    :return max_colornum: The current maximum colornum key in the dictionary 'colors'
    """
    colors = {}
    max_colornum = 0
    for v in G.vertices:
        v.colornum = v.degree
        if v.degree > max_colornum:
            max_colornum = v.degree
        colors.setdefault(v.degree, []).append(v)
    return colors, max_colornum


def __colorgroup_refinement(colors, colornum, vertices: List["Vertex"], next_colornum):
    """
    For vertices with property colornum = 'colornum', define which vertices have equal neighbours and which do not
    If vertices within this group have not the same neighbours, these vertices will be given a new colornum and put in
    a new dictionary key
    :param colors: Dictionary with property colornum as key and a list of vertices with that property as value
    :param colornum: Current colornum to be evaluated
    :param vertices: Vertices of that colornum to be evaluated
    :param next_colornum: If vertices are different, give those vertices the next_colornum as property colornum
    """

    # Creates a list of alle colornums of the neighbours of the first vertex in 'vertices'
    v0 = vertices[0]
    v0_colors = []
    for v in v0.neighbours:
        v0_colors.append(v.colornum)

    # Compare the neighbours of each vertex in 'vertices' with the first vertex in 'vertices'
    has_changed = False
    for v in vertices[1:]:
        if not __neighbours_equal(v0_colors.copy(), v):
            v.colornum = next_colornum
            colors.setdefault(next_colornum, []).append(v)
            colors[colornum].remove(v)
            has_changed = True

    return has_changed


def __neighbours_equal(v0_colors: List[int], v: Vertex):
    """
    Determines if the colornum properties of the neighbours of vertex 'v' agrees with the list of colornum properties in
    the list v0_colors
    :param v0_colors: List of colornum properties of the neighbours of the vertex to be compared with
    :param v: The vertex that needs to be compared with vertex v0
    :return: Boolean if neighbours of vertex v0 and v are equal
    """
    for n in v.neighbours:
        if n.colornum in v0_colors:
            v0_colors.remove(n.colornum)
        else:
            return False
    return True