from src.map_loader import parse_osm
from src.graph import build_graph
from src.algorithms.dijkstra import dijkstra
from src.visualizer import plot_map

# Load data
nodes, ways = parse_osm('data/uttarakhand/dehradun.osm')
graph = build_graph(ways)

# Sample coordinates (Clock Tower to IMA)
start = (78.0322, 30.3165)  # Lon, Lat
end = (77.9928, 30.3625)

# Find path
path, cost = dijkstra(graph, start, end)
print(f"Path cost: {cost:.2f} units")

# Visualize
plot_map(ways, path)
