import heapq

def astar(graph, start, end, heuristic):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, end)

    while open_heap:
        current = heapq.heappop(open_heap)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph[current]:
            tentative_g = g_score[current] + graph[current][neighbor]
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    return None
