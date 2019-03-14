from input_output.sys_output import passed, fail
from tests import decide_gi

if decide_gi.test() and decide_gi.test():
    print('')
    print('')
    passed('---> All test passed, terminated successfully!')
else:
    print('')
    print('')
    fail('---> Not all tests passed, aborted.')
