"""
License Management Interface for Genesis Dashboard

This module provides the Streamlit interface for creating, managing, and validating
licenses within the Empire OS ecosystem.
"""

import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_BASE_URL = "http://localhost:5001"
API_KEY = os.getenv("EMPIRE_API_KEY", "emperorkey123")  # Default for testing

# API request headers
HEADERS = {"x-api-key": API_KEY}

def show_license_management():
    """Display the license management interface"""
    st.markdown('<h1 class="divine-header">Empire License Management</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Sovereign License Management Console</h3>', unsafe_allow_html=True)
    
    # Create tabs for different license functions
    tabs = st.tabs(["License Dashboard", "License Builder", "License Validation", "License Audit", "Divine Alignment", "Genesis Vision"])
    
    with tabs[0]:
        show_license_dashboard()
    
    with tabs[1]:
        show_license_builder()
    
    with tabs[2]:
        show_license_validation()
    
    with tabs[3]:
        show_license_audit()
    
    with tabs[4]:
        show_divine_alignment()
        
    with tabs[5]:
        show_genesis_vision()


def show_license_dashboard():
    """Display the license dashboard with key metrics and visualizations"""
    st.markdown("### License Dashboard")
    
    # Attempt to fetch license data
    try:
        response = requests.get(f"{API_BASE_URL}/api/license/list", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            licenses = data.get("licenses", {})
            assignments = data.get("assignments", {})
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Licenses", len(licenses))
            
            with col2:
                active_count = sum(1 for lic in licenses.values() if lic.get("status") == "active")
                st.metric("Active Licenses", f"{active_count}/{len(licenses)}")
            
            with col3:
                st.metric("License Assignments", len(assignments))
            
            # Display license table
            if licenses:
                st.markdown("### Active Licenses")
                
                # Convert to a list of dictionaries for pandas
                licenses_list = []
                for license_id, lic_data in licenses.items():
                    licenses_list.append({
                        "License ID": license_id,
                        "Brand": lic_data.get("brand", "N/A"),
                        "Region": lic_data.get("region", "Global"),
                        "Status": lic_data.get("status", "Unknown"),
                        "Role Type": lic_data.get("role_map", {}).get("role_type", "None"),
                        "Modules": ", ".join(lic_data.get("modules", []))
                    })
                
                df_licenses = pd.DataFrame(licenses_list)
                st.dataframe(df_licenses, use_container_width=True)
                
                # Create a visualization of modules distribution
                all_modules = []
                for lic_data in licenses.values():
                    all_modules.extend(lic_data.get("modules", []))
                
                if all_modules:
                    module_counts = {}
                    for module in all_modules:
                        module_counts[module] = module_counts.get(module, 0) + 1
                    
                    # Create a DataFrame for plotting
                    df_modules = pd.DataFrame({
                        "Module": list(module_counts.keys()),
                        "Count": list(module_counts.values())
                    })
                    
                    fig = px.bar(
                        df_modules,
                        x="Module",
                        y="Count",
                        title="Module Distribution Across Licenses",
                        color="Count",
                        color_continuous_scale="Viridis"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Module",
                        yaxis_title="Number of Licenses",
                        coloraxis_showscale=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No licenses have been created yet. Use the License Builder to create your first license.")
        else:
            st.error(f"Failed to fetch license data: {response.status_code}")
            st.info("If the license API is not running, please start it first.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to license API: {e}")
        st.info("Make sure the license API is running on port 5001.")
        
        # Show instructions for starting the license API
        with st.expander("How to start the License API"):
            st.code("python empire_license_api.py", language="bash")


def show_license_builder():
    """Display the license builder interface"""
    st.markdown("### License Builder")
    st.markdown("Create a new license in the Empire OS ecosystem.")
    
    # License creation form
    with st.form("license_builder_form"):
        license_id = st.text_input("License ID", placeholder="Enter a unique license ID (e.g., ESOM-VOI-JEANS-D2C-001)")
        
        col1, col2 = st.columns(2)
        with col1:
            owner = st.text_input("Owner", placeholder="Enter the license owner (email or ID)")
        
        with col2:
            status = st.selectbox("Status", ["active", "pending", "suspended", "revoked"])
        
        brand = st.text_input("Brand", placeholder="Enter the brand name")
        region = st.text_input("Region", placeholder="Enter region (e.g., India / Karnataka)")
        
        # Module selection with multi-select
        module_options = [
            "Manufacturing",
            "Commerce",
            "Design",
            "Strategy",
            "Governance",
            "Ethics Filter",
            "AI Interface",
            "Finance",
            "Marketing",
            "Tailoring"
        ]
        modules = st.multiselect("Modules", module_options)
        
        # Role mapping
        st.markdown("#### Role Mapping")
        
        col1, col2 = st.columns(2)
        with col1:
            role_type = st.selectbox("Role Type", [
                "Founder",
                "Administrator",
                "Manager",
                "Developer",
                "Retailer",
                "Supply Manager",
                "Guest User",
                "Root Governor"
            ])
        
        with col2:
            power_scope_options = [
                "read",
                "write",
                "approve",
                "issue",
                "strategize",
                "override",
                "suspend",
                "allocate",
                "score"
            ]
            power_scope = st.multiselect("Power Scope", power_scope_options)
        
        submitted = st.form_submit_button("Create License")
        
        if submitted:
            if license_id and owner:
                # Prepare the data
                license_data = {
                    "license_id": license_id,
                    "owner": owner,
                    "brand": brand,
                    "region": region,
                    "modules": modules,
                    "status": status,
                    "role_map": {
                        "role_type": role_type,
                        "power_scope": power_scope,
                        "granted_by": "Genesis Dashboard",
                        "approved_at": datetime.now().isoformat()
                    }
                }
                
                # Send to the API
                try:
                    # First, try to assign the license which will create it if it doesn't exist
                    assign_response = requests.post(
                        f"{API_BASE_URL}/api/license/assign",
                        headers=HEADERS,
                        json={
                            "licenseId": license_id,
                            "assignedTo": owner,
                            "role": role_type,
                            "moduleScope": ", ".join(modules),
                            "node": brand if brand else "Unknown"
                        }
                    )
                    
                    if assign_response.status_code == 200:
                        st.success(f"License {license_id} created and assigned to {owner} successfully!")
                        
                        # Display the created license
                        st.json(assign_response.json())
                    else:
                        st.error(f"Failed to create license: {assign_response.status_code}")
                        st.json(assign_response.json() if assign_response.content else {})
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to license API: {e}")
                    st.info("Make sure the license API is running on port 5001.")
            else:
                st.error("License ID and Owner are required fields.")


def show_license_validation():
    """Display the license validation interface"""
    st.markdown("### License Validation")
    st.markdown("Validate a license against module access requirements.")
    
    # License validation form
    with st.form("license_validation_form"):
        license_id = st.text_input("License ID", placeholder="Enter the license ID to validate")
        module = st.text_input("Module", placeholder="Enter the module name (e.g., Commerce)")
        role = st.text_input("Role (Optional)", placeholder="Enter role to check (e.g., Founder)")
        
        submitted = st.form_submit_button("Validate License")
        
        if submitted:
            if license_id:
                # Send validation request
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/license/verify",
                        headers=HEADERS,
                        json={
                            "license_id": license_id,
                            "module": module,
                            "role": role
                        }
                    )
                    
                    # Display the results
                    if response.status_code == 200:
                        validation_result = response.json()
                        if validation_result.get("valid"):
                            st.success(f"✅ License {license_id} is valid for the requested access!")
                            
                            # Show license details
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Brand:** {validation_result.get('brand', 'N/A')}")
                            
                            with col2:
                                st.markdown(f"**Region:** {validation_result.get('region', 'Global')}")
                            
                            st.markdown(f"**Status:** {validation_result.get('status', 'N/A')}")
                        else:
                            st.error(f"❌ License is invalid: {validation_result.get('reason', 'Unknown reason')}")
                    else:
                        st.error(f"Error validating license: {response.status_code}")
                        if response.content:
                            st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to license API: {e}")
                    st.info("Make sure the license API is running on port 5001.")
            else:
                st.error("License ID is required.")


def show_license_audit():
    """Display the license audit interface"""
    st.markdown("### License Audit Log")
    st.markdown("View the DigitalMe action ledger for license-related activities.")
    
    # Attempt to fetch ledger data
    try:
        response = requests.get(f"{API_BASE_URL}/digitalme/ledger", headers=HEADERS)
        if response.status_code == 200:
            ledger_entries = response.json()
            
            if ledger_entries:
                # Filter options
                license_id_filter = st.text_input("Filter by License ID", "")
                role_filter = st.text_input("Filter by Role", "")
                
                # Apply filters
                filtered_entries = ledger_entries
                if license_id_filter:
                    filtered_entries = [entry for entry in filtered_entries 
                                      if license_id_filter.lower() in entry.get("license_id", "").lower()]
                
                if role_filter:
                    filtered_entries = [entry for entry in filtered_entries 
                                      if role_filter.lower() in entry.get("role", "").lower()]
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Actions", len(ledger_entries))
                
                with col2:
                    blocked_count = sum(1 for entry in ledger_entries if entry.get("action_status") == "blocked")
                    st.metric("Blocked Actions", blocked_count)
                
                with col3:
                    high_risk_count = sum(1 for entry in ledger_entries if entry.get("risk_score", 0) > 70)
                    st.metric("High Risk Actions", high_risk_count)
                
                # Display the ledger as a DataFrame
                entries_for_df = []
                for entry in filtered_entries:
                    entries_for_df.append({
                        "Timestamp": entry.get("timestamp", ""),
                        "License ID": entry.get("license_id", ""),
                        "Role": entry.get("role", ""),
                        "Action": entry.get("action", ""),
                        "Status": entry.get("action_status", ""),
                        "Risk Score": entry.get("risk_score", 0),
                        "Session ID": entry.get("session_id", ""),
                        "Device": entry.get("device", ""),
                        "Geo Location": entry.get("geo_location", ""),
                        "Validated By": entry.get("validated_by", "")
                    })
                
                if entries_for_df:
                    df_ledger = pd.DataFrame(entries_for_df)
                    st.dataframe(df_ledger, use_container_width=True)
                    
                    # Risk score distribution
                    st.markdown("### Risk Score Distribution")
                    
                    fig = px.histogram(
                        df_ledger,
                        x="Risk Score",
                        nbins=10,
                        color_discrete_sequence=["#e63946"],
                        title="Distribution of Risk Scores Across Actions"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Risk Score",
                        yaxis_title="Number of Actions",
                        bargap=0.1
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No ledger entries match the current filters.")
            else:
                st.info("No ledger entries available.")
        else:
            st.error(f"Failed to fetch ledger data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to license API: {e}")
        st.info("Make sure the license API is running on port 5001.")


def show_divine_alignment():
    """Display the Divine Alignment Layer interface"""
    st.markdown("### Divine Alignment Layer (DAL)")
    st.markdown("""
    The Divine Alignment Layer ensures that license scopes align with ethical principles.
    Check scope tags against the divine ethical keywords to ensure compliance.
    """)
    
    # Fetch the ethical keywords
    try:
        # We'll fake a request to get the keywords since we know the structure
        ethical_keywords = [
            "trust", "sustainability", "inclusion", "authenticity", "justice", 
            "transparency", "accountability", "fairness", "compassion", "honesty",
            "integrity", "respect", "equity", "benevolence", "morality"
        ]
        
        # Show DAL scope checker
        st.markdown("### Check Scope Alignment")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("dal_alignment_form"):
                license_id = st.text_input("License ID (Optional)", placeholder="Enter a license ID if applicable")
                scope_tags = st.text_area(
                    "Scope Tags", 
                    placeholder="Enter scope tags separated by commas (e.g., trust, security, profit, growth)"
                )
                submitted = st.form_submit_button("Check Alignment")
                
                if submitted:
                    if scope_tags:
                        # Call the DAL alignment API
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/api/dal/align",
                                headers=HEADERS,
                                json={
                                    "license_id": license_id,
                                    "scope_tags": scope_tags,
                                    "requester": "Streamlit DAL Interface"
                                }
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                aligned = result.get("aligned", [])
                                misaligned = result.get("misaligned", [])
                                alignment_score = result.get("alignment_score", 0)
                                
                                # Display the results
                                st.markdown(f"### Alignment Score: {alignment_score:.1f}%")
                                
                                # Use a gauge chart to visualize the alignment score
                                fig = go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=alignment_score,
                                    domain={'x': [0, 1], 'y': [0, 1]},
                                    title={'text': "Divine Alignment Score"},
                                    gauge={
                                        'axis': {'range': [0, 100], 'tickwidth': 1},
                                        'bar': {'color': "#2a4a7f"},
                                        'bgcolor': "white",
                                        'borderwidth': 2,
                                        'bordercolor': "gray",
                                        'steps': [
                                            {'range': [0, 40], 'color': 'red'},
                                            {'range': [40, 75], 'color': 'yellow'},
                                            {'range': [75, 100], 'color': 'green'}
                                        ]
                                    }
                                ))
                                
                                fig.update_layout(height=300)
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Display aligned and misaligned tags
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("#### ✅ Aligned Tags")
                                    if aligned:
                                        for tag in aligned:
                                            st.markdown(f"- {tag}")
                                    else:
                                        st.info("No aligned tags found.")
                                
                                with col2:
                                    st.markdown("#### ❌ Misaligned Tags")
                                    if misaligned:
                                        for tag in misaligned:
                                            st.markdown(f"- {tag}")
                                    else:
                                        st.success("No misaligned tags found.")
                                
                                # Provide divine guidance for improvement
                                if alignment_score < 75:
                                    st.warning("""
                                    #### Divine Guidance
                                    To improve alignment, consider replacing misaligned tags with ethical alternatives.
                                    Focus on values that promote sustainability, justice, and compassion.
                                    """)
                            else:
                                st.error(f"Error checking alignment: {response.status_code}")
                                st.json(response.json() if response.content else {})
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to license API: {e}")
                            st.info("Make sure the license API is running on port 5001.")
                    else:
                        st.error("Please enter scope tags to check alignment.")
        
        with col2:
            st.markdown("#### Ethical Keywords")
            st.markdown("The Divine Alignment Layer checks scope tags against these ethical keywords:")
            
            keywords_html = ""
            for keyword in ethical_keywords:
                keywords_html += f"<span style='background-color: rgba(42, 74, 127, 0.1); padding: 5px; margin: 2px; border-radius: 5px; display: inline-block;'>{keyword}</span>"
            
            st.markdown(f"<div style='line-height: 2.5;'>{keywords_html}</div>", unsafe_allow_html=True)
        
        # Display visual representation of ethical alignment
        st.markdown("### Divine Alignment Principles")
        principles = [
            {
                "name": "Justice (عدل)",
                "description": "Balance and fairness in all operations and resource allocation."
            },
            {
                "name": "Mercy (رحمن)",
                "description": "Compassionate treatment of all stakeholders and users."
            },
            {
                "name": "All-Knowing (علیم)",
                "description": "Complete visibility and informed decision-making."
            },
            {
                "name": "All-Seeing (بصیر)",
                "description": "Comprehensive oversight and transparency."
            },
            {
                "name": "Most Generous (کریم)",
                "description": "Optimal value creation for all participants."
            }
        ]
        
        # Create cards for each principle
        st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px;'>", unsafe_allow_html=True)
        
        for principle in principles:
            st.markdown(f"""
            <div style='flex: 1; min-width: 200px; padding: 15px; border-radius: 5px; background-color: rgba(42, 74, 127, 0.05); border-left: 4px solid #2a4a7f;'>
                <h4>{principle['name']}</h4>
                <p>{principle['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error displaying Divine Alignment Layer: {e}")


def show_genesis_vision():
    """Display the Genesis Vision timeline and visualization"""
    st.markdown("### Genesis Vision Timeline")
    st.markdown("""
    The Genesis Vision displays the brand's progression through the creation cycle,
    showing key milestones, textures, and emotions associated with each phase.
    """)
    
    # Load the vision logger data
    try:
        with open("digitalme_vision_logger.json", "r") as f:
            vision_data = json.load(f)
            
        # Load reputation data
        with open("digitalme_license_reputation.json", "r") as f:
            reputation_data = json.load(f)
            
        if vision_data:
            # Display header information
            st.markdown(f"### {vision_data.get('brand', 'Unknown Brand')} Vision Journey")
            st.markdown(f"**License ID:** {vision_data.get('license_id', 'Unknown')}")
            st.markdown(f"**Current State:** {vision_data.get('current_state', 'Unknown')}")
            st.markdown(f"**Projected Next:** {vision_data.get('projected_next', 'Unknown')}")
            
            # Display AI hint
            st.info(f"**AI Hint:** {vision_data.get('ai_hint', 'No AI hints available.')}")
            
            # Display reputation metrics
            license_id = vision_data.get('license_id')
            if license_id in reputation_data:
                rep_data = reputation_data[license_id]
                
                st.markdown("### License Reputation Metrics")
                cols = st.columns(3)
                
                with cols[0]:
                    st.metric("Total Sessions", rep_data.get("total_sessions", 0))
                    st.metric("Blocked Actions", rep_data.get("blocked_actions", 0))
                
                with cols[1]:
                    st.metric("High Risk Count", rep_data.get("high_risk_count", 0))
                    st.metric("Average Risk", f"{rep_data.get('average_risk', 0):.1f}")
                
                with cols[2]:
                    st.metric("Reputation Score", f"{rep_data.get('score', 0):.1f}/100")
                    divine_override = rep_data.get("divine_override", False)
                    override_text = "Yes" if divine_override else "No"
                    st.metric("Divine Override", override_text)
            
            # Create timeline visualization
            st.markdown("### Genesis Path Timeline")
            
            # Create a DataFrame for the timeline
            genesis_path = vision_data.get("genesis_path", [])
            if genesis_path:
                path_data = []
                for stage in genesis_path:
                    path_data.append({
                        "Day": stage.get("day", "Unknown"),
                        "Milestone": stage.get("milestone", "Unknown"),
                        "Texture": stage.get("texture", "Unknown"),
                        "Emotion": stage.get("emotion", "Unknown"),
                        "Timestamp": stage.get("timestamp", "")
                    })
                
                df_path = pd.DataFrame(path_data)
                
                # Create a timeline visualization
                fig = go.Figure()
                
                # Add the timeline points
                fig.add_trace(go.Scatter(
                    x=list(range(len(df_path))),
                    y=[1] * len(df_path),
                    mode="markers+text",
                    marker=dict(
                        size=20,
                        color=["#1a365d", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"][:len(df_path)],
                        symbol="circle",
                        line=dict(
                            color="white",
                            width=2
                        )
                    ),
                    text=df_path["Day"],
                    textposition="top center",
                    textfont=dict(
                        size=14,
                        color="#1a365d"
                    ),
                    hoverinfo="text",
                    hovertext=[
                        f"<b>{row['Day']}</b><br>"
                        f"Milestone: {row['Milestone']}<br>"
                        f"Texture: {row['Texture']}<br>"
                        f"Emotion: {row['Emotion']}<br>"
                        f"Date: {row['Timestamp'].split('T')[0] if 'T' in row['Timestamp'] else row['Timestamp']}"
                        for _, row in df_path.iterrows()
                    ]
                ))
                
                # Add horizontal line connecting the points
                fig.add_trace(go.Scatter(
                    x=list(range(len(df_path))),
                    y=[1] * len(df_path),
                    mode="lines",
                    line=dict(
                        color="#1a365d",
                        width=2,
                        dash="dashdot"
                    ),
                    hoverinfo="none"
                ))
                
                # Configure layout
                fig.update_layout(
                    title="Genesis Path Timeline",
                    showlegend=False,
                    height=300,
                    margin=dict(
                        l=20,
                        r=20,
                        t=80,
                        b=20
                    ),
                    xaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[0.5, 1.5]
                    ),
                    hovermode="closest",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display the details of each stage in expandable sections
                for i, stage in enumerate(genesis_path):
                    with st.expander(f"Stage {i+1}: {stage.get('day', 'Unknown')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Milestone:** {stage.get('milestone', 'Unknown')}")
                            st.markdown(f"**Texture:** {stage.get('texture', 'Unknown')}")
                        
                        with col2:
                            st.markdown(f"**Emotion:** {stage.get('emotion', 'Unknown')}")
                            timestamp = stage.get('timestamp', '')
                            date_str = timestamp.split('T')[0] if 'T' in timestamp else timestamp
                            st.markdown(f"**Date:** {date_str}")
            else:
                st.info("No genesis path data available for this license.")
                
            # Add projections for future stages
            st.markdown("### Vision Projections")
            st.markdown("""
            Based on the current trajectory, the following projections are available
            for the next stages of this brand's journey:
            """)
            
            projected_next = vision_data.get("projected_next", "")
            if projected_next:
                projected_stages = [
                    {
                        "day": projected_next,
                        "milestone": "Fully integrated multimodal enterprise governance",
                        "texture": "Crystalline networks and fractal boundaries",
                        "emotion": "Command, oversight, superintelligence",
                        "probability": 89.7
                    },
                    {
                        "day": "Day 6 – Land Dwellers",
                        "milestone": "Horizontal market expansion across adjacent industries",
                        "texture": "Connected pools and terraformed landscapes",
                        "emotion": "Conquest, diversification, reinforcement",
                        "probability": 67.3
                    },
                    {
                        "day": "Day 7 – Rest",
                        "milestone": "Optimization and value stabilization phase",
                        "texture": "Gentle symmetry and ordered abundance",
                        "emotion": "Completion, celebration, reinvestment",
                        "probability": 42.1
                    }
                ]
                
                # Display projections
                for i, projection in enumerate(projected_stages):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style='border-left: 4px solid #1a365d; padding-left: 15px;'>
                            <h4>{projection['day']}</h4>
                            <p><b>Milestone:</b> {projection['milestone']}</p>
                            <p><b>Texture:</b> {projection['texture']}</p>
                            <p><b>Emotion:</b> {projection['emotion']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Probability", f"{projection['probability']:.1f}%")
            else:
                st.info("No projection data available for this license.")
        else:
            st.warning("No vision data available. Please check the digitalme_vision_logger.json file.")
            
    except FileNotFoundError:
        st.error("Vision data files not found. Please make sure digitalme_vision_logger.json and digitalme_license_reputation.json exist in the project directory.")
    except json.JSONDecodeError:
        st.error("Error decoding vision data. Please check that the JSON files are properly formatted.")
    except Exception as e:
        st.error(f"Error displaying Genesis Vision: {e}")


if __name__ == "__main__":
    # Set up basic Streamlit configuration
    st.set_page_config(
        page_title="Empire License Management",
        page_icon="🏛️",
        layout="wide"
    )
    
    # Apply custom styling
    st.markdown("""
    <style>
        .divine-header {
            color: #1a365d;
            border-bottom: 2px solid #ffd700;
            padding-bottom: 10px;
        }
        .empire-subheader {
            color: #2a4a7f;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the license management interface
    show_license_management()