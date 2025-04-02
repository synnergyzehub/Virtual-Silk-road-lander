import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show_hsn_transaction_system():
    """
    Display the HSN-based transaction system with real-time trend analysis
    and gamified inventory management features
    """
    
    # Page header with styling
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, #1E3A8A 0%, #4B0082 100%); 
        padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; font-size: 2.2rem;'>🏆 HSN Transaction Suite</h1>
            <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0;'>
                Real-time analysis, organic trends, and gamified inventory management
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Setup tabs for different sections
    tabs = st.tabs([
        "📊 Dashboard", 
        "🧾 HSN Transactions", 
        "📈 Trend Analysis", 
        "🏆 Leaderboards"
    ])
    
    # Tab 1: Main Dashboard
    with tabs[0]:
        show_dashboard()
    
    # Tab 2: HSN Transaction Management
    with tabs[1]:
        show_hsn_transactions()
    
    # Tab 3: Trend Analysis
    with tabs[2]:
        show_trend_analysis()
    
    # Tab 4: Gamified Leaderboards
    with tabs[3]:
        show_gamified_leaderboard()

def show_dashboard():
    """Display the main dashboard with key metrics and summaries"""
    
    st.subheader("HSN Transaction Dashboard")
    
    # Key performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Generate some sample metrics
    today = datetime.now().strftime("%d %b %Y")
    transactions_today = random.randint(120, 180)
    transactions_yesterday = random.randint(100, 160)
    transaction_diff = transactions_today - transactions_yesterday
    
    with col1:
        st.metric(
            "Transactions Today", 
            f"{transactions_today:,}", 
            f"{transaction_diff:+d} vs yesterday",
            delta_color="normal"
        )
    
    inventory_turnover = round(random.uniform(3.5, 4.2), 2)
    inventory_turnover_prev = round(random.uniform(3.4, 3.8), 2)
    inventory_diff = inventory_turnover - inventory_turnover_prev
    
    with col2:
        st.metric(
            "Inventory Turnover", 
            f"{inventory_turnover}", 
            f"{inventory_diff:+.2f} vs last month",
            delta_color="normal"
        )
    
    hsn_compliance = random.randint(94, 99)
    hsn_compliance_prev = random.randint(90, 95)
    compliance_diff = hsn_compliance - hsn_compliance_prev
    
    with col3:
        st.metric(
            "HSN Compliance", 
            f"{hsn_compliance}%", 
            f"{compliance_diff:+d}% vs last quarter",
            delta_color="normal"
        )
    
    efficiency_score = random.randint(85, 95)
    efficiency_prev = random.randint(80, 90)
    efficiency_diff = efficiency_score - efficiency_prev
    
    with col4:
        st.metric(
            "Team Efficiency", 
            f"{efficiency_score}", 
            f"{efficiency_diff:+d} points",
            delta_color="normal"
        )
    
    # Recent activity and transaction summary
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent HSN Transactions")
        
        # Generate sample transaction data
        transactions = generate_sample_transactions(10)
        
        # Display recent transactions in a table
        st.dataframe(
            transactions[["Transaction ID", "Date", "HSN Code", "Product Category", "Quantity", "Transaction Type", "Status"]],
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("Quick Stats")
        
        # HSN code compliance chart
        hsn_data = {
            "Status": ["Correct", "Needs Review", "Incorrect"],
            "Percentage": [88, 9, 3],
            "Color": ["#4CAF50", "#FFC107", "#F44336"]
        }
        
        fig = px.pie(
            hsn_data,
            values="Percentage",
            names="Status",
            title="HSN Code Accuracy",
            color="Status",
            color_discrete_map={
                "Correct": "#4CAF50",
                "Needs Review": "#FFC107", 
                "Incorrect": "#F44336"
            },
            hole=0.6
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory movement summary
        inv_move_data = {
            "Direction": ["Inward", "Outward", "Transfer", "Return"],
            "Count": [45, 38, 12, 5]
        }
        
        fig = px.bar(
            inv_move_data,
            x="Direction",
            y="Count",
            title="Today's Inventory Movements",
            color="Direction",
            color_discrete_map={
                "Inward": "#4285F4", 
                "Outward": "#EA4335",
                "Transfer": "#FBBC05",
                "Return": "#34A853"
            }
        )
        
        fig.update_layout(height=250, margin=dict(t=30, b=0, l=0, r=0))
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Lower dashboard section
    st.subheader("HSN Code Distribution")
    
    # Generate HSN distribution data
    hsn_dist = generate_hsn_distribution()
    
    # Create a treemap visualization
    fig = px.treemap(
        hsn_dist,
        path=['HSN Section', 'HSN Chapter', 'HSN Code'],
        values='Transaction Count',
        title="HSN Code Distribution by Section, Chapter, and Code",
        color='Value',
        color_continuous_scale='Viridis',
        hover_data=['Description']
    )
    
    fig.update_layout(height=500, margin=dict(t=30, b=0, l=0, r=0))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Notifications and alerts section
    st.subheader("Alerts & Notifications")
    
    alert_data = [
        {"level": "High", "message": "HSN code 6109 has 3 misclassified items that need review", "time": "10 minutes ago"},
        {"level": "Medium", "message": "Team A has achieved 98% HSN accuracy this week, highest across all teams", "time": "2 hours ago"},
        {"level": "Low", "message": "New GST notification affecting HSN codes in chapter 61 has been published", "time": "1 day ago"},
        {"level": "Medium", "message": "Inventory turnover for HSN 6203 is below target by 12%", "time": "2 days ago"}
    ]
    
    for alert in alert_data:
        if alert["level"] == "High":
            bg_color = "#FFEBEE"
            border_color = "#F44336"
            icon = "🚨"
        elif alert["level"] == "Medium":
            bg_color = "#FFF8E1"
            border_color = "#FFC107"
            icon = "⚠️"
        else:
            bg_color = "#E8F5E9"
            border_color = "#4CAF50"
            icon = "ℹ️"
        
        st.markdown(f"""
        <div style='background-color: {bg_color}; padding: 10px 15px; border-left: 4px solid {border_color}; 
                  border-radius: 4px; margin-bottom: 10px;'>
            <div style='display: flex; align-items: center;'>
                <div style='margin-right: 10px; font-size: 1.2rem;'>{icon}</div>
                <div style='flex-grow: 1;'>
                    <div style='font-weight: bold;'>{alert["level"]} Priority</div>
                    <div>{alert["message"]}</div>
                    <div style='font-size: 0.8em; color: #666; margin-top: 5px;'>{alert["time"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_hsn_transactions():
    """Display the HSN transaction management interface"""
    
    st.subheader("HSN Transaction Management")
    
    # Create tabs for different transaction operations
    transaction_tabs = st.tabs([
        "View Transactions", 
        "Create Transaction", 
        "HSN Code Lookup", 
        "Bulk Operations"
    ])
    
    # Tab 1: View and Filter Transactions
    with transaction_tabs[0]:
        st.subheader("Transaction Records")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_options = ["Today", "Yesterday", "Last 7 Days", "Last 30 Days", "Custom Range"]
            date_filter = st.selectbox("Date Range", date_options)
            
            if date_filter == "Custom Range":
                start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=7))
                end_date = st.date_input("End Date", value=datetime.now())
        
        with col2:
            hsn_chapters = ["All Chapters", "Chapter 50-59: Textile Fibers", "Chapter 60-63: Textile Articles", 
                           "Chapter 64-67: Footwear, Headgear", "Chapter 68-70: Stone, Ceramic, Glass"]
            chapter_filter = st.selectbox("HSN Chapter", hsn_chapters)
            
            transaction_types = ["All Types", "Inward", "Outward", "Transfer", "Return"]
            type_filter = st.selectbox("Transaction Type", transaction_types)
        
        with col3:
            status_options = ["All Statuses", "Completed", "Pending", "Cancelled", "On Hold"]
            status_filter = st.selectbox("Status", status_options)
            
            search_term = st.text_input("Search Transactions", placeholder="Enter transaction ID, HSN code, or product")
        
        # Generate filtered transaction data
        transactions = generate_sample_transactions(30)
        
        # Apply filters (simplified for demo)
        if search_term:
            transactions = transactions[
                transactions["Transaction ID"].str.contains(search_term, case=False) |
                transactions["HSN Code"].astype(str).str.contains(search_term, case=False) |
                transactions["Product Category"].str.contains(search_term, case=False)
            ]
        
        if status_filter != "All Statuses":
            transactions = transactions[transactions["Status"] == status_filter]
            
        if type_filter != "All Types":
            transactions = transactions[transactions["Transaction Type"] == type_filter]
        
        # Transaction view
        st.dataframe(
            transactions,
            use_container_width=True,
            hide_index=True
        )
        
        # Export and action buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.button("📄 Export CSV", use_container_width=True)
        
        with col2:
            st.button("📊 Export Report", use_container_width=True)
        
        with col3:
            st.button("🔍 Audit Selected", use_container_width=True)
        
        with col4:
            st.button("✏️ Edit Selected", use_container_width=True)
    
    # Tab 2: Create New Transaction
    with transaction_tabs[1]:
        st.subheader("Create New HSN Transaction")
        
        # Use columns for form layout
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.selectbox(
                "Transaction Type", 
                ["Inward", "Outward", "Transfer", "Return"]
            )
            
            transaction_date = st.date_input(
                "Transaction Date",
                value=datetime.now()
            )
            
            if transaction_type == "Transfer":
                source_location = st.selectbox(
                    "Source Location",
                    ["Mumbai Main Warehouse", "Delhi Distribution Center", "Bangalore Fulfillment Hub", 
                     "Chennai Storage Facility", "Hyderabad Satellite Warehouse"]
                )
                
                dest_location = st.selectbox(
                    "Destination Location",
                    ["Mumbai Main Warehouse", "Delhi Distribution Center", "Bangalore Fulfillment Hub", 
                     "Chennai Storage Facility", "Hyderabad Satellite Warehouse"]
                )
            else:
                warehouse = st.selectbox(
                    "Warehouse Location",
                    ["Mumbai Main Warehouse", "Delhi Distribution Center", "Bangalore Fulfillment Hub", 
                     "Chennai Storage Facility", "Hyderabad Satellite Warehouse"]
                )
                
                if transaction_type in ["Inward", "Return"]:
                    vendor = st.text_input("Supplier/Vendor")
                else:
                    customer = st.text_input("Customer/Destination")
        
        with col2:
            reference_no = st.text_input("Reference Number (Invoice/PO)")
            
            document_upload = st.file_uploader("Upload Supporting Document", type=["pdf", "jpg", "png"])
            
            notes = st.text_area("Transaction Notes")
        
        # Item details section
        st.subheader("Item Details")
        
        # Option to search by HSN or product
        search_option = st.radio("Search By", ["HSN Code", "Product"], horizontal=True)
        
        if search_option == "HSN Code":
            hsn_code = st.text_input("Enter HSN Code")
            
            if hsn_code:
                st.info(f"Showing items matching HSN code: {hsn_code}")
                
                # Sample products matching HSN code
                matching_products = [
                    {"SKU": "DNM-JEN-1234", "Product": "VOI Classic Straight Jeans", "HSN": "6203", "Description": "Men's denim trousers"},
                    {"SKU": "DNM-JEN-2341", "Product": "VOI Premium Slim Jeans", "HSN": "6203", "Description": "Men's denim trousers, slim fit"},
                    {"SKU": "DNM-JEN-3412", "Product": "VOI Essential Regular Jeans", "HSN": "6203", "Description": "Men's denim trousers, regular fit"}
                ]
                
                selected_products = []
                
                for i, product in enumerate(matching_products):
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        st.write(f"**{product['Product']}**")
                        st.caption(f"SKU: {product['SKU']} • HSN: {product['HSN']}")
                    
                    with col2:
                        st.caption(product['Description'])
                    
                    with col3:
                        quantity = st.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
                    
                    with col4:
                        add = st.checkbox("Select", key=f"select_{i}")
                        if add:
                            selected_products.append({**product, "Quantity": quantity})
        else:
            product_search = st.text_input("Search Products")
            
            if product_search:
                st.info(f"Showing items matching: {product_search}")
                
                # Sample products matching search
                matching_products = [
                    {"SKU": "TST-RND-5678", "Product": "VOI Basic Round Neck T-Shirt", "HSN": "6109", "Description": "Cotton T-shirt, round neck"},
                    {"SKU": "TST-VNK-6789", "Product": "VOI Premium V-Neck T-Shirt", "HSN": "6109", "Description": "Cotton T-shirt, v-neck"},
                    {"SKU": "TST-POL-7890", "Product": "VOI Signature Polo T-Shirt", "HSN": "6109", "Description": "Cotton polo shirt"}
                ]
                
                selected_products = []
                
                for i, product in enumerate(matching_products):
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        st.write(f"**{product['Product']}**")
                        st.caption(f"SKU: {product['SKU']} • HSN: {product['HSN']}")
                    
                    with col2:
                        st.caption(product['Description'])
                    
                    with col3:
                        quantity = st.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
                    
                    with col4:
                        add = st.checkbox("Select", key=f"select_{i}")
                        if add:
                            selected_products.append({**product, "Quantity": quantity})
        
        # Manual HSN entry option
        st.divider()
        st.subheader("Manual Item Entry")
        
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        with col1:
            manual_product = st.text_input("Product Name/Description")
        
        with col2:
            manual_hsn = st.text_input("HSN Code")
        
        with col3:
            manual_quantity = st.number_input("Quantity", min_value=1, value=1)
        
        with col4:
            st.write("")
            st.write("")
            if st.button("Add Item"):
                st.success("Item added successfully")
        
        # Complete transaction button
        st.divider()
        if st.button("Submit Transaction", type="primary"):
            st.success("Transaction created successfully!")
            st.info("Transaction ID: TRX-" + datetime.now().strftime("%Y%m%d") + "-" + str(random.randint(1000, 9999)))
    
    # Tab 3: HSN Code Lookup
    with transaction_tabs[2]:
        st.subheader("HSN Code Lookup & Verification")
        
        # HSN search interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            hsn_search_option = st.radio(
                "Search Options", 
                ["HSN Code", "Product Description", "Browse Hierarchy"], 
                horizontal=True
            )
            
            if hsn_search_option == "HSN Code":
                hsn_query = st.text_input("Enter HSN Code", placeholder="e.g., 6203")
                search_button = st.button("Lookup HSN Details")
                
                if hsn_query:
                    st.success(f"HSN Code: {hsn_query}")
                    
                    # Display HSN details
                    hsn_details = {
                        "Code": hsn_query,
                        "Description": "Men's or boys' suits, ensembles, jackets, blazers, trousers, bib and brace overalls, breeches and shorts (other than swimwear)",
                        "Chapter": "Chapter 62 - Articles of apparel and clothing accessories, not knitted or crocheted",
                        "Section": "Section XI - Textiles and textile articles",
                        "GST Rate": "12%",
                        "Commonly Used For": "Men's trousers, jeans, formal pants, shorts"
                    }
                    
                    for key, value in hsn_details.items():
                        st.text(f"{key}: {value}")
                    
                    # Show recent transactions with this HSN code
                    st.subheader("Recent Transactions")
                    transactions = generate_sample_transactions(5, hsn_code=hsn_query)
                    st.dataframe(transactions, use_container_width=True, hide_index=True)
            
            elif hsn_search_option == "Product Description":
                product_query = st.text_input("Enter Product Description", placeholder="e.g., men's jeans")
                search_button = st.button("Find Matching HSN Codes")
                
                if product_query:
                    # Display matching HSN codes
                    matching_hsn_codes = [
                        {"HSN": "6203", "Description": "Men's or boys' trousers, jeans, and shorts", "Certainty": "High", "GST": "12%"},
                        {"HSN": "6103", "Description": "Men's or boys' trousers, knitted or crocheted", "Certainty": "Medium", "GST": "12%"},
                        {"HSN": "5209", "Description": "Woven fabrics of cotton (denim)", "Certainty": "Low", "GST": "5%"}
                    ]
                    
                    st.success(f"Found {len(matching_hsn_codes)} potential matches for '{product_query}'")
                    
                    for hsn in matching_hsn_codes:
                        match_color = "#4CAF50" if hsn["Certainty"] == "High" else "#FFC107" if hsn["Certainty"] == "Medium" else "#F44336"
                        
                        st.markdown(f"""
                        <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;'>
                            <div style='display: flex; justify-content: space-between;'>
                                <div>
                                    <h4 style='margin: 0;'>{hsn["HSN"]}</h4>
                                    <p style='margin: 5px 0;'>{hsn["Description"]}</p>
                                </div>
                                <div style='text-align: right;'>
                                    <span style='background-color: {match_color}; color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;'>
                                        {hsn["Certainty"]} Match
                                    </span>
                                    <p style='margin: 5px 0;'>GST: {hsn["GST"]}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            else:  # Browse Hierarchy
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    sections = [
                        "Section I - Animal products",
                        "Section VIII - Raw hides, leather, furskins",
                        "Section XI - Textiles and textile articles",
                        "Section XII - Footwear, headgear, umbrellas",
                        "Section XX - Miscellaneous manufactured articles"
                    ]
                    selected_section = st.selectbox("Select Section", sections)
                
                with col2:
                    if "Section XI" in selected_section:
                        chapters = [
                            "Chapter 50 - Silk",
                            "Chapter 52 - Cotton",
                            "Chapter 61 - Knitted or crocheted apparel",
                            "Chapter 62 - Non-knitted apparel",
                            "Chapter 63 - Other textile articles"
                        ]
                    else:
                        chapters = ["Select a section first"]
                    
                    selected_chapter = st.selectbox("Select Chapter", chapters)
                
                with col3:
                    if "Chapter 61" in selected_chapter:
                        codes = [
                            "6101 - Men's overcoats, knitted",
                            "6102 - Women's overcoats, knitted",
                            "6103 - Men's suits, knitted",
                            "6104 - Women's suits, knitted",
                            "6109 - T-shirts, knitted"
                        ]
                    elif "Chapter 62" in selected_chapter:
                        codes = [
                            "6201 - Men's overcoats, not knitted",
                            "6202 - Women's overcoats, not knitted",
                            "6203 - Men's suits, not knitted",
                            "6204 - Women's suits, not knitted",
                            "6205 - Men's shirts, not knitted"
                        ]
                    else:
                        codes = ["Select a chapter first"]
                    
                    selected_code = st.selectbox("Select HSN Code", codes)
                
                if "61" in selected_chapter or "62" in selected_chapter:
                    if st.button("View HSN Details"):
                        hsn_code = selected_code.split(" - ")[0]
                        st.success(f"HSN Code: {hsn_code}")
                        
                        # Display HSN details
                        st.text(f"Description: {selected_code.split(' - ')[1]}")
                        st.text(f"Chapter: {selected_chapter}")
                        st.text(f"Section: {selected_section}")
                        st.text("GST Rate: 12%")
        
        with col2:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
                <h4 style='margin-top: 0;'>HSN Code Tips</h4>
                <ul style='margin-bottom: 0; padding-left: 20px;'>
                    <li>Ensure correct HSN classification for proper GST rates</li>
                    <li>Refer to official HSN directories for verification</li>
                    <li>Similar products may have different HSN codes based on materials</li>
                    <li>HSN codes are 4-8 digits, with more digits indicating greater specificity</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-top: 15px;'>
                <h4 style='margin-top: 0;'>Recently Used HSN Codes</h4>
                <table style='width: 100%;'>
                    <tr>
                        <td><strong>6109</strong></td>
                        <td>T-shirts, knitted</td>
                    </tr>
                    <tr>
                        <td><strong>6203</strong></td>
                        <td>Men's suits, not knitted</td>
                    </tr>
                    <tr>
                        <td><strong>6110</strong></td>
                        <td>Sweaters, pullovers</td>
                    </tr>
                    <tr>
                        <td><strong>6104</strong></td>
                        <td>Women's suits, knitted</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 15px;'>
                <h4 style='margin-top: 0;'>Need Help?</h4>
                <p style='margin-bottom: 0;'>Our HSN AI Assistant can help you classify products correctly. 
                Just describe your product and get instant HSN code recommendations.</p>
                <button style='background-color: #2196F3; color: white; border: none; padding: 5px 10px; 
                         border-radius: 5px; margin-top: 10px; cursor: pointer;'>
                    Ask HSN Assistant
                </button>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 4: Bulk Operations
    with transaction_tabs[3]:
        st.subheader("Bulk Transaction Operations")
        
        # Options for bulk operations
        operation_type = st.radio(
            "Select Operation Type",
            ["Bulk Import", "Bulk Export", "Bulk Update", "Bulk Validation"],
            horizontal=True
        )
        
        if operation_type == "Bulk Import":
            st.info("Upload a CSV file with transaction data to import multiple transactions at once.")
            
            template_col, upload_col = st.columns(2)
            
            with template_col:
                st.download_button(
                    "Download Template",
                    data="Transaction Type,Date,HSN Code,Product,Quantity,Location\nInward,2023-04-01,6203,Men's Jeans,10,Mumbai\n",
                    file_name="transaction_import_template.csv",
                    mime="text/csv"
                )
            
            with upload_col:
                uploaded_file = st.file_uploader("Upload Transaction CSV", type="csv")
            
            if st.button("Process Bulk Import"):
                st.success("Bulk import initiated. Processing 0 records.")
                
        elif operation_type == "Bulk Export":
            st.info("Export transaction data in bulk for reporting or analysis.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                export_date_range = st.selectbox(
                    "Date Range", 
                    ["Last 7 Days", "Last 30 Days", "Last Quarter", "Last Year", "Custom Range"]
                )
                
                if export_date_range == "Custom Range":
                    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
                    end_date = st.date_input("End Date", value=datetime.now())
            
            with col2:
                export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
                
                fields_to_export = st.multiselect(
                    "Fields to Export",
                    ["Transaction ID", "Date", "HSN Code", "Product Category", "Quantity", 
                     "Transaction Type", "Status", "Location", "Value", "GST Rate"],
                    default=["Transaction ID", "Date", "HSN Code", "Product Category", "Quantity", "Transaction Type"]
                )
            
            if st.button("Generate Export"):
                st.success("Export generated successfully.")
                st.download_button(
                    "Download Export File",
                    data="Transaction ID,Date,HSN Code,Product Category,Quantity,Transaction Type\nTRX-20230401-1234,2023-04-01,6203,Men's Jeans,10,Inward\n",
                    file_name=f"transaction_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
        elif operation_type == "Bulk Update":
            st.info("Update multiple transactions at once.")
            
            update_filter = st.text_area("Enter Transaction IDs (one per line)", 
                                       placeholder="TRX-20230401-1234\nTRX-20230401-1235")
            
            field_to_update = st.selectbox(
                "Field to Update",
                ["Status", "HSN Code", "Quantity", "Transaction Date", "Location"]
            )
            
            new_value = st.text_input(f"New {field_to_update}", placeholder=f"Enter new {field_to_update}")
            
            update_reason = st.text_area("Reason for Update", placeholder="Explain why this bulk update is needed")
            
            if st.button("Process Bulk Update"):
                if update_filter and new_value and update_reason:
                    st.success(f"Bulk update initiated. {len(update_filter.split())} transactions will be updated.")
                else:
                    st.error("Please fill all required fields.")
        
        else:  # Bulk Validation
            st.info("Validate HSN codes for multiple products at once.")
            
            validation_method = st.radio(
                "Validation Method",
                ["Upload Product List", "Select Product Category"],
                horizontal=True
            )
            
            if validation_method == "Upload Product List":
                uploaded_file = st.file_uploader("Upload Product List", type=["csv", "xlsx"])
                
                if uploaded_file:
                    st.success("File uploaded successfully.")
                    st.markdown("### Preview of Uploaded Data")
                    st.dataframe(pd.DataFrame({
                        "Product": ["Men's Jeans", "Women's Top", "Kids T-Shirt", "Formal Shirt", "Casual Shorts"],
                        "Current HSN": ["6203", "6106", "6109", "6205", "6204"],
                        "Status": ["Valid", "Valid", "Valid", "Needs Review", "Valid"]
                    }))
            else:
                selected_category = st.selectbox(
                    "Select Product Category",
                    ["Men's Apparel", "Women's Apparel", "Kids' Apparel", "Accessories"]
                )
                
                if selected_category:
                    st.success(f"Selected category: {selected_category}")
                    st.markdown("### Products in Selected Category")
                    st.dataframe(pd.DataFrame({
                        "Product": ["Men's Jeans", "Formal Trousers", "Casual Shirts", "Formal Shirts", "T-Shirts"],
                        "Current HSN": ["6203", "6203", "6205", "6205", "6109"],
                        "Status": ["Valid", "Valid", "Valid", "Valid", "Valid"]
                    }), use_container_width=True)
            
            if st.button("Run HSN Validation"):
                st.success("Validation completed. 1 item needs review.")
                st.info("Download the validation report for details.")

def show_trend_analysis():
    """Display the real-time trend analysis interface"""
    
    st.subheader("Real-Time Trend Analysis")
    
    # Filter options for the analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_period = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last Quarter", "Last Year", "Year-to-Date"]
        )
    
    with col2:
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Transaction Volume", "HSN Distribution", "Compliance Analysis", "Organic Trends"]
        )
    
    with col3:
        hsn_filter = st.multiselect(
            "Filter by HSN Chapter",
            ["Chapter 61: Knitted Apparel", "Chapter 62: Non-knitted Apparel", 
             "Chapter 63: Other Textiles", "Chapter 42: Leather Goods", "Chapter 64: Footwear"]
        )
    
    # Main analysis visualization
    if analysis_type == "Transaction Volume":
        # Generate date range
        if time_period == "Last 7 Days":
            dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
        elif time_period == "Last 30 Days":
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        elif time_period == "Last Quarter":
            dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
        else:
            dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        
        # Generate transaction data
        transactions_data = pd.DataFrame({
            'Date': dates,
            'Inward': np.random.randint(20, 50, size=len(dates)),
            'Outward': np.random.randint(15, 45, size=len(dates)),
            'Transfer': np.random.randint(5, 15, size=len(dates)),
            'Return': np.random.randint(1, 8, size=len(dates))
        })
        
        # Calculate moving averages
        for col in ['Inward', 'Outward', 'Transfer', 'Return']:
            transactions_data[f'{col}_MA'] = transactions_data[col].rolling(
                window=7 if len(dates) > 10 else 3, 
                min_periods=1
            ).mean()
        
        # Create figure
        fig = go.Figure()
        
        # Add actual data
        fig.add_trace(go.Scatter(
            x=transactions_data['Date'],
            y=transactions_data['Inward'],
            name='Inward',
            mode='markers',
            marker=dict(color='rgba(66, 133, 244, 0.6)', size=8),
            hovertemplate='%{y} transactions<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=transactions_data['Date'],
            y=transactions_data['Outward'],
            name='Outward',
            mode='markers',
            marker=dict(color='rgba(234, 67, 53, 0.6)', size=8),
            hovertemplate='%{y} transactions<extra></extra>'
        ))
        
        # Add trend lines
        fig.add_trace(go.Scatter(
            x=transactions_data['Date'],
            y=transactions_data['Inward_MA'],
            name='Inward Trend',
            line=dict(color='rgb(66, 133, 244)', width=3),
            hovertemplate='%{y:.1f} trend<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=transactions_data['Date'],
            y=transactions_data['Outward_MA'],
            name='Outward Trend',
            line=dict(color='rgb(234, 67, 53)', width=3),
            hovertemplate='%{y:.1f} trend<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            title='Transaction Volume Trend Analysis',
            xaxis_title='Date',
            yaxis_title='Number of Transactions',
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Transaction metrics
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            total_transactions = transactions_data['Inward'].sum() + transactions_data['Outward'].sum() + \
                                transactions_data['Transfer'].sum() + transactions_data['Return'].sum()
            st.metric("Total Transactions", f"{total_transactions:,}", "")
            
        with metric_cols[1]:
            inout_ratio = (transactions_data['Inward'].sum() / transactions_data['Outward'].sum())
            st.metric("Inward/Outward Ratio", f"{inout_ratio:.2f}", 
                      f"{(inout_ratio - 1) * 100:.1f}%" if inout_ratio > 1 else f"{(inout_ratio - 1) * 100:.1f}%")
            
        with metric_cols[2]:
            last_day = transactions_data.iloc[-1]
            daily_change = ((last_day['Inward'] + last_day['Outward']) - 
                           (transactions_data.iloc[-2]['Inward'] + transactions_data.iloc[-2]['Outward']))
            st.metric("Daily Change", f"{daily_change:+d}", f"{daily_change:+d} transactions")
            
        with metric_cols[3]:
            trend_direction = "Up" if transactions_data['Inward_MA'].iloc[-1] > transactions_data['Inward_MA'].iloc[-7 if len(transactions_data) > 7 else -2] else "Down"
            trend_icon = "📈" if trend_direction == "Up" else "📉"
            st.metric("Trend Direction", f"{trend_icon} {trend_direction}", "")
    
    elif analysis_type == "HSN Distribution":
        # Generate HSN distribution data
        hsn_trend_data = pd.DataFrame({
            'Date': pd.date_range(end=datetime.now(), periods=6, freq='M'),
            'Chapter 61': np.random.randint(100, 200, size=6),
            'Chapter 62': np.random.randint(150, 250, size=6),
            'Chapter 63': np.random.randint(50, 100, size=6),
            'Chapter 42': np.random.randint(30, 80, size=6),
            'Chapter 64': np.random.randint(40, 90, size=6)
        })
        
        # Create stacked area chart
        fig = go.Figure()
        
        for column in ['Chapter 61', 'Chapter 62', 'Chapter 63', 'Chapter 42', 'Chapter 64']:
            fig.add_trace(go.Scatter(
                x=hsn_trend_data['Date'],
                y=hsn_trend_data[column],
                mode='lines',
                stackgroup='one',
                name=column,
                hovertemplate='%{y} transactions<extra></extra>'
            ))
        
        fig.update_layout(
            title='HSN Chapter Distribution Over Time',
            xaxis_title='Date',
            yaxis_title='Number of Transactions',
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # HSN code breakdown for the latest period
        st.subheader("HSN Code Breakdown (Latest Period)")
        
        latest_data = pd.DataFrame({
            'HSN Code': ['6109', '6203', '6204', '6110', '6205', '4202', '6403', '6104', '6206', '6201'],
            'Description': ['T-shirts', 'Men's trousers', 'Women's suits', 'Sweaters', 'Men's shirts', 
                           'Handbags', 'Footwear', 'Women's suits (knitted)', 'Women's blouses', 'Men's coats'],
            'Transactions': [152, 143, 128, 87, 76, 68, 54, 47, 42, 38],
            'Growth': [12.3, 8.7, 15.2, -3.5, 5.6, 22.1, 4.8, -2.3, 6.7, 1.2]
        })
        
        fig = px.bar(
            latest_data,
            x='HSN Code',
            y='Transactions',
            color='Growth',
            text='Transactions',
            hover_data=['Description'],
            color_continuous_scale=px.colors.diverging.RdYlGn,
            color_continuous_midpoint=0
        )
        
        fig.update_layout(
            xaxis_title='HSN Code',
            yaxis_title='Number of Transactions',
            height=400,
            coloraxis_colorbar=dict(title='Growth %')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Compliance Analysis":
        # Generate compliance data
        compliance_data = pd.DataFrame({
            'Date': pd.date_range(end=datetime.now(), periods=12, freq='W'),
            'Correct': np.random.uniform(0.85, 0.98, size=12),
            'Needs Review': np.random.uniform(0.01, 0.10, size=12),
            'Incorrect': np.random.uniform(0.01, 0.05, size=12)
        })
        
        # Create stacked area chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=compliance_data['Date'],
            y=compliance_data['Correct'] * 100,
            mode='lines',
            name='Correct',
            line=dict(width=0, color='rgba(76, 175, 80, 0.5)'),
            stackgroup='one',
            groupnorm='percent',
            hovertemplate='%{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=compliance_data['Date'],
            y=compliance_data['Needs Review'] * 100,
            mode='lines',
            name='Needs Review',
            line=dict(width=0, color='rgba(255, 193, 7, 0.5)'),
            stackgroup='one',
            hovertemplate='%{y:.1f}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=compliance_data['Date'],
            y=compliance_data['Incorrect'] * 100,
            mode='lines',
            name='Incorrect',
            line=dict(width=0, color='rgba(244, 67, 54, 0.5)'),
            stackgroup='one',
            hovertemplate='%{y:.1f}%<extra></extra>'
        ))
        
        # Add trend line for correct classifications
        fig.add_trace(go.Scatter(
            x=compliance_data['Date'],
            y=compliance_data['Correct'] * 100,
            mode='lines',
            name='Correct Trend',
            line=dict(color='rgb(76, 175, 80)', width=3),
            hovertemplate='%{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='HSN Compliance Trend Analysis',
            xaxis_title='Date',
            yaxis_title='Percentage',
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Common compliance issues
        st.subheader("Common Compliance Issues")
        
        issues_data = pd.DataFrame({
            'Issue': [
                'Misclassification between Chapters 61 and 62',
                'Incorrect categorization of blended fabric items',
                'Using general codes instead of specific ones',
                'Confusion between clothing and accessories codes',
                'Using outdated HSN codes'
            ],
            'Frequency': [28, 22, 17, 14, 9],
            'Impact': ['High', 'Medium', 'Medium', 'Low', 'High']
        })
        
        impact_colors = {'High': '#F44336', 'Medium': '#FFC107', 'Low': '#4CAF50'}
        issues_data['Color'] = issues_data['Impact'].map(impact_colors)
        
        fig = px.bar(
            issues_data,
            x='Frequency',
            y='Issue',
            color='Impact',
            color_discrete_map=impact_colors,
            text='Frequency',
            orientation='h'
        )
        
        fig.update_layout(
            xaxis_title='Frequency',
            yaxis_title='',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:  # Organic Trends
        st.subheader("Organic Trend Analysis")
        
        st.info("""
        Organic trend analysis looks at natural patterns in your transaction data without predetermined categories. 
        This can help identify unexpected correlations and emerging patterns.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            correlation_type = st.selectbox(
                "Correlation Analysis",
                ["HSN Code vs. Transaction Volume", "Time of Day vs. Error Rate", 
                 "User vs. HSN Accuracy", "Seasonal Patterns"]
            )
        
        with col2:
            insight_depth = st.slider("Analysis Depth", 1, 5, 3)
        
        # Generate organic trend visualization
        if correlation_type == "HSN Code vs. Transaction Volume":
            # Generate sample data
            hsn_volume_data = pd.DataFrame({
                'HSN Code': ['6109', '6203', '6204', '6110', '6205', '4202', '6403', '6104', '6206', '6201'],
                'Transaction Volume': np.random.randint(50, 200, 10),
                'Error Rate': np.random.uniform(0.01, 0.08, 10),
                'Processing Time': np.random.uniform(1, 5, 10)
            })
            
            fig = px.scatter(
                hsn_volume_data,
                x='Transaction Volume',
                y='Error Rate',
                size='Processing Time',
                color='Transaction Volume',
                hover_name='HSN Code',
                color_continuous_scale=px.colors.sequential.Viridis,
                size_max=20,
                title='Transaction Volume vs. Error Rate by HSN Code'
            )
            
            fig.update_layout(
                xaxis_title='Transaction Volume',
                yaxis_title='Error Rate',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Generate insights based on depth
            if insight_depth >= 3:
                st.subheader("Automated Insights")
                
                st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                    <h4 style='margin-top: 0;'>Key Observations</h4>
                    <ul>
                        <li><strong>High Volume, Low Error:</strong> HSN codes 6109 and 6203 show high transaction volume with relatively low error rates, suggesting established familiarity.</li>
                        <li><strong>High Volume, High Error:</strong> HSN code 6204 shows high activity but elevated error rates, suggesting potential classification confusion.</li>
                        <li><strong>Processing Time Correlation:</strong> Higher processing times generally correlate with higher error rates, suggesting complex classifications require more attention.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            if insight_depth >= 4:
                st.markdown("""
                <div style='background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                    <h4 style='margin-top: 0;'>Recommendations</h4>
                    <ol>
                        <li>Create targeted training materials for HSN code 6204 to reduce error rates.</li>
                        <li>Implement automated suggestions for high-error HSN codes during transaction entry.</li>
                        <li>Review and optimize the classification process for items with longer processing times.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
        
        elif correlation_type == "Time of Day vs. Error Rate":
            # Generate hourly data
            hours = list(range(9, 18))  # 9 AM to 5 PM
            hourly_data = pd.DataFrame({
                'Hour': hours,
                'Transactions': [random.randint(15, 50) for _ in hours],
                'Error Rate': [random.uniform(0.02, 0.08) for _ in hours],
                'Staff Count': [random.randint(3, 8) for _ in hours]
            })
            
            # Add hour labels
            hourly_data['Time'] = [f"{hour}:00" for hour in hours]
            
            # Create plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(
                    x=hourly_data['Time'],
                    y=hourly_data['Transactions'],
                    name='Transactions',
                    marker_color='rgba(66, 133, 244, 0.7)'
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hourly_data['Time'],
                    y=hourly_data['Error Rate'] * 100,
                    name='Error Rate (%)',
                    mode='lines+markers',
                    marker=dict(color='red'),
                    line=dict(width=3)
                ),
                secondary_y=True
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hourly_data['Time'],
                    y=hourly_data['Staff Count'],
                    name='Staff Count',
                    mode='lines+markers',
                    marker=dict(color='green'),
                    line=dict(width=3, dash='dot')
                ),
                secondary_y=False
            )
            
            fig.update_layout(
                title='Transaction Volume and Error Rate by Time of Day',
                xaxis_title='Time of Day',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=500,
                hovermode='x unified'
            )
            
            fig.update_yaxes(title_text="Transactions / Staff", secondary_y=False)
            fig.update_yaxes(title_text="Error Rate (%)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add insights based on depth
            if insight_depth >= 2:
                st.subheader("Time-based Pattern Insights")
                
                st.markdown("""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                    <h4 style='margin-top: 0;'>Observed Patterns</h4>
                    <ul>
                        <li><strong>Peak Error Times:</strong> Error rates peak during mid-day (12:00-14:00) and late afternoon (16:00-17:00).</li>
                        <li><strong>Staff-to-Error Correlation:</strong> Error rates tend to increase when the staff-to-transaction ratio decreases.</li>
                        <li><strong>High Volume Impact:</strong> Peak transaction periods often correspond with elevated error rates.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            if insight_depth >= 5:
                st.markdown("""
                <div style='background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                    <h4 style='margin-top: 0;'>Advanced Recommendations</h4>
                    <ol>
                        <li>Adjust staffing to add more experienced personnel during high-error time windows.</li>
                        <li>Implement a "quiet hour" with reduced transaction targets during peak error periods.</li>
                        <li>Schedule HSN refresher training for staff working during high-error periods.</li>
                        <li>Consider a short "mindfulness break" before the afternoon error peak to reset focus.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Generate seasonal pattern data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            seasonal_data = pd.DataFrame({
                'Month': months,
                'Transaction Volume': [
                    random.randint(800, 1000),  # Jan
                    random.randint(700, 900),   # Feb
                    random.randint(900, 1100),  # Mar
                    random.randint(800, 1000),  # Apr
                    random.randint(900, 1100),  # May
                    random.randint(1000, 1200), # Jun
                    random.randint(1100, 1300), # Jul
                    random.randint(1200, 1400), # Aug
                    random.randint(1300, 1500), # Sep
                    random.randint(1400, 1600), # Oct
                    random.randint(1600, 1800), # Nov
                    random.randint(1700, 1900)  # Dec
                ],
                'HSN Changes': [
                    random.randint(5, 15),      # Jan
                    random.randint(10, 20),     # Feb
                    random.randint(15, 25),     # Mar
                    random.randint(5, 15),      # Apr
                    random.randint(5, 15),      # May
                    random.randint(10, 20),     # Jun
                    random.randint(5, 15),      # Jul
                    random.randint(5, 15),      # Aug
                    random.randint(20, 30),     # Sep
                    random.randint(15, 25),     # Oct
                    random.randint(25, 35),     # Nov
                    random.randint(10, 20)      # Dec
                ],
                'Error Rate': [
                    random.uniform(0.03, 0.05), # Jan
                    random.uniform(0.04, 0.06), # Feb
                    random.uniform(0.05, 0.07), # Mar
                    random.uniform(0.03, 0.05), # Apr
                    random.uniform(0.02, 0.04), # May
                    random.uniform(0.04, 0.06), # Jun
                    random.uniform(0.03, 0.05), # Jul
                    random.uniform(0.02, 0.04), # Aug
                    random.uniform(0.05, 0.07), # Sep
                    random.uniform(0.04, 0.06), # Oct
                    random.uniform(0.06, 0.08), # Nov
                    random.uniform(0.04, 0.06)  # Dec
                ]
            })
            
            # Add month order for sorting
            month_order = {month: i for i, month in enumerate(months)}
            seasonal_data['MonthOrder'] = seasonal_data['Month'].map(month_order)
            seasonal_data = seasonal_data.sort_values('MonthOrder')
            
            # Create figure
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add traces
            fig.add_trace(
                go.Scatter(
                    x=seasonal_data['Month'],
                    y=seasonal_data['Transaction Volume'],
                    name='Transaction Volume',
                    mode='lines+markers',
                    marker=dict(color='blue'),
                    line=dict(width=3)
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Bar(
                    x=seasonal_data['Month'],
                    y=seasonal_data['HSN Changes'],
                    name='HSN Changes',
                    marker_color='rgba(75, 0, 130, 0.6)'
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=seasonal_data['Month'],
                    y=seasonal_data['Error Rate'] * 100,
                    name='Error Rate (%)',
                    mode='lines+markers',
                    marker=dict(color='red'),
                    line=dict(width=3)
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title='Seasonal Patterns in Transaction Volume and HSN Changes',
                xaxis_title='Month',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=500,
                hovermode='x unified'
            )
            
            fig.update_yaxes(title_text="Transaction Volume / HSN Changes", secondary_y=False)
            fig.update_yaxes(title_text="Error Rate (%)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add seasonal insights
            st.subheader("Seasonal Pattern Recognition")
            
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                <h4 style='margin-top: 0;'>Seasonal Insights</h4>
                <ul>
                    <li><strong>Festive Season Impact:</strong> Transaction volumes peak during September-December, likely due to festival and holiday season.</li>
                    <li><strong>HSN Change Patterns:</strong> Significant HSN classification changes occur in September and November, correlating with new product introductions.</li>
                    <li><strong>Error Rate Correlation:</strong> Error rates increase during both high volume periods and when there are significant HSN changes.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if insight_depth >= 4:
                st.markdown("""
                <div style='background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                    <h4 style='margin-top: 0;'>Predictive Insights</h4>
                    <p>Based on historical patterns, we predict:</p>
                    <ol>
                        <li>Q4 will continue to show the highest transaction volumes and will benefit from additional staffing.</li>
                        <li>September will remain a critical month for HSN classification changes, requiring targeted training in August.</li>
                        <li>Error rates can be reduced by 25% by proactively addressing seasonal patterns with targeted interventions.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)

def show_gamified_leaderboard():
    """Display the gamified inventory management leaderboards"""
    
    st.subheader("Inventory Management Leaderboards")
    
    # Create tabs for different leaderboard categories
    leaderboard_tabs = st.tabs([
        "Team Performance", 
        "Individual Rankings", 
        "HSN Accuracy", 
        "Achievements"
    ])
    
    # Tab 1: Team Performance
    with leaderboard_tabs[0]:
        st.subheader("Team Performance Leaderboard")
        
        # Time period filter
        period = st.selectbox(
            "Timeframe",
            ["This Week", "This Month", "This Quarter", "Year to Date", "All Time"],
            index=1
        )
        
        # Generate team performance data
        team_data = pd.DataFrame({
            'Rank': [1, 2, 3, 4, 5],
            'Team': ['Mumbai Team A', 'Delhi Team B', 'Bangalore Team A', 'Mumbai Team B', 'Chennai Team A'],
            'Transactions': [487, 423, 389, 352, 318],
            'Accuracy': [97.8, 96.5, 95.2, 94.8, 93.9],
            'Efficiency': [94, 91, 88, 86, 85],
            'Score': [9452, 8938, 8621, 8457, 8305]
        })
        
        # Create a more engaging visualization of the team leaderboard
        fig = go.Figure()
        
        # Add bars for the scores
        fig.add_trace(go.Bar(
            x=team_data['Team'],
            y=team_data['Score'],
            marker_color=['gold', 'silver', '#cd7f32', '#a9a9a9', '#a9a9a9'],  # Gold, Silver, Bronze, Grey, Grey
            width=0.6,
            hovertemplate='<b>%{x}</b><br>Score: %{y}<extra></extra>'
        ))
        
        # Add markers for accuracy
        fig.add_trace(go.Scatter(
            x=team_data['Team'],
            y=team_data['Accuracy'],
            mode='markers',
            marker=dict(
                size=20,
                color=team_data['Accuracy'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Accuracy (%)'),
                line=dict(width=2, color='white')
            ),
            name='Accuracy',
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Accuracy: %{y}%<extra></extra>'
        ))
        
        # Update layout with dual y-axes
        fig.update_layout(
            title=f'Team Performance Leaderboard - {period}',
            xaxis=dict(title='Team'),
            yaxis=dict(title='Total Score', range=[min(team_data['Score'])*0.9, max(team_data['Score'])*1.1]),
            yaxis2=dict(
                title='Accuracy (%)',
                overlaying='y',
                side='right',
                range=[90, 100],
                tickvals=[90, 92, 94, 96, 98, 100],
                tickfont=dict(color='darkblue')
            ),
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Team performance details
        st.subheader("Team Performance Details")
        
        # Show top team details
        st.markdown("""
        <div style='background: linear-gradient(90deg, rgba(255,215,0,0.2) 0%, rgba(255,215,0,0.05) 100%); 
                  padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid gold;'>
            <h3 style='margin-top: 0;'>🏆 Mumbai Team A</h3>
            <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
                <div style='flex: 1; min-width: 120px;'>
                    <p style='font-size: 0.8em; margin-bottom: 5px;'>Total Score</p>
                    <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>9,452</p>
                </div>
                <div style='flex: 1; min-width: 120px;'>
                    <p style='font-size: 0.8em; margin-bottom: 5px;'>Transactions</p>
                    <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>487</p>
                </div>
                <div style='flex: 1; min-width: 120px;'>
                    <p style='font-size: 0.8em; margin-bottom: 5px;'>Accuracy</p>
                    <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>97.8%</p>
                </div>
                <div style='flex: 1; min-width: 120px;'>
                    <p style='font-size: 0.8em; margin-bottom: 5px;'>Efficiency</p>
                    <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>94/100</p>
                </div>
            </div>
            <p style='margin-top: 15px;'><strong>Top Achievement:</strong> Perfect Week (100% accuracy for 7 consecutive days)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Team specific highlights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Team Achievements")
            
            achievements = [
                {"team": "Mumbai Team A", "achievement": "HSN Mastery", "description": "100% accuracy for 500+ transactions"},
                {"team": "Delhi Team B", "achievement": "Efficiency Expert", "description": "Highest transactions per hour rate"},
                {"team": "Bangalore Team A", "achievement": "Comeback Kings", "description": "Most improved team this month"},
                {"team": "Mumbai Team B", "achievement": "Zero Errors", "description": "No HSN errors for 3 consecutive days"}
            ]
            
            for achievement in achievements:
                st.markdown(f"""
                <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <p style='margin: 0;'><strong>{achievement['achievement']}</strong></p>
                            <p style='margin: 0; font-size: 0.8em;'>{achievement['description']}</p>
                        </div>
                        <div>
                            <p style='margin: 0; color: #666;'>{achievement['team']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Improvement Opportunities")
            
            # Create a radar chart for team skill comparison
            categories = ['HSN Accuracy', 'Processing Speed', 'Documentation', 'Problem Solving', 'Teamwork']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[98, 85, 90, 88, 95],
                theta=categories,
                fill='toself',
                name='Top Team'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[94, 92, 82, 95, 85],
                theta=categories,
                fill='toself',
                name='Your Team'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[70, 100]
                    )),
                showlegend=True,
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Individual Rankings
    with leaderboard_tabs[1]:
        st.subheader("Individual Performance Rankings")
        
        # Filters for individual rankings
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ind_period = st.selectbox(
                "Timeframe",
                ["This Week", "This Month", "This Quarter", "Year to Date"],
                key="ind_period"
            )
        
        with col2:
            ind_team = st.selectbox(
                "Team",
                ["All Teams", "Mumbai Team A", "Delhi Team B", "Bangalore Team A", "Mumbai Team B", "Chennai Team A"]
            )
        
        with col3:
            ind_metric = st.selectbox(
                "Ranking Metric",
                ["Overall Score", "Transaction Volume", "HSN Accuracy", "Processing Speed"]
            )
        
        # Generate individual performance data
        individual_data = pd.DataFrame({
            'Rank': list(range(1, 11)),
            'Name': [
                "Rajesh Singh", "Priya Sharma", "Aditya Patel", "Neha Gupta", "Vikram Desai",
                "Ananya Reddy", "Sanjay Kumar", "Deepika Shah", "Arjun Mehta", "Kavita Joshi"
            ],
            'Team': [
                "Mumbai Team A", "Delhi Team B", "Mumbai Team A", "Bangalore Team A", "Mumbai Team B",
                "Chennai Team A", "Delhi Team B", "Mumbai Team A", "Bangalore Team A", "Mumbai Team B"
            ],
            'Transactions': [127, 118, 113, 109, 104, 98, 95, 93, 91, 89],
            'Accuracy': [99.2, 97.8, 98.5, 96.7, 98.1, 95.8, 97.2, 98.9, 96.2, 95.5],
            'Speed': [3.2, 2.8, 3.5, 3.1, 2.9, 3.0, 3.3, 2.7, 3.2, 3.4],  # minutes per transaction
            'Score': [1250, 1220, 1180, 1150, 1120, 1080, 1050, 1020, 990, 960]
        })
        
        # Apply filters
        if ind_team != "All Teams":
            individual_data = individual_data[individual_data['Team'] == ind_team]
            
        # Sort based on selected metric
        if ind_metric == "Transaction Volume":
            individual_data = individual_data.sort_values('Transactions', ascending=False)
        elif ind_metric == "HSN Accuracy":
            individual_data = individual_data.sort_values('Accuracy', ascending=False)
        elif ind_metric == "Processing Speed":
            individual_data = individual_data.sort_values('Speed')
        else:  # Overall Score
            individual_data = individual_data.sort_values('Score', ascending=False)
        
        # Update ranks after filtering and sorting
        individual_data['Rank'] = range(1, len(individual_data) + 1)
        
        # Create an engaging leaderboard visualization
        fig = px.bar(
            individual_data.head(10),
            x='Name',
            y='Score' if ind_metric == "Overall Score" else 
              'Transactions' if ind_metric == "Transaction Volume" else
              'Accuracy' if ind_metric == "HSN Accuracy" else 'Speed',
            color='Team',
            text='Rank',
            title=f'Top Performers by {ind_metric} - {ind_period}',
            hover_data=['Accuracy', 'Transactions', 'Speed'],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(textposition='outside')
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title=ind_metric,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Individual badges and achievements
        st.subheader("Individual Achievements & Badges")
        
        # Show user badges in a grid
        badge_data = [
            {"name": "Rajesh Singh", "badge": "HSN Master", "icon": "🏅", "color": "#ffd700", "level": 5},
            {"name": "Priya Sharma", "badge": "Speed Demon", "icon": "⚡", "color": "#4b0082", "level": 4},
            {"name": "Aditya Patel", "badge": "Accuracy King", "icon": "🎯", "color": "#4caf50", "level": 4},
            {"name": "Vikram Desai", "badge": "Problem Solver", "icon": "🧩", "color": "#2196f3", "level": 3},
            {"name": "Deepika Shah", "badge": "Team Player", "icon": "🤝", "color": "#ff9800", "level": 5},
            {"name": "Neha Gupta", "badge": "Rising Star", "icon": "🌟", "color": "#9c27b0", "level": 2}
        ]
        
        # Display badges in a grid
        cols = st.columns(3)
        
        for i, badge in enumerate(badge_data):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {badge['color']}20 0%, {badge['color']}05 100%); 
                            border: 1px solid {badge['color']}; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                    <div style='font-size: 2em; text-align: center; margin-bottom: 10px;'>{badge['icon']}</div>
                    <h4 style='margin: 0; text-align: center;'>{badge['badge']}</h4>
                    <p style='margin: 5px 0 0 0; text-align: center; font-size: 0.8em;'>Level {badge['level']}</p>
                    <p style='margin: 5px 0 0 0; text-align: center; color: #666;'>{badge['name']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Progress tracking
        st.subheader("Your Progress Tracking")
        
        # Placeholder for user's personal stats
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Personal stats
            st.markdown("""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                <h4 style='margin-top: 0;'>Your Status</h4>
                <div style='display: flex; flex-wrap: wrap; gap: 15px;'>
                    <div style='flex: 1; min-width: 120px;'>
                        <p style='font-size: 0.8em; margin-bottom: 5px;'>Current Rank</p>
                        <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>7th</p>
                    </div>
                    <div style='flex: 1; min-width: 120px;'>
                        <p style='font-size: 0.8em; margin-bottom: 5px;'>Points to Next Rank</p>
                        <p style='font-weight: bold; font-size: 1.5em; margin: 0;'>32</p>
                    </div>
                    <div style='flex: 1; min-width: 120px;'>
                        <p style='font-size: 0.8em; margin-bottom: 5px;'>Weekly Change</p>
                        <p style='font-weight: bold; font-size: 1.5em; margin: 0; color: green;'>+2 ↑</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress to next badge
            st.markdown("""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px;'>
                <h4 style='margin-top: 0;'>Next Badge: HSN Expert (Level 3)</h4>
                <div style='margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                        <span>Progress</span>
                        <span>72%</span>
                    </div>
                    <div style='height: 8px; background-color: #f1f1f1; border-radius: 4px;'>
                        <div style='width: 72%; height: 8px; background-color: #4CAF50; border-radius: 4px;'></div>
                    </div>
                </div>
                <p style='margin: 10px 0 5px 0;'>Requirements:</p>
                <ul style='margin-top: 0;'>
                    <li><span style='color: green;'>✓</span> Process 100+ transactions (Completed: 127)</li>
                    <li><span style='color: green;'>✓</span> Maintain 95%+ accuracy (Current: 97.2%)</li>
                    <li><span style='color: orange;'>⌛</span> Complete HSN advanced training (2/3 modules completed)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Challenges and competitions
            st.markdown("""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                <h4 style='margin-top: 0;'>Active Challenges</h4>
                <div style='border-left: 3px solid #FFC107; padding-left: 10px; margin-bottom: 10px;'>
                    <p style='margin: 0;'><strong>Speed Week</strong></p>
                    <p style='margin: 0; font-size: 0.8em;'>Process 20 transactions in a day</p>
                    <p style='margin: 0; font-size: 0.8em; color: #666;'>Reward: 50 points</p>
                </div>
                <div style='border-left: 3px solid #4CAF50; padding-left: 10px;'>
                    <p style='margin: 0;'><strong>Perfect Streak</strong></p>
                    <p style='margin: 0; font-size: 0.8em;'>5 days of 100% HSN accuracy</p>
                    <p style='margin: 0; font-size: 0.8em; color: #666;'>Reward: Accuracy Badge Level Up</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips for improvement
            st.markdown("""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px;'>
                <h4 style='margin-top: 0;'>Tips to Improve</h4>
                <ul style='margin-top: 0; padding-left: 20px;'>
                    <li>Complete the HSN advanced training module</li>
                    <li>Focus on processing speed without sacrificing accuracy</li>
                    <li>Join the daily 15-minute HSN classification practice</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 3: HSN Accuracy
    with leaderboard_tabs[2]:
        st.subheader("HSN Accuracy Leaderboard")
        
        # Filter for HSN accuracy view
        hsn_period = st.selectbox(
            "Timeframe",
            ["This Week", "This Month", "This Quarter", "Year to Date"],
            key="hsn_period"
        )
        
        # Generate HSN accuracy data
        hsn_data = pd.DataFrame({
            'HSN Chapter': ['Chapter 61', 'Chapter 62', 'Chapter 63', 'Chapter 42', 'Chapter 64'],
            'Description': ['Knitted apparel', 'Non-knitted apparel', 'Other textiles', 'Leather goods', 'Footwear'],
            'Transactions': [425, 312, 187, 142, 93],
            'Correct': [408, 292, 178, 130, 87],
            'Accuracy': [96.0, 93.6, 95.2, 91.5, 93.5]
        })
        
        # Add error counts
        hsn_data['Errors'] = hsn_data['Transactions'] - hsn_data['Correct']
        
        # Calculate accuracy
        hsn_data['Accuracy'] = (hsn_data['Correct'] / hsn_data['Transactions'] * 100).round(1)
        
        # Create the accuracy chart
        fig = go.Figure()
        
        # Add bars for accuracy
        fig.add_trace(go.Bar(
            x=hsn_data['HSN Chapter'],
            y=hsn_data['Accuracy'],
            marker_color='rgba(0, 123, 255, 0.7)',
            name='Accuracy (%)'
        ))
        
        # Add line for transaction volume
        fig.add_trace(go.Scatter(
            x=hsn_data['HSN Chapter'],
            y=hsn_data['Transactions'],
            mode='lines+markers',
            marker=dict(size=10),
            line=dict(width=3, color='orange'),
            name='Transactions',
            yaxis='y2'
        ))
        
        # Configure dual y-axes
        fig.update_layout(
            title=f'HSN Chapter Accuracy - {hsn_period}',
            xaxis_title='HSN Chapter',
            yaxis=dict(
                title='Accuracy (%)',
                range=[85, 100],
            ),
            yaxis2=dict(
                title='Transaction Volume',
                titlefont=dict(color='orange'),
                tickfont=dict(color='orange'),
                anchor='x',
                overlaying='y',
                side='right',
                range=[0, max(hsn_data['Transactions']) * 1.2]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Common error patterns
        st.subheader("Common HSN Classification Errors")
        
        error_data = [
            {"category": "Chapter 61 vs 62", "description": "Confusion between knitted and non-knitted apparel", "frequency": 37, "impact": "High"},
            {"category": "Section vs Chapter", "description": "Using section codes instead of specific chapter codes", "frequency": 28, "impact": "Medium"},
            {"category": "Material Classification", "description": "Incorrect identification of material composition", "frequency": 24, "impact": "High"},
            {"category": "Accessories vs Apparel", "description": "Misclassifying accessories as apparel", "frequency": 18, "impact": "Low"},
            {"category": "Digit Errors", "description": "Transposition or incorrect digit entry", "frequency": 15, "impact": "Medium"}
        ]
        
        # Create a markdown table for error patterns
        st.markdown("""
        | Error Category | Description | Frequency | Impact |
        |----------------|-------------|-----------|--------|""")
        
        for error in error_data:
            impact_color = {
                "High": "🔴", 
                "Medium": "🟠", 
                "Low": "🟢"
            }[error["impact"]]
            
            st.markdown(f"""| {error["category"]} | {error["description"]} | {error["frequency"]} | {impact_color} {error["impact"]} |""")
        
        # HSN accuracy improvement initiatives
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Most Improved HSN Categories")
            
            improvement_data = pd.DataFrame({
                'HSN Code': ['6109', '6204', '6403', '6110', '4202'],
                'Description': ['T-shirts', 'Women's suits', 'Footwear', 'Sweaters', 'Handbags'],
                'Previous': [88.5, 90.2, 85.7, 92.1, 89.3],
                'Current': [97.8, 95.6, 90.2, 96.0, 92.4],
                'Improvement': [9.3, 5.4, 4.5, 3.9, 3.1]
            })
            
            # Create a horizontal bar chart for improvements
            fig = px.bar(
                improvement_data,
                y='HSN Code',
                x='Improvement',
                color='Improvement',
                color_continuous_scale='Viridis',
                text='Improvement',
                orientation='h',
                hover_data=['Description', 'Previous', 'Current']
            )
            
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            
            fig.update_layout(
                yaxis_title='',
                xaxis_title='Improvement (%)',
                coloraxis_showscale=False,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Training Impact on Accuracy")
            
            # Generate training impact data
            training_data = pd.DataFrame({
                'Week': list(range(1, 11)),
                'With Training': [92.5, 93.8, 94.2, 95.7, 96.3, 96.8, 97.2, 97.5, 97.8, 98.1],
                'Without Training': [92.5, 92.3, 92.5, 92.1, 92.8, 92.4, 93.0, 92.7, 93.1, 92.9]
            })
            
            # Create line chart for training impact
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=training_data['Week'],
                y=training_data['With Training'],
                mode='lines+markers',
                name='With Training',
                line=dict(color='green', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=training_data['Week'],
                y=training_data['Without Training'],
                mode='lines+markers',
                name='Without Training',
                line=dict(color='gray', width=3, dash='dot')
            ))
            
            # Add area to highlight the difference
            fig.add_trace(go.Scatter(
                x=training_data['Week'].tolist() + training_data['Week'].tolist()[::-1],
                y=training_data['With Training'].tolist() + training_data['Without Training'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(0, 200, 0, 0.2)',
                line=dict(color='rgba(255, 255, 255, 0)'),
                hoverinfo='skip',
                showlegend=False
            ))
            
            fig.update_layout(
                xaxis_title='Week',
                yaxis_title='Accuracy (%)',
                yaxis=dict(range=[90, 100]),
                height=300,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Achievements
    with leaderboard_tabs[3]:
        st.subheader("Achievements & Rewards")
        
        # Create a tabular view of available achievements
        achievement_data = [
            {"name": "HSN Master", "description": "Maintain 99%+ HSN accuracy for a month", "points": 500, "badge": "🏅"},
            {"name": "Speed Demon", "description": "Process 100+ transactions in a week", "points": 300, "badge": "⚡"},
            {"name": "Perfect Week", "description": "100% accuracy for a full week", "points": 250, "badge": "🎯"},
            {"name": "Consistency King", "description": "30 consecutive days of activity", "points": 200, "badge": "📆"},
            {"name": "Team Player", "description": "Help train 3+ team members", "points": 150, "badge": "🤝"},
            {"name": "HSN Explorer", "description": "Work with 20+ different HSN codes", "points": 100, "badge": "🔍"},
            {"name": "Rising Star", "description": "Improve accuracy by 5% in a month", "points": 100, "badge": "🌟"},
            {"name": "Quick Start", "description": "Process 10+ transactions on your first day", "points": 50, "badge": "🚀"}
        ]
        
        # Display achievements in cards
        achievement_cols = st.columns(2)
        
        for i, achievement in enumerate(achievement_data):
            with achievement_cols[i % 2]:
                st.markdown(f"""
                <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                    <div style='display: flex; align-items: center;'>
                        <div style='font-size: 2em; margin-right: 15px;'>{achievement['badge']}</div>
                        <div>
                            <h4 style='margin: 0;'>{achievement['name']}</h4>
                            <p style='margin: 5px 0 0 0; font-size: 0.9em;'>{achievement['description']}</p>
                        </div>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-top: 10px;'>
                        <span style='font-weight: bold;'>{achievement['points']} points</span>
                        <button style='background-color: #4B0082; color: white; border: none; padding: 5px 10px; 
                                 border-radius: 5px; cursor: pointer;'>Track Progress</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Weekly challenges section
        st.subheader("This Week's Challenges")
        
        challenge_data = [
            {"name": "HSN Sprint", "description": "Process 50 transactions with 95%+ accuracy", "reward": "150 points + Speed Badge", "deadline": "3 days left", "progress": 65},
            {"name": "Chapter Champion", "description": "Correctly classify 25 items in Chapter 62", "reward": "100 points", "deadline": "5 days left", "progress": 40},
            {"name": "Error Hunter", "description": "Identify and correct 10 HSN errors", "reward": "75 points", "deadline": "7 days left", "progress": 20}
        ]
        
        for challenge in challenge_data:
            st.markdown(f"""
            <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='margin: 0;'>{challenge['name']}</h4>
                    <span style='color: #FF5722;'>{challenge['deadline']}</span>
                </div>
                <p style='margin: 10px 0;'>{challenge['description']}</p>
                <div style='margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                        <span>Progress</span>
                        <span>{challenge['progress']}%</span>
                    </div>
                    <div style='height: 8px; background-color: #f1f1f1; border-radius: 4px;'>
                        <div style='width: {challenge['progress']}%; height: 8px; background-color: #4CAF50; border-radius: 4px;'></div>
                    </div>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='font-weight: bold;'>Reward: {challenge['reward']}</span>
                    <button style='background-color: #4B0082; color: white; border: none; padding: 5px 10px; 
                             border-radius: 5px; cursor: pointer;'>View Details</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reward redemption section
        st.subheader("Redeem Your Points")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
                <h3 style='margin-top: 0; text-align: center;'>Your Balance</h3>
                <p style='font-size: 2em; text-align: center; margin: 0;'>1,250</p>
                <p style='text-align: center; margin: 0; color: #666;'>points</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            reward_data = [
                {"name": "Extra Day Off", "cost": 2000, "icon": "🏖️"},
                {"name": "Team Lunch", "cost": 1500, "icon": "🍕"},
                {"name": "Company Swag", "cost": 1000, "icon": "👕"},
                {"name": "Coffee Voucher", "cost": 500, "icon": "☕"}
            ]
            
            reward_cols = st.columns(4)
            
            for i, reward in enumerate(reward_data):
                with reward_cols[i]:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; border-radius: 5px; 
                                border: 1px solid {'#ddd' if reward['cost'] > 1250 else '#4CAF50'};
                                {"color: #999;" if reward['cost'] > 1250 else ""}'>
                        <div style='font-size: 2em;'>{reward['icon']}</div>
                        <p style='margin: 5px 0;'>{reward['name']}</p>
                        <p style='margin: 5px 0; font-weight: bold;'>{reward['cost']} pts</p>
                        <button style='background-color: {'#f1f1f1' if reward['cost'] > 1250 else '#4CAF50'}; 
                                 color: {'#999' if reward['cost'] > 1250 else 'white'}; 
                                 border: none; padding: 5px 10px; border-radius: 5px; 
                                 cursor: {"not-allowed" if reward['cost'] > 1250 else "pointer"};'
                                 ${"disabled" if reward['cost'] > 1250 else ""}>
                            {"Redeem" if reward['cost'] <= 1250 else "Locked"}
                        </button>
                    </div>
                    """, unsafe_allow_html=True)

def generate_sample_transactions(count=10, hsn_code=None):
    """Generate sample transaction data"""
    
    transaction_types = ["Inward", "Outward", "Transfer", "Return"]
    status_options = ["Completed", "Pending", "Cancelled", "On Hold"]
    hsn_codes = ["6109", "6203", "6204", "6110", "6205", "4202", "6403", "6104", "6206", "6201"]
    product_categories = [
        "T-shirts", "Men's trousers", "Women's suits", "Sweaters", "Men's shirts",
        "Handbags", "Footwear", "Women's suits (knitted)", "Women's blouses", "Men's coats"
    ]
    
    # Create a mapping from HSN code to product category
    hsn_to_product = dict(zip(hsn_codes, product_categories))
    
    # Generate random transactions
    transactions = []
    
    for i in range(count):
        # Use provided HSN code or random one
        current_hsn = hsn_code if hsn_code else random.choice(hsn_codes)
        current_product = hsn_to_product[current_hsn]
        
        transaction_id = f"TRX-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        transaction_type = random.choice(transaction_types)
        quantity = random.randint(5, 50)
        status = random.choices(status_options, weights=[0.7, 0.2, 0.05, 0.05])[0]
        
        transactions.append({
            "Transaction ID": transaction_id,
            "Date": date,
            "HSN Code": current_hsn,
            "Product Category": current_product,
            "Quantity": quantity,
            "Transaction Type": transaction_type,
            "Status": status,
            "Location": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad"]),
            "Value": quantity * random.randint(500, 2000)
        })
    
    return pd.DataFrame(transactions)

def generate_hsn_distribution():
    """Generate HSN distribution data for visualization"""
    
    # Define HSN sections, chapters, and codes
    sections = {
        "Section XI": "Textiles and textile articles",
        "Section VIII": "Raw hides, leather, furskins",
        "Section XII": "Footwear, headgear, umbrellas"
    }
    
    # Chapters within sections
    chapters = {
        "Section XI": {
            "Chapter 61": "Knitted or crocheted apparel",
            "Chapter 62": "Non-knitted apparel",
            "Chapter 63": "Other textile articles"
        },
        "Section VIII": {
            "Chapter 42": "Leather articles"
        },
        "Section XII": {
            "Chapter 64": "Footwear"
        }
    }
    
    # HSN codes within chapters
    hsn_codes = {
        "Chapter 61": {
            "6109": "T-shirts, knitted",
            "6110": "Sweaters, pullovers",
            "6104": "Women's suits, knitted"
        },
        "Chapter 62": {
            "6203": "Men's suits, not knitted",
            "6204": "Women's suits, not knitted",
            "6205": "Men's shirts, not knitted"
        },
        "Chapter 63": {
            "6302": "Bed linen, table linen",
            "6305": "Sacks and bags"
        },
        "Chapter 42": {
            "4202": "Trunks, suitcases, handbags"
        },
        "Chapter 64": {
            "6403": "Footwear with leather uppers",
            "6404": "Footwear with textile uppers"
        }
    }
    
    # Generate distribution data
    dist_data = []
    
    for section, section_desc in sections.items():
        for chapter in chapters.get(section, {}):
            chapter_desc = chapters[section][chapter]
            
            for hsn_code in hsn_codes.get(chapter, {}):
                hsn_desc = hsn_codes[chapter][hsn_code]
                
                # Generate random count and value
                count = random.randint(20, 200)
                value = count * random.randint(1000, 5000)
                
                dist_data.append({
                    "HSN Section": section,
                    "HSN Chapter": chapter,
                    "HSN Code": hsn_code,
                    "Description": hsn_desc,
                    "Transaction Count": count,
                    "Value": value
                })
    
    return pd.DataFrame(dist_data)

# Function to make subplots when needed
def make_subplots(specs=None):
    """Create plotly subplots with dual y-axes"""
    # Create a basic figure
    fig = go.Figure()
    
    # Add custom method to handle secondary y-axes
    def update_yaxes_custom(title_text=None, secondary_y=False, **kwargs):
        axis_key = "yaxis2" if secondary_y else "yaxis"
        layout_update = {axis_key: {"title_text": title_text, **kwargs}}
        fig.update_layout(**layout_update)
    
    # Attach the custom method to the figure
    fig.update_yaxes = update_yaxes_custom
    
    return fig