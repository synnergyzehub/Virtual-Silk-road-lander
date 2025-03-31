import streamlit as st

# Configure the page (must be the first Streamlit command)
st.set_page_config(
    page_title="ECG Manufacturing Portal",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
from location_inventory_tracker import show_location_inventory_tracker
from inventory_story_generator import show_inventory_story_generator

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
from retail_distribution import show_retail_distribution

# Import new modules for HSN code tax mapping and trade show order engine
from hsn_tax_mapping import show_hsn_tax_mapping
from trade_show_order_engine import show_trade_show_order_engine

# Import Investment Milestone Passport feature
from investment_milestone_passport import show_investment_milestone_passport

# Import Data Integration module for centralized data management
from data_integration import show_data_integration

# Import Stock Inventory Health Radar module
from stock_analysis import show_stock_analysis

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'data_integration'  # Start with the data integration hub

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
        
        if st.button("💲 HSN Code Tax Mapping", use_container_width=True, key="hsn_tax_mapping", help="Map and analyze transaction types based on HSN codes for taxation"):
            st.session_state.page = 'hsn_tax_mapping'
            
        # Trade Show Order Engine section
        st.markdown("#### Trade Show & Procurement")
        if st.button("🏙️ Trade Show Order Engine", use_container_width=True, key="trade_show_order", help="Manage orders, samples, and procurement for trade shows"):
            st.session_state.page = 'trade_show_order_engine'
            
        if st.button("📊 Sample Management", use_container_width=True, key="sample_management", help="Track and manage product samples for trade shows and buyers"):
            st.session_state.page = 'trade_show_order_engine'
            
        if st.button("📆 Trade Show Calendar", use_container_width=True, key="trade_show_calendar", help="View upcoming trade shows and manage participation"):
            st.session_state.page = 'trade_show_order_engine'
        
        # Database initialization (hidden in an expander to not clutter the UI)
        with st.expander("⚙️ Database Management"):
            if st.button("Database Setup", use_container_width=True, key="db_init"):
                st.session_state.page = 'db_initialization'
    
    with tab2:
        # Commune Connect Portal Navigation
        st.markdown("### Voi Jeans Retail Distribution")
        
        # Integrated Retail Distribution Dashboard
        if st.button("🏬 Retail Distribution Dashboard", use_container_width=True, type="primary", key="retail_distribution"):
            st.session_state.page = 'retail_distribution'
        
        # Main retail sections
        st.markdown("#### Store Management")
        if st.button("🏬 Store Network", use_container_width=True, key="store_network"):
            st.session_state.page = 'retail_distribution'
        
        if st.button("📊 Sales Performance", use_container_width=True, key="sales_performance"):
            st.session_state.page = 'retail_distribution'
        
        if st.button("🔖 E-Wards Loyalty Program", use_container_width=True, key="loyalty_program"):
            st.session_state.page = 'retail_distribution'
        
        # Consumer Analytics
        st.markdown("#### Consumer Insights")
        if st.button("👤 Consumer Behavior Analysis", use_container_width=True, key="consumer_analysis"):
            st.session_state.page = 'retail_distribution'
            
        if st.button("🔍 Retail Fashion Trends", use_container_width=True, key="fashion_trends"):
            st.session_state.page = 'retail_distribution'
            
        if st.button("📊 Marketing Effectiveness", use_container_width=True, key="marketing_analytics"):
            st.session_state.page = 'retail_distribution'
        
        # Product Catalog Access
        st.markdown("#### Product Catalog")
        if st.button("👖 Product Collection", use_container_width=True, key="product_collection"):
            st.session_state.page = 'product_catalog'
            
        # Trade Show Access
        st.markdown("#### Trade Show Management")
        if st.button("🏙️ Trade Show Orders", use_container_width=True, key="retail_trade_show", help="Manage trade show orders and samples"):
            st.session_state.page = 'trade_show_order_engine'
        
        # Add a hint about the retail analytics
        st.info("The Retail Distribution Dashboard provides a comprehensive view of store performance, consumer behavior, and loyalty program metrics.")
        
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
            st.info("Connect with your dedicated merchandising agent for personalized support.")
    
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
            
        # Investment Milestones section
        st.markdown("#### Investment Milestones")
        if st.button("🪪 Investment Milestone Passport", use_container_width=True, key="milestone_passport", help="Collect digital badges for financial milestones and achievements"):
            st.session_state.page = 'investment_milestone_passport'
        
        # Data Integration Hub section
        st.markdown("#### Data Integration Hub")
        if st.button("📊 Empire OS Data Integration", use_container_width=True, key="data_integration_hub", help="Centralized data upload, processing and visualization from various sources"):
            st.session_state.page = 'data_integration'
        
        # Business Intelligence section
        st.markdown("#### Business Intelligence")
        if st.button("📈 Executive Dashboard", use_container_width=True, key="executive_dashboard"):
            st.session_state.page = 'manufacturing_dashboard'
        
        if st.button("📊 SS25 Performance Metrics", use_container_width=True, key="ss25_metrics"):
            st.session_state.page = 'retailer_analysis'
        
        if st.button("📉 Competitor Analysis", use_container_width=True, key="competitor_analysis"):
            st.session_state.page = 'reports'
            
        if st.button("📊 Stock Inventory Health Radar", use_container_width=True, key="stock_inventory_radar", help="Visual inventory stock level tracking and analysis", type="primary"):
            st.session_state.page = 'stock_analysis'
            
        if st.button("📍 Location Inventory Tracker", use_container_width=True, key="location_inventory", help="Track inventory across all locations (factories, warehouses, stores)", type="primary"):
            st.session_state.page = 'location_inventory'
            
        if st.button("📖 Inventory Movement Story", use_container_width=True, key="inventory_story", help="Generate narrative insights from inventory movement patterns", type="primary"):
            st.session_state.page = 'inventory_story'
        
        if st.button("🌐 Market Trend Analysis", use_container_width=True, key="license_suspension"):
            st.session_state.page = 'material_tracker'
            
        if st.button("💲 HSN Code Tax Analysis", use_container_width=True, key="hsn_tax_analysis", help="Map and analyze transaction types based on HSN codes for tax reporting"):
            st.session_state.page = 'hsn_tax_mapping'
            
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
elif st.session_state.page == 'retail_distribution':
    show_retail_distribution()
elif st.session_state.page == 'hsn_tax_mapping':
    show_hsn_tax_mapping()
elif st.session_state.page == 'trade_show_order_engine':
    show_trade_show_order_engine()
elif st.session_state.page == 'investment_milestone_passport':
    show_investment_milestone_passport()
elif st.session_state.page == 'data_integration':
    show_data_integration()
elif st.session_state.page == 'stock_analysis':
    show_stock_analysis()
elif st.session_state.page == 'location_inventory':
    show_location_inventory_tracker()
elif st.session_state.page == 'inventory_story':
    show_inventory_story_generator()

# Footer
st.markdown("---")
st.caption("Voi Jeans Retail India Pvt Ltd | Denim Excellence. CMP Manufacturing. Retail Distribution.")
