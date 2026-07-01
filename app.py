import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("🌍 Fabrication Cost Tool (STEP Enabled)")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("material_rates.csv")

# -------------------------
# INIT SESSION STATE ✅ (IMPORTANT FIX)
# -------------------------
if "volume" not in st.session_state:
    st.session_state.volume = None
    st.session_state.length = None
    st.session_state.width = None
    st.session_state.height = None

# -------------------------
# STEP FILE UPLOAD
# -------------------------
st.subheader("📂 Upload STEP File")

uploaded_file = st.file_uploader("Upload STEP file", type=["step", "stp"])

if uploaded_file is not None:

    if st.button("Process STEP File"):

        SERVER_URL = "http://127.0.0.1:5000/process_step"

        try:
            response = requests.post(
                SERVER_URL,
                files={"file": uploaded_file.getvalue()}
            )

            data = response.json()

            if "error" in data:
                st.error("❌ STEP processing failed")
                st.stop()

            # ✅ STORE IN SESSION STATE
            st.session_state.volume = data["volume"]
            st.session_state.length = data["length"]
            st.session_state.width = data["width"]
            st.session_state.height = data["height"]

            st.success("✅ STEP file processed successfully")

        except:
            st.error("❌ Cannot connect to STEP server")
            st.stop()

# -------------------------
# USER INPUTS
# -------------------------
region = st.selectbox("Region", df["Region"].unique())
material = st.selectbox("Material", df["Material"].unique())

# -------------------------
# USE STORED DATA ✅
# -------------------------
volume = st.session_state.volume
length = st.session_state.length
width = st.session_state.width
height = st.session_state.height

# -------------------------
# CALCULATIONS ✅ SAFE
# -------------------------
if volume is not None:

    density = {
        "MS": 7850,
        "SS": 8000,
        "Aluminum": 2700
    }

    weight = volume * density.get(material, 7850)

    def estimate_weld(L, W, H):
