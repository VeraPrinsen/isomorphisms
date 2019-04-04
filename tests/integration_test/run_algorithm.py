# Util imports
from input_output.file_output import load_graph_list_from_filepath
from input_output.sys_output import passed, fail
import sys
import tkinter as tk
from tkinter import filedialog
from time import time
from tests.integration_test.tournament_output import tournament_output
from tests.integration_test.test_output import test_output
# Algorithm imports
from tests.integration_test.settings import *
from tests.integration_test.isomorphism_problem import preprocessing, are_isomorph, amount_of_automorphisms

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
RUN ALGORITHM
"""
if run_mode == 1:
    error_count = 0
for file_path in file_paths:
    start_time = time()

    graphs = load_graph_list_from_filepath(file_path)
    filename = (file_path.split("/")[-1]).split(".")[0]

    # Preprocessing that should be done once per graph
    # Twin removal - Complement
    multiplication_factor = [1 for _ in range(len(graphs))]
    preprocessed_graphs = {}
    for i in range(len(graphs)):
        G_complement, factor = preprocessing(graphs[i])
        # If complement was applied, G_complement is the graph you should determine isomorphisms with
        preprocessed_graphs[i] = G_complement
        # If twin removal was applied, a factor > 1 could be returned and the amount of automorphisms should be
        # multiplied with it
        multiplication_factor[i] = factor

    # Some data structures that are used to determine if graphs are isomorphic more efficiently
    isomorphisms = []       # List of lists that saves all isomorphic pairs (or more than 2, if that is the case)
    automorphisms = {}      # Dictionary that saves for each graph the amount of automorphisms
    skip = [False for _ in range(len(graphs))]  # To check if you can skip a cycle

    # In this first loop, for each combination, it is determined if they are isomorphic or not
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            s = filename + ": Determining if [" + str(i) + "," + str(j) + "] are isomorphic (out of " + str(len(graphs) - 1) + " graphs)"
            sys.stdout.write('\r' + s)

            # If both graphs are already in the result structure, they can be skipped
            if skip[i] and skip[j]:
                continue

            # Determine if the two graphs are isomorphic
            are_isomorph_actual = are_isomorph(preprocessed_graphs[i], preprocessed_graphs[j])

            # Only save results if the combination of graphs is isomorphic
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
        group_count = 0
        for pair in isomorphisms:
            group_count += 1
            s = filename + ": Calculating amount of isomorphisms of isomorphic group " + str(pair) + " (" + str(group_count) + " out of " + str(len(isomorphisms)) + " groups)"
            sys.stdout.write('\r' + s)
            amount_automorphisms_actual = multiplication_factor[pair[0]] * amount_of_automorphisms(graphs[pair[0]])
            # Each graph in the pair has the same amount of automorphisms
            for graph in pair:
                automorphisms[graph] = amount_automorphisms_actual
    sys.stdout.write('\r' + "Done evaluating " + filename)
    print('')

    end_time = time()
    total_time = end_time - start_time

    if run_mode == 1:
        error_count += test_output(filename, len(graphs), total_time, isomorphisms, automorphisms)
    elif run_mode == 2:
        tournament_output(filename, total_time, isomorphisms, automorphisms)
    else:
        fail("RUN MODE NOT RECOGNIZED, PROGRAM WILL TERMINATE")
        break

if run_mode == 1:
    if error_count > 0:
        fail("INTEGRATION TEST FAILED - " + str(error_count) + " tests failed.")
    elif error_count == 0:
        passed("INTEGRATION TEST PASSED")
