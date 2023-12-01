import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
import folium
import re
path = r"C:\Users\Alaa\Desktop\StreamlitHajji\Wiju.geoparquet"
gdf = gpd.read_parquet(path)

# Sidebar with a multiselect widget for selecting coordinates
selected_coordinates = st.sidebar.multiselect(
    "Select Coordinates",
    gdf.geometry.apply(lambda geom: (geom.x, geom.y)),
    format_func=lambda coords: f"({coords[0]}, {coords[1]})"
)

# Display the selected points on the map
st.header("Selected Points on the Map")
if selected_coordinates:
    # Filter GeoDataFrame based on selected coordinates
    selected_points = gdf[gdf.geometry.apply(lambda geom: (geom.x, geom.y)).isin(selected_coordinates)]

    # Create a Folium map centered on the first selected point
    m = folium.Map(location=[selected_points.iloc[0].geometry.y, selected_points.iloc[0].geometry.x], zoom_start=5)

    # Add the selected points to the map
    for _, point in selected_points.iterrows():
        #Extract ID of the point 
        input_string = point['Nom']

        Id_point = ""
        for char in input_string:
            if char.isdigit():
                Id_point += char

        popup_content = f"Point: {Id_point}<br>Densité_de_population(/m²): {point['Densité_de_population(/m²)']}<br>Taux_Alphabétisme(%): {point['Taux_Alphabétisme(%)']}<br>Nom: {point['Nom']}<br>Date: {point['Date']}"
        folium.Marker(
            location=[point.geometry.y, point.geometry.x],
            popup=folium.Popup(popup_content, max_width=300),  # Adjust max_width as needed
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    # Display the map using folium_static
    folium_static(m)
else:
    st.warning("No points selected.")
