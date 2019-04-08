from supporting_components.graph import Graph, Vertex
from typing import List


def color_refinement(G: "Graph"):
    """
    Given graph G, this method changes the colornum property of the vertices in the graph, so that all vertices with
    the same colornum could be mapped to each other while structurally remaining the same graph
    :param G: Graph to be colored
    :return: Finished colored graph
    """
    # init
    #G.neighbours_of = {}

    has_changed = True
    while has_changed:
        has_changed = False
        for colornum, vertices in G.colors.copy().items():
            if len(vertices) == 1:
                continue

            G.max_colornum += 1
            has_changed = __colorgroup_refinement(G, colornum, vertices, G.max_colornum) or has_changed
    return G


def fast_color_refinement(G: "Graph"):
    """
    Performs fast color refinement on the graph.
    It creates a queue of color groups to check for the initially colored graph.
    For each color group in the queue, it splits the other color groups based on whether or not the vertices are
    neighbours of one of the vertices in the color group.
    If the result is the same for all vertices in a group, the group is left unchanged.
    The newly created group is added to the queue if the original group is in the queue.
    If the original group is not in the queue, the largest of the original and the new group is added to the queue.
    The algorithm terminates if the queue is empty.
    :param G: The graph to perform color refinement on
    :return: The colored graph
    """

    queue = __initialize_queue(G)
    neighbours_of = dict()
    while queue:
        # Get first color and remove that from the queue
        color = queue.pop(0)
        vertices_in_color_group = G.colors[color]
        # Get the neighbours of the color group grouped by color

        neighbours_of_color_group = __get_color_groups_with_neighbours_in_color_group(vertices_in_color_group, neighbours_of)

        remove_c_vertex_group = list()
        add_c_vertex_group = list()

        for c, color_group in neighbours_of_color_group.items():
            # Do nothing if the size of the set in neighbours_of_color_group is zero or if the size is the same as the size of the list in colors
            if len(color_group) == 0 or len(color_group) == len(G.colors[c]):
                continue
            # Change the color of the vertices in neighbours_of_color_group
            G.max_colornum += 1
            for vertex in color_group:
                vertex.colornum = G.max_colornum
                # Update colors of graph
                print('v')
                print(vertex)
                G.colors[c].remove(vertex)
                remove_c_vertex_group.append((c, vertex))
                G.colors.setdefault(G.max_colornum, list()).append(vertex)
                add_c_vertex_group.append((G.max_colornum, vertex))
            # Add the correct color to the queue
            if c in queue:
                queue.append(G.max_colornum)
            else:
                # Append the current color to the queue if the amount of vertices that did not change color is larger
                # than the amount of vertices that did change color
                if 2 * len(color_group) < len(G.colors[c]):
                    queue.append(c)
                else:
                    queue.append(G.max_colornum)

        # Update neighbours
        # for tup in add_c_vertex_group:
        #     neighbours_of[color].setdefault(tup[0], set()).add(tup[1])

        # for tup in remove_c_vertex_group:
        #     neighbours_of[color][tup[0]].remove(tup[1])


    return G


def __colorgroup_refinement(G, colornum, vertices: List["Vertex"], next_colornum):
    """
    For vertices with property colornum = 'colornum', define which vertices have equal neighbours and which do not
    If a vertex within this group does not have the same neighbours as the first vertex in this group, these vertices
    will be given a new colornum 'next_colornum' and are moved from key colornum to next_colornum in the dictionary
    :param G: The graph currently evaluated
    :param colornum: Current colornum to be evaluated
    :param vertices: Vertices of that colornum to be evaluated
    :param next_colornum: The next colornum that was not in colors as a key before this colorgroup refinement
    :return has_changed: Returns if the colorgroup refinement has changed some colornum values for vertices
    """

    # Creates a list of all colornums of the neighbours of the first vertex in 'vertices'
    v0 = vertices[0]
    v0_colors = []
    for v in v0.neighbours:
        v0_colors.append(v.colornum)

    # Compare each vertex other than the first vertex in 'vertices' with the first vertex in 'vertices'
    # If the vertex is different, remember it in different_vertices
    has_changed = False
    different_vertices = []
    for v in vertices[1:]:
        if not __neighbours_equal(v0_colors, v):
            different_vertices.append(v)

    # After all vertices have been compared, change the colornum of all different vertices
    for v in different_vertices:
        v.colornum = next_colornum
        G.colors.setdefault(next_colornum, []).append(v)
        G.colors[colornum].remove(v)
        has_changed = True

    return has_changed


def __neighbours_equal(v0: List[int], v: Vertex):
    """
    Determines if the colornum properties of the neighbours of vertex 'v' matches with the list of colornum properties in
    the list v0_colors
    :param v0_colors: List of colornum properties of the neighbours of the vertex to be compared with
    :param v: The vertex that needs to be compared with vertex v0
    :return: Boolean if neighbours of vertex v0 and v are equal
    """
    v0_colors = v0.copy()
    for n in v.neighbours:
        if n.colornum in v0_colors:
            v0_colors.remove(n.colornum)
        else:
            return False
    return True


def __initialize_queue(G: "Graph"):
    """
    Initializes the queue of the graph for the fast color refinement using the initial coloring.
    Puts all color groups in the queue except the largest color group.
    :param G: The graph to construct the queue for
    :return: The queue of the graph
    """
    queue = list(G.colors.keys())
    largest_color_group_size = 0
    largest_color_group = 0
    for color, vertices in G.colors.items():
        if len(vertices) > largest_color_group_size:
            largest_color_group = color
            largest_color_group_size = len(vertices)
    queue.remove(largest_color_group)
    return queue


def __get_color_groups_with_neighbours_in_color_group(vertices_in_color_group: "List[Vertex]", neighbours_of):
    """
    Returns a dict with the color of the color group as key and the set of neighbours of the color group currently
    investigated as value.
    :param vertices_in_color_group: The vertices in the color group currently investigated
    :return: The dict with the color and the vertices in those color groups with a neighbour in the color group
    currently investigated
    """

    #neighbours_of_color_group = {}
    # Get the color of the color group currently investigated
    color = vertices_in_color_group[0].colornum

    #neighbours_of = {}

    # Allocate a new dict()
    if not color in neighbours_of:
        neighbours_of[color] = {}


    for vertex in vertices_in_color_group:
        neighbours = vertex.neighbours
        for neighbour in neighbours:
            if neighbour.colornum != color:
                in_dict = False

                for colnum, v_set in neighbours_of[color].items():
                    if neighbour in v_set and neighbour.colornum != colnum:
                        print(neighbour)
                        print(v_set)
                        neighbours_of[color][colnum].remove(neighbour)
                        print('rem')

                    if neighbour in v_set and neighbour.colornum == colnum:
                        in_dict = True

                if not in_dict:
                    neighbours_of[color].setdefault(neighbour.colornum, set()).add(neighbour)
                # Only add the vertex to the map if it is not in the color group currently investigated


    return neighbours_of[color]
