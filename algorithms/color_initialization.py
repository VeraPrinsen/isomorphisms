def degree_color_initialization(G: "Graph"):
    """
    Initializes the colornum properties of all vertices in graph G based on the degree of the vertices.
    :param G: The graph to be initialized
    :return The graph with the initial coloring
    """
    for v in G.vertices:
        v.colornum = v.degree
    return G


def twins_color_initialization(G: "Graph"):
    """
    Initializes the colornum properties of all vertices in graph G based on the degree of the vertices when twins
    have been removed.
    :param G: The graph to be initialized
    :return The graph with the initial coloring
    """
    for v in G.vertices:
        v.colornum = v.degree_fixed
    return G
