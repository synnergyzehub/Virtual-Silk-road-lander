"""
Genesis Dashboard - Empire OS Admin Interface

This Streamlit application provides an administrative interface for
managing the Genesis Empowerment Matrix and Virtual Silk Road progression.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import json
import os
from typing import Dict, List, Tuple, Optional

# Import custom modules
from genesis_route_resolver import GenesisRouteResolver
import genesis_core as gc

# Page configuration
st.set_page_config(
    page_title="Genesis Dashboard - Empire OS",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_page = "login"
    st.session_state.authenticated = False
    st.session_state.license_id = None
    st.session_state.user_type = None
    st.session_state.completed_onboarding = False
    st.session_state.realm = "general"
    # Create a sample Genesis Matrix for demo purposes
    st.session_state.matrices = {}

# Custom styling
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
    .realm-card {
        border: 1px solid #e1e1e1;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #f8f9fa;
    }
    .realm-card h3 {
        color: #1a365d;
        margin-bottom: 15px;
    }
    .stage-progress {
        margin: 10px 0;
        padding: 10px;
        border-radius: 5px;
        background-color: rgba(240, 240, 240, 0.5);
    }
    .info-box {
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box.success {
        background-color: rgba(39, 174, 96, 0.1);
        border-left: 4px solid #27ae60;
    }
    .info-box.warning {
        background-color: rgba(243, 156, 18, 0.1);
        border-left: 4px solid #f39c12;
    }
    .info-box.danger {
        background-color: rgba(192, 57, 43, 0.1);
        border-left: 4px solid #c0392b;
    }
    .info-box.info {
        background-color: rgba(41, 128, 185, 0.1);
        border-left: 4px solid #2980b9;
    }
</style>
""", unsafe_allow_html=True)


# Simulated database operations (in a real app, these would connect to a database)
def save_matrix(matrix: gc.GenesisMatrix) -> bool:
    """Save a Genesis Matrix to the session state (simulated database)"""
    st.session_state.matrices[matrix.realm_id] = matrix
    return True

def get_matrix(realm_id: str) -> Optional[gc.GenesisMatrix]:
    """Get a Genesis Matrix from the session state (simulated database)"""
    return st.session_state.matrices.get(realm_id)

def get_all_matrices() -> Dict[str, gc.GenesisMatrix]:
    """Get all Genesis Matrices from the session state (simulated database)"""
    return st.session_state.matrices


# Main application navigation
def main():
    # Initialize the route resolver
    resolver = GenesisRouteResolver()
    
    # Use sidebar for main navigation
    with st.sidebar:
        st.title("Empire OS")
        st.markdown("### Genesis Administration")
        
        # Show login/user info
        if st.session_state.authenticated:
            st.success(f"Logged in as: {st.session_state.user_type}")
            st.info(f"License ID: {st.session_state.license_id}")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.current_page = "login"
                st.rerun()
        else:
            st.warning("Not logged in")
        
        st.divider()
        
        # Only show navigation when authenticated
        if st.session_state.authenticated:
            st.subheader("Navigation")
            page_options = [
                "Dashboard",
                "Realm Management",
                "Department Management", 
                "Virtual Silk Road",
                "License Verification",
                "Divine Alignment"
            ]
            selected_page = st.radio("Select page", page_options)
            
            if selected_page == "Dashboard":
                st.session_state.current_page = "dashboard"
            elif selected_page == "Realm Management":
                st.session_state.current_page = "realm_management"
            elif selected_page == "Department Management":
                st.session_state.current_page = "department_management"
            elif selected_page == "Virtual Silk Road":
                st.session_state.current_page = "silk_road"
            elif selected_page == "License Verification":
                st.session_state.current_page = "license_verification"
            elif selected_page == "Divine Alignment":
                st.session_state.current_page = "divine_alignment"
    
    # Route to the appropriate page
    if not st.session_state.authenticated:
        show_login()
    elif st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "realm_management":
        show_realm_management()
    elif st.session_state.current_page == "department_management":
        show_department_management()
    elif st.session_state.current_page == "silk_road":
        show_silk_road()
    elif st.session_state.current_page == "license_verification":
        show_license_verification()
    elif st.session_state.current_page == "divine_alignment":
        show_divine_alignment()
    elif st.session_state.current_page == "onboarding":
        show_onboarding()
    else:
        # Default fallback
        show_dashboard()


