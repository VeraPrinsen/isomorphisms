from supporting_components.graph_io import *
from algorithms.decide_gi import is_balanced_or_bijected
from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement

# Expected test results
total_tests = 22

files = ['colorref_smallexample_2_49', 'colorref_smallexample_4_7', 'colorref_smallexample_6_15']

# Dictionary containing expected outcomes.
# Sourced from canvas.utwente.nl
# Structure:
# The dictionary is keyed on filename (str)
# This dictionary contains for each key:
#   A dictionary keyed on graph no. (int)
#   This dictionary contains:
#       A dictionary container on graph no. (int)
#       This dictionary contains:
#           Tuple containing : (is_balanced, is_bijected) ((bool, bool))

expected_results = {}
expected_results['colorref_smallexample_2_49'] = {0:
                                                      {1: (True, True)}
                                                  }
expected_results['colorref_smallexample_4_7'] = {0:
                                                      {1: (False, False), 2: (True, False), 3: (False, False)},
                                                 1:
                                                     {2: (False, False), 3: (True, True)},
                                                 2:
                                                     {3: (False, False)}

                                                 }
expected_results['colorref_smallexample_6_15'] = {0:
                                                      {1: (True, True), 2: (False, False), 3: (False, False), 4: (False, False), 5: (False, False)},
                                                  1:
                                                      {2: (False, False), 3: (False, False), 4: (False, False), 5: (False, False)},
                                                  2:
                                                      {3: (True, True), 4: (False, False), 5: (False, False)},
                                                  3:
                                                      {4: (False, False), 5: (False, False)},
                                                  4:
                                                      {5: (True, False)},
                                                 }

def test_balanced_or_bijected(graph: 'Graph', is_balanced: bool, is_bijected: bool):
    """
    Tests the is_balanced_or_bijected method of decide_gi.py agains expected answers for is_balanced and is_bijected
    :param graph: The graph to test
    :param is_balanced: the expected answer for is_balanced
    :param is_bijected: the expected answer for is_bijected
    :return: bool test passes == True, test fails == False
    """
    test_is_balanced, test_is_bijected = is_balanced_or_bijected(graph)

    if not (test_is_balanced == is_balanced and test_is_bijected == is_bijected):
        print('DEBUG...')
        print('Should be  : {}, {}'.format(is_balanced, is_bijected))
        print('Calculated : {}, {}'.format(test_is_balanced, test_is_bijected))
    return test_is_balanced == is_balanced and test_is_bijected == is_bijected


# Testing loop
# A disjoint union is coloured using color_refinement(degree_color_initialization(graph))
# The method is_balanced_or_bijected is tested against a hardcoded dictionary containing the expected outcomes.
#
# Currently the following graph files are tested:
#     - colorref_smallexample_2_49
#     - colorref_smallexample_4_7
#     - colorref_smallexample_6_15

error_count = 0
graph_count = 0
for file in files:
    filename = '../test_graphs/color_refinement/' + file + '.grl'
    with open(filename) as f:
        L = load_graph(f, read_list=True)
        for i in range(0, len(L[0])):
            for j in range(0 , i):
                graph_count += 1
                graph = L[0][i] + L[0][j]
                color_refinement(degree_color_initialization(graph))
                is_balanced_or_bijected_test_result = test_balanced_or_bijected(graph, expected_results[file][j][i][0], expected_results[file][j][i][1])
                if not is_balanced_or_bijected_test_result:
                    error_count += 1
                    print('---------------------------')
                    print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                    print('---------------------------')
                    print("Is calculated is_balanced_or_bijected correctly: " + str(is_balanced_or_bijected_test_result))
                    print('')
print('---------------------------')
print("Statistics of test is_balanced_or_bijected:")
print('---------------------------')
print("Amount of graphs tested: " + str(graph_count) + "/" + str(total_tests))
print("Amount of graphs failed: " + str(error_count))
print('')
if error_count > 0:
    print('TEST FAILED')
else:
    print('TEST PASSED')
print('')
