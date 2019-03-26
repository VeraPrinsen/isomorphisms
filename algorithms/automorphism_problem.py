from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import degree_color_initialization
from supporting_components.graph import Graph, Vertex
from algorithms.color_refinement import color_refinement, get_colors
from algorithms.decide_gi import is_balanced_or_bijected
from typing import List, Dict
from math import inf
from input_output.file_output import save_graph_as_dot

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

    permutations=generate_automorphism(G=degree_color_initialization(G_disjoint_union), D=[], I=[], trivial_node=True)
    for perm in permutations:
        mat = []
        print('D:')
        for p in perm[0]:
            print(p.coupling_label, end = ',')
        print('')
        for p in perm[1]:
            print(p.coupling_label, end = ',')
        print('')

    print('')
    return 0

def generate_automorphism(G: 'Graph', D: 'List[Vertex]', I: 'List[Vertex]', trivial_node: 'Bool'):
    """
    It counts the number of isomorphisms of the graph (disjoint union of two graphs) if 'count_flag' is True.
    It checks if the graph (disjoint union of two graphs) has at least one isomorphism if 'count_flag' is False.
    :param G: The graph (disjoint union of two graphs) to check for isomorphisms
    :param D: The list of vertices in one of the graphs that is fixed
    :param I: The list of vertices in the other graph that is fixed
    :param full_search: find_all, choice of finding all or any bijection(s).
    :return: The number of isomorphisms if 'count_flag' is True or whether or not the graph has at least one
    isomorphism if 'count_flag' is False
    """


    # Do color refinement on the graph
    color_refinement(G)

    is_balanced, is_bijected = is_balanced_or_bijected(G)
    if not is_balanced:
        # If the graph is unbalanced, the graph has no isomorphism
        return []
    if is_bijected:
        # If the graph is balanced and bijected, the graph has exactly one isomorphism
        #
        # TODO: Figure out if f is not in the set of <X>
        # This is the case when (D+x,D+x) is evaluated (slide 17)
        # Remark to self: can start with the left leg calculation (D+x, D+x). or y=x (slide p 18)
        # Objective: find all in x, find one in y.
        # Do some clever calculations to generate the number of automorphisms.
        #
        # If the evaluation is in the right leg (D + x, D + y),
        # then it is OK to jump back directly to the first trivial node
        # A trivial node is the node where the left and right leg need to be compared.
        #
        # Create some sort of algorithm to create different branching behavior for x and y
        #
        #        O   (find all in x, find one in y)
        #      /  \
        # x   .     .  y
        #    / \   / \
        #   .   .  .  .
        #  xx  xy yx  yy
        return [(D,I,'bijected')]
        #return [(D,I)]

    colors, max_colornum = get_colors(G)

    # Choose the color class C with at least 4 vertices of that color in the graph
    # Choose color class with smallest amount of vertices
    C_len = inf
    for key in colors:
        if 4 <= len(colors[key]) < C_len:
            # Check firstly if Dx,Dx exists
            color_c = key

            # Choose the first occurring vertex with color C in the list of vertices of the first graph
            for v in colors[color_c]:
                if v.graph_label == 1:
                    x = v
                    C_len = len(colors[key])

    # Change the color of this vertex to a new color and append it to the list of fixed vertices for the first graph
    x.colornum = max_colornum + 1
    D_copy = D.copy()
    D_copy.append(x)

    # And branch in separate I = Ix
    Ix = []
    Iy = []

    # Must visit Dx,Dx earlier then Dx,Dy
    # Store list Ix and list Iy
    for v in colors[color_c]:
        # Look for Dx, Dx
        if v.graph_label == 2 and x.coupling_label == v.coupling_label:
            Ix.append(v)
        else:
            # Create the Dx, Dy combinations
            Iy.append(v)

    # Look for permutations
    permutations = []

    if trivial_node:
        # Always do DXDX
        # Call the left leg and wait for return (form: list with length 1 or more)
        # No need to loop al the X (last lecture 3)
        # Color the vertex
        # By reference changes so copy the current value
        if len(Ix) == 0:
            print('Error no DxDx... This is not a trivial node')
            return 0

        I_copy = I.copy()
        Ix_colornum_copy = Ix[0].colornum
        Ix[0].colornum = x.colornum
        I_copy.append(Ix[0]) # to store the actual vertex object, not reference as with append (?)
        G_DxDx = G.copy()
        # Restore the coloring in G
        Ix[0].colornum = Ix_colornum_copy
        # Changed by reference in G
        # Calculate the left leg
        # Below it will also be a trivial node
        permutations = generate_automorphism(G=G_DxDx, D=D_copy, I=I_copy, trivial_node=True)

    # allow to check again
    # But DxDx is first (lecture)
    if not trivial_node:
        Iy = Ix+Iy

    # Get the right leg to provide all results
    for vDy in Iy:
        I_copy = I.copy()
        I_copy.append(vDy)
        # Change color by reference in G
        vDy_colornum_copy = vDy.colornum
        vDy.colornum = x.colornum
        # Copy graph
        G_DxDy = G.copy()
        # Revert colorchange in G after copy
        vDy.colornum = vDy_colornum_copy

        perm_right = generate_automorphism(G=G_DxDy, D=D_copy, I=I_copy, trivial_node=False)
        if perm_right == []:
            continue
        else:
            # Got it!
            permutations += perm_right
            break

    return permutations

    # if not find_all: #syn: if not findall
    #     # Get the right leg
    #     for vDy in Iy:
    #         # Change color by reference in G
    #         vDy_colornum_copy = vDy.colornum
    #         vDy.colornum = x.colornum
    #         # Copy graph
    #         G_DxDy = G.copy()
    #         # Revert colorchange in G after copy
    #         vDy.colornum = vDy_colornum_copy
    #
    #         perm_right = generate_automorphism(G=G_DxDy, D=D.copy(), I=[vDy], find_all=False)
    #         if perm_right == [0]:
    #         if perm_right == [0]:
    #             continue
    #
    #         if perm_right == [1]:
    #             # Got it!
    #             permutations.append(perm_right)
    #             break

    # Return trivial node conclusion






    #
    # TODO: check if y = x in (D+x, D+y)
    # Flag for this if this is the case
    # Try:
    # with x == y (do this using x.label = (y.label + int(len(G.vertices)/2)) ?
    #    <<Count isomorphisms call self recursion>> if possible otherwise raise
    # except:
    #   Return 0
    #
    # Remember the empty left leg, p. 16 slides
    # Try:
    #       for all other x=!y:
    #       right leg, instruct: any hit is OK
    #       Recursively call with flag count = false like..
    # Catch: foundIT!
    #   Return Do some calculations to generate number of automorphisms...
    #           With X and Y puzzle together the number using some algebra

    # Create branches for all the possible fixed pairs of vertices for the chosen color


def __branching(G: 'Graph', colors: 'Dict[Int, List[Vertex]]', C: 'Int', D: 'List[Vertex]', I: 'List[Vertex]', count_flag: 'Bool'):
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
    for v in colors[C]:
        if v.graph_label == 2:
            g1.append(v)

    # For each of the vertices in the list of vertices with color C, fix the vertex and change its color to the new
    # color and determine the amount of isomorphisms for the resulting graph
    num_isomorphisms = 0
    for y0 in g1:
        G_copy = G.copy()
        D_copy = D.copy()
        I_copy = I.copy()
        colors_copy, max_colornum = get_colors(G_copy)
        for y in colors_copy[C]:
            if y.graph_label == 2 and y.label == y0.label:
                y.colornum = max_colornum
                I_copy.append(y)
                num_isomorphisms += count_isomorphisms(G_copy, D_copy, I_copy, count_flag)
                if not count_flag and num_isomorphisms > 0:
                    return True
                break
    return num_isomorphisms
