from supporting_components.graph import Graph
from algorithms.color_initialization import degree_color_initialization
from algorithms.decide_gi import is_balanced


def could_be_isomorphic(G: 'Graph', H: 'Graph'):
    """
    Based on properties of the graphs a few simple comparisons are made to determine if the graphs could be isomorphic.
    :param G, H: The graphs of which it should be determined if they could be isomorphic.
    :return: Boolean that indicates if the two graphs could be isomorphic or not.
    """
    # Isomorphic graphs should have the same amount of vertices
    if len(G.vertices) != len(H.vertices):
        return False
    # Isomorphic graphs should have the same amount of edges
    if len(G.edges) != len(H.edges):
        return False
    # Isomorphic graphs should have the same amount of vertices with a specific degree
    G_disjoint_union = G + H
    degree_color_initialization(G_disjoint_union)
    if not is_balanced(G_disjoint_union)[0]:
        return False

    return True