import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import datetime
import json
from database import get_db_session, EmpireEntity, BusinessModelMaster, ModuleMaster, BusinessModelModule
from database import EntityBusinessModel, LicenseTemplate, LicenseGrant, DataSharingAgreement, RiverTransaction

def show_data_sharing():
    """Display the data sharing agreement management interface"""
    st.title("Data Sharing Agreements")
    
    # Check if admin mode is enabled (for viewing Empire OS terminology)
    admin_mode = st.session_state.get('admin_mode', False)
    
    if admin_mode:
        # Show tabs with Empire OS terminology for administrators
        tabs = st.tabs(["Agreements Overview", "Create Agreement", "River Transactions", "Data Flow Visualization"])
    else:
        # Show tabs with industry-standard terminology for regular users
        tabs = st.tabs(["Agreements Overview", "Create Agreement", "Transaction Logs", "Supply Chain Network"])
    
    with tabs[0]:
        show_agreements_overview()
    
    with tabs[1]:
        show_create_agreement()
    
    with tabs[2]:
        show_river_transactions()
    
    with tabs[3]:
        show_data_flow_visualization()
        
    # Toggle for admin mode (only visible to authorized users)
    with st.sidebar:
        if st.session_state.get('is_license_holder', False):
            st.divider()
            admin_toggle = st.toggle("Show Empire OS Terminology", value=admin_mode)
            if admin_toggle != admin_mode:
                st.session_state['admin_mode'] = admin_toggle
                st.rerun()

def show_agreements_overview():
    """Display an overview of all data sharing agreements"""
    st.header("Data Sharing Agreements Overview")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect("Filter by Status", 
                                       ["Draft", "Active", "Expired", "Terminated"],
                                       default=["Active"])
    with col2:
        entity_filter = st.text_input("Filter by Entity Name")
    
    # Get agreements from database
    db = get_db_session()
    try:
        query = db.query(DataSharingAgreement).join(EmpireEntity)
        
        if status_filter:
            query = query.filter(DataSharingAgreement.status.in_(status_filter))
        
        if entity_filter:
            query = query.filter(EmpireEntity.name.like(f"%{entity_filter}%"))
        
        agreements = query.all()
        
        if not agreements:
            st.info("No data sharing agreements found with the selected filters.")
            # Show sample data for demo purposes
            show_sample_agreements()
        else:
            # Create dataframe for display
            agreements_data = []
            for agreement in agreements:
                agreements_data.append({
                    "Entity": agreement.entity.name,
                    "Agreement Reference": agreement.agreement_ref,
                    "Title": agreement.title,
                    "Version": agreement.version,
                    "Signed Date": agreement.signed_date,
                    "Status": agreement.status,
                    "Expiry Date": agreement.expiry_date
                })
            
            df = pd.DataFrame(agreements_data)
            st.dataframe(df, use_container_width=True)
            
            # Show agreement details on selection
            if agreements_data:
                selected_agreement = st.selectbox("Select an agreement to view details:", 
                                                  [a["Agreement Reference"] for a in agreements_data])
                
                # Find the selected agreement
                for agreement in agreements:
                    if agreement.agreement_ref == selected_agreement:
                        show_agreement_details(agreement)
                        break
    finally:
        db.close()

def show_sample_agreements():
    """Show sample agreements for demo purposes"""
    # Create sample data
    sample_data = [
        {
            "Entity": "Voi Jeans",
            "Agreement Reference": "DSA-VOI-2025-001",
            "Title": "Voi Jeans Brand Data Sharing Agreement",
            "Version": "1.0",
            "Signed Date": datetime.datetime(2025, 1, 15),
            "Status": "Active",
            "Expiry Date": datetime.datetime(2026, 1, 15)
        },
        {
            "Entity": "Scotts Garments",
            "Agreement Reference": "DSA-SCOTTS-2025-001",
            "Title": "Scotts Garments CMP Manufacturing Data Sharing",
            "Version": "1.0",
            "Signed Date": datetime.datetime(2025, 2, 10),
            "Status": "Active",
            "Expiry Date": datetime.datetime(2026, 2, 10)
        },
        {
            "Entity": "Fabric Mills Ltd.",
            "Agreement Reference": "DSA-FABM-2025-001",
            "Title": "Fabric Mills Material Supply Data Sharing",
            "Version": "1.0",
            "Signed Date": datetime.datetime(2025, 1, 25),
            "Status": "Active",
            "Expiry Date": datetime.datetime(2026, 1, 25)
        }
    ]
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True)
    
    # Allow selection of sample agreements
    if sample_data:
        selected_agreement = st.selectbox("Select an agreement to view details:", 
                                        [a["Agreement Reference"] for a in sample_data])
        
        # Find the selected sample agreement
        for agreement in sample_data:
            if agreement["Agreement Reference"] == selected_agreement:
                show_sample_agreement_details(agreement)
                break

