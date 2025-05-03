"""
Genesis License Dashboard

A Streamlit dashboard for managing Genesis Stack licenses.
This dashboard provides a user-friendly interface for interacting with the
Genesis License API.
"""

import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Genesis License Dashboard",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# License API configuration
API_HOST = "localhost"
API_PORT = 5001
API_BASE_URL = f"http://{API_HOST}:{API_PORT}/api/v1"
API_KEY = "emperorkey123"  # Default API key

# Initialize session state for form data if not already present
if 'holder_id' not in st.session_state:
    st.session_state.holder_id = ""
if 'holder_name' not in st.session_state:
    st.session_state.holder_name = ""
if 'holder_contact' not in st.session_state:
    st.session_state.holder_contact = ""
if 'license_id' not in st.session_state:
    st.session_state.license_id = ""
if 'license_key' not in st.session_state:
    st.session_state.license_key = ""
if 'selected_license_type' not in st.session_state:
    st.session_state.selected_license_type = "enterprise"
if 'validity_days' not in st.session_state:
    st.session_state.validity_days = 365
if 'permissions' not in st.session_state:
    st.session_state.permissions = []
if 'metadata' not in st.session_state:
    st.session_state.metadata = {}
if 'organization_size' not in st.session_state:
    st.session_state.organization_size = "Enterprise"
if 'industry' not in st.session_state:
    st.session_state.industry = "Retail"
if 'region' not in st.session_state:
    st.session_state.region = "Asia"
if 'country' not in st.session_state:
    st.session_state.country = "India"
if 'all_permissions' not in st.session_state:
    st.session_state.all_permissions = [
        "transaction_governance",
        "channel_management",
        "inventory_sync",
        "financial_reporting",
        "compliance_management",
        "divine_alignment",
        "wto_compliance",
        "resource_optimization",
        "ethical_business",
        "imperial_oversight"
    ]

