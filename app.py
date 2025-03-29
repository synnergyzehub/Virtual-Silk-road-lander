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
    tab1, tab2, tab3 = st.tabs(["🏭 Woven Supply", "🛒 Commune Connect", "🔑 Synergyze Hub"])
    
    with tab1:
        # Woven Supply Portal Navigation
        st.markdown("### Woven Supply (Factory/Vendor Network)")
        
        # Procurement System section
        st.markdown("#### Procurement System")
        if st.button("🔍 Raw Material Sourcing", use_container_width=True, key="material_tracker"):
            st.session_state.page = 'material_tracker'
            
        if st.button("👨‍💼 Vendor Management Dashboard", use_container_width=True, key="order_style_mgmt"):
            st.session_state.page = 'order_style_management'
            
        if st.button("💰 Price Negotiation Interface", use_container_width=True, key="reports"):
            st.session_state.page = 'reports'
            
        if st.button("📝 Order Placement Workflow", use_container_width=True, key="order_placement"):
            st.session_state.page = 'order_style_management'
            
        if st.button("📦 Material Tracking", use_container_width=True, key="material_tracking"):
            st.session_state.page = 'material_tracker'
            
        # Manufacturing Management section
        st.markdown("#### Manufacturing Management")
        if st.button("📋 Production Planning", use_container_width=True, key="line_plan"):
            st.session_state.page = 'line_plan'
            
        if st.button("📅 Production Scheduling", use_container_width=True, key="production_timeline"):
            st.session_state.page = 'production_timeline'
            
        if st.button("⚙️ Quality Control Tracking", use_container_width=True, key="quality_control"):
            st.session_state.page = 'production_timeline'
            
        if st.button("📊 Capacity Management", use_container_width=True, key="capacity_mgmt"):
            st.session_state.page = 'manufacturing_dashboard'
            
        if st.button("📈 Production Reporting", use_container_width=True, key="prod_reporting"):
            st.session_state.page = 'reports'
            
        # Fabric and Vendor Synchronization section
        st.markdown("#### Fabric and Vendor Synchronization")
        if st.button("📚 Material Library", use_container_width=True, key="material_library"):
            st.session_state.page = 'material_tracker'
            
        if st.button("📊 Vendor Capability Matrix", use_container_width=True, key="vendor_capability"):
            st.session_state.page = 'reports'
            
        if st.button("🔄 Material-vendor Matching", use_container_width=True, key="material_vendor_matching"):
            st.session_state.page = 'order_style_management'
            
        if st.button("📈 Performance Tracking", use_container_width=True, key="vendor_performance"):
            st.session_state.page = 'manufacturing_dashboard'
            
        # Factory Operations Dashboard section
        st.markdown("#### Factory Operations Dashboard")
        if st.button("👚 Factory Merchandiser View", use_container_width=True, key="factory_merchandiser"):
            st.session_state.page = 'merchandiser_agent'
            
        if st.button("⏱ Production Tracking Timeline", use_container_width=True, key="prod_tracking_timeline"):
            st.session_state.page = 'production_timeline'
            
        if st.button("🚚 Delivery Scheduling", use_container_width=True, key="delivery_scheduling"):
            st.session_state.page = 'line_plan'
            
        if st.button("📋 Compliance Tracking", use_container_width=True, key="compliance_tracking"):
            st.session_state.page = 'reports'
            
        # HSN-Based Forecasting section
        st.markdown("#### HSN-Based Forecasting")
        if st.button("📡 Demand Signal Integration", use_container_width=True, key="demand_signal"):
            st.session_state.page = 'manufacturing_dashboard'
            
        if st.button("📊 Supply Requirement Projections", use_container_width=True, key="supply_projections"):
            st.session_state.page = 'reports'
            
        if st.button("⏳ Timeline Forecasting", use_container_width=True, key="timeline_forecasting"):
            st.session_state.page = 'line_plan'
            
        if st.button("📉 Raw Material Demand Prediction", use_container_width=True, key="raw_material_prediction"):
            st.session_state.page = 'material_tracker'
        
        # Database initialization (hidden in an expander to not clutter the UI)
        with st.expander("⚙️ Database Management"):
            if st.button("Database Setup", use_container_width=True, key="db_init"):
                st.session_state.page = 'db_initialization'
    
    with tab2:
        # Commune Connect Portal Navigation
        st.markdown("### Commune Connect (Digital Retail)")
        
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
    
    with tab3:
        # Synergyze Hub Navigation
        st.markdown("### Synergyze Hub")
        
        # License Engine section
        st.markdown("#### License Engine")
        if st.button("📄 License Application Pages", use_container_width=True, key="license_application"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("📝 Application Review Workflow", use_container_width=True, key="application_review"):
            st.session_state.page = 'order_style_management'
        
        if st.button("💰 Payment Processing (Razorpay)", use_container_width=True, key="payment_processing"):
            st.session_state.page = 'reports'
        
        if st.button("✅ License Approval/Rejection Interface", use_container_width=True, key="license_approval"):
            st.session_state.page = 'line_plan'
        
        if st.button("🔄 License Renewal Management", use_container_width=True, key="license_renewal"):
            st.session_state.page = 'production_timeline'
        
        if st.button("🛑 License Suspension Controls", use_container_width=True, key="license_suspension"):
            st.session_state.page = 'material_tracker'
        
        # User Role Management section
        st.markdown("#### User Role Management")
        if st.button("👤 Role Definition Interface", use_container_width=True, key="role_definition"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("🔑 Permission Assignment", use_container_width=True, key="permission_assignment"):
            st.session_state.page = 'reports'
        
        if st.button("👥 Internal/External User Classification", use_container_width=True, key="user_classification"):
            st.session_state.page = 'order_style_management'
        
        if st.button("🔍 Segment-based User Categorization", use_container_width=True, key="user_categorization"):
            st.session_state.page = 'line_plan'
    
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
