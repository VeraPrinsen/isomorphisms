from tests.integration_test.solutions import isomorphism_solution, automorphism_solution
from tests.integration_test.settings import problem, console_pass, write_to_csv
from tests.integration_test.result_output import result_output
from input_output.sys_output import fail, passed, title
from input_output.file_output import create_csv_file, write_csv_line


def test_output(filename, n_graphs, processing_time, iso_test_result, iso_count_test_result):
    # Get results from solution file
    iso_solution = []
    count_solution = {}
    if filename in isomorphism_solution:
        iso_solution = isomorphism_solution[filename]
    if filename in automorphism_solution:
        count_solution = automorphism_solution[filename]

    # Dependent on the solutions that are available, print test results or not
    solution_exists = True
    if problem == 1:
        if not bool(iso_solution):
            solution_exists = False
    if problem == 2:
        if not bool(iso_solution) and not bool(count_solution):
            solution_exists = False
    if problem == 3:
        if not bool(count_solution):
            solution_exists = False

    if not solution_exists:
        result_output(filename, n_graphs, processing_time, iso_test_result, iso_count_test_result)
        return 0

    # If the right solutions are available, compare expected and tested values
    title("-------------------------------")
    title("Test results " + filename)
    title("-------------------------------")

    # When writing result to csv file, the file with corresponding column names is created here
    if write_to_csv:
        if problem == 1:
            csv_filepath = create_csv_file(filename + "-isomorphism-problem-test")
            csv_column_names = ['graph1', 'graph2',
                                'are_isomorph expected result', 'are_isomorph actual result', 'passed']
        if problem == 2:
            csv_filepath = create_csv_file(filename + "-count-isomorphism-problem-test")
            csv_column_names = ['graph1', 'graph2',
                                'are_isomorph expected result', 'are_isomorph actual result', 'passed',
                                'amount_of_isomorphisms expected result', 'amount_of_isomorphisms actual result', 'passed']
        if problem == 3:
            csv_filepath = create_csv_file(filename + "-automorphism-problem-test")
            csv_column_names = ['graph1',
                                'amount_of_automorphisms expected result', 'amount_of_automorphisms actual result', 'passed']
        # Write first row with column names
        write_csv_line(csv_filepath, csv_column_names)

    # For each (combination of) graph(s) the results are compared
    # Amount of graphs tested and amount of tests failed are saved
    n_test_graphs = 0
    error_count = 0

    # Dependent on problem adapt the i loop
    if problem == 1 or problem == 2:
        i_loop = range(n_graphs - 1)
    elif problem == 3:
        i_loop = range(n_graphs)

    for i in i_loop:
        # Dependent on problem adapt the j loop
        if problem == 1 or problem == 2:
            j_loop = range(i + 1, n_graphs)
        elif problem == 3:
            j_loop = [i]

        for j in j_loop:
            n_test_graphs += 1
            test_failed = False

            # Retrieve expected and test values
            if problem == 1 or problem == 2:
                are_isomorph_expected = False
                are_isomorph_test = False
                for pair in iso_solution:
                    if i in pair and j in pair:
                        are_isomorph_expected = True
                for pair in iso_test_result:
                    if i in pair and j in pair:
                        are_isomorph_test = True
                are_isomorph_passed = are_isomorph_expected == are_isomorph_test

                if problem == 2:
                    if are_isomorph_expected:
                        amount_isomorph_expected = count_solution[i]
                    else:
                        amount_isomorph_expected = 0
                    if are_isomorph_test:
                        amount_isomorph_test = iso_count_test_result[i]
                    else:
                        amount_isomorph_test = 0
                    amount_isomorph_passed = amount_isomorph_expected == amount_isomorph_test

            if problem == 3:
                amount_automorph_expected = count_solution[i]
                amount_automorph_test = iso_count_test_result[i]
                amount_automorph_passes = amount_automorph_expected == amount_automorph_test

            # When writing to csv, dependent on the problem to be solved, a line of results is written here
            if write_to_csv:
                if problem == 1:
                    csv_line = [i, j, are_isomorph_expected, are_isomorph_test, are_isomorph_passed]
                if problem == 2:
                    csv_line = [i, j, are_isomorph_expected, are_isomorph_test, are_isomorph_passed,
                                amount_isomorph_expected, amount_isomorph_test, amount_isomorph_passed]
                if problem == 3:
                    csv_line = [i, amount_automorph_expected, amount_automorph_test, amount_automorph_passes]
                write_csv_line(csv_filepath, csv_line)

            # Write on console the results of the GI problem 1 and 2: isomorphisms between two different graphs
            if problem == 1 or problem == 2:
                print("[" + str(i) + "," + str(j) + "] ", end='')
                if are_isomorph_expected:
                    if are_isomorph_passed:
                        if console_pass:
                            passed("[PASS] Graphs are isomorphic")
                        if problem == 2:
                            if amount_isomorph_passed:
                                if console_pass:
                                    passed("      [PASS] Amount of isomorphisms is " + str(amount_isomorph_expected))
                            else:
                                fail("      [FAIL] Amount of isomorphisms should be " + str(
                                    amount_isomorph_expected) + " not " + str(amount_isomorph_test))
                                test_failed = True
                    else:
                        fail("[FAIL] Graphs are isomorphic, are_isomorph() did not detect this")
                        test_failed = True
                else:
                    if are_isomorph_passed:
                        if console_pass:
                            passed("[PASS] Graphs are not isomorphic")
                    else:
                        fail("[FAIL] Graphs are not isomorphic, are_isomorph() detected they were")
                        test_failed = True

            # Write on console the results of the GI problem 3) Amount of automorphisms of one graph
            if problem == 3:
                print("[" + str(i) + "] ", end='')
                if amount_automorph_passes:
                    if console_pass:
                        passed("[PASS] Amount of automorphisms is " + str(amount_automorph_expected))
                else:
                    fail("[FAIL] Amount of automorphisms should be " + str(amount_automorph_expected) + " not " + str(
                        amount_automorph_test))
                    test_failed = True

            # If test failed at one of the test cases, increase error_count
            if test_failed:
                error_count += 1

    # Write summary of the test in csv file
    if write_to_csv:
        write_csv_line(csv_filepath, ["Amount of combinations of graphs tested:", n_test_graphs])
        if error_count > 0:
            write_csv_line(csv_filepath, ["Amount of tests failed:", error_count, "TEST FAILED"])
        else:
            write_csv_line(csv_filepath, ["Amount of tests failed:", error_count, "TEST PASSED"])
        write_csv_line(csv_filepath, ["Total processing time (s):", round(processing_time, 3)])

    # Print summary of the test to console
    print("Amount of combinations of graphs tested: " + str(n_test_graphs))
    print("Amount of tested graphs with failed results: " + str(error_count))
    print('')
    if error_count > 0:
        fail('TEST FAILED')
    else:
        passed('TEST PASSED')
    print('')
    print("Total processing time of " + filename + ": " + str(round(processing_time, 3)) + " s")
    print('')

    return error_count