import streamlit as st
import pandas as pd

# Try STEP library (optional)
try:
    import cadquery as cq
    from cadquery import importers
    STEP_AVAILABLE = True
except:
    STEP_AVAILABLE = False

st.title("🌍 Fabrication Cost Tool")

df = pd.read_csv("material_rates.csv")

# -------------------------
# STEP MODE or MANUAL MODE
# -------------------------
mode = st.radio("Select Mode", ["Manual Input", "STEP File"])

if mode == "STEP File":

    if not STEP_AVAILABLE:
        st.error("STEP processing not available. Use local setup with Python 3.10")
        st.stop()

    file = st.file_uploader("Upload STEP", type=["step","stp"])

    if file:
        with open("temp.step","wb") as f:
            f.write(file.read())

        shape = importers.importStep("temp.step")

        volume = sum([s.Volume() for s in shape.solids()])
        bbox = shape.val().BoundingBox()

        length, width, height = bbox.xlen, bbox.ylen, bbox.zlen

        volume = volume / 1e9

    else:
        st.stop()

else:
    length = st.number_input("Length (mm)")
    width = st.number_input("Width (mm)")
    height = st.number_input("Height (mm)")

    volume = (length/1000)*(width/1000)*(height/1000)

# -------------------------
# MATERIAL
# -------------------------
region = st.selectbox("Region", df["Region"].unique())
material = st.selectbox("Material", df["Material"].unique())

density = {"MS":7850,"SS":8000,"Aluminum":2700}

weight = volume * density.get(material,7850)

# -------------------------
# WELD ESTIMATION
# -------------------------
def estimate_weld(L,W,H):
    L/=1000; W/=1000; H/=1000
    return (L+W+H)*1.5

weld_length = estimate_weld(length,width,height)

# -------------------------
# COST
# -------------------------
row = df[(df["Region"]==region)&(df["Material"]==material)]

rate = float(row["Rate"].values[0])
currency = row["Currency"].values[0]

material_cost = weight * rate
welding_cost = weld_length * 50

total = material_cost + welding_cost

# -------------------------
# OUTPUT
# -------------------------
st.write("Weight:", round(weight,2),"kg")
st.write("Volume:", round(volume,5),"m3")
st.write("Weld Length:", round(weld_length,2))

st.write("Material Cost:", currency, round(material_cost,2))
st.write("Welding Cost:", currency, round(welding_cost,2))

st.success(f"Total Cost: {currency} {round(total,2)}")
