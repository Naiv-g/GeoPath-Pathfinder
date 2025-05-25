import heapq

def astar(graph, start, end, heuristic):
    """A* search algorithm implementation
    
    Args:
        graph: Dictionary of dictionaries representing the road network
        start: Start node (lon, lat)
        end: End node (lon, lat)
        heuristic: Function to estimate distance between nodes
        
    Returns:
        List of points representing the path, or None if no path found
    """
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, end)

    while open_heap:
        # Get node with lowest f_score
        current = heapq.heappop(open_heap)[1]

        # Check if we reached the end
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Reverse to get path from start to end

        # Explore neighbors
        for neighbor in graph[current]:
            # Calculate tentative g_score
            tentative_g = g_score[current] + graph[current][neighbor]
            
            # If this path is better than previous
            if tentative_g < g_score[neighbor]:
                # Update path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                # Add to open set if not already there
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    # No path found
    return None
