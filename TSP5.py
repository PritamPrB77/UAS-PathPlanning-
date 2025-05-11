import math
import pandas as pd
import folium
import networkx as nx
import folium
from folium.plugins import BeautifyIcon

# Load CSV
df = pd.read_csv("D:/NetworkX/tsp_locations_abs_cost.csv")

# Clean and convert
df['Latitude'] = pd.to_numeric(df['Latitude'].astype(str).str.strip(), errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'].astype(str).str.strip(), errors='coerce')
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Use first 100 records
df = df.head(100)

# Create graph and positions
G = nx.Graph()
positions = {}

for i in range(len(df)):
    lat = df.loc[i, 'Latitude']
    lon = df.loc[i, 'Longitude']
    G.add_node(i)
    positions[i] = (lat, lon)

# Add weighted edges
for i in G.nodes:
    lat1, lon1 = positions[i]
    for j in G.nodes:
        if i != j:
            lat2, lon2 = positions[j]
            distance = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
            G.add_edge(i, j, weight=distance)

# Nearest Neighbor TSP
def nearest_neighbor(graph, start):
    visited = [start]
    current = start
    total_cost = 0
    while len(visited) < len(graph.nodes):
        neighbors = [(n, graph[current][n]['weight']) for n in graph.neighbors(current) if n not in visited]
        if not neighbors:
            break
        next_node = min(neighbors, key=lambda x: x[1])[0]
        total_cost += graph[current][next_node]['weight']
        visited.append(next_node)
        current = next_node
    total_cost += graph[current][start]['weight']
    visited.append(start)
    return visited, total_cost

# Run TSP
path, cost = nearest_neighbor(G, 0)
print("Optimal Path (Heuristic):", path)
print("Total Cost:", cost)
# Draw improved Folium map with better readability


# Create map centered at starting point
start_lat, start_lon = positions[path[0]]
m = folium.Map(location=[start_lat, start_lon], zoom_start=14)

path_coords = []

# Add numbered markers for all path points
for idx, node in enumerate(path):
    lat, lon = positions[node]
    path_coords.append((lat, lon))

    # Different icon color for start, end, and mid points
    if idx == 0:
        icon = BeautifyIcon(icon_shape='marker', number=idx + 1, border_color='red', text_color='white', background_color='red')
        popup = f"Start - Node {node}"
    elif idx == len(path) - 1:
        icon = BeautifyIcon(icon_shape='marker', number=idx + 1, border_color='green', text_color='white', background_color='green')
        popup = f"End - Node {node}"
    else:
        icon = BeautifyIcon(icon_shape='marker', number=idx + 1, border_color='blue', text_color='white', background_color='blue')
        popup = f"Node {node}"

    folium.Marker(location=(lat, lon), popup=popup, icon=icon).add_to(m)

# Complete the loop by returning to the start
path_coords.append(path_coords[0])
folium.PolyLine(path_coords, color="blue", weight=3, opacity=0.6).add_to(m)

# Add popup with total path cost
folium.Marker(
    location=path_coords[0],
    popup=f"Total TSP Path Cost: {round(cost, 4)}",
    icon=folium.Icon(color='darkred', icon='info-sign')
).add_to(m)

# Save improved map
m.save("D:/NetworkX/tsp_map_readable.html")
print("Improved map saved as tsp_map_readable.html")

