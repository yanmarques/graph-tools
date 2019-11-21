import logger
import modeler
import contextual_modeler
from roads import mount_road, load_from_file, dump_roads
from util import read_choices, prompt_forever, read_float
from data_structures import Edge, TransactionContext


_logger = logger.get_logger(__file__)


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
            road_choice = prompt_forever('This info sounds good?', mount_road)
        distance = read_float('Road distance')
        if road_choice is None or distance is None:
            _logger.error('Any road choosed or invalid distance, aborting edge')
            return edge_context
        road_attrs.append(road_choice)
        weight = -1 * (road_choice.weight * distance)

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


if __name__ == '__main__':
    main()

