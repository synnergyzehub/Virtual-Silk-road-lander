import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import random
from datetime import datetime, timedelta
from core.modules.github_integration import GitHubIntegration, REPOSITORY_FLOORS

def show_github_floors():
    """
    Display the GitHub Floors visualization - part of the Empire OS
    where code repositories are managed across hierarchical floors.
    """
    st.title("GitHub Floors - Empire OS Code Management")
    st.subheader("Repository Floors & Divine Alignment Visualization")
    
    # Initialize GitHub integration
    github = GitHubIntegration()
    
    # Create sidebar for navigation
    st.sidebar.title("Empire OS Navigation")
    page = st.sidebar.selectbox(
        "Choose View",
        ["Floor Overview", "Repository Explorer", "Contribution Analytics", "Divine Alignment", "Integration Dashboard"]
    )
    
    # Mock user license level (in a real app, this would come from authenticated user)
    user_license_level = 4  # Emperor level for demo
    
    if page == "Floor Overview":
        show_floor_overview(github, user_license_level)
    elif page == "Repository Explorer":
        show_repository_explorer(github, user_license_level)
    elif page == "Contribution Analytics":
        show_contribution_analytics(github)
    elif page == "Divine Alignment":
        show_divine_alignment(github)
    elif page == "Integration Dashboard":
        show_integration_dashboard(github)

def show_floor_overview(github, license_level):
    """Display an overview of all repository floors"""
    st.header("Repository Floor Overview")
    
    # Get floors accessible to the user
    accessible_floors = github.get_repository_floors(license_level)
    
    # Create floor visualization
    st.subheader("Floor Architecture")
    
    # Use columns for building-like structure
    cols = st.columns(len(accessible_floors))
    
    # Floor colors based on license level
    floor_colors = {
        4: "#3498db",  # Emperor - Blue
        3: "#2ecc71",  # Governor - Green
        2: "#f39c12",  # Operator - Orange
        1: "#95a5a6"   # Viewer - Gray
    }
    
    # Display floors from bottom to top (higher floors first in visual)
    for i, (floor_id, floor_data) in enumerate(reversed(list(accessible_floors.items()))):
        with cols[i]:
            license_color = floor_colors.get(floor_data["license_level_required"], "#95a5a6")
            st.markdown(f"""
            <div style="background-color: {license_color}; padding: 10px; border-radius: 5px; margin-bottom: 5px; color: white;">
                <h3 style="margin: 0;">{floor_data['name']}</h3>
                <p style="margin: 0; font-size: 0.8em;">{floor_id}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"*{floor_data['description']}*")
            st.markdown(f"**License Level:** {floor_data['license_level_required']}")
            st.markdown(f"**Repositories:** {len(floor_data['repositories'])}")
            
            # Show repositories in this floor
            for repo in floor_data['repositories']:
                st.markdown(f"""
                <div style="border: 1px solid {license_color}; padding: 5px; border-radius: 3px; margin-bottom: 5px;">
                    <p style="margin: 0; font-weight: bold;">{repo['name']}</p>
                    <p style="margin: 0; font-size: 0.8em;">{repo['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Floor distribution metrics
    st.subheader("Floor Distribution")
    
    # Prepare data for charts
    floor_data = []
    for floor_id, floor in accessible_floors.items():
        floor_data.append({
            "floor_id": floor_id,
            "name": floor["name"],
            "repositories": len(floor["repositories"]),
            "license_level": floor["license_level_required"]
        })
    
    floor_df = pd.DataFrame(floor_data)
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            floor_df,
            x="floor_id",
            y="repositories",
            color="license_level",
            title="Repositories by Floor",
            color_continuous_scale=px.colors.sequential.Blues
        )
        st.plotly_chart(fig1)
    
    with col2:
        fig2 = px.pie(
            floor_df,
            values="repositories",
            names="name",
            title="Repository Distribution"
        )
        st.plotly_chart(fig2)
    
    # Repository creation form
    st.header("Create New Repository")
    with st.form("new_repository_form"):
        repo_name = st.text_input("Repository Name")
        repo_description = st.text_area("Description")
        repo_floor = st.selectbox("Floor", list(accessible_floors.keys()))
        
        submitted = st.form_submit_button("Create Repository")
        if submitted and repo_name:
            # Mock license context (would come from authenticated user)
            license_context = {
                "role": "emperor",
                "license_level": license_level
            }
            
            result = github.create_repository(
                repo_name,
                repo_description,
                repo_floor,
                license_context
            )
            
            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])
    
    # External repository integration
    st.header("Link External GitHub Repository")
    with st.form("link_repository_form"):
        github_url = st.text_input("GitHub Repository URL")
        repo_floor = st.selectbox("Assign to Floor", list(accessible_floors.keys()), key="external_floor")
        
        submitted = st.form_submit_button("Link Repository")
        if submitted and github_url:
            # Mock license context (would come from authenticated user)
            license_context = {
                "role": "emperor",
                "license_level": license_level
            }
            
            result = github.link_external_repository(
                github_url,
                repo_floor,
                license_context
            )
            
            if result["success"]:
                st.success(result["message"])
            else:
                st.error(result["message"])

