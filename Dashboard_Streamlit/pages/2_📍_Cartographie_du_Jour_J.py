import streamlit as st
import geopandas as gpd
import plotly.express as px
from tempfile import NamedTemporaryFile
import base64
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import requests
import streamlit as st
import geopandas as gpd
import plotly.express as px
import numpy as np
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

world_anim= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/carto_jour.json'
lottie_jour=load_lottiefile(world_anim)


def create_proportional_symbols_map(gdf, selected_day, selected_property):
    # Define interval labels for each property_name
    interval_data_dict = {
            'Pression(hPa)': {
                1: {'label': 'Très Basse Pression', 'size': 10},
                2: {'label': 'Basse Pression', 'size': 30},
                3: {'label': 'Moyenne Pression', 'size': 50},
            },
            'Température(en °C)': {
                1: {'label': 'Climat froid', 'size': 10},
                2: {'label': 'Climat froid à modéré', 'size': 20},
                3: {'label': 'Climat modéré à chaud', 'size': 30},
                4: {'label': 'Climat chaud', 'size': 50},
            },
            'Vitesse_Vent(Km/h)': {
                3: {'label': 'Petite brise', 'size': 10},
                1: {'label': 'Très leger brise', 'size': 20},
                2: {'label': 'Légère brise', 'size': 40},
            },
        }

# Extract the property name from the selected_property
    property_name = selected_property.split('-')[-1].strip()

# Display interval labels for the selected property_name
    interval_data = interval_data_dict.get(property_name, {})

# Define the number of intervals for each property_name
    num_intervals_dict = {
        'Pression(hPa)': 3,
        'Vitesse_Vent(Km/h)': 3,
        'Température(en °C)': 4,
    # Add other property_name: num_intervals mappings as needed
    }

# Get the number of intervals for the selected property_name or raise an error if not found
    num_intervals = num_intervals_dict.get(property_name,3) 
 # Create equal intervals for the selected property
    gdf['interval'] = pd.cut(gdf[selected_property], bins=num_intervals, labels=False).astype(int) + 1

    # Create a DataFrame for interval information
    interval_info = pd.DataFrame({
        'interval': range(1, num_intervals + 1),
        'interval_data': [interval_data.get(i, {'label': f'Interval {i}', 'size': 0}) for i in range(1, num_intervals + 1)]
    })

    # Merge the interval information with the original GeoDataFrame
    gdf = pd.merge(gdf, interval_info, on='interval', how='left')

    # Map each row to its corresponding interval size
    gdf['size_interval'] = gdf['interval_data'].apply(lambda data: data['size'])
    
    gdf['interval_label'] = gdf['interval_data'].apply(lambda x: x.get('label')).astype(str)
    
# Create the proportional symbols map with interval-based sizes
    fig = px.scatter_mapbox(gdf,
                        lat=gdf.geometry.y,
                        lon=gdf.geometry.x,
                        size='size_interval',
                        color_discrete_sequence=['black'],  # Use the size_interval column for marker sizes
                        color='interval_label',  # Color markers based on interval names for distinction
                        mapbox_style="carto-positron",
                        title=f'Proportional Symbols Map for {property_name} on {selected_day}',
                        hover_data={'size_interval': True, 'interval_label': True},
                        )

    # Customize the hover tooltip message to include interval name, size_interval, and selected_property
    fig.update_traces(hovertemplate='<b>Classe:</b> %{customdata[1]}<br>'
                                '<b>Radius:</b> %{customdata[0]:.2f}<br>'
                                '<b>Latitude:</b> %{lat:.4f}<br>'
                                '<b>Longitude:</b> %{lon:.4f}<extra></extra>',
                    showlegend=False)  # Set showlegend to False

    # Return the Plotly figure
    return fig


    # Function to create proportional symbols map
def create_graduated_color_map(gdf, selected_day, selected_property):
    # Create a density map for the selected property and day
    fig = px.density_mapbox(gdf,
                        lat=gdf.geometry.y,
                        lon=gdf.geometry.x,
                        z=gdf[selected_property],
                        radius=10,
                        mapbox_style="carto-positron",
                        title=f'Density Map for {selected_property} on {selected_day}',
                        )

    # Return the Plotly figure
    return fig

# Function to create download link for PDF
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

# Title for the Streamlit app
st.title("Choose Map Type and Display")
col1, col2 , col3 = st.columns(3)

# Text for column 1
with col1:
    st.write('')
# Text for column 2
with col2:


    st_lottie(lottie_jour,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='275px',
	   width='250px',)
with col3:
    st.write('')

path = 'https://alaasquan.github.io/Streamlit_app/Wiju.geoparquet'
response = requests.get(path)
geoparquet_content = BytesIO(response.content)
gdf = gpd.read_parquet(geoparquet_content)

# Sidebar for selecting the day
selected_day = st.sidebar.selectbox('Select Day', ['Jour0', 'Jour1', 'Jour2', 'Jour3', 'Jour4', 'Jour5', 'Jour6'])

# Get the properties columns for the selected day
properties_for_day = [col for col in gdf.columns if col.startswith(selected_day)]

# Choose the property using a selectbox
selected_property = st.sidebar.selectbox(f'Select Property for {selected_day}', properties_for_day)

# Buttons in the same line with icons
button_col1, button_col2 = st.columns(2)
map_type= ""
# Initialize the fig variable outside the if blocks
fig = None

# Button with icon for Proportional Symbols Map
with button_col1:
    if st.button("Proportional Symbols Map ", key="proportional_button"):
        map_type ="Proportional Symbols Map"
        fig = create_proportional_symbols_map(gdf, selected_day, selected_property)
        
# Button with icon for Graduated Color Symbol Map
with button_col2:
    if st.button("Graduated Color Symbol Map ", key="graduated_button"):
        map_type ="Graduated Color Symbol Map"
        fig = create_graduated_color_map(gdf, selected_day, selected_property)
        

if map_type =="Proportional Symbols Map" and fig:
    st.plotly_chart(fig)
    

elif map_type =="Graduated Color Symbol Map" and fig:
    st.plotly_chart(fig)   

    
