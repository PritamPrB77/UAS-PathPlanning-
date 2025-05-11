import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import folium
from folium.plugins import BeautifyIcon

# Load dataset
df = pd.read_csv("D:/NetworkX/tsp_locations_abs_cost.csv")
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
df.reset_index(drop=True, inplace=True)

# Limit dataset (optional)
df = df.head(100)  # Change this as needed

# Coordinates array
coords = df[['Latitude', 'Longitude']].to_numpy()

# Build KDTree for fast nearest neighbor queries
tree = KDTree(coords)

# Optimized Nearest Neighbor TSP using KDTree
def nearest_neighbor_tsp_kdtree(coords):
    n = len(coords)
    visited = set()
    path = []
    current_idx = 0
    visited.add(current_idx)
    path.append(current_idx)
    total_cost = 0

    for _ in range(n - 1):
        dist, idxs = tree.query(coords[current_idx], k=n)  # all other nodes
        for i in idxs:
            if i not in visited:
                next_idx = i
                break
        total_cost += np.linalg.norm(coords[current_idx] - coords[next_idx])
        visited.add(next_idx)
        path.append(next_idx)
        current_idx = next_idx

    # Return to start
    total_cost += np.linalg.norm(coords[current_idx] - coords[path[0]])
    path.append(path[0])

    return path, total_cost

# Run TSP
path, cost = nearest_neighbor_tsp_kdtree(coords)
print("Total Path Cost:", round(cost, 4))

# --- Map Visualization ---
m = folium.Map(location=[coords[path[0]][0], coords[path[0]][1]], zoom_start=13)
path_coords = []

for idx, node in enumerate(path):
    lat, lon = coords[node]
    path_coords.append((lat, lon))

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

folium.PolyLine(path_coords, color="blue", weight=3, opacity=0.6).add_to(m)
folium.Marker(location=path_coords[0], popup=f"Total TSP Cost: {round(cost, 2)}", icon=folium.Icon(color='darkred')).add_to(m)
m.save("D:/NetworkX/tsp_large_optimized2.html")
print("✅ Map saved as tsp_large_optimized.html")
