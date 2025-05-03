import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import os

def show_emperor_timeline():
    """
    Display the Emperor Timeline component - part of the ECG governance layer
    where licenses are issued and enterprise governance is tracked.
    """
    st.title("Emperor Timeline - ECG Governance Layer")
    st.subheader("License and Governance Timeline Visualization")
    
    # Create sidebar for navigation
    st.sidebar.title("Empire OS Navigation")
    page = st.sidebar.selectbox(
        "Choose Visualization",
        ["License Timeline", "License Calendar", "Governance Timeline", "Integration Timeline", "Compliance Dashboard"]
    )
    
    # Filtering options
    st.sidebar.subheader("Filter Options")
    if page == "License Timeline":
        time_range = st.sidebar.selectbox(
            "Time Range",
            ["Last 7 Days", "Last 30 Days", "Last Quarter", "Year to Date", "All Time"]
        )
        license_data = generate_license_data(time_range)
        show_license_timeline(license_data)
        
    elif page == "License Calendar":
        time_range = st.sidebar.selectbox(
            "Time Range",
            ["Current Month", "Last 3 Months", "Year to Date"]
        )
        license_data = generate_license_data(time_range)
        show_license_calendar(license_data)
        
    elif page == "Governance Timeline":
        event_types = st.sidebar.multiselect(
            "Event Types",
            ["Policy Change", "Audit", "Compliance Check", "License Revocation", "System Update"],
            default=["Policy Change", "Audit", "Compliance Check"]
        )
        priority_levels = st.sidebar.multiselect(
            "Priority Levels",
            ["Critical", "High", "Medium", "Low"],
            default=["Critical", "High"]
        )
        governance_events = generate_governance_events(event_types, priority_levels)
        show_governance_timeline(governance_events)
        
    elif page == "Integration Timeline":
        integration_data = generate_integration_data()
        create_integration_timeline(integration_data)
        
    elif page == "Compliance Dashboard":
        metric = st.sidebar.selectbox(
            "Compliance Metric",
            ["License Compliance", "Governance Alignment", "Realm Health", "ESG Standards"]
        )
        period = st.sidebar.selectbox(
            "Time Period",
            ["Last Quarter", "Year to Date", "Last 12 Months"]
        )
        compliance_data = generate_compliance_data(metric, period)
        
        st.subheader(f"{metric} Dashboard")
        
        # Compliance score
        score = compliance_data["score"]
        st.metric("Compliance Score", f"{score}%", f"{compliance_data['change']}%")
        
        # Create gauge chart for compliance score
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{metric} Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 90], 'color': "yellow"},
                    {'range': [90, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig)
        
        # Show compliance trend
        st.subheader("Compliance Trend")
        trend_fig = px.line(
            compliance_data["trend"], 
            x="date", 
            y="score",
            title=f"{metric} - Trend Over Time"
        )
        st.plotly_chart(trend_fig)
        
        # Show compliance breakdown
        st.subheader("Compliance Breakdown")
        breakdown_fig = px.bar(
            compliance_data["breakdown"],
            x="category",
            y="score",
            color="score",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100],
            title="Component Compliance Scores"
        )
        st.plotly_chart(breakdown_fig)
        
        # Show non-compliance issues
        st.subheader("Non-Compliance Issues")
        issue_data = compliance_data["issues"]
        if issue_data.empty:
            st.success("No non-compliance issues detected!")
        else:
            st.dataframe(issue_data)

