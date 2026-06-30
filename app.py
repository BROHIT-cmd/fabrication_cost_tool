import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("🌍 Fabrication Cost Tool (STEP Enabled)")

# -------------------------
# LOAD MATERIAL DATA
# -------------------------
df = pd.read_csv("material_rates.csv")

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

        except:
            st.error("❌ Cannot connect to STEP server")
            st.stop()

        if "error" in data:
            st.error("❌ STEP processing failed")
            st.stop()

        volume = data["volume"]
        length = data["length"]
        width = data["width"]
        height = data["height"]

        st.success("✅ STEP file processed successfully")

else:
    st.warning("Upload STEP file to continue")
    st.stop()

# -------------------------
# USER INPUTS
# -------------------------
region = st.selectbox("Region", df["Region"].unique())
material = st.selectbox("Material", df["Material"].unique())

# -------------------------
# MATERIAL PROPERTIES
# -------------------------
density = {
    "MS": 7850,
    "SS": 8000,
    "Aluminum": 2700
}

weight = volume * density.get(material, 7850)

# -------------------------
# WELD ESTIMATION
# -------------------------
def estimate_weld(L, W, H):
    L /= 1000
    W /= 1000
    H /= 1000
    return (L + W + H) * 1.5

weld_length = estimate_weld(length, width, height)

# -------------------------
# COST CALCULATION
# -------------------------
row = df[(df["Region"] == region) & (df["Material"] == material)]

rate = float(row["Rate"].values[0])
currency = row["Currency"].values[0]

material_cost = weight * rate
welding_cost = weld_length * 50

total_cost = material_cost + welding_cost

# -------------------------
# OUTPUT
# -------------------------
st.subheader("📊 Results")

st.write(f"Volume: {volume:.6f} m³")
st.write(f"Weight: {weight:.2f} kg")
st.write(f"Weld Length: {weld_length:.2f} m")

st.write(f"Material Cost: {currency} {material_cost:.2f}")
st.write(f"Welding Cost: {currency} {welding_cost:.2f}")

st.success(f"✅ Total Cost: {currency} {total_cost:.2f}")
