import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def show_emperor_timeline():
    """
    Display the Emperor's Timeline for governance decisions and license management.
    This is a crucial governance tool in the ECG layer for tracking and managing licenses.
    """
    
    # Emperor's header with special styling for the timeline view
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, rgba(75,0,130,1) 0%, rgba(128,0,128,1) 100%); 
        padding: 30px; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
            <h1 style='color: gold; margin: 0; font-size: 2.8rem;'>👑 Emperor's Timeline</h1>
            <p style='color: white; margin: 10px 0 0 0; font-size: 1.5rem;'>ECG Governance & License Management</p>
            <p style='color: rgba(255,255,255,0.7); margin: 5px 0 0 0;'>Historical Decisions & Future Planning</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Timeline tabs for different timeline views
    tabs = st.tabs([
        "📜 Governance Timeline", 
        "⚖️ License Activities", 
        "🔄 Decision Workflows",
        "📊 Impact Analysis"
    ])
    
    # Generate timeline data
    timeline_data = generate_timeline_data()
    license_data = generate_license_data()
    
    # Tab 1: Governance Timeline
    with tabs[0]:
        st.header("Imperial Governance Timeline")
        st.write("Historical record of all governance decisions and their impacts across the Empire.")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.multiselect(
                "Filter by Category", 
                options=["Policy", "License", "Financial", "Technology", "Partnership"],
                default=["Policy", "License", "Financial", "Technology", "Partnership"]
            )
        with col2:
            impact_filter = st.multiselect(
                "Filter by Impact Level",
                options=["High", "Medium", "Low"],
                default=["High", "Medium", "Low"]
            )
        with col3:
            date_range = st.date_input(
                "Date Range",
                value=(
                    datetime.now() - timedelta(days=90),
                    datetime.now() + timedelta(days=30)
                ),
                max_value=datetime.now() + timedelta(days=365)
            )
        
        # Filter the timeline data
        filtered_data = timeline_data[
            (timeline_data['category'].isin(category_filter)) &
            (timeline_data['impact'].isin(impact_filter)) &
            (timeline_data['date'] >= pd.Timestamp(date_range[0])) &
            (timeline_data['date'] <= pd.Timestamp(date_range[1]))
        ]
        
        # Create the timeline visualization
        if len(filtered_data) > 0:
            fig = create_timeline_visualization(filtered_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Timeline details table
            st.subheader("Timeline Event Details")
            st.dataframe(
                filtered_data[['date', 'title', 'category', 'impact', 'description']],
                use_container_width=True,
                column_config={
                    "date": st.column_config.DateColumn("Date"),
                    "title": st.column_config.TextColumn("Event"),
                    "category": st.column_config.TextColumn("Category"),
                    "impact": st.column_config.TextColumn("Impact"),
                    "description": st.column_config.TextColumn("Description"),
                }
            )
        else:
            st.warning("No timeline events match your filter criteria.")
    
    # Tab 2: License Activities
    with tabs[1]:
        st.header("License Activity Monitor")
        st.write("Track all license-related activities across the Empire.")
        
        # License activity metrics
        license_metrics = st.columns(4)
        with license_metrics[0]:
            st.metric("Active Licenses", "243", "+12")
        with license_metrics[1]:
            st.metric("Pending Approval", "18", "-5")
        with license_metrics[2]:
            st.metric("Recently Issued", "28", "+4")
        with license_metrics[3]:
            st.metric("Compliance Score", "92%", "+3%")
        
        # License type distribution
        st.subheader("License Distribution by Type")
        license_type_fig = px.pie(
            license_data, 
            values='count', 
            names='license_type', 
            color='license_type',
            color_discrete_map={
                'Manufacturer': '#4B0082',
                'Retailer': '#9370DB',
                'Brand': '#800080',
                'Distributor': '#BA55D3',
                'Financial': '#8A2BE2'
            },
            hole=0.4
        )
        license_type_fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(license_type_fig, use_container_width=True)
        
        # License activity stream
        st.subheader("Recent License Activity Stream")
        license_activity = generate_license_activity()
        
        for activity in license_activity:
            activity_color = "green" if activity["activity_type"] == "Issued" else "blue" if activity["activity_type"] == "Renewed" else "orange" if activity["activity_type"] == "Updated" else "red"
            
            st.markdown(
                f"""
                <div style="border-left: 4px solid {activity_color}; padding-left: 15px; margin-bottom: 15px;">
                    <p style="margin: 0; font-weight: bold;">{activity["company"]} • {activity["license_type"]} License</p>
                    <p style="margin: 0; color: {activity_color};">{activity["activity_type"]} on {activity["date"]}</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em;">{activity["description"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Tab 3: Decision Workflows
    with tabs[2]:
        st.header("Governance Decision Workflows")
        st.write("Track active governance procedures and decision-making processes.")
        
        # Create workflow funnel
        workflow_stages = {
            "Proposal Submitted": 42,
            "Under ECG Review": 28,
            "Financial Analysis": 21,
            "Technical Validation": 16,
            "Emperor Approval": 8,
            "Implementation": 5
        }
        
        # Create funnel chart
        workflow_fig = go.Figure(go.Funnel(
            y=list(workflow_stages.keys()),
            x=list(workflow_stages.values()),
            textinfo="value+percent initial",
            marker={
                "color": [
                    "#4B0082", "#600080", "#800080", 
                    "#9A0080", "#B40080", "#CE0080"
                ]
            }
        ))
        
        workflow_fig.update_layout(
            title="Decision Workflow Funnel",
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        st.plotly_chart(workflow_fig, use_container_width=True)
        
        # Active workflows table
        st.subheader("Active Governance Workflows")
        
        active_workflows = [
            {"id": "GW-2025-042", "title": "CMP License Framework Update", "stage": "Financial Analysis", "owner": "CFO Office", "priority": "High", "due_date": "2025-04-15"},
            {"id": "GW-2025-039", "title": "New Marketplace Integration Policy", "stage": "Technical Validation", "owner": "CIO Office", "priority": "Medium", "due_date": "2025-04-18"},
            {"id": "GW-2025-035", "title": "Cross-Border Trade Policy", "stage": "Emperor Approval", "owner": "ECG Council", "priority": "High", "due_date": "2025-04-10"},
            {"id": "GW-2025-031", "title": "Synergyze API Security Framework", "stage": "Implementation", "owner": "CIO Office", "priority": "Critical", "due_date": "2025-04-08"},
            {"id": "GW-2025-028", "title": "Escrow Fund Management Update", "stage": "Under ECG Review", "owner": "CFO Office", "priority": "Medium", "due_date": "2025-04-22"},
        ]
        
        # Convert to DataFrame for display
        active_df = pd.DataFrame(active_workflows)
        
        # Add color highlighting based on priority
        def highlight_priority(val):
            if val == 'Critical':
                return 'background-color: #FF000050'
            elif val == 'High':
                return 'background-color: #FFA50050'
            elif val == 'Medium':
                return 'background-color: #FFFF0050'
            else:
                return 'background-color: #00FF0050'
        
        # Display with styling
        st.dataframe(
            active_df.style.applymap(highlight_priority, subset=['priority']),
            use_container_width=True
        )
        
    # Tab 4: Impact Analysis
    with tabs[3]:
        st.header("Governance Impact Analysis")
        st.write("Analyze the effects of governance decisions across the Empire.")
        
        # Create a network graph of impact relationships
        st.subheader("Decision Impact Network")
        
        # Sample impact metrics over time
        periods = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Q2 2025"]
        
        impact_metrics = {
            "Licensee Satisfaction": [72, 75, 79, 83, 88, 92],
            "Ecosystem Growth": [25, 32, 45, 58, 67, 76],
            "Financial Stability": [68, 70, 75, 82, 87, 90],
            "Technical Reliability": [85, 86, 88, 90, 92, 95],
            "Compliance Score": [78, 82, 85, 88, 90, 92]
        }
        
        # Create the impact radar chart
        categories = list(impact_metrics.keys())
        
        fig = go.Figure()
        
        for i, period in enumerate(periods):
            values = [impact_metrics[category][i] for category in categories]
            # Add the first value again to close the loop
            values.append(values[0])
            categories_closed = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_closed,
                name=period,
                fill='toself',
                opacity=0.4 + (i * 0.1),  # Increasing opacity for newer periods
                line=dict(width=2)
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Decision impact heatmap
        st.subheader("Decision Category Impact Heatmap")
        
        impact_areas = ["Financial Health", "Licensee Growth", "Market Reach", "System Stability", "Compliance"]
        decision_categories = ["Policy Changes", "License Updates", "Fee Structure", "Technology Upgrades", "Compliance Rules"]
        
        # Generate impact scores (0-10)
        impact_scores = np.random.randint(4, 10, size=(len(impact_areas), len(decision_categories)))
        
        # Create heatmap
        heatmap_fig = px.imshow(
            impact_scores,
            labels=dict(x="Decision Category", y="Impact Area", color="Impact Score"),
            x=decision_categories,
            y=impact_areas,
            color_continuous_scale="Viridis",
            zmin=0, zmax=10
        )
        
        heatmap_fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
    # Emperor's action section at the bottom
    st.markdown("---")
    
    st.markdown(
        """
        <div style='background: rgba(75,0,130,0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #4B0082;'>
            <h3 style='margin-top: 0; color: #4B0082;'>Emperor's Actions</h3>
            <p>Take direct actions to influence governance and license management across the Empire.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("📝 New Governance Directive", use_container_width=True)
        st.button("🔍 Audit License Activities", use_container_width=True)
    
    with col2:
        st.button("✅ Approve Pending Licenses", use_container_width=True)
        st.button("📊 Generate Impact Report", use_container_width=True)
    
    with col3:
        st.button("📣 Issue ECG Council Notice", use_container_width=True)
        st.button("🔒 Update Security Protocols", use_container_width=True)

def generate_timeline_data():
    """Generate sample timeline data for demonstration"""
    # Create date range from 3 months ago to 1 month in future
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now() + timedelta(days=30)
    
    # Categories and impacts
    categories = ["Policy", "License", "Financial", "Technology", "Partnership"]
    impacts = ["High", "Medium", "Low"]
    
    # Sample events
    events = [
        {"title": "Empire OS Constitution Update", "category": "Policy", "impact": "High", 
         "description": "Major revision to the core governance principles that guide the entire ecosystem."},
        {"title": "Synergyze License Fee Structure Revision", "category": "License", "impact": "High", 
         "description": "Updated pricing model for all license types to better align with market value."},
        {"title": "Virtual Silk Road Map Expansion", "category": "Technology", "impact": "Medium", 
         "description": "Added new regions and economic zones to the Virtual Silk Road visualization."},
        {"title": "ECG Council Quarterly Review", "category": "Policy", "impact": "Medium", 
         "description": "Regular governance review of all ecosystem performance metrics."},
        {"title": "Escrow Fund Management Protocol Update", "category": "Financial", "impact": "High", 
         "description": "Enhanced security and transparency measures for all escrow transactions."},
        {"title": "CIO Security Framework Implementation", "category": "Technology", "impact": "High", 
         "description": "Deployment of advanced security protocols across all Empire OS interfaces."},
        {"title": "Manufacturer License Template v2.0 Release", "category": "License", "impact": "Medium", 
         "description": "Updated license template for manufacturers with additional compliance requirements."},
        {"title": "Cross-Border Trade Agreement", "category": "Partnership", "impact": "High", 
         "description": "New agreement facilitating seamless trade between multiple license jurisdictions."},
        {"title": "CFO Financial Visibility Enhancement", "category": "Financial", "impact": "Medium", 
         "description": "Improved financial tracking and reporting tools for license-based revenue."},
        {"title": "API Security Penetration Testing", "category": "Technology", "impact": "Low", 
         "description": "Routine security assessment of all API endpoints and data exchange protocols."},
        {"title": "ECG Partner Onboarding Optimization", "category": "Partnership", "impact": "Medium", 
         "description": "Streamlined process for bringing new partners into the ecosystem."},
        {"title": "License Compliance Audit", "category": "License", "impact": "High", 
         "description": "Comprehensive audit of all active licenses for compliance with latest standards."},
        {"title": "Emperor's Annual Address", "category": "Policy", "impact": "High", 
         "description": "Strategic direction and vision for the ecosystem's next growth phase."},
        {"title": "Smart Contract Implementation for Escrow", "category": "Technology", "impact": "High", 
         "description": "Automated contract execution for financial transactions across the system."},
        {"title": "Retail License Fee Adjustment", "category": "License", "impact": "Medium", 
         "description": "Adjustment to retail license fees based on market performance data."},
    ]
    
    # Generate dates between start and end date
    range_days = (end_date - start_date).days
    dates = [start_date + timedelta(days=random.randint(0, range_days)) for _ in range(len(events))]
    dates.sort()  # Sort dates chronologically
    
    # Create list of dictionaries with event data
    timeline_data = []
    for i, event in enumerate(events):
        timeline_data.append({
            "date": dates[i],
            "title": event["title"],
            "category": event["category"],
            "impact": event["impact"],
            "description": event["description"]
        })
    
    # Convert to DataFrame
    return pd.DataFrame(timeline_data)

def generate_license_data():
    """Generate sample license data for visualization"""
    license_types = ["Manufacturer", "Retailer", "Brand", "Distributor", "Financial"]
    counts = [78, 92, 45, 18, 10]
    
    return pd.DataFrame({
        "license_type": license_types,
        "count": counts
    })

def generate_license_activity():
    """Generate sample license activity stream"""
    activities = [
        {
            "company": "VoiJeans Retail India Pvt Ltd",
            "license_type": "Retailer",
            "activity_type": "Renewed",
            "date": "April 02, 2025",
            "description": "Annual license renewal with upgraded tier access to advanced retail analytics."
        },
        {
            "company": "Fashionista Brands LLC",
            "license_type": "Brand",
            "activity_type": "Issued",
            "date": "April 01, 2025",
            "description": "New brand license issued with private label and house brand capabilities."
        },
        {
            "company": "TextilePro Manufacturing",
            "license_type": "Manufacturer",
            "activity_type": "Updated",
            "date": "March 29, 2025",
            "description": "License updated to include FOB export compliance modules."
        },
        {
            "company": "Global Fashion Logistics",
            "license_type": "Distributor",
            "activity_type": "Compliance Alert",
            "date": "March 28, 2025",
            "description": "Warning issued for delayed inventory reporting. Requires attention."
        },
        {
            "company": "FashionBank Financial Services",
            "license_type": "Financial",
            "activity_type": "Renewed",
            "date": "March 25, 2025",
            "description": "License renewed with supply chain financing capabilities added."
        }
    ]
    
    return activities

def create_timeline_visualization(data):
    """Create a visual timeline chart from the provided data"""
    # Create a custom timeline visualization
    fig = go.Figure()
    
    # Color mapping for categories
    color_map = {
        "Policy": "#4B0082",     # Indigo
        "License": "#9370DB",    # Medium Purple
        "Financial": "#800080",  # Purple
        "Technology": "#8A2BE2", # Blue Violet
        "Partnership": "#BA55D3" # Medium Orchid
    }
    
    # Size mapping for impact
    size_map = {
        "High": 20,
        "Medium": 15,
        "Low": 10
    }
    
    # Create scatter plot for timeline events
    for category in data['category'].unique():
        category_data = data[data['category'] == category]
        
        fig.add_trace(go.Scatter(
            x=category_data['date'],
            y=[category] * len(category_data),
            mode='markers+text',
            marker=dict(
                color=color_map[category],
                size=[size_map[impact] for impact in category_data['impact']],
                line=dict(width=2, color='white')
            ),
            text=category_data['title'],
            textposition="top center",
            name=category,
            hovertemplate=
            "<b>%{text}</b><br>" +
            "Date: %{x|%b %d, %Y}<br>" +
            "Category: " + category + "<br>" +
            "Impact: %{customdata}<br>" +
            "Description: %{meta}<br>" +
            "<extra></extra>",
            customdata=category_data['impact'],
            meta=category_data['description']
        ))
    
    # Add horizontal lines for each category
    for i, category in enumerate(data['category'].unique()):
        fig.add_shape(
            type="line",
            x0=data['date'].min() - timedelta(days=5),
            y0=category,
            x1=data['date'].max() + timedelta(days=5),
            y1=category,
            line=dict(color="rgba(120, 120, 120, 0.3)", width=1, dash="dot")
        )
    
    # Add today's date vertical line
    today = datetime.now()
    fig.add_shape(
        type="line",
        x0=today,
        y0=-1,
        x1=today,
        y1=len(data['category'].unique()),
        line=dict(color="rgba(255, 0, 0, 0.5)", width=2, dash="dash")
    )
    
    # Add "Today" annotation
    fig.add_annotation(
        x=today,
        y=-0.5,
        text="Today",
        showarrow=False,
        font=dict(color="red")
    )
    
    # Configure layout
    fig.update_layout(
        title="Empire Governance Timeline",
        title_font=dict(size=20, color="#4B0082"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=50, r=20, t=50, b=20),
        xaxis=dict(
            title="Timeline",
            gridcolor="rgba(120, 120, 120, 0.2)",
            type="date"
        ),
        yaxis=dict(
            title="Category",
            gridcolor="rgba(120, 120, 120, 0)",
        ),
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig