# Util imports
from input_output.file_output import load_graph_list_from_filepath, create_csv_file, write_csv_line
from input_output.sys_output import title, passed
import tkinter as tk
from tkinter import filedialog
from time import time
# Algorithm imports
from tests.integration_test.settings import *
from tests.integration_test.isomorphism_problem import are_isomorph, amount_of_isomorphisms

"""
General integration test for the Graph Isomorphisms problem.
Settings of the algorithm must be changed in > settings.py <
"""

"""
FILE INPUT
"""
# Select files to evaluate
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames()

"""
RUN TOURNAMENT
"""
for filepath in file_paths:
    graphs = load_graph_list_from_filepath(filepath)
    filename = (filepath.split("/")[-1]).split(".")[0]

    passed("Starting evaluating " + filename)

    isomorphisms = []       # Data structure that saves all isomorphic pairs (or more than 2, if that is the case)
    iso_count = {}          # Data structure that saves for each graph the amount of automorphisms
    total_time = 0
    # In this first loop, for each combination, it is determined if they are isomorphic or not
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            G = graphs[i]
            H = graphs[j]

            G_copy = G.copy()
            H_copy = H.copy()
            start_isomorph = time()
            are_isomorph_actual = are_isomorph(G_copy, H_copy)
            end_isomorph = time()
            total_time += round((end_isomorph - start_isomorph), 3)

            # Only save results if the combination of graphs is isomorphic, unless you have to know the automorphisms
            # of each graph, then save each graph in de isomorphisms data structure.
            if are_isomorph_actual:
                # If one of the two graphs is already in a isomorphic pair, the other graph belongs to it too
                already_in_results = -1
                for pair in isomorphisms:
                    if i in pair:
                        pair.append(j)
                        already_in_results = i
                        break
                    elif j in pair:
                        pair.append(i)
                        already_in_results = j
                        break
                # Otherwise a new pair of isomorphisms should be added to the list
                if already_in_results < 0:
                    isomorphisms.append([i, j])
            else:
                if problem == 3:
                    # If graphs are not isomorphic, check for each one if it is already in the isomorphic data structure
                    # If not, add it
                    i_in_result = False
                    j_in_result = False
                    for pair in isomorphisms:
                        i_in_result = i_in_result or i in pair
                        j_in_result = j_in_result or j in pair
                    if not i_in_result:
                        isomorphisms.append([i])
                    if not j_in_result:
                        isomorphisms.append([j])

    # For each set of isomorphisms, calculate the amount of automorphisms of the first graph. This can be done
    # because the graphs are isomorphic and the amount of isomorphisms are equal to the amount of automorphisms of the
    # independent graphs
    if problem == 2 or problem == 3:
        for pair in isomorphisms:
            G_copy1 = graphs[pair[0]].copy()
            G_copy2 = graphs[pair[0]].copy()
            start_amount_isomorphisms = time()
            amount_isomorph_actual = amount_of_isomorphisms(G_copy1, G_copy2)
            end_amount_isomorphisms = time()
            total_time += round((end_amount_isomorphisms - start_amount_isomorphisms), 3)
            # Each graph in the pair has the same amount of automorphisms
            for graph in pair:
                iso_count[graph] = amount_isomorph_actual

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
    if tournament_write_to_csv:
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