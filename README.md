# 🗺️ GeoPath Visualizer: Real-World Pathfinding Visualizer

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

A comprehensive Flask-based web application that bridges theoretical pathfinding algorithms with real-world geographic challenges using authentic OpenStreetMap (OSM) data from Dehradun city.

## 🚀 Features

- **Interactive Web Interface**: Click-to-set start and end points on real Dehradun roads
- **Three Pathfinding Algorithms**: Compare A*, Dijkstra's, and Greedy Best-First Search
- **Real-time Visualization**: Animated route traversal with customizable speed controls
- **Performance Metrics**: Distance calculation, time estimation, and progress tracking
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Authentic Data**: Processes 654K+ real OpenStreetMap data points

## 🛠️ Technology Stack

### Frontend
- **HTML5 & CSS3**: Semantic structure with responsive design
- **JavaScript ES6+**: Modular function organization with async/await
- **Leaflet.js 1.9.4**: Interactive mapping with custom markers
- **Bootstrap 5.3.2**: Consistent UI components and responsive grid
- **Font Awesome 6.4.2**: Scalable vector icons

### Backend
- **Flask**: Lightweight web framework with RESTful API design
- **Python 3.11+**: Core algorithms and data processing
- **xml.etree**: OSM data parsing and validation
- **heapq**: Priority queue optimization for algorithms

## 📊 Algorithms Implemented

### 🎯 A* Search Algorithm
- **Optimality**: Guaranteed shortest path with admissible heuristic
- **Heuristic**: Euclidean distance estimation
- **Complexity**: O((V + E) log V)

### 🔄 Dijkstra's Algorithm
- **Approach**: Complete exploration with priority queue
- **Guarantee**: Shortest path to all reachable nodes
- **Use Case**: Baseline comparison for path optimality

### ⚡ Greedy Best-First Search
- **Strategy**: Heuristic-only pathfinding
- **Speed**: Fastest execution time
- **Purpose**: Educational comparison and algorithm analysis

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Naiv-g/GeoPath-Pathfinder/tree/revamp
cd GeoPath-Pathfinder
```

2. **Install dependencies**
```bash
pip install flask gunicorn
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
GeoPath-Pathfinder/
├── 📄 app.py                 # Main Flask application
├── 📁 algorithms/            # Pathfinding algorithms
│   ├── 📄 astar.py          # A* implementation
│   ├── 📄 dijkstra.py       # Dijkstra's implementation
│   └── 📄 gbfs.py           # Greedy Best-First Search
├── 📁 utils/                 # Utility modules
│   ├── 📄 graph.py          # Graph data structure
│   └── 📄 map_parser.py     # OSM data parsing
├── 📁 static/                # Frontend assets
│   ├── 📁 css/              # Stylesheets
│   └── 📁 js/               # JavaScript modules
├── 📁 templates/             # HTML templates
│   └── 📄 index.html        # Main interface
└── 📁 attached_assets/       # OSM data
    └── 📄 dehradun.osm      # 654K+ geographic data points
```

## 🎮 How to Use

1. **Select Algorithm**: Choose from A*, Dijkstra's, or Greedy Best-First Search
2. **Set Start Point**: Click "Set Start" and click anywhere on the map
3. **Set End Point**: Click "Set End" and select your destination
4. **Find Path**: Click "Find Path" to calculate and visualize the route
5. **Watch Animation**: Use animation controls to see step-by-step pathfinding
6. **Analyze Metrics**: View distance, time, and algorithm performance data

## 🎛️ API Endpoints

### GET `/api/map-data`
Returns OSM road network data and map bounds
```json
{
  "roads": [[[lon, lat], [lon, lat], ...]],
  "bounds": {"minLon": 78.03, "maxLon": 78.06, "minLat": 30.31, "maxLat": 30.34}
}
```

### POST `/api/find-path`
Calculates path between two points using selected algorithm
```json
{
  "start": [longitude, latitude],
  "end": [longitude, latitude],
  "algorithm": "astar|dijkstra|gbfs"
}
```

### POST `/api/nearest-node`
Finds nearest graph node to given coordinates
```json
{
  "point": [longitude, latitude]
}
```

## 📈 Performance Metrics

- **Graph Size**: 1,000+ nodes from real road intersections
- **Data Processing**: 654,381 lines of OSM data
- **Algorithm Speed**: Sub-second pathfinding on typical routes
- **Memory Usage**: Optimized graph representation for large datasets

## 🧪 Testing

The application includes comprehensive validation:

- ✅ OSM data parsing and integrity checks
- ✅ Algorithm correctness verification
- ✅ Cross-browser compatibility testing
- ✅ API endpoint functionality testing

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- Additional pathfinding algorithms (D*, JPS, etc.)
- Support for other cities/regions
- Performance optimizations
- Mobile app development
- Machine learning integration

## 🎓 Educational Value

This project demonstrates:
- **Graph Theory**: Practical application of theoretical concepts
- **Algorithm Analysis**: Comparative study of pathfinding approaches
- **Web Development**: Full-stack application architecture
- **Geographic Information Systems**: Real-world data processing
- **Software Engineering**: Professional development practices

## 🔮 Future Enhancements

- [ ] Step-by-step algorithm visualization
- [ ] Performance analytics dashboard
- [ ] Multiple city support
- [ ] Traffic pattern integration
- [ ] Mobile application version
- [ ] Machine learning heuristics

## 👥 Team

**Greedy by Nature**

- **Naivaidhya Garg** (Team Lead) - [@Naiv-g](https://github.com/Naiv-g)
- **Aditya** - [@aditya](https://github.com/aditya)
- **Pratyush Bisht** - [@pratyush-bisht](https://github.com/pratyush-bisht)
- **Shashwat Singh Kushwah** - [@shashwat20068](https://github.com/shashwat20068)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap**: For providing authentic geographic data
- **Leaflet.js**: For excellent mapping capabilities
- **Flask Community**: For the robust web framework
- **Bootstrap Team**: For responsive design components

## 📞 Contact

For questions, suggestions, or collaborations:

- **Email**: naivaidhyag@gmail.com
- **GitHub**: [GeoPath-Pathfinder](https://github.com/Naiv-g/GeoPath-Pathfinder)

---

⭐ **Star this repository if you found it helpful!** ⭐