def show_agreement_details(agreement):
    """Show details of a specific agreement"""
    st.subheader(f"Agreement Details: {agreement.title}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Entity:** {agreement.entity.name}")
        st.markdown(f"**Reference:** {agreement.agreement_ref}")
        st.markdown(f"**Version:** {agreement.version}")
        
    with col2:
        st.markdown(f"**Status:** {agreement.status}")
        st.markdown(f"**Signed Date:** {agreement.signed_date.strftime('%Y-%m-%d') if agreement.signed_date else 'Not signed'}")
        st.markdown(f"**Expiry Date:** {agreement.expiry_date.strftime('%Y-%m-%d') if agreement.expiry_date else 'No expiry'}")
    
    # Display sharing scope if available
    if agreement.sharing_scope:
        st.subheader("Data Sharing Scope")
        sharing_scope = agreement.sharing_scope
        if isinstance(sharing_scope, str):
            sharing_scope = json.loads(sharing_scope)
        
        col1, col2 = st.columns(2)
        with col1:
            if "networks" in sharing_scope:
                st.markdown("**Networks:**")
                for network in sharing_scope["networks"]:
                    st.markdown(f"- {network}")
        
        with col2:
            if "modules" in sharing_scope:
                st.markdown("**Modules:**")
                for module in sharing_scope["modules"]:
                    st.markdown(f"- {module}")
    
    # Display restrictions if available
    if agreement.restrictions:
        st.subheader("Usage Restrictions")
        restrictions = agreement.restrictions
        if isinstance(restrictions, str):
            restrictions = json.loads(restrictions)
        
        for restriction, value in restrictions.items():
            st.markdown(f"**{restriction}:** {value}")
    
    # Display governance rules if available
    if agreement.governance_rules:
        st.subheader("Governance Rules")
        governance_rules = agreement.governance_rules
        if isinstance(governance_rules, str):
            governance_rules = json.loads(governance_rules)
        
        for rule, value in governance_rules.items():
            st.markdown(f"**{rule}:** {value}")
    
    # Display agreement text if available
    if agreement.agreement_text:
        with st.expander("View Full Agreement Text"):
            st.markdown(agreement.agreement_text)

