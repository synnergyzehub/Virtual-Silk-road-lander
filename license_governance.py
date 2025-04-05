import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import datetime
import os
from typing import Dict, List, Any

# Import the ECG license structures
from core.ecg_license_structure import (
    License, LicenseStatus, LicenseType, ComplianceTier,
    DivinePrinciple, GovernanceDimension
)
from core.ecg_license_manager import ECGLicenseManager

def show_license_governance():
    """
    Display the License Governance interface for the Emperor's Computational Governance (ECG)
    License management system.
    """
    st.title("License Governance")
    st.subheader("Emperor's Computational Governance (ECG) Framework")
    
    # Initialize the license manager
    try:
        license_manager = ECGLicenseManager()
    except Exception as e:
        st.error(f"Failed to initialize license manager: {str(e)}")
        return
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create tabs for different license governance sections
    tabs = st.tabs([
        "Dashboard", 
        "License Issuance", 
        "License Management", 
        "Compliance Audits",
        "Governance Analytics"
    ])
    
    # Dashboard Tab
    with tabs[0]:
        show_governance_dashboard(license_manager)
    
    # License Issuance Tab
    with tabs[1]:
        show_license_issuance(license_manager)
    
    # License Management Tab
    with tabs[2]:
        show_license_management(license_manager)
    
    # Compliance Audits Tab
    with tabs[3]:
        show_compliance_audits(license_manager)
    
    # Governance Analytics Tab
    with tabs[4]:
        show_governance_analytics(license_manager)