def show_license_timeline(license_data):
    """Display license data in a timeline view"""
    st.subheader("License Issuance Timeline")
    
    # License issuance over time chart
    issuance_fig = px.line(
        license_data.groupby('date').size().reset_index(name='count'),
        x="date",
        y="count",
        title="License Issuance Volume Over Time"
    )
    st.plotly_chart(issuance_fig)
    
    # License types distribution
    st.subheader("License Type Distribution")
    type_fig = px.pie(
        license_data, 
        names='license_type', 
        title="Distribution of License Types"
    )
    st.plotly_chart(type_fig)
    
    # License status timeline
    st.subheader("License Status Timeline")
    
    # Create a color map for status
    color_map = {
        "APPROVED": "#2ecc71",  # Green
        "CONDITIONAL": "#f39c12",  # Orange/Yellow
        "PENDING": "#3498db",  # Blue
        "DENIED": "#e74c3c",  # Red
        "REVOKED": "#c0392b",  # Darker Red
        "EXPIRED": "#95a5a6"   # Gray
    }
    
    # Create the Gantt chart for license timeline
    timeline_fig = px.timeline(
        license_data,
        x_start="issued_at",
        x_end="expires_at",
        y="license_id",
        color="status",
        color_discrete_map=color_map,
        hover_data=["holder", "realm", "license_type"]
    )
    timeline_fig.update_yaxes(autorange="reversed")
    st.plotly_chart(timeline_fig)
    
    # Divine principles distribution
    st.subheader("Divine Principles in License Issuance")
    principle_fig = px.bar(
        license_data.groupby('divine_principle').size().reset_index(name='count'),
        x="divine_principle",
        y="count",
        color="divine_principle",
        title="Divine Principles Applied in Licensing"
    )
    st.plotly_chart(principle_fig)
    
    # Filter to show recent licenses
    st.subheader("Recent License Activity")
    
    # Add status indicator function
    def status_indicator(status):
        if status == "APPROVED":
            return "🟢 "
        elif status == "CONDITIONAL":
            return "🟠 "
        elif status == "PENDING":
            return "🔵 "
        elif status == "DENIED":
            return "🔴 "
        elif status == "REVOKED":
            return "⛔ "
        elif status == "EXPIRED":
            return "⚪ "
        else:
            return ""
    
    # Add status indicator to dataframe
    license_data['status_icon'] = license_data['status'].apply(status_indicator)
    license_data['display_status'] = license_data['status_icon'] + license_data['status']
    
    # Show recent licenses
    recent_licenses = license_data.sort_values('issued_at', ascending=False).head(10)
    display_cols = ['license_id', 'holder', 'license_type', 'realm', 'display_status', 'divine_principle', 'issued_at']
    st.dataframe(recent_licenses[display_cols])
    
    # Show expanded view of a selected license
    st.subheader("License Details")
    selected_license = st.selectbox("Select License ID", license_data['license_id'].tolist())
    
    # Get details for selected license
    license_details = license_data[license_data['license_id'] == selected_license].iloc[0]
    
    # Create columns for details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**License ID:** {license_details['license_id']}")
        st.markdown(f"**Holder:** {license_details['holder']}")
        st.markdown(f"**License Type:** {license_details['license_type']}")
        st.markdown(f"**Realm:** {license_details['realm']}")
    
    with col2:
        st.markdown(f"**Status:** {license_details['status']}")
        st.markdown(f"**Issued At:** {license_details['issued_at']}")
        st.markdown(f"**Expires At:** {license_details['expires_at']}")
        st.markdown(f"**Divine Principle:** {license_details['divine_principle']}")
    
    # Show conditions if any
    if isinstance(license_details.get('conditions'), list) and license_details['conditions']:
        st.subheader("License Conditions")
        for condition in license_details['conditions']:
            st.markdown(f"- {condition}")