def show_sample_agreement_details(agreement):
    """Show details of a sample agreement for demo purposes"""
    st.subheader(f"Agreement Details: {agreement['Title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Entity:** {agreement['Entity']}")
        st.markdown(f"**Reference:** {agreement['Agreement Reference']}")
        st.markdown(f"**Version:** {agreement['Version']}")
        
    with col2:
        st.markdown(f"**Status:** {agreement['Status']}")
        st.markdown(f"**Signed Date:** {agreement['Signed Date'].strftime('%Y-%m-%d') if agreement['Signed Date'] else 'Not signed'}")
        st.markdown(f"**Expiry Date:** {agreement['Expiry Date'].strftime('%Y-%m-%d') if agreement['Expiry Date'] else 'No expiry'}")
    
    # Sample sharing scope
    st.subheader("Data Sharing Scope")
    if agreement['Entity'] == "Voi Jeans":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Networks:**")
            st.markdown("- Woven Supply")
            st.markdown("- Commune Connect")
        
        with col2:
            st.markdown("**Modules:**")
            st.markdown("- Order Management")
            st.markdown("- Style Management")
            st.markdown("- Material Tracking")
            st.markdown("- Production Timeline")
            st.markdown("- License Management")
    
    elif agreement['Entity'] == "Scotts Garments":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Networks:**")
            st.markdown("- Woven Supply")
        
        with col2:
            st.markdown("**Modules:**")
            st.markdown("- Style Management")
            st.markdown("- Material Tracking")
            st.markdown("- Production Timeline")
    
    elif agreement['Entity'] == "Fabric Mills Ltd.":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Networks:**")
            st.markdown("- Woven Supply")
        
        with col2:
            st.markdown("**Modules:**")
            st.markdown("- Material Tracking")
    
    # Sample restrictions
    st.subheader("Usage Restrictions")
    st.markdown("**Data retention period:** 24 months")
    st.markdown("**Geographic restrictions:** India only")
    st.markdown("**Third-party sharing:** Prohibited without explicit consent")
    
    # Sample governance rules
    st.subheader("Governance Rules")
    st.markdown("**Audit frequency:** Quarterly")
    st.markdown("**ECG oversight:** Required for data exports")
    st.markdown("**River transaction logging:** Enabled for all operations")
    
    # Sample agreement text
    with st.expander("View Full Agreement Text"):
        st.markdown("""
        ## DATA SHARING AGREEMENT
        
        This Data Sharing Agreement (the "Agreement") is entered into by and between Voi Jeans Retail India Pvt Ltd ("Voi Jeans") and the Entity identified above (the "Partner").
        
        ### 1. PURPOSE
        
        The purpose of this Agreement is to establish terms and conditions for the sharing of data between the Parties through the Empire OS platform for business purposes related to garment manufacturing and retail distribution.
        
        ### 2. DATA SHARING SCOPE
        
        The Parties agree to share data through the networks and modules specified above, subject to the license templates and business models assigned to each Party.
        
        ### 3. RESTRICTIONS
        
        All shared data is subject to the restrictions specified above. Any use of shared data outside these restrictions is prohibited.
        
        ### 4. GOVERNANCE
        
        All data sharing activities are subject to the governance rules specified above and oversight by Empire Commune Global (ECG).
        
        ### 5. TERM AND TERMINATION
        
        This Agreement shall commence on the Effective Date and continue until the Expiry Date, unless terminated earlier in accordance with its terms.
        
        ### 6. GOVERNING LAW
        
        This Agreement shall be governed by the laws of India.
        """)

