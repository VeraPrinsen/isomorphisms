from tests.integration_test.settings import simple_cases, twin_removal, tree_algorithm, color_refinement_algorithm, branching_algorithm, complement
from supporting_components.graph import Graph
from algorithms.preprocessing import remove_twins, use_complement
from algorithms.simple_cases import could_be_isomorphic
from algorithms.tree_algorithm import is_tree, trees_are_isomorph, trees_automorphisms
from algorithms.color_refinement import color_refinement, fast_color_refinement
from algorithms.branching import count_isomorphisms
from algorithms.automorphism_problem import count_automorphisms


"""
METHODS THAT PROVIDE ALL OPTIONS OF ALGORITHMS
"""
def apply_could_be_isomorphic(G: "Graph", H: "Graph"):
    """
    If preprocessing_simple_cases is set to True, apply the simple cases algorithm to determine is graphs are
    isomorphic using simple properties of the graphs.
    """
    if simple_cases:
        if not could_be_isomorphic(G, H):
            return False
    return True


def apply_remove_twins(G: "Graph"):
    """
    If twin_removal is set to True, twin vertices are removed from the graph. The amount of automorphisms found with
    the reduced graph should be multiplied with the factor that is returned by this method.
    """
    if twin_removal:
        factor = remove_twins(G)
    else:
        factor = 1

    return factor


def apply_tree_algorithm(G: "Graph", H: "Graph" = None):
    """
    If the tree algorithm must be used, this method checks if G (and H) are trees.
    If they are the isomorphism problem is resolved using the tree isomorphism method.
    :return: Boolean that tells if the GI problem is solved
    :return: If True, the second return variable is a Boolean that tells if G and H are isomorphic, if H is a Graph
                   or the second return variable is the amount of automorphisms of tree G
    """
    if tree_algorithm:
        if H is None and is_tree(G):
            # Count automorphism problem
            return True, trees_automorphisms(G)
        elif is_tree(G) and is_tree(H):
            # Check if G and H are isomorph
            return True, trees_are_isomorph(G, H)

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
    # If it must be determined if the graphs in G are isomorphic
    if not count_flag:
        return count_isomorphisms(G, count_flag, color_refinement_method())

    # If the amount of isomorphisms / automorphisms should be determined
    if branching_algorithm == 1:
        return count_isomorphisms(G, count_flag, color_refinement_method())
    if branching_algorithm == 2:
        return count_automorphisms(G, color_refinement_method())


def apply_complement(G: "Graph"):
    """
    If complement is set to True in the settings of the integration test, a check is done if it is beneficial if the
    complement of the graph is used in further processing.
    If the complement should be used, the complement is returned, otherwise the original graph is returned.
    :param G: The graph to check for if using the complement will result in faster result
    :return: The (complement of the) graph
    """
    if complement:
        if use_complement(G):
            return True, G.complement()
    return False, G
