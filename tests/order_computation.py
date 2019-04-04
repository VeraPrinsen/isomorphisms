from input_output.sys_output import fail, passed
from supporting_components.permv2 import permutation
from algorithms.automorphism_problem import order_computation

"""
This test tests the order computation of the automorphism algorithm.
"""


def test_example_slide_21():
    p = permutation(6, cycles=[[0, 1, 2], [4, 5]])
    q = permutation(6, cycles=[[2, 3]])
    H = [p, q]
    order = order_computation(H)

    return order == 48


def test_example_redundant_permutation():
    H = []
    H.append(permutation(6, cycles=[[0, 1, 2], [4, 5]]))
    H.append(permutation(6, cycles=[[2, 3]]))
    H.append(permutation(6, cycles=[[0, 2]]))
    H.append(permutation(6, cycles=[[1, 2]]))
    H.append(permutation(6, cycles=[[0, 1]]))
    order = order_computation(H)

    return order == 48


def unit_test():
    test_name = 'order_computation'
    print('<' + test_name + '>')
    pass_bool = True
    if not test_example_slide_21():
        fail("test_example_slide_21: TEST FAILED")
        pass_bool = False

    if not test_example_redundant_permutation():
        fail("test_example_redundant_permutation: TEST FAILED")
        pass_bool = False

    if pass_bool:
        passed('' + test_name + ' PASS')

    print('</' + test_name + '>')

    return pass_bool


if __name__ == '__main__':
    # Run the unit test if file is called
    unit_test()
