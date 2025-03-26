import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from onboarding import show_onboarding
from stock_analysis import show_stock_analysis
from visualization import show_visualization

# Configure the page
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'onboarding'

if 'completed_onboarding' not in st.session_state:
    st.session_state.completed_onboarding = False

if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None

if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None

# Sidebar navigation
with st.sidebar:
    st.title("Stock Analysis Tool")
    st.markdown("---")
    
    # Navigation based on progressive disclosure
    if st.session_state.completed_onboarding:
        if st.button("Search Stocks", use_container_width=True):
            st.session_state.page = 'stock_analysis'
        
        if st.session_state.selected_stock is not None:
            if st.button("Visualization", use_container_width=True):
                st.session_state.page = 'visualization'
                
    # Reset button at the bottom
    st.markdown("---")
    if st.button("Reset Application", use_container_width=True):
        st.session_state.page = 'onboarding'
        st.session_state.completed_onboarding = False
        st.session_state.selected_stock = None
        st.session_state.stock_data = None
        st.rerun()

# Main content area based on the current page
if st.session_state.page == 'onboarding':
    show_onboarding()
elif st.session_state.page == 'stock_analysis':
    show_stock_analysis()
elif st.session_state.page == 'visualization':
    show_visualization()

# Footer
st.markdown("---")
st.caption("Stock Analysis Tool | Data provided by Yahoo Finance")
