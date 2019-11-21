import math

import modeler
from util import read_choices


TYPE_ORIENTED = 'oriented'
TYPE_NON_ORIENTED = 'non-oriented' 


class Graph:
    def __init__(self, type, valued, v, e):
        self.type = type
        self.valued = valued
        self.vertices = v
        self.arestas = e
        self.oriented = type == TYPE_ORIENTED

        self.listaAdjacencia = self.listaAdjacencia()

    def listaAdjacencia(self):
        adjacencia = {}
        for vertice in self.vertices:
            adjacencia[vertice] = []  
            for aresta in self.arestas:
                if (vertice in aresta) :
                    if (self.type == TYPE_NON_ORIENTED):
                        if (vertice == aresta[0]):
                            adjacencia[vertice].append(aresta[1])
                        else:
                            adjacencia[vertice].append(aresta[0])
                    
                    if (self.type == TYPE_ORIENTED and aresta[0] == vertice):
                        adjacencia[vertice].append(aresta[1])
        return adjacencia

    def distancia(self, a, b):
        for aresta in self.arestas:
            if (self.valued is not True):
                aresta[2] = 1

            if (self.oriented):
                if (aresta[0] == a and aresta[1] == b):
                    return aresta[2]

            if (aresta[0] == a and aresta[1] == b):
                return aresta[2]
            if (aresta[1] == a and aresta[0] == b):
                return aresta[2]


    def djikstra(self, origem):
        dist = {}
        previous = {}
        for vertice in self.vertices:
            previous[vertice] = None
            dist[vertice] = 0

        dist[origem] = None
        fila = [origem] + list(set(self.vertices) - set(origem))    
        
        while len(fila) > 0:
            u = fila[0]
            fila.remove(u)
            for vizinho in self.listaAdjacencia[u]:
                distanciaAtual = self.distancia(u, vizinho)
                if dist[u] is not None:
                    distanciaAtual += dist[u]
                if dist[vizinho] is not None and distanciaAtual > dist[vizinho]:
                    dist[vizinho] = distanciaAtual
                    previous[vizinho] = u
            fila.sort(key=lambda x: dist[x])
        
        for i in dist:
            yield { "vertice": i, "distancia": dist[i], "anterior": previous[i] }


def main(yan_graph=None):
    yan_graph = yan_graph or modeler.parse_arguments()
    
    choices = yan_graph.vertices
    index = read_choices('What is the vertice to start', choices)
    vertice = choices[index]
    
    edges = [list(e.pair) + [e.value] for e in yan_graph.edges]
    lucas_graph = Graph(type=TYPE_ORIENTED if yan_graph.is_oriented else TYPE_NON_ORIENTED,
                        valued=yan_graph.is_weighted,
                        v=yan_graph.vertices,
                        e=edges)
        
    for v in lucas_graph.djikstra(vertice):
        print(v)


if __name__ == '__main__': 
    main()