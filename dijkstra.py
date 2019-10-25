import math
from dataclasses import dataclass

import logger
import modeler
from util import read_choices, show_banner
from repr_types import adjacent_list, adjacent_matrix


_logger = logger.get_logger('dijkstra')


@dataclass
class DijkstraItem:
    vertice: str
    index: int
    path: str
    metric: int


def main():
    graph = modeler.parse_arguments()
    choices = graph.vertices
    index = read_choices('What is the vertice to start', choices)
    vertice = choices[index]
    _logger.info('starting from vertice: %s', vertice)    
    printer = map(_logger.info, search(graph, vertice))
    show_banner('Dijkstra items from search', separator='@')
    list(printer)


def load_vertice_items(graph, source_vertice):
    all_items = {}
    for index, vertice in enumerate(graph.vertices):
        all_items[vertice] = DijkstraItem(vertice=vertice,
                                        index=index,
                                        path=None,
                                        metric=math.inf)
    all_items[source_vertice].metric = 0
    return all_items
    

def search(graph, source_vertice):
    graph_adj_list = adjacent_list(graph)
    graph_adj_matrix = adjacent_matrix(graph)

    all_items = load_vertice_items(graph, source_vertice)
    
    queue = all_items.copy() 
    queue = sorted(queue, key=lambda k: queue[k].metric, reverse=True)
    _logger.debug('queue: %s', queue) 

    while len(queue):
        min_vertice = queue.pop()
        current_v = all_items[min_vertice]
        _logger.debug('vertice item: %s', current_v)
        for neighbour in graph_adj_list[current_v.index]:
            _logger.debug('vertice: %s', neighbour)
            neighbour_index = all_items[neighbour].index
            len_between_vertices = graph_adj_matrix[current_v.index][neighbour_index]
            
            alt_len = current_v.metric + len_between_vertices
            current_length = all_items[neighbour].metric            
            
            if alt_len < current_length:                      
                all_items[neighbour].metric = alt_len
                all_items[neighbour].path = current_v.vertice
                _logger.debug('new info: %s', all_items[neighbour])
            _logger.debug('queue: %s', queue)
    return iter(all_items.values())


if __name__ == '__main__':
    main()