import heapq

def gbfs(graph, start, end, heuristic):
    """Greedy Best-First Search algorithm
    
    Args:
        graph: Dictionary of dictionaries representing the road network
        start: Start node (lon, lat)
        end: End node (lon, lat)
        heuristic: Function to estimate distance between nodes
        
    Returns:
        List of points representing the path, or None if no path found
    """
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, end), start))
    
    came_from = {}
    visited = set()

    while open_heap:
        current = heapq.heappop(open_heap)[1]

        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_heap, (heuristic(neighbor, end), neighbor))

    return None
