import streamlit as st
import tempfile
from step_utils import calculate_volume

st.set_page_config(page_title="STEP Volume Calculator")

st.title("📦 STEP File Volume Calculator")

uploaded_file = st.file_uploader(
    "Upload STEP file",
    type=["step", "stp"]
)

if uploaded_file is not None:
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        volume = calculate_volume(temp_path)

        st.success("✅ Volume calculated successfully!")
        st.write(f"### Volume: {volume:.2f} cubic units")

        # Unit conversion
        st.write("#### Convert to:")
        st.write(f"- cm³: {volume/1000:.2f}")
        st.write(f"- liters: {volume/1e6:.4f}")
        st.write(f"- m³: {volume/1e9:.6f}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
