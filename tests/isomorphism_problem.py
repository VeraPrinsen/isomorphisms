from input_output.file_output import load_graph_list, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
from algorithms.isomorphism_problem import are_isomorph, amount_of_isomorphisms
from time import time


"""
To test if the general isomorphism problem algorithms works finding isomorphisms between two graphs.
"""


"""
SETTING OF TEST
"""
# Set this variable to true if you want to show passed test results
show_passed_results = False
# Set this variable to true if you want to write all results to a csv file
create_csv = False

# todo: Add more test files? How can we do this easily so we can do it the 10th of April fast?
# Change here which files you want to evaluate
torus24 = False
trees90 = False
products72 = False
cographs1 = False
bigtrees1 = False
torus144 = False
trees36 = False
modulesC = False
cubes5 = False
bigtrees3 = False
cubes6 = False


"""
DO NOT CHANGE ANYTHING BELOW HERE
"""
# If csv must be created, create an empty file here
if create_csv:
    csv_filepath = create_csv_file("isomorphism-problem-test")
    # Write first row with column names
    csv_column_names = ['file', 'graph1', 'graph2', 'are_isomorph processing time (s)', 'passed', 'amount_of_isomorphisms processing time (s)', 'passed']
    write_csv_line(csv_filepath, csv_column_names)

# Only files that needs to be evaluated are added to the list.
i_files = []
torus24 and i_files.append(0)
trees90 and i_files.append(1)
products72 and i_files.append(2)
cographs1 and i_files.append(3)
bigtrees1 and i_files.append(4)
torus144 and i_files.append(5)
trees36 and i_files.append(6)
modulesC and i_files.append(7)
cubes5 and i_files.append(8)
bigtrees3 and i_files.append(9)
cubes6 and i_files.append(10)

files = [
    'torus24',
    'trees90',
    'products72',
    'cographs1',
    'bigtrees1',
    'torus144',
    'trees36',
    'modulesC',
    'cubes5',
    'bigtrees3',
    'cubes6'
]

# Solutions given on Canvas per file
solution_isomorphisms = [
    {(0, 3): 96, (1, 2): 96},
    {(0, 3): 6912, (1, 2): 20736},
    {(0, 6): 288, (1, 5): 576, (2, 3): 576, (4, 7): 864},
    {(0, 3): 5971968, (1, 2): 995328},
    {(0, 2): 442368, (1, 3): 5308416},
    {(0, 6): 576, (1, 7): 576, (2, 4): 576, (3, 10): 576, (5, 9): 1152, (8, 11): 576},
    {(0, 7): 2, (1, 4): 6, (2, 6): 2, (3, 5): 6},
    {(0, 7): 17915904, (1, 5): 17915904, (2, 4): 2488320, (3, 6): 2985984},
    {(0, 1): 3840, (2, 3): 24},
    {(0, 2): 2772351862699137701073289910157312, (1, 3): 462058643783189616845548318359552},
    {(0, 1): 96, (2, 3): 46080}
]

# For every file that needs to be evaluated, all combinations of graphs within that file are evaluated.
error_count = 0
graph_count = 0
for i_file in i_files:
    file = files[i_file]
    filename = '/test_graphs/individualization_refinement/' + file + '.grl'
    graphs = load_graph_list(filename)
    solution_map = solution_isomorphisms[i_file]

    for i in range(0, len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            graph_count += 1
            G = graphs[i]
            H = graphs[j]

            print('---------------------------')
            print("Statistics of " + file + "-" + str(i) + "_" + str(j) + ":")
            print('---------------------------')

            start_isomorph = time()
            boolean_isomorph = are_isomorph(G.copy(), H.copy())
            end_isomorph = time()

            start_amount_isomorphisms = time()
            n_isomorphisms = amount_of_isomorphisms(G.copy(), H.copy())
            end_amount_isomorphisms = time()

            are_isomorph_result = True
            amount_isomorph_result = True
            if (i, j) in solution_map:
                if not boolean_isomorph:
                    fail("[FAIL] Graphs are isomorph, is_isomorph(G, H) did not detect it")
                    error_count += 1
                    are_isomorph_result = False
                else:
                    if show_passed_results:
                        passed("Graphs are isomorph")

                if n_isomorphisms != solution_map[(i, j)]:
                    fail("[FAIL] Amount of isomorphisms should be " + str(solution_map[(i, j)]) + ", not " + str(n_isomorphisms))
                    error_count += 1
                    amount_isomorph_result = False
                else:
                    if show_passed_results:
                        passed("Amount of isomorphisms is: " + str(n_isomorphisms))
            else:
                if boolean_isomorph:
                    fail("[FAIL] Graphs are not isomorph, is_isomorph determined they were")
                    error_count += 1
                    are_isomorph_result = False
                else:
                    if show_passed_results:
                        passed("Graphs are not isomorph")

            are_isomorph_time = round((end_isomorph - start_isomorph), 3)
            amount_isomorph_time = round((end_amount_isomorphisms - start_amount_isomorphisms), 3)
            print("Processing time is_isomorph(G, H): " + str(are_isomorph_time) + " s")
            print("Processing time amount_of_isomorphisms(G, H): " + str(amount_isomorph_time) + " s")
            print('')

            if create_csv:
                csv_graph_result = [file, i, j, are_isomorph_time, are_isomorph_result, amount_isomorph_time, amount_isomorph_result]
                write_csv_line(csv_filepath, csv_graph_result)

print('-------------------------------')
print("Statistics of branching test:")
print('-------------------------------')
print("Amount of graphs tested: " + str(graph_count))
print("Amount of graphs not colored correctly: " + str(error_count))
print('')
if error_count > 0:
    fail('TEST FAILED')
else:
    passed('TEST PASSED')
print('')
