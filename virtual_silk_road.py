import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px

def show_virtual_silk_road():
    """
    Display the Emperor's private view of the Virtual Silk Road ecosystem.
    This is a comprehensive visualization of the entire enterprise governance structure.
    Only accessible to authenticated users with Emperor-level access.
    """
    
    # Differentiate this from the public landing view with a special notice
    st.info("⚠️ This is the Emperor's private governance view with special access controls. For the public Virtual Silk Road landing page, navigate to the public view.")
    
    # Emperor's header with special styling for authorized users
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, rgba(30,58,138,1) 0%, rgba(75,0,130,1) 100%); 
        padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
            <h1 style='color: gold; margin: 0; font-size: 3rem;'>👑 Emperor's Command Center</h1>
            <p style='color: white; margin: 15px 0 0 0; font-size: 1.5rem;'>Virtual Silk Road Governance Terminal</p>
            <p style='color: rgba(255,255,255,0.7); margin: 10px 0 0 0;'>Authorized Access: Private View</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Emperor's dashboard tabs
    tabs = st.tabs([
        "🌐 Ecosystem Overview", 
        "🔬 License Management", 
        "📊 Governance Analytics",
        "📅 Review Calendar"
    ])
    
    # Tab 1: Ecosystem Overview
    with tabs[0]:
        st.header("Enterprise Ecosystem Digital Twin")
        st.write("Complete visualization of the interconnected components in the Empire OS governance model.")
        
        # Simulate complex interactive visualization
        eco_col1, eco_col2 = st.columns([2, 1])
        
        with eco_col1:
            # Create network visualization
            nodes = {'Manufacturing': 0, 'Retail': 1, 'Finance': 2, 'Logistics': 3, 
                    'Marketing': 4, 'Compliance': 5, 'Emperor': 6, 'Software': 7}
            
            # Create connections (edges) between nodes
            edges = []
            for i in range(len(nodes)-1):
                # Emperor node connects to all other nodes
                edges.append((nodes['Emperor'], i))
                
                # Other connections
                if i < len(nodes)-2:
                    edges.append((i, i+1))
            
            # Create labels and positions for nodes
            labels = list(nodes.keys())
            pos = {}
            
            # Place Emperor node in center
            pos[nodes['Emperor']] = [0, 0]
            
            # Place other nodes in a circle around Emperor
            angle_step = 2 * np.pi / (len(nodes) - 1)
            for i, node in enumerate([n for n in nodes.keys() if n != 'Emperor']):
                angle = i * angle_step
                pos[nodes[node]] = [0.5 * np.cos(angle), 0.5 * np.sin(angle)]
            
            # Create a graph using plotly
            edge_x = []
            edge_y = []
            for edge in edges:
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1, color='rgba(150, 150, 150, 0.7)'),
                hoverinfo='none',
                mode='lines')
            
            node_x = []
            node_y = []
            node_color = []
            node_size = []
            
            for node in nodes:
                x, y = pos[nodes[node]]
                node_x.append(x)
                node_y.append(y)
                # Emperor node is gold
                if node == 'Emperor':
                    node_color.append('gold')
                    node_size.append(25)
                else:
                    node_color.append('steelblue')
                    node_size.append(15)
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=labels,
                textposition="top center",
                marker=dict(
                    showscale=False,
                    color=node_color,
                    size=node_size,
                    line=dict(width=1, color='rgba(50, 50, 50, 0.8)')),
                hoverinfo='text',
                textfont=dict(size=11))
            
            # Create the figure
            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title="Empire OS Ecosystem Visualization",
                                titlefont=dict(size=16),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20, l=5, r=5, t=40),
                                annotations=[dict(
                                    text="",
                                    showarrow=False,
                                    xref="paper", yref="paper")],
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                height=500,
                                plot_bgcolor='rgba(255, 255, 255, 0.95)')
                            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with eco_col2:
            st.subheader("System Status")
            
            # System status metrics
            st.metric("Active Licenses", "324", "+12")
            st.metric("API Requests (24h)", "1.2M", "-3%")
            st.metric("System Health", "98.7%", "+0.5%")
            
            # Active administrators
            st.subheader("Active Administrators")
            admins = {
                "Emperor": {"status": "Online", "last_active": "Now", "color": "gold"},
                "CFO": {"status": "Online", "last_active": "5m ago", "color": "green"},
                "CIO": {"status": "Away", "last_active": "1h ago", "color": "orange"},
                "Marketing Officer": {"status": "Offline", "last_active": "3h ago", "color": "red"}
            }
            
            # Display admin status with colored indicators
            for admin, data in admins.items():
                st.markdown(f"""
                <div style='display: flex; align-items: center;'>
                    <div style='width: 10px; height: 10px; border-radius: 50%; background-color: {data["color"]}; margin-right: 10px;'></div>
                    <div style='flex-grow: 1;'><b>{admin}</b> <span style='color: gray; font-size: 0.8em;'>({data["status"]})</span></div>
                    <div style='color: gray; font-size: 0.8em;'>{data["last_active"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Additional ecosystem metrics
        st.subheader("Key Ecosystem Metrics")
        
        # Create three columns for metrics
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            st.markdown("""
            <div style='background-color: rgba(30, 58, 138, 0.1); padding: 15px; border-radius: 5px; text-align: center;'>
                <h3 style='margin-top: 0; color: #1E3A8A;'>$1.2M</h3>
                <p style='margin-bottom: 0;'>Revenue from License Fees</p>
            </div>
            """, unsafe_allow_html=True)
            
        with metric_cols[1]:
            st.markdown("""
            <div style='background-color: rgba(75, 0, 130, 0.1); padding: 15px; border-radius: 5px; text-align: center;'>
                <h3 style='margin-top: 0; color: #4B0082;'>27</h3>
                <p style='margin-bottom: 0;'>Connected External Systems</p>
            </div>
            """, unsafe_allow_html=True)
            
        with metric_cols[2]:
            st.markdown("""
            <div style='background-color: rgba(0, 100, 0, 0.1); padding: 15px; border-radius: 5px; text-align: center;'>
                <h3 style='margin-top: 0; color: #006400;'>98.3%</h3>
                <p style='margin-bottom: 0;'>Governance Compliance Rate</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 2: License Management
    with tabs[1]:
        st.header("License Management Console")
        st.write("Emperor-level control over all license allocations, permissions, and restrictions.")
        
        # License management interface
        license_types = [
            "Manufacturing Access License", 
            "Retail Distribution License",
            "Empire OS Core License",
            "Financial Oversight License",
            "Marketing Portal License",
            "Supply Chain Visualization License"
        ]
        
        # License status table
        license_data = {
            "License Type": license_types,
            "Active Instances": [42, 156, 3, 18, 24, 81],
            "Usage %": [78, 92, 100, 45, 63, 87],
            "Monthly Cost": ["$4,200", "$15,600", "$30,000", "$1,800", "$2,400", "$8,100"],
            "Status": ["✅ Active", "✅ Active", "✅ Active", "⚠️ Underutilized", "✅ Active", "✅ Active"]
        }
        
        df_licenses = pd.DataFrame(license_data)
        
        # Style the dataframe
        st.dataframe(df_licenses, use_container_width=True)
        
        # License allocation tools
        st.subheader("License Allocation Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # License allocation form
            selected_license = st.selectbox("Select License Type", license_types)
            entity_name = st.text_input("Entity Name")
            duration = st.radio("License Duration", ["1 Month", "6 Months", "1 Year", "Perpetual"])
            permissions = st.multiselect("Permissions", ["View", "Edit", "Delete", "Admin", "API Access"])
            
        with col2:
            # Cost calculator
            st.subheader("Cost Calculator")
            
            # Map selection to a base price
            base_prices = {
                "Manufacturing Access License": 100,
                "Retail Distribution License": 100,
                "Empire OS Core License": 10000,
                "Financial Oversight License": 100,
                "Marketing Portal License": 100,
                "Supply Chain Visualization License": 100
            }
            
            # Map duration to a multiplier
            duration_multipliers = {
                "1 Month": 1,
                "6 Months": 5.5,
                "1 Year": 10,
                "Perpetual": 30
            }
            
            # Calculate cost based on license type, duration, and permissions
            base_price = base_prices.get(selected_license, 100)
            duration_multiplier = duration_multipliers.get(duration, 1)
            permission_cost = len(permissions) * 20  # $20 per permission
            
            total_cost = base_price * duration_multiplier + permission_cost
            
            # Display calculation
            st.metric("License Cost", f"${total_cost:,.2f}")
            
            # Issue button
            if st.button("Issue License", type="primary"):
                st.success(f"License for {entity_name} has been issued successfully!")
                
        # License activation history
        st.subheader("Recent License Activations")
        
        # Sample activation data
        activation_data = {
            "Entity": ["VOI Jeans Factory #3", "Retail Store #42", "Finance Department", "Marketing Team Alpha"],
            "License Type": ["Manufacturing Access", "Retail Distribution", "Financial Oversight", "Marketing Portal"],
            "Activated On": ["2025-03-30", "2025-03-28", "2025-03-25", "2025-03-22"],
            "Activated By": ["Emperor", "CIO", "CFO", "Marketing Officer"]
        }
        
        df_activations = pd.DataFrame(activation_data)
        st.table(df_activations)
    
    # Tab 3: Governance Analytics
    with tabs[2]:
        st.header("Governance Analytics")
        st.write("Comprehensive analytics on governance metrics across the Empire OS ecosystem.")
        
        # Time-based filter for analytics
        time_range = st.radio("Time Range", ["Last 7 Days", "Last 30 Days", "Last Quarter", "Last Year"], horizontal=True)
        
        # Create analytics dashboard
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Compliance rate by department
            st.subheader("Compliance Rate by Department")
            
            dept_data = {
                "Department": ["Manufacturing", "Retail", "Finance", "Logistics", "Marketing", "Technology"],
                "Compliance Rate": [97, 94, 99, 92, 88, 96]
            }
            
            fig = px.bar(
                dept_data, 
                x="Department", 
                y="Compliance Rate",
                title="Department Compliance (%)",
                color="Compliance Rate",
                color_continuous_scale=px.colors.sequential.Viridis,
                text="Compliance Rate"
            )
            
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            
            st.plotly_chart(fig, use_container_width=True)
            
        with chart_col2:
            # API usage over time
            st.subheader("API Usage Trends")
            
            # Generate some sample data
            dates = pd.date_range(end=pd.Timestamp.now(), periods=14, freq='D')
            api_calls = np.random.randint(800, 1200, size=14) * 1000
            
            # Create a dataframe
            api_data = pd.DataFrame({
                'Date': dates,
                'API Calls': api_calls
            })
            
            fig = px.line(
                api_data, 
                x='Date', 
                y='API Calls', 
                title='Daily API Calls (14-day trend)',
                markers=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Second row of charts
        chart_col3, chart_col4 = st.columns(2)
        
        with chart_col3:
            # License usage by type
            st.subheader("License Utilization by Type")
            
            license_usage = {
                "License Type": ["Manufacturing", "Retail", "Financial", "Marketing", "Supply Chain"],
                "Allocated": [50, 200, 20, 30, 100],
                "Active": [42, 156, 18, 24, 81]
            }
            
            df_usage = pd.DataFrame(license_usage)
            df_usage["Utilization"] = (df_usage["Active"] / df_usage["Allocated"] * 100).round(1)
            
            fig = px.bar(
                df_usage,
                x="License Type",
                y=["Active", "Allocated"],
                title="License Allocation vs. Usage",
                barmode="overlay",
                opacity=0.7
            )
            
            # Add percentage labels
            for i, row in df_usage.iterrows():
                fig.add_annotation(
                    x=row["License Type"],
                    y=row["Active"],
                    text=f"{row['Utilization']}%",
                    showarrow=False,
                    yshift=10
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with chart_col4:
            # System health metrics
            st.subheader("System Health")
            
            # Create a gauge chart for system health
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = 98.7,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "System Health Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps' : [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 80], 'color': "orange"},
                        {'range': [80, 90], 'color': "yellow"},
                        {'range': [90, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 98.7
                    }
                }
            ))
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Compliance issues table
        st.subheader("Active Compliance Issues")
        
        # Sample compliance issues
        compliance_issues = {
            "Issue ID": ["GOV-2324", "GOV-2310", "GOV-2298"],
            "Department": ["Retail", "Marketing", "Manufacturing"],
            "Description": [
                "Missing quarterly retail inventory reconciliation",
                "Unapproved marketing assets in circulation",
                "Production process change without proper documentation"
            ],
            "Severity": ["Medium", "Low", "High"],
            "Status": ["In Review", "Assigned", "In Progress"],
            "Due Date": ["2025-04-10", "2025-04-15", "2025-04-05"]
        }
        
        df_issues = pd.DataFrame(compliance_issues)
        
        # Apply color coding for severity
        def color_severity(val):
            color_map = {"Low": "green", "Medium": "orange", "High": "red"}
            return f"background-color: {color_map.get(val, 'white')}; color: white;"
        
        # Display styled table
        st.dataframe(df_issues, use_container_width=True)
    
    # Tab 4: Review Calendar
    with tabs[3]:
        st.header("Governance Review Calendar")
        st.write("Schedule and tracking for governance reviews conducted by the Emperor and the council of ministers.")
        
        # Filter by month
        current_month = pd.Timestamp.now().strftime("%B %Y")
        selected_month = st.selectbox("Select Month", [current_month, "May 2025", "June 2025", "July 2025"])
        
        # Create schedule calendar
        st.subheader(f"Review Schedule: {selected_month}")
        
        # Sample review schedule
        review_data = {
            "Date": ["2025-04-05", "2025-04-12", "2025-04-19", "2025-04-26"],
            "Review Type": [
                "Manufacturing Governance",
                "Retail Distribution Compliance",
                "Financial Systems Review",
                "Full Council of Ministers Review"
            ],
            "Led By": ["Emperor & Manufacturing Minister", "Retail Minister", "CFO", "Emperor"],
            "Status": ["Scheduled", "Scheduled", "Scheduled", "Tentative"]
        }
        
        df_reviews = pd.DataFrame(review_data)
        
        # Display the schedule
        st.table(df_reviews)
        
        # Review process visualization
        st.subheader("Review Process Workflow")
        
        # Timeline data
        timeline_data = {
            "Step": [
                "Data Collection",
                "Preliminary Analysis",
                "Minister Review",
                "Emperor Review",
                "Action Items"
            ],
            "Duration (days)": [3, 2, 1, 1, 2],
            "Responsible": [
                "Department Heads",
                "Ministers & Advisors",
                "Council of Ministers",
                "Emperor",
                "All Stakeholders"
            ]
        }
        
        # Display review process
        st.table(timeline_data)
    
    # Marketing message and competitive positioning
    st.subheader("🌐 Market Democratization Strategy")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        ### Why Virtual Silk Road?
        
        - **Cost-effective Governance**
          *At a fraction of competing solutions*
          
        - **Unified Ecosystem View**
          *No more siloed information*
          
        - **Real-time Decision Making**
          *Immediate insights across operations*
          
        - **Complete API Integration**
          *Connect to any existing system*
          
        - **Modular License Structure**
          *Pay only for what you need*
        """)
    
    with col2:
        # Comparison table
        st.markdown("### Competitive Advantage")
        
        comparison_data = {
            'Feature': [
                'Unified Governance View',
                'Real-time Supply Chain Insights',
                'HSN Code Integration',
                'Emperor-level Oversight',
                'Marketing & Sales Portal',
                'Custom License Templates',
                'API-driven Architecture',
                'ROI Analytics'
            ],
            'Virtual Silk Road': [
                '✅ Included',
                '✅ Included',
                '✅ Included',
                '✅ Included',
                '✅ Included',
                '✅ Included',
                '✅ Included',
                '✅ Included'
            ],
            'Competitors': [
                '✅ $20,000+',
                '❌ Extra Module',
                '❌ Not Available',
                '❌ Limited Access',
                '❌ Separate System',
                '❌ Fixed Templates',
                '⚠️ Limited APIs',
                '⚠️ Basic Only'
            ]
        }
        
        # Create DataFrame
        df_comparison = pd.DataFrame(comparison_data)
        
        # Display comparison
        st.dataframe(df_comparison, hide_index=True)
        
        # Pricing advantage message
        st.markdown("""
        <div style="background-color: rgba(50, 205, 50, 0.1); padding: 10px; border-radius: 5px; border-left: 3px solid #32CD32; margin-top: 10px;">
            <b style="color: #32CD32;">💰 Price Advantage:</b> Our modular licensing approach provides enterprise-grade governance at 60-80% less than competing solutions.
        </div>
        """, unsafe_allow_html=True)

    # Marketing call-to-action
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(75,0,130,0.8) 0%, rgba(123,104,238,0.8) 100%); 
                padding: 25px; border-radius: 10px; margin-top: 20px; text-align: center; color: white;">
        <h2 style="color: white; margin-top: 0;">Ready to Transform Your Enterprise Governance?</h2>
        <p style="font-size: 1.2em; margin: 15px 0;">
            Contact our Marketing Officer to discover the perfect license package for your organization.
        </p>
        <div style="margin-top: 20px;">
            <span style="background-color: white; color: #4B0082; padding: 10px 20px; border-radius: 30px; font-weight: bold; display: inline-block;">
                Request Demo & Pricing ➔
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final Emperor's view message
    st.markdown("""
    <div style="background-color: rgba(70, 130, 180, 0.1); padding: 20px; border-radius: 5px; border-left: 5px solid steelblue; margin-top: 20px;">
        <h3 style="color: steelblue; margin-top: 0;">Emperor's Command Center</h3>
        <p>This visualization provides the Emperor with complete oversight of the entire ecosystem. 
        From here, the Emperor can monitor all activities, issue directives, and ensure the prosperity 
        of the empire through the Virtual Silk Road.</p>
        <p><b>For Marketing Teams:</b> Demonstrate this comprehensive view to showcase how your organization's 
        leadership can gain unprecedented visibility across all operations, enabling faster decision-making 
        and strategic advantage over competitors still using fragmented systems.</p>
    </div>
    """, unsafe_allow_html=True)