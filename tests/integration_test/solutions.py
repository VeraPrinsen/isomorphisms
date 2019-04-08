# Data structure that holds all solutions for the GI problem
isomorphism_solution = {}
# Data structure that holds all solutions for the count iso- and automorphism problem
automorphism_solution = {}

# Color-refinement test graphs
isomorphism_solution['colorref_smallexample_2_49'] = [(0, 1)]
isomorphism_solution['colorref_smallexample_4_7'] = [(1, 3), (0, 2)]
isomorphism_solution['colorref_smallexample_6_15'] = [(0, 1), (2, 3), (4, 5)]
isomorphism_solution['colorref_smallexample_4_16'] = [(0, 1), (2, 3)]

automorphism_solution['colorref_smallexample_2_49'] = {0: 1, 1: 1}
automorphism_solution['colorref_smallexample_4_7'] = {0: 2, 1: 1, 2: 2, 3: 1}
automorphism_solution['colorref_smallexample_6_15'] = {0: 1, 1: 1, 2: 1, 3: 1, 4: 6, 5: 6}
automorphism_solution['colorref_smallexample_4_16'] = {0: 4, 1: 4, 2: 1, 3: 1}

# Individualization refinement test graphs
isomorphism_solution['torus24'] = [(0, 3), (1, 2)]
isomorphism_solution['trees90'] = [(0, 3), (1, 2)]
isomorphism_solution['products72'] = [(0, 6), (1, 5), (2, 3), (4, 7)]
isomorphism_solution['cographs1'] = [(0, 3), (1, 2)]
isomorphism_solution['bigtrees1'] = [(0, 2), (1, 3)]
isomorphism_solution['torus144'] = [(0, 6), (1, 7), (2, 4), (3, 10), (5, 9), (8, 11)]
isomorphism_solution['trees36'] = [(0, 7), (1, 4), (2, 6), (3, 5)]
isomorphism_solution['modulesC'] = [(0, 7), (1, 5), (2, 4), (3, 6)]
isomorphism_solution['cubes5'] = [(0, 1), (2, 3)]
isomorphism_solution['bigtrees3'] = [(0, 2), (1, 3)]
isomorphism_solution['cubes6'] = [(0, 1), (2, 3)]

automorphism_solution['torus24'] = {0: 96, 1: 96, 2: 96, 3: 96}
automorphism_solution['trees90'] = {0: 6912, 1: 20736, 2: 20736, 3: 6912}
automorphism_solution['products72'] = {0: 288, 1: 576, 2: 576, 3: 576, 4: 864, 5: 576, 6: 288, 7: 864}
automorphism_solution['cographs1'] = {0: 5971968, 1: 995328, 2: 995328, 3: 5971968}
automorphism_solution['bigtrees1'] = {0: 442368, 1: 5308416, 2: 442368, 3: 5308416}
automorphism_solution['torus144'] = {0: 576, 1: 576, 2: 576, 3: 576, 4: 576, 5: 1152, 6: 576, 7: 576, 8: 576, 9: 1152, 10: 576, 11: 576}
automorphism_solution['trees36'] = {0: 2, 1: 6, 2: 2, 3: 6, 4: 6, 5: 6, 6: 2, 7: 2}
automorphism_solution['modulesC'] = {0: 17915904, 1: 17915904, 2: 2488320, 3: 2985984, 4: 2488320, 5: 17915904, 6: 2985984, 7: 17915904}
automorphism_solution['cubes5'] = {0: 3840, 1: 3840, 2: 24, 3: 24}
automorphism_solution['bigtrees3'] = {0: 2772351862699137701073289910157312, 1: 462058643783189616845548318359552, 2: 2772351862699137701073289910157312, 3: 462058643783189616845548318359552}
automorphism_solution['cubes6'] = {0: 96, 1: 96, 2: 46080, 3: 46080}

# Additional test instances
isomorphism_solution['Isom1'] = [(0, 2), (1, 3), (4, 6), (5, 7)]
isomorphism_solution['Isom2'] = [(0, 5), (1, 6), (2, 8), (3, 4), (7, 9)]
isomorphism_solution['Autom3'] = [(0, 5), (1, 2), (3, 4, 6)]

automorphism_solution['Autom1'] = {0: 3538944}
automorphism_solution['Autom2'] = {0: 9277129359360, 1: 1307993702400, 2: 2231764254720}
automorphism_solution['Autom3'] = {0: 32768, 1: 32768, 2: 32768, 3: 65536, 4: 65536, 5: 32768, 6: 65536}


