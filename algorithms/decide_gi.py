def is_balanced_or_bijected(G: 'Graph'):
    """
    This function returns if the graph is balanced and bijected.
    Note: Only a balanced graph can be bijected.
    :param G: Disjoint union graph
    :return: bool is_balanced, bool is_bijected
    """
    is_balanced_bool, colors = is_balanced(G)
    if is_balanced_bool:
        return is_balanced_bool, __is_bijected(colors)

    return False, False

def is_balanced(G: 'Graph'):
    """
    The vertex coloring of the `self` and `other` graph are extracted from the disjoint union.
    The extraction of `self` and `other` works via the attribute `graph_label` from Vertex.
    If `graph_label` == 1 the vertex colornum is stored in the g_self_colornums list.
    If `graph_label` == 2 the vertex colornum is stored in the g_other_colornums list.

    To determine if the disjoint union Graph coloring is balanced, the two graphs in the disjoint union are compared
    element-wise.
    :param G: Disjoint union graph
    :return: bool is_balanced, list g_self_colornums
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
                raise ValueError('Error: Vertex with graph_label {graph_label} is not an int 1 or 2"'.format(
                    graph_label=repr(v.graph_label)))
        else:
            raise ValueError('Error: Vertex with graph_label {graph_label} is not of type int"'.format(graph_label=repr(v.graph_label)))

    # If the amount of vertices of the two graphs are not the same, the graphs are not isomorphic
    if len(g_self_colornums) != len(g_other_colornums):
        return False, None

    for self_colnum in g_self_colornums:
        if self_colnum in g_other_colornums:
            g_other_colornums.remove(self_colnum)
        else:
            return False, None

    return True, g_self_colornums


def __is_bijected(g_self_colornums: list):
    """
    Bijection can be tested after a Graph has been proven to be balanced.
    With use of a set it is tested if each color only is present once.
    If this is the case, the graph is a bijected.
    :param g_self_colornums list of colors
    :return bool is_bijected
    """
    g_self_colornums_set = set(g_self_colornums)

    return len(g_self_colornums) == len(g_self_colornums_set)
