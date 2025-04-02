import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import random

def show_empire_os_dashboard():
    """
    Display the Emperor's private dashboard for Empire OS.
    This is a comprehensive visualization of license functioning and system performance.
    Only accessible to authenticated users with Emperor-level access.
    """
    
    # Emperor's header with special styling for the dashboard
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(75,0,130,1) 100%); 
        padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
            <h1 style='color: gold; margin: 0; font-size: 3rem;'>👑 Emperor's Control Terminal</h1>
            <p style='color: white; margin: 15px 0 0 0; font-size: 1.5rem;'>Empire OS Command Interface</p>
            <p style='color: rgba(255,255,255,0.7); margin: 10px 0 0 0;'>Authorized Access: Emperor Level</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Dashboard tabs for different sections
    tabs = st.tabs([
        "🌐 System Overview", 
        "⚡ License Performance", 
        "📊 Analytics Hub",
        "🔧 Control Center"
    ])
    
    # Tab 1: System Overview
    with tabs[0]:
        st.header("Empire OS System Overview")
        st.write("Real-time monitoring and control of the entire Empire OS ecosystem.")
        
        # System metrics in a grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Create a pulsing metric with animation effect
            current_value = 99.98
            
            # Create a container for the animated metric
            metric_container = st.empty()
            
            # Display initial metric
            metric_container.metric(
                "System Uptime", 
                f"{current_value}%", 
                "+0.03%"
            )
            
            # Add a light pulsing effect using CSS
            st.markdown("""
            <style>
            [data-testid="stMetricValue"] {
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.8; }
                100% { opacity: 1; }
            }
            </style>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Active Licenses", "327", "+3 today")
            
        with col3:
            st.metric("Revenue (Monthly)", "$1.24M", "+2.8%")
        
        # Create an animated network visualization
        st.subheader("Empire OS Network Activity")
        st.write("Real-time visualization of data flows between system components")
        
        # Generate network data for the animated visualization
        nodes = ["Core Kernel", "Governance", "API Gateway", "License Manager", "Security", "Data Store", "Analytics"]
        node_color = ["gold", "purple", "blue", "green", "red", "orange", "teal"]
        
        # Create an empty figure
        network_container = st.empty()
        
        # Generate random node positions
        np.random.seed(42)  # For reproducibility
        node_x = np.random.rand(len(nodes)) 
        node_y = np.random.rand(len(nodes))
        
        # Function to create a frame of the animation
        def create_network_frame():
            # Create random edges for this frame
            edges = []
            for i in range(10):  # Random number of edges
                source = np.random.randint(0, len(nodes))
                target = np.random.randint(0, len(nodes))
                if source != target:  # Avoid self-loops
                    edges.append((source, target))
            
            # Create edge traces
            edge_x = []
            edge_y = []
            
            for edge in edges:
                x0, y0 = node_x[edge[0]], node_y[edge[0]]
                x1, y1 = node_x[edge[1]], node_y[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1, color='rgba(150, 150, 150, 0.5)'),
                hoverinfo='none',
                mode='lines')
            
            # Create node trace
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=nodes,
                textposition="top center",
                marker=dict(
                    showscale=False,
                    color=node_color,
                    size=20,
                    line=dict(width=1, color='rgba(50, 50, 50, 0.8)')),
                hoverinfo='text',
                textfont=dict(size=10))
            
            # Create animation frame
            fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Real-time System Communication",
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=500,
                    plot_bgcolor='rgba(0, 0, 0, 0.02)')
            )
            
            # Add pulse animation to edges
            for i in range(len(edges)):
                # Add animated markers moving along the edges
                pulse_x = [node_x[edges[i][0]] + (node_x[edges[i][1]] - node_x[edges[i][0]]) * 0.5]
                pulse_y = [node_y[edges[i][0]] + (node_y[edges[i][1]] - node_y[edges[i][0]]) * 0.5]
                
                fig.add_trace(go.Scatter(
                    x=pulse_x, y=pulse_y,
                    mode='markers',
                    marker=dict(
                        size=8,
                        color='rgba(255, 215, 0, 0.7)',  # Gold color with transparency
                        symbol='circle',
                        line=dict(width=1)
                    ),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            return fig
        
        # Display the initial network visualization
        network_container.plotly_chart(create_network_frame(), use_container_width=True)
        
        # Add animated data flow metrics
        st.subheader("Real-time System Performance Metrics")
        
        metrics_cols = st.columns(2)
        
        with metrics_cols[0]:
            # Create an animated performance chart
            performance_container = st.empty()
            
            # Generate time series data
            time_points = 100
            x = list(range(time_points))
            y = [random.normalvariate(90, 5) for _ in range(time_points)]
            
            # Function to update the performance chart
            def update_performance_chart():
                # Create figure
                fig = px.line(
                    x=x, y=y,
                    labels={"x": "Time (s)", "y": "Performance Score"},
                    title="Core Kernel Performance"
                )
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    yaxis_range=[60, 100]
                )
                
                return fig
            
            # Display the initial performance chart
            performance_container.plotly_chart(update_performance_chart(), use_container_width=True)
        
        with metrics_cols[1]:
            # Create an animated CPU usage gauge
            cpu_container = st.empty()
            
            # Function to update the CPU gauge
            def update_cpu_gauge():
                # Create CPU usage gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=random.randint(25, 40),  # Random CPU usage between 25-40%
                    title={"text": "CPU Utilization"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "green"},
                        "steps": [
                            {"range": [0, 50], "color": "lightgreen"},
                            {"range": [50, 80], "color": "orange"},
                            {"range": [80, 100], "color": "red"}
                        ]
                    }
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                return fig
            
            # Display the initial CPU gauge
            cpu_container.plotly_chart(update_cpu_gauge(), use_container_width=True)
            
    # Tab 2: License Performance
    with tabs[1]:
        st.header("License Performance Analytics")
        
        # Add a "live data" indicator with animation
        st.markdown("""
        <div style='display: flex; align-items: center;'>
            <p style='margin: 0; color: rgba(0,0,0,0.6);'>Comprehensive visualization of license allocation, usage, and real-time performance metrics.</p>
            <span style='margin-left: 10px; font-size: 0.7em; padding: 2px 8px; background-color: rgba(75,0,130,0.1); border-radius: 10px; color: #4B0082;'>
                <span style='animation: pulse 2s infinite;'>●</span> Live Data
            </span>
        </div>
        <style>
        @keyframes pulse {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create license performance overview
        license_col1, license_col2 = st.columns([2, 1])
        
        with license_col1:
            # Create interactive control panel first
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                st.selectbox("Filter by License Family", ["All Families", "Manufacturing", "Distribution", "Financial", "Marketing", "Supply Chain"], index=0)
            with filter_col2:
                st.selectbox("Time Period", ["Last 30 Days", "Last Quarter", "Year to Date", "All Time"], index=0)
                
            # Emperor's special visualization controls
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(0,0,0,0.05) 0%, rgba(75,0,130,0.1) 100%); 
                        padding: 10px; border-radius: 8px; margin: 10px 0; border: 1px solid rgba(75,0,130,0.3);'>
                <div style='display: flex; align-items: center;'>
                    <span style='color: gold; margin-right: 8px;'>👑</span>
                    <span style='color: #4B0082; font-weight: bold;'>Emperor's Visualization Controls</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create interactive sunburst chart
            license_families = ["Manufacturing", "Distribution", "Financial", "Marketing", "Supply Chain"]
            license_types = []
            license_counts = []
            license_revenues = []
            license_renewal_rates = []
            
            # Generate hierarchical license data
            for family in license_families:
                for i in range(3):  # 3 subtypes per family
                    subtype = f"{family} {['Basic', 'Advanced', 'Premium'][i]}"
                    license_types.append(subtype)
                    count = random.randint(10, 100)
                    license_counts.append(count)
                    
                    # Calculate revenue based on type and count
                    base_price = random.randint(100, 1000)
                    revenue = count * base_price
                    license_revenues.append(revenue)
                    
                    # Add renewal rates
                    renewal_rate = random.uniform(0.85, 0.98)
                    license_renewal_rates.append(renewal_rate)
            
            # Create dataframe for the sunburst chart
            license_data = pd.DataFrame({
                "LicenseFamily": [family for family in license_families for _ in range(3)],
                "LicenseType": license_types,
                "Count": license_counts,
                "Revenue": license_revenues,
                "RenewalRate": license_renewal_rates
            })
            
            # Visualization type selector
            viz_type = st.radio(
                "Visualization Metric",
                ["License Count", "Revenue", "Renewal Rate"],
                horizontal=True
            )
            
            color_metric = "Revenue"
            if viz_type == "License Count":
                color_metric = "Count"
            elif viz_type == "Renewal Rate":
                color_metric = "RenewalRate"
            
            # Create enhanced interactive sunburst chart
            fig = px.sunburst(
                license_data,
                path=["LicenseFamily", "LicenseType"],
                values="Count",
                color=color_metric,
                color_continuous_scale="Viridis",
                hover_data=["Revenue", "RenewalRate"],
                custom_data=["Revenue", "RenewalRate"]
            )
            
            # Enhance hover information
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                              "Licenses: %{value}<br>" +
                              "Revenue: $%{customdata[0]:,.0f}<br>" +
                              "Renewal Rate: %{customdata[1]:.1%}<br>" +
                              "<extra></extra>"
            )
            
            fig.update_layout(
                height=500,
                margin=dict(l=0, r=0, t=10, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interactive insight below the chart
            st.info("👑 **Emperor Insight**: Click on any segment to zoom in and analyze detailed metrics. Double-click to zoom out. Right-click for additional controls.")
            
        with license_col2:
            # Animated border for emperor's control panel
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(30,58,138,0.05) 0%, rgba(75,0,130,0.1) 100%); 
                      padding: 15px; border-radius: 10px; border: 1px solid rgba(75,0,130,0.3);'>
                <h4 style='color: #4B0082; margin-top: 0;'>License Key Metrics</h4>
            """, unsafe_allow_html=True)
            
            # Animated license metrics with containers for potential real-time updates
            metric1 = st.empty()
            metric1.metric("Total Active Licenses", "327", "+3")
            
            metric2 = st.empty()
            metric2.metric("Revenue per License", "$3,791", "+2.1%")
            
            metric3 = st.empty()
            metric3.metric("License Renewal Rate", "94.7%", "+0.5%")
            
            metric4 = st.empty()
            metric4.metric("New Licenses (Month)", "12", "-2")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Emperor's control actions
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(75,0,130,0.8) 100%); 
                        padding: 15px; border-radius: 10px; margin-top: 15px; color: white;'>
                <h4 style='color: gold; margin-top: 0;'>👑 License Governance Controls</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Control buttons
            st.button("Generate License Report")
            st.button("Analyze Renewal Patterns")
            
            # Session history - would be functional in a real app
            st.markdown("""
            <div style='margin-top: 15px; padding: 10px; border-radius: 5px; border: 1px solid rgba(75,0,130,0.3); background-color: rgba(0,0,0,0.02);'>
                <p style='margin: 0; font-weight: bold; color: #4B0082;'>Recent Actions</p>
                <ul style='margin: 10px 0 0 0; padding-left: 20px; color: rgba(0,0,0,0.7);'>
                    <li>Modified Premium tier parameters</li>
                    <li>Approved 3 new Distribution licenses</li>
                    <li>Generated quarterly report</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional section for license performance over time
        st.subheader("License Performance Trends")
        
        # Generate time series data for license metrics
        dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
        license_counts = [300 + i * 0.5 + random.randint(-5, 5) for i in range(len(dates))]
        revenues = [1200000 + i * 1000 + random.randint(-10000, 10000) for i in range(len(dates))]
        
        # Create time series dataframe
        ts_data = pd.DataFrame({
            'Date': dates,
            'Licenses': license_counts,
            'Revenue': revenues
        })
        
        # Create interactive line chart
        ts_fig = go.Figure()
        
        # Add license count line
        ts_fig.add_trace(go.Scatter(
            x=ts_data['Date'],
            y=ts_data['Licenses'],
            name='Active Licenses',
            line=dict(color='#4B0082', width=2),
            hovertemplate='Date: %{x}<br>Licenses: %{y:.0f}<extra></extra>'
        ))
        
        # Add revenue line on secondary y-axis
        ts_fig.add_trace(go.Scatter(
            x=ts_data['Date'],
            y=ts_data['Revenue'],
            name='Revenue',
            line=dict(color='gold', width=2, dash='dot'),
            yaxis='y2',
            hovertemplate='Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        
        # Configure dual y-axes
        ts_fig.update_layout(
            xaxis=dict(title='Date'),
            yaxis=dict(
                title='Active Licenses',
                titlefont=dict(color='#4B0082'),
                tickfont=dict(color='#4B0082')
            ),
            yaxis2=dict(
                title='Revenue ($)',
                titlefont=dict(color='gold'),
                tickfont=dict(color='gold'),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            legend=dict(orientation='h', y=1.1),
            height=400,
            margin=dict(l=50, r=50, t=30, b=50),
            plot_bgcolor='rgba(0,0,0,0.02)'
        )
        
        st.plotly_chart(ts_fig, use_container_width=True)
        
        # Add emperor controls for the time series data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Export Trend Data")
        with col2:
            st.button("Calculate Projections")
        with col3:
            st.button("Set Performance Targets")
            
            # License health scorecard
            st.subheader("License Health")
            
            # Create a health score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=92,
                title={"text": "Overall License Health Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 60], "color": "red"},
                        {"range": [60, 80], "color": "orange"},
                        {"range": [80, 100], "color": "lightgreen"}
                    ]
                }
            ))
            
            fig.update_layout(
                height=250,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # License trends over time
        st.subheader("License Trends")
        
        # Generate time series data for license trends
        dates = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
        
        license_trend_data = pd.DataFrame({
            'Date': dates,
            'Manufacturing': np.random.randint(50, 100, size=12) + np.linspace(0, 20, 12),
            'Distribution': np.random.randint(40, 90, size=12) + np.linspace(0, 30, 12),
            'Financial': np.random.randint(10, 30, size=12) + np.linspace(0, 5, 12),
            'Marketing': np.random.randint(20, 50, size=12) + np.linspace(0, 15, 12),
            'Supply Chain': np.random.randint(30, 70, size=12) + np.linspace(0, 25, 12)
        })
        
        # Melt the dataframe for easier plotting
        license_trend_melted = pd.melt(
            license_trend_data, 
            id_vars=['Date'], 
            value_vars=['Manufacturing', 'Distribution', 'Financial', 'Marketing', 'Supply Chain'],
            var_name='License Type', 
            value_name='Count'
        )
        
        # Create the animated line chart
        fig = px.line(
            license_trend_melted,
            x='Date',
            y='Count',
            color='License Type',
            title="License Growth by Type (12-Month Trend)",
            labels={"Count": "Active Licenses", "Date": ""}
        )
        
        # Customize the layout
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Add animation
        fig.update_traces(mode="lines+markers")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # License geographical distribution
        st.subheader("License Geographical Distribution")
        
        # Sample geographical data
        regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
        license_counts = [120, 95, 72, 25, 15]
        
        # Create pie chart for geographical distribution
        fig = px.pie(
            values=license_counts,
            names=regions,
            title="License Distribution by Region",
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            hole=0.4
        )
        
        # Add animation
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Analytics Hub
    with tabs[2]:
        st.header("Empire OS Analytics Hub")
        st.write("Advanced analytics for the Empire OS ecosystem with interactive visualizations.")
        
        # Create analytics selector
        analysis_type = st.selectbox(
            "Select Analysis Category",
            ["Revenue Analysis", "User Engagement", "System Performance", "Governance", "Security"]
        )
        
        # Display selected analysis
        if analysis_type == "Revenue Analysis":
            st.subheader("Revenue Metrics and Projections")
            
            # Revenue overview
            rev_col1, rev_col2, rev_col3 = st.columns(3)
            
            with rev_col1:
                st.metric("Monthly Revenue", "$1.24M", "+2.8%")
            
            with rev_col2:
                st.metric("Annual Projection", "$14.88M", "+3.2%")
            
            with rev_col3:
                st.metric("Revenue per License", "$3,791", "+2.1%")
            
            # Revenue breakdown
            st.subheader("Revenue Breakdown by License Category")
            
            # Generate revenue data
            revenue_data = {
                "Category": ["Manufacturing", "Distribution", "Financial", "Marketing", "Supply Chain"],
                "Revenue": [480000, 360000, 120000, 140000, 140000],
                "Growth": [2.8, 3.2, 1.1, 4.5, 2.2]
            }
            
            df_revenue = pd.DataFrame(revenue_data)
            
            # Create animated bar chart
            fig = px.bar(
                df_revenue,
                x="Category",
                y="Revenue",
                color="Growth",
                color_continuous_scale="Viridis",
                text=df_revenue["Revenue"].apply(lambda x: f"${x/1000:.0f}K"),
                title="Monthly Revenue by License Category"
            )
            
            fig.update_layout(height=400)
            fig.update_traces(textposition="outside")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Revenue trend
            st.subheader("Revenue Trend (12-Month Historical)")
            
            # Generate time series data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
            base_revenue = 1000000  # $1M base
            
            # Create growth pattern with some randomness
            revenue_values = [
                base_revenue * (1 + 0.01 * i + 0.005 * np.random.randn()) 
                for i in range(12)
            ]
            
            revenue_trend = pd.DataFrame({
                "Date": dates,
                "Revenue": revenue_values
            })
            
            # Create area chart
            fig = px.area(
                revenue_trend,
                x="Date",
                y="Revenue",
                title="Monthly Revenue Trend",
                labels={"Revenue": "Revenue ($)"},
                color_discrete_sequence=["gold"]
            )
            
            # Format y-axis as currency
            fig.update_layout(
                height=400,
                yaxis=dict(tickprefix="$", ticksuffix="M", tickformat=".2f")
            )
            
            # Divide values by 1M for cleaner display
            fig.update_yaxes(tickvals=fig.layout.yaxis.tickvals, 
                             ticktext=[f"{val/1000000:.2f}" for val in fig.layout.yaxis.tickvals])
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "User Engagement":
            st.subheader("User Engagement Analytics")
            
            # Engagement metrics
            eng_col1, eng_col2, eng_col3 = st.columns(3)
            
            with eng_col1:
                st.metric("Daily Active Users", "412", "+15")
            
            with eng_col2:
                st.metric("Avg. Session Duration", "38 min", "+2 min")
            
            with eng_col3:
                st.metric("Feature Utilization", "76%", "+1.5%")
            
            # User engagement by module
            st.subheader("Engagement by Module")
            
            # Generate engagement data
            module_data = {
                "Module": ["License Manager", "Governance Console", "Analytics Dashboard", 
                           "API Gateway", "Security Center", "Data Explorer"],
                "Users": [320, 280, 350, 150, 210, 190],
                "Avg Time (min)": [42, 35, 48, 22, 28, 31]
            }
            
            df_modules = pd.DataFrame(module_data)
            
            # Create bubble chart for engagement
            fig = px.scatter(
                df_modules,
                x="Users",
                y="Avg Time (min)",
                size="Users",
                color="Module",
                text="Module",
                title="Module Engagement Analysis",
                size_max=60
            )
            
            fig.update_traces(textposition="top center")
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # User activity heatmap
            st.subheader("User Activity Patterns")
            
            # Generate hourly activity data
            hours = list(range(24))
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            # Create a base pattern with peak hours
            base_pattern = [1, 1, 1, 1, 1, 2, 5, 8, 10, 12, 12, 11, 13, 14, 12, 11, 10, 8, 6, 5, 4, 3, 2, 1]
            
            # Apply variations for different days
            activity_data = []
            for day in days:
                # Weekend pattern is different
                if day in ["Saturday", "Sunday"]:
                    day_pattern = [val * 0.5 + np.random.randint(0, 3) for val in base_pattern]
                else:
                    day_pattern = [val + np.random.randint(0, 3) for val in base_pattern]
                
                for hour, value in enumerate(day_pattern):
                    activity_data.append({
                        "Day": day,
                        "Hour": hour,
                        "Activity": value
                    })
            
            df_activity = pd.DataFrame(activity_data)
            
            # Create heatmap
            fig = px.density_heatmap(
                df_activity,
                x="Hour",
                y="Day",
                z="Activity",
                title="User Activity Heatmap (24-hour cycle)",
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(height=400)
            fig.update_xaxes(tickmode='array', tickvals=list(range(0, 24, 2)))
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "System Performance":
            st.subheader("System Performance Analytics")
            
            # System performance metrics
            perf_col1, perf_col2, perf_col3 = st.columns(3)
            
            with perf_col1:
                st.metric("System Uptime", "99.98%", "+0.03%")
            
            with perf_col2:
                st.metric("Avg. Response Time", "47ms", "-3ms")
            
            with perf_col3:
                st.metric("Error Rate", "0.02%", "-0.01%")
            
            # Performance trend
            st.subheader("System Performance Trend")
            
            # Generate time series data with multiple metrics
            hours = 24
            timestamps = pd.date_range(end=pd.Timestamp.now(), periods=hours, freq='H')
            
            # Create base patterns with some randomness
            cpu_usage = [30 + 15 * np.sin(i/4) + np.random.randint(-5, 5) for i in range(hours)]
            memory_usage = [45 + 10 * np.sin(i/6 + 1) + np.random.randint(-3, 3) for i in range(hours)]
            response_time = [50 + 10 * np.sin(i/5 + 2) + np.random.randint(-8, 8) for i in range(hours)]
            
            perf_data = pd.DataFrame({
                "Timestamp": timestamps,
                "CPU Usage (%)": cpu_usage,
                "Memory Usage (%)": memory_usage,
                "Response Time (ms)": response_time
            })
            
            # Create performance dashboard with multiple metrics
            perf_metrics = st.multiselect(
                "Select Performance Metrics",
                ["CPU Usage (%)", "Memory Usage (%)", "Response Time (ms)"],
                default=["CPU Usage (%)", "Response Time (ms)"]
            )
            
            if perf_metrics:
                # Create multi-line chart
                fig = px.line(
                    perf_data,
                    x="Timestamp",
                    y=perf_metrics,
                    title="Performance Metrics (24-hour trend)",
                    labels={"value": "Value", "variable": "Metric"}
                )
                
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one performance metric to display")
            
            # System resource allocation
            st.subheader("Resource Allocation by Component")
            
            # Generate resource allocation data
            components = ["Core Kernel", "Governance Engine", "License Manager", 
                          "API Gateway", "Security Framework", "Data Store", "Analytics Engine"]
            
            resource_data = {
                "Component": components,
                "CPU (%)": [25, 15, 10, 20, 12, 8, 10],
                "Memory (GB)": [16, 8, 6, 12, 8, 24, 16],
                "Storage (TB)": [0.5, 0.3, 0.2, 0.4, 0.3, 8.0, 2.0]
            }
            
            df_resources = pd.DataFrame(resource_data)
            
            # Create resource visualization
            resource_type = st.radio(
                "Resource Type",
                ["CPU (%)", "Memory (GB)", "Storage (TB)"],
                horizontal=True
            )
            
            # Create animated bar chart for selected resource
            fig = px.bar(
                df_resources,
                x="Component",
                y=resource_type,
                color="Component",
                title=f"{resource_type} Allocation by Component",
                text=df_resources[resource_type]
            )
            
            fig.update_traces(textposition="outside")
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Governance":
            st.subheader("Governance Analytics")
            
            # Governance metrics
            gov_col1, gov_col2, gov_col3 = st.columns(3)
            
            with gov_col1:
                st.metric("Compliance Score", "94.7%", "+0.5%")
            
            with gov_col2:
                st.metric("Policy Violations", "7", "-2")
            
            with gov_col3:
                st.metric("Audit Coverage", "98.2%", "+1.1%")
            
            # Compliance by department
            st.subheader("Compliance by Department")
            
            # Generate department compliance data
            dept_data = {
                "Department": ["Manufacturing", "Distribution", "Financial", "Technology", "Marketing", "Supply Chain"],
                "Compliance Score": [97, 91, 99, 96, 89, 92],
                "Critical Policies": [15, 12, 18, 14, 10, 13],
                "Violations": [0, 2, 0, 1, 3, 1]
            }
            
            df_compliance = pd.DataFrame(dept_data)
            
            # Create animated horizontal bar chart
            fig = px.bar(
                df_compliance,
                y="Department",
                x="Compliance Score",
                orientation='h',
                color="Compliance Score",
                color_continuous_scale="RdYlGn",
                text=df_compliance["Compliance Score"].apply(lambda x: f"{x}%"),
                title="Department Compliance Scores"
            )
            
            fig.update_traces(textposition="outside")
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Policy violations breakdown
            st.subheader("Policy Violations Analysis")
            
            # Generate policy violation data
            violation_data = {
                "Policy Category": ["Data Access", "User Permissions", "API Usage", 
                                   "License Terms", "Reporting", "Data Retention"],
                "Violations": [2, 1, 0, 3, 1, 0],
                "Severity": ["High", "Critical", "Low", "Medium", "Low", "Medium"]
            }
            
            df_violations = pd.DataFrame(violation_data)
            
            # Create custom severity order
            severity_order = ["Low", "Medium", "High", "Critical"]
            df_violations["Severity_Coded"] = df_violations["Severity"].apply(lambda x: severity_order.index(x))
            
            # Create sunburst chart for violations
            fig = px.sunburst(
                df_violations,
                path=["Severity", "Policy Category"],
                values="Violations",
                color="Severity_Coded",
                color_continuous_scale="YlOrRd",
                title="Policy Violations by Category and Severity"
            )
            
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Security":
            st.subheader("Security Analytics")
            
            # Security metrics
            sec_col1, sec_col2, sec_col3 = st.columns(3)
            
            with sec_col1:
                st.metric("Security Score", "96.3%", "+0.8%")
            
            with sec_col2:
                st.metric("Threat Incidents", "2", "-1")
            
            with sec_col3:
                st.metric("Avg Resolution Time", "42 min", "-8 min")
            
            # Security threat map
            st.subheader("Global Threat Intelligence Map")
            
            # Create placeholder for security map visualization
            st.markdown("""
            <div style='background-color: rgba(0,0,0,0.05); border-radius: 10px; height: 400px; 
                        display: flex; justify-content: center; align-items: center; 
                        text-align: center; padding: 20px;'>
                <p style='color: gray;'>Interactive threat intelligence map visualization would be displayed here, 
                showing global attack patterns and security incidents in real-time.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Security incident trends
            st.subheader("Security Incident Trends")
            
            # Generate time series data for security incidents
            dates = pd.date_range(end=pd.Timestamp.now(), periods=14, freq='D')
            
            # Create reasonable incident patterns
            incidents = [int(np.random.poisson(3) * np.random.choice([0, 1], p=[0.6, 0.4])) for _ in range(14)]
            total_incidents = sum(incidents)
            
            # Create incident types based on total
            incident_types = {
                "Authentication Failure": int(total_incidents * 0.4),
                "Suspicious Access": int(total_incidents * 0.3),
                "Data Access Violation": int(total_incidents * 0.2),
                "API Abuse": total_incidents - int(total_incidents * 0.4) - int(total_incidents * 0.3) - int(total_incidents * 0.2)
            }
            
            security_data = pd.DataFrame({
                "Date": dates,
                "Incidents": incidents
            })
            
            # Create line chart for incidents
            fig = px.line(
                security_data,
                x="Date",
                y="Incidents",
                title="Daily Security Incidents (14-day trend)",
                markers=True
            )
            
            fig.update_layout(height=350)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Incident type breakdown
            st.subheader("Security Incident Breakdown")
            
            # Create pie chart for incident types
            fig = px.pie(
                values=list(incident_types.values()),
                names=list(incident_types.keys()),
                title="Security Incidents by Type",
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Control Center
    with tabs[3]:
        st.header("Emperor's Control Center")
        st.write("Direct control interfaces for the Empire OS core functions.")
        
        # Create control panels
        control_col1, control_col2 = st.columns([1, 2])
        
        with control_col1:
            st.subheader("System Controls")
            
            # System control buttons
            st.button("✅ Start All Services", use_container_width=True)
            st.button("⚠️ Maintenance Mode", use_container_width=True)
            st.button("🔄 Restart Services", use_container_width=True)
            st.button("🔒 Lock System", use_container_width=True)
            
            # System status indicator
            st.markdown("""
            <div style='background-color: rgba(0,128,0,0.1); padding: 15px; border-radius: 5px; 
                      border-left: 5px solid green; margin-top: 20px;'>
                <p style='margin: 0;'><b>System Status:</b> Fully Operational</p>
                <p style='margin: 5px 0 0 0; font-size: 0.8em;'>Last updated: Just now</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions
            st.subheader("Quick Actions")
            
            quick_action = st.selectbox(
                "Select Action",
                ["Issue New License", "Revoke License", "Update Governance Policy", 
                 "Generate System Report", "View Audit Logs", "Run Security Scan"]
            )
            
            st.button("Execute Action", type="primary", use_container_width=True)
            
        with control_col2:
            st.subheader("Empire OS Command Terminal")
            
            # Create a mock terminal interface
            terminal_input = st.text_input("Enter command:", 
                                          value="show --status",
                                          placeholder="Type your command here...")
            
            # Mock terminal output based on input
            terminal_output = """
            > show --status
            
            Empire OS v3.7.2 (Imperial Edition)
            Status: ONLINE
            Uptime: 124 days, 7 hours, 12 minutes
            
            Core Services:
              ✅ Core Kernel (v3.7.2) - Running
              ✅ Governance Engine (v3.5.1) - Running
              ✅ License Manager (v3.6.0) - Running
              ✅ API Gateway (v3.7.0) - Running
              ✅ Security Framework (v3.7.2) - Running
              ✅ Data Store (v3.6.1) - Running
              ✅ Analytics Engine (v3.5.2) - Running
            
            Resources:
              CPU: 32% utilization
              Memory: 47% utilization
              Storage: 36% utilization
              
            Active Sessions: 42
            Active Licenses: 327
            
            No critical alerts detected.
            """
            
            # Display terminal with styling
            st.markdown("""
            <div style='background-color: #1E1E1E; color: #FFFFFF; font-family: monospace; 
                      padding: 15px; border-radius: 5px; height: 300px; overflow-y: auto;'>
                <pre style='color: #FFFFFF; margin: 0;'>{}</pre>
            </div>
            """.format(terminal_output), unsafe_allow_html=True)
            
            # Command history
            st.markdown("""
            <div style='margin-top: 10px;'>
                <p style='margin: 0; font-size: 0.8em; color: gray;'>Recent commands:</p>
                <p style='margin: 0; font-size: 0.8em; font-family: monospace;'>
                show --licenses<br>
                update --policy governance_policy_17<br>
                refresh --cache<br>
                stats --performance --last=12h
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # System-wide controls
        st.subheader("System-wide Controls")
        
        # Create tabs for different control categories
        control_tabs = st.tabs([
            "License Control", 
            "User Management", 
            "Governance Policies",
            "System Configuration"
        ])
        
        # Tab 1: License Control
        with control_tabs[0]:
            # License control interface
            st.subheader("License Master Control")
            
            license_control_cols = st.columns(3)
            
            with license_control_cols[0]:
                st.number_input("License Quota Limit", min_value=0, max_value=1000, value=500)
                
            with license_control_cols[1]:
                st.selectbox("Default License Term", ["1 Month", "3 Months", "6 Months", "1 Year", "Perpetual"])
                
            with license_control_cols[2]:
                st.selectbox("License Approval Mode", ["Auto-approve", "Emperor approval required", "Multi-sign required"])
            
            # License policy controls
            st.markdown("#### License Policy Settings")
            
            policy_cols = st.columns(2)
            
            with policy_cols[0]:
                st.checkbox("Enable automatic renewals", value=True)
                st.checkbox("Allow license transfers", value=False)
                st.checkbox("Enforce usage analytics", value=True)
                
            with policy_cols[1]:
                st.checkbox("Enable grace period", value=True)
                st.checkbox("Enforce security compliance", value=True)
                st.checkbox("Allow offline activation", value=False)
            
            # Big control buttons
            st.button("Save License Policy Settings", type="primary", use_container_width=True)
            
        # Tab 2: User Management
        with control_tabs[1]:
            # User management interface
            st.subheader("User Role Management")
            
            # Mock user data
            users = [
                {"name": "Emperor", "role": "Emperor", "status": "Active", "last_access": "Now"},
                {"name": "CFO", "role": "Licensed Admin", "status": "Active", "last_access": "5m ago"},
                {"name": "CIO", "role": "Licensed Admin", "status": "Away", "last_access": "1h ago"},
                {"name": "Marketing Director", "role": "Licensed User", "status": "Offline", "last_access": "3h ago"},
                {"name": "Manufacturing Lead", "role": "Licensed User", "status": "Active", "last_access": "30m ago"}
            ]
            
            # Create a dataframe for users
            df_users = pd.DataFrame(users)
            
            # Display users with styling
            st.dataframe(df_users, use_container_width=True, height=200)
            
            # User management controls
            user_control_cols = st.columns(3)
            
            with user_control_cols[0]:
                st.text_input("User Search", placeholder="Search by name...")
                
            with user_control_cols[1]:
                st.selectbox("Filter by Role", ["All Roles", "Emperor", "Licensed Admin", "Licensed User"])
                
            with user_control_cols[2]:
                st.selectbox("Filter by Status", ["All Status", "Active", "Away", "Offline"])
            
            # User action buttons
            action_cols = st.columns(4)
            
            with action_cols[0]:
                st.button("Add User", use_container_width=True)
            
            with action_cols[1]:
                st.button("Edit Selected", use_container_width=True)
            
            with action_cols[2]:
                st.button("Suspend User", use_container_width=True)
            
            with action_cols[3]:
                st.button("Delete User", use_container_width=True)
                
        # Tab 3: Governance Policies
        with control_tabs[2]:
            # Governance policy interface
            st.subheader("Governance Policy Management")
            
            # Mock policy data
            policies = [
                {"id": "GOV-001", "name": "Data Access Control", "status": "Active", "compliance": "98%"},
                {"id": "GOV-002", "name": "User Authentication", "status": "Active", "compliance": "100%"},
                {"id": "GOV-003", "name": "License Compliance", "status": "Active", "compliance": "95%"},
                {"id": "GOV-004", "name": "API Usage Limits", "status": "Active", "compliance": "92%"},
                {"id": "GOV-005", "name": "Data Retention", "status": "Pending Review", "compliance": "87%"}
            ]
            
            # Create a dataframe for policies
            df_policies = pd.DataFrame(policies)
            
            # Display policies with styling
            st.dataframe(df_policies, use_container_width=True, height=200)
            
            # Policy management controls
            policy_edit_cols = st.columns(2)
            
            with policy_edit_cols[0]:
                st.text_area("Policy Description", 
                             "This governance policy controls data access permissions across the Empire OS ecosystem. " + 
                             "It enforces security compliance and ensures proper data protection.",
                             height=100)
                
            with policy_edit_cols[1]:
                st.selectbox("Policy Status", ["Active", "Pending Review", "Inactive", "Archived"])
                st.selectbox("Enforcement", ["Strict", "Advisory", "Report Only"])
            
            # Policy action buttons
            policy_action_cols = st.columns(4)
            
            with policy_action_cols[0]:
                st.button("Create Policy", use_container_width=True)
            
            with policy_action_cols[1]:
                st.button("Save Changes", use_container_width=True)
            
            with policy_action_cols[2]:
                st.button("Publish Policy", use_container_width=True)
            
            with policy_action_cols[3]:
                st.button("Archive Policy", use_container_width=True)
                
        # Tab 4: System Configuration
        with control_tabs[3]:
            # System configuration interface
            st.subheader("System Configuration")
            
            # Configuration categories
            config_category = st.selectbox(
                "Configuration Category",
                ["Performance Settings", "Security Configuration", "Integration Settings", "Backup & Recovery"]
            )
            
            if config_category == "Performance Settings":
                # Performance settings
                perf_cols = st.columns(2)
                
                with perf_cols[0]:
                    st.slider("CPU Resource Allocation", 0, 100, 60, "%")
                    st.slider("Memory Resource Allocation", 0, 100, 70, "%")
                    st.number_input("Max Concurrent Users", min_value=50, max_value=1000, value=500)
                    
                with perf_cols[1]:
                    st.slider("API Rate Limit", 100, 10000, 5000, 100)
                    st.slider("Query Complexity Limit", 1, 100, 50)
                    st.number_input("Cache Timeout (minutes)", min_value=1, max_value=120, value=30)
                    
            elif config_category == "Security Configuration":
                # Security configurations
                security_cols = st.columns(2)
                
                with security_cols[0]:
                    st.selectbox("Authentication Mode", ["Multi-factor", "Biometric", "Single-factor", "OAuth"])
                    st.number_input("Session Timeout (minutes)", min_value=5, max_value=240, value=60)
                    st.selectbox("Encryption Level", ["Imperial-grade (512-bit)", "Military-grade (256-bit)", "Standard (128-bit)"])
                    
                with security_cols[1]:
                    st.checkbox("Enable Intrusion Detection", value=True)
                    st.checkbox("Automatic Security Updates", value=True)
                    st.checkbox("Enforce Password Rotation", value=True)
                    st.checkbox("Allow Remote Access", value=False)
                    
            elif config_category == "Integration Settings":
                # Integration settings
                integration_cols = st.columns(2)
                
                with integration_cols[0]:
                    st.multiselect("Enabled API Endpoints", ["REST API", "GraphQL", "SOAP", "WebSocket", "gRPC"], 
                                   default=["REST API", "GraphQL", "WebSocket"])
                    st.text_input("API Base URL", value="https://api.empires.vsr/v1")
                    
                with integration_cols[1]:
                    st.checkbox("Enable External Integrations", value=True)
                    st.multiselect("Approved Integration Partners", ["SAP", "Oracle", "IBM", "Microsoft", "Salesforce"],
                                  default=["SAP", "Oracle", "Microsoft"])
                    
            elif config_category == "Backup & Recovery":
                # Backup settings
                backup_cols = st.columns(2)
                
                with backup_cols[0]:
                    st.selectbox("Backup Frequency", ["Hourly", "Daily", "Weekly", "Monthly"])
                    st.number_input("Retention Period (days)", min_value=1, max_value=365, value=90)
                    st.text_input("Backup Storage Location", value="Imperial Secure Vault")
                    
                with backup_cols[1]:
                    st.checkbox("Enable Automated Backups", value=True)
                    st.checkbox("Encrypt Backup Data", value=True)
                    st.selectbox("Recovery Mode", ["Automatic", "Manual Approval Required", "Emperor Approval Only"])
            
            # Apply configuration button
            st.button("Apply Configuration Changes", type="primary", use_container_width=True)

# Special visualization for the Emperor's view of license functioning
def show_license_dashboard():
    """
    Display a dedicated dashboard for monitoring license functioning.
    This is part of the Emperor's view and shows detailed license analytics.
    """
    st.header("License Performance Dashboard")
    st.write("Comprehensive analytics on license allocation, usage, and performance metrics.")
    
    # License KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Licenses", "327", "+3")
    
    with col2:
        st.metric("Active Usage", "92%", "+2%")
    
    with col3:
        st.metric("Revenue", "$1.24M", "+2.8%")
    
    with col4:
        st.metric("Compliance", "98.7%", "+0.5%")
    
    # License distribution chart
    st.subheader("License Distribution by Type")
    
    # Generate license data
    license_types = ["Manufacturing", "Retail", "Financial", "Marketing", "Supply Chain"]
    license_counts = [120, 95, 42, 35, 35]
    license_growth = ["+2.1%", "+3.4%", "+0.5%", "+4.2%", "+1.8%"]
    
    # Create a DataFrame
    df_licenses = pd.DataFrame({
        "Type": license_types,
        "Count": license_counts,
        "Growth": license_growth
    })
    
    # Create a bar chart
    fig = px.bar(
        df_licenses,
        x="Type",
        y="Count",
        color="Type",
        text="Count",
        title="License Distribution by Type"
    )
    
    fig.update_traces(textposition="outside")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # License usage over time
    st.subheader("License Usage Trend")
    
    # Generate time series data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    usage_data = np.random.normal(90, 5, 30)  # Mean around 90% with some variance
    
    # Create a time series DataFrame
    df_usage = pd.DataFrame({
        "Date": dates,
        "Usage %": usage_data
    })
    
    # Create a line chart
    fig = px.line(
        df_usage,
        x="Date",
        y="Usage %",
        title="License Usage Percentage (30-day trend)",
        labels={"Usage %": "Usage Percentage"},
        markers=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # License revenue analytics
    st.subheader("License Revenue Analytics")
    
    # Create columns for metrics and chart
    rev_col1, rev_col2 = st.columns([2, 1])
    
    with rev_col1:
        # Generate revenue data by license type
        revenue_data = {
            "Type": license_types,
            "Revenue": [480000, 380000, 168000, 105000, 105000]
        }
        
        df_revenue = pd.DataFrame(revenue_data)
        
        # Create a pie chart
        fig = px.pie(
            df_revenue,
            values="Revenue",
            names="Type",
            title="Revenue Distribution by License Type",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )
        
        fig.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with rev_col2:
        # Revenue metrics
        st.metric("Avg. Revenue per License", "$3,791", "+2.1%")
        st.metric("Top License Revenue", "Manufacturing", "$480K")
        st.metric("Growth Rate (Monthly)", "2.8%", "+0.3%")
        
        # License health score
        st.subheader("License Health")
        
        # Create a gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=92,
            title={"text": "License Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 60], "color": "red"},
                    {"range": [60, 80], "color": "orange"},
                    {"range": [80, 100], "color": "lightgreen"}
                ]
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)