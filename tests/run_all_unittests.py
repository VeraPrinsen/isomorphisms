from input_output.sys_output import passed, fail
from tests import decide_gi, csvwriter, color_refinement, fast_color_refinement, graph, graph_del_vertex_edge, \
    isomorphism_problem, preprocessing_twins

all_pass_flag = True
result_boolean = list()

result_boolean.append(color_refinement.unit_test())
result_boolean.append(csvwriter.unit_test())
result_boolean.append(decide_gi.unit_test())
result_boolean.append(fast_color_refinement.unit_test())
result_boolean.append(graph.unit_test())
result_boolean.append(graph_del_vertex_edge.unit_test())
result_boolean.append(isomorphism_problem.unit_test())
result_boolean.append(preprocessing_twins.unit_test())

# Finally
print('')
if False in result_boolean:
    fail('---> Not all tests passed !')
else:
    passed('---> All ' + str(len(result_boolean)) + ' test(s) passed!')
