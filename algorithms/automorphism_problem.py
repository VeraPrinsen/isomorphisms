from supporting_components.basicpermutationgroup import FindNonTrivialOrbit, Stabilizer, Orbit
from supporting_components.permv2 import permutation
from supporting_components.graph import Graph, Vertex
from algorithms.decide_gi import is_balanced_or_bijected
from typing import List, Callable
from math import inf


def count_automorphisms(G: "Graph", color_refinement_method: Callable[[Graph], None]):
    """
    This method counts the amount of automorphisms of a Graph using the branching technique that uses the
    permutations to calculate the amount of automorphisms.
    :param G: The graph (disjoint union of two of the same graphs) of which the amount of automorphisms need
    to be counted.
    :param color_refinement_method: The color refinement method that is used in the branching
    :return: The amount of automorphisms of graph G
    """
    # The branching method returns a list of different mappings of the graph
    permutation_mappings = branching(G, color_refinement_method, trivial_node=True)
    # These mappings are converted to permutation objects
    permutations = mappings_to_permutations(int(len(G.vertices) / 2), permutation_mappings)
    # The order computation calculates the amount of automorphisms there are in total, given these permutations
    return order_computation(permutations)


def branching(G: 'Graph', color_refinement_method: Callable[[Graph], None], trivial_node=False):
    """
    It returns all possible mappings within graph G (which is a disjoint union of two of the same graphs).
    :param G: The graph (disjoint union of two of the same graphs)
    :param color_refinement_method: The color refinement method to use within branching.
    :param trivial_node: If set to True, the current node of the branch is a trivial node, meaning that the mappings
    that have been done are mappings from vertices to itself. This flag makes sure that branching takes place
    at least two times when a node is a trivial node.
    :return: A list of valid mappings within G.
    """
    # Do color refinement on the graph
    color_refinement_method(G)

    # Check if the current coloring of the graph is balanced or bijected
    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the current mapping is not going to result in an bijection. Return to the
        # previous node in the branching to continue with another mapping by returning an empty mapping.
        return []
    if is_bijected:
        # If the graph is balanced and bijected, this is a particular mapping of the graph to itself. Return the
        # current mapping.
        mapping = mapping_of_bijection(G)
        return [mapping]

    # If the current coloring is balanced, but not bijected, there is still some refining to do.
    # Choose the color class C with at least 4 vertices of that color in the graph (which means each graph of the
    # disjoint union has at least 2 of that color) and choose the color class with smallest amount of vertices
    C_len = inf
    for key in G.colors:
        if len(G.colors[key]) >= 4 and len(G.colors[key]) < C_len:
            C = key
            C_len = len(G.colors[key])

    # Make a list of all vertices of graph 1 and 2 in this color class C
    v_graph1_colorC = []
    v_graph2_colorC = []
    for v in G.colors[C]:
        if v.graph_label == 1:
            v_graph1_colorC.append(v)
        if v.graph_label == 2:
            v_graph2_colorC.append(v)

    # First try to find a pair of vertices with the same label, which means there are the same vertex
    # in the graph
    v1_mapped = None
    for v1 in v_graph1_colorC:
        for v2 in v_graph2_colorC:
            if v1.coupling_label == v2.coupling_label:
                # If such a pair is found the vertex to be colored in the first graph is set to d_mapping and the
                # corresponding vertex of graph 2 is put in front of the list of vertices of graph 2 with color C
                v1_mapped = v1
                v_graph2_colorC.remove(v2)
                v_graph2_colorC = [v2] + v_graph2_colorC
                # The loops can be stopped when a pair is found
                break
        if v1_mapped is not None:
            break

    # If no pair of vertices is found with the same label, a None value is put in front of the list of vertices
    # of graph 2 with color C. This is done to let the next for-loop know that there is no pair of vertices in
    # color class C. From graph 1 now any random vertex can be chosen, so the first vertex of the list of vertices
    # of graph 1 and color class C is chosen.
    if v1_mapped is None:
        v_graph2_colorC = [None] + v_graph2_colorC
        v1_mapped = v_graph1_colorC[0]

    # Create an empty list to store the mappings in that are returned from lower nodes in the branching.
    current_node_mappings = []

    # Like in the normal branching, the vertex d_mapping of graph 1 with color class C is now mapped to all vertices
    # in the list of vertices of graph 2 with color class C
    for i in range(len(v_graph2_colorC)):
        v2 = v_graph2_colorC[i]

        # If the vertex is None, this means that there was not a pair of vertices found with the same label and so
        # this loop can be skipped
        if v2 is None:
            continue

        # With the current mapping (d_mapping from graph 1 to v2 of graph 2) the permutations following that mapping
        # are retrieved using the following method. To remember if the next branching node is still trivial, the
        # current node must be trivial and the mapping must be from a pair of vertices with the same label. This is
        # only true if i is zero, because if there is a pair, the vertex of graph 2 is in front of the loop.
        still_trivial = trivial_node and i == 0
        next_node_mappings = permutations_of_mapping(G, C, v1_mapped, v2, color_refinement_method, still_trivial)

        # If there is at least one valid mapping returned from the node, the mappings are added to the mapping of the
        # current node. The next_node_mappings could be an empty list when a branch of the branching tree did not result
        # in any mappings or if the next node is a leaf and the coloring was not balanced.
        if len(next_node_mappings) != 0:
            current_node_mappings += next_node_mappings
            # If the current node is not a trivial node, the mappings can be returned and further branching can be
            # skipped
            if not trivial_node:
                return current_node_mappings

    # At the end you will be back in the root (which is a trivial node) and the result can be returned
    return current_node_mappings


