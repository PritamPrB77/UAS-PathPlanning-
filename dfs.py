




import numpy as np

import pandas as pd

import networkx as nx

import  matplotlib.pyplot as plt

# Create a Graph
G = nx.Graph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'),
         ('C', 'F'), ('C', 'G'), ('E', 'H')]

G.add_edges_from(edges)
nx.draw_spring(G,with_labels=True)
plt.show()
# Get DFS Order
dfs_nodes = list(nx.dfs_preorder_nodes(G, 'A'))
print("\nDFS using NetworkX:", dfs_nodes)

# nx.draw_spring(G,with_labels=True)
# plt.show()