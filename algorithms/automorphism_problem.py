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
    # Choose a nontrivial orbit
    a = FindNonTrivialOrbit(H)
    # Determine orbit of nontrivial orbit
    O_H = Orbit(H, a)

    # End of recursion, |H| = |O_H| * 1
    if len(H) == 1:
        return len(O_H)

    # Determine stabilizer of nontrivial orbit
    H_0 = Stabilizer(H, a)

    # |H| = |H_0| * |O_H|
    return order_computation(H_0) * len(O_H)