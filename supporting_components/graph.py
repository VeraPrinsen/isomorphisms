"""
This is a module for working with directed and undirected multigraphs.
"""
# version: 29-01-2015, Paul Bonsma
# version: 01-02-2017, Pieter Bos, Tariq Bontekoe

from typing import List, Union, Set, Dict


class GraphError(Exception):
    """
    An error that occurs while manipulating a `Graph`
    """

    def __init__(self, message: str):
        """
        Constructor
        :param message: The error message
        :type message: str
        """
        super(GraphError, self).__init__(message)


class Vertex(object):
    """
    `Vertex` objects have a property `graph` pointing to the graph they are part of,
    and an attribute `label` which can be anything: it is not used for any methods,
    except for `__str__`.
    """

    def __init__(self, graph: "Graph", label=None, graph_label=None, coupling_label=None):
        """
        Creates a vertex, part of `graph`, with optional label `label`.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        :param graph: The graph that this `Vertex` is a part of
        :param label: Optional parameter to specify a label for the vertex
        :param graph_label: Optional parameter to specify a graph label for the vertex. For ex.: used to identify vertex originating Graph in unions.
        """
        if label is None:
            label = graph._next_label()

        self._graph = graph
        self.label = label
        self.graph_label = graph_label
        self.coupling_label = coupling_label
        self._incidence = {}
        self.colornum = None
        self.degree_fixed = None
        self.n_twins = 1

    def __repr__(self):
        """
        A programmer-friendly representation of the vertex.
        :return: The string to approximate the constructor arguments of the `Vertex'
        """
        return 'Vertex(label={}, #incident={})'.format(self.label, len(self._incidence))

    def __str__(self) -> str:
        """
        A user-friendly representation of the vertex, that is, its label.
        :return: The string representation of the label.
        """
        return str(self.label)

    def is_adjacent(self, other: "Vertex") -> bool:
        """
        Returns True iff `self` is adjacent to `other` vertex.
        :param other: The other vertex
        """
        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        """
        For internal use only; adds an edge to the incidence map
        :param edge: The edge that is used to add the incidence
        """
        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    def _del_incidence(self, edge: "Edge"):
        """
        For internal use only; deletes an edge from the incidence map
        :param edge: The edge that needs to be removed
        """
        other = edge.other_end(self)

        if edge in self._incidence[other]:
            self._incidence[other].remove(edge)
            if len(self._incidence[other]) == 0:
                del self._incidence[other]

    @property
    def graph(self) -> "Graph":
        """
        The graph of this vertex
        :return: The graph of this vertex
        """
        return self._graph

    @property
    def incidence(self) -> List["Edge"]:
        """
        Returns the list of edges incident with the vertex.
        :return: The list of edges incident with the vertex
        """
        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbours(self) -> List["Vertex"]:
        """
        Returns the list of neighbors of the vertex.
        """
        return list(self._incidence.keys())

    @property
    def degree(self) -> int:
        """
        Returns the degree of the vertex
        """
        return sum(map(len, self._incidence.values()))


