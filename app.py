import streamlit as st
import pandas as pd

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("material_rates.csv")

st.title("🌍 Fabrication Cost Estimator")

# -------------------------
# USER INPUTS
# -------------------------
regions = df["Region"].unique()
materials = df["Material"].unique()

region = st.selectbox("Select Region", regions)
material = st.selectbox("Select Material", materials)
quantity = st.number_input("Quantity", min_value=1, value=1)

# Geometry
st.subheader("📏 Geometry Input")
length = st.number_input("Length (mm)")
width = st.number_input("Width (mm)")
height = st.number_input("Height (mm)")

# -------------------------
# CALCULATIONS
# -------------------------
density = {
    "MS": 7850,
    "SS": 8000,
    "Aluminum": 2700
}

volume = (length/1000) * (width/1000) * (height/1000)
weight = volume * density.get(material, 7850)

# -------------------------
# WELD ESTIMATION
# -------------------------
def estimate_weld(L, W, H):
    if H < min(L, W) * 0.2:  # sheet metal
        return 2 * (L + W) * 0.6
    elif abs(L - W) < 0.1 * L:  # box
        return 4 * (L + W + H)
    else:  # general
        return (L + W + H) * 1.5

weld_length = estimate_weld(length/1000, width/1000, height/1000)

# -------------------------
# GET MATERIAL RATE
# -------------------------
row = df[(df["Region"] == region) & (df["Material"] == material)]

if len(row) > 0:
    rate = float(row["Rate"].values[0])
    currency = row["Currency"].values[0]
else:
    st.error("Material not available for selected region")
    st.stop()

# -------------------------
# COST CALCULATIONS
# -------------------------
material_cost = weight * rate

# Welding cost (basic)
weld_rate = 50
if region == "USA":
    weld_rate = 10
elif region == "Germany":
    weld_rate = 9

welding_cost = weld_length * weld_rate

total_cost = (material_cost + welding_cost) * quantity

# -------------------------
# OUTPUT
# -------------------------
st.subheader("📊 Cost Summary")

summary = {
    "Material": material,
    "Region": region,
    "Weight (kg)": round(weight, 2),
    "Volume (m3)": round(volume, 4),
    "Weld Length (m)": round(weld_length, 2),
    "Material Cost": round(material_cost, 2),
    "Welding Cost": round(welding_cost, 2),
    "Total Cost": round(total_cost, 2)
}

df_summary = pd.DataFrame(summary.items(), columns=["Parameter", "Value"])

st.table(df_summary)

# -------------------------
# UTILITY SECTION
# -------------------------
st.subheader("🔧 Utility Tools")

# Currency Converter
st.write("### 💱 Currency Converter")
amount = st.number_input("Amount")
rate_conv = st.number_input("Conversion Rate (manual)")
st.write("Converted Value:", amount * rate_conv)

# Weight Converter
st.write("### ⚖ Weight Converter")
