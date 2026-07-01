import streamlit as st
import tempfile

# import cadquery inside function (avoids startup crash)
def calculate_volume(file_path):
    import cadquery as cq
    shape = cq.importers.importStep(file_path)
    
    volume = 0
    for solid in shape.solids().vals():
        volume += solid.Volume()
        
    return volume

st.title("STEP Volume Calculator")

uploaded_file = st.file_uploader("Upload STEP file", type=["step", "stp"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        volume = calculate_volume(temp_path)

        st.success("✅ Done")
        st.write(f"Volume (mm³): {volume:.2f}")
        st.write(f"cm³: {volume/1000:.2f}")
        st.write(f"Liters: {volume/1e6:.4f}")

    except Exception as e:
        st.error(f"Error: {e}")
