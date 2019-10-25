"""
This module provides the main structures implementation
"""


from dataclasses import dataclass, field, asdict, make_dataclass
from typing import List, Any


@dataclass
class Edge:
    pair: List[int]
    value: int = None

    def clone(self):
        return Edge(pair=self.pair[:], value=self.value)

    def __post_init__(self):
        pair_size = len(self.pair)
        assert pair_size == 2, f'Wrong edge pair size [{pair_size}], expecting 2.'

    def __repr__(self):
        return f'EdgePair(pair=[{self.pair[0]}->{self.pair[1]}], value={self.value})'


@dataclass
class Graph:
    name: str
    is_oriented: bool
    is_weighted: bool
    vertices: list = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)

    def has_vertice(self, name):
        try:
            self.vertices.index(name)
        except ValueError:
            return False
        return True

    def clone(self):
        return Graph(name=self.name,
                     is_oriented=self.is_oriented,
                     is_weighted=self.is_weighted,
                     vertices=self.vertices.copy(),
                     edges=self.edges.copy())


@dataclass
class TransactionContext:
    graph: Graph
    previous_context: Any = None
    meta: dict = field(default_factory=dict)

    def clone(self):
        return TransactionContext(graph=self.graph.clone(),
                                  previous_context=self.previous_context,
                                  meta=self.meta.copy())
