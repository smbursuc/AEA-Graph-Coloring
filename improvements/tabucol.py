import random
import graph_helper
import copy
import sys

def f(adjacency_matrix, color_matrix):
    conflicts = 0
    num_nodes = len(adjacency_matrix)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency_matrix[i][j] and color_matrix[i] == color_matrix[j]:
                conflicts += 1
    return conflicts // 2  # Divide by 2 because each conflict is counted twice


def is_in_tabu_list(color_matrix, tabu_list):
    for tabu_color_matrix in tabu_list:
        if all(color_matrix[i] == tabu_color_matrix[i] for i in range(len(color_matrix))):
            return True
    return False


def generate_neighbors(adjacency_matrix, color_matrix, tabu_list, rep, k):
    neighbors = []
    aspiration = None
    threshold = 1

    for _ in range(rep):  # Number of neighbors to generate
        # the candidate nodes will be nodes which are adjcent and have the same color
        candidate_nodes = set()  # use a set to avoid duplicates

        for i in range(len(adjacency_matrix)):
            for j in range(i+1, len(adjacency_matrix)):  # assume undirected graph, ignoring self-loops
                if adjacency_matrix[i][j] > 0: # adjacent
                    if color_matrix[i] == color_matrix[j]:  # same color
                        candidate_nodes.add(i)
                        candidate_nodes.add(j)

        candidate_nodes = list(candidate_nodes)  # convert to list for array indexing

        if not candidate_nodes:
            continue  # Skip if no node is adjacent to an edge
        node_to_move = random.choice(candidate_nodes)

        # Choose a random color j for the new subset
        current_color = color_matrix[node_to_move]
        new_color = random.choice([color for color in range(k) if color != current_color])

        # Generate the new neighbor by moving the node to the new subset
        neighbor_color_matrix = color_matrix[:]
        neighbor_color_matrix[node_to_move] = new_color

        neighbor_conflicts = f(adjacency_matrix, neighbor_color_matrix)

        # Check if the move is tabu
        is_tabu = any([tabu_move for tabu_move in tabu_list if tabu_move[0] == node_to_move and tabu_move[1] == new_color])

        if aspiration is None:
            aspiration = neighbor_conflicts - threshold

        if not is_tabu or neighbor_conflicts < aspiration:
            aspiration = neighbor_conflicts - threshold
            neighbors.append(neighbor_color_matrix)
            if neighbor_conflicts <= f(adjacency_matrix, color_matrix):
                return neighbors

    return neighbors



def tabucol(adjacency_matrix, color_matrix, k, tabu_size, rep, nbmax, debug=False):
    current_color_matrix = copy.deepcopy(color_matrix)
    nbiter = 0
    tabu_list = []
    tabu_index = 0  # To keep track of the position in the circular buffer

    while f(adjacency_matrix, current_color_matrix) > 0 and nbiter < nbmax:
        neighbors = generate_neighbors(copy.deepcopy(adjacency_matrix), copy.deepcopy(current_color_matrix), copy.deepcopy(tabu_list), rep, k)

        if neighbors:
            best_neighbor = copy.deepcopy(min(neighbors, key=lambda x: f(adjacency_matrix, x)))
            # if f(adjacency_matrix, best_neighbor) <= f(adjacency_matrix, current_color_matrix):
            #     current_color_matrix = copy.deepcopy(best_neighbor)
            # else:
            
            # Add the move to the tabu list
            
            
            if f(adjacency_matrix, best_neighbor) <= f(adjacency_matrix, current_color_matrix):
                current_color_matrix = copy.deepcopy(best_neighbor)

            for i in range(len(current_color_matrix)):
                if current_color_matrix[i] != best_neighbor[i]:
                    if len(tabu_list) < tabu_size:
                        tabu_list.append((i, current_color_matrix[i], nbmax // 10))
                    else:
                        tabu_list[tabu_index] = (i, current_color_matrix[i], nbmax // 10)
                        tabu_index = (tabu_index + 1) % tabu_size

            # if len(tabu_list) > tabu_size:
            #     tabu_list.pop(0)  # Remove oldest move from tabu list

            if debug:
                print(f"Minimum conflicts found: {f(adjacency_matrix, current_color_matrix)}")

            # print(tabu_list)
            # print("\n")

            # Update tabu list iteration count
            for i in range(len(tabu_list)):
                tabu_list[i] = (i, tabu_list[i][1], tabu_list[i][2] - 1)
                if tabu_list[i][2] <= 0:
                    #print(f"Unblocking move {tabu_list[i]}")
                    tabu_list.pop(i)
                    break

        nbiter += 1

    if debug:
        print(f"Minimum conflicts found: {f(adjacency_matrix, current_color_matrix)}")
        print(f"Number of iterations: {nbiter}")

    return current_color_matrix if f(adjacency_matrix, current_color_matrix) == 0 else None

def main():
    filename = 'improvements/inputs/zeroin.i.1.col'  # Change this to your .col file name
    nodes, edges, colors, adjacency_matrix, color_matrix = graph_helper.read_graph(filename)

    if not adjacency_matrix:
        print("Error reading graph.")
        return

    k = 49  # Number of colors
    tabu_size = 7 # Size of tabu list
    rep = 150  # Number of neighbors in sample
    nbmax = 100000  # Maximum number of iterations

    solution = tabucol(adjacency_matrix, color_matrix, k, tabu_size, rep, nbmax, True)

    if solution:
        print("Coloring found:")
        # for node_id, color in enumerate(solution):
        #     print(f"Node {node_id + 1} has color {color}")
    else:
        print("No coloring found within the maximum number of iterations.")

if __name__ == "__main__":
    main()
