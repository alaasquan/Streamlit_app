import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static as st_folium_static
import os
from branca.colormap import LinearColormap
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie
from pathlib import Path

def load_lottiefile(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()


def load_lottirurl(url: str):
	r= requests.get(url)
	if r.status_code != 200:
		return None
	return r.json

split=  'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/split.json'
lottie_split=load_lottiefile(split)


col1, col2 ,col3= st.columns(3)
with col3:
    st.write("")
# Text for column 1
with col2:
    st.title("Raster Splitmap ")
# Text for column 2
with col1:


    st_lottie(lottie_split,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='200px',
	   width='200px',)
    

# Define the directory where your images are stored
images_directory ='https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit'


# Get a list of all image files in the directory
#image_files = []

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
#tiff_path_left = os.path.join(images_directory, image_name_left)
#tiff_path_right = os.path.join(images_directory, image_name_right)
tiff_path_left= f"{images_directory}/{image_name_left}"
tiff_path_right=  f"{images_directory}/{image_name_right}"
#tiff_path_left = Path(images_directory) / image_name_left
#tiff_path_right = Path(images_directory) / image_name_right
tiff_path_left_str = str(tiff_path_left)
tiff_path_right_str = str(tiff_path_right)

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
