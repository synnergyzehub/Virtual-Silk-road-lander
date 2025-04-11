
import streamlit as st
import pandas as pd

# Sample license dataset
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
    },
    {
        "License ID": "KLSH-FACTORY-002",
        "Brand": "KAILASH TEXTILES",
        "Role": "Manufacturer",
        "Realm": "Supply_Chain",
        "Scope Tags": "tailoring, domestic, offline, vendor",
        "DAL Aligned Tags": "",
        "Empowerment Score": 58.9,
        "Quests Completed": "0/3",
        "Silk Road Node": "Northern Fabric Gate"
    }
]

st.set_page_config(page_title="Genesis License Viewer", layout="wide")

st.title("Genesis Stack: Brand License Table")

df = pd.DataFrame(licenses)

# Sidebar Filters
st.sidebar.header("Filter Licenses")
realm_filter = st.sidebar.multiselect("Realm", options=df["Realm"].unique(), default=list(df["Realm"].unique()))
score_threshold = st.sidebar.slider("Min Empowerment Score", min_value=0, max_value=100, value=60)
quest_filter = st.sidebar.checkbox("Only show licenses with incomplete quests")
search_text = st.sidebar.text_input("Search Brand or License ID")

# Filter Logic
filtered_df = df[df["Realm"].isin(realm_filter)]
filtered_df = filtered_df[filtered_df["Empowerment Score"] >= score_threshold]

if quest_filter:
    filtered_df = filtered_df[~filtered_df["Quests Completed"].str.startswith("1")]

if search_text:
    filtered_df = filtered_df[
        filtered_df["Brand"].str.contains(search_text, case=False) |
        filtered_df["License ID"].str.contains(search_text, case=False)
    ]

# Display the result
st.dataframe(filtered_df, use_container_width=True)
