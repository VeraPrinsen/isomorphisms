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

    # Dependent on problem to be solved, create loop for first graph
    if problem == 1 or problem == 2:
        i_loop = range(len(graphs)-1)
    else:
        i_loop = range(len(graphs))

    if problem == 1:
        results = []
    elif problem == 2 or problem == 3:
        results = {}
    total_time = 0
    for i in i_loop:
        # Dependent on problem to be solved, create loop for second graph
        if problem == 1 or problem == 2:
            j_loop = range(i + 1, len(graphs))
        else:
            j_loop = [i]
        for j in j_loop:
            G = graphs[i]
            H = graphs[j]

            if problem == 1 or problem == 2:
                G_copy = G.copy()
                H_copy = H.copy()
                start_isomorph = time()
                are_isomorph_actual = are_isomorph(G_copy, H_copy)
                end_isomorph = time()
                total_time += round((end_isomorph - start_isomorph), 3)
                if problem == 1 and are_isomorph_actual:
                    results.append((i, j))

            if problem == 2 or problem == 3:
                G_copy = G.copy()
                H_copy = H.copy()
                start_amount_isomorphisms = time()
                amount_isomorph_actual = amount_of_isomorphisms(G_copy, H_copy)
                end_amount_isomorphisms = time()
                total_time += round((end_amount_isomorphisms - start_amount_isomorphisms), 3)
                if problem == 2 and are_isomorph_actual:
                    results[(i, j)] = amount_isomorph_actual
                if problem == 3:
                    results[i] = amount_isomorph_actual

    print("-------------------------------")
    print("Results " + filename)
    print("-------------------------------")
    if problem == 1:
        title("Sets of isomorphic graphs:")
    elif problem == 2:
        title("Sets of isomorphic graphs:   Number of isomorphisms:")
    elif problem == 3:
        title("Graph:   Number of automorphisms:")
    for key in results:
        if problem == 1:
            print(str(key))
        elif problem == 2:
            print(str(key) + "                       " + str(results[key]))
        elif problem == 3:
            print(str(key) + "        " + str(results[key]))
    print("")

    # if write_to_csv:
    #     csv_graph_result = [filename, i, j,
    #                         are_isomorph_expected, are_isomorph_actual, are_isomorph_passed, are_isomorph_time,
    #                         amount_isomorph_expected, amount_isomorph_actual, amount_isomorph_passed, amount_isomorph_time]
    #     write_csv_line(csv_filepath, csv_graph_result)


