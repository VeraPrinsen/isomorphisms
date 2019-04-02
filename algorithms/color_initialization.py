def degree_color_initialization(G: "Graph"):
    """
    Initializes the colornum properties of all vertices in graph G based on the degree of the vertices.
    Initializes the max_colornum property of the graph as well.
    :param G: The graph to be initialized
    :return The graph with the initial coloring
    """
    max_colornum = 0
    for v in G.vertices:
        v.colornum = v.degree
        if v.colornum > max_colornum:
            max_colornum = v.colornum
    G.max_colornum = max_colornum
    return G


def twins_color_initialization(G: "Graph"):
    """
    Initializes the colornum properties of all vertices in graph G based on the degree of the vertices when twins
    have been removed.
    Initializes the max_colornum property of the graph as well.
    :param G: The graph to be initialized
    :return The graph with the initial coloring
    """
    max_colornum = 0
    for v in G.vertices:
        v.colornum = v.degree_fixed
        if v.colornum > max_colornum:
            max_colornum = v.colornum
    G.max_colornum = max_colornum
    return G
