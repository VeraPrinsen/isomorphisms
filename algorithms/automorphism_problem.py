from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import degree_color_initialization
from supporting_components.basicpermutationgroup import FindNonTrivialOrbit, Stabilizer, Orbit
from supporting_components.graph import Graph, Vertex
from algorithms.color_refinement import color_refinement, get_colors
from algorithms.decide_gi import is_balanced_or_bijected
from typing import List, Dict
from math import inf
from input_output.file_output import save_graph_as_dot
from supporting_components.permv2 import permutation

"""
With these methods, the amount of graph automorphs can be counted.

"""


def amount_of_automorphisms(G):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    G_disjoint_union = G.self_disjoint_union()
    save_graph_as_dot(G_disjoint_union, 'testGG')

    permutation_vectors=generate_automorphism(G=degree_color_initialization(G_disjoint_union), D=[], I=[])
    # Convert into objects
    permutation_objects = list()

    for raw_perm_group in permutation_vectors:
        # Contains tuple (D, I) of equal length
        cycle_list = []
        for i in range(0,len(raw_perm_group[0])):
            cycle_list.append([raw_perm_group[0][i].coupling_label, (raw_perm_group[1][i].coupling_label)])

        permutation_objects.append(permutation(len(G.vertices), cycle_list))

    print(permutation_objects)

    # With these objects do order computation and return the number
    return order_computation(permutation_objects)


def order_computation(H: 'List[permutation]'):
    """
    Based on slide 21 of lecture 4 and notes.
    TODO:
    :param H: Permutation group
    :return: int with the order of the list of permutations
    """

    # Choose a in V, |H| = |Ha| * |a^H| note: (numel(a^H) > 2)
    # Built in function basicpermutationgroup
    # Choose a with non trivial orbit a: 0^H yields |0^H|
    a = FindNonTrivialOrbit(H) # ?a=0? slide 21 lec4
    # a is unit element
    # The numel(unit element) divides the group |H|
    # Group always contains G and e
    # Now find subgroups (defined as coset) of equal size
    # https://www.youtube.com/watch?v=TCcSZEL_3CQ
    # https://www.youtube.com/watch?v=AnJOjE8nVFY
    # Use left or right cosets.
    # Each subgroup should not include the unit element or any previous elements

    # Orbit contains all elements reachable by applying all elements in <H> to a
    orbit_a = Orbit(H, a)
    # ? is orbit left coset ?
    # Stabilizer contains all elements that stay the same after applying all elements in <H> to a
    stabilizer_a = Stabilizer(H, a)

    return a


def generate_automorphism(G: 'Graph', D: 'List[Vertex]', I: 'List[Vertex]', trivial_node=True):
    """
    It counts the number of isomorphisms of the graph (disjoint union of two graphs) if 'count_flag' is True.
    It checks if the graph (disjoint union of two graphs) has at least one isomorphism if 'count_flag' is False.
    :param G: The graph (disjoint union of two graphs) to check for isomorphisms
    :param D: The list of vertices in one of the graphs that is fixed
    :param I: The list of vertices in the other graph that is fixed
    :param trivial_node: This is a trivial node (default).
    :return: The number of isomorphisms if 'count_flag' is True or whether or not the graph has at least one
    isomorphism if 'count_flag' is False
    """

    # Do color refinement on the graph
    color_refinement(G)

    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the evaluated graph has no automorphism
        return []
    if is_bijected:
        return [(D, I)]
    # Conclusion: the graph is balanced, continue refining partition...

    color_mapping, max_colornum = get_colors(G)

    # Choose the color class C with at least 4 vertices of that color in the graph
    # Choose color class with smallest amount of vertices
    color_map_length_max = inf
    for color_key in color_mapping:
        if 4 <= len(color_mapping[color_key]) < color_map_length_max:
            for v in color_mapping[color_key]:
                if v.graph_label == 1:
                    v_Dx_g1 = v
                    color_map_length_max = len(color_mapping[color_key])
                    original_color_vertex_x0 = color_key

    # Change the color of this vertex to a new color and append it to the list of fixed vertices for the first graph
    v_Dx_g1.colornum = max_colornum + 1

    # And branch in separate I = Ix
    # First the comparison D + x and I + x
    # Thereafter D + xn and I + yn
    Ix = list()
    Iy = list()

    for v in color_mapping[original_color_vertex_x0]:
        # Separate D + x, I + x if possible using the coupling_label property of v.
        if v.graph_label == 2 and v.coupling_label == v_Dx_g1.coupling_label:
            Ix.append(v)
        else:  # Create the D + x, I + y combinations
            Iy.append(v)

    # Look for permutations
    permutation_vectors_DI_tuples = list()

    if trivial_node:
        # Look for D + X, I + X
        if len(Ix) == 0:
            print('Error no DxDx... This is not a trivial node')
            return []
        # Grab the reference to the vertex with graph_label = 2 in G
        v_Dx_g2 = Ix[0]

        D_copy = D.copy()
        I_copy = I.copy()
        D_copy.append(v_Dx_g1)
        I_copy.append(v_Dx_g2)

        # Now color the vertex in the second graph (I + X)
        # Note: work in G because the vector references are pointing to G
        original_X_color_in_G = v_Dx_g2.colornum
        v_Dx_g2.colornum = v_Dx_g1.colornum

        # Copy the colored graph
        G_DxDx = G.copy()

        # Revert changes in G
        v_Dx_g2.colornum = original_X_color_in_G

        # Following the algorithmic description, the next node should be either bijected or a trivial node
        permutation_vectors_DI_tuples = generate_automorphism(G=G_DxDx, D=D_copy, I=I_copy)

    if not trivial_node:
        # Assemble with Ix as the first vector to evaluate
        Iy = Ix+Iy

    for v_Iy in Iy:
        D_copy = D.copy()
        I_copy = I.copy()
        D_copy.append(v_Dx_g1)
        I_copy.append(v_Iy)

        # Now color the vertex in the second graph (I + Y)
        # Note: work in G because the vector references are pointing to G
        original_Y_color_in_G = v_Iy.colornum
        v_Iy.colornum = v_Dx_g1.colornum

        # Copy the colored graph
        G_DxDy = G.copy()

        # Revert changes in G
        v_Iy.colornum = original_Y_color_in_G

        perm_right = generate_automorphism(G=G_DxDy, D=D_copy, I=I_copy, trivial_node=False)

        # Empty response is a dead end in the evaluation tree, pick next by continue
        if not perm_right:
            continue
        else:
            # A bijection, stop loop by break
            permutation_vectors_DI_tuples += perm_right
            break

    return permutation_vectors_DI_tuples
