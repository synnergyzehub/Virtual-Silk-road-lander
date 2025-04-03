import streamlit as st

st.title("Test Streamlit App")
st.write("Testing basic Streamlit functionality without any other dependencies")

# Test basic UI elements
st.header("UI Test")
st.button("Test Button")
st.checkbox("Test Checkbox")
st.radio("Test Radio", options=["Option 1", "Option 2"])
st.selectbox("Test Selectbox", options=["Choice 1", "Choice 2"])
st.text_input("Test Text Input")
st.text_area("Test Text Area")
st.slider("Test Slider", 0, 100, 50)