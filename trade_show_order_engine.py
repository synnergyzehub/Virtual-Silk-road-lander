import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import uuid
from database import get_db_session
from sqlalchemy import text
import io
import base64

def show_trade_show_order_engine():
    """Display the bespoke trade show and procurement order engine interface"""
    st.title("Trade Show & Procurement Order Engine")
    
    # Create sidebar for navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Select a page", [
        "Dashboard", 
        "Trade Show Order Manager", 
        "Procurement Planner",
        "Sample Management",
        "Timeline & Calendar"
    ])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Trade Show Order Manager":
        show_trade_show_order_manager()
    elif page == "Procurement Planner":
        show_procurement_planner()
    elif page == "Sample Management":
        show_sample_management()
    elif page == "Timeline & Calendar":
        show_timeline_calendar()

def show_dashboard():
    """Display the dashboard with key metrics and insights"""
    st.header("Trade Show & Procurement Dashboard")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Trade Shows", 
            value="4", 
            delta="1",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Pending Orders", 
            value="28", 
            delta="5",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Order Value (₹)", 
            value="₹ 4.2M", 
            delta="12%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Sample Success Rate", 
            value="82%", 
            delta="3%",
            delta_color="normal"
        )
    
    # Create dual-section layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Order Status Overview")
        
        # Sample order data
        order_status = pd.DataFrame({
            "Status": ["Draft", "Pending Approval", "Approved", "In Production", "Completed", "Cancelled"],
            "Count": [12, 28, 35, 45, 62, 8],
            "Value (₹)": [480000, 1120000, 1400000, 1800000, 2480000, 320000]
        })
        
        # Create bar chart with line
        fig = go.Figure()
        
        # Add bars for count
        fig.add_trace(go.Bar(
            x=order_status["Status"],
            y=order_status["Count"],
            name="Order Count",
            marker_color="royalblue"
        ))
        
        # Add line for value
        fig.add_trace(go.Scatter(
            x=order_status["Status"],
            y=order_status["Value (₹)"],
            name="Order Value (₹)",
            yaxis="y2",
            mode="lines+markers",
            marker=dict(size=8, symbol="diamond", color="crimson"),
            line=dict(width=2, dash="dot")
        ))
        
        # Update layout
        fig.update_layout(
            title_text="Order Status Distribution",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Order Count"),
            yaxis2=dict(title="Order Value (₹)", overlaying="y", side="right")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Upcoming trade shows
        st.subheader("Upcoming Trade Shows")
        
        trade_shows = pd.DataFrame({
            "Show Name": [
                "India International Garment Fair", 
                "Denim Expo Mumbai", 
                "Fashion Connect Asia", 
                "Textile India"
            ],
            "Location": ["New Delhi", "Mumbai", "Bangalore", "Ahmedabad"],
            "Start Date": ["2024-06-15", "2024-07-22", "2024-08-10", "2024-09-05"],
            "End Date": ["2024-06-18", "2024-07-25", "2024-08-13", "2024-09-08"],
            "Status": ["Confirmed", "Planning", "Confirmed", "Planning"]
        })
        
        # Add days column
        trade_shows["Days"] = (pd.to_datetime(trade_shows["End Date"]) - 
                               pd.to_datetime(trade_shows["Start Date"])).dt.days + 1
        
        # Add days remaining column
        trade_shows["Days Remaining"] = (pd.to_datetime(trade_shows["Start Date"]) - 
                                         datetime.now()).dt.days
        
        # Filter to only show upcoming
        trade_shows = trade_shows[trade_shows["Days Remaining"] > 0]
        
        # Format table
        formatted_shows = trade_shows[["Show Name", "Location", "Start Date", "End Date", "Status", "Days Remaining"]]
        formatted_shows = formatted_shows.sort_values("Days Remaining")
        
        st.dataframe(formatted_shows, use_container_width=True)
    
    with col2:
        st.subheader("Sample Development Status")
        
        # Sample data for sample development
        sample_status = pd.DataFrame({
            "Status": ["Draft", "Design Review", "In Development", "Ready for Approval", "Approved", "Rejected"],
            "Count": [15, 22, 18, 12, 35, 8]
        })
        
        # Create pie chart
        fig = px.pie(
            sample_status, 
            values="Count", 
            names="Status",
            title="Sample Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top requested styles
        st.subheader("Top Requested Styles")
        
        top_styles = pd.DataFrame({
            "Style": ["Skinny Fit Denim", "Slim Straight Jeans", "Denim Jacket", "Cargo Pants", "Relaxed Fit Jeans"],
            "Count": [42, 36, 28, 25, 22]
        })
        
        # Create horizontal bar chart
        fig = px.bar(
            top_styles, 
            y="Style", 
            x="Count",
            orientation="h",
            title="Most Requested Styles",
            color="Count",
            color_continuous_scale="Blues"
        )
        
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick access buttons
        st.subheader("Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("New Order")
            st.button("New Sample")
        
        with col2:
            st.button("Pending Approvals")
            st.button("Calendar View")

def show_trade_show_order_manager():
    """Display the trade show order manager interface"""
    st.header("Trade Show Order Manager")
    
    # Create tabs for different functions
    tab1, tab2, tab3 = st.tabs(["Order Entry", "Order Tracking", "Reporting"])
    
    with tab1:
        st.subheader("New Trade Show Order")
        
        # Trade show selection
        trade_shows = [
            "India International Garment Fair (Jun 2024)",
            "Denim Expo Mumbai (Jul 2024)",
            "Fashion Connect Asia (Aug 2024)",
            "Textile India (Sep 2024)",
            "Other (Specify)"
        ]
        
        selected_show = st.selectbox("Select Trade Show", trade_shows)
        
        if selected_show == "Other (Specify)":
            custom_show = st.text_input("Specify Trade Show Name")
        
        # Order details
        col1, col2 = st.columns(2)
        
        with col1:
            buyer_name = st.text_input("Buyer Name")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
        
        with col2:
            order_date = st.date_input("Order Date", datetime.now())
            expected_delivery = st.date_input("Expected Delivery", datetime.now() + timedelta(days=90))
            phone = st.text_input("Phone Number")
        
        # Style details
        st.subheader("Style Details")
        
        # Add multiple styles
        if "trade_show_styles" not in st.session_state:
            st.session_state.trade_show_styles = [{
                "id": str(uuid.uuid4()),
                "style_number": "",
                "description": "",
                "category": "Jeans",
                "color": "",
                "sizes": [],
                "quantity": 0,
                "unit_price": 0.0,
                "total_price": 0.0,
                "fabric_requirement": 0.0,
                "comments": ""
            }]
        
        # Categories
        categories = ["Jeans", "Jacket", "Shirt", "T-Shirt", "Shorts", "Skirt", "Dress", "Other"]
        
        # Size options
        size_options = ["XS", "S", "M", "L", "XL", "XXL", "28", "30", "32", "34", "36", "38", "40", "42"]
        
        for i, style in enumerate(st.session_state.trade_show_styles):
            st.markdown(f"### Style {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                style["style_number"] = st.text_input("Style Number", style["style_number"], key=f"style_num_{style['id']}")
                style["description"] = st.text_area("Description", style["description"], key=f"desc_{style['id']}", height=100)
                style["category"] = st.selectbox("Category", categories, categories.index(style["category"]) if style["category"] in categories else 0, key=f"cat_{style['id']}")
                style["color"] = st.text_input("Color", style["color"], key=f"color_{style['id']}")
            
            with col2:
                style["sizes"] = st.multiselect("Sizes", size_options, style["sizes"], key=f"sizes_{style['id']}")
                style["quantity"] = st.number_input("Total Quantity", min_value=0, value=style["quantity"], key=f"qty_{style['id']}")
                style["unit_price"] = st.number_input("Unit Price (₹)", min_value=0.0, value=style["unit_price"], key=f"price_{style['id']}")
                
                # Calculate total price
                style["total_price"] = style["quantity"] * style["unit_price"]
                st.text(f"Total Price: ₹ {style['total_price']:,.2f}")
            
            style["fabric_requirement"] = st.slider(
                "Fabric Requirement (meters per piece)", 
                min_value=0.0, 
                max_value=5.0, 
                value=style["fabric_requirement"] if style["fabric_requirement"] > 0 else 1.5,
                step=0.1,
                key=f"fabric_{style['id']}"
            )
            
            style["comments"] = st.text_area("Special Instructions", style["comments"], key=f"comments_{style['id']}")
            
            # Delete button for this style (except first one)
            if i > 0:
                if st.button("Remove Style", key=f"remove_{style['id']}"):
                    st.session_state.trade_show_styles.pop(i)
                    st.rerun()
            
            st.markdown("---")
        
        # Add another style button
        if st.button("Add Another Style"):
            st.session_state.trade_show_styles.append({
                "id": str(uuid.uuid4()),
                "style_number": "",
                "description": "",
                "category": "Jeans",
                "color": "",
                "sizes": [],
                "quantity": 0,
                "unit_price": 0.0,
                "total_price": 0.0,
                "fabric_requirement": 0.0,
                "comments": ""
            })
            st.rerun()
        
        # Calculate order summary
        total_styles = len(st.session_state.trade_show_styles)
        total_quantity = sum(style["quantity"] for style in st.session_state.trade_show_styles)
        total_value = sum(style["total_price"] for style in st.session_state.trade_show_styles)
        
        # Order summary
        st.subheader("Order Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Styles", total_styles)
        
        with col2:
            st.metric("Total Quantity", total_quantity)
        
        with col3:
            st.metric("Total Value", f"₹ {total_value:,.2f}")
        
        # Material requirements
        st.subheader("Material Requirements")
        
        total_fabric = sum(style["fabric_requirement"] * style["quantity"] for style in st.session_state.trade_show_styles)
        
        st.info(f"Total Fabric Required: {total_fabric:,.2f} meters")
        
        # Save or submit actions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Save as Draft"):
                st.success("Order saved as draft")
        
        with col2:
            if st.button("Submit Order"):
                if buyer_name and total_quantity > 0:
                    st.success("Order submitted successfully")
                    
                    # Generate order ID
                    order_id = f"TS-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(1000, 9999)}"
                    st.info(f"Order ID: {order_id}")
                    
                    # Reset form if needed
                    # st.session_state.trade_show_styles = [st.session_state.trade_show_styles[0]]
                    # for style in st.session_state.trade_show_styles:
                    #     for key in style:
                    #         if key != 'id' and key != 'category':
                    #             style[key] = "" if isinstance(style[key], str) else ([] if isinstance(style[key], list) else 0)
                else:
                    st.error("Please fill in all required fields")
    
    with tab2:
        st.subheader("Order Tracking")
        
        # Sample order data
        orders = pd.DataFrame({
            "Order ID": [f"TS-20240{i}-{1000+i}" for i in range(1, 11)],
            "Buyer": [
                "Fashion Retail Ltd", "Denim Connection", "Style Hub", "Apparel Group",
                "Textile Traders", "Fashion Avenue", "Garment Gallery", "Attire Associates",
                "Clothing Connect", "Fashion Forward"
            ],
            "Trade Show": [
                "India International Garment Fair", "Denim Expo Mumbai", "Fashion Connect Asia",
                "Textile India", "India International Garment Fair", "Denim Expo Mumbai",
                "Fashion Connect Asia", "Textile India", "India International Garment Fair", 
                "Denim Expo Mumbai"
            ],
            "Order Date": [
                "2024-01-15", "2024-01-22", "2024-02-05", "2024-02-12", "2024-02-18",
                "2024-02-25", "2024-03-03", "2024-03-10", "2024-03-15", "2024-03-22"
            ],
            "Delivery Date": [
                "2024-04-15", "2024-04-22", "2024-05-05", "2024-05-12", "2024-05-18",
                "2024-05-25", "2024-06-03", "2024-06-10", "2024-06-15", "2024-06-22"
            ],
            "Styles": [3, 5, 2, 4, 1, 3, 2, 6, 3, 4],
            "Total Qty": [1500, 2500, 800, 1800, 500, 1200, 700, 3000, 1100, 2000],
            "Value (₹)": [
                675000, 1125000, 360000, 810000, 225000, 540000, 315000, 1350000, 495000, 900000
            ],
            "Status": [
                "Completed", "Completed", "In Production", "In Production", "In Production",
                "Approved", "Approved", "Pending Approval", "Draft", "Draft"
            ]
        })
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            buyer_filter = st.multiselect("Filter by Buyer", options=orders["Buyer"].unique())
        
        with col2:
            show_filter = st.multiselect("Filter by Trade Show", options=orders["Trade Show"].unique())
        
        with col3:
            status_filter = st.multiselect("Filter by Status", options=orders["Status"].unique())
        
        # Apply filters
        filtered_orders = orders
        
        if buyer_filter:
            filtered_orders = filtered_orders[filtered_orders["Buyer"].isin(buyer_filter)]
        
        if show_filter:
            filtered_orders = filtered_orders[filtered_orders["Trade Show"].isin(show_filter)]
        
        if status_filter:
            filtered_orders = filtered_orders[filtered_orders["Status"].isin(status_filter)]
        
        # Convert columns to appropriate dtypes
        filtered_orders["Order Date"] = pd.to_datetime(filtered_orders["Order Date"])
        filtered_orders["Delivery Date"] = pd.to_datetime(filtered_orders["Delivery Date"])
        
        # Calculate days to delivery
        filtered_orders["Days to Delivery"] = (filtered_orders["Delivery Date"] - datetime.now()).dt.days
        
        # Format for display
        display_orders = filtered_orders.copy()
        display_orders["Order Date"] = display_orders["Order Date"].dt.strftime("%d-%b-%Y")
        display_orders["Delivery Date"] = display_orders["Delivery Date"].dt.strftime("%d-%b-%Y")
        display_orders["Value (₹)"] = display_orders["Value (₹)"].apply(lambda x: f"₹ {x:,.0f}")
        
        # Display table
        st.dataframe(
            display_orders,
            column_config={
                "Days to Delivery": st.column_config.NumberColumn(
                    "Days to Delivery",
                    help="Days remaining until delivery due date",
                    format="%d days",
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Order status",
                    width="medium",
                    options=[
                        "Draft", "Pending Approval", "Approved", 
                        "In Production", "Completed", "Cancelled"
                    ],
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Order details expansion
        st.subheader("Order Details")
        selected_order = st.selectbox("Select Order ID", orders["Order ID"])
        
        # Sample order details
        st.info(f"Showing details for Order {selected_order}")
        
        # Order header
        selected_row = orders[orders["Order ID"] == selected_order].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Buyer:** {selected_row['Buyer']}")
            st.markdown(f"**Order Date:** {pd.to_datetime(selected_row['Order Date']).strftime('%d-%b-%Y')}")
            st.markdown(f"**Status:** {selected_row['Status']}")
        
        with col2:
            st.markdown(f"**Trade Show:** {selected_row['Trade Show']}")
            st.markdown(f"**Delivery Date:** {pd.to_datetime(selected_row['Delivery Date']).strftime('%d-%b-%Y')}")
            st.markdown(f"**Days to Delivery:** {(pd.to_datetime(selected_row['Delivery Date']) - datetime.now()).days} days")
        
        with col3:
            st.markdown(f"**Total Styles:** {selected_row['Styles']}")
            st.markdown(f"**Total Quantity:** {selected_row['Total Qty']:,}")
            st.markdown(f"**Total Value:** ₹ {selected_row['Value (₹)']:,}")
        
        # Style breakdown
        styles_data = []
        np.random.seed(int(selected_order[-4:]))  # Use order number as seed for consistent random data
        
        for i in range(selected_row["Styles"]):
            style_name = f"STY-{selected_order[-4:]}-{101+i}"
            quantity = int(selected_row["Total Qty"] / selected_row["Styles"] * (0.8 + 0.4 * np.random.random()))
            price = selected_row["Value (₹)"] / selected_row["Total Qty"] * (0.9 + 0.2 * np.random.random())
            
            styles_data.append({
                "Style Number": style_name,
                "Description": np.random.choice([
                    "Skinny Fit Denim Jeans", "Relaxed Fit Jeans", "Slim Straight Jeans",
                    "Denim Jacket", "Denim Shirt", "Cargo Pants", "Denim Shorts"
                ]),
                "Category": np.random.choice(["Jeans", "Jacket", "Shirt", "Shorts"]),
                "Color": np.random.choice(["Blue", "Black", "Grey", "Indigo", "White"]),
                "Quantity": quantity,
                "Unit Price (₹)": price,
                "Total Price (₹)": quantity * price,
                "Status": selected_row["Status"] if np.random.random() > 0.3 else np.random.choice([
                    "Draft", "Pending Approval", "Approved", "In Production", "Completed"
                ])
            })
        
        styles_df = pd.DataFrame(styles_data)
        
        # Format for display
        styles_df["Unit Price (₹)"] = styles_df["Unit Price (₹)"].apply(lambda x: f"₹ {x:.2f}")
        styles_df["Total Price (₹)"] = styles_df["Total Price (₹)"].apply(lambda x: f"₹ {x:,.2f}")
        
        # Show styles
        st.markdown("#### Style Breakdown")
        st.dataframe(styles_df, hide_index=True, use_container_width=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Edit Order"):
                st.info("Opening order for editing...")
        
        with col2:
            if st.button("Download PDF"):
                st.info("Generating PDF...")
        
        with col3:
            if st.button("Send to Production"):
                st.success("Order sent to production successfully")
        
        with col4:
            if st.button("Cancel Order"):
                st.error("Order cancelled")
    
    with tab3:
        st.subheader("Trade Show Order Analytics")
        
        # Date range filter
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
        
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        
        # Sample analytics data
        order_data = pd.DataFrame({
            "Month": pd.date_range(start="2024-01-01", periods=6, freq="M"),
            "Trade Show Orders": [15, 22, 18, 25, 30, 20],
            "Regular Orders": [42, 38, 45, 40, 48, 52],
            "Trade Show Value (₹)": [6750000, 9900000, 8100000, 11250000, 13500000, 9000000],
            "Regular Value (₹)": [18900000, 17100000, 20250000, 18000000, 21600000, 23400000]
        })
        
        # Format dates
        order_data["Month"] = order_data["Month"].dt.strftime("%b %Y")
        
        # Create tabs for different analyses
        analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs([
            "Order Volume Comparison", 
            "Trade Show Performance", 
            "Buyer Analysis"
        ])
        
        with analysis_tab1:
            st.subheader("Trade Show vs Regular Orders")
            
            # Create bar chart
            fig = go.Figure()
            
            # Add Trade Show Orders bars
            fig.add_trace(go.Bar(
                x=order_data["Month"],
                y=order_data["Trade Show Orders"],
                name="Trade Show Orders",
                marker_color="royalblue"
            ))
            
            # Add Regular Orders bars
            fig.add_trace(go.Bar(
                x=order_data["Month"],
                y=order_data["Regular Orders"],
                name="Regular Orders",
                marker_color="lightslategray"
            ))
            
            # Add Trade Show Value line
            fig.add_trace(go.Scatter(
                x=order_data["Month"],
                y=order_data["Trade Show Value (₹)"] / 1000000,  # Convert to millions
                name="Trade Show Value (₹M)",
                yaxis="y2",
                mode="lines+markers",
                marker=dict(size=8, symbol="diamond", color="crimson"),
                line=dict(width=2)
            ))
            
            # Add Regular Value line
            fig.add_trace(go.Scatter(
                x=order_data["Month"],
                y=order_data["Regular Value (₹)"] / 1000000,  # Convert to millions
                name="Regular Value (₹M)",
                yaxis="y2",
                mode="lines+markers",
                marker=dict(size=8, symbol="circle", color="green"),
                line=dict(width=2, dash="dot")
            ))
            
            # Update layout
            fig.update_layout(
                title_text="Order Volume and Value Comparison",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(title="Order Count"),
                yaxis2=dict(title="Order Value (₹M)", overlaying="y", side="right"),
                barmode="group"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            trade_show_total = order_data["Trade Show Orders"].sum()
            regular_total = order_data["Regular Orders"].sum()
            trade_show_value = order_data["Trade Show Value (₹)"].sum()
            regular_value = order_data["Regular Value (₹)"].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Trade Show Orders", 
                    value=trade_show_total,
                    delta=f"{trade_show_total/(trade_show_total+regular_total)*100:.1f}%"
                )
            
            with col2:
                st.metric(
                    label="Regular Orders", 
                    value=regular_total,
                    delta=f"{regular_total/(trade_show_total+regular_total)*100:.1f}%"
                )
            
            with col3:
                st.metric(
                    label="Trade Show Value", 
                    value=f"₹{trade_show_value/10000000:.1f}Cr",
                    delta=f"{trade_show_value/(trade_show_value+regular_value)*100:.1f}%"
                )
            
            with col4:
                st.metric(
                    label="Regular Value", 
                    value=f"₹{regular_value/10000000:.1f}Cr",
                    delta=f"{regular_value/(trade_show_value+regular_value)*100:.1f}%"
                )
        
        with analysis_tab2:
            st.subheader("Trade Show Performance Analysis")
            
            # Sample trade show performance data
            trade_show_perf = pd.DataFrame({
                "Trade Show": [
                    "India International Garment Fair", 
                    "Denim Expo Mumbai",
                    "Fashion Connect Asia",
                    "Textile India"
                ],
                "Orders": [35, 28, 22, 45],
                "Value (₹)": [15750000, 12600000, 9900000, 20250000],
                "Avg. Order Value (₹)": [450000, 450000, 450000, 450000],
                "Buyers": [18, 15, 12, 22],
                "Conversion Rate (%)": [72, 68, 55, 78]
            })
            
            # Create bubble chart
            fig = px.scatter(
                trade_show_perf,
                x="Orders",
                y="Value (₹)",
                size="Buyers",
                color="Trade Show",
                hover_name="Trade Show",
                size_max=60,
                text="Trade Show"
            )
            
            # Update layout
            fig.update_layout(
                title_text="Trade Show Performance Comparison",
                xaxis_title="Number of Orders",
                yaxis_title="Total Value (₹)",
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            
            fig.update_traces(
                textposition="top center",
                marker=dict(opacity=0.7, line=dict(width=1, color="white"))
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show details table
            st.dataframe(trade_show_perf, hide_index=True, use_container_width=True)
            
            # Show ROI analysis
            st.subheader("Trade Show ROI Analysis")
            
            trade_show_roi = pd.DataFrame({
                "Trade Show": [
                    "India International Garment Fair", 
                    "Denim Expo Mumbai",
                    "Fashion Connect Asia",
                    "Textile India"
                ],
                "Total Cost (₹)": [1200000, 950000, 850000, 1500000],
                "Revenue Generated (₹)": [15750000, 12600000, 9900000, 20250000],
                "ROI (%)": [1213, 1226, 1065, 1250]
            })
            
            # Add cost breakdown
            cost_breakdown = {
                "India International Garment Fair": {
                    "Booth Rental": 600000,
                    "Travel & Accommodation": 250000,
                    "Samples & Marketing": 200000,
                    "Miscellaneous": 150000
                },
                "Denim Expo Mumbai": {
                    "Booth Rental": 500000,
                    "Travel & Accommodation": 180000,
                    "Samples & Marketing": 170000,
                    "Miscellaneous": 100000
                },
                "Fashion Connect Asia": {
                    "Booth Rental": 420000,
                    "Travel & Accommodation": 150000,
                    "Samples & Marketing": 180000,
                    "Miscellaneous": 100000
                },
                "Textile India": {
                    "Booth Rental": 750000,
                    "Travel & Accommodation": 320000,
                    "Samples & Marketing": 280000,
                    "Miscellaneous": 150000
                }
            }
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create ROI chart
                fig = px.bar(
                    trade_show_roi,
                    x="Trade Show",
                    y=["Total Cost (₹)", "Revenue Generated (₹)"],
                    barmode="group",
                    title="Cost vs Revenue by Trade Show",
                    log_y=True  # Using log scale due to large difference
                )
                
                # Add ROI as text labels
                for i, show in enumerate(trade_show_roi["Trade Show"]):
                    fig.add_annotation(
                        x=show,
                        y=trade_show_roi.iloc[i]["Revenue Generated (₹)"],
                        text=f"ROI: {trade_show_roi.iloc[i]['ROI (%)']}%",
                        showarrow=True,
                        arrowhead=3,
                        ax=0,
                        ay=-40
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Allow selecting a trade show for cost breakdown
                selected_show_roi = st.selectbox(
                    "Select Trade Show for Cost Breakdown",
                    trade_show_roi["Trade Show"]
                )
                
                # Create pie chart for cost breakdown
                cost_data = pd.DataFrame({
                    "Category": list(cost_breakdown[selected_show_roi].keys()),
                    "Amount (₹)": list(cost_breakdown[selected_show_roi].values())
                })
                
                fig = px.pie(
                    cost_data,
                    values="Amount (₹)",
                    names="Category",
                    title=f"Cost Breakdown: {selected_show_roi}",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
                st.plotly_chart(fig, use_container_width=True)
        
        with analysis_tab3:
            st.subheader("Buyer Analysis by Trade Show")
            
            # Sample buyer data
            buyer_data = pd.DataFrame({
                "Buyer": [
                    "Fashion Retail Ltd", "Denim Connection", "Style Hub", "Apparel Group",
                    "Textile Traders", "Fashion Avenue", "Garment Gallery", "Attire Associates",
                    "Clothing Connect", "Fashion Forward"
                ],
                "Trade Show": [
                    "India International Garment Fair", "Denim Expo Mumbai", "Fashion Connect Asia",
                    "Textile India", "India International Garment Fair", "Denim Expo Mumbai",
                    "Fashion Connect Asia", "Textile India", "India International Garment Fair", 
                    "Denim Expo Mumbai"
                ],
                "Orders": [5, 3, 2, 4, 3, 2, 2, 3, 2, 4],
                "Total Value (₹)": [
                    2250000, 1350000, 900000, 1800000, 1350000, 900000, 900000, 1350000, 900000, 1800000
                ],
                "Category Focus": [
                    "Jeans, Jackets", "Jeans", "Shirts, Jeans", "Full Range", "Jeans", 
                    "Jackets, Shirts", "Jeans", "Full Range", "Jeans, Shorts", "Jeans, Jackets"
                ],
                "Repeat Buyer": [
                    "Yes", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "Yes", "No"
                ]
            })
            
            # Show buyer data table
            st.dataframe(buyer_data, hide_index=True, use_container_width=True)
            
            # Create visualization of buyers by trade show
            buyers_by_show = buyer_data.groupby("Trade Show").agg({
                "Buyer": "count",
                "Orders": "sum",
                "Total Value (₹)": "sum"
            }).reset_index()
            
            buyers_by_show.rename(columns={"Buyer": "Unique Buyers"}, inplace=True)
            
            # Calculate average order value
            buyers_by_show["Avg. Order Value (₹)"] = buyers_by_show["Total Value (₹)"] / buyers_by_show["Orders"]
            
            # Create chart
            fig = px.bar(
                buyers_by_show,
                x="Trade Show",
                y="Unique Buyers",
                color="Orders",
                hover_data=["Total Value (₹)", "Avg. Order Value (₹)"],
                title="Buyer Distribution by Trade Show",
                color_continuous_scale="Viridis"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Category focus analysis
            st.subheader("Category Focus Analysis")
            
            # Extract categories from the Category Focus column
            categories = []
            for focus in buyer_data["Category Focus"]:
                for category in focus.split(", "):
                    categories.append(category)
            
            # Count frequency of each category
            category_counts = pd.Series(categories).value_counts().reset_index()
            category_counts.columns = ["Category", "Count"]
            
            # Create pie chart
            fig = px.pie(
                category_counts,
                values="Count",
                names="Category",
                title="Product Category Focus Distribution",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Repeat buyer analysis
            repeat_analysis = buyer_data["Repeat Buyer"].value_counts().reset_index()
            repeat_analysis.columns = ["Repeat Buyer", "Count"]
            
            # Create simple bar chart
            fig = px.bar(
                repeat_analysis,
                x="Repeat Buyer",
                y="Count",
                color="Repeat Buyer",
                title="Repeat vs New Buyers",
                color_discrete_map={"Yes": "green", "No": "blue"}
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_procurement_planner():
    """Display the procurement planner interface"""
    st.header("Procurement Planner")
    
    # Create tabs for different functions
    tab1, tab2, tab3 = st.tabs(["Material Planning", "Vendor Management", "Procurement Dashboard"])
    
    with tab1:
        st.subheader("Material Requirement Planning")
        
        # Order selection
        orders = [
            "TS-2024001-1001 (Fashion Retail Ltd)",
            "TS-2024002-1002 (Denim Connection)",
            "TS-2024003-1003 (Style Hub)",
            "TS-2024004-1004 (Apparel Group)",
            "TS-2024005-1005 (Textile Traders)",
            "All Orders"
        ]
        
        selected_order = st.selectbox("Select Order for Planning", orders)
        
        # Material categories
        material_categories = ["Fabric", "Trims", "Packaging", "All Categories"]
        selected_category = st.selectbox("Material Category", material_categories)
        
        # Sample material requirements
        material_req = pd.DataFrame({
            "Material": [
                "Denim Fabric (14oz)", "Denim Fabric (12oz)", "Denim Fabric (10oz)",
                "Buttons (Metal)", "Rivets", "Zipper (Metal)",
                "Leather Patch", "Poly Bags", "Cartons"
            ],
            "Category": [
                "Fabric", "Fabric", "Fabric",
                "Trims", "Trims", "Trims",
                "Trims", "Packaging", "Packaging"
            ],
            "Required Quantity": [
                12500, 15000, 8000,
                25000, 100000, 12000,
                12000, 12000, 1000
            ],
            "Unit": [
                "meters", "meters", "meters",
                "pcs", "pcs", "pcs",
                "pcs", "pcs", "pcs"
            ],
            "In Stock": [
                5000, 7000, 3000,
                10000, 50000, 5000,
                5000, 8000, 500
            ],
            "To Procure": [
                7500, 8000, 5000,
                15000, 50000, 7000,
                7000, 4000, 500
            ],
            "Estimated Cost (₹)": [
                3375000, 3200000, 1750000,
                225000, 250000, 140000,
                280000, 40000, 25000
            ],
            "Lead Time (days)": [
                30, 30, 30,
                15, 15, 20,
                20, 10, 10
            ],
            "Status": [
                "Partially Available", "Partially Available", "Partially Available",
                "Partially Available", "Partially Available", "Partially Available",
                "Partially Available", "Partially Available", "Partially Available"
            ]
        })
        
        # Filter by category if needed
        if selected_category != "All Categories":
            material_req = material_req[material_req["Category"] == selected_category]
        
        # Display material requirements
        st.dataframe(material_req, hide_index=True, use_container_width=True)
        
        # Material procurement summary
        total_to_procure = material_req["To Procure"].sum()
        total_cost = material_req["Estimated Cost (₹)"].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Materials to Procure", total_to_procure)
        
        with col2:
            st.metric("Total Estimated Cost", f"₹ {total_cost:,.0f}")
        
        with col3:
            st.metric("Average Lead Time", f"{material_req['Lead Time (days)'].mean():.1f} days")
        
        # Create procurement plan
        st.subheader("Procurement Timeline")
        
        # Create Gantt chart for procurement timeline
        material_req["Start Date"] = datetime.now()
        material_req["End Date"] = material_req.apply(
            lambda row: row["Start Date"] + timedelta(days=row["Lead Time (days)"]),
            axis=1
        )
        
        # Sort by end date
        material_req = material_req.sort_values("End Date")
        
        # Create figure
        fig = px.timeline(
            material_req,
            x_start="Start Date",
            x_end="End Date",
            y="Material",
            color="Category",
            hover_name="Material",
            hover_data=["Required Quantity", "To Procure", "Unit", "Estimated Cost (₹)"],
            title="Material Procurement Timeline"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Material",
            yaxis=dict(categoryorder="total ascending")
        )
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text="Today"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Create Purchase Requisitions"):
                st.success("Purchase requisitions created successfully!")
        
        with col2:
            if st.button("Download Procurement Plan"):
                st.info("Downloading procurement plan...")
        
        with col3:
            if st.button("Send for Approval"):
                st.info("Plan sent for approval")
    
    with tab2:
        st.subheader("Vendor Management")
        
        # Sample vendor data
        vendors = pd.DataFrame({
            "Vendor ID": ["V001", "V002", "V003", "V004", "V005", "V006"],
            "Vendor Name": [
                "Denim Mills Ltd", "Premium Fabrics", "Quality Textiles",
                "Garment Accessories", "Packaging Solutions", "Trims Manufacturing"
            ],
            "Category": [
                "Fabric", "Fabric", "Fabric",
                "Trims", "Packaging", "Trims"
            ],
            "Location": [
                "Mumbai", "Ahmedabad", "Surat",
                "Delhi", "Bangalore", "Tirupur"
            ],
            "Lead Time (days)": [30, 25, 35, 15, 10, 20],
            "Quality Rating": [4.5, 4.2, 4.0, 4.3, 3.8, 4.1],
            "Delivery Rating": [4.3, 4.0, 3.8, 4.4, 4.2, 3.9],
            "Price Rating": [3.8, 4.0, 4.2, 4.1, 4.3, 4.0],
            "Status": [
                "Approved", "Approved", "Approved",
                "Approved", "Approved", "Under Review"
            ]
        })
        
        # Vendor filter
        vendor_categories = ["All Categories"] + list(vendors["Category"].unique())
        selected_vendor_category = st.selectbox("Filter by Category", vendor_categories)
        
        # Apply filter
        filtered_vendors = vendors
        if selected_vendor_category != "All Categories":
            filtered_vendors = vendors[vendors["Category"] == selected_vendor_category]
        
        # Display vendor data
        st.dataframe(filtered_vendors, hide_index=True, use_container_width=True)
        
        # Vendor performance visualization
        st.subheader("Vendor Performance Comparison")
        
        # Create radar chart for vendor comparison
        selected_vendors = st.multiselect(
            "Select Vendors to Compare",
            vendors["Vendor Name"],
            default=vendors["Vendor Name"].iloc[0:3]
        )
        
        if selected_vendors:
            # Filter vendors
            vendor_comp = vendors[vendors["Vendor Name"].isin(selected_vendors)]
            
            # Create radar chart
            fig = go.Figure()
            
            categories = ["Quality Rating", "Delivery Rating", "Price Rating", "5 - Lead Time (days)/10"]
            
            for i, vendor in enumerate(vendor_comp["Vendor Name"]):
                row = vendor_comp[vendor_comp["Vendor Name"] == vendor].iloc[0]
                
                # Create normalized data (lead time is inverted and normalized)
                values = [
                    row["Quality Rating"],
                    row["Delivery Rating"],
                    row["Price Rating"],
                    5 - min(row["Lead Time (days)"] / 10, 5)  # Invert and normalize lead time
                ]
                
                # Close the loop by repeating first value
                values.append(values[0])
                categories_with_first = categories + [categories[0]]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories_with_first,
                    fill='toself',
                    name=vendor
                ))
            
            fig.update_layout(
                title="Vendor Performance Comparison",
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Vendor management actions
        st.subheader("Vendor Management Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Add New Vendor")
            
            new_vendor_name = st.text_input("Vendor Name")
            new_vendor_category = st.selectbox("Category", ["Fabric", "Trims", "Packaging", "Other"])
            new_vendor_location = st.text_input("Location")
            new_vendor_lead_time = st.number_input("Lead Time (days)", min_value=1, max_value=60, value=30)
            
            if st.button("Add Vendor"):
                if new_vendor_name and new_vendor_location:
                    st.success(f"Vendor '{new_vendor_name}' added successfully!")
                else:
                    st.error("Please fill in all required fields")
        
        with col2:
            st.markdown("### Vendor Evaluation")
            
            eval_vendor = st.selectbox("Select Vendor for Evaluation", vendors["Vendor Name"])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                quality_rating = st.slider("Quality Rating", 1.0, 5.0, 4.0, 0.1)
            
            with col2:
                delivery_rating = st.slider("Delivery Rating", 1.0, 5.0, 4.0, 0.1)
            
            with col3:
                price_rating = st.slider("Price Rating", 1.0, 5.0, 4.0, 0.1)
            
            evaluation_notes = st.text_area("Evaluation Notes")
            
            if st.button("Submit Evaluation"):
                st.success(f"Evaluation for '{eval_vendor}' submitted successfully!")
    
    with tab3:
        st.subheader("Procurement Dashboard")
        
        # Sample procurement data
        procurement_summary = {
            "Total Orders": 58,
            "Pending Orders": 15,
            "Completed Orders": 43,
            "Total Value (₹)": 52500000,
            "Average Lead Time (days)": 22
        }
        
        # Create metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Orders", procurement_summary["Total Orders"])
        
        with col2:
            st.metric("Pending Orders", procurement_summary["Pending Orders"])
        
        with col3:
            st.metric("Completed Orders", procurement_summary["Completed Orders"])
        
        with col4:
            st.metric("Total Value", f"₹ {procurement_summary['Total Value (₹)'] / 10000000:.1f} Cr")
        
        with col5:
            st.metric("Avg. Lead Time", f"{procurement_summary['Average Lead Time (days)']} days")
        
        # Procurement trends
        st.subheader("Procurement Trends")
        
        # Sample monthly data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        procurement_trends = pd.DataFrame({
            "Month": months,
            "Orders": [8, 10, 12, 9, 11, 8],
            "Value (₹)": [7200000, 9000000, 10800000, 8100000, 9900000, 7500000]
        })
        
        # Create line chart
        fig = go.Figure()
        
        # Add orders line
        fig.add_trace(go.Scatter(
            x=procurement_trends["Month"],
            y=procurement_trends["Orders"],
            name="Orders",
            mode="lines+markers",
            marker=dict(size=8)
        ))
        
        # Add value line (secondary axis)
        fig.add_trace(go.Scatter(
            x=procurement_trends["Month"],
            y=procurement_trends["Value (₹)"] / 1000000,  # Convert to millions
            name="Value (₹M)",
            mode="lines+markers",
            marker=dict(size=8),
            yaxis="y2"
        ))
        
        # Update layout
        fig.update_layout(
            title="Monthly Procurement Trends",
            xaxis_title="Month",
            yaxis_title="Orders",
            yaxis2=dict(
                title="Value (₹M)",
                overlaying="y",
                side="right"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Category-wise procurement
        st.subheader("Category-wise Procurement")
        
        # Sample category data
        category_data = pd.DataFrame({
            "Category": ["Fabric", "Trims", "Packaging"],
            "Value (₹)": [36750000, 12600000, 3150000],
            "Orders": [20, 25, 13]
        })
        
        # Calculate percentages
        total_value = category_data["Value (₹)"].sum()
        category_data["Percentage"] = (category_data["Value (₹)"] / total_value * 100).round(1)
        
        # Create pie chart
        fig = px.pie(
            category_data,
            values="Value (₹)",
            names="Category",
            hover_data=["Orders", "Percentage"],
            title="Procurement Value by Category",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top vendors by procurement value
        st.subheader("Top Vendors by Procurement Value")
        
        # Sample vendor data
        top_vendors = pd.DataFrame({
            "Vendor": [
                "Denim Mills Ltd", "Premium Fabrics", "Quality Textiles", 
                "Garment Accessories", "Packaging Solutions"
            ],
            "Category": ["Fabric", "Fabric", "Fabric", "Trims", "Packaging"],
            "Value (₹)": [18900000, 12600000, 5250000, 9450000, 3150000],
            "Orders": [12, 10, 8, 15, 13]
        })
        
        # Create horizontal bar chart
        fig = px.bar(
            top_vendors.sort_values("Value (₹)", ascending=True),
            y="Vendor",
            x="Value (₹)",
            color="Category",
            orientation="h",
            title="Top Vendors by Procurement Value",
            hover_data=["Orders"]
        )
        
        # Add order counts as text
        fig.update_traces(
            text=top_vendors.sort_values("Value (₹)", ascending=True)["Orders"],
            textposition="inside"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Procurement Value (₹)",
            yaxis_title="Vendor",
            xaxis=dict(tickformat=",.0f")
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_sample_management():
    """Display the sample management interface"""
    st.header("Sample Management")
    
    # Create tabs for different functions
    tab1, tab2, tab3 = st.tabs(["Sample Request", "Sample Tracking", "Approval Workflow"])
    
    with tab1:
        st.subheader("Create Sample Request")
        
        # Form for sample request
        col1, col2 = st.columns(2)
        
        with col1:
            request_for = st.selectbox(
                "Request For",
                ["Trade Show", "Buyer", "Internal Development"]
            )
            
            if request_for == "Trade Show":
                trade_shows = [
                    "India International Garment Fair (Jun 2024)",
                    "Denim Expo Mumbai (Jul 2024)",
                    "Fashion Connect Asia (Aug 2024)",
                    "Textile India (Sep 2024)",
                    "Other (Specify)"
                ]
                trade_show = st.selectbox("Select Trade Show", trade_shows)
            
            if request_for == "Buyer":
                buyers = [
                    "Fashion Retail Ltd",
                    "Denim Connection",
                    "Style Hub",
                    "Apparel Group",
                    "Textile Traders",
                    "Other (Specify)"
                ]
                buyer = st.selectbox("Select Buyer", buyers)
            
            requestor = st.text_input("Requestor Name")
            department = st.selectbox(
                "Department",
                ["Design", "Sales", "Merchandising", "Production", "QA"]
            )
        
        with col2:
            request_date = st.date_input("Request Date", datetime.now())
            required_date = st.date_input("Required By Date", datetime.now() + timedelta(days=14))
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            sample_type = st.selectbox(
                "Sample Type",
                ["Proto Sample", "Fit Sample", "Size Set", "Photo Sample", "Production Sample", "Sales Sample"]
            )
        
        # Style details
        st.subheader("Style Details")
        
        # Initialize session state for samples if not exists
        if "sample_styles" not in st.session_state:
            st.session_state.sample_styles = [{
                "id": str(uuid.uuid4()),
                "style_number": "",
                "description": "",
                "category": "Jeans",
                "color": "",
                "sizes": [],
                "quantity": 1,
                "reference_image": None,
                "special_instructions": ""
            }]
        
        # Categories
        categories = ["Jeans", "Jacket", "Shirt", "T-Shirt", "Shorts", "Skirt", "Dress", "Other"]
        
        # Size options
        size_options = ["XS", "S", "M", "L", "XL", "XXL", "28", "30", "32", "34", "36", "38", "40", "42"]
        
        for i, style in enumerate(st.session_state.sample_styles):
            st.markdown(f"### Sample {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                style["style_number"] = st.text_input(
                    "Style Number",
                    style["style_number"],
                    key=f"sample_style_num_{style['id']}"
                )
                style["description"] = st.text_area(
                    "Description",
                    style["description"],
                    key=f"sample_desc_{style['id']}",
                    height=100
                )
                style["category"] = st.selectbox(
                    "Category",
                    categories,
                    categories.index(style["category"]) if style["category"] in categories else 0,
                    key=f"sample_cat_{style['id']}"
                )
            
            with col2:
                style["color"] = st.text_input(
                    "Color",
                    style["color"],
                    key=f"sample_color_{style['id']}"
                )
                style["sizes"] = st.multiselect(
                    "Sizes",
                    size_options,
                    style["sizes"],
                    key=f"sample_sizes_{style['id']}"
                )
                style["quantity"] = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=style["quantity"],
                    key=f"sample_qty_{style['id']}"
                )
            
            style["special_instructions"] = st.text_area(
                "Special Instructions",
                style["special_instructions"],
                key=f"sample_instr_{style['id']}"
            )
            
            # Reference image upload
            style["reference_image"] = st.file_uploader(
                "Upload Reference Image",
                type=["jpg", "jpeg", "png"],
                key=f"sample_img_{style['id']}"
            )
            
            if style["reference_image"]:
                st.image(style["reference_image"], width=300)
            
            # Delete button for this style (except first one)
            if i > 0:
                if st.button("Remove Sample", key=f"remove_sample_{style['id']}"):
                    st.session_state.sample_styles.pop(i)
                    st.rerun()
            
            st.markdown("---")
        
        # Add another sample button
        if st.button("Add Another Sample"):
            st.session_state.sample_styles.append({
                "id": str(uuid.uuid4()),
                "style_number": "",
                "description": "",
                "category": "Jeans",
                "color": "",
                "sizes": [],
                "quantity": 1,
                "reference_image": None,
                "special_instructions": ""
            })
            st.rerun()
        
        # Cost and timeline information
        st.subheader("Cost & Timeline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            estimated_cost = st.number_input("Estimated Cost per Sample (₹)", min_value=0, value=5000)
            total_cost = sum(style["quantity"] for style in st.session_state.sample_styles) * estimated_cost
            st.info(f"Total Estimated Cost: ₹ {total_cost:,.0f}")
        
        with col2:
            approval_needed = st.checkbox("Requires Approval")
            approvers = st.multiselect(
                "Approvers",
                ["Design Head", "Merchandising Head", "Sales Head", "Production Head"],
                disabled=not approval_needed
            )
        
        # Submit request
        if st.button("Submit Sample Request"):
            if requestor and st.session_state.sample_styles[0]["style_number"]:
                # Generate sample request ID
                sample_req_id = f"SR-{datetime.now().strftime('%Y%m%d')}-{np.random.randint(1000, 9999)}"
                st.success(f"Sample request submitted successfully! Request ID: {sample_req_id}")
            else:
                st.error("Please fill in all required fields")
    
    with tab2:
        st.subheader("Sample Tracking & Status")
        
        # Sample requests
        sample_requests = pd.DataFrame({
            "Request ID": [f"SR-20240{i}-{1000+i}" for i in range(1, 11)],
            "Requested By": [
                "John Smith", "Mary Johnson", "David Lee", "Sarah Williams",
                "Michael Brown", "Jennifer Davis", "Robert Miller", "Elizabeth Wilson",
                "James Moore", "Patricia Taylor"
            ],
            "Department": [
                "Design", "Sales", "Merchandising", "Design",
                "Production", "Sales", "Design", "Merchandising",
                "QA", "Sales"
            ],
            "Request Date": [
                "2024-01-15", "2024-01-22", "2024-02-05", "2024-02-12", "2024-02-18",
                "2024-02-25", "2024-03-03", "2024-03-10", "2024-03-15", "2024-03-22"
            ],
            "Required Date": [
                "2024-01-29", "2024-02-05", "2024-02-19", "2024-02-26", "2024-03-03",
                "2024-03-10", "2024-03-17", "2024-03-24", "2024-03-29", "2024-04-05"
            ],
            "Samples": [3, 2, 1, 4, 2, 3, 2, 1, 3, 2],
            "Status": [
                "Completed", "Completed", "Completed", "In Development", "In Development",
                "Pattern Making", "Fabric Sourcing", "Pending Approval", "Pending", "Pending"
            ],
            "Priority": [
                "High", "Medium", "Low", "High", "Medium",
                "Medium", "Low", "High", "Medium", "Low"
            ]
        })
        
        # Status filter
        status_options = ["All"] + list(sample_requests["Status"].unique())
        selected_status = st.selectbox("Filter by Status", status_options)
        
        # Priority filter
        priority_options = ["All"] + list(sample_requests["Priority"].unique())
        selected_priority = st.selectbox("Filter by Priority", priority_options)
        
        # Department filter
        department_options = ["All"] + list(sample_requests["Department"].unique())
        selected_department = st.selectbox("Filter by Department", department_options)
        
        # Apply filters
        filtered_samples = sample_requests
        
        if selected_status != "All":
            filtered_samples = filtered_samples[filtered_samples["Status"] == selected_status]
        
        if selected_priority != "All":
            filtered_samples = filtered_samples[filtered_samples["Priority"] == selected_priority]
        
        if selected_department != "All":
            filtered_samples = filtered_samples[filtered_samples["Department"] == selected_department]
        
        # Convert columns to appropriate dtypes
        filtered_samples["Request Date"] = pd.to_datetime(filtered_samples["Request Date"])
        filtered_samples["Required Date"] = pd.to_datetime(filtered_samples["Required Date"])
        
        # Calculate days to delivery
        filtered_samples["Days to Required"] = (filtered_samples["Required Date"] - datetime.now()).dt.days
        
        # Format for display
        display_samples = filtered_samples.copy()
        display_samples["Request Date"] = display_samples["Request Date"].dt.strftime("%d-%b-%Y")
        display_samples["Required Date"] = display_samples["Required Date"].dt.strftime("%d-%b-%Y")
        
        # Display table
        st.dataframe(
            display_samples,
            column_config={
                "Days to Required": st.column_config.NumberColumn(
                    "Days to Required",
                    help="Days remaining until required date",
                    format="%d days",
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Sample status",
                    width="medium",
                    options=[
                        "Pending", "Pending Approval", "Fabric Sourcing", "Pattern Making",
                        "In Development", "Quality Check", "Completed", "Rejected"
                    ],
                ),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority",
                    help="Priority level",
                    width="small",
                    options=["High", "Medium", "Low"],
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Sample details
        st.subheader("Sample Details")
        selected_sample = st.selectbox("Select Request ID", sample_requests["Request ID"])
        
        # Sample row
        selected_row = sample_requests[sample_requests["Request ID"] == selected_sample].iloc[0]
        
        # Display sample header
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Requested By:** {selected_row['Requested By']}")
            st.markdown(f"**Department:** {selected_row['Department']}")
            st.markdown(f"**Priority:** {selected_row['Priority']}")
        
        with col2:
            st.markdown(f"**Request Date:** {pd.to_datetime(selected_row['Request Date']).strftime('%d-%b-%Y')}")
            st.markdown(f"**Required Date:** {pd.to_datetime(selected_row['Required Date']).strftime('%d-%b-%Y')}")
            days_remaining = (pd.to_datetime(selected_row['Required Date']) - datetime.now()).days
            st.markdown(f"**Days Remaining:** {days_remaining}")
        
        with col3:
            st.markdown(f"**Status:** {selected_row['Status']}")
            st.markdown(f"**Total Samples:** {selected_row['Samples']}")
            st.markdown(f"**Request Type:** {'Trade Show' if np.random.random() > 0.5 else 'Buyer'}")
        
        # Sample breakdown
        sample_details = []
        np.random.seed(int(selected_sample[-4:]))  # Use sample number as seed for consistent random data
        
        for i in range(selected_row["Samples"]):
            sample_name = f"S-{selected_sample[-4:]}-{101+i}"
            
            sample_details.append({
                "Sample ID": sample_name,
                "Style Number": f"STY-{selected_sample[-4:]}-{101+i}",
                "Description": np.random.choice([
                    "Skinny Fit Denim Jeans", "Relaxed Fit Jeans", "Slim Straight Jeans",
                    "Denim Jacket", "Denim Shirt", "Cargo Pants", "Denim Shorts"
                ]),
                "Category": np.random.choice(["Jeans", "Jacket", "Shirt", "Shorts"]),
                "Color": np.random.choice(["Blue", "Black", "Grey", "Indigo", "White"]),
                "Size": np.random.choice(["S", "M", "L", "XL", "XXL", "32", "34", "36"]),
                "Status": selected_row["Status"] if np.random.random() > 0.3 else np.random.choice([
                    "Pending", "Fabric Sourcing", "Pattern Making", "In Development", "Completed"
                ])
            })
        
        samples_df = pd.DataFrame(sample_details)
        
        # Show samples
        st.markdown("#### Sample Breakdown")
        st.dataframe(samples_df, hide_index=True, use_container_width=True)
        
        # Sample progress tracking
        st.subheader("Sample Progress")
        
        # Create sample stages
        stages = [
            "Request Created", "Approved", "Fabric Sourcing", 
            "Pattern Making", "Cutting", "Stitching", 
            "Finishing", "Quality Check", "Completed"
        ]
        
        # Determine current stage based on status
        current_stage_map = {
            "Pending": 0,
            "Pending Approval": 0,
            "Fabric Sourcing": 2,
            "Pattern Making": 3,
            "In Development": 5,
            "Quality Check": 7,
            "Completed": 8
        }
        
        current_stage = current_stage_map.get(selected_row["Status"], 0)
        
        # Create progress visualization
        progress_values = [
            1 if i <= current_stage else 0.2 for i in range(len(stages))
        ]
        
        fig = go.Figure()
        
        # Add progress bars
        fig.add_trace(go.Bar(
            x=progress_values,
            y=stages,
            orientation='h',
            marker=dict(
                color=['green' if i <= current_stage else 'lightgrey' for i in range(len(stages))],
                line=dict(color='rgba(0,0,0,0)', width=0)
            ),
            width=0.6,
            text=stages,
            textposition='auto'
        ))
        
        # Add current stage marker
        if current_stage < len(stages):
            fig.add_trace(go.Scatter(
                x=[progress_values[current_stage]],
                y=[stages[current_stage]],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=16,
                    color='gold',
                    line=dict(color='black', width=1)
                ),
                name='Current Stage'
            ))
        
        # Update layout
        fig.update_layout(
            title="Sample Development Progress",
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                range=[0, 1.1]
            ),
            yaxis=dict(
                categoryorder='array',
                categoryarray=stages[::-1]  # Reverse order to show progress from bottom to top
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Update status
        st.subheader("Update Sample Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_status = st.selectbox(
                "New Status",
                [
                    "Pending", "Pending Approval", "Fabric Sourcing", "Pattern Making",
                    "In Development", "Quality Check", "Completed", "Rejected"
                ],
                stages.index(stages[current_stage]) if current_stage < len(stages) else 0
            )
        
        with col2:
            comments = st.text_area("Comments")
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Status"):
                st.success(f"Status updated to {new_status}")
    
    with tab3:
        st.subheader("Sample Approval Workflow")
        
        # Approval queue
        approval_queue = pd.DataFrame({
            "Sample ID": ["S-1001-101", "S-1003-102", "S-1005-101", "S-1008-103", "S-1009-102"],
            "Style Number": ["STY-1001-101", "STY-1003-102", "STY-1005-101", "STY-1008-103", "STY-1009-102"],
            "Description": [
                "Skinny Fit Denim Jeans", "Slim Straight Jeans", "Denim Jacket",
                "Cargo Pants", "Denim Shorts"
            ],
            "Requested By": ["John Smith", "David Lee", "Michael Brown", "Elizabeth Wilson", "James Moore"],
            "Department": ["Design", "Merchandising", "Production", "Merchandising", "QA"],
            "Pending Approval From": ["Design Head", "Merchandising Head", "Sales Head", "Merchandising Head", "QA Head"],
            "Days Pending": [2, 1, 3, 1, 0]
        })
        
        st.markdown("### Samples Pending Approval")
        st.dataframe(approval_queue, hide_index=True, use_container_width=True)
        
        # Sample approval details
        st.subheader("Sample Approval Details")
        
        selected_approval = st.selectbox("Select Sample for Approval", approval_queue["Sample ID"])
        
        # Sample information
        selected_approval_row = approval_queue[approval_queue["Sample ID"] == selected_approval].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Sample ID:** {selected_approval_row['Sample ID']}")
            st.markdown(f"**Style Number:** {selected_approval_row['Style Number']}")
            st.markdown(f"**Description:** {selected_approval_row['Description']}")
            st.markdown(f"**Requested By:** {selected_approval_row['Requested By']}")
        
        with col2:
            st.markdown(f"**Department:** {selected_approval_row['Department']}")
            st.markdown(f"**Pending Approval From:** {selected_approval_row['Pending Approval From']}")
            st.markdown(f"**Days Pending:** {selected_approval_row['Days Pending']}")
        
        # Sample image (placeholder)
        st.markdown("### Sample Images")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Front View**")
            st.image("https://via.placeholder.com/300x400?text=Front+View", use_column_width=True)
        
        with col2:
            st.markdown("**Back View**")
            st.image("https://via.placeholder.com/300x400?text=Back+View", use_column_width=True)
        
        with col3:
            st.markdown("**Detail View**")
            st.image("https://via.placeholder.com/300x400?text=Detail+View", use_column_width=True)
        
        # Approval form
        st.subheader("Approval Decision")
        
        approval_decision = st.radio(
            "Decision",
            ["Approve", "Approve with Changes", "Reject"]
        )
        
        comments = st.text_area("Comments/Feedback")
        
        if approval_decision == "Approve with Changes":
            changes_required = st.text_area("Changes Required")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Decision"):
                st.success(f"Sample {selected_approval} {approval_decision.lower()}ed successfully!")
        
        with col2:
            if st.button("Reassign"):
                reassign_to = st.selectbox(
                    "Reassign to",
                    ["Design Head", "Merchandising Head", "Sales Head", "Production Head", "QA Head"]
                )
                if st.button("Confirm Reassignment"):
                    st.info(f"Sample {selected_approval} reassigned to {reassign_to}")
        
        # Approval history
        st.subheader("Approval History")
        
        approval_history = pd.DataFrame({
            "Date": ["2024-03-15", "2024-03-14", "2024-03-13"],
            "Approver": ["Jane Wilson (Design)", "Mark Davis (Production)", "Sarah Lee (Merchandising)"],
            "Decision": ["Approve with Changes", "Approve", "Approve with Changes"],
            "Comments": [
                "Pocket placement needs adjustment. Wash should be slightly darker.",
                "Construction looks good. Approve for next stage.",
                "Please adjust the fit around the waist by 0.5 inch."
            ]
        })
        
        st.dataframe(approval_history, hide_index=True, use_container_width=True)

def show_timeline_calendar():
    """Display the timeline and calendar view for trade shows and orders"""
    st.header("Timeline & Calendar")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Trade Show Calendar", "Order Timeline"])
    
    with tab1:
        st.subheader("Trade Show Calendar")
        
        # Sample trade show data
        trade_shows = pd.DataFrame({
            "Show Name": [
                "India International Garment Fair", 
                "Denim Expo Mumbai", 
                "Fashion Connect Asia", 
                "Textile India",
                "Garment Technology Expo",
                "India Fashion Forum",
                "Fashion & Lifestyle Exhibition",
                "Apparel Sourcing Week"
            ],
            "Location": [
                "New Delhi", 
                "Mumbai", 
                "Bangalore", 
                "Ahmedabad",
                "Greater Noida",
                "Mumbai",
                "Chennai",
                "Bangalore"
            ],
            "Start Date": [
                "2024-06-15", 
                "2024-07-22", 
                "2024-08-10", 
                "2024-09-05",
                "2024-05-10",
                "2024-06-05",
                "2024-07-15",
                "2024-08-20"
            ],
            "End Date": [
                "2024-06-18", 
                "2024-07-25", 
                "2024-08-13", 
                "2024-09-08",
                "2024-05-13",
                "2024-06-07",
                "2024-07-18",
                "2024-08-22"
            ],
            "Status": [
                "Confirmed", 
                "Planning", 
                "Confirmed", 
                "Planning",
                "Confirmed",
                "Confirmed",
                "Planning",
                "Planning"
            ],
            "Booth": [
                "A-12", 
                "TBD", 
                "C-45", 
                "TBD",
                "B-32",
                "F-08",
                "TBD",
                "TBD"
            ],
            "Team": [
                "Sales + Design", 
                "Sales", 
                "Sales + Production", 
                "Sales + Merchandising",
                "Production + Design",
                "Sales + Marketing",
                "Sales",
                "Sales + Design"
            ]
        })
        
        # Convert dates to datetime
        trade_shows["Start Date"] = pd.to_datetime(trade_shows["Start Date"])
        trade_shows["End Date"] = pd.to_datetime(trade_shows["End Date"])
        
        # Calculate duration
        trade_shows["Duration"] = (trade_shows["End Date"] - trade_shows["Start Date"]).dt.days + 1
        
        # Gantt chart for trade shows
        fig = px.timeline(
            trade_shows, 
            x_start="Start Date", 
            x_end="End Date", 
            y="Show Name",
            color="Status",
            hover_name="Show Name",
            hover_data=["Location", "Booth", "Team", "Duration"],
            title="Trade Show Schedule"
        )
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text="Today"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Trade Show",
            yaxis=dict(categoryorder="total ascending")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Month filter
        months = ["All"] + list(trade_shows["Start Date"].dt.strftime("%B %Y").unique())
        selected_month = st.selectbox("Filter by Month", months)
        
        # Status filter
        statuses = ["All"] + list(trade_shows["Status"].unique())
        selected_status = st.selectbox("Filter by Status", statuses)
        
        # Apply filters
        filtered_shows = trade_shows
        
        if selected_month != "All":
            filtered_shows = filtered_shows[filtered_shows["Start Date"].dt.strftime("%B %Y") == selected_month]
        
        if selected_status != "All":
            filtered_shows = filtered_shows[filtered_shows["Status"] == selected_status]
        
        # Format for display
        display_shows = filtered_shows.copy()
        display_shows["Start Date"] = display_shows["Start Date"].dt.strftime("%d-%b-%Y")
        display_shows["End Date"] = display_shows["End Date"].dt.strftime("%d-%b-%Y")
        
        # Display filtered trade shows
        st.dataframe(display_shows, hide_index=True, use_container_width=True)
        
        # Trade show details
        st.subheader("Trade Show Details")
        
        selected_show = st.selectbox("Select Trade Show", trade_shows["Show Name"])
        show_row = trade_shows[trade_shows["Show Name"] == selected_show].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Location:** {show_row['Location']}")
            st.markdown(f"**Dates:** {show_row['Start Date'].strftime('%d-%b-%Y')} to {show_row['End Date'].strftime('%d-%b-%Y')}")
            st.markdown(f"**Duration:** {show_row['Duration']} days")
        
        with col2:
            st.markdown(f"**Status:** {show_row['Status']}")
            st.markdown(f"**Booth:** {show_row['Booth']}")
            st.markdown(f"**Team:** {show_row['Team']}")
        
        with col3:
            days_to_show = (show_row["Start Date"] - datetime.now()).days
            if days_to_show > 0:
                st.markdown(f"**Days to Show:** {days_to_show}")
            else:
                st.markdown("**Show has passed or is ongoing**")
        
        # Pre-show tasks
        if show_row["Status"] == "Confirmed":
            st.subheader("Pre-Show Tasks")
            
            tasks = pd.DataFrame({
                "Task": [
                    "Sample Development",
                    "Marketing Material Preparation",
                    "Team Briefing",
                    "Logistics Arrangement",
                    "Booth Design Finalization"
                ],
                "Assignee": [
                    "Design Team",
                    "Marketing Team",
                    "Sales Head",
                    "Admin Team",
                    "Design Team"
                ],
                "Status": [
                    "In Progress",
                    "Completed",
                    "Pending",
                    "In Progress",
                    "Completed"
                ],
                "Due Date": [
                    (show_row["Start Date"] - timedelta(days=14)).strftime("%d-%b-%Y"),
                    (show_row["Start Date"] - timedelta(days=21)).strftime("%d-%b-%Y"),
                    (show_row["Start Date"] - timedelta(days=7)).strftime("%d-%b-%Y"),
                    (show_row["Start Date"] - timedelta(days=10)).strftime("%d-%b-%Y"),
                    (show_row["Start Date"] - timedelta(days=30)).strftime("%d-%b-%Y")
                ]
            })
            
            st.dataframe(tasks, hide_index=True, use_container_width=True)
        
        # Add new trade show
        st.subheader("Add New Trade Show")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_show_name = st.text_input("Trade Show Name")
            new_show_location = st.text_input("Location")
            new_show_status = st.selectbox("Status", ["Planning", "Confirmed", "Cancelled"])
        
        with col2:
            new_show_start = st.date_input("Start Date", datetime.now() + timedelta(days=30))
            new_show_end = st.date_input("End Date", datetime.now() + timedelta(days=33))
            new_show_booth = st.text_input("Booth Number (if known)")
        
        new_show_team = st.multiselect(
            "Team Members",
            ["Sales", "Design", "Production", "Merchandising", "Marketing"]
        )
        
        if st.button("Add Trade Show"):
            if new_show_name and new_show_location:
                st.success(f"Trade show '{new_show_name}' added successfully!")
            else:
                st.error("Please fill in all required fields")
    
    with tab2:
        st.subheader("Order Timeline")
        
        # Sample order data
        orders = pd.DataFrame({
            "Order ID": [f"TS-20240{i}-{1000+i}" for i in range(1, 11)],
            "Buyer": [
                "Fashion Retail Ltd", "Denim Connection", "Style Hub", "Apparel Group",
                "Textile Traders", "Fashion Avenue", "Garment Gallery", "Attire Associates",
                "Clothing Connect", "Fashion Forward"
            ],
            "Order Date": [
                "2024-01-15", "2024-01-22", "2024-02-05", "2024-02-12", "2024-02-18",
                "2024-02-25", "2024-03-03", "2024-03-10", "2024-03-15", "2024-03-22"
            ],
            "Start Production": [
                "2024-01-25", "2024-02-01", "2024-02-15", "2024-02-22", "2024-02-28",
                "2024-03-07", "2024-03-13", "2024-03-20", "2024-03-25", "2024-04-01"
            ],
            "Delivery Date": [
                "2024-04-15", "2024-04-22", "2024-05-05", "2024-05-12", "2024-05-18",
                "2024-05-25", "2024-06-03", "2024-06-10", "2024-06-15", "2024-06-22"
            ],
            "Status": [
                "Completed", "Completed", "In Production", "In Production", "In Production",
                "Approved", "Approved", "Pending Approval", "Draft", "Draft"
            ],
            "Total Qty": [1500, 2500, 800, 1800, 500, 1200, 700, 3000, 1100, 2000]
        })
        
        # Convert dates to datetime
        orders["Order Date"] = pd.to_datetime(orders["Order Date"])
        orders["Start Production"] = pd.to_datetime(orders["Start Production"])
        orders["Delivery Date"] = pd.to_datetime(orders["Delivery Date"])
        
        # Calculate production duration
        orders["Production Days"] = (orders["Delivery Date"] - orders["Start Production"]).dt.days
        
        # Create timeline
        fig = px.timeline(
            orders, 
            x_start="Start Production", 
            x_end="Delivery Date", 
            y="Order ID",
            color="Status",
            hover_name="Buyer",
            hover_data=["Total Qty", "Production Days", "Order Date"],
            title="Production Timeline by Order"
        )
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text="Today"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Order ID",
            yaxis=dict(categoryorder="total ascending")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Status filter
        order_statuses = ["All"] + list(orders["Status"].unique())
        selected_order_status = st.selectbox("Filter by Order Status", order_statuses)
        
        # Time filter
        time_filters = ["All", "Current Month", "Next Month", "Past Orders", "Future Orders"]
        selected_time = st.selectbox("Filter by Time Period", time_filters)
        
        # Apply filters
        filtered_orders = orders
        
        if selected_order_status != "All":
            filtered_orders = filtered_orders[filtered_orders["Status"] == selected_order_status]
        
        now = datetime.now()
        current_month_start = datetime(now.year, now.month, 1)
        next_month_start = datetime(now.year, now.month + 1 if now.month < 12 else 1, 1)
        next_month_end = datetime(now.year, now.month + 2 if now.month < 11 else (1 if now.month == 12 else 2), 1)
        
        if selected_time == "Current Month":
            next_month = current_month_start.replace(month=current_month_start.month + 1) if current_month_start.month < 12 else current_month_start.replace(year=current_month_start.year + 1, month=1)
            filtered_orders = filtered_orders[(filtered_orders["Delivery Date"] >= current_month_start) & 
                                            (filtered_orders["Delivery Date"] < next_month)]
        elif selected_time == "Next Month":
            filtered_orders = filtered_orders[(filtered_orders["Delivery Date"] >= next_month_start) & 
                                            (filtered_orders["Delivery Date"] < next_month_end)]
        elif selected_time == "Past Orders":
            filtered_orders = filtered_orders[filtered_orders["Delivery Date"] < now]
        elif selected_time == "Future Orders":
            filtered_orders = filtered_orders[filtered_orders["Delivery Date"] >= now]
        
        # Format for display
        display_orders = filtered_orders.copy()
        display_orders["Order Date"] = display_orders["Order Date"].dt.strftime("%d-%b-%Y")
        display_orders["Start Production"] = display_orders["Start Production"].dt.strftime("%d-%b-%Y")
        display_orders["Delivery Date"] = display_orders["Delivery Date"].dt.strftime("%d-%b-%Y")
        
        # Display filtered orders
        st.dataframe(display_orders, hide_index=True, use_container_width=True)
        
        # Order details
        st.subheader("Order Details & Timeline")
        
        selected_order = st.selectbox("Select Order", orders["Order ID"])
        order_row = orders[orders["Order ID"] == selected_order].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Buyer:** {order_row['Buyer']}")
            st.markdown(f"**Order Date:** {order_row['Order Date'].strftime('%d-%b-%Y')}")
            st.markdown(f"**Status:** {order_row['Status']}")
        
        with col2:
            st.markdown(f"**Production Start:** {order_row['Start Production'].strftime('%d-%b-%Y')}")
            st.markdown(f"**Delivery Date:** {order_row['Delivery Date'].strftime('%d-%b-%Y')}")
            st.markdown(f"**Production Days:** {order_row['Production Days']}")
        
        with col3:
            st.markdown(f"**Total Quantity:** {order_row['Total Qty']}")
            
            days_to_delivery = (order_row["Delivery Date"] - datetime.now()).days
            if days_to_delivery > 0:
                st.markdown(f"**Days to Delivery:** {days_to_delivery}")
            else:
                st.markdown("**Delivery date has passed**")
        
        # Detailed timeline with milestones
        st.subheader("Order Milestones")
        
        # Create milestone data
        order_date = order_row["Order Date"]
        start_production = order_row["Start Production"]
        delivery_date = order_row["Delivery Date"]
        
        # Calculate milestone dates
        approval_date = order_date + timedelta(days=5)
        fabric_receipt = start_production - timedelta(days=3)
        cutting_start = start_production
        stitching_start = start_production + timedelta(days=int(order_row["Production Days"] * 0.2))
        finishing_start = start_production + timedelta(days=int(order_row["Production Days"] * 0.6))
        qa_start = start_production + timedelta(days=int(order_row["Production Days"] * 0.8))
        packing_start = qa_start + timedelta(days=3)
        
        milestones = pd.DataFrame({
            "Milestone": [
                "Order Placed", "Order Approved", "Fabric Receipt", 
                "Cutting Start", "Stitching Start", "Finishing Start",
                "Quality Audit", "Packing & Dispatch", "Delivery"
            ],
            "Planned Date": [
                order_date, approval_date, fabric_receipt,
                cutting_start, stitching_start, finishing_start,
                qa_start, packing_start, delivery_date
            ],
            "Status": [
                "Completed", "Completed", "Completed" if fabric_receipt < datetime.now() else "Pending",
                "Completed" if cutting_start < datetime.now() else "Pending",
                "In Progress" if stitching_start < datetime.now() and finishing_start > datetime.now() else 
                ("Completed" if stitching_start < datetime.now() else "Pending"),
                "In Progress" if finishing_start < datetime.now() and qa_start > datetime.now() else 
                ("Completed" if finishing_start < datetime.now() else "Pending"),
                "In Progress" if qa_start < datetime.now() and packing_start > datetime.now() else 
                ("Completed" if qa_start < datetime.now() else "Pending"),
                "In Progress" if packing_start < datetime.now() and delivery_date > datetime.now() else 
                ("Completed" if packing_start < datetime.now() else "Pending"),
                "Completed" if delivery_date < datetime.now() else "Pending"
            ]
        })
        
        # Format for display
        milestones["Planned Date"] = milestones["Planned Date"].dt.strftime("%d-%b-%Y")
        
        # Display milestones
        st.dataframe(milestones, hide_index=True, use_container_width=True)
        
        # Create visual milestone timeline
        milestone_dates = [
            order_date, approval_date, fabric_receipt,
            cutting_start, stitching_start, finishing_start,
            qa_start, packing_start, delivery_date
        ]
        
        milestone_names = [
            "Order Placed", "Order Approved", "Fabric Receipt", 
            "Cutting Start", "Stitching Start", "Finishing Start",
            "Quality Audit", "Packing & Dispatch", "Delivery"
        ]
        
        # Determine which milestones are completed
        completed_status = [date <= datetime.now() for date in milestone_dates]
        
        # Create figure
        fig = go.Figure()
        
        # Add line connecting all points
        fig.add_trace(go.Scatter(
            x=milestone_dates,
            y=[1] * len(milestone_dates),
            mode="lines",
            line=dict(color="lightgrey", width=2),
            hoverinfo="skip"
        ))
        
        # Add completed milestone markers
        completed_dates = [date for i, date in enumerate(milestone_dates) if completed_status[i]]
        completed_names = [name for i, name in enumerate(milestone_names) if completed_status[i]]
        
        if completed_dates:
            fig.add_trace(go.Scatter(
                x=completed_dates,
                y=[1] * len(completed_dates),
                mode="markers+text",
                marker=dict(size=15, color="green", symbol="circle"),
                text=completed_names,
                textposition="top center",
                name="Completed"
            ))
        
        # Add pending milestone markers
        pending_dates = [date for i, date in enumerate(milestone_dates) if not completed_status[i]]
        pending_names = [name for i, name in enumerate(milestone_names) if not completed_status[i]]
        
        if pending_dates:
            fig.add_trace(go.Scatter(
                x=pending_dates,
                y=[1] * len(pending_dates),
                mode="markers+text",
                marker=dict(size=15, color="lightblue", symbol="circle"),
                text=pending_names,
                textposition="top center",
                name="Pending"
            ))
        
        # Add today marker
        fig.add_vline(
            x=datetime.now(),
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text="Today"
        )
        
        # Update layout
        fig.update_layout(
            title="Order Timeline",
            xaxis_title="Date",
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                range=[0.9, 1.1]
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Order actions
        st.subheader("Order Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Update Timeline"):
                st.info("Opening timeline update form...")
        
        with col2:
            if st.button("Download Order Schedule"):
                st.info("Downloading order schedule...")
        
        with col3:
            if st.button("Send Status Update"):
                st.success("Status update sent to buyer")

def download_sample_data():
    """Generate and download sample data for demonstration"""
    # Create sample orders data
    orders_data = pd.DataFrame({
        "Order ID": [f"TS-20240{i}-{1000+i}" for i in range(1, 11)],
        "Buyer": [
            "Fashion Retail Ltd", "Denim Connection", "Style Hub", "Apparel Group",
            "Textile Traders", "Fashion Avenue", "Garment Gallery", "Attire Associates",
            "Clothing Connect", "Fashion Forward"
        ],
        "Trade Show": [
            "India International Garment Fair", "Denim Expo Mumbai", "Fashion Connect Asia",
            "Textile India", "India International Garment Fair", "Denim Expo Mumbai",
            "Fashion Connect Asia", "Textile India", "India International Garment Fair", 
            "Denim Expo Mumbai"
        ],
        "Order Date": [
            "2024-01-15", "2024-01-22", "2024-02-05", "2024-02-12", "2024-02-18",
            "2024-02-25", "2024-03-03", "2024-03-10", "2024-03-15", "2024-03-22"
        ],
        "Delivery Date": [
            "2024-04-15", "2024-04-22", "2024-05-05", "2024-05-12", "2024-05-18",
            "2024-05-25", "2024-06-03", "2024-06-10", "2024-06-15", "2024-06-22"
        ],
        "Styles": [3, 5, 2, 4, 1, 3, 2, 6, 3, 4],
        "Total Qty": [1500, 2500, 800, 1800, 500, 1200, 700, 3000, 1100, 2000],
        "Value (₹)": [
            675000, 1125000, 360000, 810000, 225000, 540000, 315000, 1350000, 495000, 900000
        ],
        "Status": [
            "Completed", "Completed", "In Production", "In Production", "In Production",
            "Approved", "Approved", "Pending Approval", "Draft", "Draft"
        ]
    })
    
    # Create trade show data
    trade_shows = pd.DataFrame({
        "Show Name": [
            "India International Garment Fair", 
            "Denim Expo Mumbai", 
            "Fashion Connect Asia", 
            "Textile India"
        ],
        "Location": ["New Delhi", "Mumbai", "Bangalore", "Ahmedabad"],
        "Start Date": ["2024-06-15", "2024-07-22", "2024-08-10", "2024-09-05"],
        "End Date": ["2024-06-18", "2024-07-25", "2024-08-13", "2024-09-08"],
        "Status": ["Confirmed", "Planning", "Confirmed", "Planning"]
    })
    
    # Create sample style data
    styles_data = []
    
    for i, row in orders_data.iterrows():
        for j in range(row["Styles"]):
            style_id = f"STY-{row['Order ID'][-4:]}-{101+j}"
            styles_data.append({
                "Style ID": style_id,
                "Order ID": row["Order ID"],
                "Buyer": row["Buyer"],
                "Description": np.random.choice([
                    "Skinny Fit Denim Jeans", "Relaxed Fit Jeans", "Slim Straight Jeans",
                    "Denim Jacket", "Denim Shirt", "Cargo Pants", "Denim Shorts"
                ]),
                "Category": np.random.choice(["Jeans", "Jacket", "Shirt", "Shorts"]),
                "Color": np.random.choice(["Blue", "Black", "Grey", "Indigo", "White"]),
                "Quantity": int(row["Total Qty"] / row["Styles"] * (0.8 + 0.4 * np.random.random())),
                "Status": row["Status"]
            })
    
    styles_df = pd.DataFrame(styles_data)
    
    # Create buffer to hold the Excel file
    buffer = io.BytesIO()
    
    # Create a Pandas Excel writer with the buffer
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        orders_data.to_excel(writer, sheet_name='Orders', index=False)
        trade_shows.to_excel(writer, sheet_name='Trade Shows', index=False)
        styles_df.to_excel(writer, sheet_name='Styles', index=False)
    
    # Set the buffer position to the beginning
    buffer.seek(0)
    
    # Create a download link
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="trade_show_sample_data.xlsx">Download Sample Data</a>'
    
    return href

if __name__ == "__main__":
    show_trade_show_order_engine()