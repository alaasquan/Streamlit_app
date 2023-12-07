import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import re
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import base64

from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie

import requests
from io import BytesIO

def load_lottiefile(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()


def load_lottirurl(url: str):
	r= requests.get(url)
	if r.status_code != 200:
		return None
	return r.json

search= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/searchhhh.json'
lottie_search=load_lottiefile(search)


# Charger le GeoParquet
path = 'https://alaasquan.github.io/Streamlit_app/Wiju.geoparquet'
response = requests.get(path)
geoparquet_content = BytesIO(response.content)

gdf = gpd.read_parquet(geoparquet_content)

col1, col2= st.columns(2)

# Text for column 1
with col1:
    st.title("Search a point in Map")
# Text for column 2
with col2:

    st_lottie(lottie_search,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='150px',
	   width='170px',)


# Sidebar with a multiselect widget for selecting coordinates
selected_coordinates = st.sidebar.multiselect(
    "Select Coordinates",
    gdf.geometry.apply(lambda geom: (geom.x, geom.y)),
    format_func=lambda coords: f"({coords[0]}, {coords[1]})"
)

# Display the selected points on the map

if selected_coordinates:
    st.success("this is the selected Points on the Map , click on the marker to show some information")
    # Filter GeoDataFrame based on selected coordinates
    selected_points = gdf[gdf.geometry.apply(lambda geom: (geom.x, geom.y)).isin(selected_coordinates)]

    # Create a Folium map centered on the first selected point
    m = folium.Map(location=[selected_points.iloc[0].geometry.y, selected_points.iloc[0].geometry.x], zoom_start=5)

    # Add the selected points to the map
    for _, point in selected_points.iterrows():
        popup_content = f"Nom: {point['Nom']}<br>Point<br>Densité_de_population(/m²): {point['Densité_de_population(/m²)']}<br>Taux_Alphabétisme(%): {point['Taux_Alphabétisme(%)']}<br>Date: {point['Date']}"
        folium.Marker(
            location=[point.geometry.y, point.geometry.x],
            popup=folium.Popup(popup_content, max_width=300),  # Adjust max_width as needed
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    # Display the map using folium_static
    folium_static(m)

else:
    st.warning("Choose coordinates in the sidebar")



   
