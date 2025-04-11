
import streamlit as st
import pandas as pd

# Sample data for visualization
licenses = [
    {
        "License ID": "VOI-GENESIS-001",
        "Brand": "VOI JEANS INDIA",
        "Role": "Retailer",
        "Realm": "Commerce",
        "Scope Tags": "denim, fashion, sustainable, export, India",
        "DAL Aligned Tags": "sustainable",
        "Empowerment Score": 82.4,
        "Quests Completed": "1/4",
        "Silk Road Node": "Southern River Entry"
    }
]

st.set_page_config(page_title="Genesis License Viewer", layout="wide")

st.title("Genesis Stack: Brand License Table")

df = pd.DataFrame(licenses)

st.dataframe(df, use_container_width=True)
