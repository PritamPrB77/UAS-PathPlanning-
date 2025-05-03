
#  with out using DI Graph

import math

import pandas as pd
import folium
import networkx as nx
from itertools import permutations

# Load the CSV file (only Latitude and Longitude columns required)
df = pd.read_csv("D:\\NetworkX\\tsp_locations_abs_cost.csv")  # No cost column
print(df)
# Clean data
df.drop_duplicates(inplace=True)
df.ffill(inplace=True)
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# Create graph
G = nx.complete_graph(len(df), create_using=nx.Graph())



# Step 4: Assign Euclidean distance as edge weight
positions = {}  # to store node positions for plotting and folium

for i in G.nodes:
    lat1 = df.iloc[i]['Latitude']

    lon1 = df.iloc[i]['Longitude']
    positions[i] = (lat1, lon1)
    for j in G.nodes:
        if i != j:
            lat2 = df.iloc[j]['Latitude']
            lon2 = df.iloc[j]['Longitude']
            distance = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
            G.add_edge(i, j, weight=distance)


# Step 5: Solve TSP using brute-force
nodes = list(G.nodes)
min_path = None
min_cost = float('inf')

for perm in permutations(nodes):

    cost = 0
    for i in range(len(perm) - 1):

        cost += G[perm[i]][perm[i + 1]]['weight']
    cost += G[perm[-1]][perm[0]]['weight']  # return to start
    if cost < min_cost:
        min_cost = cost
        min_path = perm

print("Optimal TSP Path:", min_path)
print("Minimum Cost:", min_cost)

# Step 6: Visualize on Folium map
start_lat, start_lon = positions[min_path[0]]
m = folium.Map(location=[start_lat, start_lon], zoom_start=2)

# Add markers and path
path_coords = []
for node in min_path:
    lat, lon = positions[node]
    path_coords.append((lat, lon))
    folium.Marker(location=(lat, lon), popup=f"Node {node}").add_to(m)

# Complete the cycle by adding the first point again
path_coords.append(path_coords[0])
folium.PolyLine(path_coords, color="blue", weight=2.5).add_to(m)


# Save map
map_path = "D:/NetworkX/tsp2_map_no_cost.html"
m.save(map_path)

# Print result
print(f"Optimal Path: {min_path}")
print(f"Total Cost (abs(lon - lat)): {min_cost}")
