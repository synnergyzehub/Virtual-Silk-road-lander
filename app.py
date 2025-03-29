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

# Import visualization modules
from supply_chain_visualization import show_supply_chain_visualization
from synergy_visualization import show_synergy_visualization
from voi_jeans_demo import show_voi_jeans_demo

# Import notification service
from notification_service import show_notification_settings, check_twilio_credentials

# Configure the page
st.set_page_config(
    page_title="ECG Manufacturing Portal",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'notification_settings'  # Temporarily starting with notification settings for testing

# Initialize database with sample data if needed
if 'db_initialized' not in st.session_state:
    # Try to initialize database
    initialize_database()
    st.session_state.db_initialized = True

# Check for missing Twilio credentials when accessing notification features
if 'check_twilio_keys' not in st.session_state:
    st.session_state.check_twilio_keys = False
    
if st.session_state.page == 'notification_settings' and not check_twilio_credentials() and not st.session_state.check_twilio_keys:
    st.session_state.check_twilio_keys = True
    st.info("Twilio credentials required for SMS notifications. Please use the button below to set them up.")
    
    # Create a button for the user to initiate the secrets request process
    if st.button("Set Up Twilio Credentials"):
        # Use ask_secrets tool to get the secrets
        from ask_secrets import ask_secrets
        ask_secrets(
            secret_keys=["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_PHONE_NUMBER"],
            user_message="""
            To enable SMS notifications for department alerts, please provide your Twilio credentials:
            
            1. **TWILIO_ACCOUNT_SID**: Your Twilio account SID 
            2. **TWILIO_AUTH_TOKEN**: Your Twilio auth token
            3. **TWILIO_PHONE_NUMBER**: Your Twilio phone number (must be purchased from Twilio)
            
            These credentials will be stored securely as environment variables and used only for sending 
            SMS notifications to the configured department contacts.
            """
        )

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
    st.title("Voi Jeans Management Portal")
    
    # Demo button with a prominent style
    st.markdown(
        """
        <div style='background-color: #1E3A8A; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;'>
            <p style='margin: 0; font-weight: bold; color: white;'>✨ NEW!</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    if st.button("🧥 VOI JEANS DEMO", use_container_width=True, type="primary"):
        st.session_state.page = 'voi_jeans_demo'
    
    st.markdown("---")
    
    # Create three sections for navigation
    tab1, tab2, tab3 = st.tabs(["🏭 Manufacturing (Scotts)", "🏬 Retail Distribution", "⚙️ Management Hub"])
    
    with tab1:
        # Manufacturing Portal Navigation
        st.markdown("### Manufacturing (Scotts Garments - CMP)")
        
        # Procurement System section
        st.markdown("#### Denim Procurement")
        if st.button("👖 SS25 Denim Styles", use_container_width=True, key="material_tracker"):
            st.session_state.page = 'material_tracker'
            
        if st.button("🏭 Scotts Garments Management", use_container_width=True, key="order_style_mgmt"):
            st.session_state.page = 'order_style_management'
            
        if st.button("💰 CMP Cost Calculation", use_container_width=True, key="reports"):
            st.session_state.page = 'reports'
            
        if st.button("📝 Production Order Placement", use_container_width=True, key="order_placement"):
            st.session_state.page = 'order_style_management'
            
        if st.button("📦 Denim Fabric Tracking", use_container_width=True, key="material_tracking"):
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
            
        if st.button("🔄 Supply Chain Visualization", use_container_width=True, key="supply_chain_viz"):
            st.session_state.page = 'supply_chain_visualization'
            
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
        st.markdown("### Voi Jeans Retail Distribution")
        
        # Store Management
        st.markdown("#### Store Management")
        if st.button("🏬 Retail Store Network", use_container_width=True, key="browse_products"):
            st.session_state.page = 'product_catalog'
        
        if st.button("📊 Daily Sales vs Target", use_container_width=True, key="daily_sales"):
            st.session_state.page = 'retailer_analysis'
        
        if st.button("🔖 E-Wards Loyalty Program", use_container_width=True, key="loyalty_program"):
            st.session_state.page = 'product_detail'
        
        if st.button("📦 Store Inventory Management", use_container_width=True, key="view_order"):
            st.session_state.page = 'order_booking'
        
        # Product Management
        st.markdown("#### Product Management")
        
        if st.button("👖 Denim Collection", use_container_width=True, key="denim_collection"):
            st.session_state.page = 'product_catalog'
            
        if st.button("🎯 SS25 Collection Planning", use_container_width=True, key="ss25_planning"):
            st.session_state.page = 'order_style_management'
            
        if st.button("🔍 Style Performance Analysis", use_container_width=True, key="style_performance"):
            st.session_state.page = 'retailer_analysis'
        
        # Market Intelligence Section
        st.markdown("#### Retail Analytics")
        
        if st.button("📈 Sales Performance Dashboard", use_container_width=True, key="market_health"):
            st.session_state.page = 'retailer_analysis'
        
        if st.button("📱 Online vs In-Store Analysis", use_container_width=True, key="online_vs_store"):
            st.session_state.page = 'manufacturing_dashboard'
            
        if st.button("🏙️ Regional Market Insights", use_container_width=True, key="regional_insights"):
            st.session_state.page = 'reports'
        
        # Add a hint about the retail analytics
        st.info("Access real-time sales analytics and performance metrics across all Voi Jeans retail locations.")
        
        # Add access to the merchandiser agent
        st.markdown("### Your Support Team")
        
        # Merchandiser button with notification badge style
        if st.button("👩‍💼 Your Merchandiser Agent", use_container_width=True, key="merchandiser"):
            st.session_state.page = 'merchandiser_agent'
        
        # Show a hint about the merchandiser
        if 'merchandiser' in st.session_state and isinstance(st.session_state.merchandiser, dict):
            # Display merchandiser info if already assigned and valid
            st.markdown(f"""
            <div style='background-color: #1E3A8A; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                <p style='margin: 0; font-size: 0.9em;'>You're working with:</p>
                <p style='margin: 0; font-weight: bold;'>{st.session_state.merchandiser.get('name', 'Your Merchandiser')}</p>
                <p style='margin: 0; font-size: 0.8em;'>{st.session_state.merchandiser.get('specialization', 'Denim Expert')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show a teaser about having a merchandiser
            st.info("Connect with your dedicated merchandising agent for personalized support throughout your order process.")
    
    with tab3:
        # Voi Jeans Management Hub
        st.markdown("### Voi Jeans Management Hub")
        
        # Finance & Governance section
        st.markdown("#### Finance & Governance")
        if st.button("💰 CMP Cost Management", use_container_width=True, key="license_application"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("📊 Financial Performance", use_container_width=True, key="application_review"):
            st.session_state.page = 'order_style_management'
        
        if st.button("💵 Vendor Payment Processing", use_container_width=True, key="payment_processing"):
            st.session_state.page = 'reports'
        
        if st.button("📑 Compliance Documentation", use_container_width=True, key="license_approval"):
            st.session_state.page = 'line_plan'
        
        if st.button("🔄 Monthly Reconciliation", use_container_width=True, key="license_renewal"):
            st.session_state.page = 'production_timeline'
        
        # Administration section
        st.markdown("#### Administration")
        if st.button("👤 User Account Management", use_container_width=True, key="role_definition"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("🔐 Access Control Settings", use_container_width=True, key="permission_assignment"):
            st.session_state.page = 'reports'
        
        if st.button("🏢 Department Configuration", use_container_width=True, key="user_classification"):
            st.session_state.page = 'order_style_management'
        
        if st.button("📱 Mobile App Administration", use_container_width=True, key="user_categorization"):
            st.session_state.page = 'line_plan'
            
        # Check Twilio credentials
        has_twilio = check_twilio_credentials()
        
        if st.button(
            f"🔔 Notification Settings {'' if has_twilio else '⚠️'}", 
            use_container_width=True, 
            key="notification_settings",
            help="Configure SMS notifications for departments and events"
        ):
            st.session_state.page = 'notification_settings'
            
        # Business Intelligence section
        st.markdown("#### Business Intelligence")
        if st.button("📈 Executive Dashboard", use_container_width=True, key="executive_dashboard"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("📊 SS25 Performance Metrics", use_container_width=True, key="ss25_metrics"):
            st.session_state.page = 'retailer_analysis'
        
        if st.button("📉 Competitor Analysis", use_container_width=True, key="competitor_analysis"):
            st.session_state.page = 'reports'
        
        if st.button("🌐 Market Trend Analysis", use_container_width=True, key="license_suspension"):
            st.session_state.page = 'material_tracker'
            
        # Synergyze Visualization section
        st.markdown("#### Synergyze Ecosystem")
        if st.button("🔄 Synergyze Ecosystem Visualization", use_container_width=True, key="synergy_viz"):
            st.session_state.page = 'synergy_visualization'
            
        if st.button("⚖️ License Management", use_container_width=True, key="license_management"):
            st.session_state.page = 'synergy_visualization'
            
        if st.button("🔗 Supply & Retail Integration", use_container_width=True, key="woven_commune_integration"):
            st.session_state.page = 'synergy_visualization'
    
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
elif st.session_state.page == 'supply_chain_visualization':
    show_supply_chain_visualization()
elif st.session_state.page == 'synergy_visualization':
    show_synergy_visualization()
elif st.session_state.page == 'voi_jeans_demo':
    show_voi_jeans_demo()
elif st.session_state.page == 'notification_settings':
    show_notification_settings()

# Footer
st.markdown("---")
st.caption("Voi Jeans Retail India Pvt Ltd | Denim Excellence. CMP Manufacturing. Retail Distribution.")
