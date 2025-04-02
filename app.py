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
from stock_analysis import show_stock_analysis
from virtual_silk_road_landing import show_virtual_silk_road_landing
from virtual_silk_road import show_virtual_silk_road
from visualization import show_visualization
from empire_os_landing import show_empire_os_landing
from synergyze_landing import show_synergyze_landing
from hsn_transaction_system import show_hsn_transaction_system

# Configure the page
st.set_page_config(
    page_title="Synergyze | Virtual Silk Road",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for app flow
if 'page' not in st.session_state:
    st.session_state.page = 'retailer_analysis'  # Start directly on retailer analysis page for testing

if 'completed_onboarding' not in st.session_state:
    st.session_state.completed_onboarding = True  # Skip onboarding for testing

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

# Initialize new session state for authentication and access control
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

if 'user_role' not in st.session_state:
    st.session_state.user_role = 'public'  # Options: 'public', 'licensed', 'emperor'

# Sidebar navigation
with st.sidebar:
    # Application title with new branding
    st.title("Synergyze Platform")
    st.markdown("""
    <div style='background: linear-gradient(90deg, rgba(75,0,130,0.2) 0%, rgba(123,104,238,0.2) 100%); 
    padding: 10px; border-radius: 5px; margin-bottom: 15px;'>
        <p style='margin: 0; font-size: 0.9em;'>Powered by</p>
        <p style='margin: 0; font-weight: bold;'>Empire OS</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Main navigation sections
    if st.session_state.user_role == 'public':
        # Public-facing marketing pages for the ecosystem
        st.markdown("### Empire Ecosystem")
        
        if st.button("👑 Empire OS", use_container_width=True):
            st.session_state.page = 'empire_os_landing'
            
        if st.button("🌏 Virtual Silk Road", use_container_width=True):
            st.session_state.page = 'vsr_landing'
            
        if st.button("⚡ Synergyze Licenses", use_container_width=True):
            st.session_state.page = 'synergyze_landing'
            
        # Commerce portal
        st.markdown("### Buying House Portal")
        
        if st.button("🛍️ Browse Products", use_container_width=True):
            st.session_state.page = 'product_catalog'
        
        if st.session_state.selected_product is not None:
            if st.button("📋 Product Details", use_container_width=True):
                st.session_state.page = 'product_detail'
        
        if st.session_state.cart:
            if st.button("🛒 View Order", use_container_width=True):
                st.session_state.page = 'order_booking'
                
        st.markdown("### Market Intelligence")
        
        # Add ECG Market Health Check button
        if st.button("📊 Market Health Check", use_container_width=True):
            st.session_state.page = 'retailer_analysis'
            
        # Add Stock Analysis button
        if st.button("📈 Stock Analysis", use_container_width=True):
            st.session_state.page = 'stock_analysis'
            
        st.markdown("### Inventory Management")
        
        # Add HSN Transaction System button
        if st.button("🏆 HSN Transaction Suite", use_container_width=True):
            st.session_state.page = 'hsn_transaction_system'
            
    else:
        # Licensed user or Emperor view sections - private dashboards
        st.markdown("### Empire Command Center")
        
        if st.button("👑 Empire OS Control", use_container_width=True):
            st.session_state.page = 'empire_os_dashboard'
            
        if st.button("🏙️ Virtual Silk Road", use_container_width=True):
            st.session_state.page = 'virtual_silk_road'
            
        if st.button("⚡ License Management", use_container_width=True):
            st.session_state.page = 'license_management'
            
        st.markdown("### Enterprise Intelligence")
            
        if st.button("📊 Market Intelligence", use_container_width=True):
            st.session_state.page = 'retailer_analysis'
            
        if st.button("📈 Technical Analysis", use_container_width=True):
            st.session_state.page = 'visualization'
            
        st.markdown("### Advanced Tools")
        
        if st.button("🏆 HSN Transaction Suite", use_container_width=True):
            st.session_state.page = 'hsn_transaction_system'
    
    # User authentication section
    st.markdown("---")
    st.markdown("### User Access")
    
    # Simple authentication UI for demo purposes
    access_options = ['Public View', 'Licensed User', 'Emperor Access']
    selected_access = st.selectbox(
        "Select Access Level:",
        access_options,
        index=0 if st.session_state.user_role == 'public' else 
              1 if st.session_state.user_role == 'licensed' else 2
    )
    
    if st.button("Switch Access Level", use_container_width=True):
        if selected_access == 'Public View':
            st.session_state.user_role = 'public'
            st.session_state.is_authenticated = False
            st.session_state.page = 'vsr_landing'  # Default to landing page for public users
        elif selected_access == 'Licensed User':
            st.session_state.user_role = 'licensed'
            st.session_state.is_authenticated = True
            st.session_state.page = 'virtual_silk_road'  # Default to VSR for licensed users
        else:  # Emperor Access
            st.session_state.user_role = 'emperor'
            st.session_state.is_authenticated = True
            st.session_state.page = 'virtual_silk_road'  # Default to VSR for emperor too
        st.rerun()
    
    # Disclaimer for demo
    if st.session_state.user_role != 'public':
        st.markdown("""
        <div style='background-color: rgba(255, 230, 153, 0.2); padding: 10px; border-radius: 5px; border-left: 3px solid #FFD700; margin-top: 10px;'>
            <p style='margin: 0; font-size: 0.8em;'><b>Note:</b> You're viewing the {0} interface. In production, this would require proper authentication.</p>
        </div>
        """.format(
            "Emperor" if st.session_state.user_role == 'emperor' else "Licensed User"
        ), unsafe_allow_html=True)
                
    # Reset button at the bottom
    st.markdown("---")
    if st.button("🔄 Reset Application", use_container_width=True):
        st.session_state.page = 'vsr_landing'
        st.session_state.completed_onboarding = False
        st.session_state.selected_product = None
        st.session_state.cart = []
        st.session_state.order_submitted = False
        st.session_state.user_role = 'public'
        st.session_state.is_authenticated = False
        # Reset merchandiser info
        if 'merchandiser' in st.session_state:
            del st.session_state.merchandiser
        if 'conversation' in st.session_state:
            del st.session_state.conversation
        st.rerun()

# Set default page if none is selected
if 'page' not in st.session_state:
    st.session_state.page = 'vsr_landing'  # Default to the public landing page

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
elif st.session_state.page == 'stock_analysis':
    show_stock_analysis()
elif st.session_state.page == 'visualization':
    show_visualization()
elif st.session_state.page == 'hsn_transaction_system':
    show_hsn_transaction_system()
# Empire Ecosystem pages
elif st.session_state.page == 'empire_os_landing':
    show_empire_os_landing()  # Public marketing page for Empire OS
elif st.session_state.page == 'vsr_landing':
    show_virtual_silk_road_landing()  # Public marketing page for Virtual Silk Road
elif st.session_state.page == 'synergyze_landing':
    show_synergyze_landing()  # Public marketing page for Synergyze Licenses

# Private access dashboards
elif st.session_state.page == 'virtual_silk_road':
    # Check if user has proper access
    if st.session_state.user_role in ['licensed', 'emperor']:
        show_virtual_silk_road()  # Private Emperor's view
    else:
        # Redirect unauthorized users to the public landing
        st.warning("⚠️ You need licensed access to view the Emperor's Virtual Silk Road dashboard.")
        show_virtual_silk_road_landing()
# Emperor control dashboards - redirect if no access
elif st.session_state.page in ['empire_os_dashboard', 'license_management']:
    if st.session_state.user_role == 'emperor':
        # Show the Emperor's dashboard
        from empire_os_dashboard import show_empire_os_dashboard, show_license_dashboard
        
        if st.session_state.page == 'empire_os_dashboard':
            show_empire_os_dashboard()
        else:  # license_management
            show_license_dashboard()
    else:
        # Redirect unauthorized users
        st.warning("⚠️ Only the Emperor has access to this command interface.")
        show_empire_os_landing()
else:
    # Fallback to landing page if an unknown page is requested
    show_virtual_silk_road_landing()

# Footer - dynamically change based on the current section
st.markdown("---")

# Create a universal ecosystem diagram at the bottom of all pages
if st.session_state.page in ['empire_os_landing', 'vsr_landing', 'synergyze_landing', 'virtual_silk_road', 'empire_os_dashboard', 'license_management']:
    # Show the ecosystem hierarchy for all Imperial pages
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <div style="display: inline-flex; align-items: center; justify-content: center; gap: 15px;">
            <div style="text-align: center;">
                <span style="font-weight: bold; color: gold; font-size: 0.9em;">👑 EMPIRE OS</span><br>
                <span style="font-size: 0.7em; color: #666;">Operating System</span>
            </div>
            <div style="color: #999;">→</div>
            <div style="text-align: center;">
                <span style="font-weight: bold; color: #4B0082; font-size: 0.9em;">🌏 VIRTUAL SILK ROAD</span><br>
                <span style="font-size: 0.7em; color: #666;">Network</span>
            </div>
            <div style="color: #999;">→</div>
            <div style="text-align: center;">
                <span style="font-weight: bold; color: #8A2BE2; font-size: 0.9em;">⚡ SYNERGYZE</span><br>
                <span style="font-size: 0.7em; color: #666;">Licenses</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Different footers based on the specific ecosystem page
    if st.session_state.page == 'empire_os_landing':
        st.caption("Empire OS | The Ultimate Enterprise Governance Operating System | © 2025 Imperial Technology")
    elif st.session_state.page in ['vsr_landing', 'virtual_silk_road']:
        st.caption("Virtual Silk Road | Powered by Empire OS | © 2025 Imperial Technology")
    elif st.session_state.page in ['synergyze_landing', 'license_management']:
        st.caption("Synergyze Licenses | Deployed on the Virtual Silk Road | Powered by Empire OS | © 2025 Imperial Technology")
    else:
        st.caption("Empire Ecosystem | © 2025 Imperial Technology")
else:
    # For other portal pages not directly related to the Empire ecosystem
    st.caption("Buying House Portal | Ready Styles. Bulk Orders. Tailored For You.")
