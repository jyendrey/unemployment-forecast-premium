import streamlit as st

st.title("🎯 Test - Interactive Brokers Dashboard")
st.write("If you can see this, Streamlit is working!")
st.success("✅ App is running successfully")

# Simple metric
col1, col2 = st.columns(2)
with col1:
    st.metric("Current Unemployment", "4.2%", "0.1%")
with col2:
    st.metric("Model Confidence", "98.3%", "Target Achieved")

st.balloons()
