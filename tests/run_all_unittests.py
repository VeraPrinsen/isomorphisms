from input_output.sys_output import passed, fail
from tests import branching, decide_gi, csvwriter, color_refinement, fast_color_refinement, graph, \
    graph_del_vertex_edge, preprocessing_twins

"""
All unit tests will be called in sequence.
It is up to the unit test to display useful information about the test either to the console (stdout) or CSV.

Procedure:
By calling the method <imported test>.unittest(write_csv_any, write_stdout_passed, write_stdout_fail) a unit test is run.
A boolean value that is returned by the function .unittest() is stored in a list called `result_boolean`.

After all the unit test results are appended to `result_boolean`, the list is searched for any occurences of False.
If any False is detected in the list, the user is notified.

"""

# Global test settings
write_csv_any = True
write_stdout_passed = True
write_stdout_fail = True

result_boolean = list()

result_boolean.append(branching.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(color_refinement.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(csvwriter.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(decide_gi.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(fast_color_refinement.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(graph.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(graph_del_vertex_edge.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')
result_boolean.append(preprocessing_twins.unit_test(write_csv_any, write_stdout_passed, write_stdout_fail))
print('')

# Finally
print('')
if False in result_boolean:
    fail('---> Not all tests passed !')
else:
    passed('---> All ' + str(len(result_boolean)) + ' test(s) passed!')