def show_license_calendar(license_data):
    """Display license data in a calendar view"""
    st.subheader("License Calendar View")
    
    # Convert dates to datetime if they're strings
    license_data['issued_at'] = pd.to_datetime(license_data['issued_at'])
    license_data['date'] = license_data['issued_at'].dt.date
    
    # Group by date and count licenses
    daily_counts = license_data.groupby('date').size().reset_index(name='count')
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])
    
    # Create heatmap calendar
    daily_counts['day_of_week'] = daily_counts['date'].dt.day_name()
    daily_counts['week'] = daily_counts['date'].dt.isocalendar().week
    daily_counts['month'] = daily_counts['date'].dt.month_name()
    
    # Sort days of week properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_counts['day_order'] = daily_counts['day_of_week'].apply(lambda x: day_order.index(x))
    daily_counts = daily_counts.sort_values(['week', 'day_order'])
    
    # Create heatmap
    fig = px.density_heatmap(
        daily_counts,
        x='day_of_week',
        y='week',
        z='count',
        category_orders={'day_of_week': day_order},
        labels={'count': 'License Count', 'day_of_week': 'Day', 'week': 'Week'},
        title='License Issuance Calendar Heatmap'
    )
    st.plotly_chart(fig)
    
    # Show daily license issuance
    st.subheader("Daily License Issuance")
    daily_fig = px.bar(
        daily_counts.sort_values('date'),
        x='date',
        y='count',
        title='Daily License Issuance Count'
    )
    st.plotly_chart(daily_fig)
    
    # Show license types by day of week
    license_data['day_of_week'] = license_data['issued_at'].dt.day_name()
    dow_type = pd.crosstab(license_data['day_of_week'], license_data['license_type'])
    dow_type = dow_type.reindex(day_order)
    
    dow_fig = px.imshow(
        dow_type,
        labels=dict(x="License Type", y="Day of Week", color="Count"),
        title="License Types by Day of Week"
    )
    st.plotly_chart(dow_fig)

def show_governance_timeline(governance_events):
    """Display governance events in a timeline visualization"""
    st.subheader("Governance Timeline")
    
    # Create color map for event types
    color_map = {
        "Policy Change": "#3498db",  # Blue
        "Audit": "#2ecc71",          # Green
        "Compliance Check": "#f1c40f", # Yellow
        "License Revocation": "#e74c3c", # Red
        "System Update": "#9b59b6"    # Purple
    }
    
    # Create symbols map for priority
    symbol_map = {
        "Critical": "diamond",
        "High": "circle",
        "Medium": "square",
        "Low": "x"
    }
    
    # Prepare the timeline
    timeline_fig = go.Figure()
    
    for event_type in governance_events['event_type'].unique():
        df_filtered = governance_events[governance_events['event_type'] == event_type]
        
        timeline_fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['event_type'],
            mode='markers',
            marker=dict(
                symbol=[symbol_map.get(p, 'circle') for p in df_filtered['priority']],
                size=12,
                color=color_map.get(event_type, '#333333'),
                line=dict(width=1, color='darkgrey')
            ),
            name=event_type,
            text=df_filtered['description'],
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Priority: ' + 
                         df_filtered['priority'].astype(str)
        ))
    
    timeline_fig.update_layout(
        title="Empire OS Governance Events Timeline",
        xaxis_title="Date",
        yaxis_title="Event Type",
        legend_title="Event Types",
        height=600
    )
    
    st.plotly_chart(timeline_fig)
    
    # Show event details table
    st.subheader("Governance Events")
    
    # Function to color priority
    def color_priority(val):
        if val == "Critical":
            return "background-color: #ffcccc"
        elif val == "High":
            return "background-color: #ffffcc"
        elif val == "Medium":
            return "background-color: #e6ffcc"
        else:
            return "background-color: #ccffcc"
    
    # Display the events table with styled priority
    styled_events = governance_events.sort_values('date', ascending=False).style.applymap(
        color_priority, subset=['priority']
    )
    st.dataframe(styled_events)
    
    # Show distribution of events by type and priority
    st.subheader("Event Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        type_fig = px.pie(
            governance_events, 
            names='event_type', 
            title="Event Types Distribution"
        )
        st.plotly_chart(type_fig)
    
    with col2:
        priority_fig = px.pie(
            governance_events, 
            names='priority',
            color='priority',
            color_discrete_map={
                "Critical": "#e74c3c",
                "High": "#f39c12",
                "Medium": "#3498db",
                "Low": "#2ecc71"
            },
            title="Priority Distribution"
        )
        st.plotly_chart(priority_fig)

