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
    
def show_ceo_direct_advisory(enable_secret_view):
    """Show the direct advisory channel from CFO/CIO to CEO with secret license perspectives"""
    
    if not enable_secret_view:
        st.subheader("Executive Dashboard")
        st.info("Enable the 'Executive Advisory Channel' toggle at the top of the page to view the private CEO advisory channel.")
        
        # Show standard executive dashboard
        st.markdown("""
        ### Standard Executive Dashboard
        
        This dashboard provides an overview of key metrics and performance indicators 
        tracked through the standard ECG framework. It shows the consolidated view of
        license management across all business units.
        """)
        
        # Create sample metrics for demonstration
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("License Utilization", "78%", "+2%")
        with col2:
            st.metric("Cost per User", "₹1,240", "-₹120")
        with col3:
            st.metric("Active Modules", "14/20", "+2")
        with col4:
            st.metric("Compliance Score", "94%", "+5%")
            
        # Create sample charts
        st.subheader("License Utilization by Department")
        
        # Sample data for department license utilization
        dept_util = pd.DataFrame({
            'Department': ['Design', 'Manufacturing', 'Retail', 'Finance', 'Marketing', 'IT'],
            'Utilization': [85, 92, 76, 65, 72, 88],
            'Allocation': [90, 95, 85, 70, 80, 90]
        })
        
        fig = px.bar(dept_util, x='Department', y=['Utilization', 'Allocation'],
                     title="License Utilization vs Allocation by Department",
                     barmode='group', height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        return
    
    # Show the secret advisory panel when enabled
    st.subheader("🔒 CEO Direct Advisory Channel")
    st.markdown("""
    <div style='background-color: rgba(255,200,0,0.1); padding: 15px; border-radius: 5px; border-left: 5px solid gold;'>
    <h3 style='color: #B8860B;'>Private Executive Advisory Channel</h3>
    <p>This secure channel provides direct, unfiltered advice from the CFO and CIO directly to the CEO, 
    bypassing normal organizational visibility. It allows executives to share sensitive insights 
    that might be politically difficult to communicate through normal channels.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Secret license advice tabs
    cfo_tab, cio_tab, joint_tab = st.tabs(["CFO Secret License", "CIO Secret License", "Joint Advisory"])
    
    with cfo_tab:
        st.subheader("CFO to CEO: Financial Risk Assessment")
        
        st.markdown("""
        ### 🔒 Confidential Financial Perspective

        **Current License Structure Financial Analysis:**
        
        Dear CEO,
        
        Here's my unfiltered financial assessment of our current license structure that I can share directly with you:
        
        * **Cost Optimization Opportunity**: We're currently over-licensed by approximately 22% in the retail division. 
          This represents a ₹1.8M annual cost that could be reallocated.
          
        * **Hidden Cost Exposure**: The Manufacturing module licenses don't account for seasonal scaling.
          We're paying for peak capacity year-round, creating a 15% premium we could eliminate.
          
        * **License ROI Concerns**: The advanced analytics modules show only 40% utilization despite full 
          deployment costs. Consider phased rollout for future modules instead.
          
        * **Competitive Advantage**: Our competitors are using a tiered license model that creates lower per-user 
          costs. We should renegotiate our enterprise agreement with similar terms.
          
        I'm available to discuss these insights privately at your convenience.
        
        — CFO
        """)
        
        # ROI Analysis visualization
        st.subheader("🔒 Module ROI Analysis (Confidential)")
        
        # Sample data for module ROI visualization
        module_roi = pd.DataFrame({
            'Module': ['Basic ERP', 'Advanced Analytics', 'Mobile Access', 'Inventory Tracking', 
                      'Supply Chain', 'Customer Portal', 'Integration Layer'],
            'Implementation Cost': [600, 420, 180, 250, 380, 210, 320],
            'Annual Value': [950, 175, 240, 380, 410, 130, 290],
            'Type': ['Essential', 'Premium', 'Add-on', 'Essential', 'Premium', 'Add-on', 'Essential']
        })
        
        module_roi['ROI'] = (module_roi['Annual Value'] - module_roi['Implementation Cost']) / module_roi['Implementation Cost'] * 100
        
        fig = px.scatter(module_roi, x='Implementation Cost', y='Annual Value', size='Implementation Cost',
                        color='Type', hover_name='Module', size_max=50,
                        labels={'Implementation Cost': 'Implementation Cost (₹000s)', 
                                'Annual Value': 'Annual Value Generated (₹000s)'},
                        title="License Module ROI Analysis - Confidential CFO Assessment")
        
        # Add ROI reference line (45-degree line where ROI = 0%)
        max_val = max(module_roi['Implementation Cost'].max(), module_roi['Annual Value'].max())
        fig.add_shape(type="line", line=dict(dash="dash", width=1, color="gray"),
                     x0=0, y0=0, x1=max_val, y1=max_val)
        
        fig.update_layout(annotations=[
            dict(x=420, y=175, text="Potential Cut", showarrow=True, arrowhead=1, ax=40, ay=-40),
            dict(x=600, y=950, text="Strong Performer", showarrow=True, arrowhead=1, ax=0, ay=-40)
        ])
        
        st.plotly_chart(fig, use_container_width=True)
    
    with cio_tab:
        st.subheader("CIO to CEO: Technical Risk Assessment")
        
        st.markdown("""
        ### 🔒 Confidential Technical Perspective

        **Current License Structure Technical Analysis:**
        
        Dear CEO,
        
        I wanted to share these direct technical insights about our current license implementation:
        
        * **Security Vulnerability**: Our current license deployment has an undocumented API access point 
          that could potentially expose customer data. I need your approval to restrict this immediately.
          
        * **Technical Debt Accumulation**: The current vendor release cycle is forcing us to maintain 
          legacy interfaces that are increasing our maintenance overhead by 30%.
          
        * **Scaling Limitation**: Our license tier restricts database connections, which will become a 
          bottleneck when we expand to the North region next quarter.
          
        * **Integration Risk**: The lack of data federation capabilities in our current license tier may 
          cause data integrity issues when we connect to the new supply chain platform.
          
        I can provide more details in our next one-on-one meeting.
        
        — CIO
        """)
        
        # Security Risk visualization
        st.subheader("🔒 Technical Risk Assessment (Confidential)")
        
        # Sample data for risk assessment
        risk_data = pd.DataFrame({
            'Risk Area': ['Data Security', 'Scalability', 'Integration', 'Performance', 'Vendor Lock-in', 'Compliance'],
            'Impact': [8, 7, 6, 5, 7, 9],
            'Probability': [6, 8, 7, 4, 9, 5],
            'Mitigation Cost': [120, 80, 60, 40, 150, 90],
            'Category': ['Security', 'Infrastructure', 'Data', 'Infrastructure', 'License', 'Security']
        })
        
        risk_data['Risk Score'] = risk_data['Impact'] * risk_data['Probability'] / 10
        
        fig = px.scatter(risk_data, x='Probability', y='Impact', size='Mitigation Cost',
                        color='Category', hover_name='Risk Area', size_max=50,
                        labels={'Probability': 'Probability (1-10)', 'Impact': 'Impact (1-10)'},
                        title="License Technical Risk Assessment - Confidential CIO Analysis")
        
        # Add risk zones
        fig.add_shape(type="rect", x0=0, y0=0, x1=3.3, y1=3.3,
                    line=dict(color="Green"), fillcolor="rgba(0,255,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=3.3, y0=0, x1=6.6, y1=3.3,
                    line=dict(color="Yellow"), fillcolor="rgba(255,255,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=6.6, y0=0, x1=10, y1=3.3,
                    line=dict(color="Orange"), fillcolor="rgba(255,165,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=0, y0=3.3, x1=3.3, y1=6.6,
                    line=dict(color="Yellow"), fillcolor="rgba(255,255,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=3.3, y0=3.3, x1=6.6, y1=6.6,
                    line=dict(color="Orange"), fillcolor="rgba(255,165,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=6.6, y0=3.3, x1=10, y1=6.6,
                    line=dict(color="Red"), fillcolor="rgba(255,0,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=0, y0=6.6, x1=3.3, y1=10,
                    line=dict(color="Orange"), fillcolor="rgba(255,165,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=3.3, y0=6.6, x1=6.6, y1=10,
                    line=dict(color="Red"), fillcolor="rgba(255,0,0,0.1)", opacity=0.3)
        fig.add_shape(type="rect", x0=6.6, y0=6.6, x1=10, y1=10,
                    line=dict(color="DarkRed"), fillcolor="rgba(139,0,0,0.1)", opacity=0.3)
        
        # Add annotations for high-risk items
        fig.update_layout(annotations=[
            dict(x=6, y=8, text="Data Security Risk", showarrow=True, arrowhead=1, ax=40, ay=-40),
            dict(x=9, y=7, text="Vendor Lock-in Risk", showarrow=True, arrowhead=1, ax=-40, ay=20)
        ])
        
        st.plotly_chart(fig, use_container_width=True)
    
    with joint_tab:
        st.subheader("Joint CFO-CIO Executive Advisory")
        
        st.markdown("""
        ### 🔒 Confidential Joint Advisory

        **Strategic License Recommendations:**
        
        Dear CEO,
        
        After consulting privately, we've identified these key license strategy recommendations 
        that require your direct attention:
        
        1. **License Restructuring Opportunity** *(CFO & CIO)*:  
           We've identified a way to consolidate our license structure that will save approximately ₹3.2M 
           annually while expanding technical capabilities. This would require renegotiating our current 
           enterprise agreement in the next 60 days.

        2. **Competitive Intelligence Alert** *(CFO)*:  
           Our competitors are moving to consumption-based license models that could give them a 15-20% 
           cost advantage. We should consider this model for our next renewal.

        3. **Technical Architecture Risk** *(CIO)*:  
           Our current license structure enforces an architecture that won't support our three-year growth 
           plan. We need to either upgrade our license tier or explore alternative vendors.

        4. **Internal Political Challenge** *(CFO & CIO)*:  
           The proposed license optimization will face resistance from the retail division as it would 
           reduce their apparent budget allocation. We need your direct support to implement this change.
        
        We're available to discuss these issues in a closed session at your convenience.
        
        — CFO & CIO
        """)
        
        # Decision matrix visualization
        st.subheader("🔒 Executive Decision Matrix (Confidential)")
        
        # Create sample decision matrix data
        decision_data = pd.DataFrame({
            'Option': ['Status Quo', 'Tier Upgrade', 'Vendor Switch', 'Hybrid Model', 'Consumption Model'],
            'Financial Impact': [0, -800, -200, 700, 1200],
            'Technical Value': [3, 8, 7, 6, 9],
            'Implementation Risk': [1, 5, 9, 6, 7],
            'Time to Value': [0, 6, 12, 3, 4]
        })
        
        # Normalize Technical Value to same scale as Financial Impact for visualization
        max_abs_financial = max(abs(decision_data['Financial Impact'].min()), abs(decision_data['Financial Impact'].max()))
        decision_data['Technical Value Scaled'] = decision_data['Technical Value'] * max_abs_financial / 10
        
        # Create figure with secondary y-axis
        fig = go.Figure()
        
        # Add bars for financial impact
        fig.add_trace(go.Bar(
            x=decision_data['Option'],
            y=decision_data['Financial Impact'],
            name='Financial Impact (₹000s)',
            marker_color='blue',
            opacity=0.7
        ))
        
        # Add bars for technical value
        fig.add_trace(go.Bar(
            x=decision_data['Option'],
            y=decision_data['Technical Value Scaled'],
            name='Technical Value (Scaled)',
            marker_color='green',
            opacity=0.7
        ))
        
        # Create bubble chart overlay for risk and time
        fig.add_trace(go.Scatter(
            x=decision_data['Option'],
            y=[max_abs_financial * 0.7] * len(decision_data),  # Position bubbles above bars
            mode='markers',
            marker=dict(
                size=decision_data['Implementation Risk'] * 5,
                color=decision_data['Time to Value'],
                colorscale='Viridis',
                colorbar=dict(title='Months to Value'),
                showscale=True,
                opacity=0.7,
                line=dict(width=1, color='black')
            ),
            name='Risk & Time',
            text=['Risk: ' + str(r) + ', Time: ' + str(t) + ' months' 
                  for r, t in zip(decision_data['Implementation Risk'], decision_data['Time to Value'])],
            hoverinfo='text'
        ))
        
        # Update layout
        fig.update_layout(
            title='License Strategy Decision Matrix - Confidential Joint Analysis',
            xaxis=dict(title='Strategic Options'),
            yaxis=dict(title='Financial Impact (₹000s)'),
            barmode='group',
            legend=dict(x=0.01, y=0.99),
            annotations=[
                dict(x='Consumption Model', y=1500, text='Recommended', showarrow=True, 
                     arrowhead=1, ax=0, ay=-40, font=dict(size=14, color='red'))
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add call to action
        st.markdown("""
        ### 🔒 Recommended Next Steps
        
        1. **Schedule a closed executive session** to discuss these confidential recommendations
        2. **Authorize preliminary license assessment** by trusted external consultant
        3. **Establish official mandate** from CEO office for license optimization initiative
        4. **Create communication plan** for managing internal political considerations
        """)

        st.info("This confidential advisory channel provides insights that may not be appropriate for broader organizational visibility. The recommendations here represent the unfiltered perspectives of your executive leadership team.")