from supporting_components.graph import Graph, Vertex, Edge
from input_output.sys_output import fail, passed
from algorithms.preprocessing import remove_twins


"""
For this test a graph is used in which v1, v2 and v3 are triplets and v6 and v7 are twins.
"""


def test_remove_unconnected_twins():
    G = Graph(False, 0)
    v0 = Vertex(G)
    v1 = Vertex(G)
    v2 = Vertex(G)
    v3 = Vertex(G)
    v4 = Vertex(G)
    v5 = Vertex(G)
    v6 = Vertex(G)
    v7 = Vertex(G)

    e03 = Edge(v0, v3)
    e04 = Edge(v0, v4)
    e13 = Edge(v1, v3)
    e14 = Edge(v1, v4)
    e23 = Edge(v2, v3)
    e24 = Edge(v2, v4)
    e35 = Edge(v3, v5)
    e56 = Edge(v5, v6)
    e57 = Edge(v5, v7)

    G.add_edge(e03)
    G.add_edge(e04)
    G.add_edge(e13)
    G.add_edge(e14)
    G.add_edge(e23)
    G.add_edge(e24)
    G.add_edge(e35)
    G.add_edge(e56)
    G.add_edge(e57)

    # Test if all vertices and edges are in the graph
    test_result = all(v in G.vertices for v in [v1, v2, v3, v4, v5, v6, v7]) and all(e in G.edges for e in [e03, e04, e13, e14, e23, e24, e35, e56, e57])

    factor = remove_twins(G)

    # After removing twins, vertex 3, 4 and 5 should still be in the graph, only 1 of vertex 0, 1 and 2 should be in G and 1 of vertex 6 and 7.
    # Also the factor should equal 3! * 2! = 12
    return test_result \
           and all(v in G.vertices for v in [v3, v4, v5]) \
           and sum([v0 in G.vertices, v1 in G.vertices, v2 in G.vertices]) == 1 \
           and sum([v6 in G.vertices, v7 in G.vertices]) == 1 \
           and factor == 12


def test_remove_connected_twins():
    G = Graph(False, 0)
    v0 = Vertex(G)
    v1 = Vertex(G)
    v2 = Vertex(G)
    v3 = Vertex(G)
    v4 = Vertex(G)
    v5 = Vertex(G)
    v6 = Vertex(G)
    v7 = Vertex(G)

    e03 = Edge(v0, v3)
    e04 = Edge(v0, v4)
    e13 = Edge(v1, v3)
    e14 = Edge(v1, v4)
    e23 = Edge(v2, v3)
    e24 = Edge(v2, v4)
    e35 = Edge(v3, v5)
    e56 = Edge(v5, v6)
    e57 = Edge(v5, v7)

    G.add_edge(e03)
    G.add_edge(e04)
    G.add_edge(e13)
    G.add_edge(e14)
    G.add_edge(e23)
    G.add_edge(e24)
    G.add_edge(e35)
    G.add_edge(e56)
    G.add_edge(e57)

    e01 = Edge(v0, v1)
    e02 = Edge(v0, v2)
    e12 = Edge(v1, v2)
    e67 = Edge(v6, v7)
    G.add_edge(e01)
    G.add_edge(e02)
    G.add_edge(e12)
    G.add_edge(e67)

    # Test if all vertices and edges are in the graph
    test_result = all(v in G.vertices for v in [v1, v2, v3, v4, v5, v6, v7]) and all(e in G.edges for e in [e03, e04, e13, e14, e23, e24, e35, e56, e57, e01, e02, e12, e67])

    factor = remove_twins(G)

    # After removing twins, vertex 3, 4 and 5 should still be in the graph, only 1 of vertex 0, 1 and 2 should be in G and 1 of vertex 6 and 7.
    # Also the factor should equal 3! * 2! = 12
    return test_result \
           and all(v in G.vertices for v in [v3, v4, v5]) \
           and sum([v0 in G.vertices, v1 in G.vertices, v2 in G.vertices]) == 1 \
           and sum([v6 in G.vertices, v7 in G.vertices]) == 1 \
           and factor == 12


def unit_test():
    # Because this test does not show any intermediate results, the arguments are ignored.
    test_name = 'preprocessing_twins'
    print('<' + test_name + '>')
    pass_bool = True
    if not test_remove_unconnected_twins():
        fail("test_remove_unconnected_twins: TEST FAILED")
        pass_bool = False

    if not test_remove_connected_twins():
        fail("test_remove_connected_twins: TEST FAILED")
        pass_bool = False

    if pass_bool:
        passed('' + test_name + ' PASS')

    print('</' + test_name + '>')

    return pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