def create_integration_timeline(integration_data):
    """Create a timeline visualization of enterprise integrations"""
    st.subheader("Enterprise Integration Timeline")
    
    # Create Gantt chart
    fig = px.timeline(
        integration_data,
        x_start="start_date",
        x_end="end_date",
        y="integration",
        color="status",
        hover_name="integration",
        hover_data=["description", "owner"],
        color_discrete_map={
            "Completed": "#2ecc71",
            "In Progress": "#3498db",
            "Planned": "#95a5a6",
            "Delayed": "#e74c3c"
        },
        title="Empire OS Integration Timeline"
    )
    
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
    
    # Show integration status summary
    st.subheader("Integration Status")
    
    status_counts = integration_data['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    status_fig = px.bar(
        status_counts,
        x='Status',
        y='Count',
        color='Status',
        color_discrete_map={
            "Completed": "#2ecc71",
            "In Progress": "#3498db",
            "Planned": "#95a5a6",
            "Delayed": "#e74c3c"
        },
        title="Integration Status Summary"
    )
    st.plotly_chart(status_fig)
    
    # Show integration details
    st.subheader("Integration Details")
    
    # Add current status indicator
    today = datetime.now().date()
    
    def get_progress(row):
        if row['status'] == 'Completed':
            return 100
        
        start = pd.to_datetime(row['start_date']).date()
        end = pd.to_datetime(row['end_date']).date()
        total_days = (end - start).days
        elapsed_days = (today - start).days
        
        if elapsed_days < 0:
            return 0
        if elapsed_days > total_days:
            return 99  # Not 100 because it's not marked complete
        
        return int((elapsed_days / total_days) * 100)
    
    integration_data['progress'] = integration_data.apply(get_progress, axis=1)
    
    for idx, row in integration_data.iterrows():
        with st.expander(f"{row['integration']} - {row['status']}"):
            col1, col2 = st.columns([3,1])
            
            with col1:
                st.markdown(f"**Description:** {row['description']}")
                st.markdown(f"**Owner:** {row['owner']}")
                st.markdown(f"**Timeline:** {row['start_date']} to {row['end_date']}")
                
                # Progress bar
                if row['status'] != 'Planned':
                    st.progress(row['progress'] / 100)
                    st.text(f"Progress: {row['progress']}%")
            
            with col2:
                if row['status'] == 'Completed':
                    st.success("Completed")
                elif row['status'] == 'In Progress':
                    st.info("In Progress")
                elif row['status'] == 'Planned':
                    st.warning("Planned")
                elif row['status'] == 'Delayed':
                    st.error("Delayed")

