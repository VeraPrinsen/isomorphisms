from supporting_components.graph import Graph, Vertex
from math import factorial


def is_tree(G: "Graph"):
    """
    Determines if graph G is a tree based on the Theorem that the amount of edges is one less than the amount of vertices
    :return: Boolean if graph G is a tree or not
    """
    return len(G.edges) == len(G.vertices) - 1


def trees_are_isomorph(T1: "Graph", T2: "Graph"):
    """
    :param T1, T2: Graphs that are trees (so is_tree(T1) and is_tree(T2) return True)
    :return: Boolean if T1 and T2 are isomorph. If they are, T1 and T2 have a property 'automorphisms' with
    the amount of automorphisms they both have
    """
    # Determine the root of both trees
    root_T1 = __root(T1)
    root_T2 = __root(T2)

    # Tree can have one or two roots, if amount of roots is not equal, not isomorphic
    if len(root_T1) != len(root_T2):
        return False

    # If there are two roots, the amount of isomorphisms is the addition of isomorphisms from the two mappings
    # of roots to each other. Because the maximum amount of roots is 2, all roots of T1 are mapped to one root of T2.
    # Root levels are overwritten in the second cycle.
    total_isomorphisms = 0
    for i_root in range(len(root_T1)):
        root1 = root_T1[i_root]
        root2 = root_T2[0]

        # Assign level numbers to all nodes
        __assign_level(root1, 0, [])
        __assign_level(root2, 0, [])

        # Assign all vertices to level number lists
        L1 = {}
        for v in T1.vertices:
            L1.setdefault(v.level, []).append(v)
        L2 = {}
        for v in T2.vertices:
            L2.setdefault(v.level, []).append(v)

        # The number of levels of each tree should be equal, otherwise not isomorphic
        h1, h2 = max(L1.keys()), max(L2.keys())
        if h1 != h2:
            continue
        h = h1

        # From the bottom level up, assign names to the vertices
        are_isomorphic = True    # For each level it is checked if the trees still can be isomoprhic, if not, the loop is stopped
        for i in range(h, -1, -1):
            # Name the vertices of tree T1 an tree T2
            H1 = __name_vertices(L1[i])
            H2 = __name_vertices(L2[i])

            # On each level, the collections of names should be equal for the two trees for them to be isomorphic
            H1.sort()
            H2.sort()
            if H1 != H2:
                are_isomorphic = False
                break

        # Only if the previous for-loop is fully done, the trees are isomorphic
        if are_isomorphic:
            total_isomorphisms += L1[0][0].auto

    # If the trees are not isomorphic, no isomorphisms are counted
    # If total_isomorphisms is greater than 0 , the trees are isomorphic and the amount of automorphisms of each
    # tree are saved and True is returned
    if total_isomorphisms == 0:
        return False
    else:
        T1.automorphisms = total_isomorphisms
        T2.automorphisms = total_isomorphisms
        return True


def trees_automorphisms(T: "Graph"):
    """
    :param T: Graph that are trees (so is_tree(T1) and is_tree(T2) return True)
    :return: Boolean if T1 and T2 are isomorph. If they are, T1 and T2 have a property 'automorphisms' with
    the amount of automorphisms they both have
    """
    # If the tree T already has the property 'automorphisms', return that value
    if hasattr(T, 'automorphisms'):
        return T.automorphisms

    # Otherwise, calculate it

    # Determine the root of the tree
    root_T = __root(T)

    # If there are two roots, the amount of isomorphisms is the addition of isomorphisms from the two roots
    # If there are two roots, root levels are overwritten in the second cycle.
    total_isomorphisms = 0
    for i_root in range(len(root_T)):
        root = root_T[i_root]

        # Assign level numbers to all nodes
        __assign_level(root, 0, [])

        # Assign all vertices to level number lists
        L = {}
        for v in T.vertices:
            L.setdefault(v.level, []).append(v)

        # The number of levels of each tree should be equal, otherwise not isomorphic
        h = max(L.keys())

        # From the bottom level up, assign names to the vertices
        for i in range(h, -1, -1):
            # Name the vertices of tree T1 an tree T2
            H = __name_vertices(L[i])

        total_isomorphisms += L[0][0].auto

    return total_isomorphisms


def __root(T: "Graph"):
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

def __name_vertices(vertices: "List[Vertex]"):
    """
    This method names one level of vertices
    :param vertices: The vertices of a level of a tree to be named
    :return: A list of all names of the vertices in 'vertices'
    """
    # In H all names of vertices are saved
    H = []
    for v in vertices:
        # If the vertex is a leaf, the name 'lr' is assigned
        # The amount of automorphisms of the subtree of the leaf, with the leaf as root, is equal to 1
        if v.degree_fixed == 1:
            v.name = 'lr'
            v.auto = 1
        else:
            # The name of all other vertices is a sorted collection of the names of its children
            # At the same time, remember how many automorphisms the subtree of that vertex has, with that vertex as root
            children_names = []
            children_count = {}
            children_auto = {}
            for n in v.neighbours:
                # The neighbour of a vertex is a child if the level of that neighbour is larger than the level of the vertex
                if n.level > v.level:
                    # If twins are removed, add the name also for each of the removed twins
                    for _ in range(n.n_twins):
                        children_names.append(n.name)
                    children_count[n.name] = children_count.setdefault(n.name, 0) + 1
                    # The amount of isomorphisms of the subtree with 'v' as its root is all combinations of isomorphisms
                    # of all children of 'v' combined, so the amount of isomorphisms of the children must be multiplied
                    # with each other
                    children_auto[n.name] = children_auto.setdefault(n.name, 1) * n.auto

            # If children of 'v' could be mapped to each other, the amount of isomorphisms is increased by all
            # combinations of children that could be swapped. So for each set of children that could be mapped to each
            # other the amount of isomorphisms should be multiplied with factorial(amount of children that can be
            # mapped to each other)
            v_auto = 1
            for child_name in set(children_names):
                v_auto *= factorial(children_count[child_name]) * children_auto[child_name]
            v.auto = v_auto

            # To be able to compare the names of vertices, make sure the collection of children names is sorted
            # and than concatenate them to one string
            children_names.sort()
            v_name = 'l'
            for child_name in children_names:
                v_name += child_name
            v_name += 'r'
            v.name = v_name
        H.append(v.name)

    return H
