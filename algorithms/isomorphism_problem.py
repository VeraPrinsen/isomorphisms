from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import degree_color_initialization


"""
With these methods, the graph isomorphism problem can be solved.
"""


def are_isomorph(G, H):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    G_disjoint_union = G + H

    return count_isomorphisms(degree_color_initialization(G_disjoint_union), [], [], False)


def amount_of_isomorphisms(G, H):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    G_disjoint_union = G + H

    return count_isomorphisms(degree_color_initialization(G_disjoint_union), [], [], True)




