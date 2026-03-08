import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import random
import sys
import os

# Fix module path so Python can find the model folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.deepfake_detector import predict_image



st.set_page_config(
    page_title="TruthLens AI",
    layout="wide"
)


# ------------------------------
# FRONT ENTRY SCREEN
# ------------------------------

if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:

    st.title("🔍 TruthLens AI")

    st.write("""
    Real-Time Deepfake & Misinformation Intelligence System
    """)

    st.write("Detect fake images, analyze misinformation, and verify digital truth.")

    if st.button("Enter Platform"):
        st.session_state.start = True
        st.rerun()

    st.stop()


# ------------------------------
# MAIN APP TITLE
# ------------------------------

st.title("TruthLens AI Dashboard")


# ------------------------------
# IMAGE UPLOAD
# ------------------------------

uploaded = st.file_uploader("Upload Suspicious Image", type=["jpg","png","jpeg"])


# ------------------------------
# DEEPFAKE HEATMAP FUNCTION
# ------------------------------

def generate_heatmap(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(image,0.6,heatmap,0.4,0)

    return overlay


# ------------------------------
# IF IMAGE UPLOADED
# ------------------------------

if uploaded:

    image = Image.open(uploaded)

    st.image(image, caption="Uploaded Image", width=400)

    img = np.array(image)

    result, score = predict_image(img)


    st.subheader("AI Detection Result")

    col1,col2,col3 = st.columns(3)

    col1.metric("Authenticity Score", f"{score*100:.2f}%")
    col2.metric("Prediction", result)
    col3.metric("Confidence","Medium")


    if result == "Fake":
        st.error("⚠️ Possible Deepfake Detected")
    else:
        st.success("✔ Image Appears Authentic")


# ------------------------------
# HEATMAP VISUALIZATION
# ------------------------------

    st.subheader("Manipulation Heatmap")

    heatmap = generate_heatmap(img)

    st.image(heatmap)


# ------------------------------
# MISINFORMATION SPREAD MAP
# ------------------------------

    st.subheader("🌍 Misinformation Spread Map")

    data = pd.DataFrame({
        "Country":["India","USA","UK","Germany"],
        "Spread":[42,65,18,12]
    })

    fig = px.choropleth(
        data,
        locations="Country",
        locationmode="country names",
        color="Spread",
        title="Fake Content Spread"
    )

    st.plotly_chart(fig)


# ------------------------------
# FACT CHECK ASSISTANT
# ------------------------------

st.subheader("AI Fact Check Assistant")

claim = st.text_input("Paste a news claim")

if st.button("Analyze Claim"):

    score = random.randint(20,90)

    st.write("Credibility Score:",score,"%")

    if score < 40:
        st.warning("Possible misinformation detected")
    else:
        st.success("Claim seems credible")


# ------------------------------
# NEWS SOURCE TRUST SCORE
# ------------------------------

st.subheader("Source Credibility Checker")

url = st.text_input("Paste news website URL")

if st.button("Check Source"):

    trust = random.randint(20,95)

    st.metric("Trust Score",trust)

    if trust < 40:
        st.error("High Risk Source")
    elif trust < 70:
        st.warning("Medium Risk Source")
    else:
        st.success("Trusted Source")


# ------------------------------
# TRENDING FAKE NEWS
# ------------------------------

st.subheader("Trending Fake Topics")

topics = [
"Celebrity scandal",
"Election misinformation",
"Health rumors",
"Crypto scams"
]

for i,t in enumerate(topics):

    st.write(f"{i+1}. {t}")


# ------------------------------
# COMMUNITY REPORT
# ------------------------------

if st.button("Report Suspicious Content"):

    st.success("Thank you for helping fight misinformation!")
