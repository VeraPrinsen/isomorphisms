from supporting_components.basicpermutationgroup import FindNonTrivialOrbit, Stabilizer, Orbit
from supporting_components.permv2 import permutation
from typing import List


def order_computation(H: 'List[permutation]'):
    """
    Recursively computes the order of a list of permutations.
    Based on slide 21 of lecture 4 and notes.
    :param H: Permutation group
    :return: int with the order of the list of permutations
    """
    # If H has only one element and it is the unity permutation. The length of the orbit is 1.
    # Because whatever a you choose, it can only map to itself.
    if len(H) == 1 and H[0].istrivial():
        return 1

    # And because the method Stabilizer does not return the unity permutation as part of the stabilizer,]
    # if further down in the recursion the length of H is zero, this actually means that only the unity
    # permutation is left, because that one must always be in the stabilizer. So in this case, the length
    # of the orbit is also 1.
    if len(H) == 0:
        return 1

    # In any other case, the theorem holds that the order of H is the order of the stabilizer multiplied by the
    # length of the orbit ( |H| = |H0| * |0_H| ). For this theorem the theory of slide 21 of the lecture slides
    # of L4 are used.

    # Choose a with nontrivial orbit
    a = FindNonTrivialOrbit(H)
    # Determine orbit of a (list of vertices to which 'a' can be mapped to)
    O_H = Orbit(H, a)
    # Determine stabilizer of a (list of permutations that leave 'a' untouched)
    H_0 = Stabilizer(H, a)

    return order_computation(H_0) * len(O_H)