from input_output.file_output import load_graph_list, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
from algorithms.tree_algorithm import trees_count_isomorphisms
from algorithms.preprocessing import fix_degrees
from time import time


"""
To test if the tree_algorithm works finding and counting isomorphisms of trees.
"""


def unit_test(write_csv_any=False, write_stdout_passed=True, write_stdout_fail=True):
    test_name = 'tree_algorithm'
    if write_csv_any:
        csv_filepath = create_csv_file(test_name)
        print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

        write_csv_line(csv_filepath, ['file', 'i', 'j', 'Pass?', 'Are isomorph Time (s)', 'Amount isomorph Time (s)'])
    else:
        print('<' + test_name + '> ')

    # TEST FILE
    files = ["bigtrees1", "bigtrees3"]
    solution = [
        {(0, 2): 442368, (1, 3): 5308416},
        {(0, 2): 2772351862699137701073289910157312, (1, 3): 462058643783189616845548318359552}
    ]

    # Test observables
    error_count = 0
    total_tests = 0
    total_time = 0

    # For every file that needs to be evaluated, all combinations of graphs within that file are evaluated.
    for i_file in range(len(files)):
        file = files[i_file]
        filename = '/test_graphs/individualization_refinement/' + file + '.grl'
        graphs = load_graph_list(filename)

        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                # Graph test
                total_tests += 1
                T1 = graphs[i]
                T2 = graphs[j]

                fix_degrees(T1)
                fix_degrees(T2)

                start_isomorph = time()
                are_isomorph_actual = trees_count_isomorphisms(T1, T2, False)
                end_isomorph = time()

                start_amount_isomorphisms = time()
                amount_of_isomorphisms_actual = trees_count_isomorphisms(T1, T2, True)
                end_amount_isomorphisms = time()

                filestr = file + "-" + str(i) + "_" + str(j) + '\t->\t' + 'are_isomorph: ' + "{0:.3f}".format(end_isomorph - start_isomorph) + 's, amount_of_isomorphisms: ' + "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms) + 's '+ '\t'

                error_adder = 0
                are_isomorph_expected = (i, j) in solution[i_file]
                if are_isomorph_expected:
                    amount_of_isomorphisms_expected = solution[i_file][(i, j)]
                else:
                    amount_of_isomorphisms_expected = 0
                if are_isomorph_expected:
                    if not are_isomorph_actual:
                        remark = "[FAIL] Trees should be isomorphic, trees_are_isomorph() did not detect this."
                        if write_stdout_fail:
                            print('')
                            fail(filestr + remark)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_adder = 1
                    else:
                        remark = "[PASS] Trees are isomorphic."
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            print('')
                            passed(filestr + remark)

                    if amount_of_isomorphisms_actual != amount_of_isomorphisms_expected:
                        remark = "[FAIL] Amount of isomorphisms should be " + str(amount_of_isomorphisms_expected) + ", not " + str(amount_of_isomorphisms_actual)
                        if write_stdout_fail:
                            fail(filestr + remark)
                            print('')

                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_adder = 1
                    else:
                        remark = "[PASS] Amount of isomorphisms is: " + str(amount_of_isomorphisms_actual)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            passed(filestr + remark)
                            print('')
                else:
                    if are_isomorph_actual:
                        remark = "[FAIL] Trees are not isomorphic, trees_are_isomorphic() did detect it to be isomorphic though."
                        if write_stdout_fail:
                            fail(filestr + remark)
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), False,
                                               "{0:.3f}".format(end_isomorph - start_isomorph), "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        error_adder = 1
                    else:
                        remark = "[PASS] Trees are not isomorphic."
                        if write_csv_any:
                            write_csv_line(
                                csv_filepath, [file, str(i), str(j), True,
                                               "{0:.3f}".format(end_isomorph - start_isomorph),
                                               "{0:.3f}".format(end_amount_isomorphisms - start_amount_isomorphisms),
                                               "{0}".format(remark)]
                            )
                        if write_stdout_passed:
                            passed(filestr + remark)

                error_count += error_adder
                total_time += (end_isomorph - start_isomorph) + (end_amount_isomorphisms - start_amount_isomorphisms)

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
