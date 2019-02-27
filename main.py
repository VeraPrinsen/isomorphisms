from supporting_components.graph_io import *
from algorithms.color_refinement import color_refinement

with open('test_graphs/color_refinement/colorref_smallexample_4_7.grl') as f:
    L = load_graph(f, read_list=True)

with open('output_graphs/colorref_smallexample_4_7_0.dot', 'w') as g0:
    write_dot(color_refinement(L[0][3]), g0)