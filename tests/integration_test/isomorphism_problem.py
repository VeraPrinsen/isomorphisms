from algorithms.preprocessing import fix_degrees
from tests.integration_test.algorithm_options import apply_could_be_isomorphic, apply_remove_twins, apply_tree_algorithm, branching_method, apply_complement
from algorithms.color_initialization import degree_color_initialization
from supporting_components.graph import Graph


def preprocessing(G: "Graph"):
    """
    In this method all pre-processing is done that need to be done only one time. This method is called before any
    other computations are done.
    :param G: The graph to be preprocessed
    :return G_complement: If complement needed to be calculated, this is the complement of G, otherwise it is G itself
    :return factor: Factor the amount of automorphisms need to be multiplied with to get the right result
    """
    G_preprocessed = apply_complement(G)

    fix_degrees(G)
    fix_degrees(G_preprocessed)

    # Twin removal
    factor = apply_remove_twins(G)
    apply_remove_twins(G_preprocessed)

    return G_preprocessed, factor


def are_isomorph(G: "Graph", H: "Graph"):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    # Test if graphs are isomorphic using simple properties of the graphs
    if not apply_could_be_isomorphic(G, H):
        return False

    # If graph is a tree, use this algorithm to solve the GI problem
    problem_solved, is_isomorph = apply_tree_algorithm(G, H)
    if problem_solved:
        return is_isomorph

    # If GI problem is not solved, make a disjoint union of the graphs, color it and do branching
    G_disjoint_union = G + H
    degree_color_initialization(G_disjoint_union)

    return branching_method(G_disjoint_union, False)


def amount_of_automorphisms(G: "Graph"):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    # If graph is a tree, use this algorithm to solve the GI problem
    problem_solved, isomorph_count = apply_tree_algorithm(G)
    if problem_solved:
        return isomorph_count

    # If GI problem is not solved, make a disjoint union of itself, color it and do branching
    G_disjoint_union = G.self_disjoint_union()
    degree_color_initialization(G_disjoint_union)

    return branching_method(G_disjoint_union, True)