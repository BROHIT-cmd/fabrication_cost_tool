import streamlit as st
import pandas as pd

# ----------------------
# APP TITLE
# ----------------------
st.set_page_config(page_title="Fabrication Cost Tool", layout="wide")
st.title("🌍 Global Fabrication Cost Estimator")

# ----------------------
# LOAD DATA
# ----------------------
df = pd.read_csv("material_rates.csv")

# ----------------------
# INPUT SECTION
# ----------------------
st.sidebar.header("🔧 Input Parameters")

region = st.sidebar.selectbox("Select Region", sorted(df["Region"].unique()))
material = st.sidebar.selectbox("Select Material", sorted(df["Material"].unique()))
quantity = st.sidebar.number_input("Quantity", min_value=1, value=1)

unit_system = st.sidebar.selectbox(
    "Unit System", ["Metric (mm, kg)", "Imperial (inch, lb)"]
)

# ----------------------
# GEOMETRY INPUT
# ----------------------
st.subheader("📏 Geometry")

length = st.number_input("Length", value=100.0)
width = st.number_input("Width", value=50.0)
height = st.number_input("Height", value=10.0)

# ----------------------
# UNIT CONVERSION
# ----------------------
if unit_system == "Imperial (inch, lb)":
    length = length * 25.4
    width = width * 25.4
    height = height * 25.4

# convert to meters
L = length / 1000
W = width / 1000
H = height / 1000

volume = L * W * H

# ----------------------
# MATERIAL PROPERTIES
# ----------------------
density = {
    "MS": 7850,
    "SS": 8000,
    "Aluminum": 2700
}

weight = volume * density.get(material, 7850)

# weight conversion display
if unit_system == "Imperial (inch, lb)":
    weight_display = weight * 2.20462
    weight_unit = "lb"
else:
    weight_display = weight
    weight_unit = "kg"

# ----------------------
# SMART WELD ESTIMATION
# ----------------------
def estimate_weld(L, W, H):
    if H < min(L, W) * 0.2:
        return 2 * (L + W) * 0.6
    elif abs(L - W) < 0.1 * L:
        return 4 * (L + W + H)
    else:
        return (L + W + H) * 1.5

weld_length = estimate_weld(L, W, H)

# ----------------------
# GET RATE
# ----------------------
row = df[(df["Region"] == region) & (df["Material"] == material)]

if row.empty:
    st.error("❌ Material not available for selected region")
    st.stop()

rate = float(row["Rate"].values[0])
currency = row["Currency"].values[0]
last_updated = row["LastUpdated"].values[0]

# ----------------------
# WELD COST RATE
# ----------------------
weld_rate = {
    "India": 50,
    "USA": 10,
    "Germany": 9,
    "UAE": 35
}.get(region, 50)

# ----------------------
# COST CALCULATION
# ----------------------
material_cost = weight * rate
welding_cost = weld_length * weld_rate
total_cost = (material_cost + welding_cost) * quantity

# ----------------------
# OUTPUT
# ----------------------
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

col1.metric("Weight", f"{weight_display:.2f} {weight_unit}")
col2.metric("Volume (m³)", f"{volume:.5f}")
col3.metric("Weld Length (m)", f"{weld_length:.2f}")

st.write(f"Material Cost: **{currency} {material_cost:.2f}**")
st.write(f"Welding Cost: **{currency} {welding_cost:.2f}**")
st.success(f"✅ Total Cost: {currency} {total_cost:.2f}")

# ----------------------
# SUMMARY TABLE
# ----------------------
st.subheader("📋 Summary Table")

data = {
    "Parameter": [
        "Material","Region","Volume (m3)","Weight",
        "Weld Length","Material Cost","Welding Cost","Total Cost"
    ],
    "Value": [
        material, region, round(volume,5),
        f"{weight_display:.2f} {weight_unit}",
        round(weld_length,2),
        round(material_cost,2),
        round(welding_cost,2),
        round(total_cost,2)
    ]
}

df_summary = pd.DataFrame(data)
st.table(df_summary)

# ----------------------
# GLOBAL COST COMPARISON
# ----------------------
st.subheader("🌍 Global Comparison")

compare_data = []
for r in df["Region"].unique():
    row_temp = df[(df["Region"] == r) & (df["Material"] == material)]
    if not row_temp.empty:
        r_rate = float(row_temp["Rate"].values[0])
        r_currency = row_temp["Currency"].values[0]
        cost = weight * r_rate
        compare_data.append([r, f"{r_currency} {cost:.2f}"])

compare_df = pd.DataFrame(compare_data, columns=["Region","Material Cost"])
st.dataframe(compare_df)

# ----------------------
# UTILITY TOOLS
# ----------------------
st.subheader("🔧 Utility Tools")

# Currency converter (manual)
st.write("### 💱 Currency Converter")
amt = st.number_input("Enter Amount")
conv = st.number_input("Conversion Rate")
st.write("Converted:", amt * conv)

# Weight converter
st.write("### ⚖ Weight Converter")
kg = st.number_input("kg", key="kg")
st.write("lb:", kg * 2.20462)

# Volume converter
st.write("### 📦 Volume Converter")
m3 = st.number_input("m3", key="m3")
st.write("liters:", m3 * 1000)

# ----------------------
# TRUST INFO
# ----------------------
st.caption(f"Last Updated: {last_updated}")
st.caption("Source: Internal + Engineering Estimation")
