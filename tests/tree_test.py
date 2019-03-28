from input_output.file_output import load_graph_list, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
from algorithms.tree_isomorphisms import trees_are_isomorph, trees_count_isomorphisms
from time import time


def unit_test(create_csv, console_fail, console_pass):
    if create_csv:
        test_name = "isomorphisms_trees"
        csv_filepath = create_csv_file(test_name)
        print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')
        write_csv_line(csv_filepath, ['file', 'i', 'j', 'are_isomorph passed?', 'amount_of_isomorphisms passed?', 'Time (s)'])

    # TEST FILE
    files = ["bigtrees1.grl", "bigtrees3.grl"]
    location = "/test_graphs/individualization_refinement/"
    solution = [
        {(0, 2): 442368, (1, 3): 5308416},
        {(0, 2): 2772351862699137701073289910157312, (1, 3): 462058643783189616845548318359552}
    ]

    error_count = 0
    total_tests = 0
    total_time = 0
    for i_file in range(0, len(files)):
        file = files[i_file]
        filename = location + file
        graphs = load_graph_list(filename)

        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                T1 = graphs[i]
                T2 = graphs[j]

                start_are_isomorph = time()
                are_isomorph_actual, amount_of_isomorphisms_actual = trees_count_isomorphisms(T1, T2)
                end_are_isomorph = time()

                if console_fail or console_pass:
                    print('---------------------------')
                    print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
                    print('---------------------------')

                are_isomorph_expected = (i, j) in solution[i_file]
                if are_isomorph_expected:
                    amount_of_isomorphisms_expected = solution[i_file][(i, j)]
                if are_isomorph_expected:
                    if not are_isomorph_actual:
                        if console_fail:
                            remark = "[FAIL] Trees should be isomorphic, trees_are_isomorph() did not detect this."
                            fail(remark)
                            error_count += 1
                    elif console_pass:
                        remark = "Trees are isomorphic."
                        passed(remark)

                    if amount_of_isomorphisms_actual != amount_of_isomorphisms_expected:
                        if console_fail:
                            remark = "[FAIL] Amount of isomorphisms should be " + str(amount_of_isomorphisms_expected) + ", not " + str(amount_of_isomorphisms_actual)
                            fail(remark)
                            error_count += 1
                    else:
                        if console_pass:
                            passed("Amount of isomorphisms is: " + str(amount_of_isomorphisms_actual))

                else:
                    if are_isomorph_actual:
                        if console_fail:
                            remark = "[FAIL] Trees are not isomorphic, trees_are_isomorphic() did detect it to be isomorphic though."
                            fail(remark)
                            error_count += 1
                    elif console_pass:
                        remark = "Trees are not isomorphic."
                        passed(remark)

                if console_pass or console_fail:
                    print("Processing time trees_are_isomorph:", round(end_are_isomorph - start_are_isomorph, 3), 's')
                    print("")

                total_time += end_are_isomorph - start_are_isomorph
                total_tests += 1

                if create_csv:
                    line = [file, str(i), str(j), are_isomorph_expected == are_isomorph_actual, False, "{0:.3f}".format(end_are_isomorph - start_are_isomorph)]
                    write_csv_line(csv_filepath, line)

    determine_test_outcome(csv_filepath, error_count, test_name, total_tests, total_time)


def determine_test_outcome(csv_filepath, error_count, test_name, total_tests, total_time):
    # Determine test outcome
    test_pass_bool = False
    print("")
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
    unit_test(True, True, True)

