from supporting_components.graph_io import *
from algorithms.color_refinement import color_refinement
from algorithms.color_initialization import degree_color_initialization

# file = 'colorref_smallexample_4_7'
file = 'colorref_smallexample_4_16'
# file = 'colorref_smallexample_6_15'
# file = 'colorref_smallexample_2_49'
filename = 'test_graphs/color_refinement/' + file + '.grl'

with open(filename) as f:
    L = load_graph(f, read_list=True)

for i in range(0, len(L[0])):
    outputfilename = 'output_graphs/' + file + '_' + str(i) + '.dot'
    with open(outputfilename, 'w') as g0:
        write_dot(color_refinement(degree_color_initialization(L[0][i])), g0)
