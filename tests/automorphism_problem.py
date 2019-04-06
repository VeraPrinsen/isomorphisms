from input_output.sys_output import fail, passed
from algorithms.automorphism_problem import count_automorphisms
from algorithms.color_refinement import fast_color_refinement
from supporting_components.graph import Graph, Vertex, Edge
from supporting_components.permv2 import permutation
from algorithms.preprocessing import fix_degrees
from algorithms.color_initialization import degree_color_initialization

"""
To test if the new branching algorithm works.
"""


def test_example_slides16():
    G = Graph(False, 0)
    v0 = Vertex(G)
    v1 = Vertex(G)
    v2 = Vertex(G)
    v3 = Vertex(G)
    v4 = Vertex(G)
    v5 = Vertex(G)
    v6 = Vertex(G)

    G.add_edge(Edge(v0, v3))
    G.add_edge(Edge(v0, v1))
    G.add_edge(Edge(v0, v2))
    G.add_edge(Edge(v0, v5))
    G.add_edge(Edge(v0, v4))
    G.add_edge(Edge(v0, v6))
    G.add_edge(Edge(v1, v3))
    G.add_edge(Edge(v2, v3))
    G.add_edge(Edge(v4, v6))
    G.add_edge(Edge(v5, v6))

    fix_degrees(G)
    G_disjoint_union = G.self_disjoint_union()
    degree_color_initialization(G_disjoint_union)
    order = count_automorphisms(G_disjoint_union, fast_color_refinement)

    return order == 8


def test_example_slides_petersen():
    G = Graph(False, 0)
    v0 = Vertex(G)
    v1 = Vertex(G)
    v2 = Vertex(G)
    v3 = Vertex(G)
    v4 = Vertex(G)
    v5 = Vertex(G)
    v6 = Vertex(G)
    v7 = Vertex(G)
    v8 = Vertex(G)
    v9 = Vertex(G)

    G.add_edge(Edge(v0, v1))
    G.add_edge(Edge(v0, v6))
    G.add_edge(Edge(v1, v2))
    G.add_edge(Edge(v1, v7))
    G.add_edge(Edge(v2, v3))
    G.add_edge(Edge(v2, v8))
    G.add_edge(Edge(v3, v4))
    G.add_edge(Edge(v3, v9))
    G.add_edge(Edge(v4, v0))
    G.add_edge(Edge(v4, v5))
    # inner star
    G.add_edge(Edge(v5, v7))
    G.add_edge(Edge(v7, v9))
    G.add_edge(Edge(v9, v6))
    G.add_edge(Edge(v6, v8))
    G.add_edge(Edge(v8, v5))

    fix_degrees(G)
    G_disjoint_union = G.self_disjoint_union()
    degree_color_initialization(G_disjoint_union)
    order = count_automorphisms(G_disjoint_union, fast_color_refinement)

    return order == 120


def test_example_slides_star():
    G = Graph(False, 0)
    v0 = Vertex(G)
    v1 = Vertex(G)
    v2 = Vertex(G)
    v3 = Vertex(G)
    v1_1 = Vertex(G)
    v1_2 = Vertex(G)
    v2_1 = Vertex(G)
    v2_2 = Vertex(G)
    v3_1 = Vertex(G)
    v3_2 = Vertex(G)

    G.add_edge(Edge(v0, v1))
    G.add_edge(Edge(v0, v2))
    G.add_edge(Edge(v0, v3))
    G.add_edge(Edge(v1, v1_1))
    G.add_edge(Edge(v1, v1_2))
    G.add_edge(Edge(v2, v2_1))
    G.add_edge(Edge(v2, v2_2))
    G.add_edge(Edge(v3, v3_1))
    G.add_edge(Edge(v3, v3_2))

    fix_degrees(G)
    G_disjoint_union = G.self_disjoint_union()
    degree_color_initialization(G_disjoint_union)
    order = count_automorphisms(G_disjoint_union, fast_color_refinement)

    return order == 48


def unit_test():
    test_name = 'automorphisms-problem'
    print('<' + test_name + '>')
    pass_bool = True
    if not test_example_slides16():
        fail("test_example_slides16: TEST FAILED")
        pass_bool = False

    if not test_example_slides_petersen():
        fail("test_example_slides_petersen: TEST FAILED")
        pass_bool = False

    if not test_example_slides_star():
        fail("test_example_slides_star: TEST FAILED")
        pass_bool = False

    if pass_bool:
        passed('' + test_name + ' PASS')

    print('</' + test_name + '>')

    return pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
