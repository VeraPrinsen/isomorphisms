from supporting_components.graph import Graph, Vertex
from typing import List


def color_refinement(G: "Graph"):
    """
    Given graph G, this method changes the colornum property of the vertices in the graph, so that all vertices with
    the same colornum could be mapped to each other while structurally remaining the same graph
    :param G: Graph to be colored
    :return: Finished colored graph
    """

    # Get the current distribution of colors over the vertices and the maximum colornum in the graph
    colors, max_colornum = get_colors(G)

    has_changed = True
    while has_changed:
        has_changed = False
        for colornum, vertices in colors.copy().items():
            if len(vertices) == 1:
                continue

            max_colornum += 1
            has_changed = __colorgroup_refinement(colors, colornum, vertices, max_colornum) or has_changed
    return G


def get_colors(G: "Graph"):
    """
    Returns a map with the colors of the graph as keys and a list of all the vertices in the graph with that color as
    values and the maximum colornum property in the graph.
    :param G: The graph.
    :return: The color map and the maximum colornum
    """
    colors = {}
    max_colornum = 0
    for v in G.vertices:
        colors.setdefault(v.colornum, []).append(v)
        if v.colornum > max_colornum:
            max_colornum = v.colornum
    return colors, max_colornum


def __colorgroup_refinement(colors, colornum, vertices: List["Vertex"], next_colornum):
    """
    For vertices with property colornum = 'colornum', define which vertices have equal neighbours and which do not
    If a vertex within this group does not have the same neighbours as the first vertex in this group, these vertices
    will be given a new colornum 'next_colornum' and are moved from key colornum to next_colornum in the dictionary
    :param colors: Dictionary with property colornum as key and a list of vertices with that property as value
    :param colornum: Current colornum to be evaluated
    :param vertices: Vertices of that colornum to be evaluated
    :param next_colornum: The next colornum that was not in colors as a key before this colorgroup refinement
    :return has_changed: Returns if the colorgroup refinement has changed some colornum values for vertices
    """

    # Creates a list of all colornums of the neighbours of the first vertex in 'vertices'
    v0 = vertices[0]
    v0_colors = []
    for v in v0.neighbours:
        v0_colors.append(v.colornum)

    # Compare each vertex other than the first vertex in 'vertices' with the first vertex in 'vertices'
    # If the vertex is different, remember it in different_vertices
    has_changed = False
    different_vertices = []
    for v in vertices[1:]:
        if not __neighbours_equal(v0_colors, v):
            different_vertices.append(v)

    # After all vertices have been compared, change the colornum of all different vertices
    for v in different_vertices:
        v.colornum = next_colornum
        colors.setdefault(next_colornum, []).append(v)
        colors[colornum].remove(v)
        has_changed = True

    return has_changed


def __neighbours_equal(v0: List[int], v: Vertex):
    """
    Determines if the colornum properties of the neighbours of vertex 'v' matches with the list of colornum properties in
    the list v0_colors
    :param v0_colors: List of colornum properties of the neighbours of the vertex to be compared with
    :param v: The vertex that needs to be compared with vertex v0
    :return: Boolean if neighbours of vertex v0 and v are equal
    """
    v0_colors = v0.copy()
    for n in v.neighbours:
        if n.colornum in v0_colors:
            v0_colors.remove(n.colornum)
        else:
            return False
    return True