from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement
from input_output.file_output import load_graph_list, save_graph_as_dot, save_graph_in_png, create_csv_file, \
    write_csv_line
from algorithms.decide_gi import is_balanced_or_bijected
from input_output.sys_output import fail, passed
from time import time

"""
To test if the color_refinement works. This should be done by yourself by looking at the output graphs.
The test cases are those from the Solution Hints from Canvas.

Notation:
filename-0_1 = Graph of the disjoint union of Graph 0 and 1 of that file
"""


def unit_test():
    test_name = 'color_refinement'
    csv_filepath = create_csv_file(test_name)
    print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

    write_csv_line(csv_filepath, ['file', 'i', 'j', 'Pass?', 'Time (s)'])

    """
    SETTINGS OF TEST
    """
    # Enable this flag if you want to save png files of the final coloring of the disjoint union of the graph combinations
    save_png = True
    # Set this variable to true if you want to show passed test results
    show_passed_results = False

    """
    DO NOT CHANGE ANYTHING BELOW HERE
    """
    solution_isomorphisms = [
        {(1, 3), (0, 2)},
        {(0, 1), (2, 3), (4, 5)},
        {(0, 1)}
    ]

    error_count = 0
    total_tests = 0
    total_time = 0

    files = ['colorref_smallexample_4_7', 'colorref_smallexample_6_15', 'colorref_smallexample_2_49']
    for i_file in range(0, len(files)):
        file = files[i_file]
        filename = 'test_graphs/color_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)

        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                G = graphs[i] + graphs[j]

                start = time()
                color_refinement(degree_color_initialization(G))
                end = time()

                output_filename = file + '_' + str(i) + '_' + str(j)
                save_graph_as_dot(G, output_filename)

                #print('---------------------------')
                #print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                #print('---------------------------')
                csv_line = []

                if (i, j) in solution_isomorphisms[i_file]:
                    if not is_balanced_or_bijected(G)[0]:
                        remark = "[FAIL] Coloring of graph should be balanced, this is not the case."
                        fail(remark)
                        csv_line = [file, str(i), str(j), False, "{0:.3f}".format(end - start), "{0}".format(remark)]
                    elif show_passed_results:
                        remark = "Coloring of graph is balanced."
                        passed(remark)
                        csv_line = [file, str(i), str(j), True, "{0:.3f}".format(end-start), "{0}".format(remark)]
                else:
                    if is_balanced_or_bijected(G)[0]:
                        remark = "[FAIL] Coloring of graph should not be balanced, this is the case though."
                        fail(remark)
                        csv_line = [file, str(i), str(j), False, "{0:.3f}".format(end - start), "{0}".format(remark)]
                    elif show_passed_results:
                        remark = "Coloring of graph is not balanced."
                        passed(remark)
                        csv_line = [file, str(i), str(j), True, "{0:.3f}".format(end-start), "{0}".format(remark)]

                write_csv_line(csv_filepath, csv_line)
                total_time += end - start
                total_tests += 1

                #print("Processing time: " + str(round((end-start), 3)) + " ms")

                #print('')

        if save_png:
            for i in range(0, len(graphs) - 1):
                for j in range(i + 1, len(graphs)):
                    output_filename = file + '_' + str(i) + '_' + str(j)
                    save_graph_in_png(output_filename)

    return determine_test_outcome(csv_filepath, error_count, test_name, total_tests, total_time)


def determine_test_outcome(csv_filepath, error_count, test_name, total_tests, total_time):
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
    write_csv_line(csv_filepath, ['', '', '', ''])
    write_csv_line(csv_filepath, ['#Tests', '#Fail', 'PASS?', 'Time (s)'])
    write_csv_line(csv_filepath, [str(total_tests), str(error_count), str(test_pass_bool),
                                  "{0:.3f}".format(total_time)])
    print('</' + test_name + '>')
    return test_pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
