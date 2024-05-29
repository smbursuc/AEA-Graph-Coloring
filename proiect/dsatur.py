import graph_helper
import copy

def find_max_degree_vertex(adjacency_matrix, color_matrix, remaining_nodes):
    max_degree_vertex = -1
    max_degree = -1
    for node in remaining_nodes:
        degree = sum(adjacency_matrix[node])
        if degree > max_degree:
            max_degree = degree
            max_degree_vertex = node
    return max_degree_vertex

def find_max_adjacent_colors(vertex, color_matrix, color_set):
    adjacent_colors = set()
    for neighbor, is_adjacent in enumerate(vertex):
        if is_adjacent and color_matrix[neighbor] in color_set:
            adjacent_colors.add(color_matrix[neighbor])
    return len(adjacent_colors)

def dsatur(adjacency_matrix, color_matrix):
    color_number = 0
    color_set = set()
    num_nodes = len(adjacency_matrix)
    remaining_nodes = set(range(num_nodes))

    while remaining_nodes:
        # Step 2: Select uncolored vertex with maximum degree
        max_degree_vertex = find_max_degree_vertex(adjacency_matrix, color_matrix, remaining_nodes)
        max_adjacent_colors = find_max_adjacent_colors(adjacency_matrix[max_degree_vertex], color_matrix, color_set)

        # Step 3: Select vertex with maximum number of adjacent colors
        for node in remaining_nodes:
            adjacent_colors = find_max_adjacent_colors(adjacency_matrix[node], color_matrix, color_set)
            if (adjacent_colors > max_adjacent_colors) or \
                    ((adjacent_colors == max_adjacent_colors) and (sum(adjacency_matrix[node]) > sum(adjacency_matrix[max_degree_vertex]))):
                max_degree_vertex = node
                max_adjacent_colors = adjacent_colors

        # Step 4: Assign color to the selected vertex
        available_colors = set(range(1, color_number + 1)) - {color_matrix[neighbor] for neighbor, is_adjacent in enumerate(adjacency_matrix[max_degree_vertex]) if is_adjacent}
        if available_colors:
            color_matrix[max_degree_vertex] = min(available_colors)
        else:
            color_number += 1
            color_matrix[max_degree_vertex] = color_number
            color_set.add(color_number)

        # Remove colored vertex from uncolored nodes
        remaining_nodes.remove(max_degree_vertex)

    return color_number

def main():
    filename = 'improvements/inputs/inithx.i.2.col'  # Change this to your .col file name
    nodes, edges, colors, adjacency_matrix, color_matrix = graph_helper.read_graph(filename)

    if not adjacency_matrix:
        print("Error reading graph.")
        return

    color_number = dsatur(adjacency_matrix, color_matrix)

    print(f"Number of colors used: {color_number}")

    # for node, color in enumerate(color_matrix):
    #     print(f"Node {node + 1} has color {color}")

if __name__ == "__main__":
    main()
