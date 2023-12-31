import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64
import os
import folium
from streamlit_folium import folium_static as st_folium_static
from folium.plugins import DualMap
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



path = 'https://alaasquan.github.io/Streamlit_app/Wiju.geoparquet'
response = requests.get(path)
geoparquet_content = BytesIO(response.content)
gdf = gpd.read_parquet(geoparquet_content)
# Title for the Streamlit app

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

st.write('  ')

# Sidebar for selecting the property
selected_property = st.sidebar.selectbox('Select Property', ["Pression(hPa)", "Vitesse_Vent(Km/h)", "Température(en °C)"], key="unique_key_property")


# Get the columns ending with the selected property
day_columns = [col for col in gdf.columns if col.endswith(selected_property)]

if day_columns:
    # Create a temporary directory to store individual frames
    temp_dir = "temp_frames"
    os.makedirs(temp_dir, exist_ok=True)

    # Function to update the plot for each frame and save the image
    def update_and_save(frame):
        # Create a figure and axis for the animation
        fig, ax = plt.subplots(figsize=(10, 8))
        # Plot the raster data for the current frame
        column_name = day_columns[frame]
        filtered_data = gdf[gdf[column_name].notnull()]
        plot=filtered_data.plot(column=column_name,cmap='coolwarm', legend=True, ax=ax)
        plt.title(f"Raster Timelapse Frame {frame + 1} - {column_name}",color='white')
         # Customize the legend text color (replace 'blue' with your desired color
        plt.axis('off')
        # Save the figure as an image in the temporary directory
        temp_path = os.path.join(temp_dir, f"frame_{frame}.png")
        plt.savefig(temp_path, format='png', bbox_inches="tight", pad_inches=0, transparent=True)
        plt.close(fig)

    # Create the animation and save frames
    for frame in range(len(day_columns)):
        update_and_save(frame)

    # Read frames back into the frames list
    frames = []
    for frame in range(len(day_columns)):
        temp_path = os.path.join(temp_dir, f"frame_{frame}.png")
        frames.append(Image.open(temp_path).convert("RGBA"))

    # Save the frames as a GIF
    gif_buffer = BytesIO()
    frames[0].save(
        gif_buffer,
        save_all=True,
        append_images=frames[1:],
        duration=1000,  # milliseconds per frame (adjust as needed)
        loop=0,  # 0 for infinite loop
        format="GIF"
    )

    # Encode the gif bytes to base64
    gif_base64 = base64.b64encode(gif_buffer.getvalue()).decode()

    # Display the gif in Streamlit using st.markdown and HTML
    st.markdown(f'<img src="data:image/gif;base64,{gif_base64}" alt="gif">', unsafe_allow_html=True)

   
