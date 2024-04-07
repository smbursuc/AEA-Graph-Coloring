import random
import read_graph_instance
import copy

def calculate_conflicts(graph):
    conflicts = 0
    for node in graph.values():
        for neighbor in node.neighbors:
            if neighbor.color == node.color:
                conflicts += 1
    return conflicts // 2  # Divide by 2 because each conflict is counted twice


def f(solution):
    conflicts = 0
    for node in solution.values():
        for neighbor in node.neighbors:
            if neighbor.color == node.color or node.color == 'unset':
                conflicts += 1
    return conflicts // 2  # Divide by 2 because each conflict is counted twice


def generate_neighbors(solution, tabu_list, rep, k):
    neighbors = []
    aspiration = None
    threshold = 1
    
    for _ in range(rep):  # Number of neighbors to generate
        neighbor = copy.deepcopy(solution)
        node_to_move = random.choice(list(solution.values()))
        new_color = random.choice([color for color in range(k) if node_to_move.color != color or node_to_move.color == 'unset'])
        neighbor[node_to_move.id].color = new_color

        if aspiration is None:
            aspiration = f(neighbor) - threshold

        if neighbor not in tabu_list or f(neighbor) < aspiration:
            aspiration = f(neighbor) - threshold
            neighbors.append(neighbor)
            if f(neighbor) <= f(solution):
                return neighbors

    return neighbors


def tabucol(graph, k, tabu_size, rep, nbmax):
    current_solution = {node_id: node for node_id, node in graph.items()}
    nbiter = 0
    tabu_list = []
    min_asp = None

    while f(current_solution) > 0 and nbiter < nbmax:
        neighbors = generate_neighbors(current_solution, tabu_list, rep, k)

        if neighbors:
            best_neighbor = min(neighbors, key=lambda x: f(x))
            if f(best_neighbor) <= f(current_solution):
                if min_asp is None:
                    min_asp = f(best_neighbor)
                else:
                    min_asp = min(min_asp, f(best_neighbor))
                current_solution = copy.deepcopy(best_neighbor)
            else:
                tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

        nbiter += 1

    print(f"Minimum conflicts found: {min_asp}")
    return current_solution if f(current_solution) == 0 else None
    # return current_solution

def main():
    filename = 'instances/test_instance.col' # Change this to your .col file name
    filename = 'instances/queen5_5.col' # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    k = 5  # Number of colors
    tabu_size = 100 # Size of tabu list
    rep = 5  # Number of neighbors in sample
    nbmax = 100000  # Maximum number of iterations


    solution = tabucol(graph, k, tabu_size, rep, nbmax)

    if solution:
        # Assign colors to graph nodes
        for node_id, node in solution.items():
            graph[node_id].color = node.color

        # Visualization of colored graph
        read_graph_instance.visualize_graph_with_colors(solution)
    else:
        print("No coloring found within the maximum number of iterations.")

if __name__ == "__main__":
    main()