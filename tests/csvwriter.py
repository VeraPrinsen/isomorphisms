from input_output.file_output import load_graph_list, save_graph_as_dot
from algorithms.color_refinement import color_refinement
from algorithms.color_initialization import degree_color_initialization
from input_output.file_output import write_csv_line
from input_output.file_output import create_csv_file
import time
import csv

# This file is to demonstrate the workings of writing test results to a CSV file.
# The test itself is a mock and will always pass.
# The result of the test are written to CSV in the folder output_files/csv/
from input_output.sys_output import fail, passed

file = 'colorref_smallexample_4_16'
filename = 'test_graphs/color_refinement/' + file + '.grl'
graphs = load_graph_list(filename)

# Output csv creation
csv_filepath = create_csv_file('csvwriter_test')
# Write first row with column names
csv_write_array = [['file', 'i', 'time (s)', 'result']]

# Test result accumulators
end_time_sum = 0
test_result_passed = True

# mocked test loop
for i in range(0, len(graphs)):
    outputfilename = 'output_files/main/' + file + '_' + str(i) + '.dot'

    start_time = time.time()
    save_graph_as_dot(color_refinement(degree_color_initialization(graphs[i])), outputfilename)

    # In a real test this value might be false...
    test_result_mock = True

    if not test_result_mock:
        test_result_passed = False

    end_time = time.time() - start_time
    end_time_sum = end_time_sum + end_time
    # Write individual test result to the csv
    csv_write_array.append([file, str(i), "{0:.3f}".format(end_time), str(test_result_mock)])

# Write the total test result row to csv
csv_write_array.append(['', '', '', ''])
csv_write_array.append(['', '', 'Total (s)', 'All pass?'])
csv_write_array.append(['', '', "{0:.3f}".format(end_time_sum), str(test_result_passed)])

for line in csv_write_array:
    write_csv_line(csv_filepath, line)

print('CSV written to: ' + csv_filepath)

print("VERIFYING write action...")

csv_read_array =[]

with open(csv_filepath, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        csv_read_array.append(row)

# The first row is the separator line, pop it
csv_read_array.pop(0)

if csv_read_array == csv_write_array:
    passed("CSV write OK")
else:
    fail("CSV write test failed")