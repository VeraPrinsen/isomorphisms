def is_balanced_or_bijected(G: 'Graph'):
    """
    :param G:
    :return: bool is_balanced, bool is_bijected
    This function returns if the graph is balanced and bijected.
    Note: Only a balanced graph can be bijected.
    """
    is_balanced, colors = __is_balanced(G)
    if is_balanced:
        return is_balanced, __is_bijected(colors)

    return False, False

def __is_balanced(G: 'Graph'):
    """
    :param G:
    :return: bool is_balanced, list g_self_colornums

    The vertex coloring of the `self` and `other` graph are extracted from the disjoint union.
    The extraction of `self` and `other` works via the attribute `graph_label` from Vertex.
    If `graph_label` == 1 the vertex colornum is stored in the g_self_colornums list.
    If `graph_label` == 2 the vertex colornum is stored in the g_other_colornums list.

    To determine if the disjoint union Graph coloring is balanced, the two graphs in the disjoint union are compared
    element-wise.
    """
    g_self_colornums  = []
    g_other_colornums = []

    for v in G.vertices:
        if type(v.graph_label) == int:
            if v.graph_label == 1:
                g_self_colornums.append(v.colornum)
            elif v.graph_label == 2:
                g_other_colornums.append(v.colornum)
        else:
            print("Error: Vertex graph_label is not of type bool")

    for self_colnum in g_self_colornums:
        if self_colnum in g_other_colornums:
            g_other_colornums.remove(self_colnum)
        else:
            return False, None

    return True, g_self_colornums

def __is_bijected(g_self_colornums: list):
    """
    :param g_self_colornums list of colors
    :return bool is_bijected

    Bijection can be tested after a Graph has been proven to be balanced.
    With use of a set it is tested if each color only is present once.
    If this is the case, the graph is a bijected.
    """
    g_self_colornums_set = set(g_self_colornums)

    return len(g_self_colornums) == len(g_self_colornums_set)
