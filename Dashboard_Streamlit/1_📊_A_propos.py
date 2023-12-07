import streamlit as st
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Home page",
    page_icon="👋",
)

world_anim= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/Worldmap.json'
dashboard= 'https://alaasquan.github.io/Streamlit_app/Dashboard_Streamlit/Animation_Lottiefiles/dashboard.json'

def load_lottiefile(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()


def load_lottirurl(url: str):
	r= requests.get(url)
	if r.status_code != 200:
		return None
	return r.json

lottie_World_map=load_lottiefile(world_anim)
lottie_dashboard=load_lottiefile(dashboard)

# Add animation CSS
st.markdown(
    """
    <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Geospatial Analytics Dashboard")
st.sidebar.success("Select a page above.")
st_lottie(lottie_World_map,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height=None,
	   width=None,)

# Add animation CSS
# CSS styles for animations
css_styles = """
<style>
.bounce {
    animation: bounce 2s infinite;
    font-weight: bold; /* Bold text */
    font-size: 20px;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-20px);
    }
    60% {
        transform: translateY(-10px);
    }
}

.bg-title {
    background-color: #2d4059; /* Background color for titles */
    color: white; /* Text color for titles */
    padding: 5px 10px;
    display: inline-block;
    margin-bottom: 10px;
}

.typing-text {
    overflow: hidden;
    white-space: nowrap;
    animation: typing 3s steps(20, end) infinite;
}

@keyframes typing {
    from {
        width: 0;
    }
    to {
        width: 100%;
    }
}
</style>
"""
st.markdown(
    """
    <style>
        .bg-title {
            font-size: 20px ;
            color: black; /* Text color for titles */
            padding: 5px 10px;
            display: inline-block;
            margin-bottom: 5px;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Display CSS styles
st.markdown(css_styles, unsafe_allow_html=True)

# Add typing text
st.markdown('<p class=" typing-text">A project for WebMapping course - Geomatics school IAV Hassan II</p>', unsafe_allow_html=True)

# Project Description
st.write(""" ### 📌Project Overview""")
# Create two text columns
col1, col2 = st.columns(2)

# Text for column 1
with col1:
    st.write("""
             
    Welcome to our Geospatial Analytics Dashboard, where we bring data to life through interactive maps and insightful analytics.
    
    Our project revolves around the creation of a dynamic dashboard using the Streamlit library, designed to empower users with spatial and temporal insights.""")
# Text for column 2
with col2:

    st_lottie(lottie_dashboard,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height='250px',
	   width='250px',)



### 
st.write("""
         
### Key Features:        
 - **Spatial and Temporal Analysis:** Visualize data not only in space but also across time, allowing for a comprehensive understanding of trends and patterns.

- **Search and Query:** Effortlessly search for specific points on the map and conduct both spatial and feature queries to extract valuable information.

- **GeoTIFF to COG Converter:** Convert GeoTIFF files to Cloud-Optimized GeoTIFF (COG) format, optimizing storage and facilitating efficient data sharing.
""")

# Fade-in animation
st.markdown('<div class=" bg-title bounce">Why Streamlit?</div>', unsafe_allow_html=True)


("""
### 
We chose Streamlit for its user-friendly map implementation and its effectiveness in simplifying complex data analytics. The platform's intuitive interface enables users to interact with data effortlessly.

### 📊About Data
The data used in this project was created arbitrarily while we choose randomly 1000points located in Morocco and added the necessary features
		 - That is why the data value may not make any sense or logic.
		 - The data was created through a collab notebook , see link 👉🏻[here](https://colab.research.google.com/drive/1NX7QngORBa2dV5Pu9t_-Sk13_o6Ktn-x)
		 


Feel free to explore the dashboard, and let us know how we can enhance this geospatial analytics experience!
""")


