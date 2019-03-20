from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import twins_color_initialization, degree_color_initialization
from algorithms.preprocessing import remove_twins


"""
With these methods, the graph isomorphism problem can be solved.
"""


def are_isomorph(G: "Graph", H: "Graph"):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    # WITHOUT TWIN REMOVAL
    G_disjoint_union = G + H
    return count_isomorphisms(degree_color_initialization(G_disjoint_union), [], [], False)

    # todo: implement in integration test
    # WITH TWIN REMOVAL
    # remove_twins(G)
    # remove_twins(H)
    # G_disjoint_union = G + H
    # return count_isomorphisms(twins_color_initialization(G_disjoint_union), [], [], False)


def amount_of_isomorphisms(G: "Graph", H: "Graph"):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    # WITHOUT TWIN REMOVAL
    G_disjoint_union = G + H
    return count_isomorphisms(degree_color_initialization(G_disjoint_union), [], [], True)

    # todo: implement in integration test
    # WITH TWIN REMOVAL
    # factor = remove_twins(G)
    # remove_twins(H)
    # G_disjoint_union = G + H
    # return factor * count_isomorphisms(twins_color_initialization(G_disjoint_union), [], [], True)




