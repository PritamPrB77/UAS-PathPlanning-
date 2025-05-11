import pandas as pd
import math
import folium
import networkx as nx
from folium.plugins import BeautifyIcon

# Sample UAV dataset
data = {
    "Point ID": ["A", "B", "C"],
    "Latitude": [28.6139, 28.7041, 28.5355],
    "Longitude": [77.2090, 77.1025, 77.3910],
    "Risk Score": [8, 10, 0]
}
df = pd.DataFrame(data)

# Clean and reset
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df['Risk Score'] = pd.to_numeric(df['Risk Score'], errors='coerce')
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Graph construction
G = nx.Graph()
positions = {}
risks = {}

for i in range(len(df)):
    lat, lon, risk = df.loc[i, ['Latitude', 'Longitude', 'Risk Score']]
    G.add_node(i)
    positions[i] = (lat, lon)
    risks[i] = risk

# Max values for normalization
max_distance = 0
for i in G.nodes:
    for j in G.nodes:
        if i != j:
            lat1, lon1 = positions[i]
            lat2, lon2 = positions[j]
            dist = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
            max_distance = max(max_distance, dist)
max_risk = max(risks.values())

# Add edges with combined cost = norm_dist * norm_avg_risk
for i in G.nodes:
    for j in G.nodes:
        if i != j:
            lat1, lon1 = positions[i]
            lat2, lon2 = positions[j]
            distance = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
            avg_risk = (risks[i] + risks[j]) / 2
            norm_dist = distance / max_distance
            norm_risk = avg_risk / max_risk
            combined_cost = norm_dist * norm_risk
            G.add_edge(i, j, weight=combined_cost)

# Nearest Neighbor TSP
def nearest_neighbor_combined(graph, start):
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
path, cost = nearest_neighbor_combined(G, 0)

# Draw map
start_lat, start_lon = positions[path[0]]
m = folium.Map(location=[start_lat, start_lon], zoom_start=13)
path_coords = []

for idx, node in enumerate(path):
    lat, lon = positions[node]
    path_coords.append((lat, lon))
    icon_color = 'red' if idx == 0 else ('green' if idx == len(path)-1 else 'blue')
    icon = BeautifyIcon(icon_shape='marker', number=idx + 1, border_color=icon_color, text_color='white', background_color=icon_color)
    folium.Marker(location=(lat, lon), popup=f"Node {df.loc[node, 'Point ID']}", icon=icon).add_to(m)

path_coords.append(path_coords[0])
folium.PolyLine(path_coords, color="blue", weight=3, opacity=0.6).add_to(m)

folium.Marker(
    location=path_coords[0],
    popup=f"Total Combined Path Cost: {round(cost, 4)}",
    icon=folium.Icon(color='darkred', icon='info-sign')
).add_to(m)

# Save map to file
m.save("uav_tsp_combined_cost.html")
print("Map saved as 'uav_tsp_combined_cost.html'")
