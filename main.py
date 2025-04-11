import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
import uuid

st.set_page_config(
    page_title="Genesis WTO License Launcher",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .divine-alignment-high {
        color: #059669;
        font-weight: bold;
    }
    .divine-alignment-medium {
        color: #D97706;
        font-weight: bold;
    }
    .divine-alignment-low {
        color: #DC2626;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Logo and header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 class='main-header'>Genesis WTO License Launcher</h1>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### Genesis Navigation")
    page = st.radio(
        "Select Page",
        ["Entity Onboarding", "License Issuance", "WTO Compliance", "Deployment Dashboard"]
    )
    
    st.markdown("---")
    st.markdown("### Authentication")
    ecg_key = st.text_input("ECG Key", type="password", value="emperorkey123")

# Load HSN codes and WTO regions
def load_wto_regions():
    return {
        "REG-EU": {"name": "EU", "factor": 0.98, "protocol": "GDPR + EU Digital Services Act", "multiplier": 1.25},
        "REG-APAC": {"name": "APAC", "factor": 0.92, "protocol": "Pan-Asia Trade Framework", "multiplier": 1.35},
        "REG-SAARC": {"name": "SAARC", "factor": 0.94, "protocol": "South Asian Preferential Trading Arrangement", "multiplier": 1.15},
        "REG-AM": {"name": "Americas", "factor": 0.95, "protocol": "North American Free Trade Agreement", "multiplier": 1.10},
        "REG-ME": {"name": "Middle East", "factor": 0.90, "protocol": "GCC Trade Framework", "multiplier": 1.30},
        "REG-AF": {"name": "Africa", "factor": 0.96, "protocol": "African Continental Free Trade Area", "multiplier": 1.05}
    }

def load_hsn_codes():
    return {
        "HSN-GEN-10-01-B": "Core Infrastructure (Basic)",
        "HSN-GEN-10-02-S": "Core Infrastructure (Standard)",
        "HSN-GEN-10-03-P": "Core Infrastructure (Premium)",
        "HSN-GEN-10-04-E": "Core Infrastructure (Enterprise)",
        "HSN-GEN-20-01-B": "License Services (Basic)",
        "HSN-GEN-20-02-S": "License Services (Standard)",
        "HSN-GEN-20-03-P": "License Services (Premium)",
        "HSN-GEN-20-04-E": "License Services (Enterprise)",
        "HSN-GEN-30-01-B": "Entity Services (Basic)",
        "HSN-GEN-30-02-S": "Entity Services (Standard)",
        "HSN-GEN-30-03-P": "Entity Services (Premium)",
        "HSN-GEN-30-04-E": "Entity Services (Enterprise)",
        "HSN-GEN-40-01-B": "NPU Services (Basic - Shared)",
        "HSN-GEN-40-02-S": "NPU Services (Standard - Dedicated)",
        "HSN-GEN-40-03-P": "NPU Services (Premium - Cluster)",
        "HSN-GEN-40-04-E": "NPU Services (Enterprise - Custom)",
        "HSN-GEN-60-01-B": "Virtual Silk Road (Basic)",
        "HSN-GEN-60-02-S": "Virtual Silk Road (Standard)",
        "HSN-GEN-60-03-P": "Virtual Silk Road (Premium)",
        "HSN-GEN-60-04-E": "Virtual Silk Road (Enterprise)",
        "HSN-GEN-70-07-S": "Multi-Region Deployment",
        "HSN-GEN-70-08-P": "High-Availability Config",
        "HSN-GEN-70-09-E": "Divine Convergence Ready"
    }

wto_regions = load_wto_regions()
hsn_codes = load_hsn_codes()

# Entity Onboarding
if page == "Entity Onboarding":
    st.markdown("<h2 class='sub-header'>Entity Onboarding</h2>", unsafe_allow_html=True)
    
    # Basic entity information
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Basic Entity Information")
    col1, col2 = st.columns(2)
    with col1:
        legal_name = st.text_input("Legal Entity Name", "Voi Jeans Retail India Pvt Ltd")
        entity_type = st.selectbox("Entity Type", ["IP_HOLDER", "MANUFACTURER", "DISTRIBUTOR", "RETAILER", "GOVERNANCE_PROVIDER"])
    with col2:
        jurisdiction = st.text_input("Jurisdiction (Country)", "India")
        region_block = st.selectbox("WTO Region Block", list(wto_regions.keys()), format_func=lambda x: wto_regions[x]["name"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Governance and license information
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Governance & License Information")
    col1, col2 = st.columns(2)
    with col1:
        governance_class = st.selectbox("Governance Class", ["BASIC", "STANDARD", "PREMIUM", "ENTERPRISE", "EMPEROR"])
        divine_alignment = st.slider("Initial Divine Alignment Factor", 0.0, 1.0, 0.92, 0.01)
    with col2:
        license_tier = st.selectbox("License Tier", ["BASIC", "STANDARD", "PREMIUM", "ENTERPRISE"])
        wto_protocol = st.text_input("WTO Compliance Protocol", wto_regions[region_block]["protocol"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Relationship information (optional)
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Entity Relationships (Optional)")
    has_relationship = st.checkbox("Add Entity Relationship")
    if has_relationship:
        col1, col2 = st.columns(2)
        with col1:
            related_entity = st.text_input("Related Entity ID", "ENT-SCOTTS-APAC-25002")
            relationship_type = st.selectbox("Relationship Type", ["SUPPLIER_TO", "DISTRIBUTOR_FOR", "GOVERNANCE_PROVIDER_TO", "BRAND_OWNER_TO_MANUFACTURER"])
        with col2:
            contract_id = st.text_input("Contract ID", f"CONTRACT-{uuid.uuid4().hex[:8].upper()}")
            init_date = st.date_input("Relationship Start Date", datetime.now())
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Onboard entity
    if st.button("Onboard Entity"):
        entity_id = f"ENT-{legal_name.split()[0].upper()}-{wto_regions[region_block]['name']}-{datetime.now().strftime('%y%d')}"
        entity_data = {
            "entity_id": entity_id,
            "legal_name": legal_name,
            "entity_type": entity_type,
            "jurisdiction": jurisdiction,
            "region_block": wto_regions[region_block]["name"],
            "region_code": region_block,
            "wto_compliance": wto_protocol,
            "divine_alignment_factor": divine_alignment,
            "governance_class": governance_class,
            "license_tier": license_tier
        }
        
        if has_relationship:
            entity_data["relationships"] = [
                {
                    "entity_id": related_entity,
                    "relationship_type": relationship_type,
                    "contract_id": contract_id,
                    "initialized_date": init_date.strftime("%Y-%m-%d")
                }
            ]
        
        # Save entity data (in a real app)
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.markdown(f"### Entity Successfully Onboarded!")
        st.markdown(f"**Entity ID:** {entity_id}")
        st.markdown(f"**Entity Name:** {legal_name}")
        st.markdown(f"**Region:** {wto_regions[region_block]['name']}")
        st.markdown(f"**Divine Alignment:** {divine_alignment:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.json(entity_data)

# License Issuance
elif page == "License Issuance":
    st.markdown("<h2 class='sub-header'>License Issuance</h2>", unsafe_allow_html=True)
    
    # Sample entities for demo
    entities = {
        "ENT-VOI-APAC-25001": {
            "entity_id": "ENT-VOI-APAC-25001",
            "legal_name": "Voi Jeans Retail India Pvt Ltd",
            "region_code": "REG-APAC"
        },
        "ENT-SCOTTS-APAC-25002": {
            "entity_id": "ENT-SCOTTS-APAC-25002",
            "legal_name": "Scotts Garments Ltd",
            "region_code": "REG-SAARC"
        }
    }
    
    # License information
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### License Information")
    col1, col2 = st.columns(2)
    with col1:
        entity_id = st.selectbox("Entity", list(entities.keys()), format_func=lambda x: f"{x} ({entities[x]['legal_name']})")
        license_components = st.multiselect("HSN Components", list(hsn_codes.keys()), 
                                         format_func=lambda x: f"{x} - {hsn_codes[x]}", 
                                         default=["HSN-GEN-10-03-P", "HSN-GEN-20-03-P", "HSN-GEN-60-03-P"])
    with col2:
        user_count = st.number_input("User Count", min_value=10, value=250)
        npu_count = st.number_input("NPU Count", min_value=1, value=3)
        duration = st.selectbox("License Duration", ["monthly", "annual", "triennial", "perpetual"])
    
    # WTO region information
    selected_entity = entities[entity_id]
    region_code = selected_entity.get("region_code", "REG-APAC")
    region_info = wto_regions.get(region_code, wto_regions["REG-APAC"])
    
    st.markdown("### WTO Region Information")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Region Block:** {region_info['name']}")
        st.markdown(f"**Compliance Protocol:** {region_info['protocol']}")
    with col2:
        st.markdown(f"**Divine Alignment Factor:** {region_info['factor']}")
        st.markdown(f"**Region Multiplier:** {region_info['multiplier']}")
    
    # Calculate pricing
    base_price = sum([float(component.split('-')[3][0]) * 0.25 for component in license_components])
    user_scale = user_count * 0.00003
    npu_scale = npu_count * 0.1
    region_multiplier = region_info['multiplier']
    
    duration_multiplier = {
        "monthly": 1,
        "annual": 10,
        "triennial": 25,
        "perpetual": 40
    }[duration]
    
    raw_price = (base_price + user_scale + npu_scale) * region_multiplier * duration_multiplier
    
    # Apply divine alignment discount
    divine_discount = (region_info['factor'] - 0.8) * 20  # 0-20% discount based on alignment
    final_price = raw_price * (1 - divine_discount / 100)
    
    st.markdown("### Pricing Calculation")
    st.markdown(f"**Base Price:** ₿ {base_price:.2f}")
    st.markdown(f"**User Scaling:** ₿ {user_scale:.2f}")
    st.markdown(f"**NPU Scaling:** ₿ {npu_scale:.2f}")
    st.markdown(f"**Region Multiplier:** {region_multiplier:.2f}")
    st.markdown(f"**Duration Multiplier:** {duration_multiplier:.0f}x")
    st.markdown(f"**Divine Alignment Discount:** {divine_discount:.1f}%")
    st.markdown(f"**Final Price:** ₿ {final_price:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Issue license
    if st.button("Issue License"):
        license_key = f"SYN-{selected_entity['legal_name'].split()[0].upper()}-{region_info['name']}-{datetime.now().strftime('%y%m')}-{''.join(['BSPE'[min(3, int(c[8]) - 1)] for c in license_components[:3]])}"
        
        # Prepare manifest data
        issue_date = datetime.now()
        if duration == "monthly":
            expiry = issue_date + timedelta(days=30)
        elif duration == "annual":
            expiry = issue_date + timedelta(days=365)
        elif duration == "triennial":
            expiry = issue_date + timedelta(days=365*3)
        else:  # perpetual
            expiry = issue_date + timedelta(days=365*10)  # 10 years for perpetual
            
        manifest_id = f"GEN-MANIFEST-{selected_entity['legal_name'].split()[0].upper()}-{uuid.uuid4().hex[:4].upper()}"
        deployment_id = f"{selected_entity['legal_name'].split()[0].upper()}-DEPLOY-{datetime.now().strftime('%y%d')}"
        
        # Build manifest
        manifest = {
            "manifest_id": manifest_id,
            "client_id": entity_id,
            "deployment_id": deployment_id,
            "license_key": license_key,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "expiration_date": expiry.strftime("%Y-%m-%d"),
            "wto_region": {
                "region_block": region_info['name'],
                "country": selected_entity.get('jurisdiction', 'India'), # Default for demo
                "wto_compliance": region_info['protocol'],
                "divine_alignment_factor": region_info['factor'],
                "region_code": region_code
            },
            "components": [],
            "subtotal": raw_price,
            "divine_alignment_discount_rate": divine_discount / 100,
            "divine_alignment_discount_amount": raw_price * (divine_discount / 100),
            "total_price": final_price,
            "currency": "BTC",
            "divine_alignment_factor": region_info['factor']
        }
        
        # Add components
        for component in license_components:
            base = float(component.split('-')[3][0]) * 0.25
            tier = component.split('-')[3][1]
            tier_name = {"B": "Basic", "S": "Standard", "P": "Premium", "E": "Enterprise"}[tier]
            
            manifest["components"].append({
                "hsn_code": component,
                "component_name": hsn_codes[component],
                "tier": tier_name,
                "quantity": 1,
                "base_price": base,
                "user_count": user_count,
                "user_scaling_price": user_count * 0.00001,
                "npu_count": npu_count,
                "npu_scaling_price": npu_count * 0.03,
                "region": f"AWS-{region_info['name']}",
                "region_multiplier": region_multiplier,
                "duration": duration,
                "duration_multiplier": duration_multiplier,
                "total_component_price": (base + (user_count * 0.00001) + (npu_count * 0.03)) * region_multiplier * duration_multiplier
            })
        
        st.markdown("<div class='success-box'>", unsafe_allow_html=True)
        st.markdown(f"### License Successfully Issued!")
        st.markdown(f"**License Key:** {license_key}")
        st.markdown(f"**Manifest ID:** {manifest_id}")
        st.markdown(f"**Entity:** {selected_entity['legal_name']}")
        st.markdown(f"**Expiration:** {expiry.strftime('%Y-%m-%d')}")
        st.markdown(f"**Total Price:** ₿ {final_price:.2f}")
        
        # Display license manifest
        with st.expander("View License Manifest"):
            st.json(manifest)
        
        # Mock download buttons
        st.download_button(
            label="Download License Manifest",
            data=json.dumps(manifest, indent=2),
            file_name=f"{manifest_id}.json",
            mime="application/json"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

# WTO Compliance
elif page == "WTO Compliance":
    st.markdown("<h2 class='sub-header'>WTO Compliance Dashboard</h2>", unsafe_allow_html=True)
    
    # Region selection
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Regional Compliance Overview")
    selected_region = st.selectbox("Select WTO Region", list(wto_regions.keys()), 
                                 format_func=lambda x: wto_regions[x]["name"])
    region_info = wto_regions[selected_region]
    
    # Display region info
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Region Name:** {region_info['name']}")
        st.markdown(f"**Compliance Protocol:** {region_info['protocol']}")
        st.markdown(f"**Region Multiplier:** {region_info['multiplier']}")
    with col2:
        st.markdown(f"**Divine Alignment Factor:** {region_info['factor']}")
        st.markdown(f"**Trade Agreement Status:** Active")
        st.markdown(f"**Last TPR Update:** 2025-01-15")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Compliance requirements
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Compliance Requirements")
    
    # Create sample compliance data
    compliance_data = {
        "REG-EU": [
            {"requirement": "GDPR Compliance", "status": "Required", "impact": "High"},
            {"requirement": "Digital Services Act", "status": "Required", "impact": "High"},
            {"requirement": "AI Act Compliance", "status": "Required", "impact": "Medium"},
            {"requirement": "Environmental Reporting", "status": "Required", "impact": "Medium"},
            {"requirement": "Digital Markets Act", "status": "Conditional", "impact": "High"}
        ],
        "REG-APAC": [
            {"requirement": "GST Compliance", "status": "Required", "impact": "High"},
            {"requirement": "RBI Export Regulation", "status": "Required", "impact": "High"},
            {"requirement": "Data Localization", "status": "Required", "impact": "Medium"},
            {"requirement": "Digital Services Tax", "status": "Conditional", "impact": "Medium"},
            {"requirement": "Cross-Border Data Transfer", "status": "Required", "impact": "High"}
        ],
        "REG-SAARC": [
            {"requirement": "SAFTA Rules of Origin", "status": "Required", "impact": "High"},
            {"requirement": "LDC Preferential Treatment", "status": "Conditional", "impact": "High"},
            {"requirement": "Bangladesh Export Protocol", "status": "Required", "impact": "Medium"},
            {"requirement": "Regional Value Content", "status": "Required", "impact": "Medium"},
            {"requirement": "Certificate of Origin", "status": "Required", "impact": "High"}
        ],
        "REG-AM": [
            {"requirement": "USMCA Compliance", "status": "Required", "impact": "High"},
            {"requirement": "Digital Trade Provisions", "status": "Required", "impact": "Medium"},
            {"requirement": "Labor Value Content", "status": "Conditional", "impact": "Medium"},
            {"requirement": "Environmental Standards", "status": "Required", "impact": "Low"},
            {"requirement": "Rules of Origin", "status": "Required", "impact": "High"}
        ],
        "REG-ME": [
            {"requirement": "GCC Technical Regulations", "status": "Required", "impact": "High"},
            {"requirement": "Halal Certification", "status": "Conditional", "impact": "Medium"},
            {"requirement": "VAT Compliance", "status": "Required", "impact": "High"},
            {"requirement": "Digital Content Restrictions", "status": "Required", "impact": "Medium"},
            {"requirement": "Local Agent Requirement", "status": "Required", "impact": "High"}
        ],
        "REG-AF": [
            {"requirement": "AfCFTA Compliance", "status": "Required", "impact": "High"},
            {"requirement": "Rules of Origin", "status": "Required", "impact": "High"},
            {"requirement": "Trade Facilitation", "status": "Required", "impact": "Medium"},
            {"requirement": "Digital Trade Protocol", "status": "Pending", "impact": "Medium"},
            {"requirement": "Local Content Requirements", "status": "Conditional", "impact": "Medium"}
        ]
    }
    
    # Display compliance requirements
    df = pd.DataFrame(compliance_data[selected_region])
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WTO compliance simulator
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### WTO Compliance Simulator")
    col1, col2 = st.columns(2)
    with col1:
        source_region = st.selectbox("Source Region", list(wto_regions.keys()), 
                                   format_func=lambda x: wto_regions[x]["name"],
                                   index=list(wto_regions.keys()).index("REG-APAC"))
    with col2:
        target_region = st.selectbox("Target Region", list(wto_regions.keys()), 
                                   format_func=lambda x: wto_regions[x]["name"],
                                   index=list(wto_regions.keys()).index("REG-SAARC"))
    
    product_type = st.selectbox("Product Type", ["Digital Services", "Software Licenses", "Physical Goods", "Intellectual Property"])
    
    if st.button("Simulate Trade Compliance"):
        # Generate simulated compliance results
        source_name = wto_regions[source_region]["name"]
        target_name = wto_regions[target_region]["name"]
        
        st.markdown(f"### Compliance Results: {source_name} to {target_name}")
        
        # Trade allowance
        trade_allowed = True
        required_docs = [
            f"Certificate of Origin - Form {source_name}-{target_name}",
            "Commercial Invoice",
            "Packing List",
            "Bill of Lading/Airway Bill"
        ]
        
        if source_region == "REG-EU" and target_region in ["REG-APAC", "REG-SAARC"]:
            required_docs.append("GDPR Data Transfer Agreement")
            required_docs.append("Digital Services Tax Declaration")
            
        if source_region == "REG-APAC" and target_region == "REG-SAARC":
            required_docs.append("SAFTA Rules of Origin Certificate")
            required_docs.append("Bangladesh Export Protocol Compliance")
        
        # Tariff rates
        tariff_rate = 0.0
        if source_region != target_region:
            base_tariff = 5.0
            if (source_region == "REG-EU" and target_region == "REG-AM") or (source_region == "REG-AM" and target_region == "REG-EU"):
                tariff_rate = 2.5  # Reduced tariff between EU and Americas
            elif source_region == "REG-APAC" and target_region == "REG-SAARC":
                tariff_rate = 1.5  # Reduced tariff within Asia
            elif source_region == "REG-SAARC":
                tariff_rate = 0.0  # LDC preference
            else:
                tariff_rate = base_tariff
        
        # Display results
        st.markdown(f"**Trade Allowed:** {'Yes' if trade_allowed else 'No'}")
        st.markdown(f"**Tariff Rate:** {tariff_rate}%")
        st.markdown("**Required Documentation:**")
        for doc in required_docs:
            st.markdown(f"- {doc}")
            
        # Alignment impact
        source_factor = wto_regions[source_region]["factor"]
        target_factor = wto_regions[target_region]["factor"]
        alignment_impact = (source_factor + target_factor) / 2
        
        alignment_class = "high" if alignment_impact > 0.95 else "medium" if alignment_impact > 0.9 else "low"
        st.markdown(f"**Divine Alignment Impact:** <span class='divine-alignment-{alignment_class}'>{alignment_impact:.2f}</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Deployment Dashboard
elif page == "Deployment Dashboard":
    st.markdown("<h2 class='sub-header'>Deployment Dashboard</h2>", unsafe_allow_html=True)
    
    # Deployment controls
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Deployment Controls")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Deploy ECG Governance", key="deploy_ecg"):
            st.success("ECG Governance deployment initiated!")
        if st.button("Deploy Voi Jeans", key="deploy_voi"):
            st.success("Voi Jeans deployment initiated!")
        if st.button("Deploy Scotts Garments", key="deploy_scotts"):
            st.success("Scotts Garments deployment initiated!")
    with col2:
        if st.button("Restart License API", key="restart_license"):
            st.success("License API restart initiated!")
        if st.button("Restart HSN Registry", key="restart_hsn"):
            st.success("HSN Registry restart initiated!")
        if st.button("Restart NPU Coordinator", key="restart_npu"):
            st.success("NPU Coordinator restart initiated!")
    with col3:
        if st.button("Verify All Licenses", key="verify_licenses"):
            st.success("License verification initiated!")
        if st.button("Run WTO Compliance Check", key="wto_check"):
            st.success("WTO compliance check initiated!")
        if st.button("Generate Alignment Report", key="alignment_report"):
            st.success("Alignment report generation initiated!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Deployment Status
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Deployment Status")
    
    # Sample deployment data
    deployment_data = {
        "ecg-governance": {"status": "Running", "health": "Healthy", "uptime": "14d 7h 23m"},
        "voi-welcome-server": {"status": "Running", "health": "Healthy", "uptime": "7d 12h 45m"},
        "voi-license-api": {"status": "Running", "health": "Healthy", "uptime": "7d 12h 45m"},
        "voi-license-management": {"status": "Running", "health": "Healthy", "uptime": "7d 12h 45m"},
        "voi-inventory": {"status": "Running", "health": "Healthy", "uptime": "7d 12h 45m"},
        "scotts-welcome-server": {"status": "Running", "health": "Healthy", "uptime": "5d 8h 15m"},
        "scotts-license-api": {"status": "Running", "health": "Healthy", "uptime": "5d 8h 15m"},
        "scotts-license-management": {"status": "Running", "health": "Warning", "uptime": "5d 8h 15m"},
        "scotts-manufacturing": {"status": "Running", "health": "Healthy", "uptime": "5d 8h 15m"},
        "ecg-hsn-registry": {"status": "Running", "health": "Healthy", "uptime": "14d 7h 23m"},
        "ecg-governance-dashboard": {"status": "Running", "health": "Healthy", "uptime": "14d 7h 23m"},
        "npu-coordinator": {"status": "Running", "health": "Healthy", "uptime": "14d 7h 23m"}
    }
    
    # Create status dataframe
    df_status = pd.DataFrame([
        {
            "Container": name,
            "Status": data["status"],
            "Health": data["health"],
            "Uptime": data["uptime"]
        } for name, data in deployment_data.items()
    ])
    
    st.dataframe(df_status, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # License Status
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### License Status")
    
    # Sample license data
    license_data = [
        {"License Key": "SYN-VOI-APAC-2025-PPP", "Entity": "Voi Jeans Retail India Pvt Ltd", "Status": "Active", "Expiry": "2026-01-01", "Health": "Healthy"},
        {"License Key": "SYN-SCOTTS-SAARC-2025-SSS", "Entity": "Scotts Garments Ltd", "Status": "Active", "Expiry": "2026-01-10", "Health": "Warning"}
    ]
    
    df_licenses = pd.DataFrame(license_data)
    st.dataframe(df_licenses, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Docker Commands
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("### Docker Command Reference")
    
    st.code("""
# Deploy ECG Governance
docker-compose -f docker/docker-compose.ecg-governance.yml up -d

# Deploy Voi Jeans
docker-compose -f docker/docker-compose.voi-jeans.yml up -d

# Deploy Scotts Garments
docker-compose -f docker/docker-compose.scotts-garments.yml up -d

# Verify License
docker-compose exec ecg-hsn-registry python tools/verify_license.py --entity ENT-VOI-APAC-25001 --license-key SYN-VOI-APAC-2025-PPP

# Check Divine Alignment
docker-compose exec ecg-hsn-registry python tools/check_divine_alignment.py --entity ENT-VOI-APAC-25001
    """)
    
    # Deploy all button
    if st.button("DEPLOY COMPLETE GENESIS STACK", type="primary"):
        st.success("Full Genesis Stack deployment initiated!")
        st.info("This will deploy ECG, Voi Jeans, and Scotts Garments containers with their complete configurations.")
        st.balloons()
    
    st.markdown("</div>", unsafe_allow_html=True)