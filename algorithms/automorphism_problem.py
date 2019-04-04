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
    # Choose a with nontrivial orbit
    a = FindNonTrivialOrbit(H)
    # Determine orbit of a (list of vertices 'a' can be mapped to)
    O_H = Orbit(H, a)

    # If length of the list of permutation H is equal to 1 (which is the stabilizer of the previous recursive call):
    # Length of orbit = length of elements in the permutation in H
    # Stabilizer = empty set, because there is no permutation that leaves an element untouched
    # And the order is equal to the orbit that is determined using the previous stabilizer
    if len(H) == 1:
        return len(O_H)

    # Determine stabilizer of a (list of permutations that leave 'a' untouched)
    H_0 = Stabilizer(H, a)

    # Order of list of permutation H = |H|
    # Order of stabilizer (which is a list of permutations) H_0 = |H_0|
    # Length of orbit (which is a list of vertices labels) O_H = |O_H|
    # Orbit-Stabilizer-theorem:     |H| = |H_0| * |O_H|
    return order_computation(H_0) * len(O_H)