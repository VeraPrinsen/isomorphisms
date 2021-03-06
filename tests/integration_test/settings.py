"""
SETTINGS OF OUTPUT
Choose which outputs you want to produce
"""
# When set to true, passed tests are shown on the console
console_pass = True
# When set to true, test results are written to a csv file
write_to_csv = True

"""
RUN MODE
"""
# There are different modes to evaluate the graphs
# 1) Test mode - Run all files and check (if available) if the solutions are right
# 2) Tournament mode - Create output on the console as prescribed by the Project Guide
run_mode = 1

# Set this parameter to the right setting to indicate which problem to solve
# 1) Graph Isomorphism Problem - Determine if two different graphs are isomorphic
# 2) Count Isomorphisms - 1) and count the amount of isomorphisms of isomorphic graphs
# 3) Count Automorphisms - Count automorphisms within one graph
problem = 1

"""
SETTINGS OF ALGORITHM
"""
# Choose which preprocessing steps you want to have by turning them to True
simple_cases = True
twin_removal = True
tree_algorithm = True
complement = True

# Choose a color refinement algorithm
# 1 - normal color refinement
# 2 - fast color refinement
color_refinement_algorithm = 2

# Choose a branching algorithm
# 1 - normal branching
# 2 - fast branching
branching_algorithm = 2