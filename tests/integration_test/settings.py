"""
SETTINGS OF OUTPUT
Choose which outputs you want to produce
"""
# When set to true, failed tests are shown on the console
console_fail = True
# When set to true, passed tests are shown on the console
console_pass = True
# When set to true, test results are written to a csv file
write_to_csv = True

"""
TOURNAMENT SETTINGS
"""
# When set to true, test results are written to a csv file
tournament_write_to_csv = True
# Set this parameter to the right setting to indicate which algorithms to run
# 1) Graph Isomorphism Problem - Determine if two different graphs are isomorphic
# 2) Count Isomorphisms - Next to 1) also count the amount of isomorphisms
# 3) Count Automorphisms - Count automorphisms within one graph
problem = 3

"""
SETTINGS OF ALGORITHM
"""
# Choose which preprocessing steps you want to have by turning them to True
preprocessing_simple_cases = True
twin_removal = True

# Choose a color refinement algorithm
# 1 - normal color refinement
# 2 - fast color refinement
color_refinement_algorithm = 2

# Choose a branching algorithm
# 1 - normal branching
branching_algorithm = 1