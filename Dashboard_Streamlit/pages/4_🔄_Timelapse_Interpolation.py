from pathlib import Path
import streamlit as st
from io import BytesIO
from PIL import Image
import base64
import os
import tifffile as tiff
import matplotlib.pyplot as plt

# Specify the path to your GeoTIFF files
base_path = Path(r"C:\Users\Alaa\Desktop\StreamlitHajji\Dashboard_Streamlit")
attributes = ["Pression", "Temperature", "Vitesse-Vent"]

# User input: Select attribute
selected_attribute_index = st.slider("Select Attribute", min_value=0, max_value=len(attributes)-1, step=1)
attribute_names = {0: "Pression", 1: "Temperature", 2: "Vitesse-Vent"}
selected_attribute = attributes[selected_attribute_index]
st.info(f"Vous avez choisi l'attribut : {attribute_names[selected_attribute_index]}")

# Generate a list of file paths based on the selected attribute and fixed days
days = [f"Jour{i}" for i in range(7)]
selected_attribute_paths = [base_path / f"{day}-{selected_attribute}.tif" for day in days]

# Display the generated paths
st.write("Generated File Paths:")
for i, path in enumerate(selected_attribute_paths):
    
    globals()[f"path{i}"] = path


# Replace tif_paths with the dynamically generated paths
tif_paths = [
    path0,
    path1,
    path2,
    path3,
    path4,
    path5,
    path6
]

# Create a temporary directory to store individual frames
temp_dir = "temp_frames"
os.makedirs(temp_dir, exist_ok=True)

# Function to update the plot for each frame and save the image
def update_and_save(frame, tif_path):
    # Read TIFF image
    img = tiff.imread(tif_path)

    # Create a figure and axis for the animation
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot the raster data
    plt.imshow(img, cmap='viridis', origin='upper', extent=(0, img.shape[1], 0, img.shape[0]))
    plt.title(f"Raster Timelapse Frame {frame + 1} - {os.path.basename(tif_path)}")
    plt.axis('off')

    # Save the figure as an image in the temporary directory
    temp_path = os.path.join(temp_dir, f"frame_{frame}.png")
    plt.savefig(temp_path, format='png', bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)

# Create the animation and save frames
for frame, tif_path in enumerate(tif_paths):
    update_and_save(frame, tif_path)

# Read frames back into the frames list
frames = []
for frame in range(len(tif_paths)):
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
