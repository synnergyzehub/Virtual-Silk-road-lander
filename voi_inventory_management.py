import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json

def main():
    """
    Voi Jeans Retail India Pvt Ltd - Inventory Management System
    
    A comprehensive stock and inventory management platform leveraging advanced analytics 
    and interactive dashboards to optimize manufacturing, distribution, and retail operations.
    """
    st.set_page_config(
        page_title="Voi Jeans - Inventory Management",
        page_icon="👖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Set up authentication (simplified for demo)
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_role = None

    if not st.session_state.authenticated:
        show_login()
    else:
        # Sidebar for navigation
        st.sidebar.title("Voi Jeans")
        st.sidebar.subheader("Inventory Management")
        
        # User info in sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**User:** {st.session_state.user_role}")
        st.sidebar.markdown(f"**License:** Active")
        st.sidebar.markdown("---")
        
        # Navigation options based on the Synergyze frameworks
        nav_option = st.sidebar.radio(
            "Navigation",
            [
                "Dashboard", 
                "Inventory Analytics",
                "Inventory Optimization", # New feature
                "Woven Supply (Manufacturing)",
                "Commune Connect (Distribution)",
                "Store Performance",
                "Last Mile (Logistics)",
                "HSN Transaction System",
                "Sync Up (Reporting)",
                "Settings"
            ]
        )
        
        if nav_option == "Dashboard":
            show_dashboard()
        elif nav_option == "Inventory Analytics":
            show_inventory_analytics()
        elif nav_option == "Inventory Optimization": # New feature
            show_inventory_optimization()
        elif nav_option == "Woven Supply (Manufacturing)":
            show_woven_supply()
        elif nav_option == "Commune Connect (Distribution)":
            show_commune_connect()
        elif nav_option == "Store Performance":
            show_store_performance()
        elif nav_option == "Last Mile (Logistics)":
            show_last_mile()
        elif nav_option == "HSN Transaction System":
            show_hsn_transaction_system()
        elif nav_option == "Sync Up (Reporting)":
            show_sync_up()
        elif nav_option == "Settings":
            show_settings()

def show_login():
    """Display the login screen"""
    st.title("Voi Jeans Inventory Management System")
    st.markdown("### Login to access the system")
    
    # Login form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Access Your Account")
        roles = [
            "Select Your Role",
            "Brand Manager",
            "Inventory Manager",
            "Store Manager",
            "Production Manager",
            "Logistics Coordinator",
            "Finance Controller",
            "System Administrator"
        ]
        selected_role = st.selectbox("Role", roles)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if selected_role != "Select Your Role" and username and password:
                # In a real system, this would verify credentials
                st.session_state.authenticated = True
                st.session_state.user_role = selected_role
                st.rerun()
            else:
                st.error("Please complete all fields")
    
    with col2:
        st.markdown("### System Overview")
        st.markdown("""
        Our inventory management system helps Voi Jeans optimize:
        
        - **Manufacturing**: Track production across vendors
        - **Distribution**: Manage warehouses and stock transfers
        - **Retail**: Monitor store performance and inventory
        - **Analytics**: Make data-driven decisions for better performance
        
        This system integrates the Synergyze frameworks to provide a comprehensive 
        view of the entire supply chain.
        """)

def show_dashboard():
    """Display the main dashboard"""
    st.title("Voi Jeans Dashboard")
    st.subheader("Inventory Management Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Inventory Value", f"₹{random.randint(10000000, 50000000):,}", f"+{random.randint(100000, 1000000):,}")
    
    with col2:
        st.metric("Stock Turnover Rate", f"{random.uniform(1.5, 4.5):.2f}", f"+{random.uniform(0.1, 0.5):.2f}")
    
    with col3:
        st.metric("Active SKUs", f"{random.randint(500, 2000):,}", f"+{random.randint(10, 50):,}")
    
    with col4:
        st.metric("Stores Covered", f"{random.randint(80, 150):,}", f"+{random.randint(1, 5):,}")
    
    # Create columns for dashboard widgets
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Sales trend
        st.subheader("Sales Trend (Last 30 Days)")
        
        # Generate sample data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        sales_amounts = [random.randint(500000, 2000000) for _ in range(30)]
        
        df_sales = pd.DataFrame({
            "Date": dates,
            "Sales Amount": sales_amounts
        })
        
        fig = px.line(df_sales, x="Date", y="Sales Amount",
                     title="Daily Sales (₹)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory by category
        st.subheader("Inventory by Category")
        
        # Generate sample inventory data
        categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
        inventory_values = [random.randint(1000000, 10000000) for _ in range(len(categories))]
        
        df_inventory = pd.DataFrame({
            "Category": categories,
            "Inventory Value": inventory_values
        })
        
        fig = px.bar(df_inventory, x="Category", y="Inventory Value",
                    title="Inventory Value by Category (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # Inventory aging
        st.subheader("Inventory Aging")
        
        aging_buckets = ["0-30 days", "31-60 days", "61-90 days", "91-180 days", ">180 days"]
        aging_values = [random.randint(1000, 5000) for _ in range(len(aging_buckets))]
        
        df_aging = pd.DataFrame({
            "Aging": aging_buckets,
            "Value": aging_values
        })
        
        fig = px.pie(df_aging, values="Value", names="Aging", 
                    title="Inventory Aging Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Top performing stores
        st.subheader("Top Performing Stores")
        
        stores = [f"Store {random.randint(1, 100)}" for _ in range(5)]
        sales = [random.randint(100000, 1000000) for _ in range(5)]
        
        df_stores = pd.DataFrame({
            "Store": stores,
            "Sales": sales
        }).sort_values(by="Sales", ascending=False)
        
        fig = px.bar(df_stores, x="Store", y="Sales",
                    title="Top 5 Stores by Sales (₹)")
        st.plotly_chart(fig, use_container_width=True)

def show_inventory_analytics():
    """Display the inventory analytics page"""
    st.title("Inventory Analytics")
    st.subheader("Advanced Inventory Insights")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Category",
            ["All Categories", "Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
        )
    
    with col2:
        location_filter = st.selectbox(
            "Location",
            ["All Locations", "Warehouse A", "Warehouse B", "Store Inventory"]
        )
    
    with col3:
        time_filter = st.selectbox(
            "Time Period",
            ["Last 30 Days", "Last 90 Days", "Last 180 Days", "Last Year"]
        )
    
    # Inventory metrics
    st.markdown("### Inventory Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Days in Inventory", f"{random.randint(30, 90)}", f"-{random.randint(1, 10)}")
    
    with col2:
        st.metric("Stock-to-Sales Ratio", f"{random.uniform(1.0, 3.0):.2f}", f"-{random.uniform(0.1, 0.5):.2f}")
    
    with col3:
        st.metric("Out-of-Stock Items", f"{random.randint(10, 50)}", f"-{random.randint(1, 5)}")
    
    with col4:
        st.metric("Excess Inventory Value", f"₹{random.randint(1000000, 5000000):,}", f"-{random.randint(100000, 500000):,}")
    
    # Generate sample inventory data
    # In a real system, this would come from a database
    inventory_data = []
    
    categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
    sub_categories = {
        "Jeans": ["Slim Fit", "Regular Fit", "Relaxed Fit", "Skinny", "Boot Cut"],
        "T-Shirts": ["Round Neck", "V-Neck", "Polo", "Graphic", "Basic"],
        "Shirts": ["Formal", "Casual", "Denim", "Checked", "Printed"],
        "Jackets": ["Bomber", "Denim", "Leather", "Winter", "Casual"],
        "Accessories": ["Belts", "Wallets", "Socks", "Caps", "Bags"]
    }
    
    locations = ["Warehouse A", "Warehouse B", "Store 1", "Store 2", "Store 3"]
    
    for _ in range(50):
        category = random.choice(categories)
        sub_category = random.choice(sub_categories[category])
        sku = f"VOI-{category[:3].upper()}-{random.randint(1000, 9999)}"
        location = random.choice(locations)
        quantity = random.randint(10, 500)
        avg_cost = random.uniform(500, 2000)
        mrp = avg_cost * random.uniform(1.5, 2.5)
        days_in_inventory = random.randint(1, 180)
        
        inventory_data.append({
            "SKU": sku,
            "Category": category,
            "Sub-Category": sub_category,
            "Location": location,
            "Quantity": quantity,
            "Average Cost": avg_cost,
            "MRP": mrp,
            "Inventory Value": quantity * avg_cost,
            "Days in Inventory": days_in_inventory
        })
    
    df_inventory = pd.DataFrame(inventory_data)
    
    # Apply filters
    filtered_df = df_inventory
    
    if category_filter != "All Categories":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
    
    if location_filter != "All Locations":
        if location_filter == "Warehouse A" or location_filter == "Warehouse B":
            filtered_df = filtered_df[filtered_df["Location"] == location_filter]
        elif location_filter == "Store Inventory":
            filtered_df = filtered_df[filtered_df["Location"].str.contains("Store")]
    
    # Display inventory data
    st.markdown("### Inventory Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Inventory analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Inventory Value by Category")
        
        category_value = filtered_df.groupby("Category")["Inventory Value"].sum().reset_index()
        
        fig = px.pie(category_value, values="Inventory Value", names="Category",
                    title="Inventory Value Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Inventory Aging Analysis")
        
        # Define aging buckets
        def age_bucket(days):
            if days <= 30:
                return "0-30 days"
            elif days <= 60:
                return "31-60 days"
            elif days <= 90:
                return "61-90 days"
            elif days <= 180:
                return "91-180 days"
            else:
                return ">180 days"
        
        filtered_df["Age Bucket"] = filtered_df["Days in Inventory"].apply(age_bucket)
        
        age_distribution = filtered_df.groupby("Age Bucket")["Inventory Value"].sum().reset_index()
        
        # Sort in the correct order
        bucket_order = ["0-30 days", "31-60 days", "61-90 days", "91-180 days", ">180 days"]
        age_distribution["Age Bucket"] = pd.Categorical(age_distribution["Age Bucket"], categories=bucket_order, ordered=True)
        age_distribution = age_distribution.sort_values("Age Bucket")
        
        fig = px.bar(age_distribution, x="Age Bucket", y="Inventory Value",
                    title="Inventory Value by Age")
        st.plotly_chart(fig, use_container_width=True)
    
    # Inventory recommendations
    st.markdown("### Inventory Recommendations")
    
    # Calculate slow-moving inventory (items in inventory for more than 90 days)
    slow_moving = filtered_df[filtered_df["Days in Inventory"] > 90]
    slow_moving_value = slow_moving["Inventory Value"].sum()
    
    # Calculate potential stockouts (items with less than 20 units)
    potential_stockouts = filtered_df[filtered_df["Quantity"] < 20]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Slow-Moving Inventory Value:** ₹{slow_moving_value:,.2f}")
        st.markdown(f"**Number of Slow-Moving Items:** {len(slow_moving)}")
        
        if len(slow_moving) > 0:
            st.markdown("**Slow-Moving Items:**")
            st.dataframe(slow_moving[["SKU", "Category", "Sub-Category", "Quantity", "Inventory Value", "Days in Inventory"]])
    
    with col2:
        st.markdown(f"**Potential Stockout Items:** {len(potential_stockouts)}")
        
        if len(potential_stockouts) > 0:
            st.markdown("**Items at Risk of Stockout:**")
            st.dataframe(potential_stockouts[["SKU", "Category", "Sub-Category", "Quantity", "Inventory Value"]])

def show_woven_supply():
    """Display the Woven Supply (Manufacturing) page"""
    st.title("Woven Supply - Manufacturing")
    st.subheader("Production and Vendor Management")
    
    # Manufacturing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Production Orders", f"{random.randint(10, 50)}", f"+{random.randint(1, 5)}")
    
    with col2:
        st.metric("Pending Approvals", f"{random.randint(5, 20)}", f"-{random.randint(1, 3)}")
    
    with col3:
        st.metric("Production Efficiency", f"{random.randint(80, 95)}%", f"+{random.randint(1, 5)}%")
    
    with col4:
        st.metric("Quality Rating", f"{random.randint(85, 98)}%", f"+{random.randint(1, 3)}%")
    
    # Tabs for different manufacturing sections
    tab1, tab2, tab3, tab4 = st.tabs(["Production Orders", "Vendor Management", "Quality Control", "Manufacturing Analytics"])
    
    with tab1:
        st.markdown("### Production Orders")
        
        # Generate sample production order data
        production_orders = []
        
        for i in range(15):
            order_id = f"PO-{random.randint(10000, 99999)}"
            vendor = f"Vendor-{random.randint(100, 999)}"
            category = random.choice(["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"])
            quantity = random.randint(100, 1000)
            start_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            expected_completion = (datetime.now() + timedelta(days=random.randint(5, 45))).strftime("%Y-%m-%d")
            status = random.choice(["In Progress", "Pending Approval", "Quality Check", "Completed"])
            
            production_orders.append({
                "Order ID": order_id,
                "Vendor": vendor,
                "Category": category,
                "Quantity": quantity,
                "Start Date": start_date,
                "Expected Completion": expected_completion,
                "Status": status
            })
        
        df_orders = pd.DataFrame(production_orders)
        st.dataframe(df_orders, use_container_width=True)
        
        # Production order actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("Create New Order")
        
        with col2:
            st.button("Update Selected Order")
        
        with col3:
            st.button("Cancel Selected Order")
    
    with tab2:
        st.markdown("### Vendor Management")
        
        # Generate sample vendor data
        vendors = []
        
        for i in range(10):
            vendor_id = f"V-{random.randint(100, 999)}"
            vendor_name = f"Vendor-{random.randint(100, 999)}"
            specialization = random.choice(["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories", "Multiple"])
            active_orders = random.randint(0, 10)
            reliability_score = random.randint(70, 100)
            quality_score = random.randint(70, 100)
            delivery_score = random.randint(70, 100)
            
            vendors.append({
                "Vendor ID": vendor_id,
                "Vendor Name": vendor_name,
                "Specialization": specialization,
                "Active Orders": active_orders,
                "Reliability Score": reliability_score,
                "Quality Score": quality_score,
                "Delivery Score": delivery_score,
                "Overall Rating": (reliability_score + quality_score + delivery_score) // 3
            })
        
        df_vendors = pd.DataFrame(vendors).sort_values(by="Overall Rating", ascending=False)
        st.dataframe(df_vendors, use_container_width=True)
        
        # Vendor performance visualization
        st.markdown("### Vendor Performance Comparison")
        
        # Select top 5 vendors for comparison
        top_vendors = df_vendors.head(5)
        
        # Reshape data for radar chart
        categories = ["Reliability Score", "Quality Score", "Delivery Score"]
        
        fig = go.Figure()
        
        for _, vendor in top_vendors.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[vendor["Reliability Score"], vendor["Quality Score"], vendor["Delivery Score"]],
                theta=categories,
                fill='toself',
                name=vendor["Vendor Name"]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Vendor Performance Metrics"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Quality Control")
        
        # Generate sample quality control data
        qc_data = []
        
        for i in range(12):
            order_id = f"PO-{random.randint(10000, 99999)}"
            inspection_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            inspector = f"Inspector-{random.randint(1, 10)}"
            total_inspected = random.randint(50, 500)
            defects_found = random.randint(0, int(total_inspected * 0.1))
            defect_rate = (defects_found / total_inspected) * 100
            result = "Passed" if defect_rate < 5 else "Failed"
            
            qc_data.append({
                "Order ID": order_id,
                "Inspection Date": inspection_date,
                "Inspector": inspector,
                "Units Inspected": total_inspected,
                "Defects Found": defects_found,
                "Defect Rate (%)": round(defect_rate, 2),
                "Result": result
            })
        
        df_qc = pd.DataFrame(qc_data)
        st.dataframe(df_qc, use_container_width=True)
        
        # Defect trend visualization
        st.markdown("### Defect Rate Trend")
        
        # Generate sample defect trend data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        defect_rates = [random.uniform(0.5, 6.0) for _ in range(30)]
        
        df_defect_trend = pd.DataFrame({
            "Date": dates,
            "Defect Rate (%)": defect_rates
        })
        
        fig = px.line(df_defect_trend, x="Date", y="Defect Rate (%)",
                     title="30-Day Defect Rate Trend")
        
        # Add target line
        fig.add_shape(
            type="line",
            x0=min(dates),
            y0=5,
            x1=max(dates),
            y1=5,
            line=dict(
                color="Red",
                width=2,
                dash="dash",
            )
        )
        
        # Add annotation for target line
        fig.add_annotation(
            x=max(dates),
            y=5,
            text="Target (5%)",
            showarrow=False,
            yshift=10
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Manufacturing Analytics")
        
        # Generate sample manufacturing analytics data
        
        # Production by category
        categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
        production_volumes = [random.randint(1000, 10000) for _ in range(len(categories))]
        
        df_production = pd.DataFrame({
            "Category": categories,
            "Production Volume": production_volumes
        })
        
        # Production trend
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        production_trends = [random.randint(5000, 15000) for _ in range(len(months))]
        
        df_trend = pd.DataFrame({
            "Month": months,
            "Production": production_trends
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Production by Category")
            
            fig = px.pie(df_production, values="Production Volume", names="Category",
                        title="Production Volume by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Annual Production Trend")
            
            fig = px.line(df_trend, x="Month", y="Production",
                         title="Monthly Production Volume")
            st.plotly_chart(fig, use_container_width=True)
        
        # Manufacturing efficiency
        st.markdown("### Manufacturing Efficiency Analysis")
        
        efficiency_metrics = {
            "Production Line Efficiency": random.randint(80, 95),
            "Materials Utilization": random.randint(85, 98),
            "Labor Efficiency": random.randint(75, 90),
            "On-Time Completion Rate": random.randint(70, 95),
            "Quality Pass Rate": random.randint(85, 98)
        }
        
        df_efficiency = pd.DataFrame({
            "Metric": list(efficiency_metrics.keys()),
            "Value (%)": list(efficiency_metrics.values())
        })
        
        fig = px.bar(df_efficiency, x="Metric", y="Value (%)",
                    title="Manufacturing Efficiency Metrics")
        st.plotly_chart(fig, use_container_width=True)

def show_commune_connect():
    """Display the Commune Connect (Distribution) page"""
    st.title("Commune Connect - Distribution")
    st.subheader("Warehouse and Distribution Management")
    
    # Distribution metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Warehouses", f"{random.randint(3, 10)}", f"+{random.randint(0, 2)}")
    
    with col2:
        st.metric("Active Transfers", f"{random.randint(10, 50)}", f"+{random.randint(1, 5)}")
    
    with col3:
        st.metric("Distribution Efficiency", f"{random.randint(80, 95)}%", f"+{random.randint(1, 5)}%")
    
    with col4:
        st.metric("Order Fulfillment Rate", f"{random.randint(90, 99)}%", f"+{random.randint(1, 3)}%")
    
    # Tabs for different distribution sections
    tab1, tab2, tab3, tab4 = st.tabs(["Warehouse Inventory", "Stock Transfers", "Distribution Planning", "Fulfillment Analytics"])
    
    with tab1:
        st.markdown("### Warehouse Inventory")
        
        # Warehouse selector
        warehouse = st.selectbox(
            "Select Warehouse",
            ["All Warehouses", "North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"]
        )
        
        # Generate sample warehouse inventory data
        warehouse_inventory = []
        
        warehouses = ["North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"]
        
        for _ in range(50):
            wh = random.choice(warehouses)
            category = random.choice(["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"])
            sub_category = f"{category} Type {random.randint(1, 5)}"
            sku = f"VOI-{category[:3].upper()}-{random.randint(1000, 9999)}"
            quantity = random.randint(10, 500)
            capacity_used = random.randint(10, 100)
            location_code = f"{wh[:1]}-{random.randint(1, 20)}-{random.randint(1, 50)}"
            
            warehouse_inventory.append({
                "Warehouse": wh,
                "SKU": sku,
                "Category": category,
                "Sub-Category": sub_category,
                "Quantity": quantity,
                "Capacity Used (%)": capacity_used,
                "Location Code": location_code
            })
        
        df_warehouse = pd.DataFrame(warehouse_inventory)
        
        # Apply warehouse filter
        if warehouse != "All Warehouses":
            df_warehouse = df_warehouse[df_warehouse["Warehouse"] == warehouse]
        
        st.dataframe(df_warehouse, use_container_width=True)
        
        # Warehouse capacity visualization
        st.markdown("### Warehouse Capacity Utilization")
        
        # Calculate capacity utilization by warehouse
        capacity_by_warehouse = df_warehouse.groupby("Warehouse")["Capacity Used (%)"].mean().reset_index()
        
        fig = px.bar(capacity_by_warehouse, x="Warehouse", y="Capacity Used (%)",
                    title="Average Capacity Utilization by Warehouse")
        
        # Add target line
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=80,
            x1=len(warehouses) - 0.5,
            y1=80,
            line=dict(
                color="Red",
                width=2,
                dash="dash",
            )
        )
        
        # Add annotation for target line
        fig.add_annotation(
            x=len(warehouses) - 1,
            y=80,
            text="Optimal (80%)",
            showarrow=False,
            yshift=10
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Stock Transfers")
        
        # Generate sample stock transfer data
        stock_transfers = []
        
        warehouses = ["North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"]
        stores = [f"Store {random.randint(1, 100)}" for _ in range(10)]
        
        for i in range(20):
            transfer_id = f"TRF-{random.randint(10000, 99999)}"
            source = random.choice(warehouses)
            destination = random.choice(stores + warehouses)
            
            # Ensure source and destination are different
            while destination == source:
                destination = random.choice(stores + warehouses)
            
            items = random.randint(5, 50)
            total_quantity = random.randint(50, 500)
            initiation_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            expected_delivery = (datetime.now() + timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
            status = random.choice(["Initiated", "In Transit", "Delivered", "Pending"])
            
            stock_transfers.append({
                "Transfer ID": transfer_id,
                "Source": source,
                "Destination": destination,
                "Items": items,
                "Total Quantity": total_quantity,
                "Initiation Date": initiation_date,
                "Expected Delivery": expected_delivery,
                "Status": status
            })
        
        df_transfers = pd.DataFrame(stock_transfers)
        st.dataframe(df_transfers, use_container_width=True)
        
        # Transfer actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("Create New Transfer")
        
        with col2:
            st.button("Update Selected Transfer")
        
        with col3:
            st.button("Cancel Selected Transfer")
        
        # Transfer status visualization
        st.markdown("### Transfer Status Overview")
        
        status_counts = df_transfers["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig = px.pie(status_counts, values="Count", names="Status",
                    title="Transfer Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Distribution Planning")
        
        # Generate sample distribution planning data
        distribution_plans = []
        
        for i in range(15):
            plan_id = f"PLAN-{random.randint(1000, 9999)}"
            description = random.choice([
                "Seasonal Distribution", 
                "New Collection Launch", 
                "Inventory Rebalancing", 
                "Store Replenishment", 
                "Warehouse Consolidation"
            ])
            start_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=random.randint(31, 60))).strftime("%Y-%m-%d")
            locations_affected = random.randint(5, 30)
            skus_involved = random.randint(10, 100)
            total_units = random.randint(1000, 10000)
            status = random.choice(["Draft", "Approved", "In Progress", "Completed", "On Hold"])
            
            distribution_plans.append({
                "Plan ID": plan_id,
                "Description": description,
                "Start Date": start_date,
                "End Date": end_date,
                "Locations Affected": locations_affected,
                "SKUs Involved": skus_involved,
                "Total Units": total_units,
                "Status": status
            })
        
        df_plans = pd.DataFrame(distribution_plans)
        st.dataframe(df_plans, use_container_width=True)
        
        # Distribution planning visualization
        st.markdown("### Upcoming Distribution Volume")
        
        # Extract month from the start date
        df_plans["Month"] = pd.to_datetime(df_plans["Start Date"]).dt.strftime("%b")
        
        # Sum total units by month
        monthly_distribution = df_plans.groupby("Month")["Total Units"].sum().reset_index()
        
        # Sort by month chronologically
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_distribution["Month"] = pd.Categorical(monthly_distribution["Month"], categories=month_order, ordered=True)
        monthly_distribution = monthly_distribution.sort_values("Month")
        
        fig = px.bar(monthly_distribution, x="Month", y="Total Units",
                    title="Planned Distribution Volume by Month")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Fulfillment Analytics")
        
        # Generate sample fulfillment analytics data
        
        # On-time delivery rate trend
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        otd_rates = [random.uniform(80, 99) for _ in range(len(months))]
        
        df_otd = pd.DataFrame({
            "Month": months,
            "On-Time Delivery Rate (%)": otd_rates
        })
        
        # Fulfillment efficiency by location
        warehouses = ["North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"]
        picking_efficiency = [random.uniform(70, 95) for _ in range(len(warehouses))]
        packing_efficiency = [random.uniform(75, 98) for _ in range(len(warehouses))]
        shipping_efficiency = [random.uniform(80, 99) for _ in range(len(warehouses))]
        
        df_efficiency = pd.DataFrame({
            "Warehouse": warehouses,
            "Picking Efficiency (%)": picking_efficiency,
            "Packing Efficiency (%)": packing_efficiency,
            "Shipping Efficiency (%)": shipping_efficiency
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### On-Time Delivery Trend")
            
            fig = px.line(df_otd, x="Month", y="On-Time Delivery Rate (%)",
                         title="Monthly On-Time Delivery Rate")
            
            # Add target line
            fig.add_shape(
                type="line",
                x0=0,
                y0=95,
                x1=len(months) - 1,
                y1=95,
                line=dict(
                    color="Green",
                    width=2,
                    dash="dash",
                )
            )
            
            # Add annotation for target line
            fig.add_annotation(
                x=len(months) - 1,
                y=95,
                text="Target (95%)",
                showarrow=False,
                yshift=10
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Distribution Center Efficiency")
            
            # Melt the dataframe for visualization
            df_efficiency_melted = pd.melt(
                df_efficiency, 
                id_vars=["Warehouse"], 
                value_vars=["Picking Efficiency (%)", "Packing Efficiency (%)", "Shipping Efficiency (%)"],
                var_name="Metric",
                value_name="Efficiency (%)"
            )
            
            fig = px.bar(df_efficiency_melted, x="Warehouse", y="Efficiency (%)", color="Metric",
                        barmode="group", title="Fulfillment Efficiency by Location")
            st.plotly_chart(fig, use_container_width=True)
        
        # Fulfillment metrics summary
        st.markdown("### Fulfillment Metrics Summary")
        
        fulfillment_metrics = {
            "Average Order Processing Time": f"{random.uniform(0.5, 2.0):.1f} days",
            "Inventory Accuracy": f"{random.uniform(95.0, 99.9):.1f}%",
            "Perfect Order Rate": f"{random.uniform(90.0, 98.0):.1f}%",
            "Return Rate": f"{random.uniform(1.0, 5.0):.1f}%",
            "Cross-Docking Rate": f"{random.uniform(10.0, 30.0):.1f}%"
        }
        
        col1, col2, col3 = st.columns(3)
        
        metrics = list(fulfillment_metrics.items())
        
        for i, (metric, value) in enumerate(metrics):
            if i % 3 == 0:
                col1.metric(metric, value)
            elif i % 3 == 1:
                col2.metric(metric, value)
            else:
                col3.metric(metric, value)

def show_store_performance():
    """Display the Store Performance page"""
    st.title("Store Performance")
    st.subheader("Retail Store Analytics and Management")
    
    # Store performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Stores", f"{random.randint(80, 150)}", f"+{random.randint(1, 5)}")
    
    with col2:
        st.metric("Average Daily Sales", f"₹{random.randint(100000, 500000):,}", f"+{random.randint(5000, 20000):,}")
    
    with col3:
        st.metric("Conversion Rate", f"{random.uniform(20.0, 35.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
    
    with col4:
        st.metric("Average Transaction Value", f"₹{random.randint(2000, 5000):,}", f"+{random.randint(100, 500):,}")
    
    # Store selection
    st.markdown("### Store Selection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        region_filter = st.selectbox(
            "Region",
            ["All Regions", "North", "South", "East", "West", "Central"]
        )
    
    with col2:
        city_filter = st.selectbox(
            "City",
            ["All Cities", "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Ahmedabad"]
        )
    
    with col3:
        store_type_filter = st.selectbox(
            "Store Type",
            ["All Store Types", "Flagship", "Mall", "High Street", "Express", "Outlet"]
        )
    
    # Generate sample store data
    stores = []
    
    regions = ["North", "South", "East", "West", "Central"]
    cities = {
        "North": ["Delhi", "Chandigarh", "Jaipur", "Lucknow"],
        "South": ["Bangalore", "Chennai", "Hyderabad", "Kochi"],
        "East": ["Kolkata", "Bhubaneswar", "Guwahati", "Ranchi"],
        "West": ["Mumbai", "Pune", "Ahmedabad", "Surat"],
        "Central": ["Indore", "Bhopal", "Nagpur", "Raipur"]
    }
    store_types = ["Flagship", "Mall", "High Street", "Express", "Outlet"]
    
    for i in range(100):
        store_id = f"ST-{random.randint(100, 999)}"
        region = random.choice(regions)
        city = random.choice(cities[region])
        store_type = random.choice(store_types)
        area_sqft = random.randint(500, 5000)
        monthly_sales = random.randint(500000, 5000000)
        foot_traffic = random.randint(1000, 10000)
        conversion_rate = random.uniform(15.0, 40.0)
        avg_transaction = random.randint(1500, 6000)
        
        # Calculate derived metrics
        sales_per_sqft = monthly_sales / area_sqft
        transactions = int(foot_traffic * (conversion_rate / 100))
        
        stores.append({
            "Store ID": store_id,
            "Region": region,
            "City": city,
            "Store Type": store_type,
            "Area (sq.ft)": area_sqft,
            "Monthly Sales (₹)": monthly_sales,
            "Foot Traffic": foot_traffic,
            "Conversion Rate (%)": round(conversion_rate, 1),
            "Avg. Transaction (₹)": avg_transaction,
            "Sales/sq.ft (₹)": round(sales_per_sqft, 2),
            "Transactions": transactions
        })
    
    df_stores = pd.DataFrame(stores)
    
    # Apply filters
    filtered_stores = df_stores
    
    if region_filter != "All Regions":
        filtered_stores = filtered_stores[filtered_stores["Region"] == region_filter]
    
    if city_filter != "All Cities":
        filtered_stores = filtered_stores[filtered_stores["City"] == city_filter]
    
    if store_type_filter != "All Store Types":
        filtered_stores = filtered_stores[filtered_stores["Store Type"] == store_type_filter]
    
    # Display store data
    st.dataframe(filtered_stores, use_container_width=True)
    
    # Store visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales by Region")
        
        region_sales = df_stores.groupby("Region")["Monthly Sales (₹)"].sum().reset_index()
        
        fig = px.pie(region_sales, values="Monthly Sales (₹)", names="Region",
                    title="Sales Distribution by Region")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Store Performance by Type")
        
        type_performance = df_stores.groupby("Store Type").agg({
            "Monthly Sales (₹)": "mean",
            "Conversion Rate (%)": "mean",
            "Sales/sq.ft (₹)": "mean"
        }).reset_index()
        
        # Rename columns for clarity
        type_performance.columns = ["Store Type", "Avg. Monthly Sales (₹)", "Avg. Conversion Rate (%)", "Avg. Sales/sq.ft (₹)"]
        
        # Select metric for visualization
        selected_metric = st.selectbox(
            "Select Performance Metric",
            ["Avg. Monthly Sales (₹)", "Avg. Conversion Rate (%)", "Avg. Sales/sq.ft (₹)"]
        )
        
        fig = px.bar(type_performance, x="Store Type", y=selected_metric,
                    title=f"{selected_metric} by Store Type")
        st.plotly_chart(fig, use_container_width=True)
    
    # Store performance details
    st.markdown("### Store Performance Details")
    
    # Sort stores by monthly sales in descending order
    top_stores = filtered_stores.sort_values(by="Monthly Sales (₹)", ascending=False).head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 10 Performing Stores")
        
        fig = px.bar(top_stores, x="Store ID", y="Monthly Sales (₹)",
                    color="Store Type", title="Top 10 Stores by Monthly Sales")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Performance Metrics Comparison")
        
        # Create a scatter plot of sales vs. conversion rate
        fig = px.scatter(filtered_stores, x="Conversion Rate (%)", y="Monthly Sales (₹)",
                         size="Foot Traffic", color="Store Type",
                         hover_name="Store ID", hover_data=["City", "Area (sq.ft)"],
                         title="Sales vs. Conversion Rate by Store")
        st.plotly_chart(fig, use_container_width=True)

def show_last_mile():
    """Display the Last Mile (Logistics) page"""
    st.title("Last Mile - Logistics")
    st.subheader("Logistics and Delivery Management")
    
    # Logistics metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Shipments", f"{random.randint(50, 200)}", f"+{random.randint(5, 20)}")
    
    with col2:
        st.metric("On-Time Delivery", f"{random.randint(90, 98)}%", f"+{random.randint(1, 3)}%")
    
    with col3:
        st.metric("Average Delivery Time", f"{random.uniform(1.5, 3.5):.1f} days", f"-{random.uniform(0.1, 0.5):.1f} days")
    
    with col4:
        st.metric("Return Rate", f"{random.uniform(1.0, 5.0):.1f}%", f"-{random.uniform(0.1, 0.8):.1f}%")
    
    # Tabs for different logistics sections
    tab1, tab2, tab3, tab4 = st.tabs(["Shipment Tracking", "Carrier Performance", "Route Optimization", "Logistics Analytics"])
    
    with tab1:
        st.markdown("### Shipment Tracking")
        
        # Generate sample shipment data
        shipments = []
        
        for i in range(25):
            shipment_id = f"SHP-{random.randint(100000, 999999)}"
            origin = random.choice(["North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"])
            destination = f"Store {random.randint(1, 100)}"
            carrier = random.choice(["BlueDart", "Delhivery", "Ecom Express", "DTDC", "FedEx"])
            items = random.randint(5, 50)
            weight = round(random.uniform(5.0, 100.0), 2)
            ship_date = (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
            estimated_delivery = (datetime.now() + timedelta(days=random.randint(0, 5))).strftime("%Y-%m-%d")
            status = random.choice(["Processed", "In Transit", "Out for Delivery", "Delivered", "Exception"])
            tracking_number = f"TRK{random.randint(1000000, 9999999)}"
            
            shipments.append({
                "Shipment ID": shipment_id,
                "Origin": origin,
                "Destination": destination,
                "Carrier": carrier,
                "Items": items,
                "Weight (kg)": weight,
                "Ship Date": ship_date,
                "Estimated Delivery": estimated_delivery,
                "Status": status,
                "Tracking Number": tracking_number
            })
        
        df_shipments = pd.DataFrame(shipments)
        st.dataframe(df_shipments, use_container_width=True)
        
        # Shipment status visualization
        st.markdown("### Shipment Status Overview")
        
        status_counts = df_shipments["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig = px.pie(status_counts, values="Count", names="Status",
                    title="Shipment Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Carrier Performance")
        
        # Generate sample carrier performance data
        carriers = ["BlueDart", "Delhivery", "Ecom Express", "DTDC", "FedEx"]
        on_time_rates = [random.uniform(88.0, 98.0) for _ in range(len(carriers))]
        damage_rates = [random.uniform(0.1, 2.0) for _ in range(len(carriers))]
        avg_delivery_times = [random.uniform(1.5, 4.0) for _ in range(len(carriers))]
        cost_per_kg = [random.uniform(50.0, 150.0) for _ in range(len(carriers))]
        
        df_carriers = pd.DataFrame({
            "Carrier": carriers,
            "On-Time Delivery Rate (%)": on_time_rates,
            "Damage Rate (%)": damage_rates,
            "Avg. Delivery Time (days)": avg_delivery_times,
            "Cost per kg (₹)": cost_per_kg
        })
        
        st.dataframe(df_carriers, use_container_width=True)
        
        # Carrier performance visualization
        st.markdown("### Carrier Performance Comparison")
        
        # Select metric for comparison
        selected_metric = st.selectbox(
            "Select Performance Metric",
            ["On-Time Delivery Rate (%)", "Damage Rate (%)", "Avg. Delivery Time (days)", "Cost per kg (₹)"]
        )
        
        fig = px.bar(df_carriers, x="Carrier", y=selected_metric,
                    title=f"{selected_metric} by Carrier")
        st.plotly_chart(fig, use_container_width=True)
        
        # Carrier performance radar chart
        st.markdown("### Comprehensive Carrier Performance")
        
        # Normalize data for radar chart
        normalized_carriers = df_carriers.copy()
        
        # Flip metrics where lower is better
        normalized_carriers["Normalized Damage Rate"] = 100 - normalized_carriers["Damage Rate (%)"] * 50
        normalized_carriers["Normalized Delivery Time"] = 100 - (normalized_carriers["Avg. Delivery Time (days)"] - 1.5) * 40
        normalized_carriers["Normalized Cost"] = 100 - ((normalized_carriers["Cost per kg (₹)"] - 50) / 100) * 100
        
        fig = go.Figure()
        
        categories = ["On-Time Delivery Rate (%)", "Normalized Damage Rate", "Normalized Delivery Time", "Normalized Cost"]
        
        for _, carrier in normalized_carriers.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[
                    carrier["On-Time Delivery Rate (%)"],
                    carrier["Normalized Damage Rate"],
                    carrier["Normalized Delivery Time"],
                    carrier["Normalized Cost"]
                ],
                theta=categories,
                fill='toself',
                name=carrier["Carrier"]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Carrier Performance Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Route Optimization")
        
        # Generate sample route data
        routes = []
        
        for i in range(15):
            route_id = f"RT-{random.randint(100, 999)}"
            origin = random.choice(["North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse", "Central Warehouse"])
            region = random.choice(["North Region", "South Region", "East Region", "West Region", "Central Region"])
            stops = random.randint(5, 20)
            distance = random.randint(50, 500)
            vehicle_type = random.choice(["Small Van", "Medium Truck", "Large Truck"])
            fuel_consumption = round(random.uniform(8.0, 20.0), 2)
            cost = distance * random.uniform(30.0, 50.0)
            optimal = random.choice([True, False])
            
            routes.append({
                "Route ID": route_id,
                "Origin": origin,
                "Region": region,
                "Stops": stops,
                "Distance (km)": distance,
                "Vehicle Type": vehicle_type,
                "Fuel Consumption (L/100km)": fuel_consumption,
                "Total Cost (₹)": round(cost, 2),
                "Optimized": optimal
            })
        
        df_routes = pd.DataFrame(routes)
        st.dataframe(df_routes, use_container_width=True)
        
        # Route optimization visualization
        st.markdown("### Route Optimization Impact")
        
        # Compare optimized vs. non-optimized routes
        optimized = df_routes[df_routes["Optimized"] == True]
        non_optimized = df_routes[df_routes["Optimized"] == False]
        
        avg_optimized = {
            "Distance": optimized["Distance (km)"].mean(),
            "Fuel": optimized["Fuel Consumption (L/100km)"].mean(),
            "Cost": optimized["Total Cost (₹)"].mean()
        }
        
        avg_non_optimized = {
            "Distance": non_optimized["Distance (km)"].mean(),
            "Fuel": non_optimized["Fuel Consumption (L/100km)"].mean(),
            "Cost": non_optimized["Total Cost (₹)"].mean()
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Avg. Distance (km)", 
                f"{avg_optimized['Distance']:.1f}", 
                f"{((avg_optimized['Distance'] - avg_non_optimized['Distance']) / avg_non_optimized['Distance'] * 100):.1f}%"
            )
        
        with col2:
            st.metric(
                "Avg. Fuel Consumption (L/100km)", 
                f"{avg_optimized['Fuel']:.1f}", 
                f"{((avg_optimized['Fuel'] - avg_non_optimized['Fuel']) / avg_non_optimized['Fuel'] * 100):.1f}%"
            )
        
        with col3:
            st.metric(
                "Avg. Route Cost (₹)", 
                f"{avg_optimized['Cost']:.2f}", 
                f"{((avg_optimized['Cost'] - avg_non_optimized['Cost']) / avg_non_optimized['Cost'] * 100):.1f}%"
            )
        
        # Route distance by region visualization
        st.markdown("### Route Distance by Region")
        
        region_distance = df_routes.groupby("Region")["Distance (km)"].sum().reset_index()
        
        fig = px.bar(region_distance, x="Region", y="Distance (km)",
                    title="Total Route Distance by Region")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Logistics Analytics")
        
        # Generate sample logistics analytics data
        
        # Delivery time trend
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        delivery_times = [random.uniform(1.5, 4.0) for _ in range(len(months))]
        
        df_delivery = pd.DataFrame({
            "Month": months,
            "Avg. Delivery Time (days)": delivery_times
        })
        
        # Cost analysis by distance
        distances = list(range(50, 550, 50))
        costs = [d * random.uniform(28.0, 32.0) for d in distances]
        
        df_costs = pd.DataFrame({
            "Distance (km)": distances,
            "Cost (₹)": costs
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Delivery Time Trend")
            
            fig = px.line(df_delivery, x="Month", y="Avg. Delivery Time (days)",
                         title="Monthly Average Delivery Time")
            
            # Add target line
            fig.add_shape(
                type="line",
                x0=0,
                y0=2.5,
                x1=len(months) - 1,
                y1=2.5,
                line=dict(
                    color="Red",
                    width=2,
                    dash="dash",
                )
            )
            
            # Add annotation for target line
            fig.add_annotation(
                x=len(months) - 1,
                y=2.5,
                text="Target (2.5 days)",
                showarrow=False,
                yshift=10
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Logistics Cost Analysis")
            
            fig = px.scatter(df_costs, x="Distance (km)", y="Cost (₹)",
                            title="Logistics Cost by Distance",
                            trendline="ols")
            st.plotly_chart(fig, use_container_width=True)
        
        # Delivery exception analysis
        st.markdown("### Delivery Exception Analysis")
        
        exception_types = ["Weather Delay", "Address Issue", "Customer Unavailable", "Vehicle Breakdown", "Damaged Package"]
        exception_counts = [random.randint(5, 50) for _ in range(len(exception_types))]
        
        df_exceptions = pd.DataFrame({
            "Exception Type": exception_types,
            "Count": exception_counts
        })
        
        fig = px.bar(df_exceptions, x="Exception Type", y="Count",
                    title="Delivery Exceptions by Type")
        st.plotly_chart(fig, use_container_width=True)

def show_hsn_transaction_system():
    """Display the HSN Transaction System page"""
    st.title("HSN Transaction System")
    st.subheader("Harmonized System of Nomenclature for Taxation")
    
    # HSN metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total HSN Codes", f"{random.randint(50, 200)}", f"+{random.randint(1, 5)}")
    
    with col2:
        st.metric("Monthly Transactions", f"{random.randint(1000, 5000)}", f"+{random.randint(50, 200)}")
    
    with col3:
        st.metric("Avg. Tax Rate", f"{random.uniform(5.0, 18.0):.1f}%", f"{random.uniform(-0.5, 0.5):.1f}%")
    
    with col4:
        st.metric("Compliance Score", f"{random.randint(90, 99)}%", f"+{random.randint(1, 3)}%")
    
    # Tabs for different HSN sections
    tab1, tab2, tab3, tab4 = st.tabs(["HSN Code Management", "Transaction Analysis", "Tax Computation", "Compliance Monitoring"])
    
    with tab1:
        st.markdown("### HSN Code Management")
        
        # Generate sample HSN code data
        hsn_codes = []
        
        for i in range(30):
            hsn_code = f"{random.randint(1000, 9999)}"
            description = random.choice([
                "Men's Jeans", "Women's Jeans", "Men's Shirts", "Women's Tops", 
                "T-Shirts", "Jackets", "Accessories", "Footwear", "Innerwear",
                "Kids' Wear", "Winter Wear", "Packaging Material"
            ])
            tax_rate = random.choice([5, 12, 18, 28])
            item_count = random.randint(10, 100)
            last_updated = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
            
            hsn_codes.append({
                "HSN Code": hsn_code,
                "Description": description,
                "Tax Rate (%)": tax_rate,
                "Item Count": item_count,
                "Last Updated": last_updated
            })
        
        df_hsn = pd.DataFrame(hsn_codes)
        st.dataframe(df_hsn, use_container_width=True)
        
        # HSN code distribution visualization
        st.markdown("### HSN Code Distribution")
        
        # Tax rate distribution
        tax_distribution = df_hsn["Tax Rate (%)"].value_counts().reset_index()
        tax_distribution.columns = ["Tax Rate (%)", "Count"]
        
        fig = px.pie(tax_distribution, values="Count", names="Tax Rate (%)",
                    title="Distribution of Items by Tax Rate")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Transaction Analysis")
        
        # Generate sample transaction data
        transactions = []
        
        for i in range(50):
            transaction_id = f"TXN-{random.randint(10000, 99999)}"
            hsn_code = f"{random.randint(1000, 9999)}"
            transaction_type = random.choice(["Purchase", "Sale", "Stock Transfer", "Return"])
            quantity = random.randint(10, 500)
            value = quantity * random.uniform(500, 2000)
            tax_amount = value * random.choice([0.05, 0.12, 0.18, 0.28])
            date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
            party = f"Party-{random.randint(100, 999)}"
            
            transactions.append({
                "Transaction ID": transaction_id,
                "HSN Code": hsn_code,
                "Transaction Type": transaction_type,
                "Quantity": quantity,
                "Value (₹)": round(value, 2),
                "Tax Amount (₹)": round(tax_amount, 2),
                "Date": date,
                "Party": party
            })
        
        df_transactions = pd.DataFrame(transactions)
        st.dataframe(df_transactions, use_container_width=True)
        
        # Transaction analysis visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Transaction Value by Type")
            
            type_value = df_transactions.groupby("Transaction Type")["Value (₹)"].sum().reset_index()
            
            fig = px.bar(type_value, x="Transaction Type", y="Value (₹)",
                        title="Total Transaction Value by Type")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Daily Transaction Trend")
            
            # Convert date to datetime
            df_transactions["Date"] = pd.to_datetime(df_transactions["Date"])
            
            # Group by date
            daily_transactions = df_transactions.groupby(df_transactions["Date"].dt.strftime("%Y-%m-%d")).agg({
                "Transaction ID": "count",
                "Value (₹)": "sum"
            }).reset_index()
            
            daily_transactions.columns = ["Date", "Transaction Count", "Total Value (₹)"]
            
            fig = px.line(daily_transactions, x="Date", y=["Transaction Count", "Total Value (₹)"],
                         title="Daily Transaction Trend")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Tax Computation")
        
        # Generate sample tax computation data
        tax_periods = []
        
        for i in range(12):
            month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][i]
            taxable_value_5 = random.uniform(100000, 500000)
            tax_5 = taxable_value_5 * 0.05
            taxable_value_12 = random.uniform(200000, 1000000)
            tax_12 = taxable_value_12 * 0.12
            taxable_value_18 = random.uniform(500000, 2000000)
            tax_18 = taxable_value_18 * 0.18
            taxable_value_28 = random.uniform(50000, 200000)
            tax_28 = taxable_value_28 * 0.28
            
            total_taxable = taxable_value_5 + taxable_value_12 + taxable_value_18 + taxable_value_28
            total_tax = tax_5 + tax_12 + tax_18 + tax_28
            
            tax_periods.append({
                "Month": month,
                "Taxable Value @5%": round(taxable_value_5, 2),
                "Tax @5%": round(tax_5, 2),
                "Taxable Value @12%": round(taxable_value_12, 2),
                "Tax @12%": round(tax_12, 2),
                "Taxable Value @18%": round(taxable_value_18, 2),
                "Tax @18%": round(tax_18, 2),
                "Taxable Value @28%": round(taxable_value_28, 2),
                "Tax @28%": round(tax_28, 2),
                "Total Taxable Value": round(total_taxable, 2),
                "Total Tax": round(total_tax, 2)
            })
        
        df_tax = pd.DataFrame(tax_periods)
        st.dataframe(df_tax, use_container_width=True)
        
        # Tax visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Monthly Tax Collection")
            
            fig = px.line(df_tax, x="Month", y="Total Tax",
                         title="Monthly Tax Collection")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Tax Breakdown by Rate")
            
            # Create data for the pie chart
            tax_breakdown = pd.DataFrame({
                "Tax Rate": ["5%", "12%", "18%", "28%"],
                "Tax Amount": [
                    df_tax["Tax @5%"].sum(),
                    df_tax["Tax @12%"].sum(),
                    df_tax["Tax @18%"].sum(),
                    df_tax["Tax @28%"].sum()
                ]
            })
            
            fig = px.pie(tax_breakdown, values="Tax Amount", names="Tax Rate",
                        title="Tax Collection by Rate")
            st.plotly_chart(fig, use_container_width=True)
        
        # Tax efficiency metrics
        st.markdown("### Tax Efficiency Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Effective Tax Rate", f"{random.uniform(12.0, 15.0):.2f}%")
        
        with col2:
            st.metric("Input Tax Credit Used", f"₹{random.randint(500000, 2000000):,}")
        
        with col3:
            st.metric("Tax Filing Accuracy", f"{random.uniform(95.0, 99.9):.1f}%")
        
        with col4:
            st.metric("Tax Optimization Score", f"{random.randint(80, 95)}/100")
    
    with tab4:
        st.markdown("### Compliance Monitoring")
        
        # Generate sample compliance data
        compliance_items = []
        
        compliance_areas = [
            "HSN Classification", "Invoice Compliance", "E-way Bill Generation",
            "Input Tax Credit", "Tax Filing", "Documentation", "Record Keeping",
            "Audit Readiness", "Return Filing", "Tax Payment"
        ]
        
        for area in compliance_areas:
            compliance_score = random.randint(70, 100)
            last_audit = (datetime.now() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d")
            risk_level = "Low" if compliance_score >= 90 else "Medium" if compliance_score >= 80 else "High"
            action_required = random.choice(["None", "Review", "Immediate Action"])
            responsible_person = random.choice(["Tax Manager", "Finance Controller", "Compliance Officer", "External Consultant"])
            
            compliance_items.append({
                "Compliance Area": area,
                "Compliance Score": compliance_score,
                "Last Audit": last_audit,
                "Risk Level": risk_level,
                "Action Required": action_required,
                "Responsible Person": responsible_person
            })
        
        df_compliance = pd.DataFrame(compliance_items)
        st.dataframe(df_compliance, use_container_width=True)
        
        # Compliance visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Compliance Scores")
            
            fig = px.bar(df_compliance, x="Compliance Area", y="Compliance Score",
                        color="Risk Level", title="Compliance Scores by Area")
            
            # Add threshold line
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=85,
                x1=len(compliance_areas) - 0.5,
                y1=85,
                line=dict(
                    color="Red",
                    width=2,
                    dash="dash",
                )
            )
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Risk Distribution")
            
            risk_counts = df_compliance["Risk Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Count"]
            
            # Ensure proper order of risk levels
            risk_order = ["Low", "Medium", "High"]
            risk_counts["Risk Level"] = pd.Categorical(risk_counts["Risk Level"], categories=risk_order, ordered=True)
            risk_counts = risk_counts.sort_values("Risk Level")
            
            fig = px.pie(risk_counts, values="Count", names="Risk Level",
                        title="Distribution of Compliance Risk Levels",
                        color="Risk Level",
                        color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"})
            st.plotly_chart(fig, use_container_width=True)
        
        # Compliance timeline
        st.markdown("### Compliance Timeline")
        
        # Generate sample compliance events
        events = []
        event_types = ["Tax Filing", "Audit", "HSN Review", "Process Update", "Training", "System Update"]
        
        for i in range(12):
            month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][i]
            
            # Add 2-4 events per month
            for _ in range(random.randint(2, 4)):
                event_type = random.choice(event_types)
                day = random.randint(1, 28)
                date = f"2023-{i+1:02d}-{day:02d}"
                status = random.choice(["Completed", "Pending", "Overdue", "Completed"])
                owner = random.choice(["Tax Team", "Finance Team", "Compliance Team", "IT Team"])
                
                events.append({
                    "Month": month,
                    "Date": date,
                    "Event Type": event_type,
                    "Status": status,
                    "Owner": owner
                })
        
        df_events = pd.DataFrame(events)
        st.dataframe(df_events, use_container_width=True)

def show_sync_up():
    """Display the Sync Up (Reporting) page"""
    st.title("Sync Up - Reporting")
    st.subheader("Integrated Reporting and Analytics")
    
    # Reporting metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Available Reports", f"{random.randint(20, 50)}", f"+{random.randint(1, 5)}")
    
    with col2:
        st.metric("Automated Dashboards", f"{random.randint(5, 15)}", f"+{random.randint(1, 3)}")
    
    with col3:
        st.metric("Data Sources", f"{random.randint(10, 30)}", f"+{random.randint(1, 3)}")
    
    with col4:
        st.metric("Report Accuracy", f"{random.randint(95, 99)}%", f"+{random.randint(1, 2)}%")
    
    # Tabs for different reporting sections
    tab1, tab2, tab3, tab4 = st.tabs(["Executive Dashboard", "Financial Reports", "Operational KPIs", "Custom Reports"])
    
    with tab1:
        st.markdown("### Executive Dashboard")
        
        # Create a multi-metric dashboard
        st.markdown("#### Business Performance Overview")
        
        # Key business metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Revenue (YTD)", f"₹{random.randint(50000000, 200000000):,}", f"+{random.randint(5, 15)}%")
            st.metric("Gross Margin", f"{random.uniform(40.0, 55.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
        
        with col2:
            st.metric("Total Units Sold (YTD)", f"{random.randint(500000, 2000000):,}", f"+{random.randint(5, 20)}%")
            st.metric("Average Selling Price", f"₹{random.randint(1500, 3000):,}", f"+{random.uniform(1.0, 5.0):.1f}%")
        
        with col3:
            st.metric("Inventory Value", f"₹{random.randint(20000000, 100000000):,}", f"{random.randint(-10, 10)}%")
            st.metric("Inventory Turnover", f"{random.uniform(3.0, 6.0):.2f}", f"+{random.uniform(0.1, 0.5):.2f}")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales trend chart
            st.markdown("#### Revenue Trend")
            
            # Generate monthly revenue data
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            revenue = [random.randint(5000000, 20000000) for _ in range(len(months))]
            target = [random.randint(5000000, 20000000) for _ in range(len(months))]
            
            df_revenue = pd.DataFrame({
                "Month": months,
                "Actual Revenue": revenue,
                "Target Revenue": target
            })
            
            fig = px.line(df_revenue, x="Month", y=["Actual Revenue", "Target Revenue"],
                         title="Monthly Revenue vs. Target")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category performance
            st.markdown("#### Category Performance")
            
            categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
            sales = [random.randint(5000000, 20000000) for _ in range(len(categories))]
            margins = [random.uniform(35.0, 60.0) for _ in range(len(categories))]
            
            df_categories = pd.DataFrame({
                "Category": categories,
                "Sales": sales,
                "Margin (%)": margins
            })
            
            fig = px.bar(df_categories, x="Category", y="Sales",
                        color="Margin (%)", title="Sales and Margin by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Business health indicators
        st.markdown("#### Business Health Indicators")
        
        health_metrics = {
            "Customer Satisfaction": random.randint(80, 95),
            "Brand Loyalty Score": random.randint(70, 90),
            "Market Share": random.randint(15, 40),
            "Sales Growth": random.randint(5, 25),
            "Cost Optimization": random.randint(75, 95)
        }
        
        fig = go.Figure()
        
        for metric, value in health_metrics.items():
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": metric},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "royalblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 90], 'color': "lightblue"},
                        {'range': [90, 100], 'color': "royalblue"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 85
                    }
                }
            ))
        
        fig.update_layout(
            grid={'rows': 1, 'columns': 5, 'pattern': "independent"},
            height=250
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Financial Reports")
        
        # Financial report selection
        report_type = st.selectbox(
            "Select Financial Report",
            ["Profit & Loss Statement", "Balance Sheet", "Cash Flow Statement", "Sales Analysis", "Expense Analysis"]
        )
        
        if report_type == "Profit & Loss Statement":
            st.markdown("#### Profit & Loss Statement")
            
            # Generate P&L data
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            pl_data = []
            
            for month in months:
                revenue = random.randint(10000000, 30000000)
                cogs = revenue * random.uniform(0.4, 0.6)
                gross_profit = revenue - cogs
                gross_margin = (gross_profit / revenue) * 100
                
                expenses = {
                    "Marketing": revenue * random.uniform(0.05, 0.1),
                    "Salaries": revenue * random.uniform(0.1, 0.15),
                    "Rent": revenue * random.uniform(0.03, 0.05),
                    "Utilities": revenue * random.uniform(0.01, 0.02),
                    "Other": revenue * random.uniform(0.02, 0.04)
                }
                
                total_expenses = sum(expenses.values())
                operating_profit = gross_profit - total_expenses
                operating_margin = (operating_profit / revenue) * 100
                
                taxes = operating_profit * 0.25
                net_profit = operating_profit - taxes
                net_margin = (net_profit / revenue) * 100
                
                pl_data.append({
                    "Month": month,
                    "Revenue": revenue,
                    "COGS": cogs,
                    "Gross Profit": gross_profit,
                    "Gross Margin (%)": gross_margin,
                    "Total Expenses": total_expenses,
                    "Operating Profit": operating_profit,
                    "Operating Margin (%)": operating_margin,
                    "Net Profit": net_profit,
                    "Net Margin (%)": net_margin
                })
            
            df_pl = pd.DataFrame(pl_data)
            st.dataframe(df_pl, use_container_width=True)
            
            # P&L visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Profit Margins Trend")
                
                fig = px.line(df_pl, x="Month", y=["Gross Margin (%)", "Operating Margin (%)", "Net Margin (%)"],
                             title="Monthly Profit Margins")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Revenue vs. Expenses")
                
                fig = px.bar(df_pl, x="Month", y=["Revenue", "COGS", "Total Expenses"],
                            title="Revenue vs. Expenses")
                st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Sales Analysis":
            st.markdown("#### Sales Analysis")
            
            # Generate sales analysis data
            
            # Sales by channel
            channels = ["Online", "Flagship Stores", "Mall Stores", "Department Stores", "Outlet Stores"]
            channel_sales = [random.randint(5000000, 20000000) for _ in range(len(channels))]
            
            df_channels = pd.DataFrame({
                "Channel": channels,
                "Sales": channel_sales
            })
            
            # Sales by region
            regions = ["North", "South", "East", "West", "Central"]
            region_sales = [random.randint(5000000, 20000000) for _ in range(len(regions))]
            
            df_regions = pd.DataFrame({
                "Region": regions,
                "Sales": region_sales
            })
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Sales by Channel")
                
                fig = px.pie(df_channels, values="Sales", names="Channel",
                            title="Sales Distribution by Channel")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Sales by Region")
                
                fig = px.pie(df_regions, values="Sales", names="Region",
                            title="Sales Distribution by Region")
                st.plotly_chart(fig, use_container_width=True)
            
            # Sales trend analysis
            st.markdown("#### Sales Trend Analysis")
            
            # Generate monthly sales data by category
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
            
            sales_data = []
            
            for month in months:
                for category in categories:
                    sales = random.randint(1000000, 5000000)
                    units = random.randint(1000, 5000)
                    avg_price = sales / units
                    
                    sales_data.append({
                        "Month": month,
                        "Category": category,
                        "Sales": sales,
                        "Units": units,
                        "Average Price": avg_price
                    })
            
            df_sales = pd.DataFrame(sales_data)
            
            # Create pivot table for visualization
            pivot_df = df_sales.pivot_table(index="Month", columns="Category", values="Sales", aggfunc="sum")
            
            # Reset index to make Month a column
            pivot_df = pivot_df.reset_index()
            
            fig = px.line(pivot_df, x="Month", y=categories,
                         title="Monthly Sales by Category")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Operational KPIs")
        
        # Create tabs for different operational areas
        op_tab1, op_tab2, op_tab3, op_tab4 = st.tabs(["Inventory", "Supply Chain", "Retail", "Manufacturing"])
        
        with op_tab1:
            st.markdown("#### Inventory KPIs")
            
            # Inventory KPI cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Inventory Turnover", f"{random.uniform(3.0, 6.0):.2f}", f"+{random.uniform(0.1, 0.5):.2f}")
            
            with col2:
                st.metric("Days in Inventory", f"{random.randint(30, 90)}", f"-{random.randint(1, 10)}")
            
            with col3:
                st.metric("Stockout Rate", f"{random.uniform(0.5, 3.0):.2f}%", f"-{random.uniform(0.1, 0.5):.2f}%")
            
            with col4:
                st.metric("Inventory Accuracy", f"{random.uniform(95.0, 99.5):.1f}%", f"+{random.uniform(0.1, 0.5):.1f}%")
            
            # Inventory trend charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Inventory value trend
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                inventory_values = [random.randint(20000000, 50000000) for _ in range(len(months))]
                
                df_inv_trend = pd.DataFrame({
                    "Month": months,
                    "Inventory Value": inventory_values
                })
                
                fig = px.line(df_inv_trend, x="Month", y="Inventory Value",
                             title="Monthly Inventory Value")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Inventory aging
                aging_buckets = ["0-30 days", "31-60 days", "61-90 days", "91-180 days", ">180 days"]
                aging_values = [random.randint(5000000, 20000000) for _ in range(len(aging_buckets))]
                
                df_aging = pd.DataFrame({
                    "Aging": aging_buckets,
                    "Value": aging_values
                })
                
                fig = px.pie(df_aging, values="Value", names="Aging",
                            title="Inventory Aging Distribution")
                st.plotly_chart(fig, use_container_width=True)
        
        with op_tab2:
            st.markdown("#### Supply Chain KPIs")
            
            # Supply chain KPI cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Order Fulfillment Rate", f"{random.uniform(90.0, 99.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            with col2:
                st.metric("On-Time Delivery", f"{random.uniform(85.0, 98.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            with col3:
                st.metric("Lead Time (days)", f"{random.uniform(10.0, 30.0):.1f}", f"-{random.uniform(0.5, 2.0):.1f}")
            
            with col4:
                st.metric("Perfect Order Rate", f"{random.uniform(80.0, 95.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            # Supply chain performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Order cycle time trend
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                cycle_times = [random.uniform(10.0, 30.0) for _ in range(len(months))]
                
                df_cycle = pd.DataFrame({
                    "Month": months,
                    "Order Cycle Time (days)": cycle_times
                })
                
                fig = px.line(df_cycle, x="Month", y="Order Cycle Time (days)",
                             title="Monthly Order Cycle Time")
                
                # Add target line
                fig.add_shape(
                    type="line",
                    x0=0,
                    y0=15,
                    x1=len(months) - 1,
                    y1=15,
                    line=dict(
                        color="Red",
                        width=2,
                        dash="dash",
                    )
                )
                
                # Add annotation for target line
                fig.add_annotation(
                    x=len(months) - 1,
                    y=15,
                    text="Target (15 days)",
                    showarrow=False,
                    yshift=10
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Carrier performance
                carriers = ["BlueDart", "Delhivery", "Ecom Express", "DTDC", "FedEx"]
                on_time_rates = [random.uniform(85.0, 98.0) for _ in range(len(carriers))]
                
                df_carriers = pd.DataFrame({
                    "Carrier": carriers,
                    "On-Time Delivery Rate (%)": on_time_rates
                })
                
                fig = px.bar(df_carriers, x="Carrier", y="On-Time Delivery Rate (%)",
                            title="On-Time Delivery Rate by Carrier")
                
                # Add target line
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=95,
                    x1=len(carriers) - 0.5,
                    y1=95,
                    line=dict(
                        color="Green",
                        width=2,
                        dash="dash",
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with op_tab3:
            st.markdown("#### Retail KPIs")
            
            # Retail KPI cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Same Store Sales Growth", f"{random.uniform(-5.0, 15.0):.1f}%", f"+{random.uniform(0.5, 3.0):.1f}%")
            
            with col2:
                st.metric("Conversion Rate", f"{random.uniform(20.0, 35.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            with col3:
                st.metric("Avg. Transaction Value", f"₹{random.randint(2000, 5000)}", f"+{random.randint(100, 500)}")
            
            with col4:
                st.metric("Sales per Sq.Ft.", f"₹{random.randint(1000, 3000)}", f"+{random.randint(50, 300)}")
            
            # Retail performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Store type performance
                store_types = ["Flagship", "Mall", "High Street", "Express", "Outlet"]
                sales_per_sqft = [random.randint(1000, 3000) for _ in range(len(store_types))]
                conversion_rates = [random.uniform(20.0, 35.0) for _ in range(len(store_types))]
                
                df_store_types = pd.DataFrame({
                    "Store Type": store_types,
                    "Sales per Sq.Ft. (₹)": sales_per_sqft,
                    "Conversion Rate (%)": conversion_rates
                })
                
                fig = px.bar(df_store_types, x="Store Type", y="Sales per Sq.Ft. (₹)",
                            color="Conversion Rate (%)", title="Store Performance by Type")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Regional performance
                regions = ["North", "South", "East", "West", "Central"]
                sales_growth = [random.uniform(-5.0, 15.0) for _ in range(len(regions))]
                
                df_regions = pd.DataFrame({
                    "Region": regions,
                    "Sales Growth (%)": sales_growth
                })
                
                fig = px.bar(df_regions, x="Region", y="Sales Growth (%)",
                            title="Sales Growth by Region")
                
                # Color bars based on positive/negative growth
                fig.update_traces(marker_color=[
                    'green' if x >= 0 else 'red' for x in df_regions["Sales Growth (%)"]
                ])
                
                # Add zero line
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=0,
                    x1=len(regions) - 0.5,
                    y1=0,
                    line=dict(
                        color="Black",
                        width=2,
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with op_tab4:
            st.markdown("#### Manufacturing KPIs")
            
            # Manufacturing KPI cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Production Efficiency", f"{random.uniform(70.0, 95.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            with col2:
                st.metric("Defect Rate", f"{random.uniform(0.5, 3.0):.2f}%", f"-{random.uniform(0.1, 0.5):.2f}%")
            
            with col3:
                st.metric("On-Time Completion", f"{random.uniform(80.0, 95.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            with col4:
                st.metric("Production Utilization", f"{random.uniform(65.0, 90.0):.1f}%", f"+{random.uniform(0.5, 2.0):.1f}%")
            
            # Manufacturing performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Production trend
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                production = [random.randint(50000, 200000) for _ in range(len(months))]
                
                df_production = pd.DataFrame({
                    "Month": months,
                    "Production Volume": production
                })
                
                fig = px.line(df_production, x="Month", y="Production Volume",
                             title="Monthly Production Volume")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Quality control
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                defect_rates = [random.uniform(0.5, 3.0) for _ in range(len(months))]
                
                df_quality = pd.DataFrame({
                    "Month": months,
                    "Defect Rate (%)": defect_rates
                })
                
                fig = px.line(df_quality, x="Month", y="Defect Rate (%)",
                             title="Monthly Defect Rate")
                
                # Add target line
                fig.add_shape(
                    type="line",
                    x0=0,
                    y0=1.5,
                    x1=len(months) - 1,
                    y1=1.5,
                    line=dict(
                        color="Red",
                        width=2,
                        dash="dash",
                    )
                )
                
                # Add annotation for target line
                fig.add_annotation(
                    x=len(months) - 1,
                    y=1.5,
                    text="Target (1.5%)",
                    showarrow=False,
                    yshift=10
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Custom Reports")
        
        # Custom report builder
        st.markdown("#### Custom Report Builder")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            report_category = st.selectbox(
                "Report Category",
                ["Sales", "Inventory", "Manufacturing", "Financial", "Store Performance"]
            )
        
        with col2:
            # Options based on category
            if report_category == "Sales":
                dimension = st.selectbox(
                    "Dimension",
                    ["Product Category", "Region", "Store Type", "Time Period", "Customer Segment"]
                )
            elif report_category == "Inventory":
                dimension = st.selectbox(
                    "Dimension",
                    ["Product Category", "Warehouse", "Aging", "Stock Level", "Turnover Rate"]
                )
            elif report_category == "Manufacturing":
                dimension = st.selectbox(
                    "Dimension",
                    ["Factory", "Production Line", "Quality Metrics", "Efficiency", "Cost Analysis"]
                )
            elif report_category == "Financial":
                dimension = st.selectbox(
                    "Dimension",
                    ["Revenue Analysis", "Cost Structure", "Profitability", "Cash Flow", "Budget vs. Actual"]
                )
            else:  # Store Performance
                dimension = st.selectbox(
                    "Dimension",
                    ["Store Comparison", "Sales per Sq.Ft.", "Conversion Metrics", "Staff Productivity", "Customer Footfall"]
                )
        
        with col3:
            visualization = st.selectbox(
                "Visualization Type",
                ["Table", "Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Heat Map"]
            )
        
        # Time period
        col1, col2 = st.columns(2)
        
        with col1:
            time_period = st.selectbox(
                "Time Period",
                ["Last 30 Days", "Last Quarter", "Last 6 Months", "Year to Date", "Last Year", "Custom Period"]
            )
        
        with col2:
            frequency = st.selectbox(
                "Data Frequency",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]
            )
        
        # Additional options
        include_comparison = st.checkbox("Include Year-over-Year Comparison")
        include_forecast = st.checkbox("Include Forecast")
        
        # Generate dummy report
        if st.button("Generate Report"):
            st.success("Report generated successfully")
            
            # Display a dummy report based on selections
            st.markdown(f"#### {report_category} Report: {dimension}")
            
            # Generate appropriate data and visualization based on selections
            if visualization == "Table":
                # Generate sample data for the table
                data = []
                
                if report_category == "Sales":
                    # Generate sales data
                    categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
                    
                    for category in categories:
                        current_sales = random.randint(1000000, 10000000)
                        previous_sales = random.randint(1000000, 10000000)
                        yoy_change = ((current_sales - previous_sales) / previous_sales) * 100
                        
                        data.append({
                            "Category": category,
                            "Current Period Sales": current_sales,
                            "Previous Period Sales": previous_sales,
                            "YoY Change (%)": round(yoy_change, 2)
                        })
                
                elif report_category == "Inventory":
                    # Generate inventory data
                    categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
                    
                    for category in categories:
                        current_stock = random.randint(1000, 10000)
                        optimal_stock = random.randint(1000, 10000)
                        variance = ((current_stock - optimal_stock) / optimal_stock) * 100
                        turnover = random.uniform(2.0, 6.0)
                        
                        data.append({
                            "Category": category,
                            "Current Stock": current_stock,
                            "Optimal Stock": optimal_stock,
                            "Variance (%)": round(variance, 2),
                            "Turnover Rate": round(turnover, 2)
                        })
                
                # Create and display DataFrame
                df_report = pd.DataFrame(data)
                st.dataframe(df_report, use_container_width=True)
            
            elif visualization in ["Bar Chart", "Line Chart", "Pie Chart"]:
                # Generate sample data for charts
                if report_category == "Sales":
                    # Generate sales data
                    categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
                    current_sales = [random.randint(1000000, 10000000) for _ in range(len(categories))]
                    
                    if include_comparison:
                        previous_sales = [random.randint(1000000, 10000000) for _ in range(len(categories))]
                        df_report = pd.DataFrame({
                            "Category": categories,
                            "Current Period": current_sales,
                            "Previous Period": previous_sales
                        })
                    else:
                        df_report = pd.DataFrame({
                            "Category": categories,
                            "Sales": current_sales
                        })
                
                # Create and display appropriate chart
                if visualization == "Bar Chart":
                    if include_comparison:
                        fig = px.bar(df_report, x="Category", y=["Current Period", "Previous Period"],
                                    title=f"{report_category}: {dimension}")
                    else:
                        fig = px.bar(df_report, x="Category", y="Sales",
                                    title=f"{report_category}: {dimension}")
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif visualization == "Line Chart":
                    # For line chart, create time series data
                    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    values = [random.randint(1000000, 10000000) for _ in range(len(months))]
                    
                    if include_comparison:
                        prev_values = [random.randint(1000000, 10000000) for _ in range(len(months))]
                        df_report = pd.DataFrame({
                            "Month": months,
                            "Current Year": values,
                            "Previous Year": prev_values
                        })
                        
                        fig = px.line(df_report, x="Month", y=["Current Year", "Previous Year"],
                                    title=f"{report_category}: {dimension} Over Time")
                    else:
                        df_report = pd.DataFrame({
                            "Month": months,
                            "Value": values
                        })
                        
                        fig = px.line(df_report, x="Month", y="Value",
                                    title=f"{report_category}: {dimension} Over Time")
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                elif visualization == "Pie Chart":
                    # For pie chart, use categorical data
                    if report_category == "Sales":
                        fig = px.pie(df_report, values="Sales", names="Category",
                                    title=f"{report_category}: {dimension} Distribution")
                        st.plotly_chart(fig, use_container_width=True)
            
            # Add forecast if requested
            if include_forecast:
                st.markdown("#### Forecast")
                
                # Generate forecast data
                forecast_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
                forecast_values = [random.randint(1000000, 10000000) for _ in range(len(forecast_months))]
                
                df_forecast = pd.DataFrame({
                    "Month": forecast_months,
                    "Forecast": forecast_values
                })
                
                fig = px.line(df_forecast, x="Month", y="Forecast",
                             title=f"{report_category} Forecast for Next 6 Months")
                st.plotly_chart(fig, use_container_width=True)

def show_inventory_optimization():
    """Display the Inventory Optimization page with One-Click Recommendations"""
    st.title("Inventory Optimization")
    st.subheader("AI-Powered Optimization Recommendations")
    
    # Optimization banner
    st.info("""
    This module uses advanced analytics and AI algorithms to analyze your inventory data 
    and provide actionable optimization recommendations to improve efficiency and reduce costs.
    """)
    
    # Set up inventory data (in a real application, this would come from a database)
    if 'optimization_data' not in st.session_state:
        # Generate sample inventory data
        inventory_data = []
        
        categories = ["Jeans", "T-Shirts", "Shirts", "Jackets", "Accessories"]
        sub_categories = {
            "Jeans": ["Slim Fit", "Regular Fit", "Relaxed Fit", "Skinny", "Boot Cut"],
            "T-Shirts": ["Round Neck", "V-Neck", "Polo", "Graphic", "Basic"],
            "Shirts": ["Formal", "Casual", "Denim", "Checked", "Printed"],
            "Jackets": ["Bomber", "Denim", "Leather", "Winter", "Casual"],
            "Accessories": ["Belts", "Wallets", "Socks", "Caps", "Bags"]
        }
        
        locations = ["Warehouse A", "Warehouse B", "Store 1", "Store 2", "Store 3"]
        
        for _ in range(200):
            category = random.choice(categories)
            sub_category = random.choice(sub_categories[category])
            sku = f"VOI-{category[:3].upper()}-{random.randint(1000, 9999)}"
            location = random.choice(locations)
            quantity = random.randint(5, 500)
            avg_cost = random.uniform(500, 2000)
            mrp = avg_cost * random.uniform(1.5, 2.5)
            days_in_inventory = random.randint(1, 365)
            sales_velocity = random.randint(1, 50)  # Average units sold per month
            reorder_point = sales_velocity * random.uniform(0.5, 2.0)  # Calculated reorder point
            lead_time = random.randint(7, 45)  # Lead time in days
            
            # Create stocking level flags
            if quantity == 0:
                stock_status = "Out of Stock"
            elif quantity < reorder_point * 0.5:
                stock_status = "Critical"
            elif quantity < reorder_point:
                stock_status = "Low"
            elif quantity > sales_velocity * 6:
                stock_status = "Overstocked"
            else:
                stock_status = "Optimal"
            
            # Calculate recommended order quantity
            if stock_status in ["Out of Stock", "Critical", "Low"]:
                recommended_order = int(max(0, (sales_velocity * 3) - quantity))
            else:
                recommended_order = 0
            
            # Calculate excess inventory
            if stock_status == "Overstocked":
                excess_units = int(quantity - (sales_velocity * 3))
                excess_value = excess_units * avg_cost
            else:
                excess_units = 0
                excess_value = 0
            
            # Calculate days until stockout
            if sales_velocity > 0:
                days_to_stockout = int(quantity / (sales_velocity / 30))
            else:
                days_to_stockout = 999  # Arbitrary high number
            
            inventory_data.append({
                "SKU": sku,
                "Category": category,
                "Sub-Category": sub_category,
                "Location": location,
                "Quantity": quantity,
                "Average Cost": avg_cost,
                "MRP": mrp,
                "Inventory Value": quantity * avg_cost,
                "Days in Inventory": days_in_inventory,
                "Sales Velocity (monthly)": sales_velocity,
                "Reorder Point": int(reorder_point),
                "Lead Time (days)": lead_time,
                "Stock Status": stock_status,
                "Recommended Order": recommended_order,
                "Excess Units": excess_units,
                "Excess Value": excess_value,
                "Days to Stockout": days_to_stockout
            })
        
        st.session_state.optimization_data = pd.DataFrame(inventory_data)
        st.session_state.optimization_applied = False
        st.session_state.show_transfers = False
    
    # Dashboard metrics before optimization
    df = st.session_state.optimization_data
    
    # Calculate key metrics
    total_inventory_value = df["Inventory Value"].sum()
    total_excess_value = df["Excess Value"].sum()
    stockout_risk_count = len(df[df["Stock Status"].isin(["Out of Stock", "Critical", "Low"])])
    optimal_items_count = len(df[df["Stock Status"] == "Optimal"])
    
    st.subheader("Current Inventory Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Inventory Value", 
            f"₹{total_inventory_value:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Excess Inventory Value", 
            f"₹{total_excess_value:,.2f}",
            f"-{(total_excess_value/total_inventory_value*100):.1f}% opportunity",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Stockout Risk Items", 
            f"{stockout_risk_count}",
            f"{(stockout_risk_count/len(df)*100):.1f}% of items"
        )
    
    with col4:
        st.metric(
            "Optimal Stock Items", 
            f"{optimal_items_count}",
            f"{(optimal_items_count/len(df)*100):.1f}% of items"
        )
    
    # Stock status summary
    st.subheader("Stock Status Summary")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Stock status distribution chart
        status_counts = df["Stock Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        # Define color map for statuses
        color_map = {
            "Out of Stock": "red",
            "Critical": "orange",
            "Low": "yellow",
            "Optimal": "green",
            "Overstocked": "blue"
        }
        
        # Create a custom color sequence based on the order in the dataframe
        colors = [color_map[status] for status in status_counts["Status"]]
        
        fig = px.pie(
            status_counts, 
            values="Count", 
            names="Status",
            title="Inventory Status Distribution",
            color="Status",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Key Improvement Opportunities
        st.markdown("### Key Opportunities")
        
        # Calculate opportunity metrics
        excess_percent = (total_excess_value / total_inventory_value) * 100
        stockout_percent = (stockout_risk_count / len(df)) * 100
        avg_days_in_inventory = df["Days in Inventory"].mean()
        
        st.markdown(f"**Excess Inventory:** ₹{total_excess_value:,.2f} ({excess_percent:.1f}%)")
        st.markdown(f"**Stockout Risk:** {stockout_risk_count} items ({stockout_percent:.1f}%)")
        st.markdown(f"**Average Age:** {avg_days_in_inventory:.1f} days")
        
        # One-Click Optimization button
        if not st.session_state.optimization_applied:
            if st.button("🚀 Apply One-Click Optimization"):
                # In a real application, this would run complex algorithms
                # For this demo, we'll simulate optimization by adjusting the data
                df_optimized = df.copy()
                
                # Simulate optimization results
                # 1. Reduce excess inventory
                for idx, row in df_optimized[df_optimized["Stock Status"] == "Overstocked"].iterrows():
                    # Reduce quantity to optimal level (3 months of sales velocity)
                    optimal_quantity = int(row["Sales Velocity (monthly)"] * 3)
                    units_to_reduce = row["Quantity"] - optimal_quantity
                    
                    if units_to_reduce > 0:
                        df_optimized.at[idx, "Quantity"] = optimal_quantity
                        df_optimized.at[idx, "Inventory Value"] = optimal_quantity * row["Average Cost"]
                        df_optimized.at[idx, "Stock Status"] = "Optimal"
                        df_optimized.at[idx, "Excess Units"] = 0
                        df_optimized.at[idx, "Excess Value"] = 0
                        df_optimized.at[idx, "Days to Stockout"] = int(optimal_quantity / (row["Sales Velocity (monthly)"] / 30))
                
                # 2. Restock low inventory
                for idx, row in df_optimized[df_optimized["Stock Status"].isin(["Out of Stock", "Critical", "Low"])].iterrows():
                    # Increase quantity to optimal level (3 months of sales velocity)
                    optimal_quantity = int(row["Sales Velocity (monthly)"] * 3)
                    units_to_add = optimal_quantity - row["Quantity"]
                    
                    if units_to_add > 0:
                        df_optimized.at[idx, "Quantity"] = optimal_quantity
                        df_optimized.at[idx, "Inventory Value"] = optimal_quantity * row["Average Cost"]
                        df_optimized.at[idx, "Stock Status"] = "Optimal"
                        df_optimized.at[idx, "Recommended Order"] = 0
                        df_optimized.at[idx, "Days to Stockout"] = int(optimal_quantity / (row["Sales Velocity (monthly)"] / 30))
                
                # Store optimized data
                st.session_state.optimization_data_original = df.copy()
                st.session_state.optimization_data = df_optimized
                st.session_state.optimization_applied = True
                st.session_state.show_transfers = True
                
                # Rerun to show updated state
                st.rerun()
    
    # Show results after optimization
    if st.session_state.optimization_applied:
        st.success("Optimization successfully applied! Here are the results:")
        
        # Get original and optimized data
        df_original = st.session_state.optimization_data_original
        df_optimized = st.session_state.optimization_data
        
        # Calculate key metrics for comparison
        total_inventory_value_original = df_original["Inventory Value"].sum()
        total_inventory_value_optimized = df_optimized["Inventory Value"].sum()
        
        total_excess_value_original = df_original["Excess Value"].sum()
        total_excess_value_optimized = df_optimized["Excess Value"].sum()
        
        stockout_risk_count_original = len(df_original[df_original["Stock Status"].isin(["Out of Stock", "Critical", "Low"])])
        stockout_risk_count_optimized = len(df_optimized[df_optimized["Stock Status"].isin(["Out of Stock", "Critical", "Low"])])
        
        optimal_items_count_original = len(df_original[df_original["Stock Status"] == "Optimal"])
        optimal_items_count_optimized = len(df_optimized[df_optimized["Stock Status"] == "Optimal"])
        
        # Comparison metrics
        st.subheader("Optimization Impact")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_inventory = total_inventory_value_optimized - total_inventory_value_original
            delta_percent = (delta_inventory / total_inventory_value_original) * 100
            
            st.metric(
                "Total Inventory Value", 
                f"₹{total_inventory_value_optimized:,.2f}",
                f"{delta_percent:.1f}%"
            )
        
        with col2:
            delta_excess = total_excess_value_optimized - total_excess_value_original
            delta_percent = (delta_excess / total_excess_value_original) * 100 if total_excess_value_original > 0 else -100
            
            st.metric(
                "Excess Inventory Value", 
                f"₹{total_excess_value_optimized:,.2f}",
                f"{delta_percent:.1f}%",
                delta_color="inverse"
            )
        
        with col3:
            delta_stockout = stockout_risk_count_optimized - stockout_risk_count_original
            delta_percent = (delta_stockout / stockout_risk_count_original) * 100 if stockout_risk_count_original > 0 else -100
            
            st.metric(
                "Stockout Risk Items", 
                f"{stockout_risk_count_optimized}",
                f"{delta_percent:.1f}%",
                delta_color="inverse"
            )
        
        with col4:
            delta_optimal = optimal_items_count_optimized - optimal_items_count_original
            delta_percent = (delta_optimal / optimal_items_count_original) * 100 if optimal_items_count_original > 0 else 100
            
            st.metric(
                "Optimal Stock Items", 
                f"{optimal_items_count_optimized}",
                f"{delta_percent:.1f}%"
            )
        
        # Stock status distribution after optimization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Before Optimization")
            status_counts_original = df_original["Stock Status"].value_counts().reset_index()
            status_counts_original.columns = ["Status", "Count"]
            
            fig = px.pie(
                status_counts_original, 
                values="Count", 
                names="Status",
                title="Original Inventory Status",
                color="Status",
                color_discrete_map=color_map
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("After Optimization")
            status_counts_optimized = df_optimized["Stock Status"].value_counts().reset_index()
            status_counts_optimized.columns = ["Status", "Count"]
            
            fig = px.pie(
                status_counts_optimized, 
                values="Count", 
                names="Status",
                title="Optimized Inventory Status",
                color="Status",
                color_discrete_map=color_map
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary of recommendations
        st.subheader("Action Plan")
        
        # Calculate changes
        items_to_restock = df_original[df_original["Stock Status"].isin(["Out of Stock", "Critical", "Low"])]
        items_to_reduce = df_original[df_original["Stock Status"] == "Overstocked"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Items to Restock")
            restock_summary = items_to_restock.groupby("Category")["Recommended Order"].sum().reset_index()
            restock_summary.columns = ["Category", "Units to Order"]
            restock_summary["Estimated Cost"] = restock_summary["Units to Order"] * df_original.groupby("Category")["Average Cost"].mean().reset_index()["Average Cost"]
            
            # Only include categories that need restocking
            restock_summary = restock_summary[restock_summary["Units to Order"] > 0]
            
            if len(restock_summary) > 0:
                fig = px.bar(
                    restock_summary,
                    x="Category",
                    y="Units to Order",
                    title="Recommended Restocking by Category",
                    color="Category"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(restock_summary, use_container_width=True)
                
                total_restock_cost = restock_summary["Estimated Cost"].sum()
                st.markdown(f"**Total Estimated Restock Cost:** ₹{total_restock_cost:,.2f}")
            else:
                st.info("No items need restocking.")
        
        with col2:
            st.markdown("### Excess Inventory to Reduce")
            excess_summary = items_to_reduce.groupby("Category")["Excess Units"].sum().reset_index()
            excess_summary.columns = ["Category", "Units to Reduce"]
            excess_summary["Excess Value"] = excess_summary["Units to Reduce"] * df_original.groupby("Category")["Average Cost"].mean().reset_index()["Average Cost"]
            
            # Only include categories with excess inventory
            excess_summary = excess_summary[excess_summary["Units to Reduce"] > 0]
            
            if len(excess_summary) > 0:
                fig = px.bar(
                    excess_summary,
                    x="Category",
                    y="Units to Reduce",
                    title="Excess Inventory by Category",
                    color="Category"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(excess_summary, use_container_width=True)
                
                total_excess_value = excess_summary["Excess Value"].sum()
                st.markdown(f"**Total Excess Inventory Value:** ₹{total_excess_value:,.2f}")
            else:
                st.info("No excess inventory to reduce.")
        
        # Show detailed recommendations
        st.subheader("Detailed Recommendations")
        
        tabs = st.tabs(["Restocking Recommendations", "Excess Inventory", "Inventory Transfers", "All Items"])
        
        with tabs[0]:
            # Items that need restocking
            items_to_restock = df_original[df_original["Stock Status"].isin(["Out of Stock", "Critical", "Low"])].sort_values("Stock Status")
            if len(items_to_restock) > 0:
                st.dataframe(items_to_restock[["SKU", "Category", "Sub-Category", "Location", "Quantity", 
                                              "Reorder Point", "Stock Status", "Recommended Order", 
                                              "Sales Velocity (monthly)", "Days to Stockout"]],
                            use_container_width=True)
            else:
                st.info("No items need restocking.")
        
        with tabs[1]:
            # Items with excess inventory
            items_to_reduce = df_original[df_original["Stock Status"] == "Overstocked"].sort_values("Excess Value", ascending=False)
            if len(items_to_reduce) > 0:
                st.dataframe(items_to_reduce[["SKU", "Category", "Sub-Category", "Location", "Quantity", 
                                             "Sales Velocity (monthly)", "Excess Units", "Excess Value"]],
                            use_container_width=True)
            else:
                st.info("No excess inventory to reduce.")
        
        with tabs[2]:
            if st.session_state.show_transfers:
                st.markdown("### Recommended Inventory Transfers")
                st.info("The system has identified potential inventory transfers to balance stock across locations.")
                
                # Generate sample transfer recommendations
                inventory_transfers = []
                
                # Find items that are overstocked in one location and understocked in another
                overstocked_items = df_original[df_original["Stock Status"] == "Overstocked"].sort_values("Excess Value", ascending=False)
                understocked_items = df_original[df_original["Stock Status"].isin(["Out of Stock", "Critical", "Low"])].sort_values("Stock Status")
                
                # Create sample transfers (this would be more sophisticated in a real system)
                for i in range(min(10, len(overstocked_items), len(understocked_items))):
                    source_item = overstocked_items.iloc[i]
                    dest_item = understocked_items.iloc[i]
                    
                    # Find similar items (same category)
                    similar_overstocked = overstocked_items[overstocked_items["Category"] == dest_item["Category"]]
                    if len(similar_overstocked) > 0:
                        source_item = similar_overstocked.iloc[0]
                    
                    transfer_qty = min(source_item["Excess Units"], dest_item["Recommended Order"])
                    
                    if transfer_qty > 0:
                        transfer_value = transfer_qty * source_item["Average Cost"]
                        
                        inventory_transfers.append({
                            "Source Location": source_item["Location"],
                            "Source SKU": source_item["SKU"],
                            "Category": source_item["Category"],
                            "Destination Location": dest_item["Location"],
                            "Destination SKU": dest_item["SKU"],
                            "Transfer Quantity": transfer_qty,
                            "Transfer Value": transfer_value,
                            "Status": "Recommended"
                        })
                
                if len(inventory_transfers) > 0:
                    df_transfers = pd.DataFrame(inventory_transfers)
                    st.dataframe(df_transfers, use_container_width=True)
                    
                    total_transfer_value = df_transfers["Transfer Value"].sum()
                    st.markdown(f"**Total Transfer Value:** ₹{total_transfer_value:,.2f}")
                    st.markdown(f"**Total Items to Transfer:** {df_transfers['Transfer Quantity'].sum()}")
                    
                    if st.button("Generate Transfer Orders"):
                        st.success("Transfer orders have been generated and sent to warehouse managers for execution.")
                else:
                    st.info("No suitable transfers identified.")
            else:
                st.info("Apply optimization first to see inventory transfer recommendations.")
        
        with tabs[3]:
            # All items with their current status
            st.dataframe(df_optimized[["SKU", "Category", "Sub-Category", "Location", "Quantity", 
                                      "Inventory Value", "Stock Status", "Sales Velocity (monthly)",
                                      "Reorder Point", "Days to Stockout"]].sort_values("Stock Status"),
                        use_container_width=True)
        
        # Implementation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate Purchase Orders"):
                st.success("Purchase orders have been generated for all items that need restocking.")
        
        with col2:
            if st.button("Schedule Promotion Campaign"):
                st.success("Promotion campaign has been scheduled for items with excess inventory.")
        
        with col3:
            if st.button("Reset Optimization"):
                # Reset to original state
                st.session_state.optimization_applied = False
                st.session_state.show_transfers = False
                st.session_state.optimization_data = st.session_state.optimization_data_original
                st.rerun()
    
    # Inventory health score
    st.subheader("Inventory Health Score")
    
    # Calculate a simple health score based on various factors
    df = st.session_state.optimization_data
    
    # Factors for health score (0-100 scale)
    percent_optimal = (len(df[df["Stock Status"] == "Optimal"]) / len(df)) * 100
    percent_overstock = (len(df[df["Stock Status"] == "Overstocked"]) / len(df)) * 100
    percent_stockout_risk = (len(df[df["Stock Status"].isin(["Out of Stock", "Critical", "Low"])]) / len(df)) * 100
    
    avg_days_in_inventory = min(100, df["Days in Inventory"].mean())  # Cap at 100 days
    days_in_inventory_score = max(0, 100 - avg_days_in_inventory)
    
    # Calculate overall health score (weighted average)
    health_score = (
        percent_optimal * 0.4 +  # 40% weight to optimal stock items
        (100 - percent_overstock) * 0.3 +  # 30% weight to not having overstock
        (100 - percent_stockout_risk) * 0.2 +  # 20% weight to not having stockout risk
        days_in_inventory_score * 0.1  # 10% weight to days in inventory
    )
    
    # Display health score gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        title={"text": "Inventory Health Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 40], "color": "red"},
                {"range": [40, 60], "color": "orange"},
                {"range": [60, 80], "color": "yellow"},
                {"range": [80, 100], "color": "green"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": health_score
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Health score interpretation
    if health_score >= 80:
        st.success("Your inventory is well-optimized. Continue to maintain these levels for optimal performance.")
    elif health_score >= 60:
        st.warning("Your inventory is reasonably healthy but has opportunities for improvement. Focus on the recommendations above.")
    elif health_score >= 40:
        st.error("Your inventory needs significant optimization. Follow the recommendations to improve efficiency.")
    else:
        st.error("Your inventory is in critical condition. Immediate action is required to address the issues highlighted above.")

def show_settings():
    """Display the settings page"""
    st.title("Settings")
    st.subheader("System Configuration and Preferences")
    
    # Tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs(["User Preferences", "System Configuration", "Data Integration", "Notifications"])
    
    with tab1:
        st.markdown("### User Preferences")
        
        # User profile
        st.markdown("#### User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Name", value="John Doe")
            st.text_input("Email", value="john.doe@voijeans.com")
            st.text_input("Position", value=st.session_state.user_role)
        
        with col2:
            st.selectbox("Default Dashboard", ["Home Dashboard", "Inventory Analytics", "Store Performance"])
            st.selectbox("Default View", ["Detailed", "Summary", "Executive"])
            st.multiselect("Favorite Reports", ["Inventory Status", "Sales Analytics", "Store Performance", "Manufacturing KPIs"])
        
        # Display settings
        st.markdown("#### Display Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Theme", ["Light", "Dark", "System Default"])
            st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            st.selectbox("Number Format", ["1,234.56", "1.234,56", "1 234.56"])
        
        with col2:
            st.selectbox("Default Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
            st.selectbox("Start Page", ["Dashboard", "Last Visited", "Custom"])
            st.slider("Items Per Page", min_value=10, max_value=100, value=25, step=5)
        
        # Save preferences button
        st.button("Save Preferences")
    
    with tab2:
        st.markdown("### System Configuration")
        
        # System settings
        st.markdown("#### General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Language", ["English", "Hindi", "Marathi", "Tamil", "Telugu"])
            st.selectbox("Time Zone", ["Asia/Kolkata (IST)", "UTC", "America/New_York", "Europe/London"])
            st.number_input("Session Timeout (minutes)", min_value=5, max_value=120, value=30)
        
        with col2:
            st.selectbox("Date Range Presets", ["Last 7 Days, Last 30 Days, Last Quarter, Last Year", "Custom"])
            st.selectbox("Default Export Format", ["Excel (.xlsx)", "CSV", "PDF"])
            st.checkbox("Enable Advanced Analytics", value=True)
        
        # Data refresh settings
        st.markdown("#### Data Refresh Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Inventory Data Refresh", ["Real-time", "Hourly", "Daily", "Manual"])
            st.selectbox("Sales Data Refresh", ["Real-time", "Hourly", "Daily", "Manual"])
            st.selectbox("Manufacturing Data Refresh", ["Real-time", "Hourly", "Daily", "Manual"])
        
        with col2:
            st.selectbox("Financial Data Refresh", ["Daily", "Weekly", "Monthly", "Manual"])
            st.selectbox("Analytics Data Refresh", ["Daily", "Weekly", "Manual"])
            st.time_input("Scheduled Refresh Time", datetime.now().time())
        
        # Save configuration button
        st.button("Save Configuration")
    
    with tab3:
        st.markdown("### Data Integration")
        
        # Data sources
        st.markdown("#### Data Sources")
        
        data_sources = [
            {
                "Source": "ERP System",
                "Status": "Connected",
                "Last Sync": "2023-12-15 08:30",
                "Sync Frequency": "Hourly"
            },
            {
                "Source": "POS System",
                "Status": "Connected",
                "Last Sync": "2023-12-15 09:15",
                "Sync Frequency": "Real-time"
            },
            {
                "Source": "Manufacturing MES",
                "Status": "Connected",
                "Last Sync": "2023-12-15 06:00",
                "Sync Frequency": "Daily"
            },
            {
                "Source": "Warehouse Management System",
                "Status": "Connected",
                "Last Sync": "2023-12-15 07:45",
                "Sync Frequency": "Hourly"
            },
            {
                "Source": "Financial System",
                "Status": "Connected",
                "Last Sync": "2023-12-15 00:15",
                "Sync Frequency": "Daily"
            }
        ]
        
        df_sources = pd.DataFrame(data_sources)
        st.dataframe(df_sources, use_container_width=True)
        
        # Integration actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("Add New Data Source")
        
        with col2:
            st.button("Test Connections")
        
        with col3:
            st.button("Sync All Data Sources")
        
        # API configuration
        st.markdown("#### API Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("API Endpoint URL", value="https://api.voijeans.com/v1")
            st.text_input("API Key", value="******************************", type="password")
            st.selectbox("Authentication Method", ["API Key", "OAuth2", "Basic Auth"])
        
        with col2:
            st.number_input("Request Timeout (seconds)", min_value=5, max_value=120, value=30)
            st.number_input("Rate Limit (requests/minute)", min_value=10, max_value=1000, value=100)
            st.checkbox("Enable Webhook Notifications", value=True)
        
        # Save API configuration button
        st.button("Save API Configuration")
    
    with tab4:
        st.markdown("### Notifications")
        
        # Notification settings
        st.markdown("#### Notification Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Email Notifications", value=True)
            st.checkbox("In-App Notifications", value=True)
            st.checkbox("Mobile Push Notifications", value=False)
        
        with col2:
            st.checkbox("SMS Notifications", value=False)
            st.checkbox("Daily Digest", value=True)
            st.checkbox("Critical Alerts Only", value=False)
        
        # Notification events
        st.markdown("#### Notification Events")
        
        notification_events = [
            {
                "Event": "Low Stock Alert",
                "Email": True,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            },
            {
                "Event": "New Order Received",
                "Email": True,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            },
            {
                "Event": "Shipment Status Update",
                "Email": True,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            },
            {
                "Event": "Price Change",
                "Email": False,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            },
            {
                "Event": "Sales Target Achievement",
                "Email": True,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            },
            {
                "Event": "System Maintenance",
                "Email": True,
                "In-App": True,
                "Mobile": False,
                "SMS": False
            }
        ]
        
        df_events = pd.DataFrame(notification_events)
        st.dataframe(df_events, use_container_width=True)
        
        # Save notification settings button
        st.button("Save Notification Settings")

if __name__ == "__main__":
    main()