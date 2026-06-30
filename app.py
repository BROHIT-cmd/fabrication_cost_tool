import streamlit as st
import pandas as pd
import cadquery as cq
from cadquery import importers

st.set_page_config(layout="wide")
st.title("🌍 STEP-Based Fabrication Cost Estimator")

# -------------------------
# LOAD MATERIAL DATA
# -------------------------
df = pd.read_csv("material_rates.csv")

# -------------------------
# UPLOAD STEP FILE
# -------------------------
st.subheader("📂 Upload STEP File")

uploaded_file = st.file_uploader("Upload STEP file", type=["step", "stp"])

if uploaded_file:

    with open("temp.step", "wb") as f:
        f.write(uploaded_file.read())

    try:
        shape = importers.importStep("temp.step")

        # Get solids
        solids = shape.solids()

        # Volume in mm³
        volume_mm3 = sum([s.Volume() for s in solids])

        # Bounding box
        bbox = shape.val().BoundingBox()

        length = bbox.xlen
        width = bbox.ylen
        height = bbox.zlen

        # Convert
        volume_m3 = volume_mm3 / 1e9

        st.success("✅ STEP file read successfully")

    except:
        st.error("❌ Error reading STEP file")
        st.stop()

else:
    st.warning("Upload STEP file to continue")
    st.stop()

# -------------------------
# USER INPUTS
# -------------------------
regions = df["Region"].unique()
materials = df["Material"].unique()

region = st.selectbox("Region", regions)
material = st.selectbox("Material", materials)
quantity = st.number_input("Quantity", 1)

# -------------------------
# MATERIAL PROPERTIES
# -------------------------
density = {
    "MS": 7850,
    "SS": 8000,
    "Aluminum": 2700
}

weight = volume_m3 * density.get(material, 7850)

# -------------------------
# SMART WELD ESTIMATION
# -------------------------
def estimate_weld(L, W, H):
    L = L / 1000
    W = W / 1000
    H = H / 1000

    if H < min(L, W) * 0.2:
        return 2 * (L + W) * 0.6
    elif abs(L - W) < 0.1 * L:
        return 4 * (L + W + H)
    else:
        return (L + W + H) * 1.5

weld_length = estimate_weld(length, width, height)

# -------------------------
# GET RATE
# -------------------------
row = df[(df["Region"] == region) & (df["Material"] == material)]

if row.empty:
    st.error("Material not available")
    st.stop()

rate = float(row["Rate"].values[0])
currency = row["Currency"].values[0]

# -------------------------
# COST CALCULATION
# -------------------------
material_cost = weight * rate

weld_rate = {
    "India": 50,
    "USA": 10,
    "Germany": 9
}.get(region, 50)

welding_cost = weld_length * weld_rate

total_cost = (material_cost + welding_cost) * quantity

# -------------------------
# OUTPUT RESULTS
# -------------------------
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

col1.metric("Weight (kg)", f"{weight:.2f}")
col2.metric("Volume (m³)", f"{volume_m3:.6f}")
col3.metric("Weld Length (m)", f"{weld_length:.2f}")

st.write(f"Material Cost: {currency} {material_cost:.2f}")
st.write(f"Welding Cost: {currency} {welding_cost:.2f}")

st.success(f"✅ Total Cost: {currency} {total_cost:.2f}")

# -------------------------
# SUMMARY TABLE
# -------------------------
data = {
    "Parameter": [
        "Material", "Region", "Volume", "Weight",
        "Weld Length", "Material Cost", "Welding Cost", "Total Cost"
    ],
    "Value": [
        material, region,
        round(volume_m3, 6),
        round(weight, 2),
        round(weld_length, 2),
        round(material_cost, 2),
        round(welding_cost, 2),
        round(total_cost, 2)
    ]
}

st.subheader("📋 Summary")
st.table(pd.DataFrame(data))

# -------------------------
# DEBUG INFO (Optional)
# -------------------------
st.subheader("📦 Geometry Info")
st.write(f"Length: {length:.2f} mm")
st.write(f"Width: {width:.2f} mm")
st.write(f"Height: {height:.2f} mm")
