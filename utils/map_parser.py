import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

def parse_osm(osm_path):
    """Parse OSM XML file and extract road network"""
    try:
        logger.info(f"Parsing OSM file: {osm_path}")
        tree = ET.parse(osm_path)
        root = tree.getroot()

        nodes = {}
        ways = []

        # Extract nodes
        logger.debug("Extracting nodes")
        for node in root.findall('node'):
            nodes[node.get('id')] = (
                float(node.get('lon')),
                float(node.get('lat'))
            )

        # Extract roads
        logger.debug("Extracting roads")
        for way in root.findall('way'):
            if any(tag.get('k') == 'highway' for tag in way.findall('tag')):
                road = []
                for nd in way.findall('nd'):
                    node_id = nd.get('ref')
                    if node_id in nodes:
                        road.append(nodes[node_id])
                if len(road) > 1:
                    ways.append(road)

        logger.info(f"Parsed {len(nodes)} nodes and {len(ways)} roads")
        return nodes, ways
    except Exception as e:
        logger.error(f"Failed to parse OSM file: {str(e)}")
        raise RuntimeError(f"Failed to parse OSM file: {str(e)}")
