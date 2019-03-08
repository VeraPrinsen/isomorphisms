from supporting_components.graph_io import *
from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement


def test_copy(graph):
    """
    Tests the copy method of the graph
    :param graph: The graph to copy
    :return: Whether or not the graph is copied correctly
    """
    copy = graph.copy()
    return copy.is_equal(graph)


files = ['colorref_smallexample_4_7', 'colorref_smallexample_6_15', 'colorref_smallexample_2_49']
error_count = 0
graph_count = 0
for file in files:
    filename = '../test_graphs/color_refinement/' + file + '.grl'
    with open(filename) as f:
        L = load_graph(f, read_list=True)
        for i in range(0, len(L[0]) - 1):
            for j in range(i + 1, len(L[0])):
                graph_count += 1
                graph = L[0][i] + L[0][j]
                color_refinement(degree_color_initialization(graph))
                is_equal = test_copy(graph)
                if not is_equal:
                    error_count += 1
                    print('---------------------------')
                    print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                    print('---------------------------')
                    print("Is copy equal to graph: " + str(is_equal))
                    print('')
print('---------------------------')
print("Statistics of test:")
print('---------------------------')
print("Amount of graphs tested: " + str(graph_count))
print("Amount of graphs not copied correctly: " + str(error_count))
print('')
if error_count > 0:
    print('TEST FAILED')
else:
    print('TEST PASSED')
print('')
