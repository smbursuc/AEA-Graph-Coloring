def read_graph(filename):
    nodes = set()
    edges = []
    colors = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'p':
                num_nodes = int(parts[2])
                num_edges = int(parts[3])
                adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]
                color_matrix = [0] * num_nodes
            elif parts[0] == 'e':
                node1 = int(parts[1]) - 1  # Node indexing starts from 1
                node2 = int(parts[2]) - 1
                edges.append((node1, node2))
                adjacency_matrix[node1][node2] = 1
                adjacency_matrix[node2][node1] = 1

    return nodes, edges, colors, adjacency_matrix, color_matrix

if __name__ == "__main__":
    # Example usage
    nodes, edges, colors, adjacency_matrix, color_matrix = read_graph("improvements/inputs/test_instance.col")
    print("Nodes:", nodes)
    print("Edges:", edges)
    print("Colors:", colors)
    print("Adjacency Matrix:", adjacency_matrix)
    print("Color Matrix:", color_matrix)
