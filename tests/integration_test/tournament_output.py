from tests.integration_test.settings import problem, write_to_csv
from input_output.sys_output import title
from input_output.file_output import create_csv_file, write_csv_line


def tournament_output(filename, total_time, isomorphisms, iso_count):
    """
    CONSOLE OUTPUT
    """
    print("-------------------------------")
    print("Results " + filename)
    print("-------------------------------")
    if problem == 1:
        title("Sets of isomorphic graphs:")
    elif problem == 2:
        title("Sets of isomorphic graphs:   Number of isomorphisms:")
    elif problem == 3:
        title("Graph:   Number of automorphisms:")

    if problem == 1 or problem == 2:
        for pair in isomorphisms:
            if problem == 1:
                print(str(pair))
            elif problem == 2:
                print(str(pair) + "                       " + str(iso_count[pair[0]]))
    elif problem == 3:
        for g in sorted(iso_count):
            print(str(g) + "        " + str(iso_count[g]))

    print("Total processing time: " + str(round(total_time, 3)) + " s")
    print("")

    """
    FILE OUTPUT
    """
    if write_to_csv:
        # Create empty file
        csv_filename = 'tournament'
        if problem == 1:
            csv_filename += '-gi_problem'
            csv_column_names = ["Sets of isomorphic graphs"]
        elif problem == 2:
            csv_filename += '-gi_count'
            csv_column_names = ["Sets of isomorphic graphs", "Number of isomorphisms"]
        elif problem == 3:
            csv_filename += '-automorphisms'
            csv_column_names = ["Graph", "Automorphisms"]
        csv_filename += '-' + filename

        csv_filepath = create_csv_file(csv_filename)
        write_csv_line(csv_filepath, csv_column_names)

        if problem == 1 or problem == 2:
            for pair in isomorphisms:
                if problem == 1:
                    csv_graph_line = [str(pair)]
                elif problem == 2:
                    csv_graph_line = [str(pair), str(iso_count[pair[0]])]
                write_csv_line(csv_filepath, csv_graph_line)
        elif problem == 3:
            for g in sorted(iso_count):
                csv_graph_line = [str(g), str(iso_count[g])]
                write_csv_line(csv_filepath, csv_graph_line)

        write_csv_line(csv_filepath, [])
        csv_time = ["Total processing time:", str(round(total_time, 3)) + " s"]
        write_csv_line(csv_filepath, csv_time)