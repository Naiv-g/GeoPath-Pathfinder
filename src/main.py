import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.map_loader import parse_osm
from src.graph import Graph
from src.algorithms import astar, gbfs, dijkstra
from map_loader import parse_osm


class PathfinderGUI:
    def __init__(self, master, osm_file):
        self.master = master
        self.master.title("Dehradun Pathfinder")
        
        # Load map data
        self.nodes, self.ways = parse_osm(osm_file)
        self.graph = self.build_graph()
        
        # GUI Setup
        self.figure = Figure(figsize=(10, 8))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Controls
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.algorithm = tk.StringVar(value="A*")
        tk.OptionMenu(control_frame, self.algorithm, "A*", "GBFS", "Dijkstra").pack(side=tk.LEFT)
        
        self.start_btn = tk.Button(control_frame, text="Set Start", command=lambda: self.set_mode("start"))
        self.start_btn.pack(side=tk.LEFT)
        
        self.end_btn = tk.Button(control_frame, text="Set End", command=lambda: self.set_mode("end"))
        self.end_btn.pack(side=tk.LEFT)
        
        self.run_btn = tk.Button(control_frame, text="Find Path", command=self.find_path)
        self.run_btn.pack(side=tk.LEFT)
        
        self.mode = None
        self.start_node = None
        self.end_node = None
        
        self.draw_base_map()

    def build_graph(self):
        g = Graph()
        for road in self.ways:
            for i in range(len(road)-1):
                u = tuple(road[i])
                v = tuple(road[i+1])
                weight = ((u[0]-v[0])**2 + (u[1]-v[1])**2)**0.5
                g.add_edge(u, v, weight)
        return g

    def draw_base_map(self):
        self.ax.clear()
        for road in self.ways:
            x = [p[0] for p in road]
            y = [p[1] for p in road]
            self.ax.plot(x, y, 'gray', linewidth=0.5)
        self.ax.set_title("Dehradun Road Network")
        self.canvas.draw()

    def set_mode(self, mode):
        self.mode = mode
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if not event.inaxes: return
        
        click_point = (event.xdata, event.ydata)
        nearest = min(self.graph.adj_list.keys(), 
                     key=lambda p: (p[0]-click_point[0])**2 + (p[1]-click_point[1])**2)
        
        if self.mode == "start":
            self.start_node = nearest
            self.ax.plot(nearest[0], nearest[1], 'go', markersize=8)
        else:
            self.end_node = nearest
            self.ax.plot(nearest[0], nearest[1], 'ro', markersize=8)
        
        self.canvas.draw()
        self.canvas.mpl_disconnect(self.on_click)

    def find_path(self):
        if not self.start_node or not self.end_node: return
        
        heuristic = lambda a, b: ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
        
        if self.algorithm.get() == "A*":
            path = astar.astar(self.graph.adj_list, self.start_node, self.end_node, heuristic)
        elif self.algorithm.get() == "GBFS":
            path = gbfs.gbfs(self.graph.adj_list, self.start_node, self.end_node, heuristic)
        else:
            path, _ = dijkstra.dijkstra(self.graph.adj_list, self.start_node, self.end_node)
        
        if path:
            x = [p[0] for p in path]
            y = [p[1] for p in path]
            self.ax.plot(x, y, 'b-', linewidth=2)
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderGUI(root, "data/uttarakhand/dehradun.osm")
    root.mainloop()

nodes, ways = parse_osm("data/india/dehradun-complete.osm")  # Updated path