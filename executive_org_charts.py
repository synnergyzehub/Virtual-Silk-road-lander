import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from PIL import Image
import io
import base64

def show_executive_org_charts():
    """
    Display interactive organization charts for executives (CFO, CIO) with ECG perspective
    """
    st.title("Executive Organization Charts")
    st.subheader("Enterprise Capability Governance (ECG) Lens")
    
    # Secret advisory view toggle
    enable_secret_view = st.toggle("Enable Executive Advisory Channel", value=False, help="Show the direct advisory channel between CFO/CIO and CEO for license oversight")
    
    if enable_secret_view:
        st.warning("You are viewing the private executive advisory channel. This perspective provides unfiltered license insights that bypass normal organizational visibility.")
    
    # Create tabs for different executive views
    tab1, tab2, tab3, tab4 = st.tabs([
        "CFO Organization", 
        "CIO Organization", 
        "Joint Oversight",
        "CEO Direct Advisory" if enable_secret_view else "Executive Dashboard"
    ])
    
    with tab1:
        show_cfo_organization()
    
    with tab2:
        show_cio_organization()
    
    with tab3:
        show_executive_joint_oversight()
    
    with tab4:
        show_ceo_direct_advisory(enable_secret_view)

def show_cfo_organization():
    """Show CFO organizational structure with license governance view"""
    
    st.subheader("CFO Organization - Financial Governance")
    
    # Description
    st.markdown("""
    The CFO oversees the financial aspects of the enterprise, ensuring proper governance 
    of license costs, cost allocations, and financial reporting across all departments.
    The chart below demonstrates how financial governance is applied across the organization.
    """)
    
    # CFO organization chart data
    cfo_chart_data = {
        'id': [
            'CFO',
            'Financial Reporting', 'Cost Analysis', 'Treasury', 'License Finance', 'Compliance',
            'Balance Sheet', 'P&L', 'Cash Flow Statement', 'Financial KPIs',
            'CMP Costing', 'Retail Operations Cost', 'IT Infrastructure Cost', 'Marketing ROI',
            'Cash Management', 'Banking', 'Foreign Exchange',
            'License Budget', 'User Allocation Cost', 'Module ROI Analysis',
            'Audit', 'Tax Compliance', 'Financial Governance'
        ],
        'parent': [
            '',
            'CFO', 'CFO', 'CFO', 'CFO', 'CFO',
            'Financial Reporting', 'Financial Reporting', 'Financial Reporting', 'Financial Reporting',
            'Cost Analysis', 'Cost Analysis', 'Cost Analysis', 'Cost Analysis',
            'Treasury', 'Treasury', 'Treasury',
            'License Finance', 'License Finance', 'License Finance',
            'Compliance', 'Compliance', 'Compliance'
        ],
        'value': [
            50, 
            10, 10, 10, 12, 8,
            2.5, 2.5, 2.5, 2.5,
            2.5, 2.5, 2.5, 2.5,
            3, 3, 4,
            4, 4, 4,
            3, 3, 2
        ],
        'label': [
            'CFO',
            'Financial Reporting', 'Cost Analysis', 'Treasury', 'License Finance', 'Compliance',
            'Balance Sheet', 'P&L', 'Cash Flow', 'Financial KPIs',
            'CMP Costing', 'Retail Ops Cost', 'IT Cost', 'Marketing ROI',
            'Cash Management', 'Banking', 'Foreign Exchange',
            'License Budget', 'User Allocation', 'Module ROI',
            'Audit', 'Tax Compliance', 'Governance'
        ],
        'focus': [
            'All',
            'Reporting', 'Analysis', 'Management', 'License', 'Compliance',
            'Reporting', 'Reporting', 'Reporting', 'Reporting',
            'Analysis', 'Analysis', 'Analysis', 'Analysis',
            'Management', 'Management', 'Management',
            'License', 'License', 'License',
            'Compliance', 'Compliance', 'Compliance'
        ]
    }
    
    # Color map for different focus areas
    color_map = {
        'All': '#3366CC',
        'Reporting': '#DC3912',
        'Analysis': '#FF9900',
        'Management': '#109618',
        'License': '#990099',
        'Compliance': '#0099C6'
    }
    
    # Create sunburst chart
    fig = px.sunburst(
        cfo_chart_data,
        ids='id',
        parents='parent',
        values='value',
        names='label',
        color='focus',
        color_discrete_map=color_map,
        title="CFO Organization - License Governance Perspective",
        height=700
    )
    
    fig.update_layout(margin=dict(t=60, l=25, r=25, b=25))
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # License management focus
    st.subheader("License Financial Governance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### License Budget Management
        
        - **Annual License Budget Planning**
          *Forecasting license costs by department*
          
        - **Cost Allocation Models**
          *User-based and module-based allocation*
          
        - **License Utilization Analysis**
          *Measuring ROI on license investment*
          
        - **Usage-based Billing**
          *Department chargebacks for license usage*
        """)
        
    with col2:
        st.markdown("""
        ### License Financial Controls
        
        - **License Procurement Process**
          *Purchase approval workflows*
          
        - **License Audit Trail**
          *Tracking license purchases and assignments*
          
        - **Cost Optimization Strategies**
          *Right-sizing license types by user role*
          
        - **Compliance Verification**
          *Ensuring adherence to license terms*
        """)

def show_cio_organization():
    """Show CIO organizational structure with license governance view"""
    
    st.subheader("CIO Organization - Technology Governance")
    
    # Description
    st.markdown("""
    The CIO oversees the technological aspects of the enterprise, ensuring proper governance 
    of license deployments, data integration, security, and system performance across all departments.
    The chart below demonstrates how technology governance is applied across the organization.
    """)
    
    # CIO organization chart data
    cio_chart_data = {
        'id': [
            'CIO',
            'Infrastructure', 'Security', 'Data Management', 'License Admin', 'Enterprise Apps',
            'On-Premises Systems', 'Cloud Infrastructure', 'Network Management',
            'Access Control', 'Data Security', 'Compliance',
            'Database Administration', 'Data Integration', 'Data Quality', 'Master Data',
            'User Management', 'Module Deployment', 'License Monitoring',
            'ERP Systems', 'CRM Systems', 'Business Intelligence', 'Collaboration Tools'
        ],
        'parent': [
            '',
            'CIO', 'CIO', 'CIO', 'CIO', 'CIO',
            'Infrastructure', 'Infrastructure', 'Infrastructure',
            'Security', 'Security', 'Security',
            'Data Management', 'Data Management', 'Data Management', 'Data Management',
            'License Admin', 'License Admin', 'License Admin',
            'Enterprise Apps', 'Enterprise Apps', 'Enterprise Apps', 'Enterprise Apps'
        ],
        'value': [
            50, 
            10, 10, 12, 10, 8,
            3, 4, 3,
            3, 4, 3,
            3, 3, 3, 3,
            3, 4, 3,
            2, 2, 2, 2
        ],
        'label': [
            'CIO',
            'Infrastructure', 'Security', 'Data Management', 'License Admin', 'Enterprise Apps',
            'On-Premises', 'Cloud', 'Network',
            'Access Control', 'Data Security', 'Compliance',
            'Database Admin', 'Data Integration', 'Data Quality', 'Master Data',
            'User Management', 'Module Deployment', 'License Monitoring',
            'ERP Systems', 'CRM Systems', 'BI Tools', 'Collaboration'
        ],
        'domain': [
            'All',
            'Infrastructure', 'Security', 'Data', 'License', 'Applications',
            'Infrastructure', 'Infrastructure', 'Infrastructure',
            'Security', 'Security', 'Security',
            'Data', 'Data', 'Data', 'Data',
            'License', 'License', 'License',
            'Applications', 'Applications', 'Applications', 'Applications'
        ]
    }
    
    # Color map for different domains
    color_map = {
        'All': '#3366CC',
        'Infrastructure': '#DC3912',
        'Security': '#FF9900',
        'Data': '#109618',
        'License': '#990099',
        'Applications': '#0099C6'
    }
    
    # Create sunburst chart
    fig = px.sunburst(
        cio_chart_data,
        ids='id',
        parents='parent',
        values='value',
        names='label',
        color='domain',
        color_discrete_map=color_map,
        title="CIO Organization - License Technology Governance",
        height=700
    )
    
    fig.update_layout(margin=dict(t=60, l=25, r=25, b=25))
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # License management focus
    st.subheader("License Technology Governance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### License Deployment Management
        
        - **User Provisioning Workflows**
          *Automating user setup and permissions*
          
        - **Module Configuration Management**
          *Controlled deployment of new features*
          
        - **System Integration Management**
          *Connecting license modules with other systems*
          
        - **Upgrade & Patch Management**
          *Coordinated system updates*
        """)
        
    with col2:
        st.markdown("""
        ### License Technical Controls
        
        - **Access Control & Authentication**
          *Role-based access to licensed modules*
          
        - **Security Compliance**
          *Ensuring data protection across modules*
          
        - **Usage Monitoring & Analytics**
          *Tracking system utilization*
          
        - **Performance Optimization**
          *Ensuring system responsiveness*
        """)

