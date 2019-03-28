# Util imports
from input_output.file_output import load_graph_list_from_filepath, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
import tkinter as tk
from tkinter import filedialog
from time import time
# Algorithm imports
from tests.integration_test.settings import *
from tests.integration_test.solutions import *
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
# If csv must be created, create an empty file here
if write_to_csv:
    csv_filepath = create_csv_file("isomorphism-problem-test")
    # Write first row with column names
    csv_column_names = ['file', 'graph1', 'graph2',
                        'are_isomorph expected result', 'are_isomorph actual result', 'passed', 'are_isomorph processing time (s)',
                        'amount_of_isomorphisms expected result', 'amount_of_isomorphisms actual result', 'passed', 'amount_of_isomorphisms processing time (s)']
    write_csv_line(csv_filepath, csv_column_names)

"""
ACTUAL TEST
"""
# For every file that needs to be evaluated, all combinations of graphs within that file are evaluated.
graph_count = 0
error_count = 0
for filepath in file_paths:
    graphs = load_graph_list_from_filepath(filepath)
    filename = (filepath.split("/")[-1]).split(".")[0]
    solution_map = {}
    if filename in solution:
        solution_map = solution[filename]

    for i in range(0, len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            G = graphs[i]
            H = graphs[j]

            if console_pass or console_fail:
                print('---------------------------')
                print("Statistics of " + filename + "-" + str(i) + "_" + str(j) + ":")
                print('---------------------------')

            G_copy = G.copy()
            H_copy = H.copy()
            start_isomorph = time()
            are_isomorph_actual = are_isomorph(G_copy, H_copy)
            end_isomorph = time()

            start_amount_isomorphisms = time()
            amount_isomorph_actual = amount_of_isomorphisms(G, H)
            end_amount_isomorphisms = time()

            # If solution of file is in solutions.py, check if solution is correct
            if bool(solution_map):
                graph_count += 1
                are_isomorph_expected = (i, j) in solution_map
                if are_isomorph_expected:
                    amount_isomorph_expected = solution_map[(i, j)]
                else:
                    amount_isomorph_expected = 0
                are_isomorph_passed = True
                amount_isomorph_passed = True
                # Graphs should be isomorphic
                if are_isomorph_expected:
                    if not are_isomorph_actual:
                        if console_fail:
                            fail("[FAIL] Graphs are isomorph, is_isomorph(G, H) did not detect it")
                        error_count += 1
                        are_isomorph_passed = False
                    else:
                        if console_pass:
                            passed("Graphs are isomorph")

                    # If amount of isomorphisms in solution is -1, there is no answer known
                    if amount_isomorph_expected != -1:
                        if amount_isomorph_actual != amount_isomorph_expected:
                            if console_fail:
                                fail("[FAIL] Amount of isomorphisms should be " + str(amount_isomorph_expected) + ", not " + str(amount_isomorph_actual))
                            error_count += 1
                            amount_isomorph_passed = False
                        else:
                            if console_pass:
                                passed("Amount of isomorphisms is: " + str(amount_isomorph_actual))
                # Graphs should not be isomorphic
                else:
                    if are_isomorph_actual:
                        if console_fail:
                            fail("[FAIL] Graphs are not isomorph, is_isomorph determined they were")
                        error_count += 1
                        are_isomorph_passed = False
                    else:
                        if console_pass:
                            passed("Graphs are not isomorph")
            else:
                are_isomorph_expected = '-'
                are_isomorph_passed = '-'
                amount_isomorph_expected = '-'
                amount_isomorph_passed = '-'

            are_isomorph_time = round((end_isomorph - start_isomorph), 3)
            amount_isomorph_time = round((end_amount_isomorphisms - start_amount_isomorphisms), 3)

            if console_pass or console_fail:
                print("Processing time is_isomorph(G, H): " + str(are_isomorph_time) + " s")
                print("Processing time amount_of_isomorphisms(G, H): " + str(amount_isomorph_time) + " s")
                print('')

            if write_to_csv:
                csv_graph_result = [filename, i, j,
                                    are_isomorph_expected, are_isomorph_actual, are_isomorph_passed, are_isomorph_time,
                                    amount_isomorph_expected, amount_isomorph_actual, amount_isomorph_passed, amount_isomorph_time]
                write_csv_line(csv_filepath, csv_graph_result)

if console_pass or console_fail:
    print('-------------------------------')
    print("Statistics of branching test:")
    print('-------------------------------')
    print("Amount of graphs tested: " + str(graph_count))
    print("Amount of graphs with failed results: " + str(error_count))
    print('')
    if error_count > 0:
        fail('TEST FAILED')
    else:
        passed('TEST PASSED')
    print('')


