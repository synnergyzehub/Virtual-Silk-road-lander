import streamlit as st

# Basic app for testing
st.title("Empire OS Dashboard - Testing")
st.markdown("This is a simplified version for testing the Streamlit server.")

# Display a simple visualization
st.write("## Sample Data")
import pandas as pd
import numpy as np

# Create some sample data
data = pd.DataFrame({
    'Category': ['Layer 1', 'Layer 2', 'Layer 3', 'Layer 4'],
    'Value': [10, 20, 15, 25]
})

# Display the data
st.dataframe(data)

# Create a simple chart
st.bar_chart(data.set_index('Category'))

# Information message
st.info("This is a testing environment to diagnose Streamlit server issues.")