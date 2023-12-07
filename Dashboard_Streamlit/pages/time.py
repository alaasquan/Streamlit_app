
from pathlib import Path
import streamlit as st
from io import BytesIO
from PIL import Image
import base64
import os
import tifffile as tiff
import matplotlib.pyplot as plt
import folium
from folium.raster_layers import ImageOverlay
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie

def load_lottiefile(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()


def load_lottirurl(url: str):
	r= requests.get(url)
	if r.status_code != 200:
		return None
	return r.json

loop= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/loop.json'
lottie_loop=load_lottiefile(loop)


col1, col2 = st.columns(2)

# Text for column 1
with col1:
    st.title("Raster Timelapse and Comparison")
# Text for column 2
with col2:


    st_lottie(lottie_loop,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='125px',
	   width='125px',)
# Specify the path to your GeoTIFF files
base='https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit'
base_path=str(base)
attributes = ["Pression", "Temperature", "Vitesse-Vent"]

# User input: Select attribute
selected_attribute_index = st.slider("Select Attribute", min_value=0, max_value=len(attributes)-1, step=1)
attribute_names = {0: "Pression", 1: "Temperature", 2: "Vitesse-Vent"}
selected_attribute = attributes[selected_attribute_index]
st.info(f"You have chosen the attribute : {attribute_names[selected_attribute_index]}")

# Generate a list of file paths based on the selected attribute and fixed days
days = [f"Jour{i}" for i in range(7)]
#selected_attribute_paths = [f"{base}/{day}-{selected_attribute}.tif" for day in days]
selected_attribute_paths = [os.path.join(base, f"{day}-{selected_attribute}.tif") for day in days]

# Display the generated paths

for i, path in enumerate(selected_attribute_paths):
    globals()[f"path{i}"] = path

# Replace tif_paths with the dynamically generated paths

tif_paths = selected_attribute_paths
st.write(tif_paths)

import requests

# Generate a list of file paths based on the selected attribute and fixed days
selected_attribute_paths = [f"{base}/Jour{i}-{selected_attribute}.tif" for i in range(7)]

# Create a temporary directory to store individual frames
temp_dir = "temp_frames"
os.makedirs(temp_dir, exist_ok=True)

# Function to download and read GeoTIFF files
def download_and_read_tiff(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Use a BytesIO object to read the content
    with BytesIO(response.content) as stream:
        img = tiff.imread(stream)
    return img

# Function to update the plot for each frame and save the image
def update_and_save(frame, tif_url):
    # Read TIFF image
    img = download_and_read_tiff(tif_url)

    # Create a figure and axis for the animation
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot the raster data
    plt.imshow(img, cmap='viridis', origin='upper', extent=(0, img.shape[1], 0, img.shape[0]))
    
    # Set the title to Jour{frame}
    plt.title(f"Jour{frame}")
    
    plt.axis('off')

    # Save the figure as an image in-memory
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)

    # Return the image data
    return buf.getvalue()

# Create the animation and save frames
frames = [update_and_save(frame, tif_url) for frame, tif_url in enumerate(selected_attribute_paths)]



# Save the frames as a GIF
gif_buffer = BytesIO()
Image.open(BytesIO(frames[0])).save(
    gif_buffer,
    save_all=True,
    append_images=[Image.open(BytesIO(frame)) for frame in frames[1:]],
    duration=1000,  # milliseconds per frame (adjust as needed)
    loop=0,  # 0 for infinite loop
    format="GIF"
)

# Encode the gif bytes to base64
gif_base64 = base64.b64encode(gif_buffer.getvalue()).decode()
import rasterio

# ... (previous code)

# Create a folium map
m = folium.Map(location=[28.7917, -7.0926], zoom_start=5)

# Add the basemap or any other layers to your map

# Extract bounds from GeoTIFF metadata
with rasterio.open(tif_paths[0]) as src:
    bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]]

# Add the GIF layer to the map
gif_layer = ImageOverlay(
    'data:image/gif;base64,' + gif_base64,
    bounds=bounds,
    opacity=0.7,
    name='GIF Layer'
).add_to(m)


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

min_value = attribute_limits[selected_attribute]["vmin"]
max_value = attribute_limits[selected_attribute]["vmax"]


# Choose the color palette based on the selected attribute
selected_palette = color_palettes[selected_attribute]

# Create a linear color map based on the selected palette
color_map = LinearColormap(selected_palette, vmin=min_value, vmax=max_value)

if selected_attribute == "Pression":
    color_map.caption = f"{selected_attribute} (hPa)"
elif selected_attribute == "Temperature":
    color_map.caption = f"{selected_attribute} (°C)"
elif selected_attribute == "Vitesse-Vent":
    color_map.caption = f"{selected_attribute} (Km/h)"



# Add the colormap to the map
m.add_child(color_map)

folium_static(m)