import streamlit as st
import pandas as pd
import cadquery as cq
from cadquery import importers
from datetime import datetime

st.title("🌍 AI Fabrication Cost Estimator (STEP Enabled)")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("material_rates.csv")

# -------------------------
# STEP FILE UPLOAD
# -------------------------
st.subheader("📂 Upload STEP File")

uploaded_file = st.file_uploader("Upload STEP (.step/.stp)", type=["step", "stp"])

volume = 0
bounding_dims = (0, 0, 0)

if uploaded_file:
    with open("temp.step", "wb") as f:
        f.write(uploaded_file.read())

    try:
        shape = importers.importStep("temp.step")

        # Volume
        solids = shape.solids()
        volume = sum([s.Volume() for s in solids])  # mm³

        # Bounding box
        bbox = shape.val().BoundingBox()
        lx = bbox.xlen
        ly = bbox.ylen
        lz = bbox.zlen

        bounding_dims = (lx, ly, lz)

        st.success("✅ STEP File Processed Successfully")

    except Exception as e:
        st.error("Error reading STEP file")
        st.stop()

# -------------------------
# USER INPUTS
# -------------------------
regions = df["Region"].unique()
materials = df["Material"].unique()

region = st.selectbox("Region", regions)
material = st.selectbox("Material", materials)
quantity = st.number_input("Quantity", value=1)

# -------------------------
# MATERIAL PROPERTIES
# -------------------------
density = {
    "MS": 7850,
    "SS": 8000,
    "Aluminum": 2700
}

# -------------------------
# GEOMETRY CALCULATION
# -------------------------
if volume > 0:
    volume_m3 = volume / 1e9  # convert mm³ → m³
    weight = volume_m3 * density.get(material, 7850)

    length, width, height = bounding_dims

else:
    st.warning("Upload STEP file to calculate geometry")
    st.stop()

# -------------------------
# WELD ESTIMATION
# -------------------------
def estimate_weld(L, W, H):
    L /= 1000
    W /= 1000
    H /= 1000

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

if len(row) == 0:
    st.error("Material not available in selected region")
    st.stop()

rate = float(row["Rate"].values[0])
currency = row["Currency"].values[0]

# -------------------------
# COST CALCULATION
# -------------------------
material_cost = weight * rate

# Welding rates (region-based rough)
weld_rate_map = {
    "India": 50,
    "USA": 10,
    "Germany": 9
}

weld_rate = weld_rate_map.get(region, 50)

welding_cost = weld_length * weld_rate

total_cost = (material_cost + welding_cost) * quantity

# -------------------------
# OUTPUT
# -------------------------
st.subheader("📊 Results")

st.write(f"Volume: {volume_m3:.6f} m³")
st.write(f"Weight: {weight:.2f} kg")
st.write(f"Bounding Box: {length:.1f} × {width:.1f} × {height:.1f} mm")

st.write(f"Material Cost: {currency} {material_cost:.2f}")
st.write(f"Welding Cost: {currency} {welding_cost:.2f}")
st.write(f"✅ Total Cost: {currency} {total_cost:.2f}")

# -------------------------
# SUMMARY TABLE
# -------------------------
data = {
    "Material": material,
    "Region": region,
    "Weight (kg)": round(weight, 2),
    "Volume (m3)": round(volume_m3, 6),
    "Weld Length (m)": round(weld_length, 2),
    "Material Cost": round(material_cost, 2),
    "Welding Cost": round(welding_cost, 2),
    "Total Cost": round(total_cost, 2)
}

df_summary = pd.DataFrame(data.items(), columns=["Parameter", "Value"])

st.subheader("📋 Summary Table")
st.table(df_summary)

# -------------------------
# CONVERTERS
# -------------------------
st.subheader("🔧 Utility")

# Weight converter
kg = st.number_input("Weight kg")
st.write("In lb:", kg * 2.20462)

# Volume converter
v = st.number_input("Volume m3")
st.write("Liters:", v * 1000)

# -------------------------
# TRUST DATA
# -------------------------
st.write("Last Updated:", datetime.now().strftime("%Y-%m-%d"))
st.write("Source: Internal + Engineering Estimation")
