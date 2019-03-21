from input_output.sys_output import passed, fail
from tests.decide_gi import DecideGi
from tests.csvwriter import CsvWriter

all_pass_flag = True

# Add functions to test by constructing objects in a list
functions_to_test = [
    DecideGi(),
    CsvWriter(),

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
