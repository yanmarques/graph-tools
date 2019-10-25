from dataclasses import asdict
import argparse
import json
import secrets
import os

import logger
from contextual_modeler import model_graph_vertices
from data_structures import Graph, Edge
from util import read_text, read_choices, display_table, show_banner
from repr_types import maybe_remove_duplicate_edges, is_graph


_logger = logger.get_logger('modeler')


def mount_graph():
    name = read_text('Name [%random]', 
                    max_attempts=1,
                    throlling_message='Creating a random name...')
    if name is None:
        name = secrets.token_hex(6)

    _logger.info('graph name: %s', name)

    graph_type_choices = ['not-oriented', 'oriented']
    graph_type = read_choices('What is the graph type?', graph_type_choices,
                        throlling_message='Falling back to non-oriented...',
                        max_attempts=1)

    _logger.info('graph type: %s', graph_type_choices[graph_type])

    binary_choices = ['no', 'yes']
    graph_weight = read_choices("Is graph's edge weighted?", binary_choices,
                        throlling_message='Using non-weighted...',
                        max_attempts=1)

    _logger.info('graph weighted: %s', binary_choices[graph_weight])

    return Graph(name=name,
                 is_oriented=graph_type == 1,
                 is_weighted=graph_weight == 1)


def create_graph_from_interaction():
    show_banner('Keep pressing ENTER fallbacks to defaults!')
    print("\nCreate graph>")

    def prompt_forever(message, return_value):
        binary_choices = ['yes', 'no']
        can_continue = False
        while not can_continue:
            value = return_value()
            print(value)
            choice = read_choices(message, binary_choices,
                            throlling_message='Assuming everything is ok...')
            can_continue = choice == 0
        return value

    graph = prompt_forever('This info sounds good til now?', mount_graph)
    _logger.info('graph created: %s', graph)

    def modeler():
        context = model_graph_vertices(graph=graph)
        return context.graph

    while True:
        graph = prompt_forever('New info sounds good?', modeler)
        _logger.info('graph modeled: %s', graph)
        if not is_graph(graph):
            _logger.info('The graph inserted could not exist. Improper edges!')
            _logger.info('Try it again.')
            graph.edges.clear()
            graph.vertices.clear()
        else:
            _logger.debug('graph exists')
            break

    return maybe_remove_duplicate_edges(graph)


def dumps(graph, directory=''):
    dict_repr = asdict(graph)
    filename = f'{graph.name}.json'

    # handle a target directory
    if directory:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        filename = os.path.join(directory, filename)

    with open(filename, 'w') as writer:
        writer.write(json.dumps(dict_repr, indent=4))
    _logger.debug(f'graph was written to: {filename}')


def read_graph(io_wrapper):
    content = json.load(io_wrapper)
    io_wrapper.close()

    graph = Graph(name=content['name'], is_oriented=content['is_oriented'],
                  is_weighted=content['is_weighted'], vertices=content['vertices'])

    _logger.debug('graph reborned: %s', graph)

    for edge in content['edges']:
        pair = Edge(tuple(edge['pair']), value=edge['value'])
        _logger.debug('edge reborned: %s', pair)
        graph.edges.append(pair)
    return graph
    

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', help='Be moderatly verbose.',
                        default=False, action='store_true')

    parser.add_argument('-d', '--graph-directory', help='''Directory for saving
                        file graphs (default: dataset/)''', default='dataset/')

    parser.add_argument('-f', '--file-graph', help='Read graph file.',
                        type=argparse.FileType('rb'))

    args = parser.parse_args()

    logger.setup(args.verbose)

    if args.file_graph is not None:
        _logger.info('reading graph from file: %s', args.file_graph)
        graph = read_graph(args.file_graph)
    else:
        graph = create_graph_from_interaction()
        _logger.info('saving graph to file at: %s', args.graph_directory)
        dumps(graph, directory=args.graph_directory)
    return graph
