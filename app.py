import streamlit as st
import cv2
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# 1) Load colors.csv
@st.cache_data
def load_colors():
    # No header row; columns: index, name, hex, R, G, B
    return pd.read_csv('colours.csv',
                       names=["idx","color_name","hex","R","G","B"],
                       header=None)

colors = load_colors()

# 2) App UI
st.title("🎨 Color Detection App")
st.write("Upload an image, then click anywhere on it to detect the color.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg","jpeg","png"])
if not uploaded_file:
    st.warning("Please upload an image to get started.")
    st.stop()

# 3) Load and display the image via the click component
pil_img = Image.open(uploaded_file).convert("RGB")
img_array = np.array(pil_img)
img_bgr   = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

# This single call both shows the image and captures click coords
coords = streamlit_image_coordinates(pil_img, key="clicker")

# Helper: nearest‐color lookup
def get_color_name(R, G, B):
    min_dist = float('inf'); name = "Unknown"
    for _, row in colors.iterrows():
        d = abs(R-row.R) + abs(G-row.G) + abs(B-row.B)
        if d < min_dist:
            min_dist = d
            name = row.color_name
    return name

# 4) If clicked, show the color info
if coords:
    x, y = int(coords["x"]), int(coords["y"])
    b, g, r = img_bgr[y, x]
    hex_code = f"#{r:02x}{g:02x}{b:02x}"
    name = get_color_name(r, g, b)

    st.markdown(f"**Detected Color:** {name}")
    st.markdown(f"**RGB:** ({r}, {g}, {b}) | **HEX:** {hex_code}")
    st.markdown(
        f"<div style='width:100px;height:50px;background-color:{hex_code};'></div>",
        unsafe_allow_html=True
    )
else:
    st.info("Click on the above image to detect the color.")
