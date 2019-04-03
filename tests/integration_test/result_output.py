from tests.integration_test.settings import problem, write_to_csv
from input_output.sys_output import title
from input_output.file_output import create_csv_file, write_csv_line


def result_output(filename, n_graphs, processing_time, iso_result, iso_count_result):

    # Write beginning of console output
    title("-------------------------------")
    title("Results " + filename)
    title("-------------------------------")

    # Create new csv file
    if write_to_csv:
        if problem == 1:
            csv_filepath = create_csv_file(filename + "-isomorphism-problem-results")
            csv_column_names = ['graph1', 'graph2', 'are_isomorph result']
        if problem == 2:
            csv_filepath = create_csv_file(filename + "-count-isomorphism-problem-results")
            csv_column_names = ['graph1', 'graph2', 'are_isomorph result', 'amount_of_isomorphisms result']
        if problem == 3:
            csv_filepath = create_csv_file(filename + "-automorphism-problem-results")
            csv_column_names = ['graph1', 'amount_of_automorphisms result']
        # Write first row with column names
        write_csv_line(csv_filepath, csv_column_names)

    # Dependent on problem adapt the i loop
    if problem == 1 or problem == 2:
        i_loop = range(n_graphs - 1)
    elif problem == 3:
        i_loop = range(n_graphs)

    n_evaluations = 0
    for i in i_loop:
        # Dependent on problem adapt the j loop
        if problem == 1 or problem == 2:
            j_loop = range(i + 1, n_graphs)
        elif problem == 3:
            j_loop = [i]

        for j in j_loop:
            n_evaluations += 1

            # Retrieve results from data structures
            if problem == 1 or problem == 2:
                are_isomorph = [i, j] in iso_result
                if problem == 2:
                    if are_isomorph:
                        amount_isomorphisms = iso_count_result[i]
                    else:
                        amount_isomorphisms = 0
            if problem == 3:
                amount_automorphisms = iso_count_result[i]

            # Write results to csv file
            if write_to_csv:
                if problem == 1:
                    csv_line = [i, j, are_isomorph]
                if problem == 2:
                    csv_line = [i, j, are_isomorph, amount_isomorphisms]
                if problem == 3:
                    csv_line = [i, amount_automorphisms]
                write_csv_line(csv_filepath, csv_line)

            # Write results to console
            if problem == 1 or problem == 2:
                print("[" + str(i) + "," + str(j) + "] ", end='')
                if are_isomorph:
                    print("Graphs are isomorphic")
                else:
                    print("Graphs are not isomorphic")
                if problem == 2:
                    if are_isomorph:
                        print("      Amount of isomorphisms is " + str(amount_isomorphisms))
            if problem == 3:
                print("[" + str(i) + "] ", end='')
                print("Amount of automorphisms is " + str(amount_automorphisms))

    # Write summary to csv file
    if write_to_csv:
        write_csv_line(csv_filepath, ["Amount of combinations of graphs tested:", n_evaluations])
        write_csv_line(csv_filepath, ["Total processing time (s):", processing_time])

    # Write summary to console
    print("Amount of combinations of graphs evaluated: " + str(n_evaluations))
    print("Total processing time of " + filename + ": " + str(processing_time) + " s")
    print('')