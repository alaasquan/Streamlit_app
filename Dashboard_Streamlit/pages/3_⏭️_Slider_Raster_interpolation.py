import streamlit as st
import rasterio
import folium
import numpy as np
from streamlit_folium import folium_static
from rasterio.plot import reshape_as_image
from branca.colormap import LinearColormap
from pathlib import Path

st.title("GeoTIFF Image Viewer with Legend")


base='https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit'
attributes = ["Pression", "Temperature", "Vitesse-Vent"]

# User input: Select attribute and day
selected_attribute_index = st.slider("Select Attribute", min_value=0, max_value=len(attributes)-1, step=1)
selected_day = st.slider("Select Day", min_value=0, max_value=6)
days = [f"Jour{i}" for i in range(0, 7)]

# Announce the selected attribute
attribute_names = {0: "Pression", 1: "Temperature", 2: "Vitesse-Vent"}
st.success(f"Vous Avez choisis l'attribut: {attribute_names[selected_attribute_index]}")

# Get the selected attribute based on the index
selected_attribute = attributes[selected_attribute_index]

# Construct the file path based on user selection
tiff_path = Path(base) / f"{days[selected_day]}-{selected_attribute}.tif"
#real_tiff_path=

# Pre-define three color palettes
color_palettes = {
    "Pression": ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'],
    "Temperature": ['#440154', '#414287', '#27808e', '#46c06f', '#fde725'],
    "Vitesse-Vent": ['#0b0405', '#3e356b', '#3670a0', '#40b7ad', '#def5e5'],
}
# Define vmin and vmax for each attribute
attribute_limits = {
    "Pression": {"vmin": 0, "vmax": 100},
    "Temperature": {"vmin": 0, "vmax": 50},
    "Vitesse-Vent": {"vmin": 0, "vmax": 20},
}

# Get vmin and vmax based on selected attribute
min_value = attribute_limits[selected_attribute]["vmin"]
max_value = attribute_limits[selected_attribute]["vmax"]
# Choose the color palette based on the selected attribute
selected_palette = color_palettes[selected_attribute]

# Read the image data using rasterio
with rasterio.open(tiff_path) as dataset:
    bounds = dataset.bounds
    img_data = reshape_as_image(dataset.read([1, 2, 3]))

# Replace black color with transparency (assuming black is [0, 0, 0])
black_mask = (img_data[:, :, 0] == 0) & (img_data[:, :, 1] == 0) & (img_data[:, :, 2] == 0)

# Create a new array with the correct shape
alpha_channel = np.ones_like(img_data[:, :, 0], dtype=np.uint8) * 255  # Fully opaque
alpha_channel[black_mask] = 0  # Make the masked part fully transparent

# Add the alpha channel to the img_data
img_data_with_alpha = np.dstack((img_data, alpha_channel))

# Create a Folium map centered at the image bounds
map_center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
m = folium.Map(location=map_center, zoom_start=5,crs='EPSG3857')

# Add the GeoTIFF image as an overlay
folium.raster_layers.ImageOverlay(
    img_data_with_alpha,
    bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
    opacity=1,  # Adjust opacity if needed
).add_to(m)

# Create a linear color map based on the selected palette
color_map = LinearColormap(selected_palette, vmin=min_value, vmax=max_value)

# Add a title to the color map legend
color_map.caption = selected_attribute

# Add the color bar legend to the map
color_map.add_to(m)

# Display the Folium map
folium_static(m)
