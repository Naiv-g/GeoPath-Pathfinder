import xml.etree.ElementTree as ET

def parse_osm(osm_file):
    tree = ET.parse(osm_file)
    root = tree.getroot()

    nodes = {}
    ways = []

    # Extract nodes (coordinates)
    for node in root.findall('node'):
        nodes[node.get('id')] = (float(node.get('lon')), float(node.get('lat')))

    # Extract ways (roads)
    for way in root.findall('way'):
        road = []
        for nd in way.findall('nd'):
            ref = nd.get('ref')
            if ref in nodes:
                road.append(nodes[ref])
        if len(road) > 1 and 'highway' in [tag.get('k') for tag in way.findall('tag')]:
            ways.append(road)

    return nodes, ways
