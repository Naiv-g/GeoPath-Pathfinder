import os
import logging
from flask import Flask, render_template, request, jsonify
from math import sqrt
from utils.map_parser import parse_osm
from utils.graph import RoadGraph
from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from algorithms.gbfs import gbfs

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dehradun-pathfinder-secret")

# Setup paths
OSM_FILE = r"attached_assets\dehradun.osm"

# Global variables to store map data
nodes = {}
ways = []
graph = None

def initialize_data():
    """Initialize map data and graph"""
    global nodes, ways, graph
    try:
        logger.info(f"Parsing OSM file: {OSM_FILE}")
        nodes, ways = parse_osm(OSM_FILE)
        graph = RoadGraph()
        
        # Build the graph
        for road in ways:
            for i in range(len(road)-1):
                u = road[i]
                v = road[i+1]
                # Calculate Euclidean distance as weight
                distance = sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2)
                graph.add_edge(u, v, distance)
        
        logger.info(f"Graph built successfully with {len(graph.adj_list)} nodes")
        return True
    except Exception as e:
        logger.error(f"Error initializing data: {str(e)}")
        return False

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/map-data')
def get_map_data():
    """Return the map data (roads) for initial display"""
    global ways
    return jsonify({
        'roads': ways,
        'bounds': get_map_bounds()
    })

def get_map_bounds():
    """Calculate map bounds for initial view"""
    global ways
    all_points = [point for road in ways for point in road]
    
    if not all_points:
        # Default to Dehradun center if no points
        return {
            'minLon': 78.0300, 'maxLon': 78.0600,
            'minLat': 30.3100, 'maxLat': 30.3400
        }
    
    min_lon = min(p[0] for p in all_points)
    max_lon = max(p[0] for p in all_points)
    min_lat = min(p[1] for p in all_points)
    max_lat = max(p[1] for p in all_points)
    
    return {
        'minLon': min_lon, 'maxLon': max_lon,
        'minLat': min_lat, 'maxLat': max_lat
    }

@app.route('/api/find-path', methods=['POST'])
def find_path():
    """Find a path between two points using the selected algorithm"""
    global graph
    
    data = request.json
    start = tuple(data['start'])  # [lon, lat]
    end = tuple(data['end'])      # [lon, lat]
    algorithm = data['algorithm']
    
    # Find nearest nodes in the graph
    start_node = find_nearest_node(start)
    end_node = find_nearest_node(end)
    
    if not start_node or not end_node:
        return jsonify({'error': 'Invalid start or end point'}), 400
    
    # Calculate path using selected algorithm
    try:
        heuristic = lambda a, b: sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
        
        if algorithm == 'astar':
            path = astar(graph.adj_list, start_node, end_node, heuristic)
        elif algorithm == 'dijkstra':
            path, _ = dijkstra(graph.adj_list, start_node, end_node)
        elif algorithm == 'gbfs':
            path = gbfs(graph.adj_list, start_node, end_node, heuristic)
        else:
            return jsonify({'error': 'Invalid algorithm selected'}), 400
        
        if not path:
            return jsonify({'error': 'No path found'}), 404
        
        # Calculate total distance
        total_distance = sum(
            sqrt((path[i][0]-path[i+1][0])**2 + (path[i][1]-path[i+1][1])**2)
            for i in range(len(path)-1)
        )
        
        # Calculate estimated time (assuming 40 km/h average speed)
        # Converting distance to kilometers (rough approximation)
        distance_km = total_distance * 111  # 1 degree ≈ 111 km
        time_hours = distance_km / 40
        time_minutes = time_hours * 60
        
        return jsonify({
            'path': path,
            'metrics': {
                'distance': total_distance,
                'distance_km': distance_km,
                'time_minutes': time_minutes
            }
        })
    
    except Exception as e:
        logger.error(f"Pathfinding error: {str(e)}")
        return jsonify({'error': f'Pathfinding failed: {str(e)}'}), 500

def find_nearest_node(point):
    """Find the nearest node in the graph to the given point"""
    global graph
    
    if not graph or not graph.adj_list:
        return None
    
    return min(
        graph.adj_list.keys(),
        key=lambda p: sqrt((p[0]-point[0])**2 + (p[1]-point[1])**2)
    )

@app.route('/api/nearest-node', methods=['POST'])
def get_nearest_node():
    """Find the nearest node in the graph to the given point"""
    data = request.json
    point = tuple(data['point'])  # [lon, lat]
    
    nearest = find_nearest_node(point)
    
    if nearest:
        return jsonify({'node': nearest})
    else:
        return jsonify({'error': 'No nodes available'}), 404

if __name__ == '__main__':
    if initialize_data():
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.critical("Failed to initialize data, application cannot start")
