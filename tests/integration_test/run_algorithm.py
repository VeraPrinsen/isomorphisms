# Util imports
from input_output.file_output import load_graph_list_from_filepath
from input_output.sys_output import passed, fail
import sys
import tkinter as tk
from tkinter import filedialog
from time import time

from tests.integration_test.isomorphism_problem import preprocess_graphs, determine_isomorphic_pairs, test_automorphisms
from tests.integration_test.tournament_output import tournament_output
from tests.integration_test.test_output import test_output
# Algorithm imports
from tests.integration_test.settings import *
"""
General integration test for the Graph Isomorphisms problem.
Settings of the algorithm must be changed in > settings.py <
"""

def main():
    global graphs, filename, multiplication_factor, skip
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

        multiplication_factor, preprocessed_graphs, isomorphisms, automorphisms, skip = preprocess_graphs(graphs)

        # For each graph
        print(graphs)
        determine_isomorphic_pairs(graphs, filename, preprocessed_graphs, isomorphisms, skip)

        test_automorphisms(filename, preprocessed_graphs, multiplication_factor, isomorphisms, automorphisms, skip, problem)

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


if __name__ == '__main__':
    # Run the unit test if file is called
    main()