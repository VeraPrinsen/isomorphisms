from input_output.file_output import load_graph_list
from supporting_components.graph_io import *
from algorithms.color_refinement import color_refinement
from algorithms.color_initialization import degree_color_initialization

# file = 'colorref_smallexample_4_7'
file = 'colorref_smallexample_4_16'
# file = 'colorref_smallexample_6_15'
# file = 'colorref_smallexample_2_49'
filename = 'test_graphs/color_refinement/' + file + '.grl'

graphs = load_graph_list(filename)

os.makedirs(os.path.dirname('output_graphs/main/'), exist_ok=True)

for i in range(0, len(graphs)):
    outputfilename = 'output_graphs/main/' + file + '_' + str(i) + '.dot'
    with open(outputfilename, 'w') as g0:
        write_dot(color_refinement(degree_color_initialization(graphs[i])), g0)
