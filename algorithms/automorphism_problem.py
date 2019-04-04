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
    print('&&&&&&&&&&&&&')
    # Convert into objects
    permutation_objects = list()
    print(permutation_vectors)
    print('lenG={}'.format(len(G.vertices)))

    # TODO: investigate why the last permutation (from trivial node = 0) fails
    for groupid in range(0, len(permutation_vectors)):
        raw_perm_group = permutation_vectors[groupid]
        # Contains tuple (D, I) of equal length
        cycle_list = []
        for i in range(0,len(raw_perm_group[0])):
            dX = raw_perm_group[0][i]
            dY = raw_perm_group[1][i]
            cycle_list.append([dX, dY])

        permutation_objects.append(permutation(len(G.vertices), cycle_list))
        print(groupid)

        # TODO: This fails for trees

    print(permutation_objects)
    return order_computation(permutation_objects)


def tester():
    permutation_vectors = [([23, 11, 6], [23, 11, 6]),
                           ([23, 11, 6], [23, 11, 0]),
                           ([23, 11, 0], [23, 3, 8]),
                           ([23, 3, 6], [0, 12, 9])]
    permutation_objects = list()
    # print(permutation_vectors)

    # TODO: investigate why the last permutation (from trivial node = 0) fails
    for groupid in range(0, len(permutation_vectors)):
        raw_perm_group = permutation_vectors[groupid]
        # Contains tuple (D, I) of equal length
        cycle_list = []
        for i in range(0, len(raw_perm_group[0])):
            dX = raw_perm_group[0][i]
            dY = raw_perm_group[1][i]
            cycle_list.append([dX, dY])

        permutation_objects.append(permutation(24, cycle_list))
        print(groupid)

        # TODO: This fails for trees

    print(permutation_objects)
    a = order_computation(permutation_objects)
    print(a)
    assert (a==96)


def order_computation(H_0: 'List[permutation]'):
    """
    Based on slide 21 of lecture 4 and notes.
    TODO:
    :param H: Permutation group
    :return: int with the order of the list of permutations
    """
    a = FindNonTrivialOrbit(H_0)
    orb_a, transvO = Orbit(H_0, a, returntransversal=True)
    stab_a = Stabilizer(H_0, a)

    if len(H_0) == 1:
        return len(orb_a) * 1  # As theorem (=1)

    return len(orb_a) * order_computation(stab_a)


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
    color_refinement(G)

    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the evaluated graph has no automorphism
        return [(['unbalanced']),(['unbalanced'])]
    if is_bijected:
        print([D,I])
        return [(D, I)]

    # The graph is balanced, continue refining partition...

    color_mapping, max_colornum = get_colors(G)

    # Choose the color class C with at least 4 vertices of that color in the graph
    # Choose color class with smallest amount of vertices
    color_map_length_max = inf
    for color_key in color_mapping:
        if 4 <= len(color_mapping[color_key]) < color_map_length_max:
            for _ in color_mapping[color_key]:
                    color_map_length_max = len(color_mapping[color_key])
                    original_color_vertex_x0 = color_key

    # And branch in separate I = Ix
    # First the comparison D + x and I + x
    # Thereafter D + xn and I + yn
    Ix = list()  # vector of graph 2 == X of graph 1
    Iy = list()  # vectors of Iy in graph 2
    # Change the color of this vertex to a new color and append it to the list of fixed vertices for the first graph

    for v in color_mapping[original_color_vertex_x0]:
        if v.graph_label == 1:
            Ix.append(v)
            #print('v in 1={}'.format(v.coupling_label))
        if v.graph_label == 2:
            Iy.append(v)
            #print('v in 2={}'.format(v.coupling_label))

    # Look for permutations
    permutation_vectors_DI_tuples = list()

    # Color

    if trivial_node:
        # Look for D + X, I + X
        # Grab the reference to the vertex with graph_label = 2 in G

        for vy in Iy:
            for vx in Ix:
                if vx.coupling_label == vy.coupling_label:
                    v_Dx_g1 = vx
                    v_Dx_g2 = vy
                    break

        D_copy = list(D)
        I_copy = list(I)
        D_copy.append(v_Dx_g1.coupling_label)
        I_copy.append(v_Dx_g2.coupling_label)

        # Now color the vertex in the second graph (I + X)
        # Note: work in G because the vector references are pointing to G
        # color
        v_Dx_g1.colornum = max_colornum + 1

        original_g2_color_in_G = v_Dx_g2.colornum
        v_Dx_g2.colornum = v_Dx_g1.colornum

        # Copy the colored graph
        G_DxDx = G.copy()

        # Revert changes in G
        v_Dx_g2.colornum = original_g2_color_in_G

        # Following the algorithmic description, the next node should be either bijected or a trivial node
        permutation_vectors_DI_tuples = generate_automorphism(G=G_DxDx, D=D_copy, I=I_copy)

        #print(permutation_vectors_DI_tuples)
        Ix.remove(v_Dx_g1)
        #Iy.remove(v_Dx_g2)
        Ix = [v_Dx_g1] + Ix

    for v_Ix in Ix:
        D_copy = list(D)
        D_copy.append(v_Ix.coupling_label)
        original_X_color_in_G = v_Ix.colornum
        v_Ix.colornum = max_colornum + 1

        for v_Iy in Iy:
            I_copy = list(I)
            I_copy.append(v_Iy.coupling_label)

            # Permutation
            cycles = []
            for d, i in zip(D_copy, I_copy):
                cycles.append([d, i])
            try:
                permutation(len(G.vertices), cycles)
            except AssertionError:
                continue


            # Now color the vertex in the second graph (I + Y)
            # Note: work in G because the vector references are pointing to G
            original_Y_color_in_G = v_Iy.colornum
            v_Iy.colornum = v_Ix.colornum

            # Copy the colored graph
            G_DxDy = G.copy()

            # Revert changes in G
            v_Iy.colornum = original_Y_color_in_G

            perm_right = generate_automorphism(G=G_DxDy, D=D_copy, I=I_copy, trivial_node=False)
            #print(perm_right)
            # Empty response is a dead end in the evaluation tree, pick next by continue
            if perm_right == [(['unbalanced']),(['unbalanced'])]:
                continue
            else:
                # A bijection, stop loop by break
                permutation_vectors_DI_tuples += perm_right

                #print('perm_tuples')
                #print(permutation_vectors_DI_tuples)

                return permutation_vectors_DI_tuples

        # Revert color of X
        v_Ix.colornum = original_X_color_in_G

    return [(['unbalanced']),(['unbalanced'])]