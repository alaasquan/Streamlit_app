import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
from folium.plugins import MarkerCluster  # Import MarkerCluster
import plotly.express as px
from streamlit.components.v1 import html
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import base64
from PIL import Image
import json
from io import BytesIO
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

dashboard= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/chart.json'
lottie_dashboard=load_lottiefile(dashboard)


col1, col2, col3 = st.columns(3)

with col1:
    st_lottie(lottie_dashboard,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='250px',
	   width='200px',)
    
with col3:
    st_lottie(lottie_dashboard,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='250px',
	   width='200px',)
    
with col2:
    st.title('Geoanalytic interactive chart')
# Text for column 1

# Charger le GeoParquet
path = 'https://alaasquan.github.io/Streamlit_app/Wiju.geoparquet'
response = requests.get(path)
geoparquet_content = BytesIO(response.content)

gdf = gpd.read_parquet(geoparquet_content)

st.success("""
         This page is design to create an interactive chart based on the selected point.Please consider to select the **date** first to extract only the points that were collexted in the same date , then choose the id of the point you want to see its graphic chart.
         
         The graphic chart shows the variation of temperature , pression and wind speed through 7 days.

         **PS: Note that the data was created randomly and not based on a real source.** """)

# Fonction pour générer des dates séquentielles avec seulement le jour, le mois et l'année
def generate_dates(start_date, num_dates):
    # Convert the start_date string to a datetime object
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    
    return [(start_date - timedelta(days=i)).strftime('%d-%m-%Y') for i in range(num_dates)]

# Add a Selectbox to choose the date
start_date = '21-11-2023'  # Use a string for the starting date
num_dates = 7
dates = generate_dates(start_date, num_dates) 

date_rows_list = []
for date in dates:
    filtered_gdf = gdf[gdf['Date'] == date]
    rows_count = len(filtered_gdf)
    date_rows_list.append({'the date': date, 'nmbr_points': rows_count})

col1, col2 = st.columns(2)

# Add a Selectbox to choose the date in the first column
selected_date_numpoint = col1.selectbox("Select Date", date_rows_list)


# Retrieve the information for the selected date from the list
selected_date_str = selected_date_numpoint["the date"]
selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y")
# Create a list of the selected date and the 6 previous dates
selected_dates = [selected_date - timedelta(days=i) for i in range(6, -1, -1)]

# Convert the datetime objects back to string format if needed
selected_dates_str = [date.strftime("%d-%m-%Y") for date in selected_dates]

# Filter the GeoDataFrame based on the selected date
filtered_gdf = gdf[gdf['Date'] == selected_date_str]


# Gestion du clic sur la carte in the second column
selected_point = col2.selectbox("Sélect a point ID", filtered_gdf.index)


selected_point_data = filtered_gdf.loc[selected_point]

# Create a new folium map centered on the selected point
selected_point_map = folium.Map(location=[selected_point_data.geometry.y, selected_point_data.geometry.x], zoom_start=10)

# Add Marker for the selected point
popup_content_selected_point = f"<strong>Point ID:</strong> {selected_point}<br>" \
                               f"<strong>Nom:</strong> {selected_point_data['Nom']}<br>" \
                               f"<strong>Densité_de_population(/m²):</strong> {selected_point_data['Densité_de_population(/m²)']}<br>" \
                               f"<strong>Taux_Alphabétisme(%):</strong> {selected_point_data['Taux_Alphabétisme(%)']}<br>"

folium.Marker([selected_point_data.geometry.y, selected_point_data.geometry.x],
              popup=popup_content_selected_point).add_to(selected_point_map)

# Show the folium map with the selected point
st.subheader(f"Selected Point - ID: {selected_point}")
folium_static(selected_point_map)

# Create Plotly figure for the selected point
fig_selected_point = px.line(title=f"Données spatio-temporelles - Point ID: {selected_point}",
                              labels={'value': 'Valeur', 'variable': 'Attribut'},
                              width=800,
                              height=500)

attribut1_values_selected_point = [selected_point_data[f"Jour{j}-Pression(hPa)"] for j in range(6, -1, -1)]
fig_selected_point.add_scatter(x=selected_dates_str, y=attribut1_values_selected_point, mode='lines+markers', name='Pression(hPa)')

attribut2_values_selected_point = [selected_point_data[f"Jour{k}-Vitesse_Vent(Km/h)"] for k in range(6, -1, -1)]
fig_selected_point.add_scatter(x=selected_dates_str, y=attribut2_values_selected_point, mode='lines+markers', name='Vitesse_Vent(Km/h)')

attribut3_values_selected_point = [selected_point_data[f"Jour{n}-Température(en °C)"] for n in range(6, -1, -1)]
fig_selected_point.add_scatter(x=selected_dates_str, y=attribut3_values_selected_point, mode='lines+markers', name='Température(en °C)')

# Show the graphic chart for the selected point
st.plotly_chart(fig_selected_point)

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Figure_pointID_{selected_point}.pdf">Download file</a>'


    # Export the page to PDF
export_as_pdf = st.button("Export Report")

if export_as_pdf:
    pdf = FPDF()

    pdf.add_page()

    # Save Plotly figure as a PNG image
    with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig_selected_point.write_image(tmpfile.name)

        # Embed the PNG image in the PDF
        pdf.image(tmpfile.name, 10, 10, 200, 100)

    # Provide a download link for the generated PDF
    html_link = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
    st.markdown(html_link, unsafe_allow_html=True)