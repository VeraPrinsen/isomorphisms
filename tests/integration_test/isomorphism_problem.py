from tests.integration_test.algorithm_options import apply_could_be_isomorphic, apply_remove_twins, branching_method

"""
With these methods, the graph isomorphism problem can be solved.
"""
def are_isomorph(G: "Graph", H: "Graph"):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    if not apply_could_be_isomorphic(G, H):
        return False

    G_disjoint_union, _ = apply_remove_twins(G, H)

    return branching_method(G_disjoint_union, False)


def amount_of_isomorphisms(G: "Graph", H: "Graph"):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    if not apply_could_be_isomorphic(G, H):
        return 0

    G_disjoint_union, factor = apply_remove_twins(G, H)

    return factor * branching_method(G_disjoint_union, True)