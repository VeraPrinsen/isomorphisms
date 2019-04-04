from supporting_components.graph import Graph, Vertex
from algorithms.color_initialization import degree_color_initialization
from algorithms.decide_gi import is_balanced
from math import factorial
from typing import List


def fix_degrees(G: "Graph"):
    """
    Because the property 'degree' of vertices changes when the neighbours change, a property degree_fixed is added
    to vertices to fix the degree of the vertex at this moment.
    :param G:
    :return:
    """
    for v in G.vertices:
        v.degree_fixed = v.degree


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


def remove_twins(G: 'Graph'):
    """
    Removes the twins from the graph (Twins are vertices that share the same neighbours)
    Next to twins, also triplets and any number of similar vertices with the same neighbours are taken into account.
    :param G: The graph of which the twins needs to be removed
    :return factor: To find the right amount of isomorphisms, the amount of isomorphisms found with the remaining
    graph should be multiplied by this factor.
    """
    # Put all vertices in a queue for evaluation
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
        v0.n_twins += len(twin_list)
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
        return neighbours_equal(v0_neighbours, v1_neighbours)
    else:
        return neighbours_equal(v0.neighbours, v1.neighbours)


def neighbours_equal(v0_neighbours: "List[Vertex]", v1_neighbours: "List[Vertex]"):
    for neighbour in v0_neighbours:
        if neighbour in v1_neighbours:
            v1_neighbours.remove(neighbour)
        else:
            return False
    return len(v1_neighbours) == 0


def use_complement(G: "Graph"):
    """
    Whether or not the graph has more edges than half of the maximal number of edges for the graph.
    If this is true, further processing with the complement of G will likely be faster.
    :param G: The graph
    :return: Whether or not the complement should be used for further processing
    """
    number_of_vertices = len(G.vertices)
    number_of_edges = len(G.edges)
    max_edges = (number_of_vertices * (number_of_vertices - 1)) / 2
    return number_of_edges > (max_edges/2)
