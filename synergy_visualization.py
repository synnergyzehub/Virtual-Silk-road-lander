import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from PIL import Image
import io
import base64
import datetime
from data_sharing import show_data_sharing

def show_synergy_visualization():
    """Display the Synergyze ecosystem visualization showcasing the relationships between modules"""
    st.title("🔄 Synergyze Ecosystem Visualization")
    
    # Check if user has a license to view Empire OS features
    if 'has_empire_license' not in st.session_state:
        st.session_state.has_empire_license = True  # Enable for demo purposes
    
    # Create tabs for different visualization views
    if st.session_state.has_empire_license:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Ecosystem Overview", 
            "🔗 Network Visualization", 
            "📑 License Management",
            "🔄 Data Sharing",
            "⚙️ Empire OS Governance"
        ])
    else:
        tab1, tab2, tab3 = st.tabs([
            "📊 Ecosystem Overview", 
            "🔗 Network Visualization", 
            "📑 License Management"
        ])
    
    with tab1:
        show_ecosystem_overview()
    
    with tab2:
        show_network_visualization()
    
    with tab3:
        show_license_management()
    
    if st.session_state.has_empire_license:
        with tab4:
            show_data_sharing()
            
        with tab5:
            show_empire_os_governance()

def show_ecosystem_overview():
    """Display the Synergyze ecosystem overview with its three main components"""
    
    st.subheader("Voi Jeans Empire OS Synergyze Platform")
    
    # Modern intro banner with stats
    st.markdown("""
    <div style="background: linear-gradient(to right, #1E3A8A, #4A5568); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: white; margin-top: 0;">Voi Jeans Retail India Pvt Ltd</h3>
        <p>Powered by Synergyze - A Premium Enterprise License Platform</p>
        <div style="display: flex; justify-content: space-between; margin-top: 15px; text-align: center;">
            <div>
                <h4 style="margin: 0; color: #90CDF4;">20+</h4>
                <p style="margin: 0; font-size: 0.8em;">Retail Stores</p>
            </div>
            <div>
                <h4 style="margin: 0; color: #90CDF4;">₹3.24 Cr</h4>
                <p style="margin: 0; font-size: 0.8em;">Monthly Sales</p>
            </div>
            <div>
                <h4 style="margin: 0; color: #90CDF4;">24,850+</h4>
                <p style="margin: 0; font-size: 0.8em;">Loyalty Members</p>
            </div>
            <div>
                <h4 style="margin: 0; color: #90CDF4;">SS25</h4>
                <p style="margin: 0; font-size: 0.8em;">Collection Active</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    The Synergyze platform integrates three powerful components, providing Voi Jeans with a seamless digital ecosystem:
    """)
    
    # Create a more visually appealing three-panel display
    eco_col1, eco_col2, eco_col3 = st.columns(3)
    
    with eco_col1:
        st.markdown("""
        <div style="background-color: #EBF4FF; border-left: 5px solid #3182CE; padding: 15px; border-radius: 5px;">
            <h3 style="color: #2C5282;">🏭 Woven Supply</h3>
            <p style="font-weight: bold; color: #4A5568;">Manufacturing Excellence</p>
            
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✓ Smart Material Procurement</li>
                <li>✓ Scotts Garments CMP Integration</li>
                <li>✓ SS25 Production Planning</li>
                <li>✓ Quality Assurance System</li>
                <li>✓ Factory Operations Dashboard</li>
                <li>✓ Real-time Material Tracking</li>
            </ul>
            
            <p><em>Premium manufacturing visibility from fabric to finished product</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with eco_col2:
        st.markdown("""
        <div style="background-color: #F0FFF4; border-left: 5px solid #38A169; padding: 15px; border-radius: 5px;">
            <h3 style="color: #276749;">🏬 Commune Connect</h3>
            <p style="font-weight: bold; color: #4A5568;">Retail Excellence</p>
            
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✓ 20-Store Network Management</li>
                <li>✓ Digital Product Catalog</li>
                <li>✓ Real-time Inventory Control</li>
                <li>✓ Daily Sales Tracking</li>
                <li>✓ E-Wards Loyalty Program</li>
                <li>✓ Integrated Consumer Analytics</li>
            </ul>
            
            <p><em>Sophisticated retail management with consumer insights</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with eco_col3:
        st.markdown("""
        <div style="background-color: #F3E8FF; border-left: 5px solid #805AD5; padding: 15px; border-radius: 5px;">
            <h3 style="color: #553C9A;">⚙️ Synergyze Hub</h3>
            <p style="font-weight: bold; color: #4A5568;">Strategic Governance</p>
            
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✓ Enterprise License Control</li>
                <li>✓ Department-based Access</li>
                <li>✓ Multi-channel Data Integration</li>
                <li>✓ Executive Analytics Dashboard</li>
                <li>✓ Empire OS Compliance</li>
                <li>✓ Cross-Module KPI Monitoring</li>
            </ul>
            
            <p><em>Centralized governance with powerful business intelligence</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Architectural diagram using Plotly - Enhanced with 3D effect and better design
    st.subheader("Synergyze Architecture & Data Flow")
    
    # Create the architecture diagram
    fig = go.Figure()
    
    # Enhanced box styling
    # Add rectangle shapes for the boxes with gradient-like effect
    fig.add_shape(type="rect", x0=0.05, y0=0.6, x1=0.45, y1=0.9,
                  line=dict(color="#2C5282", width=2),
                  fillcolor="#2C5282", opacity=0.7)
    
    fig.add_shape(type="rect", x0=0.55, y0=0.6, x1=0.95, y1=0.9,
                  line=dict(color="#276749", width=2),
                  fillcolor="#276749", opacity=0.7)
    
    fig.add_shape(type="rect", x0=0.25, y0=0.1, x1=0.75, y1=0.4,
                  line=dict(color="#553C9A", width=2),
                  fillcolor="#553C9A", opacity=0.7)
    
    # Add data flow connectors (more complex arrows)
    # Manufacturing to Hub
    fig.add_annotation(x=0.25, y=0.55, ax=0.40, ay=0.45,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#2C5282")
    
    # Hub to Manufacturing
    fig.add_annotation(x=0.40, y=0.45, ax=0.25, ay=0.55,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#553C9A")
    
    # Retail to Hub
    fig.add_annotation(x=0.75, y=0.55, ax=0.60, ay=0.45,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#276749")
    
    # Hub to Retail
    fig.add_annotation(x=0.60, y=0.45, ax=0.75, ay=0.55,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#553C9A")
    
    # Manufacturing to Retail
    fig.add_annotation(x=0.45, y=0.75, ax=0.55, ay=0.75,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#4A5568")
    
    # Retail to Manufacturing
    fig.add_annotation(x=0.55, y=0.70, ax=0.45, ay=0.70,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, 
                       arrowcolor="#4A5568")
    
    # Add text for the boxes with enhanced styling
    fig.add_annotation(x=0.25, y=0.75, text="Woven Supply<br><span style='font-size:0.8em;'>Manufacturing</span>",
                       font=dict(size=14, color="white", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    fig.add_annotation(x=0.75, y=0.75, text="Commune Connect<br><span style='font-size:0.8em;'>Retail</span>",
                       font=dict(size=14, color="white", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    fig.add_annotation(x=0.50, y=0.25, text="Synergyze Hub<br><span style='font-size:0.8em;'>Governance</span>",
                       font=dict(size=14, color="white", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    # Data flow annotations
    fig.add_annotation(x=0.33, y=0.53, text="Materials & Production",
                       font=dict(size=10, color="#2C5282", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
                       
    fig.add_annotation(x=0.33, y=0.47, text="License & Governance",
                       font=dict(size=10, color="#553C9A", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
                       
    fig.add_annotation(x=0.67, y=0.53, text="Sales & Inventory",
                       font=dict(size=10, color="#276749", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
                       
    fig.add_annotation(x=0.67, y=0.47, text="License & Governance",
                       font=dict(size=10, color="#553C9A", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
                       
    fig.add_annotation(x=0.50, y=0.77, text="Finished Goods",
                       font=dict(size=10, color="#4A5568", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
                       
    fig.add_annotation(x=0.50, y=0.68, text="Orders & Requirements",
                       font=dict(size=10, color="#4A5568", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    # Update layout with better styling
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#F7FAFC",
        paper_bgcolor="#F7FAFC",
        showlegend=False,
        title=dict(
            text="Voi Jeans Synergyze System Architecture",
            font=dict(size=16, color="#2D3748")
        )
    )
    
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add Voi Jeans assets overview
    st.subheader("Voi Jeans Assets Performance")
    
    # Create three metrics columns showing key performance indicators
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric(
            label="SS25 Collection Performance", 
            value="₹1.82 Cr", 
            delta="+14.5%", 
            help="Revenue generated by SS25 collection across all stores"
        )
    with metric_cols[1]:
        st.metric(
            label="Manufacturing Efficiency", 
            value="96.2%", 
            delta="+3.8%", 
            help="Manufacturing efficiency score for Scotts Garments CMP production"
        )
    with metric_cols[2]:
        st.metric(
            label="E-Wards Engagement", 
            value="62%", 
            delta="+5%", 
            help="Percentage of loyalty members actively engaging with the program"
        )
    with metric_cols[3]:
        st.metric(
            label="Supply Chain SLA", 
            value="98.4%", 
            delta="+2.1%", 
            help="Service Level Agreement performance across the supply chain"
        )
    
    # Department workflows
    st.subheader("Departmental Workflows")
    
    # Create expandable sections for each department workflow
    with st.expander("🏭 Design Department Workflow"):
        st.markdown("""
        1. **Design Department**
        2. **Product Conceptualization**
        3. **Prototyping and Trend Analysis**
        4. **Collaboration with Product and Marketing Teams**
        5. **Feedback Integration and Refinement**
        6. **Synergyze: Real-Time Design Insights and Integration**
        """)
    
    with st.expander("🏭 Product Department Workflow"):
        st.markdown("""
        1. **Product Department**
        2. **Procurement of Materials and Goods**
        3. **Vendor Management and Negotiations**
        4. **Inventory Planning and Replenishment**
        5. **Quality Control for Materials and Finished Products**
        6. **Synergyze: Automates Procurement and Suggests Supplier Optimization**
        """)
    
    with st.expander("🏭 Supply Chain Department Workflow"):
        st.markdown("""
        1. **Supply Chain Department**
        2. **Warehouse Management**
        3. **Stock Distribution to Retail and E-Commerce**
        4. **Reverse Logistics for Returns**
        5. **Synergyze: Implements WMS and Optimizes Logistics Routes**
        """)
    
    with st.expander("🏬 Marketing and PR Department Workflow"):
        st.markdown("""
        1. **Marketing and PR Department**
        2. **Brand Management and Lead Generation**
        3. **Campaigns Across Channels**
        4. **Community Building and Brand Loyalty Programs**
        5. **Synergyze: Provides Analytics and Audience Segmentation**
        """)
    
    with st.expander("🏬 Retailing Department Workflow"):
        st.markdown("""
        1. **Retailing Department**
        2. **Physical Store Management**
        3. **Stock Placement and Rotation**
        4. **Driving Footfall and In-Store Promotions**
        5. **Synergyze: Tracks Sales and Supports Replenishment**
        """)
    
    with st.expander("⚙️ Finance Department Workflow"):
        st.markdown("""
        1. **Finance Department**
        2. **Budget Allocation and Expense Tracking**
        3. **Revenue Monitoring and Profit Analysis**
        4. **Audits and Compliance Checks**
        5. **Synergyze: Automates Financial Reporting and ROI Tracking**
        """)
    
    with st.expander("⚙️ HR Department Workflow"):
        st.markdown("""
        1. **HR Department**
        2. **Employee Recruitment and Training**
        3. **Payroll Management and Grievance Handling**
        4. **Building Company Culture**
        5. **Synergyze: Tracks Engagement, Centralizes Training, Automates Payroll**
        """)
    
    with st.expander("⚙️ Administration Department Workflow"):
        st.markdown("""
        1. **Administration Department**
        2. **Facility and Office Management**
        3. **Regulatory Compliance and Permits**
        4. **Office Supply and Expense Management**
        5. **Synergyze: Centralizes Compliance Tracking and Monitors Expenses**
        """)
    
    with st.expander("⚙️ IT Department Workflow"):
        st.markdown("""
        1. **IT Department**
        2. **Managing Infrastructure and Software Systems**
        3. **Ensuring Data Security and Privacy Compliance**
        4. **Scaling Digital Infrastructure with Growth**
        5. **Synergyze: Integrates Tools, Monitors Performance, Enhances Cybersecurity**
        """)
    
    with st.expander("🏬 Customer Wing Workflow"):
        st.markdown("""
        1. **Customer Wing Start**
        2. **Customer Service: Handles Queries, Returns, and Complaints**
        3. **Engages Customers via Digital Platforms**
        4. **Runs Loyalty Programs and Collects Feedback**
        5. **Synergyze: Tracks Orders and Analyzes Feedback Automatically**
        """)

def show_network_visualization():
    """Display the network visualization of the Synergyze ecosystem"""
    
    st.subheader("Voi Jeans Ecosystem Network Visualization")
    
    # Premium styled intro box
    st.markdown("""
    <div style="background: linear-gradient(to right, #2D3748, #4A5568); color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h4 style="color: white; margin-top: 0;">Enterprise Network Visualization</h4>
        <p style="margin-bottom: 5px;">This interactive visualization maps the Voi Jeans enterprise ecosystem, showing real-time connections between entities and data flow across the network.</p>
        <div style="display: flex; margin-top: 10px;">
            <div style="margin-right: 15px; display: flex; align-items: center;">
                <div style="width: 12px; height: 12px; background-color: royalblue; border-radius: 50%; margin-right: 5px;"></div>
                <span style="font-size: 0.9em;">Manufacturing</span>
            </div>
            <div style="margin-right: 15px; display: flex; align-items: center;">
                <div style="width: 12px; height: 12px; background-color: mediumseagreen; border-radius: 50%; margin-right: 5px;"></div>
                <span style="font-size: 0.9em;">Retail</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 12px; height: 12px; background-color: darkorchid; border-radius: 50%; margin-right: 5px;"></div>
                <span style="font-size: 0.9em;">Governance</span>
            </div>
        </div>
    </div>
    """
    , unsafe_allow_html=True)
    
    # Create a graph using NetworkX
    G = nx.DiGraph()
    
    # Add nodes for each entity with their respective groups
    # Woven Supply (Manufacturing) nodes
    manufacturing_nodes = ["Voi Jeans HQ", "Scotts Garments", "Fabric Suppliers", "Accessory Vendors", 
                         "Quality Control", "Logistics Handlers", "Production Planning"]
    
    # Retail nodes
    retail_nodes = ["Voi Jeans Stores", "E-commerce Platform", "Consumers", "Marketing Team", 
                    "Warehouse", "Distribution Centers", "E-Wards Loyalty Program"]
    
    # Governance nodes
    governance_nodes = ["Synergyze Hub", "License Management", "Analytics Engine", "User Access Control", 
                        "Integration Layer", "Compliance Monitoring", "KPI Dashboard"]
    
    # Add nodes with group attributes
    for node in manufacturing_nodes:
        G.add_node(node, group=1)  # Manufacturing group
    
    for node in retail_nodes:
        G.add_node(node, group=2)  # Retail group
    
    for node in governance_nodes:
        G.add_node(node, group=3)  # Governance group
    
    # Add edges to represent relationships
    # Manufacturing connections
    G.add_edge("Voi Jeans HQ", "Scotts Garments", weight=5)
    G.add_edge("Scotts Garments", "Fabric Suppliers", weight=4)
    G.add_edge("Scotts Garments", "Accessory Vendors", weight=3)
    G.add_edge("Fabric Suppliers", "Quality Control", weight=2)
    G.add_edge("Accessory Vendors", "Quality Control", weight=2)
    G.add_edge("Quality Control", "Logistics Handlers", weight=3)
    G.add_edge("Production Planning", "Scotts Garments", weight=5)
    G.add_edge("Production Planning", "Logistics Handlers", weight=3)
    
    # Retail connections
    G.add_edge("Voi Jeans HQ", "Voi Jeans Stores", weight=5)
    G.add_edge("Voi Jeans HQ", "E-commerce Platform", weight=4)
    G.add_edge("Voi Jeans Stores", "Consumers", weight=5)
    G.add_edge("E-commerce Platform", "Consumers", weight=5)
    G.add_edge("Marketing Team", "Consumers", weight=3)
    G.add_edge("Warehouse", "Voi Jeans Stores", weight=4)
    G.add_edge("Warehouse", "Distribution Centers", weight=4)
    G.add_edge("Distribution Centers", "Voi Jeans Stores", weight=3)
    G.add_edge("Distribution Centers", "E-commerce Platform", weight=3)
    G.add_edge("E-Wards Loyalty Program", "Consumers", weight=2)
    
    # Governance connections (hub-and-spoke model)
    for node in manufacturing_nodes + retail_nodes:
        G.add_edge("Synergyze Hub", node, weight=1)
    
    for gov_node in governance_nodes[1:]:  # Skip the hub itself
        G.add_edge("Synergyze Hub", gov_node, weight=2)
    
    # Create a plot
    pos = nx.spring_layout(G, k=0.30, iterations=50, seed=42)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.8, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create node traces for each group
    node_trace1 = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            color='royalblue',
            size=20,
            line=dict(width=2, color='darkblue'))
    )
    
    node_trace2 = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            color='mediumseagreen',
            size=20,
            line=dict(width=2, color='darkgreen'))
    )
    
    node_trace3 = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            color='darkorchid',
            size=20,
            line=dict(width=2, color='indigo'))
    )
    
    # Add node positions to the appropriate trace
    for node in G.nodes():
        x, y = pos[node]
        group = G.nodes[node]['group']
        
        if group == 1:  # Manufacturing
            node_trace1['x'] = node_trace1['x'] + (x,)
            node_trace1['y'] = node_trace1['y'] + (y,)
            node_trace1['text'] = node_trace1['text'] + (node,)
        elif group == 2:  # Retail
            node_trace2['x'] = node_trace2['x'] + (x,)
            node_trace2['y'] = node_trace2['y'] + (y,)
            node_trace2['text'] = node_trace2['text'] + (node,)
        else:  # Governance
            node_trace3['x'] = node_trace3['x'] + (x,)
            node_trace3['y'] = node_trace3['y'] + (y,)
            node_trace3['text'] = node_trace3['text'] + (node,)
    
    # Create the figure with the traces
    fig = go.Figure(data=[edge_trace, node_trace1, node_trace2, node_trace3],
                    layout=go.Layout(
                        title='Synergyze Ecosystem Network',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='rgba(248,248,248,1)',
                        height=700
                    ))
    
    # Add legend
    fig.add_annotation(x=0.02, y=0.98, xref="paper", yref="paper",
                      text="● Woven Supply (Manufacturing)",
                      font=dict(size=12, color="royalblue"),
                      showarrow=False, align="left")
    
    fig.add_annotation(x=0.02, y=0.94, xref="paper", yref="paper",
                      text="● Commune Connect (Retail)",
                      font=dict(size=12, color="mediumseagreen"),
                      showarrow=False, align="left")
    
    fig.add_annotation(x=0.02, y=0.90, xref="paper", yref="paper",
                      text="● Synergyze Hub (Governance)",
                      font=dict(size=12, color="darkorchid"),
                      showarrow=False, align="left")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanatory text
    st.markdown("""
    ### Understanding the Network
    
    This visualization demonstrates how Synergyze creates an interconnected ecosystem that enables seamless 
    information flow between the manufacturing and retail operations. The Synergyze Hub serves as the central 
    governance layer, distributing licenses and controls to different entities based on their role within the ecosystem.
    
    **Key Integration Points:**
    
    1. **Manufacturing to Retail**: Product data flows from Scotts Garments (manufacturer) to Voi Jeans stores
    2. **Data Collection Points**: Consumer feedback and sales data is collected and fed back to planning
    3. **License Distribution**: ECG creates and manages tailored licenses for each entity in the network
    4. **Real-time Analytics**: Performance data is available to all stakeholders through the governance layer
    """)

def show_license_management():
    """Display the license management interface for Synergyze"""
    
    st.subheader("🔑 Voi Jeans Enterprise License Platform")
    
    # Premium license banner with styling
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1A365D 0%, #2D3748 100%); border-radius: 10px; padding: 20px; margin-bottom: 20px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: white; margin-top: 0;">Premium Enterprise License</h4>
                <p style="margin-bottom: 5px;">Tailored specifically for Voi Jeans Retail India Pvt Ltd</p>
                <p style="margin-bottom: 0; font-size: 0.9em; color: #90CDF4;">License ID: VJ-SYN-2025-PREMIUM-001</p>
            </div>
            <div style="text-align: right;">
                <p style="color: #68D391; margin: 0; font-weight: bold;">ACTIVE</p>
                <p style="font-size: 0.8em; margin: 0;">Valid until: March 30, 2026</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Voi Jeans maintains an exclusive Premium Enterprise License that provides access to the full suite of Synergyze 
    capabilities across manufacturing, retail, and governance. This license enables seamless integration of all business 
    operations and provides advanced analytics and monitoring tools.
    """)
    
    # License roles table
    st.subheader("License Roles and Capabilities")
    
    license_data = {
        "License Type": [
            "Woven Supply - Manufacturer", 
            "Woven Supply - Raw Material Provider",
            "Woven Supply - Factory",
            "Woven Supply - Logistics",
            "Commune Connect - Retail Store",
            "Commune Connect - E-commerce",
            "Commune Connect - Distribution",
            "Commune Connect - Marketing",
            "Synergyze Hub - Administration",
            "Synergyze Hub - Finance",
            "Synergyze Hub - Executive"
        ],
        "Key Features": [
            "Production planning, material requisition, quality tracking",
            "Material catalog, quality specifications, order management",
            "Production tracking, efficiency metrics, QC tools",
            "Shipping, tracking, customs documentation",
            "POS integration, inventory, staff management",
            "Online catalog, order processing, digital marketing",
            "Warehouse management, inventory tracking",
            "Campaign management, analytics, customer segmentation",
            "User administration, compliance tracking, system configuration",
            "Budgeting, cost tracking, payment processing",
            "Cross-module dashboards, KPIs, strategic planning"
        ],
        "Network Access": [
            "Manufacturing network",
            "Material suppliers network",
            "Production network",
            "Distribution network",
            "Store network",
            "Digital commerce network",
            "Logistics network",
            "Consumer engagement network",
            "Administrative network",
            "Financial network",
            "Full system access"
        ],
        "Integration Level": [
            "High",
            "Medium",
            "High",
            "Medium",
            "High",
            "High",
            "Medium",
            "Medium",
            "High",
            "High",
            "Complete"
        ]
    }
    
    license_df = pd.DataFrame(license_data)
    
    st.dataframe(
        license_df,
        use_container_width=True,
        column_config={
            "License Type": st.column_config.TextColumn(
                "License Type",
                help="Type of license based on role in the ecosystem"
            ),
            "Key Features": st.column_config.TextColumn(
                "Key Features",
                help="Main capabilities provided by this license"
            ),
            "Network Access": st.column_config.TextColumn(
                "Network Access",
                help="Which parts of the network this license can access"
            ),
            "Integration Level": st.column_config.TextColumn(
                "Integration Level",
                help="Depth of integration with the Synergyze ecosystem"
            )
        },
        hide_index=True
    )
    
    # License visualization
    st.subheader("Voi Jeans License Structure")
    
    # Create a more detailed and impressive sunburst chart for license visualization
    labels = [
        "Synergyze Premium", 
        "Woven Supply", "Commune Connect", "Synergyze Hub",
        "Manufacturing", "Material", "Factory", "Logistics",
        "Retail", "E-commerce", "Distribution", "Marketing",
        "Admin", "Finance", "Executive",
        "SS25 Planning", "QC Tracking", "Factory Dashboard",
        "Denim Sourcing", "Trim Management", "Shipment Tracking",
        "Store Network", "E-Wards Loyalty", "Store Inventory", "Sales Analytics",
        "Marketplace", "Online Catalog", "Campaign Manager",
        "User Access", "System Config", "Compliance",
        "Budgeting", "CMP Costing", "Financial Reporting",
        "KPI Dashboard", "Supply Chain Vis", "Business Intelligence"
    ]
    
    parents = [
        "", 
        "Synergyze Premium", "Synergyze Premium", "Synergyze Premium",
        
        "Woven Supply", "Woven Supply", "Woven Supply", "Woven Supply",
        "Commune Connect", "Commune Connect", "Commune Connect", "Commune Connect",
        "Synergyze Hub", "Synergyze Hub", "Synergyze Hub",
        
        "Manufacturing", "Manufacturing", "Manufacturing",
        "Material", "Material", "Logistics",
        "Retail", "Retail", "Retail", "Retail", 
        "E-commerce", "E-commerce", "Marketing",
        "Admin", "Admin", "Admin",
        "Finance", "Finance", "Finance",
        "Executive", "Executive", "Executive"
    ]
    
    values = [
        100, 
        30, 30, 40,
        
        10, 5, 10, 5,
        10, 5, 10, 5,
        10, 15, 15,
        
        4, 3, 3,
        2, 2, 5,
        3, 3, 2, 2,
        2, 2, 5,
        3, 3, 4,
        5, 5, 5,
        5, 5, 5
    ]
    
    # Custom hover information with module descriptions
    module_descriptions = {
        "SS25 Planning": "Create and manage production plans for SS25 collection",
        "QC Tracking": "Track quality control metrics and defect rates",
        "Factory Dashboard": "Monitor factory operations and efficiency",
        "Denim Sourcing": "Manage denim fabric vendors and procurement",
        "Trim Management": "Inventory and sourcing for buttons, zippers and other trims",
        "Shipment Tracking": "Real-time tracking of shipments and logistics",
        "Store Network": "Manage 20+ Voi Jeans retail locations",
        "E-Wards Loyalty": "Manage customer loyalty program with 24,850+ members",
        "Store Inventory": "Track and manage in-store inventory levels",
        "Sales Analytics": "Analyze sales performance across locations",
        "Marketplace": "Manage marketplace integrations and sales channels",
        "Online Catalog": "Digital product catalog management",
        "Campaign Manager": "Plan and execute marketing campaigns",
        "User Access": "Control user permissions and access levels",
        "System Config": "Configure system settings and preferences",
        "Compliance": "Monitor regulatory and policy compliance",
        "Budgeting": "Budget planning and allocation tools",
        "CMP Costing": "Calculate and analyze CMP manufacturing costs",
        "Financial Reporting": "Generate financial reports and statements",
        "KPI Dashboard": "Executive key performance indicator dashboard",
        "Supply Chain Vis": "End-to-end supply chain visualization",
        "Business Intelligence": "Advanced analytics and reporting tools"
    }
    
    hover_data = []
    for label in labels:
        if label in module_descriptions:
            hover_data.append(f"{label}: {module_descriptions[label]}")
        else:
            hover_data.append(label)
    
    # Create a custom color scheme
    custom_colors = [
        "#1A365D",  # Root
        
        "#2C5282", "#276749", "#553C9A",  # Main categories
        
        "#3182CE", "#63B3ED", "#4299E1", "#2B6CB0",  # Manufacturing modules
        "#38A169", "#68D391", "#48BB78", "#2F855A",  # Retail modules
        "#805AD5", "#9F7AEA", "#6B46C1",  # Governance modules
        
        # Detailed modules
        "#4299E1", "#3182CE", "#2B6CB0",  # Manufacturing sub-modules
        "#90CDF4", "#63B3ED", "#2C5282",  # Material sub-modules
        "#48BB78", "#38A169", "#2F855A", "#276749",  # Retail sub-modules
        "#68D391", "#9AE6B4", "#C6F6D5",  # E-commerce sub-modules
        "#805AD5", "#9F7AEA", "#6B46C1",  # Admin sub-modules
        "#B794F4", "#D6BCFA", "#E9D8FD",  # Finance sub-modules
        "#553C9A", "#6B46C1", "#805AD5"   # Executive sub-modules
    ]
    
    fig = px.sunburst(
        names=labels,
        parents=parents,
        values=values,
        color=labels,
        color_discrete_sequence=custom_colors,
        title="Voi Jeans Premium License - Module Structure",
        hover_data=[hover_data]
    )
    
    fig.update_layout(
        margin=dict(t=60, l=0, r=0, b=0), 
        height=700,
        title=dict(
            text="Voi Jeans Premium License - Module Structure",
            font=dict(size=18, color="#2D3748")
        ),
        template="plotly_dark"
    )
    
    # Add custom styling
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Allocation: %{value}%<br>%{customdata[0]}<extra></extra>',
        textfont=dict(size=14, family="Arial, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ECG's license customization
    st.subheader("ECG's License Customization Process")
    
    st.markdown("""
    ### How ECG Creates Custom Synergyze Licenses
    
    1. **Business Assessment**: ECG evaluates the company's operations, needs, and goals
    2. **Module Selection**: Identifies the appropriate modules from the ecosystem
    3. **Role Configuration**: Configures access levels and permissions based on user roles
    4. **Network Integration**: Establishes connections to relevant networks within the ecosystem
    5. **License Deployment**: Distributes secure license credentials to authorized personnel
    6. **Continuous Adjustment**: Adjusts license features as the company's needs evolve
    
    This tailored approach ensures each company receives a Synergyze license that precisely 
    matches their operational requirements and enables them to fully leverage the platform's capabilities.
    """)
    
    # Enable Empire OS governance access for demo
    if not st.session_state.has_empire_license:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.warning("You don't currently have access to Empire OS Governance features.")
        with col2:
            if st.button("Request Empire OS Access", type="primary"):
                st.session_state.has_empire_license = True
                st.success("Empire OS Governance access granted for demonstration purposes!")
                st.info("Please reload the page to access Empire OS features.")
    else:
        st.success("You have Empire OS Governance access. You can view additional tabs for Data Sharing and Empire OS Governance.")
        # Revoke Empire OS access
        if st.button("Revoke Empire OS Access", type="secondary"):
            st.session_state.has_empire_license = False
            st.warning("Empire OS Governance access revoked.")
            st.info("Please reload the page to apply changes.")

def show_empire_os_governance():
    """Display the Empire OS governance interface"""
    
    st.subheader("⚙️ Empire OS Governance & Compliance")
    
    # Premium styled governance banner
    st.markdown("""
    <div style="background: linear-gradient(90deg, #44337A 0%, #553C9A 100%); border-radius: 10px; padding: 20px; margin-bottom: 20px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color: white; margin-top: 0;">Divine Constitution Governance</h4>
                <p style="margin-bottom: 0;">Empire OS provides white-labeled governance following Divine Constitution principles</p>
            </div>
            <div style="text-align: right;">
                <p style="color: #D6BCFA; margin: 0; font-weight: bold;">SUPREME LICENSE ACTIVE</p>
                <p style="font-size: 0.8em; margin: 0;">Governed by ECG Protocols</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show constitutional principles
    principles_col1, principles_col2 = st.columns(2)
    
    with principles_col1:
        st.markdown("""
        <div style="background-color: #F3E8FF; padding: 15px; border-radius: 5px; height: 100%;">
            <h4 style="color: #553C9A; margin-top: 0;">Divine Constitution Principles</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✓ Stewardship Over Ownership</li>
                <li>✓ Truth and Transparency</li>
                <li>✓ Divine Fairness in Trade</li>
                <li>✓ No Wastage/Excess</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with principles_col2:
        st.markdown("""
        <div style="background-color: #F3E8FF; padding: 15px; border-radius: 5px; height: 100%;">
            <h4 style="color: #553C9A; margin-top: 0;">Governance Principles</h4>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>✓ Justice by Design</li>
                <li>✓ Quiet Governance</li>
                <li>✓ Right to Build/Withdraw</li>
                <li>✓ No False Representation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    As a premium license holder with signed data sharing agreements, Voi Jeans has exclusive access to Empire OS Governance features, 
    enabling complete visibility and control over data flows, license management, and compliance monitoring.
    """)
    
    # Create tabs for different governance features
    tab1, tab2, tab3, tab4 = st.tabs([
        "EIP Registry", 
        "License Templates", 
        "River Transaction Logs",
        "ECG Compliance"
    ])
    
    with tab1:
        show_eip_registry()
    
    with tab2:
        show_license_templates()
    
    with tab3:
        show_river_logs()
    
    with tab4:
        show_ecg_compliance()

def show_eip_registry():
    """Display the Empire Identity Protocol (EIP) registry"""
    
    st.markdown("### Empire Identity Protocol (EIP) Registry")
    
    st.markdown("""
    The EIP Registry is the central repository of all registered entities in the Empire OS ecosystem.
    Each entity is assigned a unique EIP identifier and registered with its business type.
    """)
    
    # Sample EIP registry data
    eip_data = {
        "Name": ["Voi Jeans", "Killer Jeans", "Scotts Garments", "Fabric Mills Ltd.", "Fashion Retail Co."],
        "EIP ID": ["EIP_00243", "EIP_00244", "EIP_00245", "EIP_00246", "EIP_00247"],
        "Type": ["Brand", "Brand", "Manufacturer", "Manufacturer", "Retailer"],
        "Status": ["Active", "Active", "Pending", "Active", "Rejected"]
    }
    
    # Apply status styling
    def highlight_status(val):
        if val == "Active":
            return "background-color: #90EE90"  # Light green
        elif val == "Pending":
            return "background-color: #FFFFE0"  # Light yellow
        elif val == "Rejected":
            return "background-color: #FFC0CB"  # Light red
        return ""
    
    df_eip = pd.DataFrame(eip_data)
    styled_df = df_eip.style.applymap(highlight_status, subset=["Status"])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Entity registration form
    st.markdown("### Register New EIP Identity")
    
    col1, col2 = st.columns(2)
    with col1:
        entity_type = st.selectbox("Entity Type", ["Company", "Individual", "Organization"])
        business_type = st.selectbox("Business Type", ["Manufacturer", "Retailer", "Brand", "Service Provider"])
    
    with col2:
        country = st.selectbox("Country", ["India (IN)", "United States (US)", "United Kingdom (UK)", "Other"])
        registration_id = st.text_input("Registration ID (GST/PAN/CIN)")
    
    entity_name = st.text_input("Entity Name")
    
    if st.button("Register Entity", key="register_entity"):
        if entity_name:
            st.success(f"Entity '{entity_name}' registered successfully with EIP ID: EIP_{datetime.datetime.now().strftime('%Y%m%d%H%M')}")
        else:
            st.error("Entity name is required")

def show_license_templates():
    """Display the license templates for different business types and models"""
    
    st.markdown("### License Templates")
    
    st.markdown("""
    License templates define the standard terms, conditions, and access levels for different
    business types and models in the Empire OS ecosystem.
    """)
    
    # Sample license template data
    license_data = {
        "Template ID": ["TEMPLATE-CMP-001", "TEMPLATE-FOB-001", "TEMPLATE-WLBL-001", "TEMPLATE-MKT-001", 
                      "TEMPLATE-SOR-001", "TEMPLATE-LFR-001", "TEMPLATE-HOUSE-001", "TEMPLATE-PL-001"],
        "Name": ["CMP Manufacturer", "FOB Manufacturer", "White-Label Manufacturer", "Marketplace Retailer",
               "SOR Retailer", "Large Format Retailer", "House Brand", "Private Label Brand"],
        "Business Type": ["Manufacturer", "Manufacturer", "Manufacturer", "Retailer", 
                        "Retailer", "Retailer", "Brand", "Brand"],
        "Business Model": ["CMP", "FOB", "White-Label", "Marketplace", 
                         "SOR", "Large Format Retail", "House Brand", "Private Label"],
        "Data Access Level": ["Limited", "Standard", "Standard", "Limited", 
                            "Standard", "Standard", "Full", "Full"],
        "Validity (days)": [365, 365, 365, 365, 365, 365, 730, 730]
    }
    
    df_license = pd.DataFrame(license_data)
    st.dataframe(df_license, use_container_width=True)
    
    # License template matrix visualization
    st.markdown("### License Template Matrix")
    
    # Create a heatmap showing the relationship between business types and models
    matrix_data = pd.crosstab(
        df_license["Business Type"], 
        df_license["Business Model"],
        values=df_license["Template ID"],
        aggfunc=lambda x: x.iloc[0] if len(x) > 0 else ""
    )
    
    # Display matrix
    st.dataframe(matrix_data, use_container_width=True)
    
    # Show a visualization of the license template association
    st.markdown("### Template Association Flow")
    
    # Create data for a sankey diagram
    labels = list(set(df_license["Business Type"].tolist() + df_license["Business Model"].tolist() + df_license["Template ID"].tolist()))
    
    # Create source, target, value arrays for the Sankey diagram
    source = []
    target = []
    value = []
    
    for i, row in df_license.iterrows():
        source.append(labels.index(row["Business Type"]))
        target.append(labels.index(row["Business Model"]))
        value.append(1)
        
        source.append(labels.index(row["Business Model"]))
        target.append(labels.index(row["Template ID"]))
        value.append(1)
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = ["#1E3A8A" if label in df_license["Business Type"].unique() else 
                    "#047857" if label in df_license["Business Model"].unique() else
                    "#7C3AED" for label in labels]
        ),
        link = dict(
            source = source,
            target = target,
            value = value
        ))])
    
    fig.update_layout(title_text="Business Type → Model → License Template Flow", font_size=10, height=500)
    st.plotly_chart(fig, use_container_width=True)

