from algorithms.preprocessing import fix_degrees
from tests.integration_test.algorithm_options import apply_could_be_isomorphic, apply_remove_twins, apply_tree_algorithm, branching_method, apply_complement
from algorithms.color_initialization import degree_color_initialization
from supporting_components.graph import Graph

import sys

def preprocessing(G: "Graph"):
    """
    In this method all pre-processing is done that need to be done only one time. This method is called before any
    other computations are done.
    :param G: The graph to be preprocessed
    :return : A dictionary with preprocessed data:
                factor: the factor the amount of automorphisms need to be multiplied with
                complement: If it needed to be determined, this is a graph, otherwise this is None
    """
    preprocessed_data = {}

    fix_degrees(G)

    # Determine complement
    complement_applied, G_preprocessed = apply_complement(G)
    if complement_applied:
        fix_degrees(G_preprocessed)
        apply_remove_twins(G_preprocessed)
        preprocessed_data['complement'] = G_preprocessed
    else:
        preprocessed_data['complement'] = None

    # Twin removal
    factor = apply_remove_twins(G)
    preprocessed_data['factor'] = factor

    return preprocessed_data


def are_isomorph(G: "Graph", H: "Graph"):
    """
    This method determines if graph G and graph H have at least one isomorphism.
    :param G, H: The two graphs of which it must be determined if there is an isomorphism.
    :return: Boolean that indicates if graph G and H are isomorph or not.
    """
    # Test if graphs are isomorphic using simple properties of the graphs
    if not apply_could_be_isomorphic(G, H):
        return False

    # Check if the graph has disconnected graphs
    graphs_todoG=list()

    if G.is_disconnected():
        graphs_todoG.append(G.get_connected_subgraphs())
    else:
        graphs_todoG.append(G)

    graphs_todoH = list()
    if H.is_disconnected():
        graphs_todoH.append(H.get_connected_subgraphs())
    else:
        graphs_todoH.append(H)

    # One graph has more disconnected components than the other -> False
    if len(graphs_todoG) != len(graphs_todoH):
        return False

    if len(graphs_todoH) > 1:
        print('')
        print('parsing subgraphs...={}'.format(len(graphs_todoH)))
        print('len_H={}'.format(len(graphs_todoH)))
        filename='subgraphs'
        # Query for all combinations using the same root function
        graphsGH=  list(graphs_todoH + graphs_todoG)
        multiplication_factor, preprocessed_graphs, isomorphisms, automorphisms, skip = preprocess_graphs(graphsGH)
        # For each graph
        determine_isomorphic_pairs(graphsGH, filename, preprocessed_graphs, isomorphisms, skip)
        print(len(isomorphisms))
        if len(isomorphisms) == len(graphs_todoH):
            return True
        else:
            return False

    # If graph is a tree, use this algorithm to solve the GI problem
    problem_solved, is_isomorph = apply_tree_algorithm(G, H)
    if problem_solved:
        return is_isomorph

    # If GI problem is not solved, make a disjoint union of the graphs, color it and do branching
    G_disjoint_union = G + H
    degree_color_initialization(G_disjoint_union)

    return branching_method(G_disjoint_union, False)


def amount_of_automorphisms(G: "Graph"):
    """
    This method calculates the amount of isomorphisms there are between graph G and H.
    :param G, H: The two graphs of which the amount of isomorphisms must be determined.
    :return: Amount of isomorphisms graph G and H have.
    """
    # If graph is a tree, use this algorithm to solve the GI problem
    problem_solved, isomorph_count = apply_tree_algorithm(G)
    if problem_solved:
        return isomorph_count

    # Check if is disconnected
    is_disconnected = G.is_disconnected()
    print('is_disconnected?={}'.format(is_disconnected))

    graphs_todo = list()

    if is_disconnected:
        graphs_todo += G.get_connected_subgraphs()
    else:
        graphs_todo.append(G)

    results = 1

    # smallest first
    graphs_todo.sort(key=len)

    print('todo (sub)graphs:{}'.format(len(graphs_todo)))

    for G in graphs_todo:
        print(G)
        G_disjoint_union = G.self_disjoint_union()
        degree_color_initialization(G_disjoint_union)
        results = results * branching_method(G_disjoint_union, True)
        print(results)

    return results


