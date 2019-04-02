from supporting_components.graph import Graph, Vertex
from algorithms.decide_gi import is_balanced_or_bijected
from typing import List, Dict, Callable
from math import inf


def count_isomorphisms(G: 'Graph', D: 'List[Vertex]', I: 'List[Vertex]', count_flag: 'Bool', color_refinement_method: Callable[[Graph], None]):
    """
    It counts the number of isomorphisms of the graph (disjoint union of two graphs) if 'count_flag' is True.
    It checks if the graph (disjoint union of two graphs) has at least one isomorphism if 'count_flag' is False.
    :param G: The graph (disjoint union of two graphs) to check for isomorphisms
    :param D: The list of vertices in one of the graphs that is fixed
    :param I: The list of vertices in the other graph that is fixed
    :param count_flag: Whether or not the amount of isomorphisms should be returned or whether or not the graph has an
    isomorphism
    :return: The number of isomorphisms if 'count_flag' is True or whether or not the graph has at least one
    isomorphism if 'count_flag' is False
    """
    # Do color refinement on the graph
    color_refinement_method(G)

    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the graph has no isomorphism
        if not count_flag:
            return False
        return 0
    if is_bijected:
        # If the graph is balanced and bijected, the graph has exactly one isomorphism
        if not count_flag:
            return True
        return 1

    # Get the colors and its vertices of the current graph
    colors = G.colors

    # Choose the color class C with at least 4 vertices of that color in the graph
    # Choose color class with smallest amount of vertices
    C_len = inf
    for key in colors:
        if len(colors[key]) >= 4 and len(colors[key]) < C_len:
            C = key
            C_len = len(colors[key])

    # Choose the first occurring vertex with color C in the list of vertices of the first graph
    for v in colors[C]:
        if v.graph_label == 1:
            x = v
            break

    # Change the color of this vertex to a new color and append it to the list of fixed vertices for the first graph
    x.colornum = G.max_colornum + 1
    # Update colors of graph
    colors[C].remove(x)
    colors.setdefault(G.max_colornum + 1, list()).append(x)
    D.append(x)
    # Create branches for all the possible fixed pairs of vertices for the chosen color
    return __branching(G, C, D.copy(), I.copy(), count_flag, color_refinement_method)


def __branching(G: 'Graph', C: 'Int', D: 'List[Vertex]', I: 'List[Vertex]', count_flag: 'Bool', color_refinement_method: Callable[[Graph], None]):
    """
    Creates branches of the graph (disjoint union of two graphs) and count the amount of isomorphisms for those graphs.
    In one graph, one vertex of the color group is fixed. For each of the vertices in the other graph, a branch is
    created fixing that vertex.
    :param G: The graph (disjoint union of two graphs) to branch
    :param colors: The colors present in the graph (disjoint union of two graphs) and its corresponding list of vertices
    :param C: The chosen color group to create branches for
    :param D: The list of vertices in one of the graphs that is fixed
    :param I: The list of vertices in the other graph that is fixed
    :param count_flag: Whether or not the amount of isomorphisms should be returned or whether or not the graph has an
    isomorphism
    :return: The number of isomorphisms if 'count_flag' is True or whether or not the graph has at least one
    isomorphism if 'count_flag' is False
    """
    # Create the list of vertices in the other graph with color C
    g1 = []
    for v in G.colors[C]:
        if v.graph_label == 2:
            g1.append(v)

    # For each of the vertices in the list of vertices with color C, fix the vertex and change its color to the new
    # color and determine the amount of isomorphisms for the resulting graph
    num_isomorphisms = 0
    for y in g1:
        # Make a copy of everything before creating a new branch
        G_backup, max_colornum_backup, colors_backup = G.backup()
        G.max_colornum += 1
        D_copy = D.copy()
        I_copy = I.copy()
        y.colornum = G.max_colornum
        # Update colors of graph
        G.colors[C].remove(y)
        G.colors.setdefault(G.max_colornum, list()).append(y)
        I_copy.append(y)
        num_isomorphisms += count_isomorphisms(G, D_copy, I_copy, count_flag, color_refinement_method)
        if not count_flag and num_isomorphisms > 0:
            return True
        G.revert(G_backup, max_colornum_backup, colors_backup)
    if not count_flag:
        return num_isomorphisms > 0
    else:
        return num_isomorphisms
