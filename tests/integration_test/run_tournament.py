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
FILE OUTPUT
"""
# TODO: ADAPT TO TOURNAMENT
# If csv must be created, create an empty file here
if tournament_write_to_csv:
    csv_filepath = create_csv_file("tournament")
    # Write first row with column names
    csv_column_names = ['file', 'graph1', 'graph2',
                        'are_isomorph expected result', 'are_isomorph actual result', 'passed', 'are_isomorph processing time (s)',
                        'amount_of_isomorphisms expected result', 'amount_of_isomorphisms actual result', 'passed', 'amount_of_isomorphisms processing time (s)']
    write_csv_line(csv_filepath, csv_column_names)


"""
RUN TOURNAMENT
"""
for filepath in file_paths:
    graphs = load_graph_list_from_filepath(filepath)
    filename = (filepath.split("/")[-1]).split(".")[0]

    passed("Starting evaluating " + filename)

    isomorphisms = []
    iso_count = {}
    total_time = 0
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

            # Every combination should be checked
            if are_isomorph_actual:
                # Only save results if the combination of graphs is isomorphic
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
                    # Also save if graphs are not isomorphic
                    i_in_result = False
                    j_in_result = False
                    for pair in isomorphisms:
                        i_in_result = i_in_result or i in pair
                        j_in_result = j_in_result or j in pair
                    if not i_in_result:
                        isomorphisms.append([i])
                    if not j_in_result:
                        isomorphisms.append([j])

    if problem == 2 or problem == 3:
        # For each set of isomorphisms, calculate the amount of automorphisms of the first graph
        for pair in isomorphisms:
            G_copy1 = graphs[pair[0]].copy()
            G_copy2 = graphs[pair[0]].copy()
            start_amount_isomorphisms = time()
            amount_isomorph_actual = amount_of_isomorphisms(G_copy1, G_copy2)
            end_amount_isomorphisms = time()
            total_time += round((end_amount_isomorphisms - start_amount_isomorphisms), 3)
            for graph in pair:
                iso_count[graph] = amount_isomorph_actual

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

    # if write_to_csv:
    #     csv_graph_result = [filename, i, j,
    #                         are_isomorph_expected, are_isomorph_actual, are_isomorph_passed, are_isomorph_time,
    #                         amount_isomorph_expected, amount_isomorph_actual, amount_isomorph_passed, amount_isomorph_time]
    #     write_csv_line(csv_filepath, csv_graph_result)


