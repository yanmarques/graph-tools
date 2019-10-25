"""
This module provides functions to 4 different graph representations, in the following:
    - Adjacent matrix
    - Incidence matrix
    - Edge list
    - Adjacent list
"""


from data_structures import Graph, Edge


def edge_list(graph: Graph):
    if graph.is_weighted: # weighted graphs is simpler
        return [[*edge.pair, edge.value] for edge in graph.edges]

    edge_list = list()
    for edge in graph.edges:
        # start connection count number
        value = 1

        # try to match the edge already mapped on list
        index = _get_list_index(edge, edge_list)

        if index == -1: # no edges found, create it
            edge_list.append([*edge.pair, value])
        else:   # sum the present connections value and save
            value += edge_list[index][2]
            edge_list[index][2] = value

    return edge_list


def adjacent_matrix(graph: Graph):
    # create the squared matrix filled with an insignificant number
    matrix = structured_matrix(len(graph.vertices))

    for edge in graph.edges:
        # get vertices and indexes
        line_vertice, line_index, \
            column_vertice, column_index = _retrieve_edge_info(edge, graph)

        if graph.is_weighted:   # change value if highest
            current_weight = matrix[line_index][column_index]
            if edge.value > current_weight:
                matrix[line_index][column_index] = edge.value
                if not graph.is_oriented:
                    matrix[column_index][line_index] = edge.value
        else:   # appends a new path, this make works for multi edges too
            matrix[line_index][column_index] += 1
            matrix[column_index][line_index] += 1
    return matrix


def adjacent_list(graph: Graph):
    # create a list with the vertices length
    adjacent_list = structured_matrix(len(graph.vertices), column_size=0)
    
    for edge in graph.edges:
        incoming_vertice, incoming_index, \
            target_vertice, target_index = _retrieve_edge_info(edge, graph)
        # print(incoming_vertice, incoming_index, target_vertice, target_index)
        if graph.is_oriented:   # save the outgoing neighbour vertice, following vertice order
            adjacent_list[incoming_index].append(target_vertice)
        else:
            if incoming_vertice != target_vertice:  # do not save loops
                # append the outgoing neighbour
                adjacent_list[incoming_index].append(target_vertice)
            # append the incoming vertice
            adjacent_list[target_index].append(incoming_vertice)
    return adjacent_list


def incidence_matrix(graph: Graph):
    matrix = structured_matrix(len(graph.vertices), column_size=len(graph.edges))

    for index, edge in enumerate(graph.edges):
        # get vertices, edges and indexes
        vertice_one, index_one, \
            vertice_two, index_two = _retrieve_edge_info(edge, graph)

        if graph.is_oriented:
            # use a value to handle weighted grafs, ignore by default
            multiplier_value = 1
            if graph.is_weighted:
                # set edge's value
                multiplier_value = edge.value

            matrix[index_one][index] = 1 * multiplier_value    # exit vertice
            if index_one != index_two:  # loops only diverges
                matrix[index_two][index] = -1 * multiplier_value   # enters vertice
        else:
            # appends the ajacent vertice, this make works with loops
            matrix[index_one][index] += 1
            matrix[index_two][index] += 1
    return matrix


def is_graph(graph: Graph):
    if not len(graph.edges):
        return False

    if graph.is_oriented:
        return True

    adj_list = adjacent_list(graph)
    degrees = (len(vertices) for vertices in adj_list)
    odds = 0
    for d in degrees:
        if d % 2 != 0:
            odds += 1
    return odds % 2 == 0


def maybe_remove_duplicate_edges(graph: Graph):
    if graph.is_oriented:
        return graph

    new_edges = []
    for edge in graph.edges:
        if find_edge(edge.pair, new_edges) is None:
            new_edges.append(edge)

    graph.edges = new_edges
    return graph


def structured_matrix(line_size, column_size=None, padding=0):
    line_sequence = range(line_size)

    if column_size is None: # using a squared matrix
        column_size = line_size
    column_sequence = range(column_size)

    return [[padding for _ in column_sequence] for i in line_sequence]


def find_edge(target_pair, edge_list):
    pair = set(target_pair)
    for edge in edge_list:
        if pair == set(edge.pair):
            return edge
    return None


def _get_list_index(target: Edge, pair_list, default=-1):
    pair = set(target.pair)
    for index, edge in enumerate(pair_list):
        if pair == set(edge):
            return index
    return default


def _retrieve_edge_info(edge: Edge, graph: Graph):
    primary = edge.pair[0]
    secondary = edge.pair[1]
    vertices = graph.vertices
    return primary, vertices.index(primary), secondary, vertices.index(secondary)
