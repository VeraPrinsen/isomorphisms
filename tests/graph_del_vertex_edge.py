from supporting_components.graph import Graph, Vertex, Edge
from input_output.sys_output import fail, passed


def test_graph_del_edge():
    G = Graph(False, 0)
    v1 = Vertex(G)
    v2 = Vertex(G)
    e1 = Edge(v1, v2)
    G.add_edge(e1)

    test_result = e1 in G.edges and e1 in v1.incidence and e1 in v2.incidence

    G.del_edge(e1)

    return test_result and e1 not in G.edges and e1 not in v1.incidence and e1 not in v2.incidence


def test_graph_del_vertex():
    G = Graph(False, 0)
    v1 = Vertex(G)
    v2 = Vertex(G)
    e1 = Edge(v1, v2)
    G.add_edge(e1)
    test_result = v1 in G.vertices and v2 in G.vertices and e1 in G.edges and v1 in v2.neighbours

    G.del_vertex(v1)
    return test_result and v1 not in G.vertices and v2 in G.vertices and e1 not in G.edges and v1 not in v2.neighbours


def unit_test(write_csv_any=True, write_stdout_pass=True, write_stdout_fail=True):
    # Because this test does not show any intermediate results, the arguments are ignored.
    test_name = 'graph_del_vertex_edge'
    print('<' + test_name + '>')
    pass_bool = True

    if not test_graph_del_edge():
        fail("test_graph_del_edge: TEST FAILED")
        pass_bool = False

    if not test_graph_del_vertex():
        fail("test_graph_del_vertex: TEST FAILED")
        pass_bool = False

    if pass_bool:
        passed('' + test_name + ' PASS')

    print('</' + test_name + '>')

    return pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
