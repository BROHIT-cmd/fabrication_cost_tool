import streamlit as st
import tempfile
from step_utils import calculate_volume

st.set_page_config(page_title="STEP Volume Calculator")

st.title("📦 STEP File Volume Calculator")

st.write("Upload a STEP (.step / .stp) file to calculate volume.")

uploaded_file = st.file_uploader(
    "Upload STEP file",
    type=["step", "stp"]
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        with st.spinner("Calculating volume..."):
            volume = calculate_volume(temp_path)

        st.success("✅ Volume calculated successfully!")

        # Display main result
        st.subheader("📊 Results")
        st.write(f"**Volume:** {volume:.2f} mm³")

        # Conversions
        st.subheader("🔄 Unit Conversion")
        st.write(f"- cm³: {volume / 1000:.2f}")
        st.write(f"- liters: {volume / 1e6:.6f}")
        st.write(f"- m³: {volume / 1e9:.9f}")

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
