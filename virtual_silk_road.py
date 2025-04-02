import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io
import base64

def show_virtual_silk_road():
    """Display the Virtual Silk Road visualization - Emperor's view of the entire ecosystem"""
    
    st.title("🏙️ The Virtual Silk Road")
    
    st.markdown("""
    <div style="background-color: rgba(123, 104, 238, 0.1); padding: 20px; border-radius: 5px; border-left: 5px solid #7B68EE;">
        <h3 style="color: #7B68EE; margin-top: 0;">Emperor's Digital Twin of the Empire</h3>
        <p>The Virtual Silk Road is a digital representation of the entire ecosystem. It visualizes all entities, 
        data flows, license activities, and governance structures in a unified interface for the Emperor's oversight.</p>
        <p>This view connects with <b>Empire OS</b> to provide real-time insights into the health and operations of 
        the entire enterprise, powered by <b>Synergyze</b> and integrated with external systems through APIs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Integration information
    st.markdown("""
    ### External System Integration
    
    This visualization integrates with the following external systems:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### Empire OS
        [https://empire-os.replit.app/auth](https://empire-os.replit.app/auth)
        
        The central operating system that:
        - Stores all license data
        - Manages user permissions
        - Tracks transactions 
        - Provides governance oversight
        """)
    
    with col2:
        st.markdown("""
        #### Synergyze
        [https://synnergyze.com/](https://synnergyze.com/)
        
        The SAAS platform that provides:
        - Manufacturing modules
        - Retail distribution tools
        - Management dashboards
        - Analytics capabilities
        """)
    
    with col3:
        st.markdown("""
        #### Fashion Renderer
        [https://fashion-renderer-faiz32.replit.app/](https://fashion-renderer-faiz32.replit.app/)
        
        Specialized visualization tool for:
        - Product design rendering
        - Style visualization
        - Material simulation
        - Virtual showrooms
        """)
    
    # The main visualization - Emperor's view of the Virtual Silk Road
    st.markdown("### 🌐 The Empire: A Unified View")
    
    # Create network visualization of the entire ecosystem
    G = nx.Graph()
    
    # Node groups
    # 1: Emperor & Ministers
    # 2: Manufacturing (Woven Supply)
    # 3: Retail (Commune Connect)
    # 4: Management (Synergyze Hub)
    # 5: External Systems
    # 6: Governance Bodies
    
    # Add nodes for the ecosystem
    nodes = [
        # Emperor's governance
        {"id": "Emperor", "group": 1, "size": 40, "desc": "Supreme oversight of the entire empire"},
        {"id": "CFO", "group": 1, "size": 25, "desc": "Financial governance of licenses"},
        {"id": "CIO", "group": 1, "size": 25, "desc": "Technical governance of platforms"},
        {"id": "Marketing Officer", "group": 1, "size": 25, "desc": "License sales and promotion"},
        {"id": "Compliance Minister", "group": 1, "size": 25, "desc": "Regulatory oversight"},
        
        # Manufacturing
        {"id": "Manufacturing Hub", "group": 2, "size": 30, "desc": "Central manufacturing operations"},
        {"id": "CMP Operations", "group": 2, "size": 20, "desc": "Cut, Make, Pack operations"},
        {"id": "Material Library", "group": 2, "size": 20, "desc": "Material database with HSN codes"},
        {"id": "Production Planning", "group": 2, "size": 20, "desc": "Production scheduling system"},
        {"id": "Quality Control", "group": 2, "size": 20, "desc": "Quality assurance system"},
        
        # Retail
        {"id": "Retail Distribution", "group": 3, "size": 30, "desc": "Retail operations management"},
        {"id": "Store Operations", "group": 3, "size": 20, "desc": "Individual store management"},
        {"id": "Marketplace Integration", "group": 3, "size": 20, "desc": "Online marketplace connections"},
        {"id": "Inventory Management", "group": 3, "size": 20, "desc": "Multi-location inventory tracking"},
        {"id": "Customer Analytics", "group": 3, "size": 20, "desc": "Customer behavior analysis"},
        
        # Management Hub
        {"id": "Synergyze Hub", "group": 4, "size": 30, "desc": "Central management platform"},
        {"id": "License Management", "group": 4, "size": 20, "desc": "License administration"},
        {"id": "Data Governance", "group": 4, "size": 20, "desc": "Data sharing agreements"},
        {"id": "Executive Dashboards", "group": 4, "size": 20, "desc": "Executive insights"},
        {"id": "Unified Reporting", "group": 4, "size": 20, "desc": "Cross-platform analytics"},
        
        # External Systems
        {"id": "Empire OS", "group": 5, "size": 25, "desc": "Central operating system"},
        {"id": "Fashion Renderer", "group": 5, "size": 20, "desc": "Product visualization tool"},
        {"id": "HSN Tax System", "group": 5, "size": 20, "desc": "Taxation management"},
        {"id": "API Gateway", "group": 5, "size": 20, "desc": "API management system"},
        
        # Governance bodies
        {"id": "Council of Ministers", "group": 6, "size": 25, "desc": "Advisory group to Emperor"},
        {"id": "Tech Team", "group": 6, "size": 20, "desc": "Technical implementation team"},
        {"id": "Compliance Team", "group": 6, "size": 20, "desc": "Regulatory compliance team"},
        {"id": "Business Development", "group": 6, "size": 20, "desc": "Strategic deployment team"}
    ]
    
    # Add nodes to the graph
    for node in nodes:
        G.add_node(node["id"], group=node["group"], size=node["size"], desc=node["desc"])
    
    # Add edges to connect the ecosystem
    edges = [
        # Emperor connections to ministers
        ("Emperor", "CFO", 8),
        ("Emperor", "CIO", 8),
        ("Emperor", "Marketing Officer", 7),
        ("Emperor", "Compliance Minister", 7),
        ("Emperor", "Council of Ministers", 9),
        
        # Emperor direct oversight
        ("Emperor", "Manufacturing Hub", 6),
        ("Emperor", "Retail Distribution", 6),
        ("Emperor", "Synergyze Hub", 6),
        ("Emperor", "Empire OS", 7),
        
        # Ministers to functional areas
        ("CFO", "License Management", 5),
        ("CIO", "Data Governance", 5),
        ("Marketing Officer", "Business Development", 5),
        ("Compliance Minister", "Compliance Team", 5),
        
        # Council connections
        ("Council of Ministers", "Tech Team", 4),
        ("Council of Ministers", "Compliance Team", 4),
        ("Council of Ministers", "Business Development", 4),
        
        # Core platform connections
        ("Empire OS", "Manufacturing Hub", 5),
        ("Empire OS", "Retail Distribution", 5),
        ("Empire OS", "Synergyze Hub", 5),
        ("Empire OS", "API Gateway", 5),
        
        # Manufacturing connections
        ("Manufacturing Hub", "CMP Operations", 4),
        ("Manufacturing Hub", "Material Library", 4),
        ("Manufacturing Hub", "Production Planning", 4),
        ("Manufacturing Hub", "Quality Control", 4),
        ("Material Library", "HSN Tax System", 3),
        ("CMP Operations", "Fashion Renderer", 3),
        
        # Retail connections
        ("Retail Distribution", "Store Operations", 4),
        ("Retail Distribution", "Marketplace Integration", 4),
        ("Retail Distribution", "Inventory Management", 4),
        ("Retail Distribution", "Customer Analytics", 4),
        ("Store Operations", "Inventory Management", 3),
        
        # Management connections
        ("Synergyze Hub", "License Management", 4),
        ("Synergyze Hub", "Data Governance", 4),
        ("Synergyze Hub", "Executive Dashboards", 4),
        ("Synergyze Hub", "Unified Reporting", 4),
        
        # Cross-functional connections
        ("Inventory Management", "CMP Operations", 2),
        ("Executive Dashboards", "Emperor", 5),
        ("API Gateway", "Fashion Renderer", 3),
        ("API Gateway", "HSN Tax System", 3),
        
        # Governance connections
        ("License Management", "Compliance Team", 3),
        ("Data Governance", "Compliance Team", 3),
    ]
    
    # Add edges to the graph
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    # Create positions using a spring layout
    pos = nx.spring_layout(G, seed=42, k=0.3)
    
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
                line=dict(width=weight/2, color='rgba(128, 128, 128, 0.7)'),
                hoverinfo='none',
                mode='lines'
            )
        )
    
    # Create node traces for different groups
    node_traces = []
    
    # Color map for different groups
    group_colors = {
        1: '#FFD700',           # Emperor & Ministers - gold
        2: '#1E90FF',           # Manufacturing - dodger blue
        3: '#32CD32',           # Retail - lime green
        4: '#9932CC',           # Management Hub - dark orchid
        5: '#FF4500',           # External Systems - orange red
        6: '#4682B4'            # Governance Bodies - steel blue
    }
    
    # Group names for legend
    group_names = {
        1: "Emperor's Council",
        2: "Manufacturing",
        3: "Retail Distribution",
        4: "Management Hub",
        5: "External Systems",
        6: "Governance Bodies"
    }
    
    # Create a trace for each group
    for group in range(1, 7):
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_hover = []
        
        for node in G.nodes():
            if G.nodes[node]['group'] == group:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                node_size.append(G.nodes[node]['size'])
                node_hover.append(f"{node}<br>{G.nodes[node]['desc']}")
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hovertext=node_hover,
            hoverinfo='text',
            marker=dict(
                color=group_colors[group],
                size=node_size,
                line=dict(width=2, color='DarkSlateGrey')
            ),
            name=group_names[group]
        )
        
        node_traces.append(node_trace)
    
    # Create figure
    fig = go.Figure(
        data=edge_trace + node_traces,
        layout=go.Layout(
            title="Emperor's View: The Virtual Silk Road Ecosystem",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=700,
            plot_bgcolor='rgba(248,248,248,1)',
            legend=dict(
                title="Empire Components",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    )
    
    # Display the network visualization
    st.plotly_chart(fig, use_container_width=True)
    
    # HSN Code Integration 
    st.subheader("🔍 HSN Code Integration")
    
    st.markdown("""
    The Virtual Silk Road incorporates HSN (Harmonized System of Nomenclature) code taxation logic throughout 
    the system, particularly in the Material Library where each material and product is tagged with the 
    appropriate HSN code for automated taxation.
    """)
    
    # Sample HSN code mapping for demonstration
    hsn_data = {
        'HSN Code': ['5208', '5209', '5210', '5211', '6103', '6104', '6109', '6203'],
        'Description': [
            'Cotton fabric < 200 g/m²',
            'Cotton fabric > 200 g/m²',
            'Cotton-blend fabric < 200 g/m²',
            'Cotton-blend fabric > 200 g/m²',
            "Men's suits, jackets, trousers",
            "Women's suits, dresses, skirts",
            'T-shirts, singlets, vests',
            "Men's suits, jackets, trousers"
        ],
        'GST Rate': ['5%', '5%', '5%', '5%', '12%', '12%', '5%', '12%'],
        'System Integration': [
            'Material Library', 
            'Material Library', 
            'Material Library', 
            'Material Library',
            'Retail Distribution',
            'Retail Distribution',
            'Retail Distribution',
            'Retail Distribution'
        ]
    }
    
    # Create DataFrame
    df_hsn = pd.DataFrame(hsn_data)
    
    # Display sample HSN data
    st.dataframe(df_hsn)
    
    # Marketing Officer Role
    st.subheader("👨‍💼 License Marketing & Distribution")
    
    st.markdown("""
    <div style="background-color: rgba(255, 140, 0, 0.1); padding: 20px; border-radius: 5px; border-left: 5px solid darkorange;">
        <h3 style="color: darkorange; margin-top: 0;">Marketing Officer's Role</h3>
        <p>The Marketing Officer is responsible for selling licenses to clients based on the Emperor's directives, 
        after consultation with the CFO and CIO. The officer works with the Business Development team to create 
        license packages tailored to different client needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # License types and distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### License Types
        
        - **Manufacturing License**
          *Full access to manufacturing modules*
          
        - **Retail License**
          *Full access to retail distribution modules*
          
        - **Management License**
          *Full access to management hub modules*
          
        - **Enterprise License**
          *Complete access to all modules*
          
        - **Custom Licenses**
          *Tailored access based on client needs*
        """)
        
    with col2:
        st.markdown("""
        ### License Distribution Strategy
        
        - **Direct Sales**
          *Enterprise clients with custom requirements*
          
        - **Partner Network**
          *Resellers with industry specialization*
          
        - **Online Platform**
          *Self-service for standard license packages*
          
        - **API Marketplace**
          *Programmatic access for developers*
          
        - **Enterprise Agreements**
          *Multi-year contracts with premium support*
        """)
    
    # Emperor's Review Process
    st.subheader("👑 Emperor's Review Process")
    
    st.markdown("""
    The Emperor conducts regular reviews with the Council of Ministers to ensure the health and prosperity 
    of the empire. These reviews follow a structured process:
    """)
    
    # Create timeline for review process
    timeline_data = {
        'Phase': [
            'Data Collection',
            'Minister Reports',
            'Council Session',
            "Emperor's Review",
            'Directive Issuance',
            'Implementation',
            'Compliance Audit'
        ],
        'Duration': [
            '7 days',
            '3 days',
            '1 day',
            '2 days',
            '1 day',
            '30 days',
            '5 days'
        ],
        'Responsible': [
            'Tech Team',
            'Ministers',
            'Council',
            'Emperor',
            'Emperor',
            'Business Development',
            'Compliance Team'
        ],
        'Description': [
            'Gathering data from all systems',
            'Each minister prepares status report',
            'Council meets to discuss findings',
            'Emperor reviews all information',
            'Emperor issues new directives',
            'Teams execute new directives',
            'Verify compliance with directives'
        ]
    }
    
    # Create DataFrame
    df_timeline = pd.DataFrame(timeline_data)
    
    # Display review process
    st.table(df_timeline)
    
    # Final call to action
    st.markdown("""
    <div style="background-color: rgba(70, 130, 180, 0.1); padding: 20px; border-radius: 5px; border-left: 5px solid steelblue; margin-top: 20px;">
        <h3 style="color: steelblue; margin-top: 0;">Emperor's Command Center</h3>
        <p>This visualization provides the Emperor with complete oversight of the entire ecosystem. 
        From here, the Emperor can monitor all activities, issue directives, and ensure the prosperity 
        of the empire through the Virtual Silk Road.</p>
    </div>
    """, unsafe_allow_html=True)