def permutations_of_mapping(G: "Graph", C: int, v1: "Vertex", v2: "Vertex", color_refinement_method: Callable[[Graph], None], trivial_node):
    """
    In this method, a certain mapping from a vertex in graph 1 (v1) to a vertex in graph 2 (v2) is taking place
    After that, further branching takes place. In this method, a backup of the coloring before the mapping is
    remembered for further branching.
    :param G: The graph vertices are being mapped within
    :param C: The current colorclass that is being refined
    :param v1, v2: The vertex of graph 1 (v1) and graph (v2) that need to be mapped to each other
    :param color_refinement_method: The color refinement method that needs to be applied in branching
    :param trivial_node: If the node after this mapping is still a trivial node (meaning only vertices with the same
        label are mapped to each other)
    :return: The bijected mappings that follow if this particular mapping from v1 to v2 has been done
    """
    # Make a backup of the current state of the graph coloring
    max_colornum_backup, colors_backup = G.backup()

    # Color the vertex in the first graph
    G.max_colornum += 1
    v1.colornum = G.max_colornum
    G.colors[C].remove(v1)
    G.colors.setdefault(G.max_colornum, []).append(v1)

    # Color the vertex in the second graph
    v2.colornum = G.max_colornum
    G.colors[C].remove(v2)
    G.colors[G.max_colornum].append(v2)

    # Apply further branching using this new mapping and retrieve the possible mappings from this new coloring
    node_mappings = branching(G, color_refinement_method, trivial_node)

    # Apply backup coloring to graph G such that the mapping done in this method is undone.
    G.revert(max_colornum_backup, colors_backup)

    return node_mappings


def mapping_of_bijection(G: "Graph"):
    """
    If a bijection is found. Make a mapping from each vertex in graph 1 to the vertex in graph 2
    :param G: Graph with a discrete coloring
    :return: Mapping of the coloring in G
    """
    # Create an empty mapping with -1 as a stubbed temporary value
    mapping = [-1 for _ in range(int(len(G.vertices)/2))]
    # For each color in G, there should be only 2 vertices in the colors dictionary. One for graph 1 and one for
    # graph 2. On the location of the label of the vertex of graph 1 put the label of the corresponding label of the
    # vertex of graph 2
    for color in G.colors:
        vi = G.colors[color][0]
        vj = G.colors[color][1]
        if vi.graph_label == 1:
            mapping[vi.coupling_label] = vj.coupling_label
        else:
            mapping[vj.coupling_label] = vi.coupling_label

    return mapping


def mappings_to_permutations(n, mappings):
    """
    This method turns a list of mappings into a list of permutation objects.
    :param n: Amount of elements in the set that the permutations act on
    :param mappings: A list of different possible mappings on the elements in the set
    :return: List of permutations
    """
    permutation_objects = []
    for mapping in mappings:
        perm_object = permutation(n, mapping=mapping)
        permutation_objects.append(perm_object)

    return permutation_objects


def order_computation(H: 'List[permutation]'):
    """
    Recursively computes the order of a list of permutations.
    Based on slide 21 of lecture 4 and notes.
    :param H: Permutation group
    :return: int with the order of the list of permutations
    """
    # If H has only one element and it is the unity permutation. The length of the orbit is 1.
    # Because whatever 'a' you choose, it can only map to itself.
    if len(H) == 1 and H[0].istrivial():
        return 1

    # And because the method Stabilizer does not return the unity permutation as part of the stabilizer,
    # if further down in the recursion the length of H is zero, this actually means that only the unity
    # permutation is left, because that one must always be in the stabilizer. So in this case, the length
    # of the orbit is also 1.
    if len(H) == 0:
        return 1

    # In any other case, the theorem holds that the order of H is the order of the stabilizer multiplied by the
    # length of the orbit ( |H| = |H0| * |0_H| ). For this theorem the theory of slide 21 of the lecture slides
    # of lecture L4 are used.

    # Choose a with nontrivial orbit
    a = FindNonTrivialOrbit(H)
    # Determine orbit of a (list of vertices to which 'a' can be mapped)
    O_H = Orbit(H, a)
    # Determine stabilizer of a (list of permutations that leave 'a' untouched)
    H_0 = Stabilizer(H, a)

    return order_computation(H_0) * len(O_H)