class Edge(object):
    """
    Edges have properties `tail` and `head` which point to the end vertices
    (`Vertex` objects). The order of these matters when the graph is directed.
    """

    def __init__(self, tail: Vertex, head: Vertex, weight=None):
        """
        Creates an edge between vertices `tail` and `head`
        :param tail: In case the graph is directed, this is the tail of the arrow.
        :param head: In case the graph is directed, this is the head of the arrow.
        :param weight: Optional weight of the vertex, which can be any type, but usually is a number.
        """
        if tail.graph != head.graph:
            raise GraphError("Can only add edges between vertices of the same graph")

        self._tail = tail
        self._head = head
        self._weight = weight

    def __repr__(self):
        """
        A programmer-friendly representation of the edge.
        :return: The string to approximate the constructor arguments of the `Edge'
        """
        return 'Edge(head={}, tail={}, weight={})'.format(self.head.label, self.tail.label, self.weight)

    def __str__(self) -> str:
        """
        A user friendly representation of this edge
        :return: A user friendly representation of this edge
        """
        return '({}, {})'.format(str(self.tail), str(self.head))

    @property
    def tail(self) -> "Vertex":
        """
        In case the graph is directed, this represents the tail of the arrow.
        :return: The tail of this edge
        """
        return self._tail

    @property
    def head(self) -> "Vertex":
        """
        In case the graph is directed, this represents the head of the arrow.
        :return: The head of this edge
        """
        return self._head

    @property
    def weight(self):
        """
        The weight of this edge, which can also just be used as a generic label.
        :return: The weight of this edge
        """
        return self._weight

    def other_end(self, vertex: Vertex) -> Vertex:
        """
        Given one end `vertex` of the edge, this returns
        the other end vertex.
        :param vertex: One end
        :return: The other end
        """
        if self.tail == vertex:
            return self.head
        elif self.head == vertex:
            return self.tail

        raise GraphError(
            'edge.other_end(vertex): vertex must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        """
        Returns True iff the edge is incident with the
        vertex.
        :param vertex: The vertex
        :return: Whether the vertex is incident with the edge.
        """
        return self.head == vertex or self.tail == vertex


class Graph(object):
    def __init__(self, directed: bool, n: int=0, simple: bool=False):
        """
        Creates a graph.
        :param directed: Whether the graph should behave as a directed graph.
        :param simple: Whether the graph should be a simple graph, that is, not have multi-edges or loops.
        :param n: Optional, the number of vertices the graph should create immediately
        """
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0
        self.max_colornum = 0
        self.colors = {}

        for i in range(n):
            self.add_vertex(Vertex(self))

    def __repr__(self):
        """
        A programmer-friendly representation of the Graph.
        :return: The string to approximate the constructor arguments of the `Graph'
        """
        return 'Graph(directed={}, simple={}, #edges={n_edges}, #vertices={n_vertices})'.format(
            self._directed, self._simple, n_edges=len(self._e), n_vertices=len(self._v))

    def __str__(self) -> str:
        """
        A user-friendly representation of this graph
        :return: A textual representation of the vertices and edges of this graph
        """
        return 'V=[' + ", ".join(map(str, self._v)) + ']\nE=[' + ", ".join(map(str, self._e)) + ']'

    def _next_label(self) -> int:
        """
        Generates unique labels for vertices within the graph
        :return: A unique label
        """
        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def simple(self) -> bool:
        """
        Whether the graph is a simple graph, that is, it does not have multi-edges or loops.
        :return: Whether the graph is simple
        """
        return self._simple

    @property
    def directed(self) -> bool:
        """
        Whether the graph behaves as a directed graph
        :return: Whether the graph is directed
        """
        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        """
        :return: The `set` of vertices of the graph
        """
        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        """
        :return: The `set` of edges of the graph
        """
        return list(self._e)

    def __iter__(self):
        """
        :return: Returns an iterator for the vertices of the graph
        """
        return iter(self._v)

    def __len__(self) -> int:
        """
        :return: The number of vertices of the graph
        """
        return len(self._v)

    def add_vertex(self, vertex: "Vertex"):
        """
        Add a vertex to the graph.
        :param vertex: The vertex to be added.
        """
        if vertex.graph != self:
            raise GraphError("A vertex must belong to the graph it is added to")

        self._v.append(vertex)

    def del_vertex(self, vertex: "Vertex"):
        """
        Delete a vertex from the graph. Also remove edges connected to that vertex.
        :param vertex: The vertex to be removed
        """
        for e in vertex.incidence:
            vertex.graph.del_edge(e)

        self._v.remove(vertex)


    def add_edge(self, edge: "Edge"):
        """
        Add an edge to the graph. And if necessary also the vertices.
        Includes some checks in case the graph should stay simple.
        :param edge: The edge to be added
        """

        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def del_edge(self, edge: "Edge"):
        """
        Delete edge from the graph.
        :param edge: The edge to be deleted.
        """
        edge.head._del_incidence(edge)
        edge.tail._del_incidence(edge)

        if edge in self._e:
            self._e.remove(edge)

    def __add__(self, other: "Graph") -> "Graph":
        """
        Make a disjoint union of two graphs.
        A dictionary is used with the self and other graph's vertices as key.
        A graph_label property is added to distinguish between the original graphs.
        The value of the dictionary (dict) is a new vertex in the disjoint union.
        The new vertex labelled using the property `graph_label` of Vertex.
        Vertices originating from self are graph_label = True, the other graph_label = False.
        :param other: Graph to add to `self'.
        :return: New undirected graph which is a disjoint union of `self' and `other'.
        """
        disjoint_union_graph = Graph(directed=False)

        vertex_reference_self = dict()
        vertex_reference_other = dict()

        for v_before_union in self.vertices:
            vertex_reference_self[v_before_union] = Vertex(graph=disjoint_union_graph, graph_label=1)
            vertex_reference_self[v_before_union].degree_fixed = v_before_union.degree_fixed
            vertex_reference_self[v_before_union].n_twins = v_before_union.n_twins
        for v_before_union in other.vertices:
            vertex_reference_other[v_before_union] = Vertex(graph=disjoint_union_graph, graph_label=2)
            vertex_reference_other[v_before_union].degree_fixed = v_before_union.degree_fixed
            vertex_reference_other[v_before_union].n_twins = v_before_union.n_twins

        # Add edges
        # If vertex on Edge is not present when calling add.edge(), the vertex is added to the Graph object.
        for e_before_union in self.edges:
            disjoint_union_graph.add_edge(
                Edge(
                    vertex_reference_self[e_before_union.tail],
                    vertex_reference_self[e_before_union.head]
                )
            )
        for e_before_union in other.edges:
            disjoint_union_graph.add_edge(
                Edge(
                    vertex_reference_other[e_before_union.tail],
                    vertex_reference_other[e_before_union.head]
                )
            )

        return disjoint_union_graph

    def self_disjoint_union(self):
        """
        Make a disjoint union with itself.
        A unique coupling value is given to tie nodes back together when comparing.
        A graph_label property is added to distinguish between the original graphs.
        :return: New undirected graph which is a disjoint union of itself.
        """
        disjoint_union_graph = Graph(directed=False)

        vertex_reference_self = dict()
        vertex_reference_other = dict()

        for v_before_union in self.vertices:
            vertex_reference_self[v_before_union] = Vertex(graph=disjoint_union_graph, graph_label=1, coupling_label=v_before_union.label)
            vertex_reference_self[v_before_union].degree_fixed = v_before_union.degree_fixed
            vertex_reference_self[v_before_union].n_twins = v_before_union.n_twins

        for v_before_union in self.vertices:
            vertex_reference_other[v_before_union] = Vertex(graph=disjoint_union_graph, graph_label=2, coupling_label=v_before_union.label)
            vertex_reference_other[v_before_union].degree_fixed = v_before_union.degree_fixed
            vertex_reference_other[v_before_union].n_twins = v_before_union.n_twins

        # Add edges
        # If vertex on Edge is not present when calling add.edge(), the vertex is added to the Graph object.
        for e_before_union in self.edges:
            disjoint_union_graph.add_edge(
                Edge(
                    vertex_reference_self[e_before_union.tail],
                    vertex_reference_self[e_before_union.head]
                )
            )
        for e_before_union in self.edges:
            disjoint_union_graph.add_edge(
                Edge(
                    vertex_reference_other[e_before_union.tail],
                    vertex_reference_other[e_before_union.head]
                )
            )

        return disjoint_union_graph

    def __iadd__(self, other: Union[Edge, Vertex]) -> "Graph":
        """
        Add either an `Edge` or `Vertex` with the += syntax.
        :param other: The object to be added
        :return: The modified graph
        """
        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        """
        Tries to find edges between two vertices.
        :param u: One vertex
        :param v: The other vertex
        :return: The set of edges incident with both `u` and `v`
        """
        result = u._incidence.get(v, set())

        if not self._directed:
            result |= v._incidence.get(u, set())

        return set(result)

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        """
        Returns True iff vertices `u` and `v` are adjacent. If the graph is directed, the direction of the edges is
        respected.
        :param u: One vertex
        :param v: The other vertex
        :return: Whether the vertices are adjacent
        """
        return v in u.neighbours and (not self.directed or any(e.head == v for e in u.incidence))

    def copy(self):
        """
        Returns a copy of the graph.
        :return: The copy of the graph.
        """
        copy = Graph(self.directed)
        copy.max_colornum = self.max_colornum
        vertices_old_to_new = {}
        colors = {}

        for v in self.vertices:
            vertices_old_to_new[v] = Vertex(copy)
            vertices_old_to_new[v].label = v.label
            vertices_old_to_new[v].colornum = v.colornum
            vertices_old_to_new[v].graph_label = v.graph_label
            vertices_old_to_new[v].degree_fixed = v.degree_fixed
            colors.setdefault(v.colornum, list()).append(vertices_old_to_new[v])
            vertices_old_to_new[v].n_twins = v.n_twins

        for e in self.edges:
            edge = Edge(vertices_old_to_new[e.tail], vertices_old_to_new[e.head])
            copy.add_edge(edge)

        copy.colors = colors
        return copy

    def is_equal(self, other):
        """
        Returns whether or not these two graphs are equal. It checks for three things
        - If the same vertex is not in the copy.
        - If the attributes of the vertices with the same label are equal.
        - If the length of the list of the other graph is empty in the end.
        This last check should be true, since if a vertex equal to a vertex in the graph is found in the other graph,
        it is removed from the list of vertices in the other graph.
        :param other: The other graph to compare this graph with.
        :return: Whether or not these two graphs are equal.
        """
        other_vertices = other.vertices
        for v in self.vertices:
            if v in other.vertices:
                return False
            for o in other_vertices:
                if v.label == o.label:
                    if v.graph_label != o.graph_label or v.colornum != o.colornum or v.degree_fixed != o.degree_fixed:
                        return False
                    other_vertices.remove(o)
        return len(other_vertices) == 0

    def backup(self):
        """
        Creates a backup of the maximum colornum and the color map of vertices grouped by color.
        :return: The maximum colornum and the color map
        """
        colors = {}
        for v in self.vertices:
            colors.setdefault(v.colornum, list()).append(v)
        return self.max_colornum, colors

    def revert(self, max_colornum: "int", colors: "Dict[int, List[Vertex]]"):
        """
        Convert a graph to the state of the arguments
        :param max_colornum: The maximum colornum
        :param colors: The map of color with its vertices
        """
        for color, vertices in colors.items():
            for v in vertices:
                v.colornum = color
        self.max_colornum = max_colornum
        self.colors = colors

    def complement(self):
        """
        Create the complement of the graph.
        :return: The complement
        """
        complement = Graph(self.directed)
        vertices_original_to_complement = {}

        # Create vertex mapping from original graph to complement graph
        for v in self.vertices:
            vertices_original_to_complement[v] = Vertex(complement)
            vertices_original_to_complement[v].label = v.label
            vertices_original_to_complement[v].degree_fixed = v.degree_fixed
        # Add edge to complement graph only if the edge does not exist in the original graph and no undirected edge is
        # already present in the complement graph between those two vertices
        for v in self.vertices:
            neighbours = v.neighbours
            for w in self.vertices:
                if w not in neighbours and v != w and not any((edge.tail == vertices_original_to_complement[v] and edge.head == vertices_original_to_complement[w]) or (edge.head == vertices_original_to_complement[v] and edge.tail == vertices_original_to_complement[w]) for edge in complement.edges):
                    complement.add_edge(Edge(vertices_original_to_complement[v], vertices_original_to_complement[w]))
        return complement

    def is_disconnected(self):
        """
        Checks if the graph is disconnected.
        :return: Whether or not the graph is disconnected
        """
        reached_vertices = self.bfs(1, self.vertices[0])
        return len(reached_vertices) < len(self.vertices)

    def bfs(self, part, starting_vertex):
        """
        Breadth first search through the graph to find all vertices that can be reached from the starting vertex.
        It labels the reached vertices with the part property specified in the arguments.
        :param part: The part of the graph currently searching for, set in the part property of the reached vertices
        :param starting_vertex: The starting vertex of the bfs
        :return: The list of vertices found
        """
        starting_vertex.part = part
        active_vertices = [starting_vertex]
        reached_vertices = [starting_vertex]
        while active_vertices:
            active_vertex = active_vertices[0]  # BFS
            for vertex in active_vertex.neighbours:
                if vertex not in reached_vertices:
                    reached_vertices.append(vertex)
                    active_vertices.append(vertex)
                    vertex.part = part
            active_vertices.remove(active_vertex)
        return reached_vertices

    def get_connected_subgraphs(self):
        """
        Returns the connected subgraphs of the disconnected graph.
        Continues bfs on the graph until all vertices are visited.
        Each vertex belongs to the group of vertices with the same part property.
        Using the list of lists of vertices of the parts, the disconnected subgraphs are constructed.
        :return: The connected subgraphs
        """
        vertices_connected_subgraphs = []
        reached_vertices = []
        for v in self.vertices:
            if hasattr(v, 'part'):
                reached_vertices.append(v)
        vertices_connected_subgraphs.append(reached_vertices)
        number_of_vertices = len(reached_vertices)
        part = 1
        while number_of_vertices < len(self.vertices):
            for v in self.vertices:
                if not hasattr(v, 'part'):
                    vertex = v
                    part += 1
                    break
            reached_vertices = self.bfs(part, vertex)
            vertices_connected_subgraphs.append(reached_vertices)
            number_of_vertices += len(reached_vertices)
        return vertices_connected_subgraphs


class UnsafeGraph(Graph):
    @property
    def vertices(self) -> List["Vertex"]:
        return self._v

    @property
    def edges(self) -> List["Edge"]:
        return self._e

    def add_vertex(self, vertex: "Vertex"):
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        left = u._incidence.get(v, None)
        right = None

        if not self._directed:
            right = v._incidence.get(u, None)

        if left is None and right is None:
            return set()

        if left is None:
            return right

        if right is None:
            return left

        return left | right

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u._incidence or (not self._directed and u in v._incidence)
