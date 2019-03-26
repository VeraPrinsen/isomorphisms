from tests.integration_test.settings import preprocessing_simple_cases, twin_removal, color_refinement_algorithm, branching_algorithm
from supporting_components.graph import Graph
from algorithms.preprocessing import could_be_isomorphic, remove_twins
from algorithms.color_initialization import degree_color_initialization, twins_color_initialization
from algorithms.color_refinement import color_refinement, fast_color_refinement
from algorithms.branching import count_isomorphisms


"""
METHODS THAT PROVIDE ALL OPTIONS OF ALGORITHMS
"""
def apply_could_be_isomorphic(G: "Graph", H: "Graph"):
    if preprocessing_simple_cases:
        if not could_be_isomorphic(G, H):
            return False
    return True


def apply_remove_twins(G: "Graph", H: "Graph"):
    if twin_removal:
        factor = remove_twins(G)
        remove_twins(H)
        G_disjoint_union = G + H
        twins_color_initialization(G_disjoint_union)
    else:
        factor = 1
        G_disjoint_union = G + H
        degree_color_initialization(G_disjoint_union)

    return G_disjoint_union, factor


def color_refinement_method():
    if color_refinement_algorithm == 1:
        return color_refinement
    elif color_refinement_algorithm == 2:
        return fast_color_refinement


def branching_method(G: "Graph", count):
    if branching_algorithm == 1:
        return count_isomorphisms(G, [], [], count, color_refinement_method())