from supporting_components.graph import Graph, Vertex
from math import factorial


def is_tree(G: "Graph"):
    """
    Determines if graph G is a tree based on the Theorem that the amount of edges is one less than the amount of vertices
    :return: Boolean if graph G is a tree or not
    """
    return len(G.edges) == len(G.vertices) - 1


def trees_count_isomorphisms(T1: "Graph", T2: "Graph", count_flag: "Bool"):
    """
    :param T1, T2: Graphs that are trees (so is_tree(T1) and is_tree(T2) return True)
    :param count_flag: Flag that determines what return argument is
    :return: If count_flag is False, the return argument is a boolean indicating if T1 and T2 are isomorphic or not
    If count_flag is True, the return argument is the amount of isomorphisms between T1 and T2
    """
    # Determine the root of both trees
    root_T1 = __root_label(T1)
    root_T2 = __root_label(T2)

    # Tree can have one or two roots, if amount of roots is not equal, not isomorphic
    if len(root_T1) != len(root_T2):
        if count_flag:
            return 0
        return False

    # If there are two roots, the amount of isomorphisms is the addition of isomorphisms from the two mappings
    # of roots to each other. Because the maximum amount of roots is 2, all roots of T1 are mapped to one root of T2.
    # Root levels are overwritten in the second cycle.
    total_isomorphisms = 0
    # for i_root in range(len(root_T1)):
    for i_root in [0]:
        root1 = root_T1[i_root]
        root2 = root_T2[0]

        # Assign level numbers to all nodes
        __assign_level(root1, 0, [])
        __assign_level(root2, 0, [])

        # Assign all vertices to level number lists
        L1 = {}
        for v in T1:
            L1.setdefault(v.level, []).append(v)
        L2 = {}
        for v in T2:
            L2.setdefault(v.level, []).append(v)

        # The number of levels of each tree should be equal, otherwise not isomorphic
        h1, h2 = max(L1.keys()), max(L2.keys())
        if max(L1.keys()) != max(L2.keys()):
            continue
        h = h1

        # From the bottom level up, assign names to the vertices
        # If the vertex is a leaf, the name 'lr' is assigned
        # The name of all other vertices is a sorted collection of the names of its children
        # At the same time, remember how many automorphisms the subtree of that vertex has
        are_isomorphic = True    # For each level it is checked if the trees still can be isomoprhic, if not, the loop can be stopped
        for i in range(h, -1, -1):
            # Name the vertices of tree T1
            H1 = []
            for v in L1[i]:
                if v.degree_fixed == 1:
                    v.name = 'lr'
                    v.auto = 1
                else:
                    # For each vertex, get the set of string assigned to its children
                    children_names = []
                    children_count = {}
                    children_auto = {}
                    for n in v.neighbours:
                        if n.level > v.level:
                            for _ in range(n.n_twins):
                                children_names.append(n.name)
                            children_count[n.name] = children_count.setdefault(n.name, 0) + 1
                            children_auto[n.name] = children_auto.setdefault(n.name, 1) * n.auto
                    v_auto = 1
                    for child_name in set(children_names):
                        v_auto *= factorial(children_count[child_name]) * children_auto[child_name]
                    v.auto = v_auto

                    children_names.sort()
                    v_name = 'l'
                    for child_name in children_names:
                        v_name += child_name
                    v_name += 'r'
                    v.name = v_name
                H1.append(v.name)

            # Name the vertices of tree T2
            H2 = []
            for v in L2[i]:
                if v.degree_fixed == 1:
                    v.name = 'lr'
                    v.auto = 1
                else:
                    # For each vertex, get the set of string assigned to its children
                    children_names = []
                    children_count = {}
                    children_auto = {}
                    for n in v.neighbours:
                        if n.level > v.level:
                            for _ in range(n.n_twins):
                                children_names.append(n.name)
                            children_count[n.name] = children_count.setdefault(n.name, 0) + 1
                            children_auto[n.name] = children_auto.setdefault(n.name, 1) * n.auto
                    v_auto = 1
                    for child_name in set(children_names):
                        v_auto *= factorial(children_count[child_name]) * children_auto[child_name]
                    v.auto = v_auto

                    children_names.sort()
                    v_name = 'l'
                    for child_name in children_names:
                        v_name += child_name
                    v_name += 'r'
                    v.name = v_name
                H2.append(v.name)

            # On each level, the collections of names should be equal for the two trees for them to be isomorphic
            H1.sort()
            H2.sort()
            if H1 != H2:
                are_isomorphic = False
                break

        # Only if the previous for-loop is fully done, the trees are isomorphic
        # If count_flag is False, True is immediately returned
        # If the amount of isomorphisms are counted, all other root combination should be taken into account
        if are_isomorphic:
            if count_flag:
                total_isomorphisms += L1[0][0].auto
            else:
                return True

    # If count_flag is True, the amount of isomorphisms is returned
    # If count_flag is False, if the trees are isomorphic, the method should have already returned True,
    # so the trees are not isomorphic
    if count_flag:
        return total_isomorphisms
    return False


def __root_label(T: "Graph"):
    """
    Determines the root of tree T by removing all leaves from the tree until there are 1 or 2 vertices left.
    :return: A list of vertices of the roots of tree T
    """
    T_copy = T.copy()

    # Leaves are removed from the copy untill 1 or 2 vertices remain
    while len(T_copy.vertices) > 2:
        vertices_to_remove = []
        for v in T_copy.vertices:
            if v.degree == 1:
                vertices_to_remove.append(v)
        for v in vertices_to_remove:
            T_copy.del_vertex(v)

    root_labels = []
    for v in T_copy.vertices:
        root_labels.append(v.label)

    # From the original tree, the roots are returned
    T_root = []
    for v in T.vertices:
        if v.label in root_labels:
            T_root.append(v)

    return T_root


def __assign_level(vertex: "Vertex", level, already_assigned: "List[Vertex]"):
    """
    Assumes that levels are assigned to tree from root to the leafs
    :param vertex: Vertex that a level needs to be assigned to
    :param level: The level that needs to be assigned
    :param already_assigned: List of vertices with all vertices that already have assigned a level
    """
    vertex.level = level
    already_assigned.append(vertex)
    for neighbour in vertex.neighbours:
        if neighbour not in already_assigned:
            __assign_level(neighbour, level + 1, already_assigned)
