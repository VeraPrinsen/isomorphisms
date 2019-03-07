from supporting_components.graph_io import *
from algorithms.color_refinement import color_refinement
from algorithms.decide_gi import is_balanced_or_bijected


# TODO: create a nice test that verifies the following:
# colorref_smallexample_2_49
# 0, 1, (is_balanced, is_bijected), (True, True)
#
# colorref_smallexample_4_7
# 0, 1, (is_balanced, is_bijected), (False, False)
# 0, 2, (is_balanced, is_bijected), (True, False)
# 1, 2, (is_balanced, is_bijected), (False, False)
# 0, 3, (is_balanced, is_bijected), (False, False)
# 1, 3, (is_balanced, is_bijected), (True, True)
# 2, 3, (is_balanced, is_bijected), (False, False)
#
# colorref_smallexample_6_15
# 0, 1, (is_balanced, is_bijected), (True, True)
# 0, 2, (is_balanced, is_bijected), (False, False)
# 1, 2, (is_balanced, is_bijected), (False, False)
# 0, 3, (is_balanced, is_bijected), (False, False)
# 1, 3, (is_balanced, is_bijected), (False, False)
# 2, 3, (is_balanced, is_bijected), (True, True)
# 0, 4, (is_balanced, is_bijected), (False, False)
# 1, 4, (is_balanced, is_bijected), (False, False)
# 2, 4, (is_balanced, is_bijected), (False, False)
# 3, 4, (is_balanced, is_bijected), (False, False)
# 0, 5, (is_balanced, is_bijected), (False, False)
# 1, 5, (is_balanced, is_bijected), (False, False)
# 2, 5, (is_balanced, is_bijected), (False, False)
# 3, 5, (is_balanced, is_bijected), (False, False)
# 4, 5, (is_balanced, is_bijected), (True, False)


# With (from canvas)

# Here are some of the answers of the instances for this week (an instance with 4 graphs is counted as graphs 0,1,2,3):
#
#     colorref_smallexample_2_49 : These two graphs are isomorphic
#     colorref_smallexample_4_7 : 1 and 3 are isomorphic, 0 and 2 are isomorphic (yet remain undecided after color refinement), and all other pairs are not isomorphic.
#     colorref_smallexample_6_15 : 0 and 1 are isomorphic, as well as 2 and 3. Graphs 4 and 5 are isomorphic (yet remain undecided after color refinement), and all other pairs of graphs are not isomorphic


# Preferably automatically in some way.
# Below test it manually for now:

# file = 'colorref_smallexample_4_7'
# file = 'colorref_smallexample_4_16'
file = 'colorref_smallexample_6_15'
# file = 'colorref_smallexample_2_49'
filename = 'test_graphs/color_refinement/' + file + '.grl'

with open(filename) as f:
    L = load_graph(f, read_list=True)

print(file)
for i in range(0, len(L[0])):
    for j in range(0, i):
        print ('{}, {}, (is_balanced, is_bijected), {}'.format(str(j), str(i), is_balanced_or_bijected(color_refinement(L[0][i]+L[0][j]))))