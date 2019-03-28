from input_output.file_output import load_graph_list, write_csv_line, create_csv_file
from input_output.sys_output import passed, fail
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


def unit_test(write_csv_any=True, write_stdout_passed=True, write_stdout_fail=True):
    test_name = 'graph'
    if write_csv_any:
        csv_filepath = create_csv_file(test_name)
        print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

        write_csv_line(csv_filepath, ['file', 'i', 'j', 'Pass?', 'Time (s)'])
    else:
        print('<' + test_name + '> ')

    files = ['colorref_smallexample_4_7', 'colorref_smallexample_6_15', 'colorref_smallexample_2_49']

    # Test observables
    error_count = 0
    total_tests = 0
    total_time = 0  # No time keeping

    # Test loop
    for file in files:
        filename = 'test_graphs/color_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)
        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                # Graph test
                total_tests += 1
                graph = graphs[i] + graphs[j]
                color_refinement(degree_color_initialization(graph))
                is_equal = test_copy(graph)
                if not is_equal:
                    error_count += 1
                    if write_stdout_fail:
                        fail('---------------------------')
                        fail("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                        fail("Is NOT copy equal to graph: " + str(is_equal))
                    if write_csv_any:
                        write_csv_line(csv_filepath, [file, str(i), str(j), False, "{0:.3f}".format(0)])
                else:
                    if write_stdout_passed:
                        passed('---------------------------')
                        passed("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                        passed("Is copy equal to graph: " + str(is_equal))
                    if write_csv_any:
                        write_csv_line(csv_filepath, [file, str(i), str(j), True, "{0:.3f}".format(0)])

    # Determine test outcome
    test_pass_bool = False
    if error_count == 0:
        test_pass_bool = True
        passed(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestname:\n{0}\t\t{1}\t\t{2}\t{3}\t{4}'.format(
                str(total_tests),
                str(error_count),
                str(test_pass_bool),
                "{0:.3f}".format(
                    total_time),
                test_name)
        )
    else:
        fail(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestname:\n{0}\t\t{1}\t\t{2}\t{3}\t{4}'.format(
                str(total_tests),
                str(error_count),
                str(test_pass_bool),
                "{0:.3f}".format(
                    total_time),
                test_name)
        )
    # Test summary
    if write_csv_any:
        write_csv_line(csv_filepath, ['', '', '', ''])
        write_csv_line(csv_filepath, ['#Tests', '#Fail', 'PASS?', 'Time (s)'])
        write_csv_line(csv_filepath, [str(total_tests), str(error_count), str(test_pass_bool),
                                      "{0:.3f}".format(total_time)])
    print('</' + test_name + '>')
    return test_pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
