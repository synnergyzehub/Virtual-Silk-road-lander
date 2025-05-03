import streamlit as st

st.title("Test Streamlit App")
st.write("This is a simple test app to verify that Streamlit is working properly.")

st.header("Sample Data Display")
import pandas as pd
import numpy as np

# Create a sample dataframe
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': np.random.randint(1, 100, 5)
})

st.dataframe(data)

st.header("Interactive Elements")
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")

st.button("Click Me!")