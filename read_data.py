from math import sqrt

def distance(point1, point2):
    return round(sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))

def to_distance_matrix(coordinates):
    n = len(coordinates)
    return [[distance(coordinates[i], coordinates[j]) for j in range(n)] for i in range(n)]

def read_data(filepath: str):
    with open(filepath) as file:
        node_coordinates = []
        in_node_coord_section = False
        for line in file:
            if line == 'NODE_COORD_SECTION\n':
                in_node_coord_section = True
            elif line == 'EOF\n':
                in_node_coord_section = False
            elif in_node_coord_section:
                index, x, y = line.split()
                node_coordinates.append((int(x), int(y)))
    return to_distance_matrix(node_coordinates)
