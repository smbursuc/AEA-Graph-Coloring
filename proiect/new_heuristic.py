import random
import read_graph_instance
import copy
import numpy as np
import time

def calculate_conflicts(graph):
    conflicts = 0
    for node in graph.values():
        for neighbor in node.neighbors:
            if neighbor.color == node.color:
                conflicts += 1
    return conflicts // 2  # Divide by 2 because each conflict is counted twice


def initialize_pheromone_matrix(graph):
    num_nodes = len(graph)
    pheromone_matrix = np.ones((num_nodes, num_nodes))
    np.fill_diagonal(pheromone_matrix, 0)  # No pheromone on self-loops
    return pheromone_matrix

def update_pheromone(pheromone_matrix, solutions, evaporation_rate):
    for solution in solutions:
        conflicts = calculate_conflicts(solution)
        # Update pheromone based on conflicts (lower conflicts => stronger pheromone)
        for node_id, node in solution.items():
            for neighbor in node.neighbors:
                # Update pheromone based on conflicts (lower conflicts => stronger pheromone)
                pheromone_matrix[node_id - 1][neighbor.id - 1] += 1 / (conflicts + 1)
                pheromone_matrix[neighbor.id - 1][node_id - 1] += 1 / (conflicts + 1)
    # Evaporation
    pheromone_matrix *= (1 - evaporation_rate)



def construct_ant_solution(graph, pheromone_matrix, k):
    solution = {node_id: node for node_id, node in graph.items()}
    for node_id, node in solution.items():
        # Adjust node_id to zero-based indexing
        node_id -= 1
        
        # Calculate probabilities for choosing colors based on pheromone levels, node degree, and conflicts
        color_probabilities = []
        for color in range(k):
            pheromone_sum = sum(pheromone_matrix[node_id])
            pheromone_probability = pheromone_matrix[node_id][color] / pheromone_sum
            # Calculate the number of conflicts with this color
            conflicts_with_color = sum(1 for neighbor in node.neighbors if neighbor.color == color)
            # Heuristic: Choose the color that minimizes conflicts with neighbors and considers node degree
            degree = node.degree()  # Assuming degree is a method and needs to be called
            degree_factor = 1 / (degree + 1)  # Adding 1 to avoid division by zero
            color_probabilities.append((color, pheromone_probability * degree_factor / (conflicts_with_color + 1)))  # Adding 1 to avoid division by zero
        
        # Choose color based on probabilities
        chosen_color = random.choices(*zip(*color_probabilities))[0]
        node.color = chosen_color
        
    return solution


def local_search(graph, solution,k):
    improved = True
    max_iterations = 5

    start_time = time.time()
    timeout_duration = 500
    is_timeout = False 

    while improved and max_iterations > 0:
        improved = False
        conflicts = calculate_conflicts(solution)
        for node_id, node in solution.items():
            current_color = node.color
            for color in range(k):
                if color != current_color:
                    original_color = node.color
                    node.color = color
                    new_conflicts = calculate_conflicts(solution)
                    if new_conflicts < conflicts:
                        improved = True
                        conflicts = new_conflicts
                    else:
                        node.color = original_color
        # if improved:
        #     print("Local search: Conflicts reduced to", conflicts)
        max_iterations -= 1

        if time.time() - start_time > timeout_duration:
            is_timeout = True
            break

    if is_timeout:
        return "timeout"
    return solution

def ant_col_with_local_search(graph, k, num_ants, evaporation_rate, iterations):
    pheromone_matrix = initialize_pheromone_matrix(graph)
    best_solution = None
    best_conflicts = float('inf')
    ok=0
    i=0
    while(ok == 0 and i<iterations):
        ant_solutions = []
        for _ in range(num_ants):
            ant_solution = construct_ant_solution(graph, pheromone_matrix, k)
            ant_solution = local_search(graph, ant_solution,k)  # Apply local search
            ant_solutions.append(ant_solution)
            conflicts = calculate_conflicts(ant_solution)
            if conflicts < best_conflicts:
                best_conflicts = conflicts
                best_solution = copy.deepcopy(ant_solution)
                update_pheromone(pheromone_matrix, ant_solutions, evaporation_rate)
                # print(best_conflicts)
                if best_conflicts == 0:
                    ok=1
        i=i+1
        
    return best_solution


def main():
    filename = 'instances/queen5_5.col' # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    k = 5  # Number of colors
    num_ants = 10  # Number of ants
    evaporation_rate = 0.1 # Evaporation rate
    iterations = 100  # Number of iterations

    solution = ant_col_with_local_search(graph, k, num_ants, evaporation_rate, iterations)

    if solution:
        brrr = calculate_conflicts(solution)

        print("CONFLCITS : ", brrr)
        # Assign colors to graph nodes
        for node_id, node in solution.items():
            graph[node_id].color = node.color

        # Visualization of colored graph
        read_graph_instance.visualize_graph_with_colors(graph)
    else:
        print("No coloring found.")

if __name__ == "__main__":
    main()

    