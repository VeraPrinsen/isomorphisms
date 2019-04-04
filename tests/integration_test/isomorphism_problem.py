from algorithms.preprocessing import fix_degrees
from tests.integration_test.algorithm_options import apply_could_be_isomorphic, apply_remove_twins, apply_tree_algorithm, branching_method, apply_complement

"""
With these methods, the graph isomorphism problem can be solved.
"""
def are_isomorph(G: "Graph", H: "Graph"):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    fix_degrees(G), fix_degrees(H)

    if not apply_could_be_isomorphic(G, H):
        return False

    G = apply_complement(G)
    H = apply_complement(H)

    G_disjoint_union, _ = apply_remove_twins(G, H)

    problem_solved, is_isomorph = apply_tree_algorithm(G, H, False)
    if problem_solved:
        return is_isomorph

    return branching_method(G_disjoint_union, False)


def amount_of_isomorphisms(G: "Graph", H: "Graph"):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    fix_degrees(G), fix_degrees(H)

    if not apply_could_be_isomorphic(G, H):
        return 0

    G_disjoint_union, factor = apply_remove_twins(G, H)

    problem_solved, isomorph_count = apply_tree_algorithm(G, H, True)
    if problem_solved:
        return factor * isomorph_count

    return factor * branching_method(G_disjoint_union, True)