# CSS for styling
def local_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .active-badge {
        background-color: #10B981;
        color: white;
    }
    .inactive-badge {
        background-color: #EF4444;
        color: white;
    }
    .pending-badge {
        background-color: #F59E0B;
        color: white;
    }
    .divine-alignment {
        margin-top: 10px;
        padding: 10px;
        border-radius: 4px;
        background-color: #F0F9FF;
        border-left: 4px solid #3B82F6;
    }
    .license-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        background-color: white;
    }
    .license-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .license-key {
        font-family: monospace;
        padding: 0.5rem;
        background-color: #F3F4F6;
        border-radius: 0.25rem;
        margin-top: 0.5rem;
        overflow-x: auto;
        white-space: nowrap;
    }
    .renewal-notice {
        padding: 0.5rem;
        border-radius: 0.25rem;
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# API client functions
def make_api_request(method, endpoint, data=None, params=None):
    """Make a request to the License API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        # Check if response was successful
        response.raise_for_status()
        
        # Parse JSON response
        if response.content:
            return response.json()
        return {"status": "success"}
    
    except requests.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return {"error": str(e)}

def check_api_health():
    """Check if the License API is healthy"""
    try:
        response = requests.get(f"http://{API_HOST}:{API_PORT}/health")
        return response.json()
    except requests.RequestException:
        return None

def get_license_types():
    """Get available license types from the API"""
    response = make_api_request("GET", "/license-types")
    if "license_types" in response:
        return response["license_types"]
    return []

def create_license(license_data):
    """Create a new license"""
    response = make_api_request("POST", "/licenses", data=license_data)
    return response

def get_license(license_id):
    """Get a license by ID"""
    response = make_api_request("GET", f"/licenses/{license_id}")
    return response

def verify_license(license_id):
    """Verify a license by ID"""
    response = make_api_request("POST", f"/licenses/{license_id}/verify")
    return response

def update_license(license_id, update_data):
    """Update a license"""
    response = make_api_request("PATCH", f"/licenses/{license_id}", data=update_data)
    return response

def revoke_license(license_id, reason):
    """Revoke a license"""
    response = make_api_request("POST", f"/licenses/{license_id}/revoke", data={"reason": reason})
    return response

def renew_license(license_id, validity_days):
    """Renew a license"""
    response = make_api_request("POST", f"/licenses/{license_id}/renew", data={"validity_days": validity_days})
    return response

def check_renewal_needed(license_id):
    """Check if a license needs renewal"""
    response = make_api_request("GET", f"/licenses/{license_id}/check-renewal")
    return response

def verify_license_key(license_id, license_key):
    """Verify a license key"""
    response = make_api_request("POST", f"/licenses/{license_id}/verify-key", data={"license_key": license_key})
    return response

def list_licenses(filters=None):
    """List all licenses with optional filtering"""
    response = make_api_request("GET", "/licenses", params=filters)
    return response

def get_divine_governance():
    """Get divine governance information"""
    response = make_api_request("GET", "/divine-governance")
    return response
    
def get_divine_scorecard(license_id):
    """Get detailed divine principles scorecard for a license"""
    response = make_api_request("GET", f"/divine-scorecard/{license_id}")
    return response
    
def save_divine_scorecard(license_id, output_dir=None):
    """Save divine principles scorecard for a license to the filesystem"""
    params = {}
    if output_dir:
        params["output_dir"] = output_dir
    response = make_api_request("POST", f"/divine-scorecard/save/{license_id}", params=params)
    return response

# UI Components
def render_header():
    """Render the dashboard header"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("# 🔑")
    
    with col2:
        st.title("Genesis License Dashboard")
        st.markdown("Manage your Genesis Stack licenses with divine governance")

def render_sidebar():
    """Render the sidebar"""
    st.sidebar.title("Genesis License System")
    
    # API Status
    health = check_api_health()
    if health and health.get("status") == "healthy":
        st.sidebar.success("✅ License API Connected")
    else:
        st.sidebar.error("❌ License API Disconnected")
    
    # API Config
    st.sidebar.header("API Configuration")
    global API_HOST, API_PORT, API_BASE_URL, API_KEY
    
    API_HOST = st.sidebar.text_input("API Host", value=API_HOST)
    API_PORT = st.sidebar.number_input("API Port", value=API_PORT, min_value=1, max_value=65535)
    API_BASE_URL = f"http://{API_HOST}:{API_PORT}/api/v1"
    API_KEY = st.sidebar.text_input("API Key", value=API_KEY, type="password")
    
    # Divine governance info
    st.sidebar.header("Divine Governance")
    governance = get_divine_governance()
    
    if governance:
        # Display governance levels
        st.sidebar.subheader("Governance Levels")
        for level in governance.get("governance_levels", []):
            st.sidebar.markdown(f"- {level.capitalize()}")
        
        # Display minimum alignment
        min_alignment = governance.get("min_divine_alignment", 0)
        st.sidebar.subheader("Minimum Divine Alignment")
        st.sidebar.progress(min_alignment / 100, text=f"{min_alignment}%")
        
        # Display verification interval
        interval = governance.get("verification_interval", 0)
        if interval:
            hours = interval / 3600
            st.sidebar.subheader("Verification Interval")
            st.sidebar.markdown(f"{hours:.1f} hours")
    
    # App info
    st.sidebar.markdown("---")
    st.sidebar.caption("Genesis License Dashboard v1.0")
    st.sidebar.caption("© 2025 Divine Governance Council")

def render_license_creation():
    """Render the license creation form"""
    st.header("Create New License")
    
    # Get available license types
    license_types = get_license_types()
    
    with st.form("license_creation_form"):
        # License type selection
        st.subheader("License Type")
        selected_license_type = st.selectbox(
            "Select License Type",
            options=license_types,
            index=license_types.index(st.session_state.selected_license_type) if st.session_state.selected_license_type in license_types else 0,
            key="license_type_select"
        )
        
        # License holder information
        st.subheader("License Holder")
        col1, col2 = st.columns(2)
        
        with col1:
            holder_id = st.text_input("Holder ID", value=st.session_state.holder_id)
            holder_name = st.text_input("Holder Name", value=st.session_state.holder_name)
        
        with col2:
            holder_contact = st.text_input("Contact Email", value=st.session_state.holder_contact)
            validity_days = st.number_input("Validity (days)", value=st.session_state.validity_days, min_value=1, max_value=3650)
        
        # Permissions
        st.subheader("Permissions")
        permissions = st.multiselect(
            "Select Permissions",
            options=st.session_state.all_permissions,
            default=st.session_state.permissions
        )
        
        # Metadata
        st.subheader("Metadata")
        col1, col2 = st.columns(2)
        
        with col1:
            organization_size = st.selectbox(
                "Organization Size",
                options=["Individual", "Small", "Medium", "Enterprise", "Global"],
                index=["Individual", "Small", "Medium", "Enterprise", "Global"].index(st.session_state.organization_size)
            )
            industry = st.text_input("Industry", value=st.session_state.industry)
        
        with col2:
            region = st.text_input("Region", value=st.session_state.region)
            country = st.text_input("Country", value=st.session_state.country)
        
        # Submit button
        submitted = st.form_submit_button("Create License", type="primary")
        
        if submitted:
            # Save form data to session state
            st.session_state.holder_id = holder_id
            st.session_state.holder_name = holder_name
            st.session_state.holder_contact = holder_contact
            st.session_state.selected_license_type = selected_license_type
            st.session_state.validity_days = validity_days
            st.session_state.permissions = permissions
            st.session_state.organization_size = organization_size
            st.session_state.industry = industry
            st.session_state.region = region
            st.session_state.country = country
            
            # Prepare license data
            license_data = {
                "type": selected_license_type,
                "holder": {
                    "id": holder_id,
                    "name": holder_name,
                    "contact": holder_contact
                },
                "validity_days": validity_days,
                "permissions": permissions,
                "metadata": {
                    "organization_size": organization_size,
                    "industry": industry,
                    "region": region,
                    "country": country
                }
            }
            
            # Create license
            with st.spinner("Creating license..."):
                response = create_license(license_data)
                
                if "error" in response:
                    st.error(f"Failed to create license: {response['error']}")
                else:
                    st.success("License created successfully!")
                    
                    # Store license ID and key in session state
                    license_data = response.get("license", {})
                    st.session_state.license_id = license_data.get("id", "")
                    st.session_state.license_key = response.get("license_key", "")
                    
                    # Display license details
                    st.subheader("License Details")
                    
                    st.markdown(f"**License ID:** {st.session_state.license_id}")
                    st.markdown(f"**License Type:** {license_data.get('type', '')}")
                    st.markdown(f"**Status:** {license_data.get('status', '')}")
                    st.markdown(f"**Issued:** {license_data.get('issued_at', '')}")
                    st.markdown(f"**Expires:** {license_data.get('expires_at', '')}")
                    
                    # Display license key
                    st.markdown("**License Key:**")
                    st.code(st.session_state.license_key)
                    
                    # Display divine alignment
                    divine_verification = license_data.get("divine_verification", {})
                    alignment_score = divine_verification.get("alignment_score", 0)
                    
                    st.markdown(f"**Divine Alignment Score:** {alignment_score}%")
                    st.progress(alignment_score / 100)

def render_license_management():
    """Render the license management section"""
    st.header("License Management")
    
    # Search for license
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_license_id = st.text_input("License ID", value=st.session_state.license_id)
    
    with search_col2:
        search_button = st.button("Load License", type="primary")
    
    if search_button and search_license_id:
        with st.spinner("Loading license..."):
            license_data = get_license(search_license_id)
            
            if "error" in license_data:
                st.error(f"Failed to load license: {license_data['error']}")
            else:
                # Store license ID in session state
                st.session_state.license_id = search_license_id
                
                # Display license details
                st.subheader("License Details")
                
                # Format license status with badge
                status = license_data.get("status", "")
                status_badge = f'<span class="status-badge {status}-badge">{status.upper()}</span>'
                
                # Basic info
                st.markdown(f"**License ID:** {search_license_id}")
                st.markdown(f"**License Type:** {license_data.get('type', '')}")
                st.markdown(f"**Status:** {status_badge}", unsafe_allow_html=True)
                
                # Dates
                issued_at = license_data.get("issued_at", "")
                expires_at = license_data.get("expires_at", "")
                
                if issued_at:
                    try:
                        issued_date = datetime.fromisoformat(issued_at.replace('Z', '+00:00'))
                        issued_at = issued_date.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                if expires_at:
                    try:
                        expires_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                        expires_at = expires_date.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                st.markdown(f"**Issued:** {issued_at}")
                st.markdown(f"**Expires:** {expires_at}")
                
                # Holder information
                holder = license_data.get("holder", {})
                st.subheader("License Holder")
                st.markdown(f"**ID:** {holder.get('id', '')}")
                st.markdown(f"**Name:** {holder.get('name', '')}")
                st.markdown(f"**Contact:** {holder.get('contact', '')}")
                
                # Permissions
                st.subheader("Permissions")
                permissions = license_data.get("permissions", [])
                if permissions:
                    for permission in permissions:
                        st.markdown(f"- {permission}")
                else:
                    st.markdown("No permissions assigned")
                
                # Divine verification
                st.subheader("Divine Verification")
                divine_verification = license_data.get("divine_verification", {})
                alignment_score = divine_verification.get("alignment_score", 0)
                verification_timestamp = divine_verification.get("verification_timestamp", "")
                
                if verification_timestamp:
                    try:
                        verification_date = datetime.fromisoformat(verification_timestamp.replace('Z', '+00:00'))
                        verification_timestamp = verification_date.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                st.markdown(f"**Alignment Score:** {alignment_score}%")
                st.progress(alignment_score / 100)
                st.markdown(f"**Last Verification:** {verification_timestamp}")
                st.markdown(f"**Verification Authority:** {divine_verification.get('verification_authority', '')}")
                
                # Metadata
                st.subheader("Metadata")
                metadata = license_data.get("metadata", {})
                if metadata:
                    for key, value in metadata.items():
                        st.markdown(f"**{key}:** {value}")
                else:
                    st.markdown("No metadata available")
                
                # Check if renewal is needed
                st.subheader("Renewal Status")
                with st.spinner("Checking renewal status..."):
                    renewal_data = check_renewal_needed(search_license_id)
                    
                    if "error" not in renewal_data:
                        renewal_needed = renewal_data.get("renewal_needed", False)
                        days_until_expiry = renewal_data.get("days_until_expiry", 0)
                        
                        if renewal_needed:
                            st.warning(f"⚠️ This license needs renewal. {days_until_expiry} days until expiry.")
                            
                            # Offer renewal option
                            renewal_col1, renewal_col2 = st.columns([3, 1])
                            
                            with renewal_col1:
                                renewal_days = st.number_input("Renewal Period (days)", value=365, min_value=1, max_value=3650)
                            
                            with renewal_col2:
                                renew_button = st.button("Renew License")
                            
                            if renew_button:
                                with st.spinner("Renewing license..."):
                                    response = renew_license(search_license_id, renewal_days)
                                    
                                    if "error" in response:
                                        st.error(f"Failed to renew license: {response['error']}")
                                    else:
                                        st.success(f"License renewed successfully until {response.get('license', {}).get('expires_at', '')}")
                        else:
                            st.success(f"✅ This license does not need renewal. {days_until_expiry} days until expiry.")
                
                # License Operations
                st.subheader("License Operations")
                
                # Create columns for different operations
                ops_col1, ops_col2, ops_col3 = st.columns(3)
                
                with ops_col1:
                    verify_button = st.button("Verify License")
                    
                    if verify_button:
                        with st.spinner("Verifying license..."):
                            verification = verify_license(search_license_id)
                            
                            if "error" in verification:
                                st.error(f"Failed to verify license: {verification['error']}")
                            else:
                                is_valid = verification.get("valid", False)
                                reason = verification.get("reason", "")
                                
                                if is_valid:
                                    st.success(f"✅ License is valid: {reason}")
                                else:
                                    st.error(f"❌ License is invalid: {reason}")
                
                with ops_col2:
                    update_button = st.button("Update Metadata")
                    
                    if update_button:
                        # Show update form
                        with st.form("update_form"):
                            st.subheader("Update Metadata")
                            
                            updated_organization_size = st.selectbox(
                                "Organization Size",
                                options=["Individual", "Small", "Medium", "Enterprise", "Global"],
                                index=["Individual", "Small", "Medium", "Enterprise", "Global"].index(
                                    metadata.get("organization_size", "Enterprise")
                                )
                            )
                            
                            updated_industry = st.text_input("Industry", value=metadata.get("industry", ""))
                            updated_region = st.text_input("Region", value=metadata.get("region", ""))
                            updated_country = st.text_input("Country", value=metadata.get("country", ""))
                            
                            update_submit = st.form_submit_button("Save Updates")
                            
                            if update_submit:
                                update_data = {
                                    "metadata": {
                                        "organization_size": updated_organization_size,
                                        "industry": updated_industry,
                                        "region": updated_region,
                                        "country": updated_country
                                    }
                                }
                                
                                with st.spinner("Updating license..."):
                                    response = update_license(search_license_id, update_data)
                                    
                                    if "error" in response:
                                        st.error(f"Failed to update license: {response['error']}")
                                    else:
                                        st.success("License updated successfully!")
                
                with ops_col3:
                    revoke_button = st.button("Revoke License")
                    
                    if revoke_button:
                        # Show revocation form
                        with st.form("revoke_form"):
                            st.subheader("Revoke License")
                            st.warning("⚠️ This action cannot be undone!")
                            
                            revocation_reason = st.text_area("Revocation Reason", value="")
                            
                            revoke_submit = st.form_submit_button("Confirm Revocation")
                            
                            if revoke_submit and revocation_reason:
                                with st.spinner("Revoking license..."):
                                    response = revoke_license(search_license_id, revocation_reason)
                                    
                                    if "error" in response:
                                        st.error(f"Failed to revoke license: {response['error']}")
                                    else:
                                        st.success("License revoked successfully!")

def render_license_verification():
    """Render the license verification section"""
    st.header("License Verification")
    
    # License verification form
    with st.form("license_verification_form"):
        st.subheader("Verify License and Key")
        
        verification_license_id = st.text_input("License ID", value=st.session_state.license_id)
        verification_license_key = st.text_input("License Key", value=st.session_state.license_key)
        
        verify_submit = st.form_submit_button("Verify", type="primary")
        
        if verify_submit and verification_license_id and verification_license_key:
            with st.spinner("Verifying license and key..."):
                # First verify the license itself
                license_verification = verify_license(verification_license_id)
                
                if "error" in license_verification:
                    st.error(f"Failed to verify license: {license_verification['error']}")
                else:
                    license_valid = license_verification.get("valid", False)
                    license_reason = license_verification.get("reason", "")
                    
                    # Then verify the license key
                    key_verification = verify_license_key(verification_license_id, verification_license_key)
                    
                    if "error" in key_verification:
                        st.error(f"Failed to verify license key: {key_verification['error']}")
                    else:
                        key_valid = key_verification.get("valid", False)
                        
                        # Display results
                        st.subheader("Verification Results")
                        
                        # License verification result
                        if license_valid:
                            st.success(f"✅ License is valid: {license_reason}")
                        else:
                            st.error(f"❌ License is invalid: {license_reason}")
                        
                        # Key verification result
                        if key_valid:
                            st.success("✅ License key is valid")
                        else:
                            st.error("❌ License key is invalid")
                        
                        # Overall result
                        if license_valid and key_valid:
                            st.success("✅ License and key combination is valid")
                        else:
                            st.error("❌ License and key combination is invalid")

def render_license_directory():
    """Render the license directory"""
    st.header("License Directory")
    
    # Fetch all licenses
    with st.spinner("Loading licenses..."):
        response = list_licenses()
        
        if "error" in response:
            st.error(f"Failed to load licenses: {response['error']}")
        else:
            licenses = response.get("licenses", [])
            
            if licenses:
                # Create a dataframe for easier display
                license_data = []
                
                for license_info in licenses:
                    # Extract and format data
                    license_id = license_info.get("id", "")
                    license_type = license_info.get("type", "")
                    status = license_info.get("status", "")
                    holder_name = license_info.get("holder", {}).get("name", "")
                    issued_at = license_info.get("issued_at", "")
                    expires_at = license_info.get("expires_at", "")
                    
                    # Format dates
                    if issued_at:
                        try:
                            issued_date = datetime.fromisoformat(issued_at.replace('Z', '+00:00'))
                            issued_at = issued_date.strftime("%Y-%m-%d")
                        except:
                            pass
                    
                    if expires_at:
                        try:
                            expires_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                            expires_at = expires_date.strftime("%Y-%m-%d")
                        except:
                            pass
                    
                    # Add to data list
                    license_data.append({
                        "License ID": license_id,
                        "Type": license_type,
                        "Status": status,
                        "Holder": holder_name,
                        "Issued": issued_at,
                        "Expires": expires_at
                    })
                
                # Create and display dataframe
                if license_data:
                    df = pd.DataFrame(license_data)
                    st.dataframe(df, use_container_width=True)
                
                # Display license cards for a more visual representation
                st.subheader("License Cards")
                
                for license_info in licenses:
                    # Extract data
                    license_id = license_info.get("id", "")
                    license_type = license_info.get("type", "").capitalize()
                    status = license_info.get("status", "")
                    holder_name = license_info.get("holder", {}).get("name", "")
                    expires_at = license_info.get("expires_at", "")
                    
                    # Format date
                    if expires_at:
                        try:
                            expires_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                            expires_at = expires_date.strftime("%Y-%m-%d")
                        except:
                            pass
                    
                    # Divine alignment
                    divine_verification = license_info.get("divine_verification", {})
                    alignment_score = divine_verification.get("alignment_score", 0)
                    
                    # Create status badge
                    status_badge = f'<span class="status-badge {status}-badge">{status.upper()}</span>'
                    
                    # Display license card
                    st.markdown(f"""
                    <div class="license-card">
                        <h3>{license_type} License</h3>
                        <p><strong>ID:</strong> {license_id}</p>
                        <p><strong>Status:</strong> {status_badge}</p>
                        <p><strong>Holder:</strong> {holder_name}</p>
                        <p><strong>Expires:</strong> {expires_at}</p>
                        <div class="divine-alignment">
                            <p><strong>Divine Alignment:</strong> {alignment_score}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No licenses found in the system.")

def render_divine_governance():
    """Render the divine governance section"""
    st.header("Divine Governance")
    
    # Create tabs for different sections
    governance_tab, scorecard_tab = st.tabs(["Governance Overview", "Divine Scorecard"])
    
    with governance_tab:
        # Fetch divine governance information
        with st.spinner("Loading divine governance information..."):
            governance = get_divine_governance()
            
            if "error" in governance:
                st.error(f"Failed to load divine governance information: {governance['error']}")
            else:
                # Display governance levels
                st.subheader("Governance Levels")
                
                levels = governance.get("governance_levels", [])
                if levels:
                    for level in levels:
                        st.markdown(f"- **{level.capitalize()}**")
                
                # Display divine principles
                st.subheader("Divine Principles")
                
                principles = governance.get("divine_principles", [])
                if principles:
                    for principle in principles:
                        name = principle.get("name", "")
                        description = principle.get("description", "")
                        
                        with st.expander(f"{name}: {description}"):
                            st.markdown(f"**Purpose:** {principle.get('purpose', 'N/A')}")
                            
                            # Display factors
                            factors = principle.get("factors", [])
                            if factors:
                                st.markdown("**Evaluation Factors:**")
                                for factor in factors:
                                    factor_name = factor.get("name", "")
                                    factor_weight = factor.get("weight", 0)
                                    factor_desc = factor.get("description", "")
                                    st.markdown(f"- **{factor_name}** (Weight: {factor_weight:.2f}): {factor_desc}")
                
                # Display governance metrics
                st.subheader("Governance Metrics")
                
                min_alignment = governance.get("min_divine_alignment", 0)
                st.markdown(f"**Minimum Divine Alignment Required:** {min_alignment}%")
                st.progress(min_alignment / 100)
                
                verification_interval = governance.get("verification_interval", 0)
                if verification_interval:
                    hours = verification_interval / 3600
                    st.markdown(f"**Verification Interval:** {hours:.1f} hours")
                
                # Divine governance visualization
                st.subheader("Divine Governance Visualization")
                
                # Create radar chart data for divine principles
                if principles:
                    # Prepare data for radar chart
                    categories = [p.get("name", "") for p in principles]
                    values = [p.get("base_score", 85) for p in principles]
                    
                    # Create dataframe
                    df = pd.DataFrame({
                        'Category': categories,
                        'Value': values
                    })
                    
                    # Create and display chart using plotly
                    fig = px.line_polar(df, r='Value', theta='Category', line_close=True)
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )
                        ),
                        title="Divine Governance Principles",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    with scorecard_tab:
        st.subheader("Divine Principles Scorecard")
        st.markdown("""
        The Divine Principles Scorecard provides a detailed evaluation of a license against
        the divine governance principles. It measures alignment with ethical business practices
        and provides recommendations for improvement.
        """)
        
        # License ID input for scorecard
        scorecard_license_id = st.text_input("License ID", 
                                             value=st.session_state.license_id if 'license_id' in st.session_state else "")
        
        # Create columns for action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            view_scorecard = st.button("View Scorecard")
        with col2:
            save_scorecard_btn = st.button("Save Scorecard to File")
        
        # View scorecard
        if view_scorecard and scorecard_license_id:
            with st.spinner("Loading divine scorecard..."):
                scorecard_data = get_divine_scorecard(scorecard_license_id)
                
                if "error" in scorecard_data:
                    st.error(f"Failed to load scorecard: {scorecard_data['error']}")
                else:
                    st.success(f"Divine Principles Scorecard for License: {scorecard_data.get('license_id', scorecard_license_id)}")
                    st.markdown(f"**License Type:** {scorecard_data.get('license_type', 'N/A')}")
                    st.markdown(f"**Holder:** {scorecard_data.get('holder_name', 'N/A')}")
                    
                    # Display overall score
                    overall_score = scorecard_data.get('overall_score', 0)
                    st.markdown(f"**Overall Divine Alignment Score: {overall_score:.2f}%**")
                    st.progress(overall_score / 100)
                    
                    # Create scorecard visualization
                    principle_scores = scorecard_data.get('principle_scores', [])
                    
                    if principle_scores:
                        # Create radar chart for principle scores
                        categories = [p.get('principle_name', p.get('principle_id', 'Unknown')) for p in principle_scores]
                        values = [p.get('overall_score', 0) for p in principle_scores]
                        
                        # Create figure
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name='License Alignment'
                        ))
                        
                        # Update layout
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100]
                                )
                            ),
                            showlegend=False,
                            height=500,
                            title="Divine Principles Alignment"
                        )
                        
                        # Display the chart
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display detailed principle scores
                        st.subheader("Detailed Principle Scores")
                        
                        # Create columns for metrics
                        metric_cols = st.columns(len(principle_scores))
                        
                        # Display metrics for each principle
                        for i, (col, principle) in enumerate(zip(metric_cols, principle_scores)):
                            principle_name = principle.get('principle_name', principle.get('principle_id', 'Unknown'))
                            principle_score = principle.get('overall_score', 0)
                            col.metric(label=principle_name, value=f"{principle_score:.1f}%")
                        
                        # Display detailed information for each principle
                        for principle in principle_scores:
                            principle_name = principle.get('principle_name', principle.get('principle_id', 'Unknown'))
                            principle_score = principle.get('overall_score', 0)
                            principle_desc = principle.get('description', '')
                            
                            with st.expander(f"{principle_name} - {principle_score:.2f}%"):
                                st.markdown(f"**Description:** {principle_desc}")
                                
                                # Get factor scores
                                factors = principle.get('factors', [])
                                if factors:
                                    # Create a bar chart for factor scores
                                    factor_names = [f.get('name', 'Unknown') for f in factors]
                                    factor_scores = [f.get('score', 0) for f in factors]
                                    factor_weights = [f.get('weight', 0) for f in factors]
                                    
                                    # Create horizontal bar chart
                                    fig = go.Figure()
                                    
                                    fig.add_trace(go.Bar(
                                        x=factor_scores,
                                        y=factor_names,
                                        orientation='h',
                                        text=[f"{s:.1f}%" for s in factor_scores],
                                        marker_color='rgb(26, 118, 255)',
                                        textposition='auto'
                                    ))
                                    
                                    # Update layout
                                    fig.update_layout(
                                        title=f"Factor Scores for {principle_name}",
                                        yaxis_title="Factors",
                                        xaxis_title="Score (%)",
                                        xaxis=dict(range=[0, 100]),
                                        height=300
                                    )
                                    
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    # Show factor details as a table
                                    factor_data = []
                                    for factor in factors:
                                        factor_data.append({
                                            "Factor": factor.get('name', 'Unknown'),
                                            "Score": f"{factor.get('score', 0):.2f}%",
                                            "Weight": f"{factor.get('weight', 0):.2f}"
                                        })
                                    
                                    if factor_data:
                                        st.dataframe(pd.DataFrame(factor_data))
                        
                        # Display recommendations if available
                        recommendations = scorecard_data.get('recommendations', [])
                        if recommendations:
                            st.subheader("Improvement Recommendations")
                            
                            for recommendation in recommendations:
                                rec_principle = recommendation.get('principle_id', 'Unknown')
                                rec_factor = recommendation.get('factor', 'Unknown')
                                rec_text = recommendation.get('text', '')
                                
                                st.markdown(f"**{rec_principle} - {rec_factor}:** {rec_text}")
        
        # Save scorecard to file
        if save_scorecard_btn and scorecard_license_id:
            with st.spinner("Saving divine scorecard..."):
                save_result = save_divine_scorecard(scorecard_license_id)
                
                if "error" in save_result:
                    st.error(f"Failed to save scorecard: {save_result['error']}")
                else:
                    save_path = save_result.get('path', 'Unknown location')
                    st.success(f"Scorecard saved to {save_path}")

# Main application
def main():
    """Main application"""
    # Apply CSS
    local_css()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main content tabs
    tabs = st.tabs([
        "License Creation",
        "License Management",
        "License Verification",
        "License Directory",
        "Divine Governance"
    ])
    
    # Populate each tab
    with tabs[0]:
        render_license_creation()
    
    with tabs[1]:
        render_license_management()
    
    with tabs[2]:
        render_license_verification()
    
    with tabs[3]:
        render_license_directory()
    
    with tabs[4]:
        render_divine_governance()

if __name__ == "__main__":
    main()