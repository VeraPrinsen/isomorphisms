from supporting_components.graph import Graph, Vertex
from algorithms.color_initialization import degree_color_initialization
from algorithms.decide_gi import __is_balanced
from math import factorial


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
    degree_color_initialization(G)
    degree_color_initialization(H)
    if not __is_balanced(G + H)[0]:
        return False

    return True


def remove_twins(G: 'Graph'):
    """
    Removes the twins from the graph (Twins are vertices that share the same neighbours)
    Next to twins, also triplets and any number of similar vertices with the same neighbours are taken into account.
    :param G: The graph of which the twins needs to be removed
    :return factor: To find the right amount of isomorphisms, the amount of isomorphisms found with the remaining
    graph should be multiplied by this factor.
    """
    queue = []
    for v in G.vertices:
        queue.append(v)

    factor = 1
    while len(queue) > 0:
        v0 = queue.pop(0)
        twin_list = []
        for v1 in queue:
            if are_twins(v0, v1):
                # v0 and v1 are twins, add to list for removal later
                twin_list.append(v1)

        # For a pair of twins, if one of them is removed, you will still find half of all isomorphisms.
        # If there exists a triplet, if only one of them is kept in, you have to multiply the amount of
        # isomorphisms found by 3! = 6.
        # In general, for all n vertices that have the same neighbours, if only one is kept. The factor
        # should be multiplied by n!.
        factor *= factorial(len(twin_list) + 1)
        for twin in twin_list:
            # delete all twins from the graph G
            G.del_vertex(twin)
            # also remove it from the queue
            queue.remove(twin)

    return factor


def are_twins(v0: "Vertex", v1: "Vertex"):
    """
    Vertices are twins if:
    1) They are not connected to each other and v0.neighbours == v1.neighbours
    2) They are connected to each other and v0.neighbours \ v1 == v1.neighbours \ v0
    :param v0, v1: Vertices to be compared
    :return: Boolean if vertices v0 and v1 are twins or not
    """
    if v0 in v1.neighbours:
        v0_neighbours = v0.neighbours
        v0_neighbours.remove(v1)
        v1_neighbours = v1.neighbours
        v1_neighbours.remove(v0)
        return v0_neighbours == v1_neighbours
    else:
        return v0.neighbours == v1.neighbours