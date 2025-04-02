import streamlit as st
import pandas as pd
import numpy as np

# Simplest possible app to check if Streamlit is working
st.set_page_config(
    page_title="Streamlit Test",
    page_icon="🧪",
    layout="wide"
)

# Header
st.title("Streamlit Test App")
st.write("This is a simple app to test if Streamlit is working properly.")

# Simple interactive elements
st.header("Basic Interactive Elements")

# Simple text input
name = st.text_input("Enter your name", "")
if name:
    st.write(f"Hello, {name}!")

# Simple slider
number = st.slider("Select a number", 0, 100, 50)
st.write(f"Selected number: {number}")

# Simple dataframe
st.header("Sample Data")
data = pd.DataFrame({
    "Column 1": list(range(5)),
    "Column 2": [n*2 for n in range(5)],
    "Column 3": [n*n for n in range(5)]
})
st.dataframe(data)

# Simple chart
st.header("Sample Chart")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# Footer
st.markdown("---")
st.caption("Simple Streamlit Test App | Created for testing purposes")

# Print a message to console for debugging
print("Streamlit app is running!")