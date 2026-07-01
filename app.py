import streamlit as st
import pandas as pd
import subprocess

st.title("Simple STEP Cost Tool")

# ------------------------
# Upload STEP file
# ------------------------
uploaded_file = st.file_uploader("Upload STEP file", type=["step", "stp"])

if uploaded_file:

    # Save file
    with open("temp.step", "wb") as f:
        f.write(uploaded_file.read())

    # Process STEP
    if st.button("Calculate"):

        result = subprocess.run(
            [
                r"C:\Program Files\FreeCAD 0.21\bin\FreeCADCmd.exe",
                "step_reader_simple.py",
                "temp.step"
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        volume, length, width, height = map(float, output.split(","))

        volume = volume / 1e9  # convert mm³ to m³

        # ------------------------
        # User Inputs
        # ------------------------
        material = st.selectbox("Material", ["MS", "SS", "Aluminum"])
        region = st.selectbox("Region", ["India", "USA"])

        density = {"MS": 7850, "SS": 8000, "Aluminum": 2700}
        rate = {"India": 70, "USA": 1.2}

        weight = volume * density[material]

        material_cost = weight * rate[region]
        welding_cost = (length + width + height)/1000 * 50
        total_cost = material_cost + welding_cost

        # ------------------------
        # Output
        # ------------------------
        st.success("STEP processed")

        st.write("Volume (m3):", round(volume, 6))
        st.write("Weight (kg):", round(weight, 2))
        st.write("Total Cost:", total_cost)
