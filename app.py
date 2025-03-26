import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from onboarding import show_onboarding
from product_catalog import show_product_catalog
from product_detail import show_product_detail
from order_booking import show_order_booking
from order_confirmation import show_order_confirmation
from merchandiser_agent import show_merchandiser_agent
from retailer_analysis import show_retailer_analysis

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
        # Main navigation items with icons for better UI
        st.markdown("### Main Navigation")
        
        if st.button("🛍️ Browse Products", use_container_width=True):
            st.session_state.page = 'product_catalog'
        
        if st.session_state.selected_product is not None:
            if st.button("📋 Product Details", use_container_width=True):
                st.session_state.page = 'product_detail'
        
        if st.session_state.cart:
            if st.button("🛒 View Order", use_container_width=True):
                st.session_state.page = 'order_booking'
        
        # Market Intelligence Section
        st.markdown("### Market Intelligence")
        
        # Add JC Penney analysis button
        if st.button("📊 Retailer Analysis", use_container_width=True):
            st.session_state.page = 'retailer_analysis'
        
        # Add a hint about JC Penney analysis
        st.info("Access market data on JC Penney and other major retailers to inform your buying decisions.")
        
        # Add access to the merchandiser agent
        st.markdown("### Your Support Team")
        
        # Merchandiser button with notification badge style
        if st.button("👩‍💼 Your Merchandiser Agent", use_container_width=True):
            st.session_state.page = 'merchandiser_agent'
        
        # Show a hint about the merchandiser
        if 'merchandiser' in st.session_state:
            # Display merchandiser info if already assigned
            st.markdown(f"""
            <div style='background-color: #1E3A8A; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                <p style='margin: 0; font-size: 0.9em;'>You're working with:</p>
                <p style='margin: 0; font-weight: bold;'>{st.session_state.merchandiser['name']}</p>
                <p style='margin: 0; font-size: 0.8em;'>{st.session_state.merchandiser['specialization']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show a teaser about having a merchandiser
            st.info("Connect with your dedicated merchandising agent for personalized support throughout your order process.")
                
    # Additional resources
    st.markdown("### Resources")
    resources_expander = st.expander("Helpful Resources")
    with resources_expander:
        st.markdown("- [Fabric Guide]()")
        st.markdown("- [Size Charts]()")
        st.markdown("- [Customization Options]()")
        st.markdown("- [Production Process]()")
                
    # Reset button at the bottom
    st.markdown("---")
    if st.button("🔄 Reset Application", use_container_width=True):
        st.session_state.page = 'onboarding'
        st.session_state.completed_onboarding = False
        st.session_state.selected_product = None
        st.session_state.cart = []
        st.session_state.order_submitted = False
        # Also reset merchandiser
        if 'merchandiser' in st.session_state:
            del st.session_state.merchandiser
        if 'conversation' in st.session_state:
            del st.session_state.conversation
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
elif st.session_state.page == 'merchandiser_agent':
    show_merchandiser_agent()
elif st.session_state.page == 'retailer_analysis':
    show_retailer_analysis()

# Footer
st.markdown("---")
st.caption("Buying House Portal | Ready Styles. Bulk Orders. Tailored For You.")
