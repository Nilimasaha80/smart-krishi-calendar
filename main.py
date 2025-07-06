import streamlit as st
from agent import get_calendar_plan

st.title("🌾 Smart Krishi Calendar")

location = st.text_input("📍 Enter your location (e.g., Etawah)")
soil_type = st.selectbox("🧪 Choose your soil type", ["Sandy", "Loamy", "Clayey"])
crop = st.text_input("🌱 Which crop do you want to grow?")

if st.button("Generate Calendar Plan"):
    with st.spinner("Thinking..."):
        response = get_calendar_plan(location, soil_type, crop)
        st.success("✅ Here's your AI-assisted farming plan:")
        st.markdown(response)