def show_create_agreement():
    """Display the interface to create a new data sharing agreement"""
    st.header("Create Data Sharing Agreement")
    
    # Get entities from database
    db = get_db_session()
    try:
        entities = db.query(EmpireEntity).all()
        entity_names = [entity.name for entity in entities]
        
        if not entity_names:
            # Add sample entities for demo
            entity_names = ["Voi Jeans", "Scotts Garments", "Fabric Mills Ltd.", "Killer Jeans"]
    finally:
        db.close()
    
    # Agreement form
    with st.form("create_agreement_form"):
        entity_name = st.selectbox("Entity", entity_names)
        agreement_ref = st.text_input("Agreement Reference", value="DSA-" + entity_name.replace(" ", "").upper()[:4] + "-" + datetime.datetime.now().strftime("%Y-%m"))
        title = st.text_input("Agreement Title", value=entity_name + " Data Sharing Agreement")
        version = st.text_input("Version", value="1.0")
        
        col1, col2 = st.columns(2)
        with col1:
            effective_date = st.date_input("Effective Date", value=datetime.datetime.now())
        with col2:
            expiry_date = st.date_input("Expiry Date", value=datetime.datetime.now() + datetime.timedelta(days=365))
        
        # Networks and modules selection
        st.subheader("Data Sharing Scope")
        col1, col2 = st.columns(2)
        with col1:
            networks = st.multiselect("Networks", ["Woven Supply", "Commune Connect"], 
                                      default=["Woven Supply", "Commune Connect"] if entity_name == "Voi Jeans" else ["Woven Supply"])
        
        with col2:
            all_modules = [
                "Order Management", "Style Management", "Material Tracking", 
                "Production Timeline", "Line Planning", "Reporting",
                "Retail Analytics", "Store Management", "License Management",
                "Finance & Governance"
            ]
            
            default_modules = []
            if entity_name == "Voi Jeans":
                default_modules = all_modules
            elif entity_name == "Scotts Garments":
                default_modules = ["Style Management", "Material Tracking", "Production Timeline", "Line Planning"]
            elif entity_name == "Fabric Mills Ltd.":
                default_modules = ["Material Tracking"]
            
            modules = st.multiselect("Modules", all_modules, default=default_modules)
        
        # Restrictions
        st.subheader("Usage Restrictions")
        col1, col2 = st.columns(2)
        with col1:
            retention_period = st.number_input("Data Retention Period (months)", min_value=1, value=24)
        with col2:
            geo_restriction = st.selectbox("Geographic Restriction", ["India only", "Global", "Asia only"])
        
        third_party_sharing = st.selectbox("Third-party Sharing", [
            "Prohibited without explicit consent", 
            "Permitted with notification",
            "Permitted without notification"
        ])
        
        # Governance rules
        st.subheader("Governance Rules")
        col1, col2 = st.columns(2)
        with col1:
            audit_frequency = st.selectbox("Audit Frequency", ["Monthly", "Quarterly", "Semi-annually", "Annually"])
        with col2:
            ecg_oversight = st.selectbox("ECG Oversight", ["Required for all operations", "Required for data exports", "Required for sensitive data only", "Not required"])
        
        river_logging = st.selectbox("River Transaction Logging", ["Enabled for all operations", "Enabled for write operations only", "Enabled for sensitive data only"])
        
        # Agreement text (simplified for demo)
        st.subheader("Agreement Text")
        st.info("A standard agreement template will be generated based on your selections. You can review and edit it before finalizing.")
        
        # Submit button
        submitted = st.form_submit_button("Create Agreement")
        
        if submitted:
            # In a real application, this would save to the database
            st.success(f"Data Sharing Agreement created for {entity_name} with reference {agreement_ref}")
            
            # Show a sample of what would be saved
            st.json({
                "entity": entity_name,
                "agreement_ref": agreement_ref,
                "title": title,
                "version": version,
                "effective_date": effective_date.strftime("%Y-%m-%d"),
                "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                "sharing_scope": {
                    "networks": networks,
                    "modules": modules
                },
                "restrictions": {
                    "retention_period": f"{retention_period} months",
                    "geo_restriction": geo_restriction,
                    "third_party_sharing": third_party_sharing
                },
                "governance_rules": {
                    "audit_frequency": audit_frequency,
                    "ecg_oversight": ecg_oversight,
                    "river_logging": river_logging
                }
            })

def show_river_transactions():
    """Display River transaction logs"""
    admin_mode = st.session_state.get('admin_mode', False)
    
    if admin_mode:
        # Empire OS terminology for administrators
        st.header("River Transaction Logs")
        st.markdown("""
        River is the Empire OS transaction logging system that records all data access, sharing, and license operations.
        All transactions are immutable and provide an audit trail for governance and compliance.
        """)
    else:
        # Industry-standard terminology for regular users
        st.header("System Transaction Logs")
        st.markdown("""
        The system maintains comprehensive logs of all data access, sharing, and license operations.
        All transactions are securely recorded and provide an audit trail for compliance and monitoring purposes.
        """)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        entity_filter = st.text_input("Filter by Entity")
    with col2:
        transaction_type_filter = st.multiselect("Transaction Type", 
                                                ["Data Access", "License Grant", "Data Sharing", "License Update", "Agreement Signature"],
                                                default=[])
    with col3:
        date_range = st.date_input("Date Range", 
                                  value=(datetime.datetime.now() - datetime.timedelta(days=7), datetime.datetime.now()),
                                  help="Filter transactions by date range")
    
    # Get transactions from database
    db = get_db_session()
    try:
        transactions = db.query(RiverTransaction).all()
        
        if not transactions:
            # Show sample transactions for demo
            show_sample_transactions()
        else:
            # Create dataframe for display
            transactions_data = []
            for tx in transactions:
                entity = db.query(EmpireEntity).filter_by(id=tx.entity_id).first()
                entity_name = entity.name if entity else "Unknown"
                
                transactions_data.append({
                    "Transaction ID": tx.transaction_id,
                    "Entity": entity_name,
                    "Type": tx.transaction_type,
                    "Resource": f"{tx.resource_type}: {tx.resource_id}",
                    "Timestamp": tx.timestamp,
                    "Access Level": tx.access_level,
                    "Status": tx.status
                })
            
            df = pd.DataFrame(transactions_data)
            st.dataframe(df, use_container_width=True)
    finally:
        db.close()

