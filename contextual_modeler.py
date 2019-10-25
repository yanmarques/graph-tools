from dataclasses import dataclass, field
from typing import Any

import logger
from data_structures import Graph, Edge, TransactionContext
from context import run_interactive_context
from util import read_text, read_int


_logger = logger.get_logger(__name__)


def with_vertice(message, throlling_message=None, one_transaction=True):
    def wrapper_fn(fn):
        def store_vertice_interceptor(context, vertice):
            context.graph = upsert_vertice(context.graph, vertice)
            return fn(context, vertice)

        def runner(**kwargs):
            next_context = TransactionContext(**kwargs)
            reader_predicate = text_reader(message=message,
                                           max_attempts=1,
                                           throlling_message=throlling_message)

            return run_interactive_context(next_context, reader_predicate,
                                           callback=store_vertice_interceptor,
                                           one_transaction=one_transaction)
        return runner
    return wrapper_fn


def text_reader(*args, **kwargs):
    def wrapper(context):
        vertice = read_text(*args, **kwargs)
        if vertice is None:
            return False

        vertices_list = vertice.strip().split()
        context.meta['total_size'] = len(vertices_list)

        return vertices_list
    return wrapper


@with_vertice('Adjacent vertice label',
              throlling_message='Exited vertice.',
              one_transaction=False)
def edge_builder(edge_context, pair):
    _logger.info('runnin-graph %s', edge_context.graph)
    vertice = edge_context.meta['vertice']
    weight = None

    if edge_context.graph.is_weighted:
        weight = read_int(f'[{vertice}->{pair}] Edge weight',
                          default=1,
                          max_attempts=1,
                          throlling_message='Using weight 1 by default.')

    edge = Edge((vertice, pair), value=weight)
    _logger.info(f'Creating edge {edge}...')
    edge_context.graph.edges.append(edge)
    return edge_context


@with_vertice('Vertice label', throlling_message='Vertices and edges created.')
def model_graph_vertices(context, vertice):
    # do nothing when creating a bunch of vertices
    # transaction will not be saved now, all vertices will
    # be created later in one big transaction
    if context.meta['total_size'] > 1:
        return context

    context.meta['vertice'] = vertice
    _logger.info('running-graph %s', context.graph)

    next_context = edge_builder(graph=context.graph,
                        meta=context.meta,
                        previous_context=context.previous_context)

    _logger.info('running-graph %s', context.graph)
    return next_context


def upsert_vertice(graph, vertice):
    if graph.has_vertice(vertice):
        _logger.info('Vertice %s already exists.', vertice)
    else:
        _logger.info('Creating vertice %s...', vertice)
        graph.vertices.append(vertice)
    return graph
