import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from onboarding import show_onboarding
from product_catalog import show_product_catalog
from product_detail import show_product_detail
from order_booking import show_order_booking
from order_confirmation import show_order_confirmation

# Configure the page
st.set_page_config(
    page_title="Buying House Portal",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'onboarding'

if 'completed_onboarding' not in st.session_state:
    st.session_state.completed_onboarding = False

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

# Sidebar navigation
with st.sidebar:
    st.title("Buying House Portal")
    st.markdown("---")
    
    # Navigation based on progressive disclosure
    if st.session_state.completed_onboarding:
        if st.button("Browse Products", use_container_width=True):
            st.session_state.page = 'product_catalog'
        
        if st.session_state.selected_product is not None:
            if st.button("Product Details", use_container_width=True):
                st.session_state.page = 'product_detail'
        
        if st.session_state.cart:
            if st.button("View Order", use_container_width=True):
                st.session_state.page = 'order_booking'
                
    # Reset button at the bottom
    st.markdown("---")
    if st.button("Reset Application", use_container_width=True):
        st.session_state.page = 'onboarding'
        st.session_state.completed_onboarding = False
        st.session_state.selected_product = None
        st.session_state.cart = []
        st.session_state.order_submitted = False
        st.rerun()

# Main content area based on the current page
if st.session_state.page == 'onboarding':
    show_onboarding()
elif st.session_state.page == 'product_catalog':
    show_product_catalog()
elif st.session_state.page == 'product_detail':
    show_product_detail()
elif st.session_state.page == 'order_booking':
    show_order_booking()
elif st.session_state.page == 'order_confirmation':
    show_order_confirmation()

# Footer
st.markdown("---")
st.caption("Buying House Portal | Ready Styles. Bulk Orders. Tailored For You.")
