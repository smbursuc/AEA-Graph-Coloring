import graph_helper
import copy

def calculate_conflicts(adjacency_matrix, color_matrix):
    conflicts = 0
    num_nodes = len(adjacency_matrix)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency_matrix[i][j] and color_matrix[i] == color_matrix[j]:
                conflicts += 1
    return conflicts

def find_max_degree_vertex(adjacency_matrix, color_matrix, remaining_nodes):
    max_degree_vertex = -1
    max_degree = -1
    for node in remaining_nodes:
        degree = sum(adjacency_matrix[node])
        if degree > max_degree:
            max_degree = degree
            max_degree_vertex = node
    return max_degree_vertex

def find_maximal_independent_set(adjacency_matrix, color_matrix, remaining_nodes):
    independent_set = set()
    while remaining_nodes:
        max_degree_vertex = find_max_degree_vertex(adjacency_matrix, color_matrix, remaining_nodes)
        independent_set.add(max_degree_vertex)
        remaining_nodes.remove(max_degree_vertex)

        for neighbor in remaining_nodes.copy():
            if adjacency_matrix[max_degree_vertex][neighbor]:
                remaining_nodes.remove(neighbor)

    return independent_set

def recursive_largest_first(adjacency_matrix, color_matrix):
    color_number = 0
    remaining_nodes = set(range(len(adjacency_matrix)))

    while remaining_nodes:
        independent_set = find_maximal_independent_set(adjacency_matrix, color_matrix, copy.deepcopy(remaining_nodes))
        color_number += 1

        for node in independent_set:
            color_matrix[node] = color_number
            remaining_nodes.remove(node)

    return color_number

def main():
    filename = 'improvements/inputs/inithx.i.2.col'  # Change this to your .col file name
    nodes, edges, colors, adjacency_matrix, color_matrix = graph_helper.read_graph(filename)

    if not adjacency_matrix:
        print("Error reading graph.")
        return

    color_number = recursive_largest_first(adjacency_matrix, color_matrix)

    print(f"Number of colors used: {color_number}")

    # for node, color in enumerate(color_matrix):
    #     print(f"Node {node + 1} has color {color}")

if __name__ == "__main__":
    main()
