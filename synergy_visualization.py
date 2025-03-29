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
        st.session_state.has_empire_license = False
    
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
    
    st.subheader("Synergyze Ecosystem Structure")
    
    st.markdown("""
    The Synergyze platform consists of three core components, each tailored to specific business needs:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏭 Woven Supply
        **Manufacturing Side**
        
        - Raw Material Procurement
        - Vendor Management
        - Production Planning
        - Quality Control
        - Factory Operations
        - Material Tracking
        
        *Streamlines the supply chain from sourcing to production*
        """)
    
    with col2:
        st.markdown("""
        ### 🏬 Commune Connect
        **Retail Side**
        
        - Store Management
        - Product Catalog
        - Inventory Control
        - Sales Tracking
        - Customer Engagement
        - E-commerce Integration
        
        *Connects retail operations with customer-facing channels*
        """)
    
    with col3:
        st.markdown("""
        ### ⚙️ Synergyze Hub
        **Governance Layer**
        
        - License Management
        - Role-Based Access
        - Data Integration
        - Analytics & Reporting
        - Compliance Management
        - Performance Monitoring
        
        *Centralized governance and controls for the entire ecosystem*
        """)
    
    # Architectural diagram using Plotly
    st.subheader("Architectural Relationship")
    
    # Create the architecture diagram
    fig = go.Figure()
    
    # Add rectangle shapes for the boxes
    fig.add_shape(type="rect", x0=0.05, y0=0.6, x1=0.45, y1=0.9,
                  line=dict(color="RoyalBlue", width=2),
                  fillcolor="LightSkyBlue", opacity=0.7)
    
    fig.add_shape(type="rect", x0=0.55, y0=0.6, x1=0.95, y1=0.9,
                  line=dict(color="MediumSeaGreen", width=2),
                  fillcolor="LightGreen", opacity=0.7)
    
    fig.add_shape(type="rect", x0=0.3, y0=0.1, x1=0.7, y1=0.4,
                  line=dict(color="DarkOrchid", width=2),
                  fillcolor="Plum", opacity=0.7)
    
    # Add arrows connecting the boxes
    fig.add_annotation(x=0.25, y=0.55, ax=0.25, ay=0.45,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2, arrowcolor="gray")
    
    fig.add_annotation(x=0.75, y=0.55, ax=0.75, ay=0.45,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2, arrowcolor="gray")
    
    fig.add_annotation(x=0.5, y=0.65, ax=0.5, ay=0.35,
                       xref="paper", yref="paper", axref="paper", ayref="paper",
                       showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2, arrowcolor="gray")
    
    # Add text for the boxes
    fig.add_annotation(x=0.25, y=0.75, text="Woven Supply<br>(Manufacturing)",
                       font=dict(size=14, color="black", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    fig.add_annotation(x=0.75, y=0.75, text="Commune Connect<br>(Retail)",
                       font=dict(size=14, color="black", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    fig.add_annotation(x=0.5, y=0.25, text="Synergyze Hub<br>(Governance)",
                       font=dict(size=14, color="black", family="Arial"),
                       showarrow=False, xref="paper", yref="paper")
    
    # Update layout
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="white",
        showlegend=False,
        title="Synergyze System Architecture"
    )
    
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
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
    
    st.subheader("Network Visualization")
    
    st.markdown("""
    This interactive network visualization displays the relationships between different departments, 
    entities, and stakeholders in the Synergyze ecosystem.
    
    - **Woven Supply (Blue)**: Manufacturing side including suppliers, factories, and raw material providers
    - **Commune Connect (Green)**: Retail side including stores, consumers, and distribution channels
    - **Synergyze Hub (Purple)**: Governance layer connecting and orchestrating the entire ecosystem
    """)
    
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
    
    st.subheader("Synergyze License Management")
    
    st.markdown("""
    ECG provides each company with a customized Synergyze license based on their specific needs. 
    This license system determines what modules, features, and capabilities are available to each entity 
    within the ecosystem.
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
    
    # Create a sunburst chart for license visualization
    labels = [
        "Synergyze", 
        "Woven Supply", "Commune Connect", "Synergyze Hub",
        "Manufacturing", "Material", "Factory", "Logistics",
        "Retail", "E-commerce", "Distribution", "Marketing",
        "Admin", "Finance", "Executive"
    ]
    
    parents = [
        "", 
        "Synergyze", "Synergyze", "Synergyze",
        "Woven Supply", "Woven Supply", "Woven Supply", "Woven Supply",
        "Commune Connect", "Commune Connect", "Commune Connect", "Commune Connect",
        "Synergyze Hub", "Synergyze Hub", "Synergyze Hub"
    ]
    
    values = [100, 30, 30, 40, 10, 5, 10, 5, 10, 5, 10, 5, 10, 15, 15]
    
    fig = px.sunburst(
        names=labels,
        parents=parents,
        values=values,
        title="Voi Jeans License Structure - Module Distribution",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_layout(margin=dict(t=60, l=0, r=0, b=0), height=600)
    
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
    
    st.subheader("⚙️ Empire OS Governance")
    
    st.markdown("""
    Empire OS provides the governance and compliance layer for the entire Synergyze ecosystem.
    As a license holder with signed data sharing agreements, you have access to this protected section.
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