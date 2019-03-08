from supporting_components.graph_io import load_graph, write_dot
import subprocess
import os


"""
Before you can use this module you must install graphviz on the terminal to be able to do this:
    https://stackoverflow.com/questions/1494492/graphviz-how-to-go-from-dot-to-a-graph
Install instructions:
    https://www.graphviz.org/download/
"""

ROOT = os.path.abspath('../')


def load_graph_list(filename):
    """
    Given a filename, this method loads a list of graphs from that filename
    :param filename: The file the graphs should be extracted from
    :return: A list of graphs
    """
    with open(filename) as f:
        L = load_graph(f, read_list=True)

    return L[0]


def save_graph_as_dot(G, filename):
    """
    This method saves a graph in a dot file  .
    :param G: The graph to be saved.
    :param filename: The filename in which the graph should be saved.
    """
    dot_filename = ROOT + '/output_graphs/dot/' + filename + '.dot'
    with open(dot_filename, 'w') as g0:
        write_dot(G, g0)


def save_graph_in_png(filename):
    """
    This method can use a .dot file and transform it into a png image of the graph.
    :param filename: The filename of the .dot file without the extension, this will also be the filename for the .png file
    """
    dot_filename = ROOT + '/output_graphs/dot/' + filename + '.dot'
    png_filename = ROOT + '/output_graphs/png/' + filename + '.png'
    subprocess.run(["dot", "-Tpng", dot_filename, "-o", png_filename])