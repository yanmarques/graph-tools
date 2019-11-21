import logger
import modeler
import contextual_modeler
import lucas_dijkstra
from roads import mount_road, load_from_file, dump_roads
from util import read_choices, prompt_forever, read_float
from data_structures import Edge, TransactionContext


_logger = logger.get_logger(__file__)

DEFAULT_WEIGHTS = {
    'road': 20,
    'distance': 10
}


@contextual_modeler.with_vertice('Adjacent vertice label',
                                throlling_message='Exited vertice.',
                                one_transaction=False)
def road_edge_builder(edge_context, pair):
    _logger.info('runnin-graph %s', edge_context.graph)
    vertice = edge_context.meta['vertice']
    weight = None

    if edge_context.graph.is_weighted:
        road_attrs = edge_context.meta['roads']
        choices = [r.road_name for r in road_attrs]
        road_choice = read_choices('Choose a road', choices, default=None, max_attempts=1)
        _logger.info('road choice: %s', road_choice)
        if road_choice is None:
            road = prompt_forever('This info sounds good?', mount_road)
            if road is not None:
                road_attrs.append(road)
        else:
            road = road_attrs[road_choice]
        distance = read_float('Road distance')
        if road is None or distance is None:
            _logger.error('Any road choosed or invalid distance, aborting edge')
            return edge_context
        
        default_road_weight = DEFAULT_WEIGHTS['road']
        real_road_weight = road.weight * default_road_weight
        default_distance_weight = DEFAULT_WEIGHTS['distance']
        real_distance_weight = (-1 * distance) * default_distance_weight
        weight = (real_road_weight * default_road_weight) + \
                (real_distance_weight * default_distance_weight) / sum(DEFAULT_WEIGHTS.values())
        if weight < 0:
            weight = 0

    edge = Edge((vertice, pair), value=weight)
    _logger.info(f'Creating edge {edge}...')
    edge_context.graph.edges.append(edge)
    return edge_context


def road_graph_modeler(graph):
    def wrapper():
        roads = load_from_file() or []
        initial_context = TransactionContext(graph=graph,
                                    meta={'roads': roads})

        recv_context = contextual_modeler.model_graph_vertices(context=initial_context)
        
        dump_roads(recv_context.meta['roads'])
        
        return recv_context.graph
    return wrapper


def main():
    # patch the edge builder
    contextual_modeler.edge_builder = road_edge_builder
    modeler.get_graph_modeler = road_graph_modeler

    graph = modeler.parse_arguments()
    _logger.info('created graph: %s', graph)

    lucas_dijkstra.main(yan_graph=graph)


if __name__ == '__main__':
    main()

