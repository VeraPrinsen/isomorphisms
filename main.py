from input_output.file_output import load_graph_list, save_graph_as_dot
from algorithms.color_refinement import color_refinement
from algorithms.color_initialization import degree_color_initialization
from input_output.file_output import write_csv_line
from input_output.file_output import create_csv_file
import time
import os

# file = 'colorref_smallexample_4_7'
file = 'colorref_smallexample_4_16'
# file = 'colorref_smallexample_6_15'
# file = 'colorref_smallexample_2_49'
filename = 'test_graphs/color_refinement/' + file + '.grl'

graphs = load_graph_list(filename)

# Test output csv creation
csv_filepath = create_csv_file('main')
# Write first row with column names
write_csv_line(csv_filepath, ['file', 'i', 'time (s)', 'result'])

# Test result accumulators
end_time_sum = 0
test_result_passed = True

# main test loop
for i in range(0, len(graphs)):
    outputfilename = 'output_files/main/' + file + '_' + str(i) + '.dot'

    start_time = time.time()
    save_graph_as_dot(color_refinement(degree_color_initialization(graphs[i])), outputfilename)

    test_result = True
    if not test_result:
        test_result_passed = False

    end_time = time.time() - start_time
    end_time_sum = end_time_sum + end_time
    # Write individual test result to the csv
    write_csv_line(csv_filepath, [file, str(i), "{0:.3f}".format(end_time), str(test_result)])

# Write the total test result row to csv
write_csv_line(csv_filepath, ['', '', '', ''])
write_csv_line(csv_filepath, ['', '', 'Total (s)', 'All pass?'])
write_csv_line(csv_filepath, ['', '', "{0:.3f}".format(end_time_sum), str(test_result_passed)])
