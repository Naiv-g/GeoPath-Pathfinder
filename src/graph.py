from collections import defaultdict

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(dict)

    def add_edge(self, u, v, weight):
        self.adj_list[u][v] = weight
        self.adj_list[v][u] = weight  # Bidirectional

def build_graph(ways):
    graph = Graph()
    for road in ways:
        for i in range(len(road)-1):
            u = road[i]
            v = road[i+1]
            # Calculate Euclidean distance as weight
            weight = ((u[0]-v[0])**2 + (u[1]-v[1])**2)**0.5
            graph.add_edge(u, v, weight)
    return graph
