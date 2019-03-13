from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement
from input_output.file_output import load_graph_list, save_graph_as_dot, save_graph_in_png
from algorithms.decide_gi import is_balanced_or_bijected
from input_output.sys_output import fail, passed
from time import time

"""
To test if the color_refinement works. This should be done by yourself by looking at the output graphs.
The test cases are those from the Solution Hints from Canvas.

Notation:
filename-0_1 = Graph of the disjoint union of Graph 0 and 1 of that file
"""


"""
SETTINGS OF TEST
"""
# Enable this flag if you want to save png files of the final coloring of the disjoint union of the graph combinations
save_png = True
# Set this variable to true if you want to show passed test results
show_passed_results = False

"""
DO NOT CHANGE ANYTHING BELOW HERE
"""
solution_isomorphisms = [
    {(1, 3), (0, 2)},
    {(0, 1), (2, 3), (4, 5)},
    {(0, 1)}
]

files = ['colorref_smallexample_4_7', 'colorref_smallexample_6_15', 'colorref_smallexample_2_49']
for i_file in range(0,len(files)):
    file = files[i_file]
    filename = '../test_graphs/color_refinement/' + file + '.grl'
    graphs = load_graph_list(filename)

    for i in range(0, len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            G = graphs[i] + graphs[j]

            start = time()
            color_refinement(degree_color_initialization(G))
            end = time()

            output_filename = file + '_' + str(i) + '_' + str(j)
            save_graph_as_dot(G, output_filename)

            print('---------------------------')
            print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
            print('---------------------------')

            if (i, j) in solution_isomorphisms[i_file]:
                if not is_balanced_or_bijected(G)[0]:
                    fail("[FAIL] Coloring of graph should be balanced, this is not the case.")
                elif show_passed_results:
                    passed("Coloring of graph is balanced.")
            else:
                if is_balanced_or_bijected(G)[0]:
                    fail("[FAIL] Coloring of graph should not be balanced, this is the case though.")
                elif show_passed_results:
                    passed("Coloring of graph is not balanced.")

            print("Processing time: " + str(round((end-start)*1000, 3)) + " ms")
            print('')

    if save_png:
        for i in range(0, len(graphs) - 1):
            for j in range(i + 1, len(graphs)):
                output_filename = file + '_' + str(i) + '_' + str(j)
                save_graph_in_png(output_filename)