def determine_isomorphic_pairs(graphs: "List[Graph]", filename, preprocessed_graphs, isomorphisms, skip):
    # In this first loop, for each combination, it is determined if they are isomorphic or not
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            s = filename + ": Determining if [" + str(i) + "," + str(j) + "] are isomorphic (out of " + str(
                len(graphs) - 1) + " graphs)"
            sys.stdout.write('\r' + s)

            # If both graphs are already in the result structure, they can be skipped
            if skip[i] and skip[j]:
                continue

            # Determine if the two graphs are isomorphic
            if bool(preprocessed_graphs[i]):
                G = preprocessed_graphs[i]
            else:
                G = graphs[i]
            if bool(preprocessed_graphs[j]):
                H = preprocessed_graphs[j]
            else:
                H = graphs[j]
            are_isomorph_actual = are_isomorph(G, H)

            # Only save results if the combination of graphs is isomorphic
            if are_isomorph_actual:
                # If one of the two graphs is already in a isomorphic pair, the other graph belongs to it too
                if skip[i] or skip[j]:
                    for pair in isomorphisms:
                        if i in pair:
                            pair.append(j)
                            skip[j] = True
                            break
                        elif j in pair:
                            pair.append(i)
                            skip[i] = True
                            break
                # Otherwise a new pair of isomorphisms should be added to the list
                else:
                    isomorphisms.append([i, j])
                    skip[i] = True
                    skip[j] = True

def preprocess_graphs(graphs):
    # Preprocessing that should be done once per graph
    # Twin removal - Complement
    multiplication_factor = [1 for _ in range(len(graphs))]
    preprocessed_graphs = {}
    for i in range(len(graphs)):
        preprocessed_data = preprocessing(graphs[i])
        # If complement was applied, the value of key 'complement' is the complement graph, otherwise it is None
        preprocessed_graphs[i] = preprocessed_data['complement']
        # If twin removal was applied, a factor > 1 could be returned and the amount of automorphisms should be
        # multiplied with it
        multiplication_factor[i] = preprocessed_data['factor']

    # Some data structures that are used to determine if graphs are isomorphic more efficiently
    isomorphisms = []  # List of lists that saves all isomorphic pairs (or more than 2, if that is the case)
    automorphisms = {}  # Dictionary that saves for each graph the amount of automorphisms
    skip = [False for _ in range(len(graphs))]  # To check if you can skip a cycle

    return multiplication_factor, preprocessed_graphs, isomorphisms, automorphisms, skip

def test_automorphisms(filename, graphs, multiplication_factor, isomorphisms, automorphisms, skip, problem):
    # If the problem to be resolved is the #Automorphism problem, all graphs need to be in de result, also those
    # that are not an isomorphism with any other graph. Those graphs will be added to the isomorphism result as
    # singular isomorphism groups
    if problem == 3:
        for i in range(len(skip)):
            if not skip[i]:
                isomorphisms.append([i])
    # For each set of isomorphisms, calculate the amount of automorphisms of the first graph. This can be done
    # because the graphs are isomorphic and the amount of isomorphisms are equal to the amount of automorphisms of the
    # independent graphs
    if problem == 2 or problem == 3:
        group_count = 0
        for pair in isomorphisms:
            group_count += 1
            s = filename + ": Calculating amount of isomorphisms of isomorphic group " + str(pair) + " (" + str(
                group_count) + " out of " + str(len(isomorphisms)) + " groups)"
            sys.stdout.write('\r' + s)
            amount_automorphisms_actual = multiplication_factor[pair[0]] * amount_of_automorphisms(graphs[pair[0]])
            # Each graph in the pair has the same amount of automorphisms
            for graph in pair:
                automorphisms[graph] = amount_automorphisms_actual
    sys.stdout.write('\r' + "Done evaluating " + filename)
    print('')
