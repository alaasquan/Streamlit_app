import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static as st_folium_static
import os
from branca.colormap import LinearColormap

st.title("Split Panel Raster Maps")

# Define the directory where your images are stored
images_directory = r"C:\Users\Alaa\Desktop\StreamlitHajji\Dashboard_Streamlit"

# Get a list of all image files in the directory
image_files = [file for file in os.listdir(images_directory) if file.endswith(".tif")]

# Create select boxes for choosing attribute and day
attribute = st.selectbox("Select Attribute", ["Pression", "Temperature", "Vitesse-Vent"])

# Use st.beta_columns to place day_left and day_right in the same line
day_left_col, day_right_col = st.columns(2)
day_left = day_left_col.selectbox("Select Day (Left Layer)", ["Jour0", "Jour1", "Jour2", "Jour3", "Jour4", "Jour5", "Jour6"])
day_right = day_right_col.selectbox("Select Day (Right Layer)", ["Jour0", "Jour1", "Jour2", "Jour3", "Jour4", "Jour5", "Jour6"])

# Construct the image names based on the selected attribute and day
image_name_left = f"{day_left}-{attribute}.tif"
image_name_right = f"{day_right}-{attribute}.tif"

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
min_value = attribute_limits[attribute]["vmin"]
max_value = attribute_limits[attribute]["vmax"]

# Choose the color palette based on the selected attribute
selected_palette = color_palettes[attribute]

# Construct the full paths for the selected layers
tiff_path_left = os.path.join(images_directory, image_name_left)
tiff_path_right = os.path.join(images_directory, image_name_right)

# Load the GeoTIFFs into Leafmap
m = leafmap.Map()
m.split_map(tiff_path_left, tiff_path_right)

# Create a linear color map based on the selected palette
color_map = LinearColormap(selected_palette, vmin=min_value, vmax=max_value)

# Customize the caption based on the selected attribute
if attribute == "Pression":
    color_map.caption = f"{attribute} (hPa)"
elif attribute == "Temperature":
    color_map.caption = f"{attribute} (°C)"
elif attribute == "Vitesse-Vent":
    color_map.caption = f"{attribute} (Km/h)"

# Add the colormap to the map
m.add_child(color_map)

# Display the map in Streamlit
st_folium_static(m)
