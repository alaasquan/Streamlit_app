import streamlit as st
import rasterio
from rasterio.windows import Window
from PIL import Image
import numpy as np
import tempfile
import os
from rio_cogeo.cogeo import cog_translate
import time

st.title("COG TIFF")

# Function to read a GeoTIFF image with multiple bands
def read_image(file_path, band_order):
    with rasterio.open(file_path) as dataset:
        # Read the image data for the specified bands
        bands_data = [dataset.read(band) for band in band_order]

        # Stack the bands to create a multi-band image
        stacked_data = np.stack(bands_data, axis=-1)

        # Normalize the data to 0-255 for display
        normalized_data = (stacked_data / stacked_data.max()) * 255

        # Convert to uint8 to work with PIL
        uint8_data = normalized_data.astype(np.uint8)

        return uint8_data

# Function to convert GeoTIFF to COG
def convert_to_cog(input_path, output_path):
    with rasterio.open(input_path) as src_ds:
        profile = src_ds.profile.copy()

        # Specify the destination (dst) parameters
        dst_kwargs = {
            "driver": "COG",
            "blockxsize": 256,
            "blockysize": 256,
            "tiled": True,
            "compress": "deflate",
        }

        # Update the output path directly in the profile
        profile.update(dst_kwargs)

        # Convert to COG with the specified output path
        cog_translate(input_path, output_path, dst_kwargs=dst_kwargs)

# Function to get file size in MB
def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

# File uploader for GeoTIFF
tiff_file = st.file_uploader("Upload GeoTIFF File", type=["tif", "tiff"])

# Input band order with example for GeoTIFF
example_band_order = "4, 3, 2"  # Example: enter the band order as a comma-separated list
band_order_str = st.text_input(f"Enter the band order for GeoTIFF (e.g., '4,3,2' for RGB Sentinel-2 image):", value=example_band_order)
band_order = [int(band.strip()) for band in band_order_str.split(',') if band.strip()]

if tiff_file and band_order:
    # Save the uploaded GeoTIFF file to a temporary location
    temp_tiff_path = os.path.join(tempfile.gettempdir(), "uploaded_tiff.tif")
    with open(temp_tiff_path, "wb") as temp_file:
        temp_file.write(tiff_file.read())

    # Measure the start time for rendering the original GeoTIFF
    start_time_original = time.time()

    # Display the GeoTIFF image using PIL
    image_data = read_image(temp_tiff_path, band_order)
    image = Image.fromarray(image_data)
    st.image(image, caption="GeoTIFF Image", use_column_width=True)

    # Measure the end time for rendering the original GeoTIFF
    end_time_original = time.time()

    # Calculate the rendering time for the original GeoTIFF
    rendering_time_original = end_time_original - start_time_original
    st.text(f"Rendering time for original GeoTIFF: {rendering_time_original:.2f} seconds")

    # Display the size of the GeoTIFF image
    picture_size = get_file_size(temp_tiff_path)
    st.text(f"This GeoTIFF image has {picture_size:.2f} MegaBytes")

    # Specify the output path for COG
    cog_output_path = os.path.join(os.path.dirname(temp_tiff_path), f"{os.path.splitext(os.path.basename(temp_tiff_path))[0]}_COG.tif")

    

    # Convert to COG
    convert_to_cog(temp_tiff_path, cog_output_path)
    # Measure the start time for displaying the COG
    start_time_cog = time.time()
    
    # Display the COG image using PIL
    cog_image_data = read_image(cog_output_path, band_order)
    cog_image = Image.fromarray(cog_image_data)
    st.image(cog_image, caption="COG Image", use_column_width=True)
    # Measure the end time for displaying the COG
    end_time_cog = time.time()
    # Calculate the rendering time for the original GeoTIFF
    rendering_time_COG = end_time_cog - start_time_cog
    st.text(f"Rendering time for original GeoTIFF: {rendering_time_COG:.2f} seconds")

    # Display the size of the COG image
    cog_size = get_file_size(cog_output_path)
    st.text(f"This COG image has {cog_size:.2f} MegaBytes")

    # Clean up temporary files
    os.remove(temp_tiff_path)