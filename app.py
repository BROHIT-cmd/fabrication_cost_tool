import streamlit as st
import subprocess

st.title("Simple STEP Cost Tool")

# Upload STEP file
file = st.file_uploader("Upload STEP file", type=["step","stp"])

if file:
    # Save file locally
    with open("temp.step", "wb") as f:
        f.write(file.read())

    if st.button("Calculate Cost"):

        # Run FreeCAD command
        result = subprocess.run(
            [
                r"C:\Users\BROHIT\FreeCAD.exe",
                "-c",
                """
import Part
shape=Part.Shape()
shape.read('temp.step')
v=shape.Volume
bb=shape.BoundBox
print(str(v)+","+str(bb.XLength)+","+str(bb.YLength)+","+str(bb.ZLength))
"""
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if output == "":
            st.error("STEP read failed")
        else:
            volume, L, W, H = map(float, output.split(","))

            volume = volume / 1e9  # mm³ → m³

            # Simple inputs
            material = st.selectbox("Material", ["MS","SS","Aluminum"])
            region = st.selectbox("Region", ["India","USA"])

            density = {"MS":7850,"SS":8000,"Aluminum":2700}
            rate = {"India":70,"USA":1.2}

            weight = volume * density[material]

            # Simple weld estimate
            weld = (L + W + H)/1000

            material_cost = weight * rate[region]
            welding_cost = weld * 50
            total_cost = material_cost + welding_cost

            # Output
            st.success("✅ Done")

            st.write("Volume (m3):", round(volume,6))
            st.write("Weight (kg):", round(weight,2))
            st.write("Total Cost:", round(total_cost,2))
