from input_output.sys_output import passed, fail
from tests import decide_gi, csvwriter

all_pass_flag = True
result_boolean = list()

result_boolean.append(decide_gi.unit_test())
result_boolean.append(csvwriter.unit_test())

# Finally
print('')
if False in result_boolean:
    fail('---> Not all tests passed !')
else:
    passed('---> All test passed!')
