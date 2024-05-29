import random
from random import randrange
import graph_helper
import copy
from collections import deque
import time

def f(adjacency_matrix, color_matrix):
    conflicts = 0
    num_nodes = len(adjacency_matrix)
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency_matrix[i][j] and color_matrix[i] == color_matrix[j]:
                conflicts += 1
    return conflicts  # Divide by 2 because each conflict is counted twice


def is_in_tabu_list(color_matrix, tabu_list):
    for tabu_color_matrix in tabu_list:
        if all(color_matrix[i] == tabu_color_matrix[i] for i in range(len(color_matrix))):
            return True
    return False


def generate_neighbors(adjacency_matrix, move_candidates, colors, tabu_list, rep, k, aspiration_level, debug=False):
    neighbors = []
    threshold = 1

    for _ in range(rep):  # Number of neighbors to generate
        node_to_move = random.choice(move_candidates)

        # Choose a random color j for the new subset
        current_color = colors[node_to_move]
        new_color = random.choice(randrange(0, len(move_candidates)))

        if current_color == new_color:
            new_color = colors[-1]

        # Generate the new neighbor by moving the node to the new subset
        neighbor_colors = copy.deepcopy(colors)
        neighbor_colors[node_to_move] = new_color

        neighbors.append(neighbor_colors)

        curr_conflicts = f(adjacency_matrix, colors)
        neighbor_conflicts = f(adjacency_matrix, neighbor_colors)

        if f(adjacency_matrix, neighbor_colors) < curr_conflicts:
            if neighbor_conflicts <= aspiration_level.setdefault(curr_conflicts, curr_conflicts - threshold):
                aspiration_level[curr_conflicts] = neighbor_conflicts - 1

                if (node_to_move, new_color) in tabu_list: # permit tabu move if it is better any prior
                    tabu_list.remove((node_to_move, new_color))
                    if debug:
                        print("tabu permitted;", curr_conflicts, "->", neighbor_conflicts)
                    break
            else:
                if (node_to_move, new_color) in tabu_list:
                    # tabu move isn't good enough
                    continue
            if debug:
                print (curr_conflicts, "->", neighbor_conflicts)
            break

    return neighbors



def tabucol(adjacency_matrix, k, tabu_size, rep, nbmax, debug=False):
    colors = list(range(k))
    nbiter = 0
    tabu_list = deque()
    threshold = 1

    # Generate a random solution:
    current_color_matrix = [colors[random.randrange(0, len(colors))] for _ in range(len(adjacency_matrix))]

    aspiration_level = dict()

    start_time = time.time()
    timeout_duration = 300
    is_timeout = False 

    while nbiter < nbmax:

        move_candidates = set()  # use a set to avoid duplicates
        conflict_count = 0
        for i in range(len(adjacency_matrix)):
            for j in range(i+1, len(adjacency_matrix)):  # assume undirected graph, ignoring self-loops
                if adjacency_matrix[i][j] == 1: # adjacent
                    if current_color_matrix[i] == current_color_matrix[j]:  # same color
                        move_candidates.add(i)
                        move_candidates.add(j)
                        conflict_count += 1
        move_candidates = list(move_candidates)  # convert to list for array indexing

        if conflict_count == 0:
            # Found a valid coloring.
            break

        for _ in range(rep):  # Number of neighbors to generate
            node_to_move = move_candidates[random.randrange(0, len(move_candidates))]

            # Choose a random color j for the new subset
            current_color = current_color_matrix[node_to_move]
            new_color = colors[random.randrange(0, len(colors))]

            if current_color == new_color:
                new_color = colors[-1]

            # Generate the new neighbor by moving the node to the new subset
            neighbor_colors = copy.deepcopy(current_color_matrix)
            neighbor_colors[node_to_move] = new_color

            #curr_conflicts = f(adjacency_matrix, current_color_matrix)
            neighbor_conflicts = f(adjacency_matrix, neighbor_colors)

            if neighbor_conflicts < conflict_count:
                if neighbor_conflicts <= aspiration_level.setdefault(conflict_count, conflict_count - threshold):

                    aspiration_level[conflict_count] = neighbor_conflicts - threshold

                    if (node_to_move, new_color) in tabu_list: # permit tabu move if it is better any prior
                        tabu_list.remove((node_to_move, new_color))
                        if debug:
                            print("tabu permitted;", conflict_count, "->", neighbor_conflicts)
                        break
                    else:
                        if (node_to_move, new_color) in tabu_list:
                            # tabu move isn't good enough
                            continue
                if debug:
                    print(f"Reduced conflicts from {conflict_count} to {neighbor_conflicts}")
                break

        tabu_list.append((node_to_move, current_color_matrix[node_to_move]))
        if len(tabu_list) > tabu_size:  # queue full
            tabu_list.popleft()  # remove the oldest move

        # Move to next iteration of tabucol with new solution
        current_color_matrix = neighbor_colors

        nbiter += 1

        if debug and nbiter % 500 == 0:
            print(f"Iteration {nbiter}")

        if time.time() - start_time > timeout_duration:
            is_timeout = True
            print("Timeout reached.")
            break

        # if debug:
        #     print(f"Minimum conflicts found: {f(adjacency_matrix, current_color_matrix)}")
        #     print(f"Number of iterations: {nbiter}")

    if f(adjacency_matrix, current_color_matrix) == 0:
        return current_color_matrix
    else:
        if is_timeout:
            return "timeout"
        return None


def main():
    filename = 'improvements/inputs/zeroin.i.1.col'  # Change this to your .col file name
    nodes, edges, colors, adjacency_matrix, color_matrix = graph_helper.read_graph(filename)

    if not adjacency_matrix:
        print("Error reading graph.")
        return

    k = 49  # Number of colors
    tabu_size = 7 # Size of tabu list
    rep = 150  # Number of neighbors in sample
    nbmax = 10000  # Maximum number of iterations

    solution = tabucol(adjacency_matrix, k, tabu_size, rep, nbmax, True)

    if solution:
        print("Coloring found:")
        # for node_id, color in enumerate(solution):
        #     print(f"Node {node_id + 1} has color {color}")
    else:
        print("No coloring found within the maximum number of iterations.")

if __name__ == "__main__":
    main()
