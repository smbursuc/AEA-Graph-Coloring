import read_graph_instance

def calculate_conflicts(graph):
    conflicts = 0
    for node in graph.values():
        for neighbor in node.neighbors:
            if neighbor.color == node.color:
                conflicts += 1
    return conflicts // 2  # Divide by 2 because each conflict is counted twice

def find_max_degree_vertex(graph):
    max_degree_vertex = max(graph, key=lambda node: len(node.neighbors))
    return max_degree_vertex


def find_maximal_independent_set(graph):
    independent_set = set()
    remaining_nodes = set(graph.values())

    while remaining_nodes:
        max_degree_vertex = find_max_degree_vertex(remaining_nodes)
        independent_set.add(max_degree_vertex)
        remaining_nodes.remove(max_degree_vertex)

        for neighbor in max_degree_vertex.neighbors:
            remaining_nodes -= {neighbor}

    return independent_set


def recursive_largest_first(graph):
    color_number = 0

    while graph:
        independent_set = find_maximal_independent_set(graph)
        #print(f"Independent set: {[node.id for node in independent_set]}")
        color_number += 1

        for node in independent_set:
            node.color = color_number
            del graph[node.id]  # Remove node from the graph

    return color_number

def main():
    filename = 'instances/queen5_5.col'  # Change this to your .col file name
    #filename = 'instances/test_instance.col'  # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    if not graph:
        print("Error reading graph.")
        return

    color_number = recursive_largest_first(graph)

    print(f"Number of colors used: {color_number}")

    read_graph_instance.visualize_graph_with_colors(graph)

    for node in graph.values():
        print(f"Node {node.id} has color {node.color}")

if __name__ == "__main__":
    main()