import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from PIL import Image
import io
import base64

def show_voi_jeans_demo():
    """Display a demo focused on Voi Jeans and their departmental structure"""
    
    st.title("🧥 Voi Jeans Organization & Synergyze Implementation")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🏢 Organizational Structure", "🔄 Department Workflows", "📊 Integration Demo"])
    
    with tab1:
        show_org_structure()
    
    with tab2:
        show_department_workflows()
    
    with tab3:
        show_integration_demo()

def show_org_structure():
    """Show Voi Jeans organizational structure and how it maps to Synergyze"""
    
    st.subheader("Voi Jeans Organizational Structure")
    
    st.markdown("""
    Voi Jeans Retail India Pvt Ltd operates with a unique organizational structure that leverages 
    Scotts Garments as their CMP (Cut, Make, Pack) manufacturing partner. The Synergyze platform 
    connects these entities through specialized modules for each department.
    """)
    
    # Organization chart using Plotly
    org_chart_data = {
        'id': [
            'CEO', 
            'Head of Design', 'Head of Manufacturing', 'Head of Retail', 'Head of Finance', 'Head of Marketing',
            'Design Team', 'Product Development', 'QA Team',
            'Scotts Garments', 'Production Planning', 'Material Procurement',
            'Store Operations', 'E-commerce', 'Inventory Management',
            'Financial Planning', 'Accounts', 'Audit',
            'Digital Marketing', 'Brand Management', 'Customer Relations'
        ],
        'parent': [
            '',
            'CEO', 'CEO', 'CEO', 'CEO', 'CEO',
            'Head of Design', 'Head of Design', 'Head of Design',
            'Head of Manufacturing', 'Head of Manufacturing', 'Head of Manufacturing',
            'Head of Retail', 'Head of Retail', 'Head of Retail',
            'Head of Finance', 'Head of Finance', 'Head of Finance',
            'Head of Marketing', 'Head of Marketing', 'Head of Marketing'
        ],
        'value': [50, 10, 10, 10, 10, 10, 3, 3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4],
        'label': [
            'CEO', 
            'Head of Design', 'Head of Manufacturing', 'Head of Retail', 'Head of Finance', 'Head of Marketing',
            'Design Team', 'Product Development', 'QA Team',
            'Scotts Garments', 'Production Planning', 'Material Procurement',
            'Store Operations', 'E-commerce', 'Inventory Management',
            'Financial Planning', 'Accounts', 'Audit',
            'Digital Marketing', 'Brand Management', 'Customer Relations'
        ],
        'module': [
            'Synergyze Hub',
            'Woven Supply', 'Woven Supply', 'Commune Connect', 'Synergyze Hub', 'Commune Connect',
            'Woven Supply', 'Woven Supply', 'Woven Supply',
            'Woven Supply', 'Woven Supply', 'Woven Supply',
            'Commune Connect', 'Commune Connect', 'Commune Connect',
            'Synergyze Hub', 'Synergyze Hub', 'Synergyze Hub',
            'Commune Connect', 'Commune Connect', 'Commune Connect'
        ]
    }
    
    # Create a color map
    color_map = {
        'Woven Supply': 'royalblue',
        'Commune Connect': 'mediumseagreen',
        'Synergyze Hub': 'darkorchid'
    }
    
    # Map colors
    colors = [color_map[module] for module in org_chart_data['module']]
    
    # Create sunburst chart
    fig = px.sunburst(
        org_chart_data,
        ids='id',
        parents='parent',
        values='value',
        names='label',
        color='module',
        color_discrete_map=color_map,
        title="Voi Jeans Organization Structure with Synergyze Module Mapping",
        height=700
    )
    
    fig.update_layout(margin=dict(t=60, l=25, r=25, b=25))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Department breakdown with Synergyze mapping
    st.subheader("Department Breakdown with Synergyze Module Mapping")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏭 Woven Supply Departments
        **Manufacturing Side**
        
        - **Design Team**  
          *SS25 collection design, tech packs*
        
        - **Product Development**  
          *Prototyping, material testing*
        
        - **QA Team**  
          *Quality standards, inspections*
        
        - **Scotts Garments**  
          *CMP manufacturing partner*
        
        - **Production Planning**  
          *Scheduling, capacity management*
        
        - **Material Procurement**  
          *Sourcing, vendor management*
        """)
    
    with col2:
        st.markdown("""
        ### 🏬 Commune Connect Departments
        **Retail Side**
        
        - **Store Operations**  
          *20 retail stores management*
        
        - **E-commerce**  
          *Online store, digital sales*
        
        - **Inventory Management**  
          *Stock allocation, replenishment*
        
        - **Digital Marketing**  
          *Social media, SEO, SEM*
        
        - **Brand Management**  
          *Brand identity, campaigns*
        
        - **Customer Relations**  
          *Loyalty program, service*
        """)
    
    with col3:
        st.markdown("""
        ### ⚙️ Synergyze Hub Departments
        **Governance Layer**
        
        - **CEO Office**  
          *Executive dashboard, strategic KPIs*
        
        - **Financial Planning**  
          *Budgeting, forecasting*
        
        - **Accounts**  
          *Payments, receivables*
        
        - **Audit**  
          *Compliance, reporting*
        
        - **IT Services**  
          *System maintenance, security*
        
        - **HR Department**  
          *Recruitment, training, payroll*
        """)

def show_department_workflows():
    """Show department workflows with interactive elements"""
    
    st.subheader("Voi Jeans Department Workflows")
    
    st.markdown("""
    Each department at Voi Jeans follows specific workflows optimized by the Synergyze platform.
    Below are the key workflows for major departments, highlighting how information and processes flow.
    """)
    
    # Create expandable sections for each department's workflow
    
    with st.expander("🧵 Design to Manufacturing Workflow", expanded=True):
        st.markdown("""
        ### Design to Manufacturing Process
        
        1. **Design Conceptualization** (Design Team)
           - Trend research and market analysis
           - Creation of mood boards and design concepts
           - Synergyze Integration: Real-time trend data and historical performance metrics
        
        2. **Sample Development** (Product Development)
           - Creation of prototypes and samples
           - Material selection and testing
           - Synergyze Integration: Digital tech pack creation and version control
        
        3. **Tech Pack Generation** (Design Team)
           - Detailed specifications for production
           - Size charts and grading
           - Synergyze Integration: Automated spec sheet generation with production requirements
        
        4. **Production Order Creation** (Production Planning)
           - Style-wise order creation with quantities
           - Timeline establishment
           - Synergyze Integration: Capacity planning and automatic timeline suggestions
        
        5. **Manufacturing at Scotts Garments** (CMP Partner)
           - Cutting, Making, Packing operations
           - Quality checks and approvals
           - Synergyze Integration: Real-time production tracking and quality reporting
        
        6. **Final QA and Dispatch** (QA Team)
           - Final quality inspection
           - Packaging verification
           - Synergyze Integration: Automated quality reports with defect tracking
        """)
        
        # Create a basic workflow diagram
        nodes = ["Design", "Product Development", "Tech Pack", "Production Order", "Manufacturing", "QA & Dispatch"]
        edges = [(0,1), (1,2), (2,3), (3,4), (4,5)]
        
        G = nx.DiGraph()
        for i, node in enumerate(nodes):
            G.add_node(i, name=node)
        G.add_edges_from(edges)
        
        pos = {i: (i, 0) for i in range(len(nodes))}
        
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
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        
        for node, attr in G.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(attr['name'])
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            marker=dict(
                size=30,
                color='royalblue',
                line=dict(width=2, color='DarkSlateGrey')),
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title="Design to Manufacturing Workflow",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=300,
                        plot_bgcolor='rgba(248,248,248,1)'
                    ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("🏬 Retail Distribution Workflow"):
        st.markdown("""
        ### Retail Distribution Process
        
        1. **Inventory Planning** (Inventory Management)
           - Forecasting and demand planning
           - Store-wise allocation planning
           - Synergyze Integration: AI-driven sales forecasting by store and style
        
        2. **Warehouse Operations** (Inventory Management)
           - Receiving finished goods from Scotts Garments
           - Quality verification and storage
           - Synergyze Integration: Automated receiving and put-away tracking
        
        3. **Store Allocation** (Store Operations)
           - Style and size distribution to 20 stores
           - E-commerce stock allocation
           - Synergyze Integration: Algorithm-based allocation optimization by store performance
        
        4. **Store Merchandising** (Store Operations)
           - Visual merchandising guidelines
           - In-store product placement
           - Synergyze Integration: Planogram compliance tracking and best practices sharing
        
        5. **Sales Operations** (Store Operations)
           - Daily sales tracking vs targets
           - Promotion management
           - Synergyze Integration: Real-time sales dashboards and alerts
        
        6. **Replenishment** (Inventory Management)
           - Stock level monitoring
           - Inter-store transfers
           - Synergyze Integration: Automated replenishment suggestions and transfer orders
        """)
        
        # Create a basic workflow diagram for retail
        retail_nodes = ["Inventory Planning", "Warehouse", "Store Allocation", "Store Merchandising", "Sales", "Replenishment"]
        retail_edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,1)]
        
        G_retail = nx.DiGraph()
        for i, node in enumerate(retail_nodes):
            G_retail.add_node(i, name=node)
        G_retail.add_edges_from(retail_edges)
        
        # Position nodes in a circle
        pos_retail = nx.circular_layout(G_retail)
        
        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G_retail.edges():
            x0, y0 = pos_retail[edge[0]]
            x1, y1 = pos_retail[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        
        for node, attr in G_retail.nodes(data=True):
            x, y = pos_retail[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(attr['name'])
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            marker=dict(
                size=30,
                color='mediumseagreen',
                line=dict(width=2, color='DarkSlateGrey')),
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title="Retail Distribution Workflow",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=400,
                        plot_bgcolor='rgba(248,248,248,1)'
                    ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💰 Finance and Governance Workflow"):
        st.markdown("""
        ### Finance and Governance Process
        
        1. **Financial Planning** (Finance Department)
           - Budget creation and allocation
           - Capital expenditure planning
           - Synergyze Integration: Automated budget vs actual tracking
        
        2. **Procurement Management** (Finance Department)
           - Vendor payment processing
           - CMP cost management with Scotts Garments
           - Synergyze Integration: Vendor performance metrics and payment scheduling
        
        3. **Sales Reconciliation** (Finance Department)
           - Daily sales reconciliation
           - Store-wise performance analysis
           - Synergyze Integration: Automated sales reconciliation and exception flagging
        
        4. **Cost Analysis** (Finance Department)
           - Product costing and margin analysis
           - Profitability reporting
           - Synergyze Integration: Style-wise profitability dashboards with drill-down capability
        
        5. **Compliance Management** (Audit Team)
           - Statutory compliance tracking
           - Internal policy adherence
           - Synergyze Integration: Compliance calendar with automated alerts and documentation
        
        6. **Performance Reporting** (CEO Office)
           - Executive dashboards
           - KPI tracking
           - Synergyze Integration: Real-time performance metrics with predictive analytics
        """)
        
        # Create a hierarchical diagram for finance
        finance_data = {
            'id': [
                'Financial Governance', 
                'Planning', 'Operations', 'Reporting',
                'Budgeting', 'Forecasting',
                'Procurement', 'Payments', 'Reconciliation',
                'Performance', 'Compliance', 'Executive'
            ],
            'parent': [
                '', 
                'Financial Governance', 'Financial Governance', 'Financial Governance',
                'Planning', 'Planning',
                'Operations', 'Operations', 'Operations',
                'Reporting', 'Reporting', 'Reporting'
            ],
            'value': [50, 20, 20, 20, 10, 10, 7, 7, 6, 7, 7, 6]
        }
        
        # Create treemap
        fig = px.treemap(
            finance_data,
            ids='id',
            parents='parent',
            values='value',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            title="Finance and Governance Structure"
        )
        
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_integration_demo():
    """Show integration between departments and data flow"""
    
    st.subheader("Voi Jeans Integration Demonstration")
    
    st.markdown("""
    ### Cross-Departmental Integration via Synergyze
    
    The true power of the Synergyze platform is in how it connects all departments and external partners
    within the Voi Jeans ecosystem. This demonstration shows the data flow and integration points.
    """)
    
    # Create a network graph showing integration
    G = nx.DiGraph()
    
    # Define nodes with their groups
    nodes = [
        ("Design", 1), ("Production Planning", 1), ("Scotts Garments", 1), 
        ("Inventory Management", 2), ("Store Operations", 2), ("E-commerce", 2),
        ("Finance", 3), ("CEO Dashboard", 3)
    ]
    
    # Add nodes
    for name, group in nodes:
        G.add_node(name, group=group)
    
    # Define edges with weights
    edges = [
        ("Design", "Production Planning", 5),
        ("Production Planning", "Scotts Garments", 7),
        ("Scotts Garments", "Inventory Management", 6),
        ("Inventory Management", "Store Operations", 8),
        ("Inventory Management", "E-commerce", 5),
        ("Store Operations", "Finance", 4),
        ("E-commerce", "Finance", 4),
        ("Finance", "CEO Dashboard", 3),
        ("CEO Dashboard", "Design", 2),
        ("Store Operations", "Design", 3),
        ("E-commerce", "Design", 3)
    ]
    
    # Add edges
    for source, target, weight in edges:
        G.add_edge(source, target, weight=weight)
    
    # Create positions
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(f"Data flow: {edge[0]} to {edge[1]}")
    
    # Create different node traces for different groups
    node_traces = []
    colors = ['royalblue', 'mediumseagreen', 'darkorchid']
    groups = {}
    
    for name, group in nodes:
        if group not in groups:
            groups[group] = {
                'x': [],
                'y': [],
                'text': [],
                'color': colors[group-1]
            }
        x, y = pos[name]
        groups[group]['x'].append(x)
        groups[group]['y'].append(y)
        groups[group]['text'].append(name)
    
    # Create a trace for each group
    for group_id, group_data in groups.items():
        node_trace = go.Scatter(
            x=group_data['x'],
            y=group_data['y'],
            text=group_data['text'],
            mode='markers+text',
            textposition="top center",
            marker=dict(
                size=30,
                color=group_data['color'],
                line=dict(width=2, color='DarkSlateGrey')),
            name=f"Group {group_id}"
        )
        node_traces.append(node_trace)
    
    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )
    
    # Create figure with all traces
    fig = go.Figure(data=[edge_trace] + node_traces,
                 layout=go.Layout(
                    title="Voi Jeans Integration Map - Data Flow Between Departments",
                    showlegend=True,
                    legend=dict(
                        title="Department Groups",
                        x=0,
                        y=1,
                        traceorder="normal",
                        itemsizing="constant"
                    ),
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    height=600,
                    plot_bgcolor='rgba(248,248,248,1)'
                ))
    
    # Update node trace legends
    fig.data[1].name = "Woven Supply (Manufacturing)"
    fig.data[2].name = "Commune Connect (Retail)"
    fig.data[3].name = "Synergyze Hub (Governance)"
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show key integration examples
    st.subheader("Key Integration Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Design to Sales Feedback Loop
        
        1. **Sales Performance Data** collected from all 20 Voi Jeans stores
        2. **Style-wise Analysis** processed through Synergyze Hub
        3. **Performance Insights** shared with Design team
        4. **Design Adjustments** made for future collections
        5. **Production Planning** updated based on sales trends
        
        *Synergyze enables real-time data flow from retail stores back to design, 
        creating a closed feedback loop that optimizes product development.*
        """)
    
    with col2:
        st.markdown("""
        ### 💼 Scotts Garments CMP Integration
        
        1. **Production Orders** sent to Scotts Garments via Synergyze
        2. **Material Procurement** tracked in shared platform
        3. **Production Progress** updated daily by factory team
        4. **Quality Metrics** reported in real-time
        5. **Shipping Information** integrated with Voi Jeans inventory
        
        *The CMP (Cut, Make, Pack) relationship with Scotts Garments is fully
        digitized through Synergyze, providing transparency and efficiency.*
        """)
    
    # Demo data flow visualization
    st.subheader("Real-time Data Flow Visualization")
    
    # Create sample data for demonstration
    dates = pd.date_range(start='2025-01-01', periods=90, freq='D')
    
    # Generate sample design approval data (increasing and then plateau)
    design_data = np.cumsum(np.random.normal(3, 1, size=90))
    design_data = np.clip(design_data, 0, 100)
    
    # Generate sample production data (follows design with delay)
    production_data = np.concatenate([np.zeros(10), design_data[:-10]])
    
    # Generate sample shipping data (follows production with delay)
    shipping_data = np.concatenate([np.zeros(20), production_data[:-20]])
    
    # Generate sample sales data (follows shipping with delay)
    sales_data = np.concatenate([np.zeros(30), shipping_data[:-30]])
    
    # Create DataFrame
    flow_data = pd.DataFrame({
        'Date': dates,
        'Design Approvals': design_data,
        'Production Completion': production_data,
        'Store Inventory': shipping_data,
        'Sales': sales_data
    })
    
    # Create line chart
    fig = px.line(
        flow_data, 
        x='Date', 
        y=['Design Approvals', 'Production Completion', 'Store Inventory', 'Sales'],
        title='SS25 Collection - Data Flow Timeline',
        labels={'value': 'Cumulative Units', 'variable': 'Process Stage'},
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Units",
        legend_title="Process Stage",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    This visualization demonstrates how Synergyze enables end-to-end visibility of the product lifecycle. 
    From design approval through production at Scotts Garments to inventory receipt at Voi Jeans stores 
    and finally to sales, all data is connected in a unified platform with appropriate time lags between stages.
    """)

if __name__ == "__main__":
    show_voi_jeans_demo()