def generate_license_data(time_range):
    """Generate sample license data based on the selected time range"""
    # Determine date range based on selected time range
    today = datetime.now()
    
    if time_range == "Last 7 Days":
        start_date = today - timedelta(days=7)
    elif time_range == "Last 30 Days":
        start_date = today - timedelta(days=30)
    elif time_range == "Last Quarter":
        start_date = today - timedelta(days=90)
    elif time_range == "Year to Date":
        start_date = datetime(today.year, 1, 1)
    elif time_range == "Current Month":
        start_date = datetime(today.year, today.month, 1)
    elif time_range == "Last 3 Months":
        start_date = today - timedelta(days=90)
    else:  # All Time
        start_date = today - timedelta(days=365)
    
    # Generate number of licenses based on time range
    if time_range in ["Last 7 Days", "Current Month"]:
        num_licenses = random.randint(20, 50)
    elif time_range in ["Last 30 Days", "Last 3 Months"]:
        num_licenses = random.randint(50, 150)
    else:
        num_licenses = random.randint(150, 300)
    
    # License types and their probabilities
    license_types = ["Viewer", "Operator", "Governor", "Emperor"]
    type_probs = [0.4, 0.35, 0.2, 0.05]
    
    # License statuses and their probabilities
    statuses = ["APPROVED", "CONDITIONAL", "PENDING", "DENIED", "REVOKED", "EXPIRED"]
    status_probs = [0.6, 0.15, 0.1, 0.05, 0.05, 0.05]
    
    # Divine principles and their probabilities
    principles = ["Al-Adl (Justice)", "Ar-Rahman (Mercy)", "Al-Hakim (Wisdom)", 
                  "Al-Alim (Knowledge)", "Al-Muqsit (Equity)", "None"]
    principle_probs = [0.25, 0.2, 0.2, 0.15, 0.15, 0.05]
    
    # Realms
    realms = ["RealmOne", "RealmTwo", "RealmThree", "AllRealms"]
    realm_probs = [0.4, 0.3, 0.2, 0.1]
    
    # Holders
    holders = ["factory-operator", "retailer-agent", "realm-governor", "emperor", 
               "logistics-manager", "financial-analyst", "customer-service"]
    
    # Generate license data
    licenses = []
    
    for i in range(num_licenses):
        # Random date within the range
        date_range = (today - start_date).days
        random_days = random.randint(0, date_range)
        issue_date = today - timedelta(days=random_days)
        
        # Random expiration 30-90 days after issuance
        expire_days = random.randint(30, 90)
        expire_date = issue_date + timedelta(days=expire_days)
        
        # Select license type and other attributes
        license_type = random.choices(license_types, weights=type_probs)[0]
        status = random.choices(statuses, weights=status_probs)[0]
        principle = random.choices(principles, weights=principle_probs)[0]
        realm = random.choices(realms, weights=realm_probs)[0]
        holder = random.choice(holders)
        
        # Generate license ID
        license_id = f"LIC-{random.randint(10000, 99999)}"
        
        # Conditions (only for conditional licenses)
        conditions = None
        if status == "CONDITIONAL":
            possible_conditions = [
                "Initial batch limited to 500 units",
                "Weekly progress reports required",
                "Governance review after 15 days",
                "ESG impact monitoring mandatory",
                "Limited to non-critical operations"
            ]
            num_conditions = random.randint(1, 3)
            conditions = random.sample(possible_conditions, num_conditions)
        
        # Create license object
        license_obj = {
            "license_id": license_id,
            "holder": holder,
            "license_type": license_type,
            "realm": realm,
            "status": status,
            "divine_principle": principle,
            "issued_at": issue_date,
            "expires_at": expire_date,
            "conditions": conditions,
            "date": issue_date.date()  # For grouping
        }
        
        licenses.append(license_obj)
    
    # Convert to DataFrame
    license_df = pd.DataFrame(licenses)
    
    return license_df

