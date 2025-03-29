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

# Import manufacturing portal modules
from manufacturing_dashboard import show_manufacturing_dashboard
from order_style_management import show_order_style_management
from material_tracker import show_material_tracker
from production_timeline import show_production_timeline
from line_plan import show_line_plan
from reports import show_reports
from init_db import show_db_initialization, initialize_database

# Configure the page
st.set_page_config(
    page_title="ECG Manufacturing Portal",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database with sample data if needed
if 'db_initialized' not in st.session_state:
    # Try to initialize database
    initialize_database()
    st.session_state.db_initialized = True

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'manufacturing_dashboard'  # Start directly on manufacturing dashboard page

if 'completed_onboarding' not in st.session_state:
    st.session_state.completed_onboarding = True  # Skip onboarding for testing

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

# Sidebar navigation
with st.sidebar:
    st.title("ECG Management Portal")
    st.markdown("---")
    
    # Create two sections for navigation
    tab1, tab2 = st.tabs(["🏭 Manufacturing", "👕 Buying House"])
    
    with tab1:
        # Manufacturing Portal Navigation
        st.markdown("### Manufacturing Portal")
        
        if st.button("🏭 Dashboard Overview", use_container_width=True, key="mfg_dashboard"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("📋 Order & Style Management", use_container_width=True, key="order_style_mgmt"):
            st.session_state.page = 'order_style_management'
        
        if st.button("🧶 Material Tracker", use_container_width=True, key="material_tracker"):
            st.session_state.page = 'material_tracker'
        
        if st.button("⏱ Production Timeline", use_container_width=True, key="production_timeline"):
            st.session_state.page = 'production_timeline'
        
        if st.button("📅 Line Plan Interface", use_container_width=True, key="line_plan"):
            st.session_state.page = 'line_plan'
        
        if st.button("📊 Reports & Export", use_container_width=True, key="reports"):
            st.session_state.page = 'reports'
        
        # Database initialization (hidden in an expander to not clutter the UI)
        with st.expander("⚙️ Database Management"):
            if st.button("Database Setup", use_container_width=True, key="db_init"):
                st.session_state.page = 'db_initialization'
    
    with tab2:
        # Buying House Portal Navigation
        st.markdown("### Buying House Portal")
        
        # Main navigation items with icons for better UI
        if st.button("🛍️ Browse Products", use_container_width=True, key="browse_products"):
            st.session_state.page = 'product_catalog'
        
        if st.session_state.selected_product is not None:
            if st.button("📋 Product Details", use_container_width=True, key="product_details"):
                st.session_state.page = 'product_detail'
        
        if st.session_state.cart:
            if st.button("🛒 View Order", use_container_width=True, key="view_order"):
                st.session_state.page = 'order_booking'
        
        # Market Intelligence Section
        st.markdown("### Market Intelligence")
        
        # Add ECG Market Health Check button
        if st.button("📊 ECG Market Health Check", use_container_width=True, key="market_health"):
            st.session_state.page = 'retailer_analysis'
        
        # Add a hint about the ECG Market Health Check
        st.info("Access ECG's proprietary market health analysis on major retailers to inform your strategic decisions.")
        
        # Add access to the merchandiser agent
        st.markdown("### Your Support Team")
        
        # Merchandiser button with notification badge style
        if st.button("👩‍💼 Your Merchandiser Agent", use_container_width=True, key="merchandiser"):
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
        st.markdown("- [Manufacturing Handbook]()")
                
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
# Manufacturing portal pages
elif st.session_state.page == 'manufacturing_dashboard':
    show_manufacturing_dashboard()
elif st.session_state.page == 'order_style_management':
    show_order_style_management()
elif st.session_state.page == 'material_tracker':
    show_material_tracker()
elif st.session_state.page == 'production_timeline':
    show_production_timeline()
elif st.session_state.page == 'line_plan':
    show_line_plan()
elif st.session_state.page == 'reports':
    show_reports()
elif st.session_state.page == 'db_initialization':
    show_db_initialization()

# Footer
st.markdown("---")
st.caption("ECG Management Portal | Streamlined Manufacturing. Tailored Solutions. Global Excellence.")
