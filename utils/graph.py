from collections import defaultdict

class RoadGraph:
    """Graph representation of a road network"""
    def __init__(self):
        self.adj_list = defaultdict(dict)
        
    def add_edge(self, u, v, weight):
        """Add an edge between nodes u and v with given weight"""
        self.adj_list[u][v] = weight
        self.adj_list[v][u] = weight  # Bidirectional
