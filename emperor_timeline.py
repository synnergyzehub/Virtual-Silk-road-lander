import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show_emperor_timeline():
    """
    Display the Emperor Timeline component - part of the ECG governance layer
    where licenses are issued and enterprise governance is tracked.
    """
    st.title("Emperor Timeline")
    
    # Styled subtitle
    st.markdown("""
    <div style='background: linear-gradient(90deg, rgba(75,0,130,0.2) 0%, rgba(123,104,238,0.2) 100%); 
    padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
        <h3 style='margin: 0; color: #4B0082;'>The Enterprise Command & Governance Timeline</h3>
        <p style='margin: 5px 0 0 0;'>Track the evolution of your enterprise ecosystem in real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different timeline views
    timeline_tabs = st.tabs(["Enterprise Licenses", "Governance Events", "Compliance", "Integration Timeline"])
    
    # Tab 1: Enterprise Licenses Timeline
    with timeline_tabs[0]:
        st.subheader("Enterprise License Issuance & Renewal Timeline")
        
        # Time range selector
        col1, col2 = st.columns([3, 1])
        with col1:
            time_range = st.select_slider(
                "Timeline Range",
                options=["Last 30 Days", "Last Quarter", "Last Year", "All Time"],
                value="Last Quarter"
            )
        
        with col2:
            view_mode = st.radio("View Mode", ["Timeline", "Calendar"], horizontal=True)
        
        # Generate sample license data
        licenses_data = generate_license_data(time_range)
        
        # Display the licenses in selected view mode
        if view_mode == "Timeline":
            show_license_timeline(licenses_data)
        else:
            show_license_calendar(licenses_data)
        
        # License statistics
        st.subheader("License Statistics")
        stats_cols = st.columns(4)
        
        with stats_cols[0]:
            active_count = len(licenses_data[licenses_data['Status'] == 'Active'])
            st.metric("Active Licenses", active_count, f"+{random.randint(1, 5)} from last period")
            
        with stats_cols[1]:
            pending_count = len(licenses_data[licenses_data['Status'] == 'Pending Renewal'])
            st.metric("Pending Renewal", pending_count, f"-{random.randint(1, 3)} from last period")
            
        with stats_cols[2]:
            revenue = sum(licenses_data['Value'])
            st.metric("License Revenue", f"${revenue:,}", f"+{random.randint(5, 15)}%")
            
        with stats_cols[3]:
            compliance = random.uniform(0.92, 0.99)
            st.metric("Compliance Rate", f"{compliance:.2%}", f"+{random.uniform(0.01, 0.05):.2%}")
    
    # Tab 2: Governance Events
    with timeline_tabs[1]:
        st.subheader("Enterprise Governance Events")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            event_types = st.multiselect(
                "Event Types",
                ["Policy Change", "Audit", "Inspection", "Compliance Review", "Milestone", "Risk Event"],
                default=["Policy Change", "Audit", "Milestone"]
            )
            
        with col2:
            priority_filter = st.multiselect(
                "Priority Level",
                ["Critical", "High", "Medium", "Low"],
                default=["Critical", "High"]
            )
            
        with col3:
            date_range = st.date_input(
                "Date Range",
                [datetime.now() - timedelta(days=90), datetime.now()],
                key="gov_date_range"
            )
        
        # Generate governance events data
        gov_events = generate_governance_events(event_types, priority_filter)
        
        # Display events in a timeline
        show_governance_timeline(gov_events)
        
        # Key governance metrics
        st.subheader("Governance Metrics")
        
        metrics_cols = st.columns(2)
        
        with metrics_cols[0]:
            # Governance health score
            gov_score = random.uniform(85, 98)
            st.markdown(f"""
            <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px;'>
                <h4 style='margin: 0 0 10px 0;'>Governance Health Score</h4>
                <div style='display: flex; align-items: center;'>
                    <div style='font-size: 2.5em; font-weight: bold; margin-right: 15px; color: {"green" if gov_score > 90 else "orange"};'>
                        {gov_score:.1f}
                    </div>
                    <div>
                        <div style='height: 8px; width: 200px; background-color: #ddd; border-radius: 4px;'>
                            <div style='height: 100%; width: {gov_score}%; background-color: {"green" if gov_score > 90 else "orange"}; border-radius: 4px;'></div>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8em;'>
                            <span>0</span>
                            <span>50</span>
                            <span>100</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with metrics_cols[1]:
            # Risk assessment
            risk_level = random.choice(["Low", "Moderate", "Elevated", "High"])
            risk_color = {
                "Low": "green",
                "Moderate": "#FFC107",
                "Elevated": "orange",
                "High": "red"
            }[risk_level]
            
            st.markdown(f"""
            <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px;'>
                <h4 style='margin: 0 0 10px 0;'>Current Risk Assessment</h4>
                <div style='display: flex; align-items: center;'>
                    <div style='font-size: 1.5em; font-weight: bold; margin-right: 15px; color: {risk_color};'>
                        {risk_level}
                    </div>
                    <div style='flex-grow: 1;'>
                        <p style='margin: 0; font-size: 0.9em;'>Based on {len(gov_events)} governance events</p>
                        <p style='margin: 5px 0 0 0; font-size: 0.8em;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent policy changes
        st.subheader("Recent Policy Changes")
        
        policy_changes = [event for event in gov_events if event['Type'] == 'Policy Change'][:3]
        
        for policy in policy_changes:
            st.markdown(f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <span style='font-weight: bold;'>{policy['Title']}</span>
                    <span style='color: #666; font-size: 0.9em;'>{policy['Date'].strftime('%Y-%m-%d')}</span>
                </div>
                <p style='margin: 0 0 10px 0;'>{policy['Description']}</p>
                <div>
                    <span style='background-color: {"#F44336" if policy["Priority"] == "Critical" else "#FF9800" if policy["Priority"] == "High" else "#4CAF50"}; 
                          color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;'>
                        {policy['Priority']}
                    </span>
                    <span style='margin-left: 10px; font-size: 0.9em;'>Affected Licenses: {policy['Affected']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 3: Compliance Timeline
    with timeline_tabs[2]:
        st.subheader("License Compliance Timeline")
        
        # Compliance filter
        col1, col2 = st.columns(2)
        
        with col1:
            compliance_metric = st.selectbox(
                "Compliance Metric",
                ["Overall Compliance", "Financial Compliance", "Operational Compliance", "Security Compliance", "Legal Compliance"]
            )
            
        with col2:
            compliance_period = st.select_slider(
                "Time Period",
                options=["Last 30 Days", "Last Quarter", "Last Year"],
                value="Last Quarter"
            )
        
        # Generate compliance data
        compliance_data = generate_compliance_data(compliance_metric, compliance_period)
        
        # Create compliance trend chart
        fig = px.line(
            compliance_data,
            x='Date',
            y='Compliance',
            color='Category',
            line_shape='spline',
            markers=True,
            title=f"{compliance_metric} Trend Over Time"
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Compliance Score (%)',
            yaxis=dict(range=[75, 100]),
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Compliance events
        st.subheader("Compliance Events")
        
        events_cols = st.columns(3)
        
        for i, category in enumerate(['Audits', 'Reviews', 'Violations']):
            with events_cols[i]:
                event_count = random.randint(3, 12) if category == 'Violations' else random.randint(8, 25)
                last_event = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
                status_color = "red" if category == 'Violations' else "green"
                
                st.markdown(f"""
                <div style='border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;'>
                    <h3 style='margin: 0 0 10px 0;'>{event_count}</h3>
                    <p style='margin: 0 0 5px 0; font-weight: bold;'>{category}</p>
                    <p style='margin: 0; font-size: 0.8em; color: #666;'>Last event: {last_event}</p>
                    <p style='margin: 5px 0 0 0; font-size: 0.9em; color: {status_color};'>
                        {"⚠️ Attention needed" if category == 'Violations' else "✅ All compliant"}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Compliance action items
        st.subheader("Compliance Action Items")
        
        action_items = [
            {
                "title": "Quarterly Compliance Report Submission",
                "deadline": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                "status": "In Progress",
                "priority": "High",
                "assigned_to": "Governance Team"
            },
            {
                "title": "License Renewal Documentation Review",
                "deadline": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                "status": "Not Started",
                "priority": "Medium",
                "assigned_to": "Legal Department"
            },
            {
                "title": "Address Security Compliance Violations",
                "deadline": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                "status": "Overdue",
                "priority": "Critical",
                "assigned_to": "Security Officer"
            }
        ]
        
        for item in action_items:
            status_color = {"In Progress": "#FFC107", "Not Started": "#9E9E9E", "Overdue": "#F44336", "Completed": "#4CAF50"}
            priority_color = {"Critical": "#F44336", "High": "#FF9800", "Medium": "#FFC107", "Low": "#4CAF50"}
            
            st.markdown(f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <span style='font-weight: bold;'>{item['title']}</span>
                    <span style='color: #666; font-size: 0.9em;'>Deadline: {item['deadline']}</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <div>
                        <span style='background-color: {status_color[item["status"]]}; 
                              color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;'>
                            {item['status']}
                        </span>
                        <span style='background-color: {priority_color[item["priority"]]}; 
                              color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em; margin-left: 5px;'>
                            {item['priority']}
                        </span>
                    </div>
                    <div>
                        <span style='font-size: 0.9em;'>Assigned to: {item['assigned_to']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 4: Integration Timeline
    with timeline_tabs[3]:
        st.subheader("Enterprise Integration Timeline")
        
        # Explain the integration timeline
        st.markdown("""
        The Integration Timeline shows how different components of your enterprise governance ecosystem
        connect and interact over time. This view helps visualize the relationships between:
        
        - **Empire OS**: The core operating system and governance layer
        - **Virtual Silk Road**: The network layer connecting all enterprise components
        - **Synergyze Licenses**: The permission and licensing layer
        - **Enterprise Applications**: Custom applications built on the ecosystem
        """)
        
        # Integration visualization
        st.subheader("Enterprise Integration Visualization")
        
        # Generate integration timeline data
        integration_data = generate_integration_data()
        
        # Create a timeline visualization of integrations
        fig = create_integration_timeline(integration_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Integration statistics
        stats_cols = st.columns(4)
        
        integration_stats = {
            "Total Integrations": random.randint(25, 40),
            "Active Connections": random.randint(18, 30),
            "Data Flow Rate": f"{random.randint(50, 200)} GB/day",
            "API Calls": f"{random.randint(5, 20)}M daily"
        }
        
        for i, (stat_name, stat_value) in enumerate(integration_stats.items()):
            with stats_cols[i]:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; border-radius: 5px;'>
                    <p style='margin: 0; font-size: 0.9em; color: #666;'>{stat_name}</p>
                    <p style='margin: 5px 0 0 0; font-size: 1.5em; font-weight: bold;'>{stat_value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent integration events
        st.subheader("Recent Integration Events")
        
        integration_events = [
            {
                "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                "event": "New API Gateway Deployed",
                "components": ["Empire OS", "Virtual Silk Road"],
                "impact": "Positive",
                "description": "Deployed a new API gateway to improve connection management between Empire OS and the Virtual Silk Road network."
            },
            {
                "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "event": "License Verification Service Upgraded",
                "components": ["Synergyze", "Enterprise Applications"],
                "impact": "Neutral",
                "description": "Updated the license verification service to accommodate new license types and improve verification speed."
            },
            {
                "date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
                "event": "Data Synchronization Issue",
                "components": ["Virtual Silk Road", "Synergyze"],
                "impact": "Negative",
                "description": "Experienced data synchronization issues between Virtual Silk Road and Synergyze license database, resulting in temporary verification delays."
            }
        ]
        
        for event in integration_events:
            impact_color = {"Positive": "green", "Neutral": "#FFC107", "Negative": "red"}[event["impact"]]
            
            st.markdown(f"""
            <div style='border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                    <span style='font-weight: bold;'>{event['event']}</span>
                    <span style='color: #666; font-size: 0.9em;'>{event['date']}</span>
                </div>
                <p style='margin: 0 0 10px 0;'>{event['description']}</p>
                <div style='display: flex; justify-content: space-between;'>
                    <div>
                        <span style='color: {impact_color}; font-weight: bold;'>
                            {event['impact']} Impact
                        </span>
                    </div>
                    <div>
                        <span style='font-size: 0.9em;'>Components: {', '.join(event['components'])}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_license_timeline(license_data):
    """Display license data in a timeline view"""
    # Create plotly figure for timeline
    fig = go.Figure()
    
    # Add events to timeline
    for status in ['Active', 'Pending Renewal', 'Expired', 'Revoked']:
        status_data = license_data[license_data['Status'] == status]
        
        if not status_data.empty:
            color_map = {
                'Active': 'green',
                'Pending Renewal': 'orange',
                'Expired': 'gray',
                'Revoked': 'red'
            }
            
            fig.add_trace(go.Scatter(
                x=status_data['Issued Date'],
                y=status_data['Licensee'],
                mode='markers',
                name=status,
                marker=dict(
                    symbol='circle',
                    size=12,
                    color=color_map[status],
                    line=dict(width=2, color='DarkSlateGrey')
                ),
                text=status_data.apply(
                    lambda row: f"License: {row['Type']}<br>" + 
                                f"Status: {row['Status']}<br>" + 
                                f"Value: ${row['Value']:,}<br>" +
                                f"Expires: {row['Expiry Date'].strftime('%Y-%m-%d')}", 
                    axis=1
                ),
                hoverinfo='text'
            ))
    
    # Add expiry date markers for active licenses
    active_data = license_data[license_data['Status'] == 'Active']
    if not active_data.empty:
        fig.add_trace(go.Scatter(
            x=active_data['Expiry Date'],
            y=active_data['Licensee'],
            mode='markers',
            name='Expiry Date',
            marker=dict(
                symbol='diamond',
                size=10,
                color='rgba(0, 0, 0, 0.5)',
                line=dict(width=1, color='DarkSlateGrey')
            ),
            text=active_data.apply(
                lambda row: f"License: {row['Type']}<br>" + 
                            f"Expires on: {row['Expiry Date'].strftime('%Y-%m-%d')}", 
                axis=1
            ),
            hoverinfo='text'
        ))
        
        # Add connecting lines between issuance and expiry
        for _, row in active_data.iterrows():
            fig.add_trace(go.Scatter(
                x=[row['Issued Date'], row['Expiry Date']],
                y=[row['Licensee'], row['Licensee']],
                mode='lines',
                line=dict(color='rgba(0, 128, 0, 0.3)', width=2, dash='dot'),
                showlegend=False,
                hoverinfo='none'
            ))
    
    # Configure layout
    fig.update_layout(
        title='License Timeline',
        xaxis_title='Date',
        yaxis_title='Licensee',
        height=500,
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True)

def show_license_calendar(license_data):
    """Display license data in a calendar view"""
    st.warning("Calendar view is under development. Displaying tabular view instead.")
    
    # Sort by issued date descending
    license_data_sorted = license_data.sort_values('Issued Date', ascending=False)
    
    # Create status indicator function
    def status_indicator(status):
        colors = {
            'Active': 'green',
            'Pending Renewal': 'orange',
            'Expired': 'gray',
            'Revoked': 'red'
        }
        return f'<span style="color: {colors[status]}; font-weight: bold;">●</span> {status}'
    
    # Add status indicator column
    license_data_display = license_data_sorted.copy()
    license_data_display['Status Display'] = license_data_display['Status'].apply(status_indicator)
    
    # Format dates for display
    license_data_display['Issued Date'] = license_data_display['Issued Date'].dt.strftime('%Y-%m-%d')
    license_data_display['Expiry Date'] = license_data_display['Expiry Date'].dt.strftime('%Y-%m-%d')
    
    # Format value as currency
    license_data_display['Value'] = license_data_display['Value'].apply(lambda x: f"${x:,}")
    
    # Select and reorder columns for display
    display_columns = ['Licensee', 'Type', 'Status Display', 'Issued Date', 'Expiry Date', 'Value']
    
    # Display the dataframe
    st.markdown(license_data_display[display_columns].to_html(
        escape=False, index=False), unsafe_allow_html=True)

def show_governance_timeline(governance_events):
    """Display governance events in a timeline visualization"""
    # Sort events by date
    sorted_events = sorted(governance_events, key=lambda x: x['Date'])
    
    # Create a figure for the timeline
    fig = go.Figure()
    
    # Add events to the timeline
    for event_type in set(event['Type'] for event in sorted_events):
        type_events = [event for event in sorted_events if event['Type'] == event_type]
        
        # Define marker colors based on priority
        colors = []
        for event in type_events:
            if event['Priority'] == 'Critical':
                colors.append('red')
            elif event['Priority'] == 'High':
                colors.append('orange')
            elif event['Priority'] == 'Medium':
                colors.append('#FFC107')
            else:  # Low
                colors.append('green')
        
        fig.add_trace(go.Scatter(
            x=[event['Date'] for event in type_events],
            y=[event_type] * len(type_events),
            mode='markers',
            name=event_type,
            marker=dict(
                symbol='circle',
                size=15,
                color=colors,
                line=dict(width=2, color='DarkSlateGrey')
            ),
            text=[
                f"Title: {event['Title']}<br>" +
                f"Date: {event['Date'].strftime('%Y-%m-%d')}<br>" +
                f"Priority: {event['Priority']}<br>" +
                f"Description: {event['Description']}"
                for event in type_events
            ],
            hoverinfo='text'
        ))
    
    # Configure layout
    fig.update_layout(
        title='Governance Events Timeline',
        xaxis_title='Date',
        yaxis=dict(
            title='Event Type',
            categoryorder='array',
            categoryarray=sorted(set(event['Type'] for event in sorted_events))
        ),
        height=400,
        hovermode='closest',
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add a vertical line for today
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="rgba(0, 0, 0, 0.5)",
        annotation_text="Today",
        annotation_position="top right"
    )
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True)

def create_integration_timeline(integration_data):
    """Create a timeline visualization of enterprise integrations"""
    # Create figure for the timeline
    fig = go.Figure()
    
    # Define component colors
    component_colors = {
        'Empire OS': '#4B0082',
        'Virtual Silk Road': '#8A2BE2',
        'Synergyze': '#9370DB',
        'Enterprise App': '#BA55D3'
    }
    
    # Add traces for each integration event
    for event in integration_data:
        # Determine color based on source component
        color = component_colors.get(event['source'], '#666666')
        
        fig.add_trace(go.Scatter(
            x=[event['date']],
            y=[0],  # All points at y=0
            mode='markers',
            marker=dict(
                symbol='circle',
                size=15,
                color=color,
                line=dict(width=2, color='white')
            ),
            text=f"{event['description']}<br>{event['source']} → {event['target']}",
            hoverinfo='text',
            name=event['event_type']
        ))
    
    # Configure layout
    fig.update_layout(
        title='Enterprise Integration Events',
        xaxis=dict(
            title='Date',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            zeroline=False,
            showgrid=False
        ),
        height=250,
        hovermode='closest',
        showlegend=False
    )
    
    # Add a vertical line for today
    fig.add_vline(
        x=datetime.now(),
        line_width=2,
        line_dash="dash",
        line_color="rgba(0, 0, 0, 0.5)"
    )
    
    # Add annotations for component types
    legend_x = datetime.now() - timedelta(days=100)  # Position left of today
    for i, (component, color) in enumerate(component_colors.items()):
        fig.add_annotation(
            x=legend_x,
            y=0.1 + (i * 0.2),
            text=component,
            showarrow=False,
            bgcolor=color,
            bordercolor='white',
            borderwidth=1,
            borderpad=4,
            font=dict(color='white', size=10),
            opacity=0.8
        )
    
    return fig

def generate_license_data(time_range):
    """Generate sample license data based on the selected time range"""
    # Determine date range based on selection
    end_date = datetime.now()
    
    if time_range == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last Quarter":
        start_date = end_date - timedelta(days=90)
    elif time_range == "Last Year":
        start_date = end_date - timedelta(days=365)
    else:  # All Time
        start_date = end_date - timedelta(days=730)  # ~2 years
    
    # License types
    license_types = [
        "Enterprise Governance", 
        "Manufacturing Control",
        "Distribution Network",
        "Retail Operations",
        "Supply Chain Analytics",
        "Financial Management",
        "Inventory Control"
    ]
    
    # Licensee companies
    licensees = [
        "VOI Jeans Ltd.",
        "Fashion Retail Group",
        "Textile Manufacturing Inc.",
        "Apparel Distribution Co.",
        "Global Logistics Partners",
        "Retail Analytics Solutions",
        "Supply Chain Innovations",
        "Fashion Management Group",
        "Clothing Retail Chain"
    ]
    
    # Generate random licenses
    licenses = []
    
    # Number of licenses based on time range
    if time_range == "Last 30 Days":
        num_licenses = random.randint(5, 10)
    elif time_range == "Last Quarter":
        num_licenses = random.randint(15, 25)
    elif time_range == "Last Year":
        num_licenses = random.randint(30, 50)
    else:  # All Time
        num_licenses = random.randint(50, 80)
    
    for _ in range(num_licenses):
        # Random issue date within range
        days_span = (end_date - start_date).days
        issued_date = start_date + timedelta(days=random.randint(0, days_span))
        
        # License duration between 6 months and 2 years
        duration_days = random.randint(180, 730)
        expiry_date = issued_date + timedelta(days=duration_days)
        
        # License value between $10,000 and $500,000
        value = random.randint(10, 500) * 1000
        
        # Determine status based on expiry date
        if expiry_date < datetime.now():
            status = random.choices(
                ["Expired", "Revoked"], 
                weights=[0.8, 0.2]
            )[0]
        elif expiry_date < datetime.now() + timedelta(days=30):
            status = "Pending Renewal"
        else:
            status = "Active"
        
        licenses.append({
            "Licensee": random.choice(licensees),
            "Type": random.choice(license_types),
            "Issued Date": issued_date,
            "Expiry Date": expiry_date,
            "Value": value,
            "Status": status
        })
    
    return pd.DataFrame(licenses)

def generate_governance_events(event_types, priority_levels):
    """Generate governance events based on selected filters"""
    events = []
    
    # Event descriptions by type
    descriptions = {
        "Policy Change": [
            "Updated data governance policy to enhance compliance with industry standards",
            "Revised security protocols for enterprise application access",
            "Implemented new license validation procedures",
            "Modified financial reporting requirements for licensees",
            "Updated user access control policies"
        ],
        "Audit": [
            "Conducted comprehensive license compliance audit",
            "Performed security controls assessment",
            "Reviewed financial reporting accuracy",
            "Audited data governance implementation",
            "Completed enterprise application usage audit"
        ],
        "Inspection": [
            "Inspected manufacturing facility for compliance",
            "Conducted on-site review of inventory management systems",
            "Inspected retail operations for license adherence",
            "Performed distribution center operational review",
            "Inspected data center security measures"
        ],
        "Compliance Review": [
            "Assessed compliance with updated governance standards",
            "Reviewed license usage against terms and conditions",
            "Evaluated regulatory compliance for enterprise applications",
            "Reviewed data protection measures for compliance",
            "Assessed operational adherence to governance policies"
        ],
        "Milestone": [
            "Reached 100 active enterprise licenses",
            "Achieved governance implementation across all business units",
            "Completed integration of enterprise governance framework",
            "Graduated first cohort of governance certified managers",
            "Implemented enterprise-wide reporting system"
        ],
        "Risk Event": [
            "Identified potential security vulnerability in license verification",
            "Detected attempted unauthorized access to governance system",
            "Observed compliance deviation in retail operations",
            "Noted potential financial reporting discrepancy",
            "Identified risk in supply chain governance implementation"
        ]
    }
    
    # Generate events for the past 180 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    # Number of events depends on selected filters
    num_events = len(event_types) * random.randint(3, 7)
    
    for _ in range(num_events):
        # Select event type from chosen types
        event_type = random.choice(event_types)
        
        # Select priority from chosen levels
        priority = random.choice(priority_levels)
        
        # Random date within range
        days_span = (end_date - start_date).days
        event_date = start_date + timedelta(days=random.randint(0, days_span))
        
        # Random number of affected licenses
        affected = random.randint(1, 20)
        
        # Create event
        events.append({
            "Type": event_type,
            "Title": f"{event_type}: {random.choice(descriptions[event_type][:3])}",
            "Description": random.choice(descriptions[event_type]),
            "Date": event_date,
            "Priority": priority,
            "Affected": affected
        })
    
    # Sort by date
    return sorted(events, key=lambda x: x['Date'], reverse=True)

def generate_compliance_data(metric, period):
    """Generate sample compliance data for visualization"""
    # Determine date range
    end_date = datetime.now()
    
    if period == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
        freq = 'D'  # Daily data points
    elif period == "Last Quarter":
        start_date = end_date - timedelta(days=90)
        freq = 'W'  # Weekly data points
    else:  # Last Year
        start_date = end_date - timedelta(days=365)
        freq = 'M'  # Monthly data points
    
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    # Categories to include based on selected metric
    if metric == "Overall Compliance":
        categories = ["Financial", "Operational", "Security", "Legal"]
    else:
        # Extract first word from metric as category
        category = metric.split()[0]
        categories = [category]
    
    # Generate data for each category
    data = []
    
    for category in categories:
        # Base compliance level and trend direction
        if category == "Financial":
            base = random.uniform(92, 95)
            trend = random.uniform(0.05, 0.2)  # Positive trend
        elif category == "Operational":
            base = random.uniform(88, 92)
            trend = random.uniform(0.1, 0.3)  # Positive trend
        elif category == "Security":
            base = random.uniform(90, 93)
            trend = random.uniform(-0.1, 0.2)  # Mixed trend
        else:  # Legal or other
            base = random.uniform(94, 97)
            trend = random.uniform(0, 0.1)  # Slight positive trend
        
        # Generate compliance values with trend and some randomness
        for i, date in enumerate(date_range):
            # Add trend over time with some randomness
            compliance = min(base + (trend * i) + random.uniform(-1, 1), 100)
            
            # Special case: if date is around 1/3 through the range, add a dip for drama
            if i == len(date_range) // 3:
                compliance -= random.uniform(3, 7)
            
            data.append({
                "Date": date,
                "Category": category,
                "Compliance": compliance
            })
    
    return pd.DataFrame(data)

def generate_integration_data():
    """Generate integration timeline data"""
    # Define possible integration events
    event_types = [
        "API Integration",
        "Data Flow Established",
        "Module Connection",
        "System Upgrade",
        "Integration Enhancement"
    ]
    
    # Define core components
    components = [
        "Empire OS", 
        "Virtual Silk Road", 
        "Synergyze", 
        "Enterprise App"
    ]
    
    # Generate random integration events
    events = []
    
    # Date range for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Generate 15-25 events
    for _ in range(random.randint(15, 25)):
        # Random date within range
        days_span = (end_date - start_date).days
        event_date = start_date + timedelta(days=random.randint(0, days_span))
        
        # Source and target components (ensure they're different)
        source = random.choice(components)
        target = random.choice([c for c in components if c != source])
        
        # Integration event details
        event = {
            "date": event_date,
            "event_type": random.choice(event_types),
            "source": source,
            "target": target,
            "description": f"{random.choice(event_types)} between {source} and {target}"
        }
        
        events.append(event)
    
    # Sort by date
    return sorted(events, key=lambda x: x['date'])