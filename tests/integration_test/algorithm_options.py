from tests.integration_test.settings import preprocessing_simple_cases, twin_removal, tree_algorithm, color_refinement_algorithm, branching_algorithm
from supporting_components.graph import Graph
from algorithms.preprocessing import could_be_isomorphic, remove_twins
from algorithms.tree_isomorphisms import is_tree, trees_count_isomorphisms
from algorithms.color_initialization import degree_color_initialization, twins_color_initialization
from algorithms.color_refinement import color_refinement, fast_color_refinement
from algorithms.branching import count_isomorphisms


"""
METHODS THAT PROVIDE ALL OPTIONS OF ALGORITHMS
"""
def apply_could_be_isomorphic(G: "Graph", H: "Graph"):
    """
    If preprocessing_simple_cases is set to True, apply the simple cases algorithm to determine is graphs are
    isomorphic using simple properties of the graphs.
    """
    if preprocessing_simple_cases:
        if not could_be_isomorphic(G, H):
            return False
    return True


def apply_remove_twins(G: "Graph", H: "Graph"):
    """
    If twin_removal is set to True, twin vertices are removed from both graphs. The factor with which the amount
    of isomorphisms found with the reduced graphs should be multiplied with is returned.
    Furthermore the graphs are colored based on the degrees before twins were removed, instead of the current
    amount of degrees of vertices.
    """
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


def apply_tree_algorithm(G: "Graph", H: "Graph", count_isomorphisms: "Bool"):
    """
    If the tree algorithm must be used, this method checks if G and H are trees.
    If they are the isomorphism problem is resolved using the tree isomorphism method.
    """
    if tree_algorithm:
        if is_tree(G) and is_tree(H):
            return True, trees_count_isomorphisms(G, H, count_isomorphisms)

    return False, None


def color_refinement_method():
    """
    This method returns the color_refinement method that is chosen in the settings.
    """
    if color_refinement_algorithm == 1:
        return color_refinement
    elif color_refinement_algorithm == 2:
        return fast_color_refinement


def branching_method(G: "Graph", count_flag: "Bool"):
    """
    This method returns if the disjoint union graph G is isomorph or the amount of isomorphisms based on the value
    of count_flag. Also the right color_refinement method is passed along here.
    """
    if branching_algorithm == 1:
        return count_isomorphisms(G, [], [], count_flag, color_refinement_method())