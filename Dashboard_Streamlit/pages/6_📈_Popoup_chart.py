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
import matplotlib.pyplot as plt
from io import BytesIO
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

dashboard='https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/chart.json'
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
    st.title('Geoanalytic Popup Chart')


# Charger la GeoDataFrame depuis le fichier geoparquet


# Charger le GeoParquet
path = 'https://alaasquan.github.io/Streamlit_app/Wiju.geoparquet'
response = requests.get(path)
geoparquet_content = BytesIO(response.content)

gdf = gpd.read_parquet(geoparquet_content)
st.success('Click on a marker to display the chart in a popup')


# Afficher la carte interactive avec Folium
m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=5)

# DÃ©finir une variable pour stocker l'index du point sÃ©lectionnÃ©
selected_point_idx = None
def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Figure_pointID_{selected_point_idx}.pdf">Download file</a>'

def on_click(e):
    global selected_point_idx
    # RÃ©cupÃ©rer l'index du point cliquÃ©
    selected_point_idx = e.target.options['custom_id']

Attibut=['Pression(hPa)', 'Vitesse_Vent(Km/h)' , 'Température(en °C)' ]
# Ajouter des marqueurs Ã  la carte avec des identifiants personnalisÃ©s
for idx, row in gdf.iterrows():
    popup_content = f"<strong>Point ID:</strong> {idx}<br>" \
                    f"<strong>Nom:</strong> {row['Nom']}<br>" \
                    f"<strong>Densité_de_population(/m²):</strong> {row['Densité_de_population(/m²)']}<br>" \
                    f"<strong>Taux_Alphabétisme(%):</strong> {row['Taux_Alphabétisme(%)']}<br>"
    
    # CrÃ©er un graphique avec Matplotlib
    fig, ax = plt.subplots(figsize=(6, 3))
    for i in range(0, 3):  # Supposant que vous avez 3 attributs
        attribut_columns = [f'Jour{j}-{Attibut[i]}' for j in range(6, -1, -1)]
        attribut_values = [row[col] for col in attribut_columns]
        ax.plot(range(7), attribut_values, label=f'Attribut {i}')

    ax.set_title("Données spatio-temporelles")
    ax.set_xlabel("Jours")
    ax.set_ylabel("Valeur")
    ax.legend()

    # Convertir le graphique en image
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    
    # Convertir l'image en base64
    image_base64 = base64.b64encode(image_stream.read()).decode()

    # Ajouter le contenu HTML de l'image comme popup sur la carte Leaflet
    popup = folium.Popup(f"<img src='data:image/png;base64,{image_base64}'/>", max_width=800)
    marker = folium.Marker([row.geometry.y, row.geometry.x],
                          popup=popup,
                          tooltip=f"Point ID: {idx}",
                          custom_id=idx)  # Ajouter un attribut personnalisÃ© pour stocker l'index
    marker.add_to(m)

# Afficher la carte dans le Dashboard
folium_static(m)

# Afficher le graphique en tant que popup une fois le point cliquÃ©
if selected_point_idx is not None:
    st.write(f"Graphique du point sÃ©lectionnÃ© (ID: {selected_point_idx}):")
    selected_point_data = gdf.loc[selected_point_idx]

    # CrÃ©er un graphique avec Matplotlib
    fig, ax = plt.subplots(figsize=(8, 5))
    for i in range(1, 4):  # Supposant que vous avez 3 attributs
        attribut_columns = [f"Attibut{i}Jour-{j}" for j in range(6, -1, -1)]
        attribut_values = [selected_point_data[col] for col in attribut_columns]
        ax.plot(range(7), attribut_values, label=f'Attribut {i}')

    ax.set_title("Donnéees spatio-temporelles")
    ax.set_xlabel("Jours")
    ax.set_ylabel("Valeur")
    ax.legend()

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)
    st.write(selected_point_idx)

        # Export the page to PDF
    export_as_pdf = st.button("Export Report")

    if export_as_pdf:
        pdf = FPDF()

        pdf.add_page()

        # Save Plotly figure as a PNG image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.write_image(tmpfile.name)

            # Embed the PNG image in the PDF
            pdf.image(tmpfile.name, 10, 10, 200, 100)

        # Provide a download link for the generated PDF
        html_link = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
        st.markdown(html_link, unsafe_allow_html=True)

