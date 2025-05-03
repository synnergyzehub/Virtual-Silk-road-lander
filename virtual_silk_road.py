#!/usr/bin/env python3
"""
Virtual Silk Road - SynergyzeOS Trading Platform

This module provides a Streamlit-based interface for the Virtual Silk Road
trading platform, which demonstrates the SynergyzeOS licensing ecosystem
within the Genesis Stack.
"""

import os
import json
import time
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Virtual Silk Road | SynergyzeOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
LICENSE_API_URL = "http://localhost:5001"
LICENSE_API_KEY = "emperorkey123"  # Default key for development

def check_license_status(license_id):
    """Check the status of a license with the License API."""
    try:
        response = requests.get(
            f"{LICENSE_API_URL}/api/license/verify/{license_id}",
            headers={"Authorization": f"Bearer {LICENSE_API_KEY}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"valid": False, "message": f"Error: {response.status_code}"}
    except Exception as e:
        return {"valid": False, "message": f"Error connecting to License API: {e}"}

def get_all_licenses():
    """Get all licenses from the License API."""
    try:
        response = requests.get(
            f"{LICENSE_API_URL}/api/license/list",
            headers={"Authorization": f"Bearer {LICENSE_API_KEY}"}
        )
        if response.status_code == 200:
            return response.json().get("licenses", [])
        else:
            st.error(f"Error fetching licenses: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to License API: {e}")
        return []

def load_sample_data():
    """Load sample trading data if not available from API."""
    # Generated trading data with rich structure
    return {
        "trade_routes": [
            {"id": "TR001", "name": "Silk Road Express", "origin": "Beijing", "destination": "Istanbul", "status": "active"},
            {"id": "TR002", "name": "Spice Route", "origin": "Mumbai", "destination": "Alexandria", "status": "active"},
            {"id": "TR003", "name": "Tea Caravan", "origin": "Chengdu", "destination": "Moscow", "status": "pending"},
            {"id": "TR004", "name": "Diamond Path", "origin": "Johannesburg", "destination": "Amsterdam", "status": "active"},
            {"id": "TR005", "name": "Incense Trail", "origin": "Muscat", "destination": "Damascus", "status": "inactive"}
        ],
        "trade_goods": [
            {"id": "TG001", "name": "Premium Silk", "origin": "China", "value_per_unit": 120, "units": "meters"},
            {"id": "TG002", "name": "Saffron", "origin": "Iran", "value_per_unit": 200, "units": "grams"},
            {"id": "TG003", "name": "Porcelain", "origin": "China", "value_per_unit": 50, "units": "pieces"},
            {"id": "TG004", "name": "Spices", "origin": "India", "value_per_unit": 80, "units": "kilograms"},
            {"id": "TG005", "name": "Tea", "origin": "China", "value_per_unit": 40, "units": "kilograms"},
            {"id": "TG006", "name": "Diamonds", "origin": "Africa", "value_per_unit": 5000, "units": "carats"},
            {"id": "TG007", "name": "Incense", "origin": "Arabia", "value_per_unit": 60, "units": "kilograms"}
        ],
        "trading_partners": [
            {"id": "TP001", "name": "Imperial Trading Co.", "region": "China", "reputation": 95},
            {"id": "TP002", "name": "Ottoman Merchants Guild", "region": "Turkey", "reputation": 88},
            {"id": "TP003", "name": "Venetian Exchange", "region": "Italy", "reputation": 92},
            {"id": "TP004", "name": "Mughal Traders Association", "region": "India", "reputation": 85},
            {"id": "TP005", "name": "Russian Fur Company", "region": "Russia", "reputation": 78}
        ]
    }

def load_trade_data():
    """Load historical trade data."""
    # Generate sample historical trade data
    dates = pd.date_range(end=datetime.now(), periods=60, freq='D')
    
    # Create data for multiple trade goods
    goods = ['Silk', 'Spices', 'Tea', 'Porcelain', 'Diamonds']
    data = []
    
    for good in goods:
        # Base value with randomness
        base_value = {
            'Silk': 100,
            'Spices': 80,
            'Tea': 60,
            'Porcelain': 90,
            'Diamonds': 500
        }[good]
        
        # Add some trends and seasonality
        for date in dates:
            value = base_value
            
            # Add trend
            value += (date.dayofyear / 365) * 20
            
            # Add weekly pattern
            value += (date.dayofweek % 7) * 2
            
            # Add some randomness
            value += pd.np.random.normal(0, 10)
            
            # Ensure no negative values
            value = max(value, 0)
            
            data.append({
                'Date': date,
                'Good': good,
                'Value': round(value, 2),
                'Volume': round(pd.np.random.randint(50, 200) * (1 + date.dayofyear / 1000), 0)
            })
    
    return pd.DataFrame(data)

def render_license_status():
    """Render the license status section."""
    st.subheader("SynergyzeOS License Status")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # License verification
        license_id = st.text_input("Enter License ID:", value="SYN-SILK-GLOBAL-250411")
        if st.button("Verify License"):
            with st.spinner("Verifying license..."):
                license_status = check_license_status(license_id)
                if license_status.get("valid"):
                    st.success(f"License {license_id} is valid until {license_status.get('expiry_date')}")
                    st.json(license_status)
                else:
                    st.error(f"License validation failed: {license_status.get('message')}")
    
    with col2:
        # License health indicator
        st.metric(
            label="License Health",
            value="98%",
            delta="2.3%",
            delta_color="normal"
        )
        
        # Active modules
        st.write("Active Modules:")
        st.caption("✅ Commerce Engine")
        st.caption("✅ Governance Layer")
        st.caption("✅ Identity Verification")
        st.caption("✅ Trade Routes")

def render_trade_routes(data):
    """Render the trade routes section."""
    st.subheader("Silk Road Trade Routes")
    
    # Convert trade routes to DataFrame
    routes_df = pd.DataFrame(data["trade_routes"])
    
    # Create world map of trade routes
    fig = go.Figure()
    
    # Define route coordinates (simplified for demo)
    route_coords = {
        "Beijing": (116.4, 39.9),
        "Istanbul": (28.9, 41.0),
        "Mumbai": (72.8, 19.1),
        "Alexandria": (29.9, 31.2),
        "Chengdu": (104.0, 30.7),
        "Moscow": (37.6, 55.7),
        "Johannesburg": (28.0, -26.2),
        "Amsterdam": (4.9, 52.4),
        "Muscat": (58.4, 23.6),
        "Damascus": (36.3, 33.5)
    }
    
    # Add traces for each route
    for _, route in routes_df.iterrows():
        if route["status"] == "active":
            line_color = "rgba(0, 128, 0, 0.7)"
        elif route["status"] == "pending":
            line_color = "rgba(255, 165, 0, 0.7)"
        else:
            line_color = "rgba(169, 169, 169, 0.5)"
        
        # Get coordinates
        origin_coords = route_coords.get(route["origin"])
        dest_coords = route_coords.get(route["destination"])
        
        if origin_coords and dest_coords:
            # Add route line
            fig.add_trace(go.Scattergeo(
                lon=[origin_coords[0], dest_coords[0]],
                lat=[origin_coords[1], dest_coords[1]],
                mode="lines",
                line=dict(width=2, color=line_color),
                name=route["name"],
                hoverinfo="text",
                text=f"{route['name']}: {route['origin']} to {route['destination']} ({route['status']})"
            ))
            
            # Add origin point
            fig.add_trace(go.Scattergeo(
                lon=[origin_coords[0]],
                lat=[origin_coords[1]],
                mode="markers",
                marker=dict(size=8, color="red"),
                name=route["origin"],
                hoverinfo="text",
                text=route["origin"],
                showlegend=False
            ))
            
            # Add destination point
            fig.add_trace(go.Scattergeo(
                lon=[dest_coords[0]],
                lat=[dest_coords[1]],
                mode="markers",
                marker=dict(size=8, color="blue"),
                name=route["destination"],
                hoverinfo="text",
                text=route["destination"],
                showlegend=False
            ))
    
    # Update map layout
    fig.update_geos(
        projection_type="natural earth",
        showcoastlines=True,
        coastlinecolor="black",
        showland=True,
        landcolor="lightgreen",
        showocean=True,
        oceancolor="lightblue",
        showcountries=True,
        countrycolor="black"
    )
    
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(
            y=0.99,
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Route status table
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # More detailed route information
        st.dataframe(routes_df)
    
    with col2:
        # Route status summary
        status_counts = routes_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(
            status_counts,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map={
                'active': 'green',
                'pending': 'orange',
                'inactive': 'gray'
            },
            title="Route Status Distribution"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)

def render_trade_goods(data):
    """Render the trade goods section."""
    st.subheader("Traded Goods")
    
    # Convert trade goods to DataFrame
    goods_df = pd.DataFrame(data["trade_goods"])
    
    # Trade goods visualization
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Bar chart of trade goods by value
        fig = px.bar(
            goods_df, 
            x='name', 
            y='value_per_unit',
            color='origin',
            title="Trade Goods Value Comparison",
            labels={'name': 'Good', 'value_per_unit': 'Value per Unit', 'origin': 'Origin'},
            hover_data=['units']
        )
        
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Trade goods table
        st.dataframe(goods_df)
        
        # Add ability to trade goods (simulated)
        st.write("### Execute Trade")
        
        good = st.selectbox("Select Good:", options=goods_df['name'].tolist())
        quantity = st.number_input("Quantity:", min_value=1, max_value=1000, value=10)
        
        selected_good = goods_df[goods_df['name'] == good].iloc[0]
        trade_value = selected_good['value_per_unit'] * quantity
        
        # Calculate trade fee based on SynergyzeOS license
        trade_fee = trade_value * 0.02  # 2% fee
        
        st.write(f"Trade Value: ${trade_value:,.2f}")
        st.write(f"Trade Fee: ${trade_fee:,.2f}")
        
        if st.button("Execute Trade"):
            # Verify license for commerce operation
            license_status = check_license_status("SYN-SILK-GLOBAL-250411")
            
            if license_status.get("valid"):
                st.success(f"Trade executed: {quantity} {selected_good['units']} of {good}")
                
                # Simulate NPU governance check
                st.info("✅ SynergyzeOS License validated by NPU node")
                st.info("✅ Trade conforms to Ethical Commerce guidelines")
                st.info("✅ Divine Alignment Layer verification passed")
            else:
                st.error("Trade failed: Invalid SynergyzeOS license")
                st.info("❌ License validation failed")
                st.info("❌ Unable to verify with NPU node")

def render_market_trends():
    """Render market trends based on historical data."""
    st.subheader("Market Trends")
    
    # Load historical trade data
    df = load_trade_data()
    
    # Time series chart
    goods = df['Good'].unique()
    selected_goods = st.multiselect("Select Goods to Display:", options=goods, default=goods[:3])
    
    if selected_goods:
        filtered_df = df[df['Good'].isin(selected_goods)]
        
        # Create line chart
        fig = px.line(
            filtered_df,
            x='Date',
            y='Value',
            color='Good',
            title="Historical Prices of Trade Goods",
            labels={'Value': 'Value per Unit', 'Date': 'Date'}
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Value",
            legend_title="Trade Good",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume chart
        fig2 = px.bar(
            filtered_df,
            x='Date',
            y='Volume',
            color='Good',
            title="Trading Volume Over Time",
            labels={'Volume': 'Volume (Units)', 'Date': 'Date'}
        )
        
        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume",
            legend_title="Trade Good",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Please select at least one trade good to display.")

def render_governance_compliance(data):
    """Render governance compliance information."""
    st.subheader("Empire Computational Governance")
    
    # Convert trading partners to DataFrame
    partners_df = pd.DataFrame(data["trading_partners"])
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Partner reputation gauge chart
        fig = go.Figure()
        
        for _, partner in partners_df.iterrows():
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=partner["reputation"],
                title={"text": partner["name"]},
                domain={"x": [0, 1], "y": [0, 0.2 * (5 - _)]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 50], "color": "red"},
                        {"range": [50, 75], "color": "orange"},
                        {"range": [75, 90], "color": "lightgreen"},
                        {"range": [90, 100], "color": "green"}
                    ],
                    "threshold": {
                        "line": {"color": "black", "width": 4},
                        "thickness": 0.75,
                        "value": 90
                    }
                }
            ))
        
        fig.update_layout(height=600, margin=dict(l=50, r=50, t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Computational governance visualization
        st.write("### NPU Governance Layer")
        st.markdown("""
        The Empire Computational Governance layer uses dedicated Neural Processing Units (NPUs) 
        to enforce trading rules and ethical standards through the Divine Alignment Layer.
        
        Each transaction is verified against:
        - **Ethical Commerce Standards**: Ensuring fair trade practices
        - **Jurisdictional Compliance**: Meeting local trade regulations
        - **Divine Alignment**: Conformance to ethical principles
        - **License Validation**: SynergyzeOS license verification
        """)
        
        # Compliance metrics
        metrics = [
            {"name": "Ethical Commerce", "value": 98.2, "threshold": 95},
            {"name": "Jurisdictional Compliance", "value": 100.0, "threshold": 100},
            {"name": "Divine Alignment", "value": 87.5, "threshold": 80},
            {"name": "License Validation", "value": 100.0, "threshold": 100}
        ]
        
        metrics_df = pd.DataFrame(metrics)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics_df["name"],
            y=metrics_df["value"],
            marker_color=[
                "green" if val >= threshold else "orange"
                for val, threshold in zip(metrics_df["value"], metrics_df["threshold"])
            ],
            text=metrics_df["value"].apply(lambda x: f"{x}%"),
            textposition="auto"
        ))
        
        # Add threshold lines
        for i, row in metrics_df.iterrows():
            fig.add_shape(
                type="line",
                x0=i-0.4, x1=i+0.4,
                y0=row["threshold"], y1=row["threshold"],
                line=dict(color="red", width=2, dash="dash")
            )
        
        fig.update_layout(
            title="Governance Compliance Metrics",
            xaxis_title="Metric",
            yaxis_title="Compliance (%)",
            yaxis_range=[0, 105],
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main function to run the Virtual Silk Road app."""
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=SynergyzeOS", width=150)
        st.title("Virtual Silk Road")
        st.caption("SynergyzeOS Trading Platform")
        
        st.write("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Dashboard", "Trading Floor", "Route Management", "License Management", "Governance"]
        )
        
        st.write("---")
        
        # License info
        st.write("### SynergyzeOS License")
        st.info("License: SYN-SILK-GLOBAL-250411")
        st.info("NPU Node: NPU-SILK-001")
        st.info("Status: Active")
        
        # Governance reminder
        st.write("### ECG Oversight")
        st.warning("All trades are validated through the Empire Computational Governance (ECG) layer running on dedicated NPU hardware.")
    
    # Page header
    st.title("Virtual Silk Road Trading Platform")
    st.caption("Powered by SynergyzeOS on the Genesis Stack")
    
    # Load data
    data = load_sample_data()
    
    # Render selected page
    if page == "Dashboard":
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Trade Routes",
                value=len(data["trade_routes"]),
                delta="1",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                label="Active Partners",
                value=len(data["trading_partners"]),
                delta="2",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                label="Trade Goods",
                value=len(data["trade_goods"]),
                delta=None
            )
        
        with col4:
            st.metric(
                label="Divine Alignment",
                value="87.5%",
                delta="3.2%",
                delta_color="normal"
            )
        
        # License status
        render_license_status()
        
        # Trade routes map
        render_trade_routes(data)
        
        # Market trends
        render_market_trends()
    
    elif page == "Trading Floor":
        render_trade_goods(data)
        render_market_trends()
    
    elif page == "Route Management":
        render_trade_routes(data)
    
    elif page == "License Management":
        st.header("SynergyzeOS License Management")
        
        # Display license information
        licenses = get_all_licenses()
        
        if licenses:
            st.write("### Available Licenses")
            licenses_df = pd.DataFrame(licenses)
            st.dataframe(licenses_df)
        else:
            st.warning("No licenses available or unable to connect to License API.")
            
            # Show sample license data
            st.write("### Sample License Data")
            sample_licenses = [
                {
                    "license_id": "SYN-SILK-GLOBAL-250411",
                    "entity_name": "Silk Road Trading Co.",
                    "issue_date": "2025-04-11",
                    "expiry_date": "2026-04-10",
                    "status": "active",
                    "modules": ["commerce", "governance", "identity", "trading"]
                }
            ]
            st.dataframe(pd.DataFrame(sample_licenses))
        
        # License request form
        st.write("### Request New License")
        
        col1, col2 = st.columns(2)
        
        with col1:
            entity_name = st.text_input("Entity Name:", value="Silk Road Trading Co.")
            license_type = st.selectbox("License Type:", ["Standard", "Premium", "Enterprise"])
            
        with col2:
            region = st.text_input("Region:", value="GLOBAL")
            modules = st.multiselect("Modules:", 
                ["Commerce", "Governance", "Identity", "Trading", "Analytics"],
                default=["Commerce", "Governance", "Identity", "Trading"]
            )
        
        if st.button("Request License"):
            with st.spinner("Processing license request..."):
                # Simulate processing time
                time.sleep(2)
                st.success("License request submitted for approval by ECG team.")
                st.info("Your license will be reviewed by the Emperor's Computational Governance team within 24 hours.")
                st.info("You will be notified once your license is approved and assigned to an NPU node.")
    
    elif page == "Governance":
        render_governance_compliance(data)
        
        # Add interactive governance visualization
        st.write("### NPU Node Assignment")
        st.markdown("""
        Your trading operations are governed by dedicated Neural Processing Units (NPUs)
        that enforce computational governance rules and ethical standards.
        
        Current Assignment:
        - **NPU Node**: NPU-SILK-001
        - **Region**: GLOBAL
        - **Divine Alignment Score**: 87.5%
        """)
        
        # NPU health visualization
        npu_health = {
            "CPU": 32,
            "Memory": 64,
            "Storage": 1024,
            "Temperature": 45,
            "Uptime": 732,
            "Governance Rules": 128
        }
        
        st.write("### NPU Node Health")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU Cores", npu_health["CPU"])
            st.metric("Memory (GB)", npu_health["Memory"])
        
        with col2:
            st.metric("Storage (GB)", npu_health["Storage"])
            st.metric("Temperature (°C)", npu_health["Temperature"])
        
        with col3:
            st.metric("Uptime (hours)", npu_health["Uptime"])
            st.metric("Governance Rules", npu_health["Governance Rules"])
        
        # Governance rules visualization
        st.write("### Active Governance Rules")
        
        governance_rules = [
            {"id": "GR001", "name": "Ethical Commerce", "severity": "Critical", "status": "Active"},
            {"id": "GR002", "name": "Fair Trade Practices", "severity": "High", "status": "Active"},
            {"id": "GR003", "name": "Data Sovereignty", "severity": "Critical", "status": "Active"},
            {"id": "GR004", "name": "License Validation", "severity": "Critical", "status": "Active"},
            {"id": "GR005", "name": "Trade Route Validation", "severity": "Medium", "status": "Active"},
            {"id": "GR006", "name": "Partner Reputation Check", "severity": "High", "status": "Active"},
            {"id": "GR007", "name": "Transaction Limits", "severity": "Medium", "status": "Active"},
            {"id": "GR008", "name": "Jurisdictional Compliance", "severity": "High", "status": "Active"}
        ]
        
        rules_df = pd.DataFrame(governance_rules)
        
        # Apply color to severity
        def color_severity(val):
            color_map = {
                "Critical": "background-color: red; color: white",
                "High": "background-color: orange; color: black",
                "Medium": "background-color: yellow; color: black",
                "Low": "background-color: green; color: white"
            }
            return color_map.get(val, "")
        
        st.dataframe(rules_df.style.applymap(color_severity, subset=["severity"]))
    
    # Footer
    st.write("---")
    st.caption("© 2025 SynergyzeOS Trading Platform | Powered by Genesis Stack and NPU Governance")
    st.caption("License validation provided by Empire Computational Governance (ECG) through the SynergyzeOS platform.")

if __name__ == "__main__":
    main()