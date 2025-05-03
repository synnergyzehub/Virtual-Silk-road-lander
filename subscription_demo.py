"""
Subscription Demo for Empire OS

This app demonstrates the freemium model for Empire OS, showcasing data flow
visualization from factory to consumer with different subscription tiers.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import json
import uuid

# Import custom modules
from core.subscription_manager import (
    SubscriptionManager, SubscriptionTier, FeatureAccess, SUBSCRIPTION_PRICING
)
from core.data_flow import DataFlowManager, DataFlowStage

# Constants
CLIENT_ID_KEY = "client_id"
SUBSCRIPTION_TIER_KEY = "subscription_tier"

# Initialize managers
subscription_manager = SubscriptionManager()
data_flow_manager = DataFlowManager()

# Page configuration
st.set_page_config(
    page_title="Empire OS Subscription Demo",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to ensure client ID is available
def ensure_client_id():
    if CLIENT_ID_KEY not in st.session_state:
        # Generate a unique client ID for this session
        st.session_state[CLIENT_ID_KEY] = f"demo_{uuid.uuid4().hex[:8]}"
        
        # Create a free demo subscription for this client
        subscription_manager.create_subscription(
            client_id=st.session_state[CLIENT_ID_KEY],
            tier=SubscriptionTier.FREE_DEMO.value
        )
        
        # Set the subscription tier in session state
        st.session_state[SUBSCRIPTION_TIER_KEY] = SubscriptionTier.FREE_DEMO.value

# Function to get feature access for current client
def get_feature_access(feature_name):
    client_id = st.session_state.get(CLIENT_ID_KEY)
    if not client_id:
        return FeatureAccess.NONE
    
    access = subscription_manager.check_feature_access(client_id, feature_name)
    return access

# Function to check if feature is accessible
def can_access_feature(feature_name, min_access=FeatureAccess.LIMITED):
    access = get_feature_access(feature_name)
    return access.value >= min_access.value

# Function to render subscription banner
def render_subscription_banner():
    current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
    
    if current_tier == SubscriptionTier.FREE_DEMO.value:
        st.sidebar.warning(
            "💎 **Free Demo Mode** 💎\n\n"
            "You are currently using the free demo version with limited access. "
            "Upgrade to unlock full features and comprehensive insights."
        )
        upgrade_col1, upgrade_col2 = st.sidebar.columns(2)
        with upgrade_col1:
            st.button("Upgrade to Basic", key="upgrade_basic", on_click=lambda: set_subscription_tier(SubscriptionTier.BASIC.value))
        with upgrade_col2:
            st.button("Upgrade to Premium", key="upgrade_premium", on_click=lambda: set_subscription_tier(SubscriptionTier.PREMIUM.value))
    elif current_tier == SubscriptionTier.BASIC.value:
        st.sidebar.info(
            "💼 **Basic Subscription** 💼\n\n"
            "You have access to data organization features and basic analytics. "
            "Upgrade to Premium for advanced features."
        )
        st.sidebar.button("Upgrade to Premium", key="upgrade_to_premium", on_click=lambda: set_subscription_tier(SubscriptionTier.PREMIUM.value))
    else:  # Premium
        st.sidebar.success(
            "👑 **Premium Subscription** 👑\n\n"
            "You have full access to all Empire OS features and divine governance capabilities."
        )

# Function to set subscription tier
def set_subscription_tier(tier):
    st.session_state[SUBSCRIPTION_TIER_KEY] = tier
    client_id = st.session_state.get(CLIENT_ID_KEY)
    if client_id:
        subscription_manager.update_subscription(client_id, tier=tier)

# Function to create flow visualization
def create_flow_visualization():
    # Get current subscription tier
    current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
    
    # Determine access level based on tier
    access_level = {
        SubscriptionTier.FREE_DEMO.value: "limited",
        SubscriptionTier.BASIC.value: "partial",
        SubscriptionTier.PREMIUM.value: "full"
    }.get(current_tier, "limited")
    
    # Get flow stages and connections
    stages = data_flow_manager.get_all_flow_stages()
    connections = data_flow_manager.get_flow_connections(access_level)
    
    # Create nodes for the Sankey diagram
    nodes = []
    for stage_id, stage_info in stages.items():
        nodes.append(stage_info["name"])
    
    # Create links for the Sankey diagram
    links_source = []
    links_target = []
    links_value = []
    links_color = []
    
    # Map stage IDs to node indices
    stage_to_index = {stage_id: i for i, stage_id in enumerate(stages.keys())}
    
    # Add connections
    for conn in connections:
        source_idx = stage_to_index[conn["from"]]
        target_idx = stage_to_index[conn["to"]]
        
        # Generate a random value for flow volume
        value = np.random.randint(1, 100)
        
        links_source.append(source_idx)
        links_target.append(target_idx)
        links_value.append(value)
        
        # Add a color based on access level
        if access_level == "limited":
            links_color.append("rgba(44, 160, 44, 0.5)")  # Green with transparency
        elif access_level == "partial":
            links_color.append("rgba(31, 119, 180, 0.6)")  # Blue with transparency
        else:  # full
            links_color.append("rgba(214, 39, 40, 0.6)")  # Red with transparency
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="blue"
        ),
        link=dict(
            source=links_source,
            target=links_target,
            value=links_value,
            color=links_color
        )
    )])
    
    # Update layout
    fig.update_layout(
        title_text=f"Data Flow Visualization ({access_level.capitalize()} Access)",
        font_size=12,
        height=500
    )
    
    return fig

# Function to display flow stage details
def display_flow_stage_details(stage_id):
    # Get current subscription tier
    current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
    
    # Determine access level based on tier
    access_level = {
        SubscriptionTier.FREE_DEMO.value: "limited",
        SubscriptionTier.BASIC.value: "partial",
        SubscriptionTier.PREMIUM.value: "full"
    }.get(current_tier, "limited")
    
    # Get stage info
    stage_info = data_flow_manager.get_flow_stage(stage_id)
    if not stage_info:
        st.error(f"Stage information not found for: {stage_id}")
        return
    
    # Display stage information
    st.subheader(stage_info["name"])
    st.write(stage_info["description"])
    
    # Generate flow data
    client_id = st.session_state.get(CLIENT_ID_KEY)
    if not client_id:
        st.warning("Client ID not found. Session may have expired.")
        return
    
    flow_data = data_flow_manager.generate_sample_flow_data(
        client_id=client_id,
        stage=stage_id,
        access_level=access_level
    )
    
    # Extract stage data
    stage_data = flow_data["stages"].get(stage_id, {}).get("data", [])
    if not stage_data:
        st.warning(f"No data available for {stage_info['name']}.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(stage_data)
    
    # Prepare date column
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    
    # Display metrics over time
    st.subheader("Metrics Over Time")
    
    # Create multi-line chart with available metrics
    metrics = [col for col in df.columns if col != "date"]
    fig = px.line(
        df, x="date", y=metrics,
        title=f"{stage_info['name']} Metrics",
        labels={"date": "Date", "value": "Score", "variable": "Metric"}
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Score (0-100)",
        legend_title="Metrics",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display insights (if available)
    insights = flow_data["stages"].get(stage_id, {}).get("insights", [])
    if insights and access_level in ["partial", "full"]:
        st.subheader("Key Insights")
        
        # Create columns for insights
        cols = st.columns(min(len(insights), 2))
        
        for i, insight in enumerate(insights):
            col_idx = i % len(cols)
            with cols[col_idx]:
                st.metric(
                    label=insight["text"],
                    value=f"{insight['value']}%",
                    delta=f"Impact: {insight['impact']}/5"
                )
    
    # Display divine insights
    divine_insights = data_flow_manager.get_divine_insights(
        stage=stage_id,
        access_level=access_level
    )
    
    stage_divine = divine_insights.get(stage_id, {})
    if stage_divine:
        st.subheader("Divine Alignment Analysis")
        
        # Display base score
        st.metric(
            label="Divine Alignment Score",
            value=f"{stage_divine.get('divine_alignment_score', 0)}%",
            delta=None
        )
        
        # Display detailed dimensions for partial and full access
        dimensions = stage_divine.get("dimensions", {})
        if isinstance(dimensions, dict) and access_level in ["partial", "full"]:
            if access_level == "partial":
                # Display as metrics
                dim_cols = st.columns(len(dimensions))
                for i, (dim_name, dim_score) in enumerate(dimensions.items()):
                    dim_cols[i].metric(
                        label=dim_name,
                        value=f"{dim_score}%",
                        delta=None
                    )
            else:  # full access
                # Display as expandable sections with components
                for dim_name, dim_data in dimensions.items():
                    if isinstance(dim_data, dict):
                        with st.expander(f"{dim_name}: {dim_data.get('score', 0)}%"):
                            components = dim_data.get("components", {})
                            comp_cols = st.columns(len(components))
                            for i, (comp_name, comp_score) in enumerate(components.items()):
                                comp_cols[i].metric(
                                    label=comp_name,
                                    value=f"{comp_score}%",
                                    delta=None
                                )
            
        # Display recommendations for full access
        recommendations = stage_divine.get("recommendations", [])
        if recommendations and access_level == "full":
            st.subheader("Divine Governance Recommendations")
            for rec in recommendations:
                st.info(
                    f"**{rec['dimension']} ({rec['score']}%)**: {rec['text']} "
                    f"Potential improvement: **{rec['potential_improvement']}%**"
                )

# Function to display pricing comparison
def display_pricing_comparison():
    st.header("Subscription Tiers")
    
    # Get pricing info
    pricing = SUBSCRIPTION_PRICING
    
    # Create columns for tiers
    free_col, basic_col, premium_col = st.columns(3)
    
    # Free Demo Tier
    with free_col:
        st.subheader("Free Demo")
        st.write("Experience the basics")
        st.write("### $0 /month")
        st.write(pricing[SubscriptionTier.FREE_DEMO.value]["description"])
        st.write("#### Features:")
        st.write("✅ Limited data flow visualization")
        st.write("✅ Basic divine alignment score")
        st.write("✅ Sample insights demonstration")
        st.write("❌ No data integration")
        st.write("❌ No custom reporting")
        
        current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
        if current_tier == SubscriptionTier.FREE_DEMO.value:
            st.success("**Current Plan**")
        else:
            st.button("Downgrade to Free", key="downgrade_free", on_click=lambda: set_subscription_tier(SubscriptionTier.FREE_DEMO.value))
    
    # Basic Tier
    with basic_col:
        st.subheader("Basic")
        st.write("Organize your data")
        st.write(f"### ${pricing[SubscriptionTier.BASIC.value]['monthly']} /month")
        st.write(pricing[SubscriptionTier.BASIC.value]["description"])
        st.write("#### Features:")
        st.write("✅ Enhanced data flow visualization")
        st.write("✅ Partial divine alignment analysis")
        st.write("✅ Data integration for one stream")
        st.write("✅ Monthly insights report")
        st.write("❌ No multi-source integration")
        
        current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
        if current_tier == SubscriptionTier.BASIC.value:
            st.success("**Current Plan**")
        else:
            st.button("Switch to Basic", key="switch_basic", on_click=lambda: set_subscription_tier(SubscriptionTier.BASIC.value))
    
    # Premium Tier
    with premium_col:
        st.subheader("Premium")
        st.write("Full divine governance")
        st.write(f"### ${pricing[SubscriptionTier.PREMIUM.value]['monthly']} /month")
        st.write(pricing[SubscriptionTier.PREMIUM.value]["description"])
        st.write("#### Features:")
        st.write("✅ Complete data flow visualization")
        st.write("✅ Comprehensive divine governance")
        st.write("✅ Multi-source data integration")
        st.write("✅ Advanced analytics and insights")
        st.write("✅ Custom reporting and recommendations")
        
        current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
        if current_tier == SubscriptionTier.PREMIUM.value:
            st.success("**Current Plan**")
        else:
            st.button("Upgrade to Premium", key="upgrade_premium_main", on_click=lambda: set_subscription_tier(SubscriptionTier.PREMIUM.value))

# Function to display feature comparison table
def display_feature_comparison():
    st.header("Feature Comparison")
    
    # Get tier comparison data
    comparison = subscription_manager.get_tier_comparison()
    
    # Convert to DataFrame for display
    data = []
    for feature, tiers in comparison.items():
        row = {"Feature": feature}
        row.update(tiers)
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Replace access level names with symbols
    df = df.replace({
        "NONE": "❌",
        "LIMITED": "⭐",
        "PARTIAL": "⭐⭐",
        "FULL": "⭐⭐⭐"
    })
    
    # Display the table
    st.table(df)

# Function to display subscription form
def display_subscription_form():
    st.header("Contact Us for Enterprise Licenses")
    
    with st.form("subscription_form"):
        company_name = st.text_input("Company Name")
        contact_name = st.text_input("Contact Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        
        tier_options = ["Basic", "Premium", "Enterprise (Custom)"]
        selected_tier = st.selectbox("Interested in Tier", tier_options)
        
        message = st.text_area("Additional Information")
        
        submitted = st.form_submit_button("Request Information")
        
        if submitted:
            st.success("Thank you for your interest! Our ECG licensing team will contact you shortly.")
            
            # Log the form submission (in a real app, this would send the data)
            if not os.path.exists("data/leads"):
                os.makedirs("data/leads")
                
            lead_data = {
                "timestamp": datetime.now().isoformat(),
                "company_name": company_name,
                "contact_name": contact_name,
                "email": email,
                "phone": phone,
                "interested_tier": selected_tier,
                "message": message
            }
            
            with open(f"data/leads/lead_{uuid.uuid4().hex[:8]}.json", "w") as f:
                json.dump(lead_data, f, indent=2)

# Main app function
def main():
    """
    Empire OS Subscription Demo
    
    Demonstrates the freemium model for Empire OS with data flow visualization
    from factory to consumer.
    """
    # Ensure client ID is available
    ensure_client_id()
    
    # Display header
    st.title("Empire OS Divine Mechanics")
    st.markdown("##### Data Flow Visualization & Governance Demo")
    
    # Sidebar
    with st.sidebar:
        st.title("Empire OS")
        
        # Display emojis instead of an image for the logo
        st.markdown("<h1 style='text-align: center; color: gold;'>🏛️👑</h1>", unsafe_allow_html=True)
        
        # Display current subscription info
        render_subscription_banner()
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Select a page",
            ["Flow Visualization", "Factory Analysis", "Distribution Analysis", 
             "Store Analysis", "Consumer Analysis", "Subscription Plans"],
            key="page_selection"
        )
        
        st.divider()
        
        # Display client info
        client_id = st.session_state.get(CLIENT_ID_KEY, "Unknown")
        st.caption(f"Demo Client ID: {client_id}")
    
    # Main content
    if page == "Flow Visualization":
        st.header("Data Flow Visualization")
        st.write(
            "This visualization shows how data flows through your supply chain from "
            "factory production to consumer experience. The width of each connection "
            "represents the volume of data flowing between stages."
        )
        
        # Display the flow visualization
        flow_fig = create_flow_visualization()
        st.plotly_chart(flow_fig, use_container_width=True)
        
        # Display notes based on subscription tier
        current_tier = st.session_state.get(SUBSCRIPTION_TIER_KEY, SubscriptionTier.FREE_DEMO.value)
        
        if current_tier == SubscriptionTier.FREE_DEMO.value:
            st.info(
                "**Free Demo Limitations**: You're viewing a simplified visualization "
                "with limited connections and basic metrics. Upgrade for a comprehensive view."
            )
        elif current_tier == SubscriptionTier.BASIC.value:
            st.info(
                "**Basic Subscription**: You have access to enhanced visualizations "
                "with more connections and metrics. Upgrade to Premium for the complete picture."
            )
        else:  # Premium
            st.success(
                "**Premium Access**: You're viewing the complete data flow visualization "
                "with all connections and comprehensive metrics."
            )
    
    elif page == "Factory Analysis":
        display_flow_stage_details(DataFlowStage.FACTORY.value)
    
    elif page == "Distribution Analysis":
        display_flow_stage_details(DataFlowStage.DISTRIBUTION.value)
    
    elif page == "Store Analysis":
        display_flow_stage_details(DataFlowStage.STORE.value)
    
    elif page == "Consumer Analysis":
        display_flow_stage_details(DataFlowStage.CONSUMER.value)
    
    elif page == "Subscription Plans":
        st.header("Empire OS Subscription Plans")
        st.write(
            "Choose the right subscription plan to unlock the full potential of "
            "the Empire OS divine mechanics and data governance platform."
        )
        
        # Display pricing comparison
        display_pricing_comparison()
        
        st.divider()
        
        # Display feature comparison
        display_feature_comparison()
        
        st.divider()
        
        # Display subscription form
        display_subscription_form()


if __name__ == "__main__":
    main()