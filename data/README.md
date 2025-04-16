# Map Data
- `india.osm.pbf`: Full India map (1.4GB) from [Geofabrik](https://download.geofabrik.de/asia/india.html)
- `dehradun-complete.osm`: Extracted region (77.95°E-78.15°E, 30.25°N-30.45°N)

## Usage
```python
from map_loader import parse_osm
nodes, ways = parse_osm("data/india/dehradun-complete.osm")  # For development
# or
parse_osm("data/india/india.osm.pbf")  # For full dataset