def show_login():
    """Display the login screen"""
    st.markdown('<h1 class="divine-header">Genesis Administration Portal</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Divine Mechanics Computational System</h3>', unsafe_allow_html=True)
    
    # Login form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Access Your Realm")
        user_types = [
            "Select Your Role",
            "Emperor",
            "Minister",
            "Realm Administrator",
            "Department Manager",
            "Supply Manager",
            "Retailer",
            "Guest User"
        ]
        
        selected_role = st.selectbox("Role", user_types)
        license_id = st.text_input("License ID", placeholder="Enter your license ID")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login"):
            if selected_role != "Select Your Role" and license_id and password:
                # In a real system, this would verify credentials against a database
                st.session_state.authenticated = True
                st.session_state.license_id = license_id
                st.session_state.user_type = selected_role.lower().replace(" ", "_")
                
                # Set a sample realm for demo purposes
                if selected_role in ["Emperor", "Minister", "Realm Administrator"]:
                    st.session_state.realm = "governance"
                elif selected_role in ["Department Manager", "Supply Manager"]:
                    st.session_state.realm = "supply_chain"
                elif selected_role == "Retailer":
                    st.session_state.realm = "commerce"
                else:
                    st.session_state.realm = "general"
                
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("Please complete all fields")
    
    with col2:
        st.markdown("### System Overview")
        st.markdown("""
        The Genesis Administration Portal provides access to:
        
        - **Realm Management**: Create and manage organizational realms
        - **Department Oversight**: Monitor department performance and alignment
        - **Virtual Silk Road**: Track progression through digital transformation
        - **License Verification**: Ensure compliance with divine governance
        - **Divine Alignment**: Measure alignment with universal principles
        
        This system is part of the Empire OS ecosystem, implementing divine
        governance through the Emperor's Computational Governance (ECG) framework.
        """)


