import streamlit as st
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Home page",
    page_icon="👋",
)

world_anim= r'C:\Users\Alaa\Desktop\StreamlitHajji\Dashboard_Streamlit\pages\Animation_Json\Worldmap.json'
dashboard= r"C:\Users\Alaa\Desktop\StreamlitHajji\Dashboard_Streamlit\pages\Animation_Json\dashboard.json"
def load_lottiefile(filepath: str):
	with open(filepath, 'r') as f:
		return json.load(f)

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
st.title("Meet the team")

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



("""

Our project is driven by the collaborative efforts of two members:

- **Mastari Wijdane:** & **Saqouane Alaa:** , geomatics and land surveying engineering students @Iav Hassan II .

""")

# Team Members
st.markdown('Team Members', unsafe_allow_html=True)
st.write("""
- **Wijdane:** [GitHub Profile](https://github.com/wijdanemastari)
- **Alaa:** [GitHub Profile](https://github.com/alaasquan)

Feel free to explore the dashboard, and let us know how we can enhance this geospatial analytics experience!
""")

# Display images of team members
col1, col2 = st.columns(2)

# Image for Wiju
with col1:
   
    wiju_image_path =r"D:\CV\MyResume\AlaaPics\wijdane.jpeg"
    wiju_image = Image.open(wiju_image_path)
    st.image(wiju_image, caption="Wijdane", use_column_width=True)

# Image for Weirdo
with col2:
    
    weirdo_image_path=r"D:\CV\MyResume\AlaaPics\Alaa-.jpeg"
    weirdo_image = Image.open(weirdo_image_path)
    st.image(weirdo_image, caption="Alaa", use_column_width=True)

st.sidebar.success("Select a page above.")
st_lottie(lottie_World_map,
	   speed= 0.75,
	   reverse=False,
	   loop=True,
	   quality='low',
	   height=None,
	   width=None,)

# Add typing text
st.markdown('<p class=" typing-text">Geoanalytic Dashboard : A project for WebMapping course - Geomatics school IAV Hassan II</p>', unsafe_allow_html=True)