def show_sample_transactions():
    """Show sample transactions for demo purposes"""
    # Create sample transaction data
    now = datetime.datetime.now()
    sample_transactions = [
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-001",
            "Entity": "Voi Jeans",
            "Type": "Data Access",
            "Resource": "Order: PO-2025-001",
            "Timestamp": now - datetime.timedelta(hours=1),
            "Access Level": "Read",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-002",
            "Entity": "Scotts Garments",
            "Type": "Data Access",
            "Resource": "Style: ST-2025-001",
            "Timestamp": now - datetime.timedelta(hours=2),
            "Access Level": "Read",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-003",
            "Entity": "Voi Jeans",
            "Type": "Data Access",
            "Resource": "Material: FAB-DENIM-001",
            "Timestamp": now - datetime.timedelta(hours=3),
            "Access Level": "Read",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-004",
            "Entity": "Fabric Mills Ltd.",
            "Type": "Data Access",
            "Resource": "Material: FAB-DENIM-001",
            "Timestamp": now - datetime.timedelta(hours=4),
            "Access Level": "Write",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-005",
            "Entity": "Voi Jeans",
            "Type": "License Update",
            "Resource": "License: LIC-VOI-2025-001",
            "Timestamp": now - datetime.timedelta(days=1),
            "Access Level": "Write",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-006",
            "Entity": "Scotts Garments",
            "Type": "Agreement Signature",
            "Resource": "Agreement: DSA-SCOTTS-2025-001",
            "Timestamp": now - datetime.timedelta(days=2),
            "Access Level": "Write",
            "Status": "Success"
        },
        {
            "Transaction ID": "TXN-" + now.strftime("%Y%m%d") + "-007",
            "Entity": "Voi Jeans",
            "Type": "Data Sharing",
            "Resource": "Style: ST-2025-002",
            "Timestamp": now - datetime.timedelta(days=2, hours=2),
            "Access Level": "Full",
            "Status": "Success"
        }
    ]
    
    # Apply filters if provided
    entity_filter = st.session_state.get('entity_filter', '')
    transaction_type_filter = st.session_state.get('transaction_type_filter', [])
    date_range = st.session_state.get('date_range', (now - datetime.timedelta(days=7), now))
    
    filtered_transactions = sample_transactions
    
    if entity_filter:
        filtered_transactions = [tx for tx in filtered_transactions if entity_filter.lower() in tx["Entity"].lower()]
    
    if transaction_type_filter:
        filtered_transactions = [tx for tx in filtered_transactions if tx["Type"] in transaction_type_filter]
    
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
        end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
        filtered_transactions = [tx for tx in filtered_transactions 
                                if start_datetime <= tx["Timestamp"] <= end_datetime]
    
    # Display filtered transactions
    if filtered_transactions:
        df = pd.DataFrame(filtered_transactions)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No transactions found with the selected filters.")