def show_dashboard():
    """Display the main dashboard"""
    st.markdown('<h1 class="divine-header">Genesis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Divine Governance Overview</h3>', unsafe_allow_html=True)
    
    # Get all matrices
    matrices = get_all_matrices()
    
    # Summary metrics
    if matrices:
        # Calculate aggregate metrics
        realm_count = len(matrices)
        avg_score = sum(gc.calculate_divine_alignment(matrix) for matrix in matrices.values()) / realm_count
        operable_count = sum(1 for matrix in matrices.values() if matrix.operability_status)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Realms", realm_count)
        
        with col2:
            st.metric("Operable Realms", f"{operable_count} / {realm_count}")
        
        with col3:
            st.metric("Average Divine Alignment", f"{avg_score:.1f}%")
        
        with col4:
            dataset_count = sum(matrix.dataset_count for matrix in matrices.values())
            st.metric("Total Datasets", dataset_count)
        
        # Realm status overview
        st.markdown("### Realm Status Overview")
        
        realm_data = []
        for realm_id, matrix in matrices.items():
            divine_alignment = gc.calculate_divine_alignment(matrix)
            valid, reason = gc.check_license_validity(matrix)
            
            realm_data.append({
                "Realm ID": realm_id,
                "License ID": matrix.license_id,
                "Divine Alignment": divine_alignment,
                "Operability": "✅ Operable" if matrix.operability_status else "❌ Not Operable",
                "License Valid": "✅ Valid" if valid else "❌ Invalid",
                "Department Count": len(matrix.departments),
                "Datasets": matrix.dataset_count,
                "Last Updated": matrix.last_updated.strftime("%Y-%m-%d %H:%M")
            })
        
        # Convert to DataFrame and display
        if realm_data:
            df_realms = pd.DataFrame(realm_data)
            st.dataframe(df_realms, use_container_width=True)
            
            # Divine alignment distribution
            st.markdown("### Divine Alignment Distribution")
            
            fig = px.histogram(
                df_realms, 
                x="Divine Alignment",
                nbins=10,
                color_discrete_sequence=["#1a365d"],
                title="Distribution of Divine Alignment Scores Across Realms"
            )
            
            fig.update_layout(
                xaxis_title="Divine Alignment Score",
                yaxis_title="Number of Realms",
                bargap=0.1
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No realm data available for visualization")
    else:
        st.info("No realms have been created yet. Go to Realm Management to create your first realm.")
        
        # Show a call to action
        if st.button("Create Your First Realm"):
            st.session_state.current_page = "realm_management"
            st.rerun()


def show_realm_management():
    """Display the realm management interface"""
    st.markdown('<h1 class="divine-header">Realm Management</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Create and Manage Organizational Realms</h3>', unsafe_allow_html=True)
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Create New Realm")
        
        # Form for creating a new realm
        with st.form("new_realm_form"):
            realm_name = st.text_input("Realm Name", placeholder="Enter a unique name for this realm")
            license_id = st.text_input("License ID", placeholder="Enter license ID for this realm")
            
            realm_type = st.selectbox(
                "Realm Type",
                [
                    "Brand",
                    "Manufacturer",
                    "Retailer",
                    "Government",
                    "Institution"
                ]
            )
            
            divine_use_intent = st.selectbox(
                "Divine Use Intent",
                [
                    "Al-Haqq (Truth Governance)",
                    "Al-Adl (Justice Systems)",
                    "Ar-Rahman (Compassionate Operations)",
                    "Al-Alim (Knowledge Distribution)",
                    "Al-Muqsit (Equitable Resource Management)"
                ]
            )
            
            pane_assignment = st.slider("CPCC Pane Assignment", min_value=1, max_value=9, value=5)
            
            submitted = st.form_submit_button("Create Realm")
            
            if submitted:
                if realm_name and license_id:
                    # Generate a realm ID
                    realm_id = f"REALM-{pane_assignment}-{uuid.uuid4().hex[:6].upper()}"
                    
                    # Create a new Genesis Matrix
                    new_matrix = gc.GenesisMatrix(realm_id=realm_id, license_id=license_id)
                    
                    # Save the matrix
                    save_matrix(new_matrix)
                    
                    st.success(f"Realm '{realm_name}' created successfully with ID: {realm_id}")
                else:
                    st.error("Please provide both Realm Name and License ID")
    
    with col2:
        st.markdown("### Existing Realms")
        
        # Get all matrices
        matrices = get_all_matrices()
        
        if matrices:
            # Create a selectbox for choosing a realm
            realm_ids = list(matrices.keys())
            selected_realm = st.selectbox("Select Realm", realm_ids)
            
            if selected_realm:
                matrix = matrices[selected_realm]
                
                # Display realm details
                st.markdown(f"#### Realm Details: {selected_realm}")
                
                divine_alignment = gc.calculate_divine_alignment(matrix)
                valid, reason = gc.check_license_validity(matrix)
                
                cols = st.columns(2)
                with cols[0]:
                    st.markdown(f"**License ID**: {matrix.license_id}")
                    st.markdown(f"**Created**: {matrix.created_at.strftime('%Y-%m-%d')}")
                    st.markdown(f"**Departments**: {len(matrix.departments)}")
                
                with cols[1]:
                    st.markdown(f"**Divine Alignment**: {divine_alignment:.1f}%")
                    st.markdown(f"**Operability**: {'Operable' if matrix.operability_status else 'Not Operable'}")
                    st.markdown(f"**License Status**: {'Valid' if valid else 'Invalid'}")
                
                # Add warning or info box based on status
                if not valid:
                    st.markdown(f"""
                    <div class="info-box warning">
                        <strong>License Invalid:</strong> {reason}
                    </div>
                    """, unsafe_allow_html=True)
                elif divine_alignment < 75:
                    st.markdown(f"""
                    <div class="info-box info">
                        <strong>Alignment Opportunity:</strong> Divine alignment is below optimal levels. 
                        Consider improving department scores and balancing progression stages.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="info-box success">
                        <strong>Good Standing:</strong> This realm is well-aligned with divine governance principles.
                    </div>
                    """, unsafe_allow_html=True)
                
                # Actions
                st.markdown("#### Realm Actions")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Details", key="view_details"):
                        st.session_state.selected_realm = selected_realm
                        st.session_state.current_page = "department_management"
                        st.rerun()
                
                with col2:
                    if st.button("❌ Delete Realm", key="delete_realm"):
                        # In a real application, this would have a confirmation dialog
                        if selected_realm in st.session_state.matrices:
                            del st.session_state.matrices[selected_realm]
                            st.success(f"Realm {selected_realm} deleted successfully")
                            st.rerun()
        else:
            st.info("No realms have been created yet. Use the form on the left to create your first realm.")


def show_department_management():
    """Display the department management interface"""
    st.markdown('<h1 class="divine-header">Department Management</h1>', unsafe_allow_html=True)
    
    # Get all matrices
    matrices = get_all_matrices()
    
    if not matrices:
        st.info("No realms have been created yet. Go to Realm Management to create your first realm.")
        return
    
    # Select a realm
    if 'selected_realm' in st.session_state and st.session_state.selected_realm in matrices:
        selected_realm = st.session_state.selected_realm
    else:
        realm_ids = list(matrices.keys())
        selected_realm = st.selectbox("Select Realm", realm_ids)
    
    if not selected_realm:
        st.warning("Please select a realm to manage its departments")
        return
    
    matrix = matrices[selected_realm]
    
    st.markdown(f'<h3 class="empire-subheader">Managing Departments for Realm: {selected_realm}</h3>', unsafe_allow_html=True)
    
    # Create tabs for different department functions
    tab1, tab2, tab3 = st.tabs(["Department Overview", "Add Department", "Update Department"])
    
    with tab1:
        st.markdown("### Department Overview")
        
        if matrix.departments:
            # Create a DataFrame for the departments
            dept_data = []
            for name, dept in matrix.departments.items():
                dept_data.append({
                    "Department": name,
                    "Type": dept["type"],
                    "Governance Level": dept["governance_level"],
                    "Score": dept["score"],
                    "Datasets": dept["datasets"],
                    "Silk Road Stage": dept["silk_road_stage"],
                    "Users": len(dept["users"]),
                    "Modules": len(dept["modules"])
                })
            
            df_depts = pd.DataFrame(dept_data)
            st.dataframe(df_depts, use_container_width=True)
            
            # Visualize department scores
            st.markdown("### Department Scores")
            
            fig = px.bar(
                df_depts,
                x="Department",
                y="Score",
                color="Governance Level",
                title="Department Performance Scores",
                color_discrete_map={
                    "policy": "#1a365d",
                    "strategic": "#2a4a7f",
                    "operational": "#4a69bd"
                }
            )
            
            fig.update_layout(
                xaxis_title="Department",
                yaxis_title="Score (0-100)",
                legend_title="Governance Level"
            )
            
            # Add threshold line
            fig.add_shape(
                type="line",
                line=dict(dash="dash", color="red", width=2),
                y0=gc.DEPARTMENT_SCORE_THRESHOLD,
                y1=gc.DEPARTMENT_SCORE_THRESHOLD,
                x0=-0.5,
                x1=len(df_depts) - 0.5
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Visualize Silk Road stages
            st.markdown("### Silk Road Stage Distribution")
            
            # Count departments in each stage
            stage_counts = df_depts["Silk Road Stage"].value_counts().reset_index()
            stage_counts.columns = ["Stage", "Count"]
            
            # Reorder stages by their progression sequence
            stage_order = {stage: i for i, stage in enumerate(gc.SILK_ROAD_STAGES)}
            stage_counts["Order"] = stage_counts["Stage"].map(stage_order)
            stage_counts = stage_counts.sort_values("Order")
            
            fig = px.bar(
                stage_counts,
                x="Stage",
                y="Count",
                title="Department Distribution Across Silk Road Stages",
                color="Count",
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(
                xaxis_title="Silk Road Stage",
                yaxis_title="Number of Departments",
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("This realm has no departments yet. Use the 'Add Department' tab to create departments.")
    
    with tab2:
        st.markdown("### Add New Department")
        
        with st.form("add_department_form"):
            dept_name = st.text_input("Department Name", placeholder="Enter department name")
            
            dept_type = st.selectbox(
                "Department Type",
                [t.value for t in gc.DepartmentType]
            )
            
            governance_level = st.selectbox(
                "Governance Level",
                [l.value for l in gc.GovernanceLevel]
            )
            
            submitted = st.form_submit_button("Add Department")
            
            if submitted:
                if dept_name:
                    # Add the department
                    success = matrix.add_department(
                        name=dept_name,
                        dept_type=gc.DepartmentType(dept_type),
                        governance_level=gc.GovernanceLevel(governance_level)
                    )
                    
                    if success:
                        st.success(f"Department '{dept_name}' added successfully")
                    else:
                        st.error(f"Department '{dept_name}' already exists")
                else:
                    st.error("Please provide a department name")
    
    with tab3:
        st.markdown("### Update Department")
        
        if not matrix.departments:
            st.info("No departments to update. Add departments first.")
        else:
            dept_options = list(matrix.departments.keys())
            selected_dept = st.selectbox("Select Department", dept_options)
            
            if selected_dept:
                dept = matrix.departments[selected_dept]
                
                # Show current values
                st.markdown(f"**Current Score**: {dept['score']}")
                st.markdown(f"**Current Datasets**: {dept['datasets']}")
                st.markdown(f"**Current Silk Road Stage**: {dept['silk_road_stage']}")
                
                # Form for updates
                with st.form("update_department_form"):
                    new_score = st.slider(
                        "Department Score",
                        min_value=0.0,
                        max_value=100.0,
                        value=float(dept['score']),
                        step=1.0
                    )
                    
                    add_datasets = st.number_input(
                        "Add Datasets",
                        min_value=0,
                        max_value=100,
                        value=0
                    )
                    
                    submitted = st.form_submit_button("Update Department")
                    
                    if submitted:
                        # Update score
                        if new_score != dept['score']:
                            matrix.update_department_score(selected_dept, new_score)
                        
                        # Add datasets
                        for _ in range(add_datasets):
                            matrix.add_dataset(selected_dept)
                        
                        st.success(f"Department '{selected_dept}' updated successfully")
                        
                        # Show the updated Silk Road stage
                        updated_dept = matrix.departments[selected_dept]
                        if updated_dept['silk_road_stage'] != dept['silk_road_stage']:
                            st.success(f"Department progressed to {updated_dept['silk_road_stage']} stage!")


def show_silk_road():
    """Display the Virtual Silk Road visualization"""
    st.markdown('<h1 class="divine-header">Virtual Silk Road</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Progression Through Digital Transformation</h3>', unsafe_allow_html=True)
    
    # Get all matrices
    matrices = get_all_matrices()
    
    if not matrices:
        st.info("No realms have been created yet. Go to Realm Management to create your first realm.")
        return
    
    # Select a realm
    if 'selected_realm' in st.session_state and st.session_state.selected_realm in matrices:
        selected_realm = st.session_state.selected_realm
    else:
        realm_ids = list(matrices.keys())
        selected_realm = st.selectbox("Select Realm", realm_ids)
    
    if not selected_realm:
        st.warning("Please select a realm to view its Silk Road progression")
        return
    
    matrix = matrices[selected_realm]
    
    # Silk Road visualization
    st.markdown("### Virtual Silk Road Progression")
    
    # Display introduction to the Silk Road concept
    st.markdown("""
    The Virtual Silk Road represents the digital transformation journey of your organization.
    Each department progresses through stages from initial checkpoint entry to full operability unlock.
    
    This gamified approach treats:
    - Departments as 'cities' along the Silk Road
    - Modules as 'checkpoints' that must be passed
    - Users as 'travelers' carrying knowledge through the system
    """)
    
    # Create a visualization of the Silk Road
    if matrix.departments:
        # Get progress for all departments
        progress = matrix.get_silk_road_progress()
        
        # Create a progress table
        progress_data = []
        for dept_name, prog_info in progress.items():
            progress_data.append({
                "Department": dept_name,
                "Current Stage": prog_info["current_stage"],
                "Progress (%)": prog_info["progress_pct"],
                "Next Stage": prog_info["next_stage"] if prog_info["next_stage"] else "Complete"
            })
        
        df_progress = pd.DataFrame(progress_data)
        st.dataframe(df_progress, use_container_width=True)
        
        # Create a stage flow diagram
        st.markdown("### Silk Road Stage Flow")
        
        # Create nodes for all stages
        stages = gc.SILK_ROAD_STAGES
        
        # Visualize departments flowing through stages
        dept_flows = []
        for dept_name, dept in matrix.departments.items():
            current_stage = dept["silk_road_stage"]
            current_idx = stages.index(current_stage)
            
            # Add flows up to current stage
            for i in range(current_idx):
                dept_flows.append({
                    "from": stages[i],
                    "to": stages[i+1],
                    "value": 1,
                    "department": dept_name
                })
        
        # Build Sankey diagram
        if dept_flows:
            # Create nodes and links
            all_nodes = list(set([flow["from"] for flow in dept_flows] + 
                                [flow["to"] for flow in dept_flows]))
            
            node_ids = {node: i for i, node in enumerate(all_nodes)}
            
            sources = [node_ids[flow["from"]] for flow in dept_flows]
            targets = [node_ids[flow["to"]] for flow in dept_flows]
            values = [flow["value"] for flow in dept_flows]
            labels = [flow["department"] for flow in dept_flows]
            
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=all_nodes,
                    color="blue"
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    label=labels,
                    color="rgba(41, 128, 185, 0.5)"
                )
            )])
            
            fig.update_layout(
                title_text="Departments Flowing Through Silk Road Stages",
                font_size=12,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed progression stages
        st.markdown("### Stage Progression Details")
        
        for stage_name in stages:
            depts_in_stage = [name for name, dept in matrix.departments.items() 
                             if dept["silk_road_stage"] == stage_name]
            depts_passed_stage = [name for name, dept in matrix.departments.items() 
                                 if stages.index(dept["silk_road_stage"]) > stages.index(stage_name)]
            
            # Calculate completion percentage
            completion = (len(depts_passed_stage) + len(depts_in_stage)) / len(matrix.departments) * 100
            
            st.markdown(f"""
            <div class="stage-progress">
                <h4>{stage_name}</h4>
                <p>Completion: {completion:.1f}%</p>
                <p>Departments in this stage: {len(depts_in_stage)}</p>
                <p>Departments passed this stage: {len(depts_passed_stage)}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("This realm has no departments yet. Add departments to visualize Silk Road progression.")


def show_license_verification():
    """Display the license verification interface"""
    st.markdown('<h1 class="divine-header">License Verification</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Validate Divine Governance Compliance</h3>', unsafe_allow_html=True)
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Verify License")
        
        # License verification form
        with st.form("license_verification_form"):
            license_id = st.text_input("License ID", placeholder="Enter license ID to verify")
            realm_id = st.text_input("Realm ID (optional)", placeholder="Enter realm ID if known")
            
            submitted = st.form_submit_button("Verify License")
            
            if submitted:
                if license_id:
                    # Check if we have this license in any of our matrices
                    matrices = get_all_matrices()
                    matching_matrices = []
                    
                    for r_id, matrix in matrices.items():
                        if matrix.license_id == license_id:
                            if not realm_id or r_id == realm_id:
                                matching_matrices.append((r_id, matrix))
                    
                    if matching_matrices:
                        st.success(f"License {license_id} found in {len(matching_matrices)} realm(s)")
                        
                        # Show detailed results for each match
                        for r_id, matrix in matching_matrices:
                            valid, reason = gc.check_license_validity(matrix)
                            divine_alignment = gc.calculate_divine_alignment(matrix)
                            
                            # Display verification result
                            if valid:
                                st.markdown(f"""
                                <div class="info-box success">
                                    <h4>Realm: {r_id}</h4>
                                    <p><strong>Status:</strong> ✅ Valid</p>
                                    <p><strong>Divine Alignment:</strong> {divine_alignment:.1f}%</p>
                                    <p><strong>Operability:</strong> {'✅ Operable' if matrix.operability_status else '❌ Not Operable'}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="info-box danger">
                                    <h4>Realm: {r_id}</h4>
                                    <p><strong>Status:</strong> ❌ Invalid</p>
                                    <p><strong>Reason:</strong> {reason}</p>
                                    <p><strong>Divine Alignment:</strong> {divine_alignment:.1f}%</p>
                                    <p><strong>Operability:</strong> {'✅ Operable' if matrix.operability_status else '❌ Not Operable'}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error(f"No matching license found for ID: {license_id}")
                else:
                    st.error("Please enter a license ID to verify")
    
    with col2:
        st.markdown("### License Requirements")
        st.markdown("""
        For a license to be valid, the following criteria must be met:
        
        1. **Matrix Operability**: The realm must have achieved operability status
        2. **Minimum Score**: The weighted score must exceed the threshold of 70.0
        3. **Divine Alignment**: The divine alignment score must be at least 60.0
        4. **Dataset Requirements**: At least 300 datasets must be registered
        
        The verification process evaluates how well each department in the realm
        progresses through the Virtual Silk Road and whether overall governance
        aligns with divine principles.
        """)
        
        st.markdown("### License Governance Structure")
        
        # Show a simple diagram of the license governance structure
        st.markdown("""
        ```
        Emperor (ECG)
           ├── Licenses
           │    ├── Realm 1
           │    │    ├── Department A
           │    │    │    ├── Module 1
           │    │    │    └── Module 2
           │    │    └── Department B
           │    └── Realm 2
           └── Divine Alignment Layer
                └── Governance Verification
        ```
        """)
        
        st.markdown("""
        Each license is evaluated on multiple dimensions:
        
        1. **Justice (عدل)**: Balanced inventory across all locations
        2. **Mercy (رحمن)**: Prevention of stockouts and disruptions
        3. **All-Knowing (علیم)**: Data-driven decision-making capability
        4. **All-Seeing (بصیر)**: Complete visibility into operations
        5. **Most Generous (کریم)**: Efficient resource allocation for all stakeholders
        """)


def show_divine_alignment():
    """Display the divine alignment analysis interface"""
    st.markdown('<h1 class="divine-header">Divine Alignment Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Measure Alignment with Divine Governance Principles</h3>', unsafe_allow_html=True)
    
    # Get all matrices
    matrices = get_all_matrices()
    
    if not matrices:
        st.info("No realms have been created yet. Go to Realm Management to create your first realm.")
        return
    
    # Select a realm
    if 'selected_realm' in st.session_state and st.session_state.selected_realm in matrices:
        selected_realm = st.session_state.selected_realm
    else:
        realm_ids = list(matrices.keys())
        selected_realm = st.selectbox("Select Realm", realm_ids)
    
    if not selected_realm:
        st.warning("Please select a realm to analyze its divine alignment")
        return
    
    matrix = matrices[selected_realm]
    
    # Calculate divine alignment score
    divine_alignment = gc.calculate_divine_alignment(matrix)
    
    # Show summary
    st.markdown("### Divine Alignment Summary")
    
    # Create a gauge chart for the divine alignment score
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=divine_alignment,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Divine Alignment Score"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'red'},
                {'range': [50, 75], 'color': 'yellow'},
                {'range': [75, 100], 'color': 'green'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': gc.DEPARTMENT_SCORE_THRESHOLD
            }
        }
    ))
    
    # Set the gauge size
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the alignment category
    if divine_alignment < 50:
        st.markdown("""
        <div class="info-box danger">
            <h3>🚫 Out of Alignment</h3>
            <p>This realm is significantly misaligned with divine governance principles. 
            Immediate corrective action is required to bring the realm into compliance.</p>
        </div>
        """, unsafe_allow_html=True)
    elif divine_alignment < 75:
        st.markdown("""
        <div class="info-box warning">
            <h3>⚠️ At Risk</h3>
            <p>This realm shows concerning deviations from divine governance principles.
            Attention is needed to improve alignment in the areas highlighted below.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box success">
            <h3>✅ Divine-Compatible</h3>
            <p>This realm demonstrates good alignment with divine governance principles.
            Continue to monitor and maintain these high standards of operation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed analysis
    st.markdown("### Detailed Alignment Analysis")
    
    # Get weighted score
    weighted_score = matrix.get_weighted_score()
    
    # Calculate other component scores
    if matrix.departments:
        # Calculate stage balance
        stage_counts = {}
        for dept in matrix.departments.values():
            stage = dept["silk_road_stage"]
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        stage_balance = 100.0
        if stage_counts:
            ideal_count = len(matrix.departments) / len(gc.SILK_ROAD_STAGES)
            variance = sum((count - ideal_count) ** 2 for count in stage_counts.values())
            stage_balance = max(0, 100 - (variance * 10))
        
        # Create component scores
        components = {
            "Weighted Score": weighted_score,
            "Stage Balance": stage_balance,
            "Dataset Completeness": min(100, (matrix.dataset_count / gc.MIN_DATASETS_REQUIRED) * 100),
            "Operability Status": 100 if matrix.operability_status else 0
        }
        
        # Display components
        component_df = pd.DataFrame({
            "Component": list(components.keys()),
            "Score": list(components.values())
        })
        
        fig = px.bar(
            component_df,
            x="Component",
            y="Score",
            title="Divine Alignment Component Scores",
            color="Score",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100]
        )
        
        fig.update_layout(
            xaxis_title="Component",
            yaxis_title="Score (0-100)",
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Department contribution to alignment
        st.markdown("### Department Contribution to Alignment")
        
        # Calculate each department's contribution 
        dept_contributions = []
        
        for name, dept in matrix.departments.items():
            # Basic score contribution
            score_contribution = dept["score"] / 100
            
            # Stage progression contribution
            stage_idx = gc.SILK_ROAD_STAGES.index(dept["silk_road_stage"])
            stage_contribution = stage_idx / (len(gc.SILK_ROAD_STAGES) - 1)
            
            # Dataset contribution
            dataset_contribution = min(1.0, dept["datasets"] / (gc.MIN_DATASETS_REQUIRED / len(matrix.departments)))
            
            # Calculate overall contribution
            overall_contribution = (score_contribution * 0.5) + (stage_contribution * 0.3) + (dataset_contribution * 0.2)
            overall_contribution *= 100  # Convert to percentage
            
            dept_contributions.append({
                "Department": name,
                "Type": dept["type"],
                "Governance Level": dept["governance_level"],
                "Alignment Contribution": overall_contribution
            })
        
        # Display department contributions
        dept_contrib_df = pd.DataFrame(dept_contributions)
        
        fig = px.pie(
            dept_contrib_df,
            values="Alignment Contribution",
            names="Department",
            title="Department Contributions to Divine Alignment",
            hover_data=["Type", "Governance Level"]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("This realm has no departments yet. Add departments to perform detailed alignment analysis.")
    
    # Recommendations
    st.markdown("### Divine Alignment Recommendations")
    
    if matrix.departments:
        # Generate recommendations based on analysis
        recommendations = []
        
        # Check overall score
        if weighted_score < gc.DEPARTMENT_SCORE_THRESHOLD:
            recommendations.append(
                "**Improve Department Scores**: The overall weighted score is below the threshold. "
                "Focus on departments with the lowest scores first."
            )
        
        # Check dataset count
        if matrix.dataset_count < gc.MIN_DATASETS_REQUIRED:
            recommendations.append(
                f"**Increase Dataset Registration**: Currently at {matrix.dataset_count} of {gc.MIN_DATASETS_REQUIRED} "
                f"required datasets. Continue to register datasets across all departments."
            )
        
        # Check stage distribution
        stage_counts = {}
        for dept in matrix.departments.values():
            stage = dept["silk_road_stage"]
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        if len(stage_counts) < 2:
            recommendations.append(
                "**Advance Silk Road Progression**: All departments are in the same stage. "
                "Work on advancing at least some departments to later stages."
            )
        
        # Check for departments stuck at earlier stages
        early_stages = gc.SILK_ROAD_STAGES[:2]  # First two stages
        depts_in_early_stages = [name for name, dept in matrix.departments.items() 
                              if dept["silk_road_stage"] in early_stages]
        
        if depts_in_early_stages:
            dept_list = ", ".join(depts_in_early_stages)
            recommendations.append(
                f"**Advance Lagging Departments**: The following departments are in early stages: {dept_list}. "
                f"Focus on helping these departments progress to later stages."
            )
        
        # Display recommendations
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("No specific recommendations at this time. Continue maintaining divine alignment.")
    else:
        st.info("Add departments to receive divine alignment recommendations.")


def show_onboarding():
    """Display the onboarding process for new users"""
    st.markdown('<h1 class="divine-header">Empire OS Onboarding</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="empire-subheader">Welcome to Divine Governance</h3>', unsafe_allow_html=True)
    
    # Create a step indicator
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    
    steps = ["Welcome", "License Introduction", "Genesis Matrix", "Divine Alignment", "Completion"]
    current_step = st.session_state.onboarding_step
    
    # Display step indicator
    cols = st.columns(len(steps))
    for i, step in enumerate(steps, 1):
        with cols[i-1]:
            if i < current_step:
                st.markdown(f"✅ **{step}**")
            elif i == current_step:
                st.markdown(f"🔶 **{step}**")
            else:
                st.markdown(f"⬜ {step}")
    
    st.divider()
    
    # Show current step content
    if current_step == 1:
        st.markdown("### Welcome to Empire OS")
        st.markdown("""
        Empire OS is a divine governance platform implementing eternal principles
        for sustainable and ethical organizational management.
        
        This onboarding process will introduce you to:
        
        - The ECG License System
        - The Genesis Empowerment Matrix
        - Divine Alignment Principles
        - Virtual Silk Road Progression
        
        By the end of this process, you'll understand how to use these tools
        to ensure your organization operates in harmony with divine principles.
        """)
        
        if st.button("Continue to License Introduction"):
            st.session_state.onboarding_step = 2
            st.rerun()
    
    elif current_step == 2:
        st.markdown("### License Introduction")
        st.markdown("""
        The Emperor's Computational Governance (ECG) license system is the foundation
        of Empire OS. Each license represents a covenant to operate according to
        divine principles.
        
        **Key License Concepts:**
        
        - **Realm**: An organizational unit (company, department, etc.)
        - **License**: Permission to operate within divine governance
        - **Department**: Functional units within a realm
        - **Divine Alignment**: Measure of adherence to divine principles
        
        Licenses are issued by the Emperor and must maintain minimum alignment scores
        to remain valid and operational.
        """)
        
        if st.button("Continue to Genesis Matrix"):
            st.session_state.onboarding_step = 3
            st.rerun()
    
    elif current_step == 3:
        st.markdown("### Genesis Empowerment Matrix")
        st.markdown("""
        The Genesis Empowerment Matrix is the computational structure that tracks
        your realm's progress through the stages of divine governance implementation.
        
        **Matrix Components:**
        
        - **Departments**: Organizational units (Manufacturing, Retail, etc.)
        - **Scores**: Performance metrics for each department
        - **Datasets**: Data points registered within the system
        - **Silk Road Stages**: Progression pathway for digital transformation
        
        The matrix calculates your overall operability status and monitors compliance
        with divine governance requirements.
        """)
        
        # Simple interactive demonstration
        st.markdown("### Interactive Demonstration")
        
        demo_score = st.slider("Department Score", 0, 100, 50)
        demo_datasets = st.slider("Registered Datasets", 0, 500, 100)
        
        # Calculate operability status
        operable = (demo_score >= gc.DEPARTMENT_SCORE_THRESHOLD and 
                   demo_datasets >= gc.MIN_DATASETS_REQUIRED)
        
        if operable:
            st.success("✅ This configuration would achieve operability status")
        else:
            if demo_score < gc.DEPARTMENT_SCORE_THRESHOLD:
                st.warning(f"⚠️ Score is below the threshold of {gc.DEPARTMENT_SCORE_THRESHOLD}")
            if demo_datasets < gc.MIN_DATASETS_REQUIRED:
                st.warning(f"⚠️ Dataset count is below the requirement of {gc.MIN_DATASETS_REQUIRED}")
        
        if st.button("Continue to Divine Alignment"):
            st.session_state.onboarding_step = 4
            st.rerun()
    
    elif current_step == 4:
        st.markdown("### Divine Alignment")
        st.markdown("""
        Divine Alignment is the measure of how well your organization embodies
        divine governance principles in its operations.
        
        **Divine Principles:**
        
        1. **Justice (عدل)**: Fair and balanced resource distribution
        2. **Mercy (رحمن)**: Compassionate treatment of stakeholders
        3. **All-Knowing (علیم)**: Data-driven decision making
        4. **All-Seeing (بصیر)**: Complete visibility across operations
        5. **Most Generous (کریم)**: Optimizing value for all stakeholders
        
        Your divine alignment score is calculated based on department performance,
        stage progression balance, dataset completeness, and overall operability.
        """)
        
        # Simple divine alignment calculator
        st.markdown("### Divine Alignment Calculator")
        
        d_score = st.slider("Department Score", 0, 100, 75)
        d_stage = st.selectbox("Silk Road Stage", gc.SILK_ROAD_STAGES, index=2)
        d_datasets = st.slider("Dataset Count", 0, 500, 300)
        
        # Calculate sample divine alignment
        stage_idx = gc.SILK_ROAD_STAGES.index(d_stage)
        stage_contrib = (stage_idx / (len(gc.SILK_ROAD_STAGES) - 1)) * 100
        dataset_contrib = min(100, (d_datasets / gc.MIN_DATASETS_REQUIRED) * 100)
        
        alignment = (d_score * 0.6) + (stage_contrib * 0.2) + (dataset_contrib * 0.2)
        
        # Display alignment gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=alignment,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Divine Alignment Score"},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': 'red'},
                    {'range': [50, 75], 'color': 'yellow'},
                    {'range': [75, 100], 'color': 'green'}
                ]
            }
        ))
        
        # Set the gauge size
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Complete Onboarding"):
            st.session_state.onboarding_step = 5
            st.rerun()
    
    elif current_step == 5:
        st.markdown("### Onboarding Complete")
        st.markdown("""
        Congratulations! You have completed the Empire OS onboarding process.
        
        You now understand the key components of the divine governance system:
        
        ✅ ECG License System
        ✅ Genesis Empowerment Matrix
        ✅ Divine Alignment Principles
        ✅ Virtual Silk Road Progression
        
        You are now ready to begin your journey toward divine governance.
        """)
        
        if st.button("Go to Dashboard"):
            st.session_state.completed_onboarding = True
            st.session_state.current_page = "dashboard"
            st.rerun()


if __name__ == "__main__":
    main()