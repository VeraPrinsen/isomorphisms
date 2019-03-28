from input_output.file_output import load_graph_list, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
from algorithms.branching import count_isomorphisms
from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement
from time import time


"""
To test if the branching algorithm works finding isomorphisms between two graphs.
If a test fails, a red [FAIL] print statement is shown in the terminal.
Furthermore, the processing time per file is mentioned in the terminal.

Notation:
filename-0_1 = Graph of the disjoint union of Graph 0 and 1 of that file
"""


def unit_test(write_csv_any=True, write_stdout_passed=True, write_stdout_fail=True):
    test_name = 'isomorphism_problem'
    if write_csv_any:
        csv_filepath = create_csv_file(test_name)
        print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

        write_csv_line(csv_filepath, ['file', 'i', 'j', 'Pass?', 'Are isomorph Time (s)', 'Amount isomorph Time (s)'])
    else:
        print('<' + test_name + '> ')

    """
    SETTING OF TEST
    """

    # Change here which files you want to evaluate
    torus24 = True
    trees90 = False
    products72 = False
    cographs1 = False
    bigtrees1 = False
    torus144 = False
    trees36 = False
    modulesC = False
    cubes5 = False
    bigtrees3 = False
    cubes6 = False

    """
    DO NOT CHANGE ANYTHING BELOW HERE
    """
    # Only files that needs to be evaluated are added to the list.
    i_files = []
    torus24 and i_files.append(0)
    trees90 and i_files.append(1)
    products72 and i_files.append(2)
    cographs1 and i_files.append(3)
    bigtrees1 and i_files.append(4)
    torus144 and i_files.append(5)
    trees36 and i_files.append(6)
    modulesC and i_files.append(7)
    cubes5 and i_files.append(8)
    bigtrees3 and i_files.append(9)
    cubes6 and i_files.append(10)

    files = [
        'torus24',
        'trees90',
        'products72',
        'cographs1',
        'bigtrees1',
        'torus144',
        'trees36',
        'modulesC',
        'cubes5',
        'bigtrees3',
        'cubes6'
    ]

    # Solutions given on Canvas per file
    solution_isomorphisms = [
        {(0, 3): 96, (1, 2): 96},
        {(0, 3): 6912, (1, 2): 20736},
        {(0, 6): 288, (1, 5): 576, (2, 3): 576, (4, 7): 864},
        {(0, 3): 5971968, (1, 2): 995328},
        {(0, 2): 442368, (1, 3): 5308416},
        {(0, 6): 576, (1, 7): 576, (2, 4): 576, (3, 10): 576, (5, 9): 1152, (8, 11): 576},
        {(0, 7): 2, (1, 4): 6, (2, 6): 2, (3, 5): 6},
        {(0, 7): 17915904, (1, 5): 17915904, (2, 4): 2488320, (3, 6): 2985984},
        {(0, 1): 3840, (2, 3): 24},
        {(0, 2): 2772351862699137701073289910157312, (1, 3): 462058643783189616845548318359552},
        {(0, 1): 96, (2, 3): 46080}
    ]

    # Test observables
    error_count = 0
    total_tests = 0
    total_time = 0

    # For every file that needs to be evaluated, all combinations of graphs within that file are evaluated.
    for i_file in i_files:
        file = files[i_file]
        filename = 'test_graphs/individualization_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)
        solution_map = solution_isomorphisms[i_file]

        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                # Graph test
                total_tests += 1
                G = graphs[i]
                H = graphs[j]

                start_isomorph = time()
                boolean_isomorph = are_isomorph(G, H)
                end_isomorph = time()

                start_amount_isomorphisms = time()
                n_isomorphisms = amount_of_isomorphisms(G, H)
                end_amount_isomorphisms = time()

                filestr = '-> are_isomorph: ' + "{0:.3f}".format(end_isomorph - start_isomorph) + 's, amount_of_isomorphisms: ' + "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms) + ' s ' + file + "-" + str(i) + "_" + str(j)

                if (i, j) in solution_map:
                    if not boolean_isomorph:
                        remark = "[FAIL] Graphs are isomorph, is_isomorph(G, H) did not detect it"
                        if write_stdout_fail:
                            fail(filestr + remark)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_count += 1
                    else:
                        remark = "[PASS] Graphs are isomorph"
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            passed(filestr + remark)

                    if n_isomorphisms != solution_map[(i, j)]:
                        remark = "[FAIL] Amount of isomorphisms should be " + str(solution_map[(i, j)]) + ", not " + str(n_isomorphisms)
                        if write_stdout_fail:
                            fail(filestr + remark)

                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_count += 1
                    else:
                        remark = "[PASS] Amount of isomorphisms is: " + str(n_isomorphisms)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            passed(filestr + remark)
                else:
                    if boolean_isomorph:
                        remark = "[FAIL] Graphs are not isomorph, is_isomorph determined they were"
                        if write_stdout_fail:
                            fail(filestr + remark)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_count += 1
                    else:
                        remark = "[PASS] Graphs are not isomorph"
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            passed(filestr + remark)

                total_time += (end_isomorph - start_isomorph) + (end_amount_isomorphisms - start_amount_isomorphisms)
                if write_stdout_passed:
                    print("Processing time is_isomorph(G, H): " + str(round((end_isomorph - start_isomorph) * 1000, 3)) + " ms")
                    print("Processing time amount_of_isomorphisms(G, H): " + str(round((end_amount_isomorphisms - start_amount_isomorphisms) * 1000, 3)) + " ms")
                    print('')

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