def show_repository_explorer(github, license_level):
    """Display detailed repository explorer"""
    st.header("Repository Explorer")
    
    # Get floors accessible to the user
    accessible_floors = github.get_repository_floors(license_level)
    
    # Flatten repositories into a single list
    all_repos = []
    for floor_id, floor_data in accessible_floors.items():
        for repo in floor_data['repositories']:
            repo_with_floor = repo.copy()
            repo_with_floor['floor_id'] = floor_id
            repo_with_floor['floor_name'] = floor_data['name']
            all_repos.append(repo_with_floor)
    
    # Convert to DataFrame
    repos_df = pd.DataFrame(all_repos)
    
    # Display filter options
    st.subheader("Filter Repositories")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_floor = st.selectbox(
            "Floor",
            ["All Floors"] + list(accessible_floors.keys())
        )
    
    # Apply filters
    filtered_repos = repos_df
    if selected_floor != "All Floors":
        filtered_repos = repos_df[repos_df['floor_id'] == selected_floor]
    
    # Display repositories
    st.subheader(f"Repositories ({len(filtered_repos)})")
    
    # Create a card for each repository
    for i, repo in filtered_repos.iterrows():
        with st.expander(f"{repo['name']} ({repo['floor_id']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {repo['description']}")
                st.markdown(f"**Floor:** {repo['floor_name']} ({repo['floor_id']})")
                
                # Add divine principle alignment (mock data)
                divine_principle = github._assign_divine_principle()
                st.markdown(f"**Divine Principle Alignment:** {divine_principle}")
                
                # Add mock activity data
                activity_level = random.choice(["High", "Medium", "Low"])
                st.markdown(f"**Activity Level:** {activity_level}")
            
            with col2:
                # Display license level indicator
                floor_license = accessible_floors[repo['floor_id']]['license_level_required']
                if floor_license == 4:
                    st.markdown("🔵 Emperor Level")
                elif floor_license == 3:
                    st.markdown("🟢 Governor Level")
                elif floor_license == 2:
                    st.markdown("🟠 Operator Level")
                else:
                    st.markdown("⚪ Viewer Level")
                
                # Add buttons for repository actions
                st.button("View Code", key=f"view_{i}")
                st.button("Clone Repository", key=f"clone_{i}")
                st.button("View Metrics", key=f"metrics_{i}")
    
    # Repository search
    st.subheader("Search Repositories")
    search_term = st.text_input("Search by name or description")
    
    if search_term:
        search_results = repos_df[
            repos_df['name'].str.contains(search_term, case=False) | 
            repos_df['description'].str.contains(search_term, case=False)
        ]
        
        if not search_results.empty:
            st.success(f"Found {len(search_results)} repositories")
            st.dataframe(search_results[['name', 'description', 'floor_id']])
        else:
            st.warning("No repositories found matching your search")

