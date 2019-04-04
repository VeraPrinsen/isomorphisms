from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import degree_color_initialization
from input_output.sys_output import passed
from supporting_components.basicpermutationgroup import FindNonTrivialOrbit, Stabilizer, Orbit
from supporting_components.graph import Graph, Vertex
from algorithms.color_refinement import color_refinement
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
    #save_graph_as_dot(G_disjoint_union, 'testGG')

    permutation_vectors=generate_automorphism(G=degree_color_initialization(G_disjoint_union), D=[], I=[])
    print('&&&&&&permutationobjects&&&&&&&')
    # Convert into objects
    permutation_objects = list()
    print(permutation_vectors)

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


def order_computation(H: 'List[permutation]'):
    """
    Recursively computes the order of a list of permutations.
    Based on slide 21 of lecture 4 and notes.
    :param H: Permutation group
    :return: int with the order of the list of permutations
    """
    # Choose a with nontrivial orbit
    a = FindNonTrivialOrbit(H)
    # Determine orbit of a (list of vertices 'a' can be mapped to)
    O_H = Orbit(H, a)

    # If length of the list of permutation H is equal to 1 (which is the stabilizer of the previous recursive call):
    # Length of orbit = length of elements in the permutation in H
    # Stabilizer = empty set, because there is no permutation that leaves an element untouched
    # And the order is equal to the orbit that is determined using the previous stabilizer
    if len(H) == 1:
        return len(O_H)

    # Determine stabilizer of a (list of permutations that leave 'a' untouched)
    H_0 = Stabilizer(H, a)

    # Order of list of permutation H = |H|
    # Order of stabilizer (which is a list of permutations) H_0 = |H_0|
    # Length of orbit (which is a list of vertices labels) O_H = |O_H|
    # Orbit-Stabilizer-theorem:     |H| = |H_0| * |O_H|
    return order_computation(H_0) * len(O_H)


def generate_automorphism(G: 'Graph', D: 'List[Vertex]', I: 'List[Vertex]', trivial_node=True):
    """
    It counts the number of isomorphisms of the graph (disjoint union of two graphs) if 'count_flag' is True.
    It checks if the graph (disjoint union of two graphs) has at least one isomorphism if 'count_flag' is False.
    :param G: The graph (disjoint union of two graphs) to check for isomorphisms
    :param D: The list of vertex.coupling_label in one of the graph_label=1 that is fixed
    :param I: The list of vertex.coupling_label in one of the graph_label=2 that is fixed
    :param trivial_node: This is a trivial node (default).
    :return: The number of isomorphisms if 'count_flag' is True or whether or not the graph has at least one
    isomorphism if 'count_flag' is False
    """
    color_refinement(G)

    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the evaluated graph has no automorphism
        return [(['unbalanced']), (['unbalanced'])]
    if is_bijected:
        passed('bijected!')
        print([D,I])
        return [(D, I)]

    # Choose the color class C with at least 4 vertices of that color in the graph
    # Choose color class with smallest amount of vertices
    C_len = inf
    for key in G.colors:
        if len(G.colors[key]) >= 4 and len(G.colors[key]) < C_len:
            C = key
            C_len = len(G.colors[key])

    # And branch in separate I = Ix
    # First the comparison D + x and I + x
    # Thereafter D + xn and I + yn
    Ix = list()  # vector of graph 2 == X of graph 1
    Iy = list()  # vectors of Iy in graph 2
    # Change the color of this vertex to a new color and append it to the list of fixed vertices for the first graph

    for v in G.colors[C]:
        if v.graph_label == 1:
            Ix.append(v)
        if v.graph_label == 2:
            Iy.append(v)

    # Look for permutations
    DI_permutations = list()

    # Branching non-trivial (g1(X) - g2(Y))
    # optimize to reduce the search space... X - Y and Y - X not necessary due to symmetry
    # Make a copy of everything before creating a new branch
    max_colornum_backup_preX, colors_backup_preX = G.backup()

    # Branching trivial (g1(X) g2(X))

    if trivial_node:
        # Look for D + X, I + X
        D_copy = list(D)
        I_copy = list(I)

        # Grab the reference to the vertex with graph_label = 2 in G

        for vy in Iy:
            for vx in Ix:
                if vx.coupling_label == vy.coupling_label:
                    x1 = vx
                    x2 = vy
                    break

        # Update colors of graph 1
        x1.colornum = G.max_colornum + 1
        G.colors[C].remove(x1)
        G.colors.setdefault(G.max_colornum + 1, list()).append(x1)

        # Make a copy of everything before creating a new branch
        G.max_colornum += 1
        # Add to the visited nodes in g1
        D_copy.append(x1.coupling_label)

        # Update colors of graph 2
        x2.colornum = G.max_colornum
        G.colors[C].remove(x2)
        G.colors.setdefault(G.max_colornum, list()).append(x2)

        # Add to the visited nodes in g2
        I_copy.append(x2.coupling_label)

        DI_permutations = generate_automorphism(G=G, D=D_copy, I=I_copy)
        G.revert(max_colornum_backup_preX, colors_backup_preX)

        # Reduce options after first trivial node branch iteration
        Ix.remove(x1)
        Ix = [x1] + Ix
        Iy.remove(x2)

    # Branching, check all

    for x1 in Ix:
        G.revert(max_colornum_backup_preX, colors_backup_preX)

        for y2 in Iy:

            D_copy = list(D)

            # Color x1
            # Update colors of graph 1
            x1.colornum = G.max_colornum + 1

            G.colors[C].remove(x1)
            G.colors.setdefault(G.max_colornum + 1, list()).append(x1)

            # Make a copy of everything before creating a new branch
            G.max_colornum += 1
            D_copy.append(x1.coupling_label)

            I_copy = list(I)
            # Update colors of graph 2
            y2.colornum = G.max_colornum
            G.colors[C].remove(y2)
            G.colors.setdefault(G.max_colornum, list()).append(y2)

            # Add to the visited nodes in g2
            I_copy.append(y2.coupling_label)

            # Permutation "validity checker"
            # Uncomment om permutaties te checken op geldigheid volgens de library
            # cycles = []
            # for d, i in zip(D_copy, I_copy):
            #     cycles.append([d, i])
            # try:
            #     permutation(len(G.vertices), cycles)
            # except AssertionError:
            #     continue

            perm_right = generate_automorphism(G=G, D=D_copy, I=I_copy, trivial_node=False)
            # Empty response is a dead end in the evaluation tree, pick next by continue
            if perm_right == [(['unbalanced']),(['unbalanced'])]:
                continue
            else:
                # A bijection, stop loop by break
                DI_permutations += perm_right

                return DI_permutations

    return [(['unbalanced']),(['unbalanced'])]

