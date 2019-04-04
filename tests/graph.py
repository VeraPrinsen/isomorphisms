from input_output.file_output import load_graph_list, write_csv_line, create_csv_file
from input_output.sys_output import passed, fail
from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement
from algorithms.preprocessing import fix_degrees


def test_copy(graph):
    """
    Tests the copy method of the graph
    :param graph: The graph to copy
    :return: Whether or not the graph is copied correctly
    """
    copy = graph.copy()
    return copy.is_equal(graph)


def test_complement(G: "Graph"):
    """
    Tests the complement method of the graph.
    :param G: The graph
    :return: Whether or not the complement is correctly
    """
    complement = G.complement()
    max_edges = (len(G.vertices) * (len(G.vertices) - 1)) / 2
    return len(complement.edges) + len(G.edges) == max_edges and test_incidence_complement(G, complement)


def test_incidence_complement(G: "Graph", complement: "Graph"):
    """
    Tests whether or not the incidences of the vertices in the graphs are completely different.
    :param G: The graph
    :param complement: The complement of the graph
    :return: Whether or not the incidences of the vertices are completely different
    """
    # Loop over both lists of vertices
    for v in G.vertices:
        for w in complement.vertices:
            if v.label == w.label:
                # If the labels of the vertices are the same (so they resemble the same vertex)
                for i in v.incidence:
                    if i in w.incidence:
                        return False
    return True


def unit_test(write_csv_any=False, write_stdout_passed=True, write_stdout_fail=True):
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
        filename = '/test_graphs/color_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)
        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                # Graph test
                total_tests += 1

                fix_degrees(graphs[i])
                fix_degrees(graphs[j])
                graph = graphs[i] + graphs[j]
                color_refinement(degree_color_initialization(graph))
                is_equal = test_copy(graph)
                is_correct_complement = test_complement(graph)
                if not is_equal:
                    error_count += 1
                    if write_stdout_fail:
                        print('---------------------------')
                        print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                        fail("Is NOT copy equal to graph: " + str(is_equal))
                    if write_csv_any:
                        write_csv_line(csv_filepath, [file, str(i), str(j), False, "{0:.3f}".format(0)])
                if not is_correct_complement:
                    error_count += 1
                    if write_stdout_fail:
                        print('---------------------------')
                        print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                        fail("Is complement constructed correctly: " + str(is_correct_complement))
                    if write_csv_any:
                        write_csv_line(csv_filepath, [file, str(i), str(j), False, "{0:.3f}".format(0)])
                else:
                    if write_stdout_passed:
                        print('---------------------------')
                        print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                        passed("Is copy equal to graph and complement constructed correctly: " + str(is_equal) + " and " + str(is_correct_complement))
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