def show_contribution_analytics(github):
    """Display repository contribution analytics"""
    st.header("Contribution Analytics")
    
    # Repository selection (mock)
    selected_repo = st.selectbox(
        "Select Repository",
        ["Divine-Mechanics", "RiverOS-Core", "Realm-Governance", "Empire-OS-Dashboard", "Virtual-Silk-Road"]
    )
    
    # Time period selection
    time_period = st.selectbox(
        "Time Period",
        ["Last Week", "Last Month", "Last Quarter", "Year to Date"]
    )
    
    # Get mock contribution metrics
    metrics = github.get_contribution_metrics(selected_repo, time_period)
    
    # Display overall metrics
    st.subheader("Overall Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Commits", metrics['total_commits'])
    with col2:
        st.metric("Lines Added", metrics['total_additions'])
    with col3:
        st.metric("Lines Removed", metrics['total_deletions'])
    
    # Display divine alignment
    st.subheader("Divine Principle Alignment")
    alignment = metrics['divine_principle_alignment']
    
    # Create a gauge chart for alignment score
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=alignment['score'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Divine Alignment Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "red"},
                {'range': [60, 70], 'color': "orange"},
                {'range': [70, 85], 'color': "yellow"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    st.plotly_chart(fig)
    
    st.markdown(f"**Alignment Level:** {alignment['level']}")
    st.markdown(f"**Dominant Divine Principle:** {alignment['dominant_principle']}")
    
    # Display contributors
    st.subheader("Top Contributors")
    contrib_df = pd.DataFrame(metrics['contributors'])
    
    # Create contribution chart
    contrib_fig = px.bar(
        contrib_df.head(10),
        x='name',
        y='commits',
        color='divine_alignment_score',
        color_continuous_scale=px.colors.sequential.Viridis,
        title="Top 10 Contributors by Commits"
    )
    st.plotly_chart(contrib_fig)
    
    # Show contributor details
    st.dataframe(contrib_df[['name', 'role', 'commits', 'additions', 'deletions', 'divine_alignment_score']])
    
    # Contribution over time (mock)
    st.subheader("Contribution Over Time")
    
    # Generate mock time series data
    days = 90 if time_period == "Last Quarter" else 30
    dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
    
    time_data = pd.DataFrame({
        'date': dates,
        'commits': [random.randint(0, 15) for _ in range(days)],
        'alignment': [random.uniform(70, 95) for _ in range(days)]
    })
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Add commits line
    fig.add_trace(go.Scatter(
        x=time_data['date'],
        y=time_data['commits'],
        name='Commits',
        line=dict(color='blue', width=2)
    ))
    
    # Add alignment line on secondary axis
    fig.add_trace(go.Scatter(
        x=time_data['date'],
        y=time_data['alignment'],
        name='Divine Alignment',
        line=dict(color='red', width=2),
        yaxis='y2'
    ))
    
    # Update layout for dual y-axes
    fig.update_layout(
        title='Commits and Divine Alignment Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Commits',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Divine Alignment',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            anchor='x',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    st.plotly_chart(fig)

def show_divine_alignment(github):
    """Display divine alignment of code repositories"""
    st.header("Divine Alignment Analysis")
    
    # Generate mock data for divine alignment across repositories
    floors = github.get_repository_floors(4)  # Emperor level
    
    # Flatten repositories
    repos = []
    for floor_id, floor_data in floors.items():
        for repo in floor_data['repositories']:
            repo_copy = repo.copy()
            repo_copy['floor_id'] = floor_id
            repo_copy['floor_name'] = floor_data['name']
            repo_copy['license_level'] = floor_data['license_level_required']
            
            # Add mock alignment data
            repo_copy['alignment_score'] = random.uniform(60, 95)
            repo_copy['divine_principle'] = github._assign_divine_principle()
            
            repos.append(repo_copy)
    
    # Convert to DataFrame
    repos_df = pd.DataFrame(repos)
    
    # Calculate alignment metrics
    avg_alignment = repos_df['alignment_score'].mean()
    min_alignment = repos_df['alignment_score'].min()
    max_alignment = repos_df['alignment_score'].max()
    
    # Display overall metrics
    st.subheader("Overall Divine Alignment")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Alignment", f"{avg_alignment:.1f}%")
    with col2:
        st.metric("Lowest Alignment", f"{min_alignment:.1f}%")
    with col3:
        st.metric("Highest Alignment", f"{max_alignment:.1f}%")
    
    # Create visualization of alignment by floor
    st.subheader("Alignment by Floor")
    
    floor_alignment = repos_df.groupby(['floor_id', 'floor_name'])['alignment_score'].mean().reset_index()
    floor_fig = px.bar(
        floor_alignment,
        x='floor_id',
        y='alignment_score',
        color='alignment_score',
        color_continuous_scale=px.colors.sequential.Viridis,
        title="Average Divine Alignment by Floor",
        labels={'alignment_score': 'Alignment Score (%)'}
    )
    st.plotly_chart(floor_fig)
    
    # Divine principles distribution
    st.subheader("Divine Principles Distribution")
    
    principles_count = repos_df['divine_principle'].value_counts().reset_index()
    principles_count.columns = ['Principle', 'Count']
    
    principle_fig = px.pie(
        principles_count,
        values='Count',
        names='Principle',
        title="Distribution of Divine Principles"
    )
    st.plotly_chart(principle_fig)
    
    # Repository alignment ranking
    st.subheader("Repository Alignment Ranking")
    
    # Sort by alignment score
    ranked_repos = repos_df.sort_values('alignment_score', ascending=False)
    
    # Color function for alignment score
    def color_alignment(val):
        if val >= 90:
            return 'background-color: #c8e6c9'  # Light green
        elif val >= 80:
            return 'background-color: #fff9c4'  # Light yellow
        elif val >= 70:
            return 'background-color: #ffecb3'  # Light orange
        else:
            return 'background-color: #ffcdd2'  # Light red
    
    # Display styled dataframe
    styled_repos = ranked_repos[['name', 'floor_id', 'divine_principle', 'alignment_score']].style.applymap(
        color_alignment, subset=['alignment_score']
    )
    st.dataframe(styled_repos)
    
    # Alignment improvement recommendations
    st.subheader("Alignment Improvement Recommendations")
    
    # Find lowest aligned repositories
    low_aligned = ranked_repos[ranked_repos['alignment_score'] < 75].head(3)
    
    if not low_aligned.empty:
        for _, repo in low_aligned.iterrows():
            with st.expander(f"Improve: {repo['name']} ({repo['alignment_score']:.1f}%)"):
                st.markdown(f"**Current Principle:** {repo['divine_principle']}")
                
                # Generate random recommendations
                recommendations = [
                    "Integrate explicit divine principle references in documentation",
                    "Add ethical validation checks to core functions",
                    "Implement ESG impact assessment for critical operations",
                    "Review code for alignment with realm health metrics",
                    "Add balance verification in transaction processing"
                ]
                
                st.markdown("**Recommendations:**")
                for rec in random.sample(recommendations, 3):
                    st.markdown(f"- {rec}")
                
                st.markdown("**Expected Improvement:** +10-15% alignment")
    else:
        st.success("All repositories maintain good divine alignment!")

def show_integration_dashboard(github):
    """Display GitHub integration dashboard"""
    st.header("GitHub Integration Dashboard")
    
    # Mock integration status
    integration_status = {
        "connected": True,
        "api_status": "Healthy",
        "last_sync": (datetime.now() - timedelta(minutes=random.randint(5, 120))).strftime("%Y-%m-%d %H:%M:%S"),
        "webhooks": "Active",
        "sync_frequency": "15 minutes"
    }
    
    # Display connection status
    st.subheader("Connection Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if integration_status["connected"]:
            st.success("Connected to GitHub")
        else:
            st.error("Disconnected from GitHub")
    
    with col2:
        st.info(f"API Status: {integration_status['api_status']}")
    
    with col3:
        st.info(f"Last Synchronized: {integration_status['last_sync']}")
    
    # Integration settings
    st.subheader("Integration Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Webhooks:** {integration_status['webhooks']}")
        st.markdown(f"**Sync Frequency:** {integration_status['sync_frequency']}")
        st.markdown("**Authentication:** OAuth2")
    
    with col2:
        # Controls
        st.button("Force Synchronization")
        st.button("Reconnect GitHub")
        st.checkbox("Enable Automatic PR Reviews", value=True)
    
    # Activity feed
    st.subheader("Recent Activity")
    
    # Generate mock activity data
    activities = []
    
    activity_types = [
        "Repository Created", "Pull Request Merged", "Branch Created",
        "Issue Opened", "Code Review Completed", "Release Published"
    ]
    
    repos = ["Divine-Mechanics", "RiverOS-Core", "Realm-Governance", "Virtual-Silk-Road"]
    users = ["emperor", "realm-governor", "factory-operator", "developer-1"]
    
    for i in range(10):
        activities.append({
            "timestamp": (datetime.now() - timedelta(hours=i*3 + random.randint(0, 2))).strftime("%Y-%m-%d %H:%M"),
            "activity": random.choice(activity_types),
            "repository": random.choice(repos),
            "user": random.choice(users),
            "divine_principle": github._assign_divine_principle(),
            "alignment_score": random.randint(70, 98)
        })
    
    # Display activities
    activity_df = pd.DataFrame(activities)
    st.dataframe(activity_df)
    
    # Integration metrics
    st.subheader("Integration Metrics")
    
    # Generate mock metrics
    start_date = datetime.now() - timedelta(days=30)
    dates = [start_date + timedelta(days=i) for i in range(31)]
    
    metrics_data = pd.DataFrame({
        'date': dates,
        'sync_count': [random.randint(30, 100) for _ in range(31)],
        'api_calls': [random.randint(500, 2000) for _ in range(31)],
        'error_rate': [random.uniform(0, 5) for _ in range(31)]
    })
    
    # Create chart
    metric_fig = px.line(
        metrics_data,
        x='date',
        y=['sync_count', 'error_rate'],
        title="Integration Performance",
        labels={'value': 'Count', 'variable': 'Metric'}
    )
    st.plotly_chart(metric_fig)
    
    # Integration with other systems
    st.subheader("Integrations with Empire OS Components")
    
    integrations = [
        {"system": "License Gateway", "status": "Active", "health": "Good"},
        {"system": "Divine Transformer", "status": "Active", "health": "Excellent"},
        {"system": "ESG Validator", "status": "Active", "health": "Good"},
        {"system": "Realm Scanner", "status": "Active", "health": "Fair"},
        {"system": "Empire Dashboard", "status": "Active", "health": "Good"}
    ]
    
    # Display integrations
    integration_df = pd.DataFrame(integrations)
    
    # Color health status
    def color_health(val):
        if val == 'Excellent':
            return 'background-color: #c8e6c9'  # Light green
        elif val == 'Good':
            return 'background-color: #bbdefb'  # Light blue
        elif val == 'Fair':
            return 'background-color: #ffecb3'  # Light orange
        else:
            return 'background-color: #ffcdd2'  # Light red
    
    styled_integrations = integration_df.style.applymap(color_health, subset=['health'])
    st.dataframe(styled_integrations)

if __name__ == "__main__":
    show_github_floors()