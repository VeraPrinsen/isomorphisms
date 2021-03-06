from algorithms.color_initialization import degree_color_initialization
from algorithms.color_refinement import color_refinement, fast_color_refinement
from input_output.file_output import load_graph_list, save_graph_as_dot, create_csv_file, write_csv_line
from input_output.sys_output import fail, passed
from algorithms.preprocessing import fix_degrees
from time import time

"""
To test if the fast_color_refinement works and if it is faster compared to color_refinement. 
The correctness should be checked by yourself by looking at the graphs.
"""

def unit_test(write_csv_any=False, write_stdout_passed=True, write_stdout_fail=True):
    test_name = 'fast_color_refinement'
    if write_csv_any:
        csv_filepath = create_csv_file(test_name)
        print('<' + test_name + '> ' + 'Appending to CSV: ' + "file:///" + csv_filepath.replace('\\', '/') + '\nStart...')

        write_csv_line(csv_filepath, ['file', 'i', 'mode', 'Pass?', 'Time (s)'])
    else:
        print('<' + test_name + '>')

    """
    SETTINGS OF TEST
    """
    save_dot = False

    # Graph files to test. The latter list can be commented out for speed.
    files = ['5', '10', '20', '40', '80', '160', '320', '640'] + ['1280', '2560', '5120', '10240']
    # Do slow: also apply regular color_refinement to these graphs for comparison.
    do_slow = [True, True, True, True, False, False, False, False] + [False, False, False, False]

    """
    DO NOT CHANGE ANYTHING BELOW HERE
    """
    # There won't be any errors to detect algorithmically.
    error_count = 0
    total_tests = 0
    total_time = 0

    # File loop
    for i_file in range(0, len(files)):
        file = files[i_file]
        filename = '/test_graphs/fast_color_refinement/threepaths' + file + '.gr'
        graphs = load_graph_list(filename)

        for i in range(0, len(graphs)):
            # Graph test
            fix_degrees(graphs[i])

            # Time degree step separately
            start_degree_color_initialization = time()
            G_initialized = degree_color_initialization(graphs[i])
            end_degree_color_initialization = time()

            if do_slow[i_file]:
                total_tests += 1
                start_color_refinement = time()
                G_colored = color_refinement(G_initialized)
                end_color_refinement = time()

                output_filename = 'threepaths' + file + '_' + str(i)
                save_graph_as_dot(G_colored, output_filename)

            total_tests += 1
            start_copy_g_initialized = time()
            G_initialized_copy = G_initialized.copy()
            end_copy_g_initialized = time()

            start_fast_color_refinement = time()
            G_colored_fast = fast_color_refinement(G_initialized_copy)
            end_fast_color_refinement = time()

            if save_dot:
                output_filename = 'threepaths' + file + '_' + str(i) + 'fast'
                save_graph_as_dot(G_colored_fast, output_filename)

            if write_stdout_passed:
                print('')
                print("Statistics of threepaths" + file + "-" + str(i) + ":")
                print("Processing time degree_color_initialization: " + str(round(end_degree_color_initialization - start_degree_color_initialization, 3)) + " s")
                print("Processing time G_initialized.copy():        " + str(round(end_copy_g_initialized - start_copy_g_initialized, 3))+' s')

            if write_csv_any:
                write_csv_line(csv_filepath, [file, str(i), 'c_init', True, "{0:.3f}".format(end_degree_color_initialization - start_degree_color_initialization)])

            total_time += end_degree_color_initialization - start_degree_color_initialization

            if do_slow[i_file]:
                if write_stdout_passed:
                    print("Processing time color_refinement:            " + str(round(end_color_refinement - start_color_refinement, 3)) + " s")
                total_time += end_color_refinement - start_color_refinement
                if write_csv_any:
                    write_csv_line(csv_filepath, [file, str(i), 'slow', True, "{0:.3f}".format(end_color_refinement - start_color_refinement)])
            else:
                if write_stdout_passed:
                    print("Processing time color_refinement:            skipped")

            if write_stdout_passed:
                print("Processing time fast_color_refinement:       " + str(round(end_fast_color_refinement - start_fast_color_refinement, 3)) + " s")

            total_time += end_fast_color_refinement - start_fast_color_refinement
            if write_csv_any:
                write_csv_line(csv_filepath, [file, str(i), 'fast', True, "{0:.3f}".format(end_fast_color_refinement - start_fast_color_refinement)])

    # Determine test outcome
    test_pass_bool = False
    if error_count == 0:
        test_pass_bool = True
        passed(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestname:\n{0}\t\t{1}\t\t{2}\t{3}\t{4}'.format(
                str(total_tests),
                str(error_count),
                str(test_pass_bool),
                "{0:.3f}".format(
                    total_time),
                test_name)
        )
    else:
        fail(
            '#Tests\t#Fail\tPASS?\tTime(s)\tTestname:\n{0}\t\t{1}\t\t{2}\t{3}\t{4}'.format(
                str(total_tests),
                str(error_count),
                str(test_pass_bool),
                "{0:.3f}".format(
                    total_time),
                test_name)
        )
    # Test summary
    if write_csv_any:
        write_csv_line(csv_filepath, ['', '', '', ''])
        write_csv_line(csv_filepath, ['#Tests', '#Fail', 'PASS?', 'Time (s)'])
        write_csv_line(csv_filepath, [str(total_tests), str(error_count), str(test_pass_bool),
                                  "{0:.3f}".format(total_time)])
        print('</' + test_name + '>')
    return test_pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()