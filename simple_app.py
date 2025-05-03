import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def main():
    """
    Simplified Empire OS for diagnostic purposes
    """
    st.set_page_config(
        page_title="Empire OS - Divine Mechanics",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar navigation
    st.sidebar.title("Empire OS")
    st.sidebar.subheader("Divine Mechanics")
    
    nav_selection = st.sidebar.radio(
        "Navigation", 
        ["Home", "Divine License Ledger", "Realm Panes", "Divine Alignment"]
    )
    
    # Apply custom styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1E1E1E;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 24px;
        color: #4A4A4A;
        margin-bottom: 20px;
    }
    .pane-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .metric-container {
        background-color: #F0F2F6;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if nav_selection == "Home":
        show_home()
    elif nav_selection == "Divine License Ledger":
        show_license_ledger()
    elif nav_selection == "Realm Panes":
        show_realm_panes()
    elif nav_selection == "Divine Alignment":
        show_divine_alignment()

def show_home():
    """Display the home dashboard"""
    st.markdown('<div class="main-header">Empire OS - Divine Mechanics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Unified Enterprise Governance Operating System</div>', unsafe_allow_html=True)
    
    # System overview
    st.subheader("System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Active Licenses", value=random.randint(80, 120), delta=random.randint(1, 10))
        
    with col2:
        st.metric(label="Realm Health", value=f"{random.randint(90, 99)}%", delta=f"{random.randint(1, 5)}%")
        
    with col3:
        st.metric(label="Divine Alignment", value=f"{random.randint(85, 95)}%", delta=f"{random.randint(-2, 5)}%")
    
    # Create sample activity data
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    activity = [random.randint(5, 50) for _ in range(30)]
    licenses = [random.randint(70, 130) for _ in range(30)]
    
    # Convert to DataFrame
    activity_df = pd.DataFrame({
        'Date': dates,
        'Activity': activity,
        'Active Licenses': licenses
    })
    
    # Create activity chart
    fig = px.line(activity_df, x='Date', y=['Activity', 'Active Licenses'], 
                 title='System Activity (Last 30 Days)')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent events
    st.subheader("Recent Events")
    
    event_types = ["License Issued", "License Renewed", "License Terminated", 
                  "Realm Scanned", "Divine Alignment Checked"]
    statuses = ["Completed", "Completed", "Completed", "Pending", "In Progress"]
    timestamps = [(datetime.now() - timedelta(minutes=random.randint(5, 300))).strftime("%Y-%m-%d %H:%M") 
                 for _ in range(5)]
    
    events_df = pd.DataFrame({
        "Event Type": event_types,
        "Status": statuses,
        "Timestamp": timestamps
    })
    
    st.dataframe(events_df, use_container_width=True)

def show_license_ledger():
    """Display the Divine License Ledger"""
    st.markdown('<div class="main-header">Divine License Ledger</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">License Flow and Governance Records</div>', unsafe_allow_html=True)
    
    # License metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Licenses", value=random.randint(100, 150))
        
    with col2:
        st.metric(label="Active", value=random.randint(80, 120))
        
    with col3:
        st.metric(label="Pending", value=random.randint(5, 20))
        
    with col4:
        st.metric(label="Expired", value=random.randint(10, 30))
    
    # License data
    license_statuses = ["Active", "Active", "Active", "Active", "Pending", "Expired"]
    license_types = ["Full", "Standard", "Basic", "Trial", "Enterprise", "Developer"]
    license_dates = [(datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d") 
                   for _ in range(6)]
    expiry_dates = [(datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d") 
                   for _ in range(6)]
    
    license_df = pd.DataFrame({
        "License ID": [f"LIC-{random.randint(1000, 9999)}" for _ in range(6)],
        "Type": license_types,
        "Status": license_statuses,
        "Issue Date": license_dates,
        "Expiry Date": expiry_dates,
        "Divine Alignment": [f"{random.randint(80, 99)}%" for _ in range(6)]
    })
    
    st.dataframe(license_df, use_container_width=True)
    
    # License distribution
    st.subheader("License Distribution")
    
    # Create license type distribution
    license_counts = {
        "Full": random.randint(30, 50),
        "Standard": random.randint(40, 60),
        "Basic": random.randint(20, 40),
        "Trial": random.randint(10, 30),
        "Enterprise": random.randint(5, 15),
        "Developer": random.randint(15, 25)
    }
    
    license_dist_df = pd.DataFrame({
        "License Type": list(license_counts.keys()),
        "Count": list(license_counts.values())
    })
    
    fig = px.bar(license_dist_df, x="License Type", y="Count", 
                title="License Distribution by Type")
    st.plotly_chart(fig, use_container_width=True)

def show_realm_panes():
    """Display the Realm Panes visualization"""
    st.markdown('<div class="main-header">Realm Panes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Realm One - Pane Cluster Stack</div>', unsafe_allow_html=True)
    
    # Display description of panes
    st.write("""
    The Realm One Pane Cluster Stack represents the core components of the Empire OS
    Divine Mechanics system. Each pane serves a specific function in the governance framework.
    """)
    
    # Create columns for panes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pane-title">Justice Pane</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="metric-container">
        Responsible for ensuring compliance with governance rules, 
        enforcing policies, and maintaining order within the system.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="pane-title">DigitalMe</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="metric-container">
        Manages digital identity verification and context, 
        ensuring proper authentication and authorization.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pane-title">Mercy Pane</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="metric-container">
        Provides flexibility and compassion in governance, 
        allowing for exceptions and adaptations when necessary.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="pane-title">Metering Pane</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="metric-container">
        Tracks usage, performance, and resources within the system,
        providing analytics and measurements for optimization.
        </div>
        """, unsafe_allow_html=True)
    
    # Central components
    st.markdown('<div class="pane-title">Divine License Ledger</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-container">
    The central record-keeping system that maintains all license transactions,
    governance events, and system activities. It serves as the single source of truth.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="pane-title">Transformer Pane</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-container">
    Processes and transforms governance inputs using divine principles,
    creating recommendations and actions based on the 99 names framework.
    </div>
    """, unsafe_allow_html=True)
    
    # Pane activity metrics
    st.subheader("Pane Activity Metrics")
    
    # Create sample pane activity data
    panes = ["Justice", "Mercy", "Transformer", "DigitalMe", "Metering"]
    transactions = [random.randint(50, 200) for _ in range(5)]
    uptime = [random.uniform(95, 99.9) for _ in range(5)]
    
    pane_df = pd.DataFrame({
        "Pane": panes,
        "Transactions": transactions,
        "Uptime (%)": uptime
    })
    
    # Create activity chart
    fig = px.bar(pane_df, x="Pane", y="Transactions", 
                title="Transactions by Pane",
                color="Transactions")
    st.plotly_chart(fig, use_container_width=True)

def show_divine_alignment():
    """Display the Divine Alignment visualization"""
    st.markdown('<div class="main-header">Divine Alignment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sustainable Devolution of Realms</div>', unsafe_allow_html=True)
    
    st.write("""
    Divine Alignment represents the core governance framework that ensures all activities
    within the Empire OS are aligned with the principles of People, Planet, and Profits.
    This triple bottom line approach ensures sustainable and ethical governance.
    """)
    
    # Create alignment score metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        people_score = random.randint(80, 95)
        st.metric(label="People Alignment", value=f"{people_score}%", 
                 delta=f"{random.randint(-3, 5)}%")
        
    with col2:
        planet_score = random.randint(75, 90)
        st.metric(label="Planet Alignment", value=f"{planet_score}%", 
                 delta=f"{random.randint(-2, 7)}%")
        
    with col3:
        profit_score = random.randint(85, 98)
        st.metric(label="Profit Alignment", value=f"{profit_score}%", 
                 delta=f"{random.randint(-1, 6)}%")
    
    # Overall divine alignment
    overall_score = (people_score + planet_score + profit_score) // 3
    
    st.subheader("Overall Divine Alignment")
    
    # Create a gauge chart for divine alignment
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Divine Alignment Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "royalblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 90], 'color': "lightblue"},
                {'range': [90, 100], 'color': "royalblue"}
            ],
            'threshold': {
                'line': {'color': "green", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Stakeholder distribution
    st.subheader("Stakeholder Distribution")
    
    # Create stakeholder data
    stakeholders = {
        "Believers": random.randint(60, 80),
        "Non-Believers": random.randint(15, 30),
        "Hypocrites": random.randint(5, 15)
    }
    
    stakeholder_df = pd.DataFrame({
        "Stakeholder": list(stakeholders.keys()),
        "Percentage": list(stakeholders.values())
    })
    
    fig = px.pie(stakeholder_df, values="Percentage", names="Stakeholder",
                title="Stakeholder Distribution", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()