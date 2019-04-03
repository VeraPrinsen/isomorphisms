from tests.integration_test.solutions import solution
from tests.integration_test.settings import problem, console_pass, write_to_csv
from tests.integration_test.result_output import result_output
from input_output.sys_output import fail, passed, title
from input_output.file_output import create_csv_file, write_csv_line


def test_output(filename, n_graphs, processing_time, isomorphisms, iso_count):
    solution_map = solution[filename]

    if not bool(solution_map):
        result_output(filename, n_graphs, processing_time, isomorphisms, iso_count)
        return

    title("-------------------------------")
    title("Test results " + filename)
    title("-------------------------------")

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

    n_test_graphs = 0
    n_total_graphs = 0
    error_count = 0
    for i in range(n_graphs-1):
        # Dependent on problem adapt the j loop
        if problem == 1 or problem == 2:
            j_loop = range(i + 1, n_graphs)
        elif problem == 3:
            j_loop = [i]

        for j in j_loop:
            n_total_graphs += 1
            test_failed = False

            if problem == 1 or problem == 2:
                print("[" + str(i) + "," + str(j) + "] ", end='')
            if problem == 3:
                print("Graph " + str(i))

            if bool(solution_map):
                n_test_graphs += 1

                # Retrieve expected and test values
                if problem == 1 or problem == 2:
                    are_isomorph_expected = (i, j) in solution_map
                    are_isomorph_test = [i, j] in isomorphisms
                    are_isomorph_passed = are_isomorph_expected == are_isomorph_test

                    if problem == 2:
                        if are_isomorph_test:
                            amount_isomorph_test = iso_count[i]
                        else:
                            amount_isomorph_test = 0
                        if are_isomorph_expected:
                            amount_isomorph_expected = solution_map[(i, j)]
                        else:
                            amount_isomorph_expected = 0
                        amount_isomorph_passed = amount_isomorph_expected == amount_isomorph_test

                if problem == 3:
                    amount_automorph_expected = solution_map[i]
                    amount_automorph_test = iso_count[i]
                    amount_automorph_passes = amount_automorph_expected == amount_automorph_test

                if write_to_csv:
                    if problem == 1:
                        csv_line = [i, j, are_isomorph_expected, are_isomorph_test, are_isomorph_passed]
                    if problem == 2:
                        csv_line = [i, j, are_isomorph_expected, are_isomorph_test, are_isomorph_passed,
                                    amount_isomorph_expected, amount_isomorph_test, amount_isomorph_passed]
                    if problem == 3:
                        csv_line = [i, amount_automorph_expected, amount_automorph_test, amount_automorph_passes]
                    write_csv_line(csv_filepath, csv_line)

                # Check if solution is correct for GI problem 1 and 2) Isomorphisms between two different graphs
                if problem == 1 or problem == 2:
                    if are_isomorph_expected:
                        if not are_isomorph_test:
                            fail("[FAIL] Graphs are isomorphic, are_isomorph() did not detect this")
                            test_failed = True
                        else:
                            if console_pass:
                                passed("[PASS] Graphs are isomorphic")
                            if problem == 2:
                                if amount_isomorph_expected != amount_isomorph_test:
                                    fail("[      FAIL] Amount of isomorphisms should be " + str(amount_isomorph_expected) + " not " + str(amount_isomorph_test))
                                    test_failed = True
                                else:
                                    if console_pass:
                                        passed("      [PASS] Amount of isomorphisms is " + str(amount_isomorph_expected))
                    else:
                        if are_isomorph_expected:
                            fail("[FAIL] Graphs are not isomorphic, are_isomorph() detected they were")
                            test_failed = True
                        else:
                            if console_pass:
                                passed("[PASS] Graphs are not isomorphic")

                # Check if solution is correct for GI problem 3) Amount of automorphisms of one graph
                if problem == 3:
                    if amount_automorph_expected != amount_automorph_test:
                        fail("[FAIL] Amount of automorphisms should be " + str(amount_automorph_expected) + " not " + str(amount_automorph_test))
                        test_failed = True
                    else:
                        if console_pass:
                            passed("[PASS] Amount of automorphisms is " + str(amount_automorph_expected))

                if test_failed:
                    error_count += 1

            else:
                print("no solutions")
                # JUST PRINT RESULTS, TAKE INTO ACCOUNT THAT MORE THAN 2 GRAPHS CAN BE ISOMORPHIC

    if write_to_csv:
        write_csv_line(csv_filepath, ["Total processing time (s):", processing_time])

    print("Total processing time of " + filename + ": " + str(processing_time) + " s")