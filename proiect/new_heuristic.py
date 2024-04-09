import random
import read_graph_instance
import copy
import numpy as np

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

# def update_pheromone(pheromone_matrix, solutions, evaporation_rate):
#     for solution in solutions:
#         conflicts = calculate_conflicts(solution)
#         # Update pheromone based on conflicts (lower conflicts => stronger pheromone)
#         for node_id, node in solution.items():
#             for neighbor in node.neighbors:
#                 # Update pheromone based on conflicts (lower conflicts => stronger pheromone)
#                 pheromone_matrix[node_id - 1][neighbor.id - 1] += 1 / (conflicts + 1)
#                 pheromone_matrix[neighbor.id - 1][node_id - 1] += 1 / (conflicts + 1)
#     # Evaporation
#     pheromone_matrix *= (1 - evaporation_rate)

def update_pheromone(pheromone_matrix, solutions, evaporation_rate):
    for solution in solutions:
        conflicts = calculate_conflicts(solution)
        penalty_factor = 1 + conflicts  # Higher conflicts, higher penalty

        # Update pheromone based on conflicts (lower conflicts => stronger pheromone)
        for node_id, node in solution.items():
            for neighbor in node.neighbors:
                # Update pheromone with penalty for conflicts
                delta_pheromone = 1 / (penalty_factor * ((conflicts + 1)*3))
                pheromone_matrix[node_id - 1][neighbor.id - 1] += delta_pheromone
                pheromone_matrix[neighbor.id - 1][node_id - 1] += delta_pheromone
    # Evaporation
    pheromone_matrix *= (1 - evaporation_rate)

# def construct_ant_solution(graph, pheromone_matrix, k):
#     solution = {node_id: node for node_id, node in graph.items()}
#     for node_id, node in solution.items():
#         # Adjust node_id to zero-based indexing
#         node_id -= 1
#         # Calculate probabilities for choosing colors based on pheromone levels and heuristics
#         color_probabilities = []
#         for color in range(k):
#             pheromone_sum = sum(pheromone_matrix[node_id])
#             pheromone_probability = pheromone_matrix[node_id][color] / pheromone_sum
#             # Add heuristic information (e.g., number of conflicts)
#             # You can implement additional heuristic information here
#             color_probabilities.append((color, pheromone_probability))
#         # Choose color based on probabilities
#         chosen_color = random.choices(*zip(*color_probabilities))[0]
#         node.color = chosen_color
#     return solution

def construct_ant_solution(graph, pheromone_matrix, k):
    solution = {node_id: node for node_id, node in graph.items()}
    for node_id, node in solution.items():
        # Adjust node_id to zero-based indexing
        node_id -= 1
        color_probabilities = []
        for color in range(k):
            pheromone_sum = sum(pheromone_matrix[node_id])
            pheromone_probability = pheromone_matrix[node_id][color] / pheromone_sum

            # Heuristic based on node degree (higher degree, more options)
            node_degree_weight = 1 / (node.degree() + 1)  # Normalize weight

            # Heuristic based on available colors for neighbors (fewer options, prefer this color)
            available_neighbor_colors = set(neighbor.color for neighbor in node.neighbors if neighbor.color is not None)
            neighbor_color_weight = len(available_neighbor_colors)   

            # Combine pheromone with heuristics (adjust weights as needed)
            
            conflict_count = 0
            for neighbor in node.neighbors:
                if neighbor.color == color:
                    conflict_count += 1
            combined_probability = pheromone_probability * node_degree_weight * neighbor_color_weight * (1 / ((conflict_count + 1)*3))
            color_probabilities.append((color, combined_probability)) 

        chosen_color = random.choices(*zip(*color_probabilities))[0]
        node.color = chosen_color
    return solution

def ant_col(graph, k, num_ants, evaporation_rate, iterations):
    pheromone_matrix = initialize_pheromone_matrix(graph)
    best_solution = None
    best_conflicts = float('inf')
    ok=0
    while(ok == 0):
        ant_solutions = []
        for _ in range(num_ants):
            ant_solution = construct_ant_solution(graph, pheromone_matrix, k)
            ant_solutions.append(ant_solution)
            conflicts = calculate_conflicts(ant_solution)
            if conflicts < best_conflicts:
                best_conflicts = conflicts
                best_solution = copy.deepcopy(ant_solution)
                print(best_conflicts)
                if best_conflicts == 0:
                    ok=1
        update_pheromone(pheromone_matrix, ant_solutions, evaporation_rate)
    return best_solution


def main():
    filename = 'instances/le450_15c.col' # Change this to your .col file name
    graph = read_graph_instance.read_col_graph(filename)

    k = 5  # Number of colors
    num_ants = 10  # Number of ants
    evaporation_rate = 0.25 # Evaporation rate
    iterations = 100  # Number of iterations

    solution = ant_col(graph, k, num_ants, evaporation_rate, iterations)

    if solution:
        # Assign colors to graph nodes
        for node_id, node in solution.items():
            graph[node_id].color = node.color

        # Visualization of colored graph
        read_graph_instance.visualize_graph_with_colors(graph)
    else:
        print("No coloring found.")

if __name__ == "__main__":
    main()

    