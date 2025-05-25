import heapq

def dijkstra(graph, start, end):
    """Dijkstra's algorithm for finding shortest path
    
    Args:
        graph: Dictionary of dictionaries representing the road network
        start: Start node (lon, lat)
        end: End node (lon, lat)
        
    Returns:
        Tuple of (path, cost) or (None, inf) if no path found
    """
    queue = [(0, start, [])]
    visited = set()
    
    while queue:
        cost, node, path = heapq.heappop(queue)
        
        if node not in visited:
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return path, cost
            
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
    
    return None, float('inf')