def show_data_flow_visualization():
    """Display visualization of data flows between entities"""
    admin_mode = st.session_state.get('admin_mode', False)
    
    if admin_mode:
        # Empire OS terminology for administrators
        st.header("Data Flow Visualization")
        st.markdown("""
        This visualization shows how data flows between different entities in the ecosystem
        based on their data sharing agreements and license templates.
        """)
    else:
        # Industry-standard terminology for regular users
        st.header("Supply Chain Network Visualization")
        st.markdown("""
        This visualization shows how information flows between different partners in the supply chain network
        based on their data sharing agreements and access permissions.
        """)
    
    # Create a network graph
    G = nx.DiGraph()
    
    # Add nodes for different entity types
    G.add_node("Voi Jeans", role="Brand", network="Both")
    G.add_node("Scotts Garments", role="Manufacturer", network="Woven Supply")
    G.add_node("Fabric Mills Ltd.", role="Material Supplier", network="Woven Supply")
    G.add_node("Retail Stores", role="Retailer", network="Commune Connect")
    G.add_node("Synergyze Hub", role="Governance", network="Both")
    G.add_node("ECG", role="Compliance", network="Both")
    
    # Add edges representing data flows
    G.add_edge("Voi Jeans", "Scotts Garments", data_type="Orders, Styles")
    G.add_edge("Scotts Garments", "Voi Jeans", data_type="Production Updates")
    G.add_edge("Fabric Mills Ltd.", "Scotts Garments", data_type="Material Details")
    G.add_edge("Voi Jeans", "Retail Stores", data_type="Product Data")
    G.add_edge("Retail Stores", "Voi Jeans", data_type="Sales Data")
    G.add_edge("Voi Jeans", "Synergyze Hub", data_type="License Data")
    G.add_edge("Scotts Garments", "Synergyze Hub", data_type="License Data")
    G.add_edge("Fabric Mills Ltd.", "Synergyze Hub", data_type="License Data")
    G.add_edge("Retail Stores", "Synergyze Hub", data_type="License Data")
    G.add_edge("Synergyze Hub", "ECG", data_type="Compliance Data")
    G.add_edge("ECG", "Synergyze Hub", data_type="Approvals")
    
    # Define node positions
    pos = {
        "Voi Jeans": (0, 0),
        "Scotts Garments": (-1, -1),
        "Fabric Mills Ltd.": (-2, -1.5),
        "Retail Stores": (1, -1),
        "Synergyze Hub": (0, 1),
        "ECG": (0, 2)
    }
    
    # Define node colors based on network
    node_colors = {
        "Voi Jeans": "#1E3A8A",  # Deep blue
        "Scotts Garments": "#047857",  # Green
        "Fabric Mills Ltd.": "#059669",  # Light green
        "Retail Stores": "#7C3AED",  # Purple
        "Synergyze Hub": "#EA580C",  # Orange
        "ECG": "#BE123C"  # Red
    }
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        # Add curve to the edge
        edge_trace = go.Scatter(
            x=[x0, (x0+x1)/2, x1],
            y=[y0, (y0+y1)/2 + 0.2, y1],
            line=dict(width=2, color='#999'),
            hoverinfo='text',
            text=G.edges[edge]['data_type'],
            mode='lines'
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=list(G.nodes()),
        textposition='bottom center',
        marker=dict(
            showscale=False,
            color=[node_colors[node] for node in G.nodes()],
            size=30,
            line_width=2
        ),
        hoverinfo='text',
        hovertext=[f"{node}<br>Role: {G.nodes[node]['role']}<br>Network: {G.nodes[node]['network']}" for node in G.nodes()]
    )
    
    # Create the figure
    admin_mode = st.session_state.get('admin_mode', False)
    
    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title='Data Sharing Network' if admin_mode else 'Supply Chain Network',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        width=800,
                        height=600,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation of the visualization
    admin_mode = st.session_state.get('admin_mode', False)
    
    if admin_mode:
        # Empire OS terminology for administrators
        st.subheader("Understanding the Data Flow")
        st.markdown("""
        - **Voi Jeans** (Brand) is at the center of the ecosystem, interacting with both manufacturing and retail networks
        - **Scotts Garments** (Manufacturer) receives orders and styles from Voi Jeans and sends back production updates
        - **Fabric Mills Ltd.** (Material Supplier) provides material details to Scotts Garments
        - **Retail Stores** receive product data from Voi Jeans and send back sales data
        - **Synergyze Hub** serves as the governance layer, managing licenses for all entities
        - **ECG** (Empire Commune Global) provides compliance oversight and approvals for the ecosystem
        
        All data flows are governed by data sharing agreements and license templates configured in the Empire OS.
        """)
    else:
        # Industry-standard terminology for regular users
        st.subheader("Understanding the Supply Chain Network")
        st.markdown("""
        - **Voi Jeans** (Brand) is at the center of the supply chain, coordinating with manufacturing partners and retail channels
        - **Scotts Garments** (Manufacturer) receives style information and production orders from Voi Jeans and provides production status updates
        - **Fabric Mills Ltd.** (Material Supplier) provides fabric specifications and availability to manufacturing partners
        - **Retail Stores** receive product information from Voi Jeans and share sales performance data
        - **Management Hub** provides centralized governance and compliance monitoring for all partners
        - **Compliance Team** ensures all operations meet industry standards and regulatory requirements
        
        All information sharing is governed by formal data sharing agreements that protect each partner's sensitive information.
        """)
    
    # Add license flow visualization
    admin_mode = st.session_state.get('admin_mode', False)
    
    if admin_mode:
        # Empire OS terminology for administrators
        st.subheader("License Template Flow")
        st.markdown("This shows how license templates are assigned based on entity types and business models:")
    else:
        # Industry-standard terminology for regular users
        st.subheader("Access Permission Framework")
        st.markdown("This shows how system access permissions are assigned based on company types and business relationships:")
    
    # Create sample license flow data
    license_data = {
        "Business Type": ["Brand", "Brand", "Manufacturer", "Manufacturer", "Retailer", "Retailer"],
        "Business Model": ["House Brand", "Private Label", "CMP", "FOB", "SOR", "Marketplace"],
        "License Template": ["TEMPLATE-HOUSE-001", "TEMPLATE-PL-001", "TEMPLATE-CMP-001", "TEMPLATE-FOB-001", "TEMPLATE-SOR-001", "TEMPLATE-MKT-001"],
        "Entity Example": ["Voi Jeans", "Killer Jeans", "Scotts Garments", "Export Partner", "Department Store", "Online Marketplace"]
    }
    
    df_license = pd.DataFrame(license_data)
    st.dataframe(df_license, use_container_width=True)
    
    # Add sankey diagram to visualize the license flow
    labels = list(set(license_data["Business Type"] + license_data["Business Model"] + license_data["License Template"]))
    
    # Create source, target, value arrays for the Sankey diagram
    source = []
    target = []
    value = []
    
    # Business Type to Business Model
    for i, bt in enumerate(license_data["Business Type"]):
        bm = license_data["Business Model"][i]
        lt = license_data["License Template"][i]
        
        source.append(labels.index(bt))
        target.append(labels.index(bm))
        value.append(1)
        
        source.append(labels.index(bm))
        target.append(labels.index(lt))
        value.append(1)
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = ["#1E3A8A" if label in license_data["Business Type"] else 
                    "#047857" if label in license_data["Business Model"] else
                    "#7C3AED" for label in labels]
        ),
        link = dict(
            source = source,
            target = target,
            value = value
        ))])
    
    admin_mode = st.session_state.get('admin_mode', False)
    fig.update_layout(
        title_text="License Template Flow" if admin_mode else "Access Permission Framework", 
        font_size=10, 
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

def create_license_template_matrix():
    """Create a visual matrix of business types, models, and license templates"""
    # This would be populated from the database in a real implementation
    business_types = ["Manufacturer", "Retailer", "Brand"]
    
    business_models = {
        "Manufacturer": ["CMP", "FOB", "White-Label"],
        "Retailer": ["Marketplace", "SOR", "Large Format Retail"],
        "Brand": ["House Brand", "Private Label"]
    }
    
    license_templates = {
        "Manufacturer": {
            "CMP": "TEMPLATE-CMP-001",
            "FOB": "TEMPLATE-FOB-001",
            "White-Label": "TEMPLATE-WLBL-001"
        },
        "Retailer": {
            "Marketplace": "TEMPLATE-MKT-001",
            "SOR": "TEMPLATE-SOR-001",
            "Large Format Retail": "TEMPLATE-LFR-001"
        },
        "Brand": {
            "House Brand": "TEMPLATE-HOUSE-001",
            "Private Label": "TEMPLATE-PL-001"
        }
    }
    
    # Create heatmap data
    data = []
    for bt in business_types:
        for bm in business_models[bt]:
            data.append({
                "Business Type": bt,
                "Business Model": bm,
                "License Template": license_templates[bt][bm]
            })
    
    return pd.DataFrame(data)