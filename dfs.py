from dataclasses import dataclass

import logger
import modeler
import repr_types
from util import show_banner


_logger = logger.get_logger('dfs')


@dataclass
class Board:
    visited: bool = False
    entry: str = None
    visit_timestamp: int = 0
    completed_timestamp: int = 0


def main():
    graph = modeler.parse_arguments()
    table, timestamp = dfs_search(graph) 
    printer = map(print, table)
    show_banner('Results from Deepth First Search')
    list(printer)
    _logger.info('total timestamp: %d', timestamp)


def dfs_search(graph):
    table = dict([(v, Board()) for v in graph.vertices])
    adjacent_list = repr_types.adjacent_list(graph)    

    def visit(exit_vertice, time, board):
        board.visited = True
        
        time += 1
        board.visit_timestamp = time
        
        def visit_and_store(vertice, *args):
            board.entry = vertice
            return visit(vertice, *args)
        
        index = graph.vertices.index(exit_vertice)
        time = cycle_visiting(adjacent_list[index], visit_and_store, time=time)
        
        time += 1
        board.completed_timestamp = time
        return time


    def cycle_visiting(vertices, callback, time=0):
        for vertice in vertices:    
            board = table[vertice]
            if not board.visited:
                time = callback(vertice, time, board)
        return time
    
    timestamp = cycle_visiting(graph.vertices, visit)
    return iter(table.values()), timestamp


if __name__ == '__main__':
    main()