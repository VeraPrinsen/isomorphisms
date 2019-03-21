import time

from input_output.file_output import load_graph_list, create_csv_file, write_csv_line
from input_output.sys_output import fail
from input_output.sys_output import passed
from supporting_components.graph_io import *
from algorithms.decide_gi import is_balanced_or_bijected
from algorithms.color_initialization import degree_color_initialization
import tests.fun_provider as fun_provider


class DecideGi:

    def unittest(self):
        # Swap in the color refinement object Default_color_refinement().
        # This object has .color_refine(), which is what this function expects for color refinement during test.
        return _test_decide_gi(test_name='decide_gi_unit', color_refine_object=fun_provider.Default_color_refinement())

    # Create a function for the object to be called externally
    def run_color_refinement(self, color_refine_object: "Default_color_refinement"):
        return _test_decide_gi(test_name='decide_gi_CR', color_refine_object=color_refine_object)

    def run_fast_color_refinement(self, color_refine_object: "Fast_color_refinement"):
        # Need to implement
        return _test_decide_gi(test_name='decide_gi_FCR', color_refine_object = color_refine_object)


def _test_balanced_or_bijected(graph: 'Graph', is_balanced: 'Bool', is_bijected: 'Bool'):
    """
    Tests the is_balanced_or_bijected method of decide_gi.py against expected answers for is_balanced and is_bijected
    :param graph: The graph to test
    :param is_balanced: the expected answer for is_balanced
    :param is_bijected: the expected answer for is_bijected
    :return: 'Bool' test passes == True, test fails == False
    """
    test_is_balanced, test_is_bijected = is_balanced_or_bijected(graph)

    if not (test_is_balanced == is_balanced and test_is_bijected == is_bijected):
        raise ValueError('LOGGING: ' +
                         'is_balanced was: {} ({})... '.format(test_is_balanced, is_balanced) +
                         'is_bijected was: {} ({})...'.format(test_is_bijected, is_bijected)
                         )
    else:
        return True


def _test_decide_gi(test_name, color_refine_object: "Object"):
    csv_filepath = create_csv_file(test_name)
    print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

    write_csv_line(csv_filepath, ['file', 'j', 'i', 'Pass?', 'Time (s)'])

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

    expected_results = dict()
    expected_results['colorref_smallexample_2_49'] = {0: {1: (True, True)}}
    expected_results['colorref_smallexample_4_7'] = {0: {1: (False, False), 2: (True, False), 3: (False, False)},
                                                     1: {2: (False, False), 3: (True, True)},
                                                     2: {3: (False, False)}
                                                     }
    expected_results['colorref_smallexample_6_15'] = {
        0: {1: (True, True), 2: (False, False), 3: (False, False), 4: (False, False), 5: (False, False)},
        1: {2: (False, False), 3: (False, False), 4: (False, False), 5: (False, False)},
        2: {3: (True, True), 4: (False, False), 5: (False, False)},
        3: {4: (False, False), 5: (False, False)},
        4: {5: (True, False)}
        }

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
    total_time = 0

    for file in files:
        filename = 'test_graphs/color_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)

        for i in range(0, len(graphs)):
            for j in range(0, i):
                t0 = time.time()
                graph_count += 1

                # Create disjoint union
                graph = graphs[i] + graphs[j]

                # Color refinement with degree coloring initialization
                color_refine_object.color_refine(degree_color_initialization(graph))

                # Try catch for test_balanced_or_bijected raises ValueError
                try:
                    is_balanced_or_bijected_test_result = _test_balanced_or_bijected(graph, expected_results[file][j][i][0], expected_results[file][j][i][1])

                    t1 = time.time() - t0
                    pass_line = [file, str(j), str(i), str(is_balanced_or_bijected_test_result), "{0:.3f}".format(t1)]
                    write_csv_line(csv_filepath, pass_line)

                except ValueError as err:
                    error_count += 1

                    t1 = time.time() - t0
                    fail_line = [file, str(j), str(i), False, "{0:.3f}".format(t1), "{0}".format(err)]
                    write_csv_line(csv_filepath, fail_line)
                    print(*fail_line, sep='\t', end='')
                    fail('! Error #'+str(error_count))

                total_time += t1


    # Determine test outcome
    test_pass_bool = False
    if error_count == 0 and total_tests == graph_count:
        test_pass_bool = True
        passed(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestfile:\n{0}/{1}\t{2}\t\t{3}\t{4}\t{5}'.format(str(graph_count),
                                                                    str(total_tests), str(error_count),
                                                                    str(test_pass_bool), "{0:.3f}".format(total_time),
                                                                                             test_name)
            )
    else:
        fail(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestfile:\n{0}/{1}\t{2}\t\t{3}\t{4}\t{5}'.format(str(graph_count),
                                                                    str(total_tests), str(error_count),
                                                                    str(test_pass_bool), "{0:.3f}".format(total_time),
                                                                                             test_name)
            )

    # Test summary
    write_csv_line(csv_filepath, ['', '', '', ''])
    write_csv_line(csv_filepath, ['#Tests', '#Fail', 'PASS?', 'Time (s)'])
    write_csv_line(csv_filepath, [str(graph_count) + "/" + str(total_tests), str(error_count), str(test_pass_bool), "{0:.3f}".format(total_time)])

    print('</' + test_name + '>')
    return test_pass_bool
