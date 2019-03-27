from supporting_components.graph import Graph, Vertex
from math import factorial


def is_tree(G: "Graph"):
    return len(G.edges) == len(G.vertices) - 1


def trees_amount_of_isomorphisms(T1: "Graph", T2: "Graph"):
    """
    :param T1, T2: Graphs that are trees (so is_tree(T1) and is_tree(T2) return True)
    :return:
    """
    root_T1 = root_label(T1)
    root_T2 = root_label(T2)

    # Tree can have one or two roots, if amount of roots is not equal, not isomorphic
    if len(root_T1) != len(root_T2):
        return False, 0

    # Assign level numbers to all nodes
    # todo: adept to when there are 2 roots.
    assign_level(root_T1[0], 0, [])
    assign_level(root_T2[0], 0, [])

    # Assign all vertices to level number lists
    L1 = {}
    for v in T1:
        L1.setdefault(v.level, []).append(v)
    L2 = {}
    for v in T2:
        L2.setdefault(v.level, []).append(v)

    # The number of levels of each tree should be equal
    h1, h2 = max(L1.keys()), max(L2.keys())
    if max(L1.keys()) != max(L2.keys()):
        return False, 0
    h = h1

    for i in range(h, -1, -1):
        H1 = []
        for v in L1[i]:
            if v.degree == 1:
                v.name = 'lr'
                v.auto = 1
            else:
                # For each vertex, get the set of string assigned to its children
                children_names = []
                children_count = {}
                children_auto = {}
                for n in v.neighbours:
                    if n.level > v.level:
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

        H2 = []
        for v in L2[i]:
            if v.degree == 1:
                v.name = 'lr'
                v.auto = 1
            else:
                # For each vertex, get the set of string assigned to its children
                children_names = []
                children_count = {}
                children_auto = {}
                for n in v.neighbours:
                    if n.level > v.level:
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

        H1.sort()
        H2.sort()
        if H1 != H2:
            return False, 0

    return True, L1[0][0].auto


def trees_are_isomorph(T1: "Graph", T2: "Graph"):
    """
    :param T1, T2: Graphs that are trees (so is_tree(T1) and is_tree(T2) return True)
    :return:
    """
    root_T1 = root_label(T1)
    root_T2 = root_label(T2)

    # Tree can have one or two roots, if amount of roots is not equal, not isomorphic
    if len(root_T1) != len(root_T2):
        return False

    # Assign level numbers to all nodes
    assign_level(root_T1[0], 0, [])
    assign_level(root_T2[0], 0, [])

    # Assign all vertices to level number lists
    L1 = {}
    for v in T1:
        L1.setdefault(v.level, []).append(v)
    L2 = {}
    for v in T2:
        L2.setdefault(v.level, []).append(v)

    # The number of levels of each tree should be equal
    h1, h2 = max(L1.keys()), max(L2.keys())
    if max(L1.keys()) != max(L2.keys()):
        return False
    h = h1

    # Tree is processed level by leven, from bottom to root
    # Vertices in the same layer whose subtrees are isomorphic, get the same string
    for i in range(0, h+1):
        H1 = []
        for v in L1[i]:
            if v.degree == 1:
                # v.string = 0
                H1.append(1)
            else:
                # For each vertex, get the set of string assigned to its children
                str = 0
                for n in v.neighbours:
                    if n.level > v.level:
                        str += 1
                # v.string = str
                H1.append(str)

        H2 = []
        for v in L2[i]:
            if v.degree == 1:
                # v.string = 0
                H2.append(1)
            else:
                # For each vertex, get the set of string assigned to its children
                str = 0
                for n in v.neighbours:
                    if n.level > v.level:
                        str += 1
                # v.string = str
                H2.append(str)

        H1.sort()
        H2.sort()
        if H1 != H2:
            return False

    return True

def root_label(T: "Graph"):
    """
    Root of tree T
    :param T:
    :return:
    """
    T_copy = T.copy()

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

    T_root = []
    for v in T.vertices:
        if v.label in root_labels:
            T_root.append(v)

    return T_root


def assign_level(vertex: "Vertex", level, already_assigned: "List[Vertex]"):
    vertex.level = level
    already_assigned.append(vertex)
    if vertex.degree == 1:
        vertex.tree_label = 0
    else:
        for neighbour in vertex.neighbours:
            if neighbour not in already_assigned:
                assign_level(neighbour, level+1, already_assigned)
