import math
import logger
import modeler
from repr_types import adjacent_list, adjacent_matrix, find_edge
from util import show_banner, display_table
from dijkstra import load_vertice_items
from kruskal import spanning_tree_graph


_logger = logger.get_logger('prim_jarnik')


def main():
    graph = spanning_tree_graph()
    assert not graph.is_oriented, '[-] Minimum spanning trees requires non-oriented graphs'
    printer = map(_logger.info, min_spanning_tree(graph))
    show_banner('Results from Prim-Jarnik algo')
    list(printer)


def min_spanning_tree(graph):
    adj_matrix = adjacent_matrix(graph)
    adj_list = adjacent_list(graph)
    queue = sorted(graph.vertices, reverse=True)
    _logger.debug('queue: %s', queue) 
    all_items = load_vertice_items(graph, queue[-1])
    
    while len(queue):
        curr_vertice = queue.pop()
        curr_item = all_items[curr_vertice]
        _logger.debug('vertice: %s', curr_vertice)
        for adj_vertice in adj_list[curr_item.index]:
            _logger.debug('adjacent_vertice: %s', adj_vertice)
            if not adj_vertice in queue:
                continue
            adj_item = all_items[adj_vertice]
            new_metric = adj_matrix[curr_item.index][adj_item.index]
            _logger.debug('new metric: %d', new_metric)
            _logger.debug('adjacent item: %s', adj_item)
            if new_metric < adj_item.metric:
                adj_item.path = curr_vertice
                adj_item.metric = new_metric
                _logger.debug('new info: %s', all_items[adj_vertice])
        queue.sort(key=lambda k: all_items[k].metric, reverse=True)
        if curr_item.path is not None:
            adj_vertice = curr_item.path
            yield find_edge((curr_vertice, adj_vertice), graph.edges)


if __name__ == '__main__':
    main()