def generate_governance_events(event_types, priority_levels):
    """Generate governance events based on selected filters"""
    # Determine date range (last 6 months)
    today = datetime.now()
    start_date = today - timedelta(days=180)
    
    # Number of events based on filters
    num_events = len(event_types) * len(priority_levels) * random.randint(2, 5)
    
    events = []
    
    for i in range(num_events):
        # Random date within range
        days_ago = random.randint(0, 180)
        event_date = today - timedelta(days=days_ago)
        
        # Select event type and priority
        event_type = random.choice(event_types)
        priority = random.choice(priority_levels)
        
        # Generate description based on event type
        if event_type == "Policy Change":
            descriptions = [
                "Updated license issuance criteria to include ESG impact assessment",
                "Modified realm governance structure for better accountability",
                "Added new divine principles to license evaluation",
                "Revised transaction approval workflow for high-volume orders",
                "Updated compliance requirements for cross-realm operations"
            ]
        elif event_type == "Audit":
            descriptions = [
                "Quarterly audit of license issuance compliance",
                "Realm health verification audit",
                "Divine alignment audit of governance decisions",
                "ESG impact assessment validation",
                "Audit of cross-realm transaction integrity"
            ]
        elif event_type == "Compliance Check":
            descriptions = [
                "Verified alignment of licenses with divine principles",
                "Checked adherence to realm health guidelines",
                "Reviewed ESG impact assessment accuracy",
                "Validated license conditions enforcement",
                "Verified transaction integrity across system"
            ]
        elif event_type == "License Revocation":
            descriptions = [
                "Revoked license due to repeated condition violations",
                "Enterprise-wide license review resulting in selective revocations",
                "Temporary suspension of licenses pending investigation",
                "License downgrade from Governor to Operator level",
                "Mandatory license renewal with enhanced scrutiny"
            ]
        else:  # System Update
            descriptions = [
                "Upgraded divine transformer algorithm for better recommendations",
                "Enhanced realm scanner sensitivity to economic imbalances",
                "Improved license gateway processing efficiency",
                "Added new ESG impact metrics to validation system",
                "Implemented faster transaction processing with integrity checks"
            ]
        
        description = random.choice(descriptions)
        
        # Realm affected
        realm = random.choice(["RealmOne", "RealmTwo", "RealmThree", "All Realms"])
        
        # Responsible entity
        responsible = random.choice(["Emperor", "Realm Governor", "System", "Governance Council", "Audit Committee"])
        
        events.append({
            "date": event_date,
            "event_type": event_type,
            "priority": priority,
            "description": description,
            "realm": realm,
            "responsible": responsible
        })
    
    # Convert to DataFrame and filter
    events_df = pd.DataFrame(events)
    
    # Sort by date
    events_df = events_df.sort_values("date")
    
    return events_df

def generate_compliance_data(metric, period):
    """Generate sample compliance data for visualization"""
    # Generate overall compliance score
    score = random.randint(75, 98)
    change = random.uniform(-5, 8)
    
    # Generate trend data
    if period == "Last Quarter":
        days = 90
    elif period == "Year to Date":
        days = (datetime.now() - datetime(datetime.now().year, 1, 1)).days
    else:  # Last 12 Months
        days = 365
    
    # Create dates
    dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -7)]
    
    # Generate scores with a slight upward trend and some noise
    base_score = score - (change * 5)  # Start lower if change is positive
    trend_scores = []
    
    for i in range(len(dates)):
        trend_score = min(100, max(50, base_score + (i * change / 10) + random.uniform(-5, 5)))
        trend_scores.append(trend_score)
    
    trend_data = pd.DataFrame({
        "date": dates,
        "score": trend_scores
    })
    
    # Generate breakdown data
    categories = []
    
    if metric == "License Compliance":
        categories = ["License Issuance", "Condition Monitoring", "Expiration Management", 
                      "Divine Alignment", "Cross-Realm Consistency"]
    elif metric == "Governance Alignment":
        categories = ["Policy Enforcement", "Decision Transparency", "Stakeholder Representation", 
                     "Divine Principle Adherence", "Accountability Mechanisms"]
    elif metric == "Realm Health":
        categories = ["Social Dimension", "Economic Dimension", "Ecological Dimension", 
                     "Spiritual Dimension", "Cross-Dimension Balance"]
    else:  # ESG Standards
        categories = ["Environmental Impact", "Social Responsibility", "Governance Quality", 
                     "Reporting Transparency", "Continuous Improvement"]
    
    # Generate scores for each category
    category_scores = []
    
    for category in categories:
        # Base on overall score but add variation
        cat_score = min(100, max(50, score + random.uniform(-15, 10)))
        category_scores.append(cat_score)
    
    breakdown_data = pd.DataFrame({
        "category": categories,
        "score": category_scores
    })
    
    # Generate issues data (more issues if score is lower)
    issues = []
    
    if score < 85:
        num_issues = random.randint(3, 6)
    elif score < 95:
        num_issues = random.randint(1, 3)
    else:
        num_issues = 0
    
    possible_issues = [
        "Incomplete license documentation for cross-realm transactions",
        "Divine principle application inconsistency in governance decisions",
        "Delayed compliance reporting in ecological dimension",
        "Insufficient stakeholder engagement in realm health monitoring",
        "ESG impact assessments lacking quantitative metrics",
        "Governance transparency declining in financial transactions",
        "Realm scanner sensitivity requiring recalibration",
        "License condition monitoring showing gaps in enforcement",
        "Social dimension metrics showing negative trend in community wellbeing",
        "Spiritual alignment verification process needs enhancement"
    ]
    
    if num_issues > 0:
        selected_issues = random.sample(possible_issues, num_issues)
        severity = ["High", "Medium", "Low"]
        
        for issue in selected_issues:
            issues.append({
                "issue": issue,
                "severity": random.choice(severity),
                "identified": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "status": random.choice(["Open", "In Progress", "Scheduled"])
            })
    
    issues_data = pd.DataFrame(issues)
    
    # Combine all data
    compliance_data = {
        "score": score,
        "change": round(change, 1),
        "trend": trend_data,
        "breakdown": breakdown_data,
        "issues": issues_data
    }
    
    return compliance_data

