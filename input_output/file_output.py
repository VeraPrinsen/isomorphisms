from supporting_components.graph_io import load_graph, write_dot
import subprocess
import os
import csv
import time


"""
Before you can use this module you must install graphviz on the terminal to be able to do this:
    https://stackoverflow.com/questions/1494492/graphviz-how-to-go-from-dot-to-a-graph
Install instructions:
    https://www.graphviz.org/download/
"""

# change dir to path of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath('../')
os.chdir(ROOT)


def load_graph_list_from_filepath(filepath):
    """
    Given a filepath, this method loads a list of graphs from that file
    :param filepath: The file the graphs should be extracted from
    :return: A list of graphs
        """
    with open(filepath) as f:
        L = load_graph(f, read_list=True)

    return L[0]


def load_graph_list(filename):
    """
    Given a filename, this method loads a list of graphs from that filename
    :param filename: The file the graphs should be extracted from
    :return: A list of graphs
    """
    return load_graph_list_from_filepath(ROOT + filename)


def save_graph_as_dot(G, filename):
    """
    This method saves a graph in a dot file.
    If folder /output_files/dot does not exist it is created
    :param G: The graph to be saved.
    :param filename: The filename in which the graph should be saved.
    """
    dot_filename = ROOT + '/output_files/dot/' + filename + '.dot'
    os.makedirs(os.path.dirname(dot_filename), exist_ok=True)

    with open(dot_filename, 'w') as g0:
        write_dot(G, g0)


def save_graph_in_png(filename):
    """
    This method can use a .dot file and transform it into a png image of the graph.
    If folder /output_files/dot or /output_files/png does not exist it is created using os.makedirs().
    :param filename: The filename of the .dot file without the extension, this will also be the filename for the .png file
    """
    dot_filename = ROOT + '/output_files/dot/' + filename + '.dot'
    png_filename = ROOT + '/output_files/png/' + filename + '.png'
    os.makedirs(os.path.dirname(dot_filename), exist_ok=True)
    os.makedirs(os.path.dirname(png_filename), exist_ok=True)

    subprocess.run(["dot", "-Tpng", dot_filename, "-o", png_filename])


def create_csv_file(name: 'String'):
    """
    Creates an empty CSV file with `sep=.` initializer part for Excel compatibility.
    The filename will be timestamped by prefixing name with the current time:
    example: YYYYMMDD-HH_MM_SS-name
    The path of the csv file, including extension .csv, is returned as String.
    If the folder output_files/csv does not exist it is created using os.makedirs().
    The argument newline = '' to prevent double carriage returns in non-binary mode.
    :param name: preferred name of the file
    :return: string csv_filename, path to the file
    """

    csv_filename = ROOT + '/output_files/csv/' + time.strftime('%Y%m%d-%H_%M_%S') + '-' + name + '.csv'
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    with open(csv_filename, 'w', newline='') as csv_init:
        # Python converts \n to OS specific newline.
        csv_init.write('sep=,\n')

    return csv_filename


def write_csv_line(csv_filename: 'String', col_strlist: 'List[String]'):
    """
    Appends a csv line to a file.
    Uses Excel compatible delimiter, quotechar and quoting.
    The argument newline = '' to prevent double carriage returns in non-binary mode.
    :param csv_filename:
    :param col_strlist:
    :return:
    """
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(col_strlist)

