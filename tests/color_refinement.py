from supporting_components.graph_io import *
from time import time
from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement
from input_output.file_output import save_graph_as_dot, save_graph_in_png

"""
To test if the color_refinement works. This should be done by yourself by looking at the output graphs.
The test cases are those from the Solution Hints from Canvas.

Notation:
filename-0_1 = Graph of the disjoint union of Graph 0 and 1 of that file

# Small Example 2_49:
G0 and G1 are isomorphic (discrete coloring)

# Small Example 4_7:
G1 and G3 are isomorphic (discrete coloring)
G0 and G2 are isomorphic (but undecided after coloring)

# Small Example 6_15:
G0 and G1 are isomorphic (discrete coloring)
G2 and G3 are isomorphic (discrete coloring)
G4 and G5 are isomorphic (but undecided after coloring)

"""

savePng = True

files = ['colorref_smallexample_4_7', 'colorref_smallexample_6_15', 'colorref_smallexample_2_49']
for file in files:
    filename = '../test_graphs/color_refinement/' + file + '.grl'
    with open(filename) as f:
        L = load_graph(f, read_list=True)

    for i in range(0, len(L[0]) - 1):
        for j in range(i + 1, len(L[0])):
            G = L[0][i] + L[0][j]
            start = time()
            color_refinement(degree_color_initialization(G))
            end = time()

            output_filename = file + '_' + str(i) + '_' + str(j)
            save_graph_as_dot(G, output_filename)

            print('---------------------------')
            print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
            print('---------------------------')
            print("Processing time: " + str(round((end-start)*1000, 3)) + " ms")
            print('')

    if savePng:
        for i in range(0, len(L[0]) - 1):
            for j in range(i + 1, len(L[0])):
                output_filename = file + '_' + str(i) + '_' + str(j)
                save_graph_in_png(output_filename)

