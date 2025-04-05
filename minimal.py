"""
Minimal Streamlit App - Empire OS
=================================

This is a minimal Streamlit application that serves as a template for Empire OS modules.
It includes basic styling, navigation components, and the core ECG license system integration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import sys
import os

# Add core directory to path
sys.path.append(os.path.abspath('.'))

# Import license API
try:
    from core.license_api import LicenseAPI
    license_api_available = True
except ImportError as e:
    print(f"License API import error: {e}")
    license_api_available = False

# Set page configuration
st.set_page_config(
    page_title="Empire OS - Minimal Template",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title
st.title("Empire OS - Minimal Template")
st.markdown("### A foundation for divine governance applications")

# Show license API status
if license_api_available:
    st.sidebar.success("✅ ECG License API is available")
else:
    st.sidebar.warning("⚠️ ECG License API is not available - Using simulation mode")

# Sidebar navigation
with st.sidebar:
    st.title("Empire OS")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["Home", "Dashboard", "License System", "Settings"]
    )
    st.markdown("---")
    st.markdown("#### Empire OS v1.0")
    st.markdown("Divine Mechanics Computational System")

# Display the selected page
if page == "Home":
    st.header("Welcome to Empire OS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Empire OS** is a unified enterprise governance platform implementing divine principles
        for sustainable and ethical organizational management.
        
        This minimal template provides the foundational components for building Empire OS modules.
        """)
        
        st.markdown("### Features")
        st.markdown("""
        - Integrated ECG License System
        - Divine Governance Framework
        - Interactive Data Visualization
        - Multi-dimensional Compliance Tracking
        """)
    
    with col2:
        # Create a simple visualization
        data = pd.DataFrame({
            'Dimension': ['People', 'Planet', 'Profit'],
            'Compliance': [85, 78, 92]
        })
        
        fig = px.bar(
            data, 
            x='Dimension', 
            y='Compliance',
            color='Compliance',
            color_continuous_scale=px.colors.sequential.Viridis,
            title="Divine Alignment by Dimension"
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric(
            label="Overall Divine Alignment",
            value="85%",
            delta="5%"
        )

elif page == "Dashboard":
    st.header("Dashboard")
    
    # Create a multi-column dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Active Licenses",
            value="124",
            delta="12"
        )
    
    with col2:
        st.metric(
            label="Compliance Rate",
            value="92%",
            delta="3%"
        )
    
    with col3:
        st.metric(
            label="Divine Alignment Score",
            value="85/100",
            delta="7"
        )
    
    # Create sample data for time series
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    compliance_data = pd.DataFrame({
        'Date': dates,
        'People': [random.randint(70, 95) for _ in range(len(dates))],
        'Planet': [random.randint(65, 90) for _ in range(len(dates))],
        'Profit': [random.randint(75, 98) for _ in range(len(dates))]
    })
    
    # Plot time series
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=compliance_data['Date'], y=compliance_data['People'], mode='lines', name='People'))
    fig.add_trace(go.Scatter(x=compliance_data['Date'], y=compliance_data['Planet'], mode='lines', name='Planet'))
    fig.add_trace(go.Scatter(x=compliance_data['Date'], y=compliance_data['Profit'], mode='lines', name='Profit'))
    
    fig.update_layout(
        title="Compliance Trends by Dimension",
        xaxis_title="Date",
        yaxis_title="Compliance Score",
        legend_title="Dimension",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # License distribution
    license_data = pd.DataFrame({
        'Type': ['Corporate', 'Government', 'Individual', 'Educational', 'Nonprofit'],
        'Count': [45, 12, 38, 18, 11]
    })
    
    fig = px.pie(
        license_data,
        values='Count',
        names='Type',
        title="License Distribution by Type",
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "License System":
    st.header("License System")
    
    tab1, tab2, tab3 = st.tabs(["Issue License", "Validate License", "Audit Compliance"])
    
    with tab1:
        st.markdown("### Issue New License")
        
        col1, col2 = st.columns(2)
        
        with col1:
            entity_name = st.text_input("Entity Name", "Voi Jeans Retail India Pvt Ltd")
            entity_id = st.text_input("Entity ID", "VOI-JEANS-001")
            license_type = st.selectbox(
                "License Type",
                ["corporate", "individual", "government", "nonprofit", "educational", "research", "developer"]
            )
        
        with col2:
            validity_days = st.slider("Validity (Days)", 30, 1095, 365)
            compliance_tier = st.selectbox(
                "Compliance Tier",
                ["tier_1", "tier_2", "tier_3", "tier_4", "tier_5"]
            )
        
        st.markdown("#### Authorized Modules")
        modules_col1, modules_col2, modules_col3 = st.columns(3)
        
        with modules_col1:
            module1 = st.checkbox("inventory_management", True)
            module2 = st.checkbox("supply_chain_optimization", True)
        
        with modules_col2:
            module3 = st.checkbox("retail_analytics", True)
            module4 = st.checkbox("manufacturing_insights", True)
        
        with modules_col3:
            module5 = st.checkbox("distribution_planning", True)
            module6 = st.checkbox("governance_framework", False)
        
        modules = []
        for module, checked in [
            ("inventory_management", module1),
            ("supply_chain_optimization", module2),
            ("retail_analytics", module3),
            ("manufacturing_insights", module4),
            ("distribution_planning", module5),
            ("governance_framework", module6)
        ]:
            if checked:
                modules.append(module)
        
        if st.button("Issue License"):
            if license_api_available:
                try:
                    # Use the actual license API to issue a license
                    license_result = LicenseAPI.issue_license(
                        entity_name=entity_name,
                        entity_id=entity_id,
                        license_type=license_type,
                        validity_days=validity_days,
                        compliance_tier=compliance_tier,
                        modules=modules
                    )
                    
                    st.success(f"License issued successfully for {entity_name}")
                    st.json(license_result)
                except Exception as e:
                    st.error(f"Failed to issue license: {str(e)}")
            else:
                # Fallback to simulation if license API is not available
                st.success(f"License issued successfully for {entity_name} (Simulation)")
                st.json({
                    "license_id": f"ECG-{random.randint(10000000, 99999999)}",
                    "entity_name": entity_name,
                    "entity_id": entity_id,
                    "license_type": license_type,
                    "issue_date": datetime.now().isoformat(),
                    "expiry_date": (datetime.now() + timedelta(days=validity_days)).isoformat(),
                    "compliance_tier": compliance_tier,
                    "authorized_modules": modules,
                    "note": "This is a simulated license as the ECG License API is not available"
                })
    
    with tab2:
        st.markdown("### Validate License")
        
        license_id = st.text_input("License ID", "ECG-1A2B3C4D")
        
        if st.button("Validate"):
            if license_api_available:
                try:
                    # Use the actual license API to validate a license
                    validation_result = LicenseAPI.validate_license(license_id)
                    
                    if validation_result.get("is_valid", False):
                        st.success("License is valid")
                    else:
                        st.error(f"License validation failed: {validation_result.get('message', 'Unknown error')}")
                    
                    st.json(validation_result)
                except Exception as e:
                    st.error(f"Failed to validate license: {str(e)}")
            else:
                # Fallback to simulation if license API is not available
                st.success("License is valid (Simulation)")
                st.json({
                    "license_id": license_id,
                    "is_valid": True,
                    "message": "License is valid",
                    "entity_name": "Voi Jeans Retail India Pvt Ltd",
                    "status": "active",
                    "compliance_score": 85.7,
                    "expiry_date": (datetime.now() + timedelta(days=300)).isoformat(),
                    "note": "This is a simulated validation as the ECG License API is not available"
                })
    
    with tab3:
        st.markdown("### Compliance Audit")
        
        license_id = st.text_input("License ID for Audit", "ECG-1A2B3C4D")
        auditor = st.text_input("Auditor", "Emperor's Governance Team")
        
        st.markdown("#### Dimension Scores")
        
        st.markdown("**People Dimension**")
        people_col1, people_col2, people_col3 = st.columns(3)
        with people_col1:
            justice_people = st.slider("Justice", 0, 100, 85, key="justice_people")
        with people_col2:
            mercy_people = st.slider("Mercy", 0, 100, 90, key="mercy_people")
        with people_col3:
            knowledge_people = st.slider("All-Knowing", 0, 100, 75, key="knowledge_people")
        
        st.markdown("**Planet Dimension**")
        planet_col1, planet_col2, planet_col3 = st.columns(3)
        with planet_col1:
            justice_planet = st.slider("Justice", 0, 100, 80, key="justice_planet")
        with planet_col2:
            mercy_planet = st.slider("Mercy", 0, 100, 85, key="mercy_planet")
        with planet_col3:
            knowledge_planet = st.slider("All-Knowing", 0, 100, 70, key="knowledge_planet")
        
        st.markdown("**Profit Dimension**")
        profit_col1, profit_col2, profit_col3 = st.columns(3)
        with profit_col1:
            justice_profit = st.slider("Justice", 0, 100, 90, key="justice_profit")
        with profit_col2:
            mercy_profit = st.slider("Mercy", 0, 100, 80, key="mercy_profit")
        with profit_col3:
            knowledge_profit = st.slider("All-Knowing", 0, 100, 85, key="knowledge_profit")
        
        findings = st.text_area(
            "Findings",
            """Strong commitment to ethical labor practices
Environmental initiatives exceed industry standards
Profit sharing mechanisms align with justice principles"""
        )
        
        recommendations = st.text_area(
            "Recommendations",
            """Enhance data collection for better visibility
Implement advanced training on divine principles
Extend governance practices to supplier network"""
        )
        
        if st.button("Submit Audit"):
            dimension_scores = {
                "people": {
                    "justice": float(justice_people),
                    "mercy": float(mercy_people),
                    "all_knowing": float(knowledge_people)
                },
                "planet": {
                    "justice": float(justice_planet),
                    "mercy": float(mercy_planet),
                    "all_knowing": float(knowledge_planet)
                },
                "profit": {
                    "justice": float(justice_profit),
                    "mercy": float(mercy_profit),
                    "all_knowing": float(knowledge_profit)
                }
            }
            
            findings_list = findings.split("\n")
            recommendations_list = recommendations.split("\n")
            
            if license_api_available:
                try:
                    # Use the actual license API to perform an audit
                    audit_result = LicenseAPI.perform_audit(
                        license_id=license_id,
                        auditor=auditor,
                        dimension_scores=dimension_scores,
                        findings=findings_list,
                        recommendations=recommendations_list
                    )
                    
                    st.success(f"Compliance audit submitted for {license_id}")
                    st.json(audit_result)
                except Exception as e:
                    st.error(f"Failed to perform compliance audit: {str(e)}")
            else:
                # Fallback to simulation if license API is not available
                # Calculate overall score
                all_scores = []
                for dimension in dimension_scores.values():
                    for score in dimension.values():
                        all_scores.append(score)
                
                overall_score = sum(all_scores) / len(all_scores)
                
                st.success(f"Compliance audit submitted for {license_id} (Simulation)")
                st.json({
                    "audit_id": f"AUDIT-{random.randint(10000000, 99999999)}",
                    "license_id": license_id,
                    "auditor": auditor,
                    "timestamp": datetime.now().isoformat(),
                    "overall_score": round(overall_score, 2),
                    "dimension_scores": dimension_scores,
                    "findings": findings_list,
                    "recommendations": recommendations_list,
                    "note": "This is a simulated audit as the ECG License API is not available"
                })

elif page == "Settings":
    st.header("Settings")
    
    st.markdown("### System Configuration")
    
    st.checkbox("Enable Dark Mode", False)
    st.checkbox("Enable Real-time Notifications", True)
    st.checkbox("Automatic Compliance Audits", True)
    
    st.markdown("### User Preferences")
    
    theme = st.selectbox(
        "UI Theme",
        ["Default", "Dark", "Light", "Emperor"]
    )
    
    dashboard_refresh = st.selectbox(
        "Dashboard Refresh Rate",
        ["30 seconds", "1 minute", "5 minutes", "15 minutes", "30 minutes", "1 hour"]
    )
    
    st.radio(
        "Default Visualization Type",
        ["Interactive", "Static", "Tabular"]
    )
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully")

# Footer
st.markdown("---")
st.markdown("Empire OS - The Divine Mechanics Computational System © 2025")