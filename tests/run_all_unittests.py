from input_output.sys_output import passed, fail
from tests.decide_gi import Decide_gi
from tests.csvwriter import Csvwriter

all_pass_flag = True

# Add functions to test by constructing objects in a list
functions_to_test = [
    Decide_gi(),
    Csvwriter(),

]

for test_object in functions_to_test:
    if not test_object.unittest():
        all_pass_flag = False

# Finally
print('')
if all_pass_flag:
    passed('---> All test passed!')
else:
    fail('---> Not all tests passed !')