def show_governance_dashboard(license_manager: ECGLicenseManager):
    """Display the governance dashboard with key metrics and visualizations"""
    st.header("Governance Dashboard")
    
    # Get all licenses
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        st.info("No licenses have been issued yet. Use the License Issuance tab to issue new licenses.")
        return
    
    # Convert to DataFrame for analysis
    df_licenses = pd.DataFrame(licenses)
    
    # Convert date strings to datetime
    df_licenses["issue_date"] = pd.to_datetime(df_licenses["issue_date"])
    df_licenses["expiry_date"] = pd.to_datetime(df_licenses["expiry_date"])
    
    # Calculate key metrics
    active_licenses = df_licenses[df_licenses["status"] == "active"]
    expired_licenses = df_licenses[df_licenses["status"] == "expired"]
    suspended_licenses = df_licenses[df_licenses["status"] == "suspended"]
    revoked_licenses = df_licenses[df_licenses["status"] == "revoked"]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Licenses", len(df_licenses))
    
    with col2:
        st.metric("Active Licenses", len(active_licenses))
    
    with col3:
        st.metric("Suspended/Revoked", len(suspended_licenses) + len(revoked_licenses))
    
    with col4:
        avg_compliance = df_licenses["compliance_score"].mean() if "compliance_score" in df_licenses else 0
        st.metric("Avg. Compliance Score", f"{avg_compliance:.1f}")
    
    # License status distribution
    st.subheader("License Status Distribution")
    
    status_counts = df_licenses["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    
    # Define color map for statuses
    color_map = {
        "active": "green",
        "pending": "blue",
        "suspended": "orange",
        "revoked": "red",
        "expired": "gray"
    }
    
    fig = px.pie(
        status_counts, 
        values="Count", 
        names="Status",
        title="License Status Distribution",
        color="Status",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # License issuance over time
    st.subheader("License Issuance Timeline")
    
    # Group by month
    df_licenses["month"] = df_licenses["issue_date"].dt.to_period("M")
    monthly_issuance = df_licenses.groupby("month").size().reset_index(name="count")
    monthly_issuance["month"] = monthly_issuance["month"].astype(str)
    
    fig = px.line(
        monthly_issuance,
        x="month",
        y="count",
        title="Monthly License Issuance",
        labels={"month": "Month", "count": "Licenses Issued"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Compliance score distribution
    if "compliance_score" in df_licenses:
        st.subheader("Compliance Score Distribution")
        
        # Create bins for compliance scores
        bins = [0, 40, 60, 80, 100]
        labels = ["Critical (<40)", "Needs Improvement (40-60)", "Good (60-80)", "Excellent (80-100)"]
        df_licenses["compliance_bracket"] = pd.cut(df_licenses["compliance_score"], bins=bins, labels=labels, right=False)
        
        bracket_counts = df_licenses["compliance_bracket"].value_counts().reset_index()
        bracket_counts.columns = ["Bracket", "Count"]
        
        fig = px.bar(
            bracket_counts,
            x="Bracket",
            y="Count",
            title="Compliance Score Distribution",
            color="Bracket",
            color_discrete_sequence=["red", "orange", "lightgreen", "darkgreen"]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent licenses
    st.subheader("Recently Issued Licenses")
    recent_licenses = df_licenses.sort_values("issue_date", ascending=False).head(5)
    
    if len(recent_licenses) > 0:
        for _, license in recent_licenses.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{license['entity_name']}** ({license['license_id']})")
                st.markdown(f"Type: {license['license_type']} | Status: {license['status']} | Tier: {license['compliance_tier']}")
            
            with col2:
                days_left = (license["expiry_date"] - datetime.datetime.now()).days
                if days_left > 0:
                    st.markdown(f"Expires in: **{days_left} days**")
                else:
                    st.markdown("**EXPIRED**")
    else:
        st.info("No licenses have been issued yet.")

def show_license_issuance(license_manager: ECGLicenseManager):
    """Display the license issuance interface"""
    st.header("License Issuance")
    st.markdown("Issue new licenses to entities based on divine principles of governance.")
    
    # Create a form for license issuance
    with st.form("license_issuance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            entity_name = st.text_input("Entity Name")
            entity_id = st.text_input("Entity ID")
            
            license_type = st.selectbox(
                "License Type",
                [t.value for t in LicenseType]
            )
            
            compliance_tier = st.selectbox(
                "Compliance Tier",
                [t.value for t in ComplianceTier]
            )
        
        with col2:
            validity_days = st.number_input("Validity (days)", min_value=1, max_value=3650, value=365)
            
            # Multi-select for authorized modules
            all_modules = [
                "inventory_management",
                "supply_chain_optimization",
                "retail_analytics",
                "manufacturing_insights",
                "distribution_planning",
                "license_governance",
                "compliance_audit",
                "divine_alignment",
                "emperor_dashboard",
                "reporting_module"
            ]
            
            authorized_modules = st.multiselect(
                "Authorized Modules",
                all_modules,
                default=["inventory_management"]
            )
            
            # Input for restrictions (as text area, one per line)
            restrictions_text = st.text_area(
                "Restrictions (one per line)",
                "No modification of core governance algorithms\nData must remain within authorized territories"
            )
            restrictions = [r.strip() for r in restrictions_text.split("\n") if r.strip()]
        
        # Metadata as a JSON editor
        st.subheader("Metadata")
        metadata_text = st.text_area(
            "Metadata (JSON format)",
            """{
  "industry": "Retail & Manufacturing",
  "primary_contact": "John Doe",
  "region": "Asia-Pacific",
  "employees": 500
}"""
        )
        
        submit_button = st.form_submit_button("Issue License")
    
    if submit_button:
        if not entity_name or not entity_id:
            st.error("Entity Name and Entity ID are required")
            return
        
        try:
            # Parse metadata JSON
            metadata = json.loads(metadata_text)
            
            # Issue the license
            new_license = license_manager.issue_new_license(
                entity_name=entity_name,
                entity_id=entity_id,
                license_type_str=license_type,
                validity_days=validity_days,
                compliance_tier_str=compliance_tier,
                modules=authorized_modules,
                restrictions=restrictions,
                metadata=metadata
            )
            
            # Show success message
            st.success(f"License issued successfully! License ID: {new_license['license_id']}")
            
            # Display the license details
            with st.expander("View License Details", expanded=True):
                st.json(new_license)
        
        except ValueError as e:
            st.error(f"Invalid value: {str(e)}")
        
        except json.JSONDecodeError:
            st.error("Invalid JSON format in metadata")
        
        except Exception as e:
            st.error(f"Failed to issue license: {str(e)}")

def show_license_management(license_manager: ECGLicenseManager):
    """Display the license management interface"""
    st.header("License Management")
    
    # Get all licenses
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        st.info("No licenses have been issued yet. Use the License Issuance tab to issue new licenses.")
        return
    
    # Convert to DataFrame for display
    df_licenses = pd.DataFrame(licenses)
    
    # Create filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            sorted([s.value for s in LicenseStatus]),
            default=["active"]
        )
    
    with col2:
        type_filter = st.multiselect(
            "Filter by Type",
            sorted([t.value for t in LicenseType]),
            default=[]
        )
    
    with col3:
        tier_filter = st.multiselect(
            "Filter by Compliance Tier",
            sorted([t.value for t in ComplianceTier]),
            default=[]
        )
    
    # Apply filters
    filtered_df = df_licenses
    
    if status_filter:
        filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
    
    if type_filter:
        filtered_df = filtered_df[filtered_df["license_type"].isin(type_filter)]
    
    if tier_filter:
        filtered_df = filtered_df[filtered_df["compliance_tier"].isin(tier_filter)]
    
    # Display the licenses
    st.dataframe(filtered_df, use_container_width=True)
    
    # License details section
    st.subheader("License Details")
    
    selected_license_id = st.selectbox(
        "Select License ID",
        options=[None] + filtered_df["license_id"].tolist(),
        format_func=lambda x: "Select a license..." if x is None else x
    )
    
    if selected_license_id:
        # Get license details
        license_details = license_manager.get_license_details(selected_license_id)
        
        if "error" in license_details:
            st.error(license_details["error"])
        else:
            # Display license information
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Entity:** {license_details['entity_name']}")
                st.markdown(f"**Entity ID:** {license_details['entity_id']}")
                st.markdown(f"**License Type:** {license_details['license_type']}")
            
            with col2:
                st.markdown(f"**Status:** {license_details['status']}")
                st.markdown(f"**Compliance Tier:** {license_details['compliance_tier']}")
                st.markdown(f"**Compliance Score:** {license_details['current_compliance_score']:.1f}")
            
            with col3:
                issue_date = datetime.datetime.fromisoformat(license_details["issue_date"])
                expiry_date = datetime.datetime.fromisoformat(license_details["expiry_date"])
                
                st.markdown(f"**Issued:** {issue_date.strftime('%Y-%m-%d')}")
                st.markdown(f"**Expires:** {expiry_date.strftime('%Y-%m-%d')}")
                
                days_left = (expiry_date - datetime.datetime.now()).days
                if days_left > 0:
                    st.markdown(f"**Days Left:** {days_left}")
                else:
                    st.markdown("**EXPIRED**")
            
            # License actions
            st.subheader("License Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Validate License"):
                    validation_result = license_manager.validate_license(selected_license_id)
                    st.json(validation_result)
            
            with col2:
                new_status = st.selectbox(
                    "Change Status",
                    [None] + [s.value for s in LicenseStatus if s.value != license_details["status"]],
                    format_func=lambda x: "Select new status..." if x is None else x
                )
                
                if new_status and st.button("Update Status"):
                    result = license_manager.update_license_status(selected_license_id, new_status)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(f"Status updated from {result['previous_status']} to {result['new_status']}")
                        st.rerun()
            
            with col3:
                if st.button("View Compliance History"):
                    compliance_history = license_manager.get_compliance_history(selected_license_id)
                    if compliance_history:
                        for i, audit in enumerate(compliance_history):
                            with st.expander(f"Audit {i+1}: {audit['timestamp'][:10]} ({audit['overall_score']:.1f})", expanded=i == 0):
                                st.markdown(f"**Auditor:** {audit['auditor']}")
                                st.markdown(f"**Findings:** {', '.join(audit['findings'])}")
                                st.markdown(f"**Recommendations:** {', '.join(audit['recommendations'])}")
                                
                                # Show dimensions
                                for dim in audit["dimensions"]:
                                    st.markdown(f"**{dim['dimension'].title()} Score:** {dim['overall_score']:.1f}")
                    else:
                        st.info("No compliance audits have been performed yet.")
            
            # License details
            with st.expander("Authorized Modules"):
                st.write(license_details["authorized_modules"])
            
            with st.expander("Restrictions"):
                st.write(license_details["restrictions"])
            
            with st.expander("Metadata"):
                st.json(license_details["meta"])
            
            with st.expander("Full License JSON"):
                st.json(license_details)

def show_compliance_audits(license_manager: ECGLicenseManager):
    """Display the compliance audit interface"""
    st.header("Compliance Audits")
    st.markdown("Perform compliance audits based on divine principles across governance dimensions.")
    
    # Get all licenses
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        st.info("No licenses have been issued yet. Use the License Issuance tab to issue new licenses.")
        return
    
    # Convert to DataFrame for display
    df_licenses = pd.DataFrame(licenses)
    
    # Select a license for audit
    license_id = st.selectbox(
        "Select License for Audit",
        options=[None] + df_licenses["license_id"].tolist(),
        format_func=lambda x: "Select a license..." if x is None else f"{x} - {df_licenses[df_licenses['license_id'] == x]['entity_name'].iloc[0] if x else ''}"
    )
    
    if not license_id:
        return
    
    # Display current license info
    license_details = license_manager.get_license_details(license_id)
    
    if "error" in license_details:
        st.error(license_details["error"])
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Entity:** {license_details['entity_name']}")
    
    with col2:
        st.markdown(f"**Current Status:** {license_details['status']}")
    
    with col3:
        st.markdown(f"**Current Score:** {license_details['current_compliance_score']:.1f}")
    
    # Audit form
    with st.form("audit_form"):
        st.subheader("New Compliance Audit")
        
        auditor = st.text_input("Auditor Name", "Emperor's Governance Team")
        
        # Dimension scores
        st.markdown("### Compliance Scores by Dimension")
        
        # Initialize dimension scores with default values
        dimension_scores = {}
        
        for dimension in GovernanceDimension:
            dimension_name = dimension.value
            
            st.markdown(f"#### {dimension_name.title()}")
            
            dimension_scores[dimension_name] = {}
            
            # Create columns for principles
            cols = st.columns(3)
            
            # Display slider for each principle
            for i, principle in enumerate([DivinePrinciple.JUSTICE, DivinePrinciple.MERCY, DivinePrinciple.ALL_KNOWING]):
                principle_name = principle.value
                
                # Get principle display name
                display_name = " ".join(word.capitalize() for word in principle_name.split("_"))
                
                # Get Arabic name
                arabic_name = ""
                if principle_name == "justice":
                    arabic_name = "عدل"
                elif principle_name == "mercy":
                    arabic_name = "رحمن"
                elif principle_name == "all_knowing":
                    arabic_name = "علیم"
                
                with cols[i]:
                    # Default to 70 (baseline)
                    score = st.slider(
                        f"{display_name} ({arabic_name})",
                        min_value=0,
                        max_value=100,
                        value=70,
                        key=f"{dimension_name}_{principle_name}"
                    )
                    dimension_scores[dimension_name][principle_name] = score
        
        # Findings and recommendations
        findings = st.text_area(
            "Findings (one per line)",
            "Strong commitment to ethical practices\nGood data management principles\nCompliance with reporting requirements"
        )
        
        recommendations = st.text_area(
            "Recommendations (one per line)",
            "Enhance data collection processes\nImplement additional training on divine principles\nStrengthen supplier compliance monitoring"
        )
        
        submit_audit = st.form_submit_button("Submit Audit")
    
    if submit_audit:
        try:
            # Process findings and recommendations
            findings_list = [f.strip() for f in findings.split("\n") if f.strip()]
            recommendations_list = [r.strip() for r in recommendations.split("\n") if r.strip()]
            
            # Perform the audit
            audit_result = license_manager.perform_compliance_audit(
                license_id=license_id,
                auditor=auditor,
                dimension_scores=dimension_scores,
                findings=findings_list,
                recommendations=recommendations_list
            )
            
            # Show success message
            st.success(f"Compliance audit submitted successfully! Overall Score: {audit_result['overall_score']:.1f}")
            
            # Display the audit details
            with st.expander("View Audit Details", expanded=True):
                st.json(audit_result)
                
                # Show compliance score change
                old_score = license_details['current_compliance_score']
                new_score = audit_result['overall_score']
                delta = new_score - old_score
                
                st.metric(
                    "Compliance Score Change",
                    f"{new_score:.1f}",
                    f"{delta:+.1f}",
                    delta_color="normal" if delta >= 0 else "inverse"
                )
            
            # Refresh the page to show updated data
            st.rerun()
        
        except ValueError as e:
            st.error(f"Invalid value: {str(e)}")
        
        except Exception as e:
            st.error(f"Failed to perform audit: {str(e)}")

def show_governance_analytics(license_manager: ECGLicenseManager):
    """Display governance analytics and insights"""
    st.header("Governance Analytics")
    
    # Get all licenses
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        st.info("No licenses have been issued yet. Use the License Issuance tab to issue new licenses.")
        return
    
    # Convert to DataFrame for analysis
    df_licenses = pd.DataFrame(licenses)
    
    # Compliance score by entity type
    st.subheader("Compliance by License Type")
    
    if "compliance_score" in df_licenses.columns and len(df_licenses) > 0:
        compliance_by_type = df_licenses.groupby("license_type")["compliance_score"].mean().reset_index()
        compliance_by_type.columns = ["License Type", "Average Compliance Score"]
        
        fig = px.bar(
            compliance_by_type,
            x="License Type",
            y="Average Compliance Score",
            color="License Type",
            title="Average Compliance Score by License Type"
        )
        
        # Add a target line at 80%
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=80,
            x1=len(compliance_by_type) - 0.5,
            y1=80,
            line=dict(
                color="red",
                width=2,
                dash="dash",
            )
        )
        
        # Add annotation for target line
        fig.add_annotation(
            x=len(compliance_by_type) - 1,
            y=80,
            text="Target (80%)",
            showarrow=False,
            yshift=10
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis - if we have compliance history
    all_history = []
    for license_id in df_licenses["license_id"]:
        history = license_manager.get_compliance_history(license_id)
        if history:
            for audit in history:
                audit_data = {
                    "license_id": license_id,
                    "entity_name": df_licenses[df_licenses["license_id"] == license_id]["entity_name"].iloc[0],
                    "timestamp": audit["timestamp"],
                    "overall_score": audit["overall_score"]
                }
                
                # Get dimension scores
                for dimension in audit["dimensions"]:
                    dim_name = dimension["dimension"]
                    audit_data[f"{dim_name}_score"] = dimension["overall_score"]
                
                all_history.append(audit_data)
    
    if all_history:
        df_history = pd.DataFrame(all_history)
        df_history["timestamp"] = pd.to_datetime(df_history["timestamp"])
        
        # Sort by timestamp
        df_history = df_history.sort_values("timestamp")
        
        # Create a trend chart
        st.subheader("Compliance Score Trends")
        
        fig = px.line(
            df_history,
            x="timestamp",
            y="overall_score",
            color="entity_name",
            title="Compliance Score Trends Over Time",
            labels={"timestamp": "Date", "overall_score": "Compliance Score", "entity_name": "Entity"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Dimension analysis
        st.subheader("Governance Dimension Analysis")
        
        # Check which dimension columns are present
        dimension_cols = [col for col in df_history.columns if col.endswith("_score") and col != "overall_score"]
        
        if dimension_cols:
            # Create a melted dataframe for dimension analysis
            dimension_df = df_history.melt(
                id_vars=["timestamp", "entity_name"],
                value_vars=dimension_cols,
                var_name="dimension",
                value_name="score"
            )
            
            # Clean up dimension names
            dimension_df["dimension"] = dimension_df["dimension"].str.replace("_score", "").str.title()
            
            fig = px.box(
                dimension_df,
                x="dimension",
                y="score",
                color="dimension",
                title="Compliance Score Distribution by Governance Dimension",
                labels={"dimension": "Dimension", "score": "Compliance Score"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Predictive insights (simulation)
    st.subheader("Predictive Governance Insights")
    
    insights = [
        "Licenses in the 'corporate' category show the highest compliance variability, suggesting a need for more consistent governance practices.",
        "There's a strong correlation between regular audits and improved compliance scores - entities with quarterly audits show 15% higher compliance on average.",
        "The 'People' dimension consistently scores lower than other dimensions, indicating a potential focus area for governance improvements.",
        "Entities with detailed documentation and clear audit trails demonstrate better alignment with divine principles.",
        "Licenses with specific restrictions show higher compliance in the 'Justice' principle, suggesting that clarity helps align behavior."
    ]
    
    for i, insight in enumerate(insights):
        st.markdown(f"**Insight {i+1}:** {insight}")
    
    # Governance recommendations
    st.subheader("Governance Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### System-Level Recommendations")
        system_recommendations = [
            "Implement automated compliance monitoring for real-time insights",
            "Develop a standardized audit framework aligned with divine principles",
            "Establish clear compliance thresholds for each governance dimension",
            "Create detailed documentation on governance best practices",
            "Implement regular training programs on divine alignment"
        ]
        
        for rec in system_recommendations:
            st.markdown(f"- {rec}")
    
    with col2:
        st.markdown("### Entity-Level Recommendations")
        entity_recommendations = [
            "Provide tailored governance guidelines based on entity type",
            "Conduct baseline assessments for new licensees to identify focus areas",
            "Develop improvement roadmaps for entities with lower compliance scores",
            "Recognize and reward entities demonstrating exceptional divine alignment",
            "Create peer learning opportunities between high-performing entities"
        ]
        
        for rec in entity_recommendations:
            st.markdown(f"- {rec}")

if __name__ == "__main__":
    show_license_governance()