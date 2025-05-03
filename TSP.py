import networkx as nx
import itertools
import matplotlib.pyplot as plt

# Step 1: Create a graph
G = nx.Graph()

# Step 2: Add nodes (cities)
G.add_nodes_from([0, 1, 2, 3])

# Step 3: Add weighted edges (distances between cities)
G.add_weighted_edges_from([
    (0, 1, 10),
    (0, 2, 15),
    (0, 3, 20),
    (1, 2, 35),
    (1, 3, 25),
    (2, 3, 30)
])


# Step 4: Function to calculate total path cost
def calculate_path_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]['weight']
    cost += graph[path[-1]][path[0]]['weight']  # Return to start
    return cost


# Step 5: Find all possible permutations of nodes (excluding start node)
nodes = list(G.nodes)
start_node = nodes[0]
other_nodes = nodes[1:]

min_cost = float('inf')
best_path = []

# Find best path using permutations
for perm in itertools.permutations(other_nodes):
    current_path = [start_node] + list(perm)
    current_cost = calculate_path_cost(G, current_path)

    if current_cost < min_cost:
        min_cost = current_cost
        best_path = current_path

# Step 6: Print the best path and its cost
print("Best Path:", best_path + [start_node])  # adding start at end to complete the loop
print("Minimum Cost:", min_cost)

# Step 7: Visualization of the graph using Matplotlib

# 7.1: Plot the graph without highlighting the path
pos = nx.spring_layout(G)  # Positions for nodes
plt.figure(figsize=(8, 6))

# Draw the nodes and edges
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=12, font_weight="bold",
        edge_color="gray")

# Step 8: Highlight the best TSP path
# Draw the edges for the best path in a different color (highlight)
path_edges = [(best_path[i], best_path[i + 1]) for i in range(len(best_path) - 1)] + [(best_path[-1], best_path[0])]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
# Show weights on edges
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


# Step 9: Display the final plot
plt.title("TSP Path with Minimum Cost", fontsize=15)
plt.show()
