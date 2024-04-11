import plotly.express as px

# Define center coordinates of Paris (latitude, longitude)
center_lat = 48.8566
center_lon = 2.3522

# Create a sample heatmap data (replace with your data)
heatmap_data = dict(
    lat=[48.87, 48.85, 48.82],
    lon=[2.37, 2.34, 2.32],
    value=[50, 30, 10]
)

# Create the map with heatmap
fig = px.density_mapbox(
    lat=heatmap_data["lat"],
    lon=heatmap_data["lon"],
    z=heatmap_data["value"],
    mapbox_style="open-street-map",
    center=dict(lat=center_lat, lon=center_lon),
    zoom=12,
)

# Optional: Add a title
fig.update_layout(title="Simple Heatmap over Paris Map (Toy Example)")

fig.show()