def show_executive_joint_oversight():
    """Show how CFO and CIO jointly oversee license governance"""
    
    st.subheader("Executive Joint Oversight - ECG Framework")
    
    # Description
    st.markdown("""
    The CFO and CIO work together through the Enterprise Capability Governance (ECG) framework
    to ensure holistic oversight of license management, balancing financial considerations with
    technological capabilities and security requirements.
    """)
    
    # Create a network visualization of the governance model
    
    # Create a graph
    G = nx.Graph()
    
    # Add nodes
    nodes = [
        {"id": "CFO", "group": 1, "size": 25},
        {"id": "CIO", "group": 2, "size": 25},
        {"id": "ECG Framework", "group": 3, "size": 30},
        {"id": "License Budget", "group": 1, "size": 15},
        {"id": "Cost Allocation", "group": 1, "size": 15},
        {"id": "Finance Compliance", "group": 1, "size": 15},
        {"id": "ROI Analysis", "group": 1, "size": 15},
        {"id": "User Management", "group": 2, "size": 15},
        {"id": "Module Deployment", "group": 2, "size": 15},
        {"id": "Data Security", "group": 2, "size": 15},
        {"id": "System Integration", "group": 2, "size": 15},
        {"id": "Woven Supply", "group": 4, "size": 20},
        {"id": "Commune Connect", "group": 5, "size": 20},
        {"id": "Synergyze Hub", "group": 6, "size": 20},
    ]
    
    # Add nodes to the graph
    for node in nodes:
        G.add_node(node["id"], group=node["group"], size=node["size"])
    
    # Add edges
    edges = [
        ("CFO", "ECG Framework", 5),
        ("CIO", "ECG Framework", 5),
        ("ECG Framework", "Woven Supply", 3),
        ("ECG Framework", "Commune Connect", 3),
        ("ECG Framework", "Synergyze Hub", 3),
        ("CFO", "License Budget", 2),
        ("CFO", "Cost Allocation", 2),
        ("CFO", "Finance Compliance", 2),
        ("CFO", "ROI Analysis", 2),
        ("CIO", "User Management", 2),
        ("CIO", "Module Deployment", 2),
        ("CIO", "Data Security", 2),
        ("CIO", "System Integration", 2),
        ("License Budget", "ECG Framework", 1),
        ("Cost Allocation", "ECG Framework", 1),
        ("Finance Compliance", "ECG Framework", 1),
        ("ROI Analysis", "ECG Framework", 1),
        ("User Management", "ECG Framework", 1),
        ("Module Deployment", "ECG Framework", 1),
        ("Data Security", "ECG Framework", 1),
        ("System Integration", "ECG Framework", 1),
    ]
    
    # Add edges to the graph
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    # Create positions using a spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Create edge trace
    edge_trace = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = G.get_edge_data(edge[0], edge[1])['weight']
        
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=weight, color='rgba(128, 128, 128, 0.7)'),
                hoverinfo='none',
                mode='lines'
            )
        )
    
    # Create node traces for different groups
    node_traces = []
    
    # Color map for different groups
    group_colors = {
        1: 'rgb(31, 119, 180)',    # CFO group - blue
        2: 'rgb(44, 160, 44)',      # CIO group - green
        3: 'rgb(214, 39, 40)',      # ECG Framework - red
        4: 'royalblue',             # Woven Supply - royalblue
        5: 'mediumseagreen',        # Commune Connect - medium sea green
        6: 'darkorchid'             # Synergyze Hub - dark orchid
    }
    
    # Create a trace for each group
    for group in range(1, 7):
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in G.nodes():
            if G.nodes[node]['group'] == group:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                node_size.append(G.nodes[node]['size'])
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            marker=dict(
                color=group_colors[group],
                size=node_size,
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name=f"Group {group}"
        )
        
        node_traces.append(node_trace)
    
    # Create figure
    fig = go.Figure(
        data=edge_trace + node_traces,
        layout=go.Layout(
            title="CFO-CIO Joint Oversight via Enterprise Capability Governance (ECG) Framework",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            plot_bgcolor='rgba(248,248,248,1)'
        )
    )
    
    # Display the network visualization
    st.plotly_chart(fig, use_container_width=True)
    
    # Governance model explanation
    st.subheader("ECG Governance Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Financial Governance (CFO)
        
        The CFO contributes to the ECG framework through:
        
        - **Budget Allocation & Oversight**
          *Ensuring appropriate financial resources*
          
        - **Value Realization Tracking**
          *Measuring return on license investments*
          
        - **Cost Optimization**
          *Right-sizing license expenditures*
          
        - **Financial Compliance**
          *Ensuring proper financial controls*
        """)
        
    with col2:
        st.markdown("""
        ### Technology Governance (CIO)
        
        The CIO contributes to the ECG framework through:
        
        - **Technical Implementation**
          *Ensuring proper system configuration*
          
        - **Security & Access Control**
          *Protecting sensitive data*
          
        - **Integration Management**
          *Connecting systems appropriately*
          
        - **Performance Optimization**
          *Ensuring system responsiveness*
        """)
    
    # Joint decision framework
    st.markdown("""
    ### Joint Decision Framework
    
    The CFO and CIO collaborate through structured processes:
    
    1. **License Acquisition & Renewal**
       - CFO: Budget approval, cost justification
       - CIO: Technical requirements, implementation planning
    
    2. **Module Activation & Deployment**
       - CFO: Cost allocation, ROI expectations
       - CIO: Resource allocation, integration planning
    
    3. **Usage Policy Development**
       - CFO: Cost management policies
       - CIO: Usage monitoring, technical controls
    
    4. **Governance Review Cycles**
       - Regular joint reviews of license utilization, costs, and performance
       - Coordinated decision-making for upgrades and changes
    """)