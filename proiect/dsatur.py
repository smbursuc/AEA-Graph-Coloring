import read_graph_instance

def find_max_degree_vertex(graph):
    max_degree_vertex = max(graph, key=lambda node: len(node.neighbors))
    return max_degree_vertex


def find_max_adjacent_colors(vertex, color_set):
    adjacent_colors = set()
    for neighbor in vertex.neighbors:
        if neighbor.color in color_set:
            adjacent_colors.add(neighbor.color)
    return len(adjacent_colors)


def dsatur(graph):
    color_number = 0
    color_set = set()
    uncolored_nodes = set(graph.values())

    while uncolored_nodes:
        # Step 2: Select uncolored vertex with maximum degree
        max_degree_vertex = find_max_degree_vertex(uncolored_nodes)
        max_adjacent_colors = find_max_adjacent_colors(max_degree_vertex, color_set)

        # Step 3: Select vertex with maximum number of adjacent colors
        for node in uncolored_nodes:
            adjacent_colors = find_max_adjacent_colors(node, color_set)
            if adjacent_colors > max_adjacent_colors or \
                    (adjacent_colors == max_adjacent_colors and len(node.neighbors) > len(max_degree_vertex.neighbors)):
                max_degree_vertex = node
                max_adjacent_colors = adjacent_colors

        # Step 4: Assign color to the selected vertex
        available_colors = set(range(1, color_number + 1)) - {neighbor.color for neighbor in max_degree_vertex.neighbors}
        if available_colors:
            max_degree_vertex.color = min(available_colors)
        else:
            color_number += 1
            max_degree_vertex.color = color_number
            color_set.add(color_number)

        # Remove colored vertex from uncolored nodes
        uncolored_nodes.remove(max_degree_vertex)

    return color_number


def main():
    filename = 'instances/le450_15c.col'  # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    if not graph:
        print("Error reading graph.")
        return

    color_number = dsatur(graph)

    print(f"Number of colors used: {color_number}")

    read_graph_instance.visualize_graph_with_colors(graph)

    # Example usage:
    for node in graph.values():
        print(f"Node {node.id} has color {node.color}")

if __name__ == "__main__":
    main()
