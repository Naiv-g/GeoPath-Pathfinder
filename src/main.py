import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import xml.etree.ElementTree as ET
from collections import defaultdict
import heapq
from math import sqrt

# Configure paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "uttarakhand"
OSM_FILE = DATA_DIR / "dehradun.osm"

# Add project root to Python path
sys.path.append(str(BASE_DIR))

class RoadGraph:
    def __init__(self):
        self.adj_list = defaultdict(dict)
    
    def add_edge(self, u, v, weight):
        self.adj_list[u][v] = weight
        self.adj_list[v][u] = weight  # Bidirectional

def parse_osm(osm_path):
    """Parse OSM XML file and extract road network"""
    tree = ET.parse(osm_path)
    root = tree.getroot()

    nodes = {}
    ways = []

    # Extract nodes
    for node in root.findall('node'):
        nodes[node.get('id')] = (
            float(node.get('lon')),
            float(node.get('lat'))
        )

    # Extract roads
    for way in root.findall('way'):
        if any(tag.get('k') == 'highway' for tag in way.findall('tag')):
            road = []
            for nd in way.findall('nd'):
                node_id = nd.get('ref')
                if node_id in nodes:
                    road.append(nodes[node_id])
            if len(road) > 1:
                ways.append(road)

    return nodes, ways

def astar(graph, start, end, heuristic):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    
    while open_heap:
        current_cost, current = heapq.heappop(open_heap)
        
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
                f_score = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_heap, (f_score, neighbor))
    
    return None

class PathfinderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Dehradun Pathfinder")
        self.master.geometry("1200x800")
        
        # Verify OSM file exists
        if not OSM_FILE.exists():
            self.show_file_error()
            return
        
        # Initialize state
        self.nodes, self.ways = parse_osm(OSM_FILE)
        self.graph = RoadGraph()
        self.build_graph()
        self.start_node = None
        self.end_node = None
        self.current_path = None
        
        # Setup UI
        self.create_widgets()
        self.setup_map()
        self.connect_events()

    def show_file_error(self):
        error_msg = (
            f"Required map file not found at:\n{OSM_FILE}\n\n"
            "Please:\n"
            "1. Create folder: GeoPath-Pathfinder/data/uttarakhand/\n"
            "2. Download from: https://download.geofabrik.de/asia/india/uttarakhand-latest.osm.pbf\n"
            "3. Rename to 'dehradun.osm'"
        )
        messagebox.showerror("Missing Map File", error_msg)
        self.master.destroy()

    def create_widgets(self):
        """Create GUI components"""
        # Control panel
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Algorithm selection
        self.algorithm = ttk.Combobox(control_frame, values=["A*", "Dijkstra", "GBFS"])
        self.algorithm.current(0)
        self.algorithm.pack(side=tk.LEFT, padx=5)

        # Control buttons
        ttk.Button(control_frame, text="Set Start", command=self.set_start_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Set End", command=self.set_end_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Find Path", command=self.find_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reset View", command=self.reset_view).pack(side=tk.RIGHT, padx=5)

        # Map display
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master)
        self.toolbar.update()

    def build_graph(self):
        """Construct road network graph"""
        for road in self.ways:
            for i in range(len(road)-1):
                u = road[i]
                v = road[i+1]
                distance = sqrt((u[0]-v[0])**2 + (u[1]-v[1])**2)
                self.graph.add_edge(u, v, distance)
                self.graph.add_edge(v, u, distance)
            
    def setup_map(self):
        """Initialize map visualization"""
        self.ax.clear()
        for road in self.ways:
            x = [p[0] for p in road]
            y = [p[1] for p in road]
            self.ax.plot(x, y, 'gray', linewidth=0.5, alpha=0.7)
        self.ax.set_title("Dehradun Road Network")
        self.canvas.draw()

    def connect_events(self):
        """Connect matplotlib events"""
        self.canvas.mpl_connect('button_press_event', self.on_map_click)
        self.canvas.mpl_connect('scroll_event', self.on_zoom)
        self.canvas.mpl_connect('button_press_event', self.on_pan_start)
        self.canvas.mpl_connect('button_release_event', self.on_pan_end)
        self.canvas.mpl_connect('motion_notify_event', self.on_pan_move)

    def on_pan_start(self, event):
        """Start panning with middle mouse button"""
        if event.button == 2:  # Middle mouse button
            self.pan_start = (event.x, event.y)

    def on_pan_end(self, event):
        """End panning"""
        self.pan_start = None

    def on_pan_move(self, event):
        """Handle panning"""
        if self.pan_start and event.inaxes:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.ax.set_xlim(self.ax.get_xlim() - dx * 0.02)
            self.ax.set_ylim(self.ax.get_ylim() + dy * 0.02)
            self.canvas.draw()
            self.pan_start = (event.x, event.y)

    def on_zoom(self, event):
        """Handle zoom with mouse wheel"""
        if event.inaxes:
            scale = 1.1 if event.button == 'up' else 0.9
            self.ax.set_xlim(self.ax.get_xlim()[0] * scale, 
                            self.ax.get_xlim()[1] * scale)
            self.ax.set_ylim(self.ax.get_ylim()[0] * scale, 
                            self.ax.get_ylim()[1] * scale)
            self.canvas.draw()

    def set_start_mode(self):
        """Activate start point selection"""
        self.master.config(cursor="crosshair")
        self.selection_mode = "start"

    def set_end_mode(self):
        """Activate end point selection"""
        self.master.config(cursor="crosshair")
        self.selection_mode = "end"

    def on_map_click(self, event):
        """Handle map clicks for point selection"""
        if not event.inaxes or not hasattr(self, 'selection_mode'):
            return

        # Find nearest road node
        click_point = (event.xdata, event.ydata)
        nearest = min(self.graph.adj_list.keys(),
                     key=lambda p: sqrt((p[0]-click_point[0])**2 + (p[1]-click_point[1])**2))

        # Update visualization
        if self.selection_mode == "start":
            self.start_node = nearest
            self.ax.plot(nearest[0], nearest[1], 'go', markersize=8, zorder=3)
        else:
            self.end_node = nearest
            self.ax.plot(nearest[0], nearest[1], 'ro', markersize=8, zorder=3)

        self.canvas.draw()
        self.master.config(cursor="")
        self.selection_mode = None

    def find_path(self):
        """Calculate and display shortest path"""
        if not self.start_node or not self.end_node:
            messagebox.showwarning("Missing Points", "Please set both start and end points")
            return

        try:
            heuristic = lambda a, b: sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
            path = astar(self.graph.adj_list, self.start_node, self.end_node, heuristic)
            
            if path:
                self.draw_path(path)
                distance = sum(
                    sqrt((path[i][0]-path[i+1][0])**2 + (path[i][1]-path[i+1][1])**2)
                    for i in range(len(path)-1)
                )
                messagebox.showinfo("Path Found", f"Total distance: {distance:.2f} units")
            else:
                messagebox.showinfo("No Path", "No valid path found between selected points")
        except Exception as e:
            messagebox.showerror("Error", f"Pathfinding failed: {str(e)}")

    def draw_path(self, path):
        """Visualize the calculated path"""
        # Clear previous path
        if self.current_path:
            self.current_path.remove()
        
        x = [p[0] for p in path]
        y = [p[1] for p in path]
        self.current_path, = self.ax.plot(x, y, 'b-', linewidth=2, zorder=2)
        self.canvas.draw()

    def reset(self):
        """Reset all selections"""
        self.start_node = None
        self.end_node = None
        if self.current_path:
            self.current_path.remove()
            self.current_path = None
        self.ax.clear()
        self.setup_map()

    def reset_view(self):
        """Reset zoom to initial view"""
        self.ax.autoscale()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()