import random
import read_graph_instance
import copy
import sys
import time
import matplotlib.pyplot as plt
sys.setrecursionlimit(50000)  # Set the recursion limit to a higher value, e.g., 5000


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
    return conflicts  # Divide by 2 because each conflict is counted twice


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


def tabucol(graph, k, tabu_size, rep, nbmax, debug=False):
    current_solution = {node_id: node for node_id, node in graph.items()}
    nbiter = 0
    tabu_list = []
    min_asp = None
    conflict_list = {}

    start_time = time.time()
    while f(current_solution) > 0 and nbiter < nbmax:
        neighbors = generate_neighbors(current_solution, tabu_list, rep, k)

        curr_conflicts = f(current_solution)
        conflict_list[nbiter] = curr_conflicts 

        if neighbors:
            best_neighbor = min(neighbors, key=lambda x: f(x))
            if f(best_neighbor) <= curr_conflicts:
                if min_asp is None:
                    min_asp = f(best_neighbor)
                else:
                    min_asp = min(min_asp, f(best_neighbor))
                

                if debug:
                    print(f"New minimum aspiration: {min_asp}")
            else:
                tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_size:
                current_solution = copy.deepcopy(tabu_list.pop(0))
                tabu_list.clear()
        current_solution = copy.deepcopy(best_neighbor)

        nbiter += 1

        if time.time() - start_time > 300:
            is_timeout = True
            print("Timeout reached.")
            break

    if debug:
        print(f"Minimum conflicts found: {min_asp}")
        print(f"Number of iterations: {nbiter}")

        # Extract keys and values
    keys = list(conflict_list.keys())
    values = list(conflict_list.values())

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(values, keys)

    # Adding labels and title
    plt.xlabel('Iterations')
    plt.ylabel('Conflicts')
    plt.title('queen8_12.col')

    # Display the graph
    plt.show()

    return current_solution if f(current_solution) == 0 else None
    # return current_solution

def main():
    #filename = 'instances/test_instance.col' # Change this to your .col file name
    filename = 'instances/le450_15c.col' # Change this to your .col file name
    #filename = 'instances_k/myciel6.col' # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    k = 7  # Number of colors
    tabu_size = 100 # Size of tabu list
    rep = 5  # Number of neighbors in sample
    nbmax = 100000  # Maximum number of iterations


    solution = tabucol(graph, k, tabu_size, rep, nbmax, True)

    if solution:
        for node_id, node in solution.items():
            graph[node_id].color = node.color

        read_graph_instance.visualize_graph_with_colors(solution)
    else:
        print("No coloring found within the maximum number of iterations.")

if __name__ == "__main__":
    main()