from util import show_banner, display_table
import logger
import modeler
import repr_types


_logger = logger.get_logger('kruskal')


def spanning_tree_graph():
    graph = modeler.parse_arguments()
    assert graph.is_weighted, '[*] Minimum spanning trees requires weighted graphs.'
    return graph


def main():
    graph = spanning_tree_graph()
    printer = map(_logger.info, min_spanning_tree(graph))
    show_banner('Edges from Kruskal algo', separator='&')
    list(printer)


def min_spanning_tree(graph):
    all_items = {}

    for vertice in graph.vertices:
        all_items[vertice] = [vertice]

    adj_matrix = repr_types.adjacent_matrix(graph)
    queue = sorted(graph.edges, key=lambda e: e.value)
    _logger.debug('queue: %s', queue) 

    for edge in queue:
        _logger.debug('edge: %s', edge)
        item1 = all_items[edge.pair[0]]
        item2 = all_items[edge.pair[1]]
        if item1 == item2: continue
        item1.extend(item2)
        for vertice in item2:
            all_items[vertice] = item1
        yield edge


if __name__ == '__main__':
    main()