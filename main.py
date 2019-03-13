from input_output.file_output import load_graph_list
from supporting_components.graph_io import *
from algorithms.color_refinement import color_refinement
from algorithms.color_initialization import degree_color_initialization
from input_output.file_output import write_csv_line
from input_output.file_output import create_csv_file
import time

# file = 'colorref_smallexample_4_7'
file = 'colorref_smallexample_4_16'
# file = 'colorref_smallexample_6_15'
# file = 'colorref_smallexample_2_49'
filename = 'test_graphs/color_refinement/' + file + '.grl'

graphs = load_graph_list(filename)

csv_target_filename = create_csv_file('main')
write_csv_line(csv_target_filename, ['file', 'i', 'time (ms)'])

for i in range(0, len(graphs)):
    outputfilename = 'output_graphs/' + file + '_' + str(i) + '.dot'

    start_time = time.time()
    with open(outputfilename, 'w') as g0:
        write_dot(color_refinement(degree_color_initialization(graphs[i])), g0)

    end_time = time.time() - start_time

    write_csv_line(csv_target_filename, [file, str(i), str(end_time)])