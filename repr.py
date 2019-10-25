import logging
import traceback

from modeler import parse_arguments
from util import display_table
from repr_types import (maybe_remove_duplicate_edges,
    adjacent_matrix,
    edge_list,
    adjacent_list,
    incidence_matrix,
    structured_matrix,
    is_graph)


def main():
    graph = parse_arguments()

    adj_headers = graph.vertices
    display_table('Adjacent matrix', adj_headers, adjacent_matrix(graph),
                  lines=adj_headers)

    incidence_headers = [str(edge.pair) for edge in graph.edges]
    display_table('Incidence matrix', incidence_headers, incidence_matrix(graph),
                  lines=adj_headers)

    adj_list = adjacent_list(graph)
    vertices_length = len(graph.vertices)
    
    # create a squared matrix to transpose from list, padding empty values
    adj_sqr_list = structured_matrix(vertices_length, padding='-')

    for line_index, pairs in enumerate(adj_list):
        for column_index, vertice in enumerate(pairs):
            adj_sqr_list[column_index][line_index] = vertice

    display_table('Adjacent list', adj_headers, adj_sqr_list)

    edge_list_headers = ['VERTICE', 'ADJACENT VERTICE']

    if graph.is_weighted:
        edge_list_headers.append('WEIGHT')
    else:
        edge_list_headers.append('CONNECTIONS')

    display_table('Edge lists', edge_list_headers, edge_list(graph), end="")


if __name__ == '__main__':
    main()