def show_river_logs():
    """Display the River transaction logs for data access auditing"""
    
    st.markdown("### River Transaction Logs")
    
    st.markdown("""
    River is the Empire OS transaction logging system that records all data access, sharing, and license operations.
    All transactions are immutable and provide an audit trail for governance and compliance.
    """)
    
    # Sample transaction data
    now = datetime.datetime.now()
    transaction_data = {
        "Transaction ID": [f"TXN-{now.strftime('%Y%m%d')}-{i+1:03d}" for i in range(7)],
        "Entity": ["Voi Jeans", "Scotts Garments", "Voi Jeans", "Fabric Mills Ltd.", "Voi Jeans", 
                 "Scotts Garments", "Voi Jeans"],
        "Type": ["Data Access", "Data Access", "Data Access", "Data Access", "License Update", 
               "Agreement Signature", "Data Sharing"],
        "Resource": ["Order: PO-2025-001", "Style: ST-2025-001", "Material: FAB-DENIM-001", 
                   "Material: FAB-DENIM-001", "License: LIC-VOI-2025-001", 
                   "Agreement: DSA-SCOTTS-2025-001", "Style: ST-2025-002"],
        "Timestamp": [now - datetime.timedelta(hours=i) for i in range(1, 8)],
        "Access Level": ["Read", "Read", "Read", "Write", "Write", "Write", "Full"],
        "Status": ["Success", "Success", "Success", "Success", "Success", "Success", "Success"]
    }
    
    df_txn = pd.DataFrame(transaction_data)
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        entity_filter = st.selectbox("Filter by Entity", ["All"] + list(set(df_txn["Entity"])))
    with col2:
        type_filter = st.selectbox("Filter by Type", ["All"] + list(set(df_txn["Type"])))
    with col3:
        status_filter = st.selectbox("Filter by Status", ["All", "Success", "Failed", "Pending"])
    
    # Apply filters
    filtered_df = df_txn
    if entity_filter != "All":
        filtered_df = filtered_df[filtered_df["Entity"] == entity_filter]
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    
    # Format timestamps
    filtered_df["Timestamp"] = filtered_df["Timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Transaction volume visualization
    st.markdown("### Transaction Volume")
    
    # Create sample transaction volume data
    dates = [now - datetime.timedelta(days=i) for i in range(7)]
    volumes = [124, 98, 145, 132, 156, 87, 115]
    volume_data = pd.DataFrame({
        "Date": dates,
        "Volume": volumes
    })
    
    # Create bar chart
    fig = px.bar(
        volume_data, 
        x="Date", 
        y="Volume", 
        title="Daily Transaction Volume",
        labels={"Date": "Date", "Volume": "Transaction Count"}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_ecg_compliance():
    """Display the ECG compliance monitoring dashboard"""
    
    st.markdown("### ECG Compliance Monitoring")
    
    st.markdown("""
    Empire Commune Global (ECG) provides oversight and compliance monitoring for all entities
    in the Empire OS ecosystem. This dashboard shows the current compliance status for your organization.
    """)
    
    # Compliance status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Overall Compliance Score", value="92%", delta="+3%")
    
    with col2:
        st.metric(label="Audit Status", value="Approved", delta="Last: 2025-02-15")
    
    with col3:
        st.metric(label="Data Sharing Compliance", value="98%", delta="+2%")
    
    # Compliance details
    st.markdown("### Compliance Details")
    
    compliance_data = {
        "Category": ["Data Protection", "Financial Reporting", "Industry Standards", "User Access Control", 
                   "Data Retention", "Third-party Sharing"],
        "Status": ["Compliant", "Compliant", "Compliant", "Compliant", "Warning", "Compliant"],
        "Score": [95, 90, 94, 98, 82, 93],
        "Last Check": ["2025-03-25", "2025-03-20", "2025-03-15", "2025-03-25", "2025-03-25", "2025-03-20"]
    }
    
    # Apply color based on status
    def color_status(val):
        if val == "Compliant":
            return "background-color: #90EE90"  # Light green
        elif val == "Warning":
            return "background-color: #FFFFE0"  # Light yellow
        elif val == "Non-compliant":
            return "background-color: #FFC0CB"  # Light red
        return ""
    
    # Apply color based on score
    def color_score(val):
        if val >= 90:
            return "color: green"
        elif val >= 80:
            return "color: orange"
        else:
            return "color: red"
    
    df_compliance = pd.DataFrame(compliance_data)
    styled_df = df_compliance.style.applymap(color_status, subset=["Status"]).applymap(color_score, subset=["Score"])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Compliance history visualization
    st.markdown("### Compliance History")
    
    # Create sample history data
    history_data = {
        "Date": [datetime.datetime(2025, month, 1) for month in range(1, 4)],
        "Data Protection": [90, 92, 95],
        "Financial Reporting": [85, 87, 90],
        "Industry Standards": [88, 90, 94],
        "User Access Control": [95, 96, 98],
        "Data Retention": [75, 80, 82],
        "Third-party Sharing": [88, 90, 93]
    }
    
    df_history = pd.DataFrame(history_data)
    
    # Melt the dataframe for easier plotting
    df_melted = pd.melt(df_history, id_vars=["Date"], var_name="Category", value_name="Score")
    
    # Create line chart
    fig = px.line(
        df_melted, 
        x="Date", 
        y="Score", 
        color="Category",
        title="Compliance Score Trends",
        labels={"Date": "Date", "Score": "Compliance Score (%)"}
    )
    
    fig.update_layout(yaxis_range=[70, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # ECG recommendations
    st.markdown("### ECG Recommendations")
    
    with st.expander("Data Retention Policy Enhancement"):
        st.markdown("""
        **Status: Recommended Action Required**
        
        Your organization's data retention policy needs updating to comply with the latest ECG guidelines:
        
        1. Implement automated data purging for records older than 24 months
        2. Add documentation for retention exception cases
        3. Update user notification templates for data deletion events
        
        **Deadline for implementation: April 15, 2025**
        """)
    
    with st.expander("Financial Health Check"):
        st.markdown("""
        **Status: Compliant**
        
        Your organization's financial health indicators meet all ECG requirements:
        
        - Liquidity ratio: 2.8 (above required 1.5)
        - Debt-to-equity ratio: 0.4 (below maximum 0.6)
        - Operating margin: 18% (above required 10%)
        
        Continue maintaining current financial governance practices.
        """)
    
    with st.expander("Industry Compliance Update"):
        st.markdown("""
        **Status: Compliant**
        
        Your organization has successfully implemented the latest textile industry compliance requirements:
        
        - Sustainable sourcing documentation complete
        - Supply chain transparency reporting implemented
        - Carbon footprint calculation methodology approved
        
        Next audit scheduled for: August 15, 2025
        """)
        
    # Premium services notice
    st.info("""
    **Note:** Premium charges apply for the governance and compliance checking services provided by ECG.
    These services ensure your organization maintains the highest standards of data governance and regulatory compliance.
    """)
    
    # Compliance documentation
    with st.expander("Required Compliance Documentation"):
        st.markdown("""
        ### Required Documentation
        
        The following documents must be maintained and updated to maintain ECG compliance:
        
        1. Data Sharing Agreement (Review annually)
        2. Data Protection Impact Assessment (Review bi-annually)
        3. Industry-specific Compliance Certificates (Renew as required)
        4. Financial Health Documentation (Update quarterly)
        5. User Access Control Audit Logs (Maintain continuously)
        
        All documentation must be accessible for ECG audits with 72-hour notice.
        """)

if __name__ == "__main__":
    show_synergy_visualization()