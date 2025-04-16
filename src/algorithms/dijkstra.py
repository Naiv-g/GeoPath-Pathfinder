import heapq

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return path, cost
            
            for neighbor, weight in graph.adj_list[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
    
    return None, float('inf')
