import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id):
        self.id = id
        self.color = 'unset'
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)


def read_col_graph(filename):
    nodes = {}
    edges = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('p'):
                _, _, num_nodes, _ = line.split()
                num_nodes = int(num_nodes)
                for i in range(1, num_nodes + 1):
                    nodes[i] = Node(i)
            elif line.startswith('e'):
                _, src, dest = line.split()
                src = int(src)
                dest = int(dest)
                edges.append((src, dest))

    for src, dest in edges:
        nodes[src].add_neighbor(nodes[dest])
        nodes[dest].add_neighbor(nodes[src])

    return nodes

def visualize_graph(graph):
    G = nx.Graph()
    node_colors = []

    for node_id, node in graph.items():
        for neighbor in node.neighbors:
            G.add_edge(node_id, neighbor.id)
        # Assign node color based on the 'color' attribute
        if node.color == 'unset':
            node_colors.append('gray')  # Default color for unset nodes
        else:
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink']
            node_colors.append(colors[node.color])

    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()

def visualize_graph_with_colors(graph):
    G = nx.Graph()

    # Add nodes to the graph in the desired order
    node_ids = sorted(graph.keys())
    for node_id in node_ids:
        G.add_node(node_id)

    for node_id, node in graph.items():
        for neighbor in node.neighbors:
            G.add_edge(node_id, neighbor.id)

    # Get node colors in the correct order
    node_colors = [graph[node_id].color for node_id in node_ids]

    nx.draw(G, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)
    plt.show()



def main():
    filename = 'instances/test_instance.col'  # Change this to your .col file name
    graph = read_col_graph(filename)

    if not graph:
        print("Error reading graph.")
        return

    visualize_graph(graph)
    
    # Example usage:
    for node_id, node in graph.items():
        print(f"Node {node_id} has neighbors: {[neighbor.id for neighbor in node.neighbors]}")


if __name__ == "__main__":
    main()
    
