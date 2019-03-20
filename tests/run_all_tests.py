from input_output.sys_output import passed, fail
from tests.decide_gi import Decide_gi
from tests import fun_provider

all_pass_flag = True

# Add functions to test by constructing objects in a list
functions_to_test = [
    Decide_gi()
]

# Types of tests to run on test objects
test_types_to_run = [
    'run_color_refinement',
    'run_fast_color_refinement'
]

for test_object in functions_to_test:
    if 'run_color_refinement' in test_types_to_run:
        if not test_object.run_color_refinement(fun_provider.Default_color_refinement()):
            all_pass_flag = False

    if 'run_fast_color_refinement' in test_types_to_run:
        if not test_object.run_fast_color_refinement(fun_provider.Fast_color_refinement()):
            all_pass_flag = False


# Finally
print('')
if all_pass_flag:
    passed('---> All test passed!')
else:
    fail('---> Not all tests passed, aborted.')