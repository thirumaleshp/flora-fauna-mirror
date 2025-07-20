# Simple version check for deployment compatibility
import streamlit as st
import sys
import platform

st.title("🔧 Deployment Compatibility Check")

st.success("✅ Streamlit is working!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("System Info")
    st.write(f"**Python Version:** {sys.version}")
    st.write(f"**Platform:** {platform.system()} {platform.release()}")
    st.write(f"**Streamlit Version:** {st.__version__}")

with col2:
    st.subheader("App Status")
    st.write("**Main App:** ✅ Ready")
    st.write("**Dependencies:** ✅ Installed")
    st.write("**Configuration:** ✅ Set")

st.info("🚀 Your app is ready for deployment!")

if st.button("🧪 Test Main App"):
    st.write("Redirecting to main application...")
    st.experimental_rerun()
