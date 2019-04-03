# Util imports
from input_output.file_output import load_graph_list_from_filepath
from input_output.sys_output import passed
import tkinter as tk
from tkinter import filedialog
from time import time
from tests.integration_test.tournament_output import tournament_output
from tests.integration_test.test_output import test_output
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

    isomorphisms = []       # List of lists that saves all isomorphic pairs (or more than 2, if that is the case)
    iso_count = {}          # Dictionary that saves for each graph the amount of automorphisms
    total_time = 0
    skip = [False for _ in range(len(graphs))]  # To check if you can skip a cycle
    # In this first loop, for each combination, it is determined if they are isomorphic or not
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            G = graphs[i]
            H = graphs[j]

            # If both graphs are already in the result structure, they can be skipped
            if skip[i] and skip[j]:
                continue

            # Determine if the two graphs are isomorphic
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
                if skip[i] or skip[j]:
                    for pair in isomorphisms:
                        if i in pair:
                            pair.append(j)
                            skip[j] = True
                            break
                        elif j in pair:
                            pair.append(i)
                            skip[i] = True
                            break
                # Otherwise a new pair of isomorphisms should be added to the list
                else:
                    isomorphisms.append([i, j])
                    skip[i] = True
                    skip[j] = True

    # If the problem to be resolved is the #Automorphism problem, all graphs need to be in de result, also those
    # that are not an isomorphism with any other graph. Those graphs will be added to the isomorphism result as
    # singular isomorphism groups
    if problem == 3:
        for i in range(len(skip)):
            if not skip[i]:
                isomorphisms.append([i])

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

    if run_mode == 1:
        test_output(filename, len(graphs), total_time, isomorphisms, iso_count)
    elif run_mode == 2:
        tournament_output(filename, total_time, isomorphisms, iso_count)
    else:
        print("RUN MODE NOT RECOGNIZED, PROGRAM WILL TERMINATE")
        break