def generate_integration_data():
    """Generate integration timeline data"""
    # Define integrations
    integrations = [
        {
            "integration": "Digital Me Identity System",
            "description": "Core identity and authentication module integration",
            "owner": "Identity Team",
            "start_date": "2025-01-15",
            "end_date": "2025-03-01",
            "status": "Completed"
        },
        {
            "integration": "License Gateway",
            "description": "Divine principle-based licensing system",
            "owner": "Governance Team",
            "start_date": "2025-02-01",
            "end_date": "2025-04-15",
            "status": "Completed"
        },
        {
            "integration": "ESG Validator",
            "description": "Transaction validation based on ESG impact",
            "owner": "Sustainability Team",
            "start_date": "2025-03-01",
            "end_date": "2025-05-15",
            "status": "In Progress"
        },
        {
            "integration": "Realm Scanner",
            "description": "Realm health monitoring and alerting system",
            "owner": "Monitoring Team",
            "start_date": "2025-03-15",
            "end_date": "2025-06-01",
            "status": "In Progress"
        },
        {
            "integration": "Divine Transformer",
            "description": "Divine principle recommendation engine",
            "owner": "Core Algorithms Team",
            "start_date": "2025-04-01",
            "end_date": "2025-07-15",
            "status": "In Progress"
        },
        {
            "integration": "Federal Alignment Protocol",
            "description": "Cross-realm governance synchronization",
            "owner": "Integration Team",
            "start_date": "2025-05-01",
            "end_date": "2025-08-15",
            "status": "Planned"
        },
        {
            "integration": "Realm Action Ledger",
            "description": "Immutable transaction recording system",
            "owner": "Data Team",
            "start_date": "2025-04-15",
            "end_date": "2025-07-01",
            "status": "In Progress"
        },
        {
            "integration": "RiverOS Simulation Engine",
            "description": "Predictive simulation for actions and decisions",
            "owner": "Data Science Team",
            "start_date": "2025-06-01",
            "end_date": "2025-09-15",
            "status": "Planned"
        },
        {
            "integration": "Divine Alignment Layer",
            "description": "Ethical oversight and alignment verification system",
            "owner": "Ethics Team",
            "start_date": "2025-06-15",
            "end_date": "2025-10-01",
            "status": "Planned"
        },
        {
            "integration": "Virtual Silk Road Portal",
            "description": "Public-facing marketplace and collaboration platform",
            "owner": "User Experience Team",
            "start_date": "2025-03-01",
            "end_date": "2025-05-15",
            "status": "Delayed"
        }
    ]
    
    # Convert to DataFrame
    return pd.DataFrame(integrations)

if __name__ == "__main__":
    show_emperor_timeline()