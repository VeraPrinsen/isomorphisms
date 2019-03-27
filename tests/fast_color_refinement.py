from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement, fast_color_refinement
from input_output.file_output import load_graph_list, save_graph_as_dot, save_graph_in_png
from algorithms.decide_gi import is_balanced_or_bijected
from input_output.sys_output import fail, passed
from time import time

"""
To test if the fast_color_refinement works and if it is faster compared to color_refinement. 
The correctness should be checked by yourself by looking at the graphs.
"""

"""
SETTINGS OF TEST
"""
# Enable this flag if you want to save png files of the final coloring of the disjoint union of the graph combinations
save_png = False

"""
DO NOT CHANGE ANYTHING BELOW HERE
"""
files = ['5', '10', '20', '40', '80', '160', '320', '640', '1280', '2560', '5120', '10240']
do_slow = [True, True, True, True, True, True, True, True, True, False, False, False]
for i_file in range(0, len(files)):
    file = files[i_file]
    filename = '/test_graphs/fast_color_refinement/threepaths' + file + '.gr'
    graphs = load_graph_list(filename)

    for i in range(0, len(graphs)):
        start_degree_color_initialization = time()
        G_initialized = degree_color_initialization(graphs[i])
        end_degree_color_initialization = time()
        if do_slow[i_file]:
            start_color_refinement = time()
            G_colored = color_refinement(G_initialized.copy())
            end_color_refinement = time()

            output_filename = 'threepaths' + file + '_' + str(i)
            save_graph_as_dot(G_colored, output_filename)

        G_copy = G_initialized.copy()

        start_fast_color_refinement = time()
        G_colored_fast = fast_color_refinement(G_copy)
        end_fast_color_refinement = time()

        output_filename = 'threepaths' + file + '_' + str(i) + 'fast'
        save_graph_as_dot(G_colored_fast, output_filename)

        print('---------------------------')
        print("Statistics of threepaths" + file + "-" + str(i) + ":")
        print('---------------------------')
        print('Processing time degree_color_initialization: ' + str(round(end_degree_color_initialization - start_degree_color_initialization, 3)) + " s")
        if do_slow[i_file]:
            print("Processing time color_refinement: " + str(round(end_color_refinement - start_color_refinement, 3)) + " s")
        print("Processing time fast_color_refinement: " + str(round(end_fast_color_refinement - start_fast_color_refinement, 3)) + " s")
        print('')

    if save_png:
        for i in range(0, len(graphs)):
            output_filename = 'threepaths' + file + '_' + str(i)
            save_graph_in_png(output_filename)
