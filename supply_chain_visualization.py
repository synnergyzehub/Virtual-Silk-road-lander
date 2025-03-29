import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from database import get_db_session, Order, Style, Material, ProductionEntry, ProductionLine, LineAllocation

def show_supply_chain_visualization():
    """Display supply chain visualization and end-to-end process flow"""
    st.title("Supply Chain Visualization & Automation")
    
    tabs = st.tabs(["📊 SCM Dashboard", "🔄 End-to-End Process Flow", "🚚 Logistics Tracking", "📱 Automated Notifications", "🤖 Process Automation"])
    
    with tabs[0]:
        show_scm_dashboard()
    
    with tabs[1]:
        show_process_flow()
    
    with tabs[2]:
        show_logistics_tracking()
    
    with tabs[3]:
        show_notifications_center()
    
    with tabs[4]:
        show_process_automation()

def show_scm_dashboard():
    """Show Supply Chain Management Dashboard with KPIs and visualizations"""
    st.header("Supply Chain Management Dashboard")
    
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="On-time Delivery", value="92%", delta="3%")
    
    with col2:
        st.metric(label="Inventory Turnover", value="4.2x", delta="-0.3x")
    
    with col3:
        st.metric(label="Material Utilization", value="87%", delta="2%")
    
    with col4:
        st.metric(label="Cost Savings", value="₹18.5L", delta="₹2.3L")
    
    st.subheader("Supply Chain Network")
    
    # Create supply chain network diagram
    # Simple network diagram that shows the flow from raw materials to retail
    fig = go.Figure()
    
    # Nodes
    nodes = {
        "raw_materials": {"name": "Raw Materials", "x": 0, "y": 2, "size": 20, "color": "blue"},
        "spinners": {"name": "Spinners & Weavers", "x": 1, "y": 3, "size": 20, "color": "orange"},
        "denim_mills": {"name": "Denim Mills", "x": 2, "y": 2, "size": 25, "color": "indigo"},
        "scotts": {"name": "Scotts Garments", "x": 3, "y": 2, "size": 30, "color": "green"},
        "warehouse": {"name": "Voi Distribution Center", "x": 4, "y": 2, "size": 25, "color": "red"},
        "stores": {"name": "Retail Stores", "x": 5, "y": 1, "size": 20, "color": "purple"},
        "online": {"name": "Online Channels", "x": 5, "y": 3, "size": 20, "color": "pink"}
    }
    
    # Add nodes
    for node_id, node in nodes.items():
        fig.add_trace(go.Scatter(
            x=[node["x"]], 
            y=[node["y"]],
            mode='markers+text',
            marker=dict(size=node["size"], color=node["color"]),
            text=[node["name"]],
            textposition="bottom center",
            name=node["name"],
            hoverinfo="text",
            hovertext=f"{node['name']}"
        ))
    
    # Add edges
    edges = [
        ("raw_materials", "spinners"),
        ("raw_materials", "denim_mills"),
        ("spinners", "denim_mills"),
        ("denim_mills", "scotts"),
        ("scotts", "warehouse"),
        ("warehouse", "stores"),
        ("warehouse", "online")
    ]
    
    for edge in edges:
        source = nodes[edge[0]]
        target = nodes[edge[1]]
        
        fig.add_trace(go.Scatter(
            x=[source["x"], target["x"]],
            y=[source["y"], target["y"]],
            mode='lines',
            line=dict(width=2, color='rgba(150, 150, 150, 0.5)'),
            hoverinfo='none',
            showlegend=False
        ))
    
    fig.update_layout(
        title="Voi Jeans Supply Chain Network",
        showlegend=False,
        height=400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(240, 240, 240, 0.8)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Time Analysis")
        
        # Create lead time analysis chart
        process_steps = ['Order Creation', 'Material Sourcing', 'Production', 'Quality Check', 'Transportation', 'Delivery']
        baseline_times = [3, 25, 15, 3, 5, 1]
        actual_times = [2, 22, 13, 4, 4, 1]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Baseline (days)',
            x=process_steps,
            y=baseline_times,
            marker_color='indianred'
        ))
        
        fig.add_trace(go.Bar(
            name='Actual (days)',
            x=process_steps,
            y=actual_times,
            marker_color='lightseagreen'
        ))
        
        fig.update_layout(
            barmode='group',
            height=350,
            xaxis_title="Process Step",
            yaxis_title="Days"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Raw Material Cost Trends")
        
        # Create raw material cost trend chart
        dates = pd.date_range(start='2025-01-01', periods=12, freq='M')
        cotton_prices = [180, 185, 183, 189, 195, 200, 205, 208, 210, 205, 200, 195]
        polyester_prices = [120, 122, 125, 130, 135, 133, 130, 128, 125, 123, 120, 118]
        dyestuff_prices = [300, 305, 310, 315, 320, 325, 330, 333, 335, 330, 325, 320]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=cotton_prices,
            mode='lines+markers',
            name='Cotton (₹/kg)'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=polyester_prices,
            mode='lines+markers',
            name='Polyester (₹/kg)'
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=dyestuff_prices,
            mode='lines+markers',
            name='Dyestuff (₹/kg)'
        ))
        
        fig.update_layout(
            height=350,
            xaxis_title="Month",
            yaxis_title="Price (₹/kg)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Inventory status
    st.subheader("Inventory Status")
    
    inventory_data = {
        "Raw Denim": {"Current": 12500, "Min": 5000, "Max": 20000, "UOM": "meters", "Status": "Optimal"},
        "Buttons": {"Current": 25000, "Min": 10000, "Max": 30000, "UOM": "pieces", "Status": "Optimal"},
        "Zippers": {"Current": 8000, "Min": 10000, "Max": 30000, "UOM": "pieces", "Status": "Low"},
        "Rivets": {"Current": 35000, "Min": 15000, "Max": 40000, "UOM": "pieces", "Status": "Optimal"},
        "Pocket Fabric": {"Current": 3000, "Min": 2000, "Max": 10000, "UOM": "meters", "Status": "Optimal"},
        "Thread": {"Current": 500, "Min": 300, "Max": 1000, "UOM": "spools", "Status": "Optimal"},
    }
    
    # Convert to DataFrame
    inventory_df = pd.DataFrame.from_dict(inventory_data, orient='index')
    inventory_df = inventory_df.reset_index().rename(columns={"index": "Material"})
    
    # Add color coding
    def get_status_color(status):
        if status == "Low":
            return "background-color: yellow"
        elif status == "Critical":
            return "background-color: red; color: white"
        else:
            return "background-color: lightgreen"
    
    # Show the inventory table with styling
    st.dataframe(inventory_df.style.applymap(
        lambda _: get_status_color("Low"), 
        subset=pd.IndexSlice[inventory_df[inventory_df["Status"] == "Low"].index, ["Status"]]
    ).applymap(
        lambda _: get_status_color("Critical"), 
        subset=pd.IndexSlice[inventory_df[inventory_df["Status"] == "Critical"].index, ["Status"]]
    ).applymap(
        lambda _: get_status_color("Optimal"), 
        subset=pd.IndexSlice[inventory_df[inventory_df["Status"] == "Optimal"].index, ["Status"]]
    ))
    
    # Action items
    st.subheader("Action Items")
    
    action_items = [
        "📋 Place order for 15,000 zippers by end of week",
        "📊 Review cotton price trends for upcoming purchases",
        "🚚 Confirm shipment schedule with Scotts Garments",
        "⚙️ Optimize inventory levels for pocket fabric"
    ]
    
    for item in action_items:
        st.markdown(f"- {item}")

def show_process_flow():
    """Show end-to-end process flow visualization"""
    st.header("End-to-End Process Flow")
    
    # Process flow diagram
    stages = [
        {"name": "Design & Development", "steps": ["Market Research", "Trend Analysis", "Design Creation", "Sample Development", "Design Approval"]},
        {"name": "Raw Material Sourcing", "steps": ["Material Planning", "Vendor Selection", "Price Negotiation", "PO Creation", "Material Testing"]},
        {"name": "Manufacturing", "steps": ["Pattern Making", "Cutting", "Sewing", "Washing", "Finishing", "Quality Check"]},
        {"name": "Logistics", "steps": ["Packaging", "Warehouse Receipt", "Inventory Management", "Distribution Planning"]},
        {"name": "Retail Distribution", "steps": ["Store Allocation", "E-commerce Integration", "Retail Display", "Sales Analysis"]}
    ]
    
    # Define the current active step for the demo
    current_stage = 2  # Manufacturing
    current_step = 3   # Washing
    
    # Display the process flow
    for i, stage in enumerate(stages):
        st.subheader(f"{i+1}. {stage['name']}")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if i < current_stage:
                st.markdown("✅")
            elif i == current_stage:
                st.markdown("🔄")
            else:
                st.markdown("⏳")
        
        with col2:
            step_cols = st.columns(len(stage["steps"]))
            
            for j, step in enumerate(stage["steps"]):
                with step_cols[j]:
                    if i < current_stage or (i == current_stage and j < current_step):
                        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #90EE90; border-radius: 5px;'>{step}<br>✅</div>", unsafe_allow_html=True)
                    elif i == current_stage and j == current_step:
                        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #ADD8E6; border-radius: 5px;'>{step}<br>🔄</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #F5F5F5; border-radius: 5px;'>{step}<br>⏳</div>", unsafe_allow_html=True)
    
    # Timeline visualization
    st.subheader("Project Timeline")
    
    # Create sample timeline data
    today = datetime.now().date()
    timeline_data = {
        "Design & Development": {"start": today - timedelta(days=90), "end": today - timedelta(days=60), "status": "Completed"},
        "Raw Material Sourcing": {"start": today - timedelta(days=70), "end": today - timedelta(days=30), "status": "Completed"},
        "Manufacturing": {"start": today - timedelta(days=30), "end": today + timedelta(days=15), "status": "In Progress"},
        "Logistics": {"start": today + timedelta(days=10), "end": today + timedelta(days=25), "status": "Planned"},
        "Retail Distribution": {"start": today + timedelta(days=20), "end": today + timedelta(days=40), "status": "Planned"}
    }
    
    # Convert to DataFrame
    timeline_df = pd.DataFrame([
        dict(Task=task, Start=data["start"], Finish=data["end"], Status=data["status"]) 
        for task, data in timeline_data.items()
    ])
    
    # Create gantt chart
    fig = px.timeline(
        timeline_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Status",
        color_discrete_map={"Completed": "green", "In Progress": "blue", "Planned": "gray"}
    )
    
    fig.update_layout(
        title="SS25 Collection Timeline",
        xaxis_title="Date",
        yaxis_title="Phase",
        height=400
    )
    
    # Add vertical line for today
    fig.add_vline(x=today, line_width=2, line_dash="dash", line_color="red", annotation_text="Today")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Process dependencies
    st.subheader("Process Dependencies & Critical Path")
    
    # Display critical path
    critical_path = [
        {"Task": "Style Finalization", "Duration": "15 days", "Predecessors": "None", "On Critical Path": "Yes"},
        {"Task": "Fabric Booking", "Duration": "7 days", "Predecessors": "Style Finalization", "On Critical Path": "Yes"},
        {"Task": "Fabric Production", "Duration": "30 days", "Predecessors": "Fabric Booking", "On Critical Path": "Yes"},
        {"Task": "Fabric Testing", "Duration": "5 days", "Predecessors": "Fabric Production", "On Critical Path": "No"},
        {"Task": "Pattern Making", "Duration": "10 days", "Predecessors": "Style Finalization", "On Critical Path": "No"},
        {"Task": "Cutting", "Duration": "7 days", "Predecessors": "Fabric Production, Pattern Making", "On Critical Path": "Yes"},
        {"Task": "Sewing", "Duration": "14 days", "Predecessors": "Cutting", "On Critical Path": "Yes"},
        {"Task": "Washing", "Duration": "5 days", "Predecessors": "Sewing", "On Critical Path": "Yes"},
        {"Task": "Finishing", "Duration": "3 days", "Predecessors": "Washing", "On Critical Path": "Yes"},
        {"Task": "Quality Check", "Duration": "2 days", "Predecessors": "Finishing", "On Critical Path": "Yes"},
        {"Task": "Packing", "Duration": "3 days", "Predecessors": "Quality Check", "On Critical Path": "Yes"},
        {"Task": "Shipping", "Duration": "5 days", "Predecessors": "Packing", "On Critical Path": "Yes"}
    ]
    
    # Convert to DataFrame
    critical_path_df = pd.DataFrame(critical_path)
    
    # Format the table
    def highlight_critical_path(x):
        if x == "Yes":
            return "background-color: #FFD700"
        return ""
    
    st.dataframe(critical_path_df.style.applymap(highlight_critical_path, subset=["On Critical Path"]))
    
    # Add a note about the critical path
    st.info("The critical path represents the sequence of dependent tasks that determine the minimum time needed to complete the project. Any delay in critical path tasks will delay the entire project.")

def show_logistics_tracking():
    """Show logistics tracking visualization"""
    st.header("Logistics Tracking")
    
    # Map showing current shipments
    st.subheader("Current Shipments Tracking")
    
    # Create shipment tracking data
    shipments = [
        {"id": "SHP-2025-001", "origin": "Scotts Garments, Bangalore", "destination": "Voi DC, Mumbai", "status": "In Transit", "lat_origin": 12.9716, "lon_origin": 77.5946, "lat_dest": 19.0760, "lon_dest": 72.8777, "progress": 60, "eta": "Apr 2, 2025"},
        {"id": "SHP-2025-002", "origin": "Voi DC, Mumbai", "destination": "Flagship Store, Delhi", "status": "Delivered", "lat_origin": 19.0760, "lon_origin": 72.8777, "lat_dest": 28.7041, "lon_dest": 77.1025, "progress": 100, "eta": "Mar 29, 2025"},
        {"id": "SHP-2025-003", "origin": "Denim Mill, Ahmedabad", "destination": "Scotts Garments, Bangalore", "status": "In Transit", "lat_origin": 23.0225, "lon_origin": 72.5714, "lat_dest": 12.9716, "lon_dest": 77.5946, "progress": 30, "eta": "Apr 5, 2025"}
    ]
    
    # India coordinates
    center_lat = 20.5937
    center_lon = 78.9629
    
    # Create map
    fig = go.Figure(go.Scattermapbox())
    
    # Add origin and destination markers
    for shipment in shipments:
        # Origin marker
        fig.add_trace(go.Scattermapbox(
            lat=[shipment["lat_origin"]],
            lon=[shipment["lon_origin"]],
            mode='markers',
            marker=dict(size=12, color='blue'),
            text=[f"Origin: {shipment['origin']}"],
            name=f"Origin: {shipment['id']}"
        ))
        
        # Destination marker
        fig.add_trace(go.Scattermapbox(
            lat=[shipment["lat_dest"]],
            lon=[shipment["lon_dest"]],
            mode='markers',
            marker=dict(size=12, color='red'),
            text=[f"Destination: {shipment['destination']}"],
            name=f"Destination: {shipment['id']}"
        ))
        
        # Line connecting origin and destination
        # Calculate intermediate point for in-transit shipments
        if shipment["status"] == "In Transit":
            progress_fraction = shipment["progress"] / 100
            intermediate_lat = shipment["lat_origin"] + (shipment["lat_dest"] - shipment["lat_origin"]) * progress_fraction
            intermediate_lon = shipment["lon_origin"] + (shipment["lon_dest"] - shipment["lon_origin"]) * progress_fraction
            
            # Add current position marker
            fig.add_trace(go.Scattermapbox(
                lat=[intermediate_lat],
                lon=[intermediate_lon],
                mode='markers',
                marker=dict(size=10, color='green'),
                text=[f"Current Position: {shipment['id']}"],
                name=f"Current: {shipment['id']}"
            ))
            
            # Add lines for progress
            fig.add_trace(go.Scattermapbox(
                lat=[shipment["lat_origin"], intermediate_lat],
                lon=[shipment["lon_origin"], intermediate_lon],
                mode='lines',
                line=dict(width=3, color='green'),
                text=f"Completed: {shipment['progress']}%",
                name=f"Completed Path: {shipment['id']}"
            ))
            
            fig.add_trace(go.Scattermapbox(
                lat=[intermediate_lat, shipment["lat_dest"]],
                lon=[intermediate_lon, shipment["lon_dest"]],
                mode='lines',
                line=dict(width=3, color='gray', dash='dash'),
                text=f"Remaining: {100 - shipment['progress']}%",
                name=f"Remaining Path: {shipment['id']}"
            ))
        else:
            # For delivered shipments, show complete line
            fig.add_trace(go.Scattermapbox(
                lat=[shipment["lat_origin"], shipment["lat_dest"]],
                lon=[shipment["lon_origin"], shipment["lon_dest"]],
                mode='lines',
                line=dict(width=3, color='green'),
                text=f"Completed: 100%",
                name=f"Completed Path: {shipment['id']}"
            ))
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Shipment details table
    st.subheader("Shipment Details")
    
    # Convert to DataFrame for display
    shipments_display = [
        {"Shipment ID": s["id"], 
         "Origin": s["origin"], 
         "Destination": s["destination"], 
         "Status": s["status"], 
         "Progress": f"{s['progress']}%", 
         "ETA": s["eta"]} 
        for s in shipments
    ]
    shipments_df = pd.DataFrame(shipments_display)
    
    # Apply styling
    def color_status(val):
        color_map = {
            "In Transit": "background-color: yellow",
            "Delivered": "background-color: lightgreen",
            "Delayed": "background-color: red; color: white"
        }
        return color_map.get(val, "")
    
    st.dataframe(shipments_df.style.applymap(color_status, subset=["Status"]))
    
    # Delivery performance
    st.subheader("Delivery Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # On-time delivery performance chart
        months = ['Jan', 'Feb', 'Mar']
        on_time = [89, 91, 92]
        delayed = [11, 9, 8]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='On Time',
            x=months,
            y=on_time,
            marker_color='green'
        ))
        
        fig.add_trace(go.Bar(
            name='Delayed',
            x=months,
            y=delayed,
            marker_color='red'
        ))
        
        fig.update_layout(
            title="Delivery Performance (2025)",
            barmode='stack',
            height=350,
            yaxis=dict(title='Percentage (%)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Reason for delays pie chart
        delay_reasons = ['Weather conditions', 'Production delays', 'Documentation issues', 'Customs clearance', 'Transportation issues']
        delay_percentages = [15, 35, 10, 20, 20]
        
        fig = go.Figure(data=[go.Pie(
            labels=delay_reasons,
            values=delay_percentages,
            hole=.3
        )])
        
        fig.update_layout(
            title="Reasons for Delay (Q1 2025)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_notifications_center():
    """Show automated notifications center"""
    st.header("Automated Notifications Center")
    
    # Tab for different notification types
    notification_tabs = st.tabs(["📱 SMS Notifications", "📧 Email Alerts", "📊 Dashboard Alerts", "⚙️ Configuration"])
    
    with notification_tabs[0]:
        st.subheader("SMS Notification System")
        
        # Sample SMS templates
        sms_templates = [
            {"name": "Material Shortage Alert", "template": "ALERT: Material shortage detected for {material_name}. Current level: {current_level} {uom}. Please reorder immediately. -Voi SCM System", "recipients": "Procurement Team", "trigger": "Inventory below threshold"},
            {"name": "Shipment Status Update", "template": "Shipment {shipment_id} is now {status}. ETA: {eta}. Track at voijeans.com/track. -Voi Logistics", "recipients": "Store Managers", "trigger": "Shipment status change"},
            {"name": "Production Delay Alert", "template": "URGENT: Production delay detected in {production_line} for style {style_number}. Current efficiency: {efficiency}%. -Voi Production", "recipients": "Production Managers", "trigger": "Efficiency below 80%"},
            {"name": "Quality Issue Alert", "template": "QC ALERT: High defect rate ({defect_rate}%) detected for {style_number}. Please investigate immediately. -Voi QC Team", "recipients": "Quality Team", "trigger": "Defect rate above 5%"}
        ]
        
        # Display SMS templates
        for i, template in enumerate(sms_templates):
            with st.expander(f"{template['name']} - {template['trigger']}"):
                st.markdown(f"**Template:** {template['template']}")
                st.markdown(f"**Recipients:** {template['recipients']}")
                
                # Add test button
                if st.button(f"Test SMS", key=f"test_sms_{i}"):
                    st.success("Test SMS would be sent in production environment")
                    st.info("SMS notifications require Twilio integration")
    
    with notification_tabs[1]:
        st.subheader("Email Alert System")
        
        # Sample email notifications
        email_notifications = [
            {"subject": "Weekly Inventory Report", "frequency": "Weekly (Monday)", "recipients": "All Department Heads", "attachment": "Yes"},
            {"subject": "Critical Material Shortage Alert", "frequency": "Real-time", "recipients": "Procurement Team", "attachment": "No"},
            {"subject": "Production Efficiency Report", "frequency": "Daily", "recipients": "Production Managers", "attachment": "Yes"},
            {"subject": "Shipping Status Update", "frequency": "Real-time", "recipients": "Logistics Team, Store Managers", "attachment": "No"},
            {"subject": "Quality Control Report", "frequency": "Daily", "recipients": "Quality Team, Production Team", "attachment": "Yes"}
        ]
        
        # Convert to DataFrame
        email_df = pd.DataFrame(email_notifications)
        
        # Display as table
        st.dataframe(email_df)
        
        # Email configuration
        st.subheader("Email Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("SMTP Server", value="smtp.voijeans.com", disabled=True)
            st.text_input("SMTP Port", value="587", disabled=True)
            
        with col2:
            st.text_input("Sender Email", value="scm-alerts@voijeans.com", disabled=True)
            st.text_input("Reply-to Email", value="supply-chain@voijeans.com", disabled=True)
        
        if st.button("Test Email Configuration"):
            st.success("Email configuration test successful!")
    
    with notification_tabs[2]:
        st.subheader("Dashboard Alerts")
        
        # Sample dashboard alerts
        dashboard_alerts = [
            {"type": "Critical", "message": "Raw denim inventory below threshold (3 days supply remaining)", "timestamp": "2025-03-29 08:32:15", "status": "Unresolved"},
            {"type": "Warning", "message": "Shipment SHP-2025-001 may be delayed due to weather conditions", "timestamp": "2025-03-29 10:15:22", "status": "Unresolved"},
            {"type": "Info", "message": "Production efficiency above target for Scotts Line 2", "timestamp": "2025-03-29 09:45:01", "status": "Acknowledged"},
            {"type": "Critical", "message": "Quality issues detected in latest batch of zippers from Vendor A", "timestamp": "2025-03-28 15:10:33", "status": "Resolved"},
            {"type": "Warning", "message": "Seasonal demand forecast updated - SS25 projections increased by 12%", "timestamp": "2025-03-28 11:20:18", "status": "Acknowledged"}
        ]
        
        # Convert to DataFrame
        alerts_df = pd.DataFrame(dashboard_alerts)
        
        # Format the timestamps
        alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"])
        alerts_df["timestamp"] = alerts_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        
        # Apply styling
        def color_alert_type(val):
            color_map = {
                "Critical": "background-color: red; color: white",
                "Warning": "background-color: yellow",
                "Info": "background-color: lightblue"
            }
            return color_map.get(val, "")
        
        def color_status(val):
            color_map = {
                "Unresolved": "background-color: red; color: white",
                "Acknowledged": "background-color: yellow",
                "Resolved": "background-color: lightgreen"
            }
            return color_map.get(val, "")
        
        st.dataframe(alerts_df.style.applymap(color_alert_type, subset=["type"]).applymap(color_status, subset=["status"]))
        
        # Alert statistics
        st.subheader("Alert Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Alerts Today", "14")
        
        with col2:
            st.metric("Critical Alerts", "3", delta="2")
        
        with col3:
            st.metric("Avg Resolution Time", "3.2 hours", delta="-0.5 hours")
    
    with notification_tabs[3]:
        st.subheader("Notification Configuration")
        
        # Configure notification thresholds
        st.markdown("### Alert Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.slider("Inventory Alert Threshold (%)", 10, 50, 20)
            st.slider("Quality Defect Rate Threshold (%)", 1, 10, 5)
            st.slider("Production Efficiency Alert Threshold (%)", 60, 90, 75)
        
        with col2:
            st.slider("Delivery Delay Threshold (days)", 1, 7, 3)
            st.slider("Cost Variance Threshold (%)", 5, 25, 10)
            st.slider("Lead Time Variance Threshold (%)", 5, 30, 15)
        
        # Configure notification recipients
        st.markdown("### Recipient Configuration")
        
        recipient_groups = [
            {"name": "Procurement Team", "members": "Anjali Patel, Vikram Mehta, Rohan Sharma"},
            {"name": "Production Managers", "members": "Rajesh Kumar, Priya Singh, Amit Verma"},
            {"name": "Quality Control Team", "members": "Neha Gupta, Alok Tiwari, Sanjay Mishra"},
            {"name": "Logistics Team", "members": "Deepak Kumar, Shreya Reddy, Anand Joshi"},
            {"name": "Store Managers", "members": "Rahul Khanna, Pooja Patel, Vivek Singhania, + 15 more"}
        ]
        
        # Convert to DataFrame
        recipient_df = pd.DataFrame(recipient_groups)
        
        # Display as table
        st.dataframe(recipient_df)
        
        # Save configuration button
        if st.button("Save Configuration"):
            st.success("Notification configuration saved successfully!")

def show_process_automation():
    """Show process automation capabilities"""
    st.header("Process Automation")
    
    st.markdown("""
    ### Automated Process Management
    
    Our system can automate several key processes in the supply chain to improve efficiency, reduce errors, and provide real-time visibility.
    """)
    
    # Display automation capabilities
    automation_options = [
        {
            "name": "Inventory Management Automation",
            "description": "Automatically reorder materials when inventory falls below threshold. Generate purchase requisitions and send to approved vendors.",
            "status": "Active",
            "trigger": "Inventory level below threshold",
            "action": "Generate purchase requisition"
        },
        {
            "name": "Production Scheduling Automation",
            "description": "Automatically generate optimal production schedules based on orders, capacity, and delivery dates. Adjust schedules when disruptions occur.",
            "status": "Active",
            "trigger": "New order confirmation or production disruption",
            "action": "Update production schedule"
        },
        {
            "name": "Quality Control Automation",
            "description": "Automatically flag quality issues, generate reports, and create action items for resolution. Track quality metrics over time.",
            "status": "Active",
            "trigger": "Quality check results outside parameters",
            "action": "Generate QC alert and action items"
        },
        {
            "name": "Logistics Optimization",
            "description": "Automatically optimize transportation routes and consolidate shipments to minimize costs. Generate shipping documents and track deliveries.",
            "status": "Active",
            "trigger": "Shipment ready for dispatch",
            "action": "Generate optimal route and shipping documents"
        },
        {
            "name": "Demand Forecasting",
            "description": "Automatically generate demand forecasts based on historical data, seasonal trends, and market signals. Update inventory and production plans.",
            "status": "Configuration Required",
            "trigger": "Monthly",
            "action": "Update demand forecast and inventory plan"
        }
    ]
    
    # Display automation options
    for i, option in enumerate(automation_options):
        with st.expander(f"{option['name']} - {option['status']}"):
            st.markdown(f"**Description:** {option['description']}")
            st.markdown(f"**Trigger:** {option['trigger']}")
            st.markdown(f"**Action:** {option['action']}")
            
            # Add configuration or test button
            if option['status'] == "Active":
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(f"Test", key=f"test_automation_{i}"):
                        st.success(f"Test successful! Automation would trigger: {option['action']}")
                with col2:
                    if st.button(f"Configure", key=f"config_automation_{i}"):
                        st.info(f"Configuration panel for {option['name']} would open here")
            else:
                if st.button(f"Configure and Activate", key=f"activate_automation_{i}"):
                    st.info(f"Configuration wizard for {option['name']} would start here")
    
    # Automation performance metrics
    st.subheader("Automation Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Processes Automated", "14/20", help="Number of processes that are fully automated")
    
    with col2:
        st.metric("Time Saved (hrs/week)", "42", delta="8%", help="Hours saved per week through automation")
    
    with col3:
        st.metric("Error Reduction", "73%", delta="12%", help="Reduction in process errors since automation")
    
    # Automation ROI chart
    st.subheader("Automation ROI")
    
    # Create automation ROI data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    investment = [250000, 50000, 50000, 50000, 50000, 50000]
    cumulative_investment = [sum(investment[:i+1]) for i in range(len(investment))]
    savings = [30000, 80000, 120000, 150000, 180000, 210000]
    cumulative_savings = [sum(savings[:i+1]) for i in range(len(savings))]
    
    # Calculate ROI
    roi = [(cumulative_savings[i] - cumulative_investment[i]) / cumulative_investment[i] * 100 for i in range(len(months))]
    
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Bar(
        x=months,
        y=savings,
        name='Monthly Savings',
        marker_color='green'
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_savings,
        mode='lines+markers',
        name='Cumulative Savings',
        line=dict(color='darkgreen', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_investment,
        mode='lines+markers',
        name='Cumulative Investment',
        line=dict(color='red', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=roi,
        mode='lines+markers',
        name='ROI (%)',
        line=dict(color='blue', width=3),
        yaxis='y2'
    ))
    
    # Create a secondary Y-axis
    fig.update_layout(
        title='Automation ROI (2025)',
        yaxis=dict(
            title='Amount (₹)',
            side='left'
        ),
        yaxis2=dict(
            title='ROI (%)',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        height=500,
        legend=dict(
            x=0.01,
            y=0.99
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Automation roadmap
    st.subheader("Automation Roadmap")
    
    roadmap_items = [
        {"phase": "Phase 1 (Complete)", "projects": ["Inventory Management Automation", "Production Scheduling", "Basic Quality Control Alerts"]},
        {"phase": "Phase 2 (Current)", "projects": ["Logistics Optimization", "Advanced QC Integration", "Supplier Portal Integration"]},
        {"phase": "Phase 3 (Q3 2025)", "projects": ["AI-based Demand Forecasting", "Predictive Maintenance", "Digital Twin Integration"]},
        {"phase": "Phase 4 (Q1 2026)", "projects": ["Supply Chain Control Tower", "Blockchain for Traceability", "Autonomous Supplier Selection"]}
    ]
    
    for item in roadmap_items:
        with st.expander(item["phase"]):
            for project in item["projects"]:
                st.markdown(f"- {project}")