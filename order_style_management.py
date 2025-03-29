import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import os
import tempfile
import sqlalchemy.orm

from database import get_db_session, Buyer, Order, Style
from db_operations import (
    get_all_buyers, get_buyer_by_id, add_buyer,
    get_all_orders, get_orders_by_buyer, get_order_by_po, add_order, update_order_status,
    get_styles_by_order, add_style, update_style_status,
    import_orders_from_excel
)

def show_order_style_management():
    """Display the order and style management interface"""
    st.title("📋 Order & Style Management")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📝 Add/Edit Orders", "📤 Import/Export"])
    
    with tab1:
        show_order_overview()
    
    with tab2:
        show_order_editor()
    
    with tab3:
        show_import_export()

def show_order_overview():
    """Display an overview of all orders with filtering options"""
    st.subheader("Orders Overview")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get all buyers for filter
        buyers = get_all_buyers()
        buyer_names = ["All Buyers"] + [buyer.name for buyer in buyers]
        selected_buyer = st.selectbox("Filter by Buyer", buyer_names)
    
    with col2:
        # Status filter
        status_options = ["All Statuses", "New", "In Progress", "Completed", "Cancelled"]
        selected_status = st.selectbox("Filter by Status", status_options)
    
    with col3:
        # Date range filter
        date_options = ["All Time", "Last 30 Days", "Last 90 Days", "Custom Range"]
        selected_date_range = st.selectbox("Filter by Date", date_options)
    
    # If custom date range is selected
    if selected_date_range == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.now().date())
    else:
        # Set default date ranges
        end_date = datetime.now().date()
        if selected_date_range == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
        elif selected_date_range == "Last 90 Days":
            start_date = end_date - timedelta(days=90)
        else:  # All Time
            start_date = datetime(2000, 1, 1).date()
    
    # Get orders based on filters
    if selected_buyer == "All Buyers":
        orders = get_all_orders()
    else:
        # Find buyer id
        buyer = next((b for b in buyers if b.name == selected_buyer), None)
        if buyer:
            orders = get_orders_by_buyer(buyer.id)
        else:
            orders = []
    
    # Filter by status
    if selected_status != "All Statuses":
        orders = [order for order in orders if order.status == selected_status]
    
    # Filter by date
    orders = [order for order in orders if start_date <= order.order_date <= end_date]
    
    if orders:
        # Create dataframe for displaying orders
        order_data = []
        
        for order in orders:
            # Get all styles for this order
            styles = get_styles_by_order(order.id)
            
            # Calculate total styles and completed styles
            total_styles = len(styles)
            completed_styles = sum(1 for style in styles if style.status == 'Completed')
            progress = (completed_styles / total_styles * 100) if total_styles > 0 else 0
            
            # Calculate days to delivery
            days_to_delivery = (order.delivery_date - datetime.now().date()).days
            
            order_data.append({
                "id": order.id,
                "PO Number": order.po_number,
                "Buyer": order.buyer.name,
                "Order Date": order.order_date,
                "Delivery Date": order.delivery_date,
                "Days to Delivery": days_to_delivery,
                "Status": order.status,
                "Total Quantity": order.total_quantity,
                "Styles Count": total_styles,
                "Progress": progress
            })
        
        # Convert to dataframe
        df = pd.DataFrame(order_data)
        
        # Create interactive table with selection
        st.dataframe(
            df.drop(columns=["id", "Progress"]),
            use_container_width=True,
            column_config={
                "PO Number": st.column_config.TextColumn("PO Number"),
                "Buyer": st.column_config.TextColumn("Buyer"),
                "Order Date": st.column_config.DateColumn("Order Date"),
                "Delivery Date": st.column_config.DateColumn("Delivery Date"),
                "Days to Delivery": st.column_config.NumberColumn(
                    "Days to Delivery",
                    help="Days remaining until delivery date",
                    format="%d days"
                ),
                "Status": st.column_config.TextColumn("Status"),
                "Total Quantity": st.column_config.NumberColumn("Total Quantity"),
                "Styles Count": st.column_config.NumberColumn("Styles Count")
            },
            hide_index=True
        )
        
        # Create visualization section
        st.subheader("Order Visualization")
        
        # Order by status chart
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for order status
            fig = px.pie(
                status_counts, 
                values="Count", 
                names="Status",
                title="Orders by Status",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar chart for delivery timeline
            delivery_df = df.copy()
            # Convert to datetime first if not already
            delivery_df["Delivery Date"] = pd.to_datetime(delivery_df["Delivery Date"])
            delivery_df["Delivery Month"] = delivery_df["Delivery Date"].dt.strftime("%Y-%m")
            month_counts = delivery_df["Delivery Month"].value_counts().reset_index()
            month_counts.columns = ["Month", "Count"]
            month_counts = month_counts.sort_values("Month")
            
            fig = px.bar(
                month_counts,
                x="Month",
                y="Count",
                title="Delivery Timeline by Month",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        # Order details section
        st.subheader("Order Details")
        
        # Select order to view details
        selected_po = st.selectbox(
            "Select Order to View Details",
            options=df["PO Number"].tolist(),
            format_func=lambda x: f"{x} - {df[df['PO Number'] == x]['Buyer'].iloc[0]}"
        )
        
        if selected_po:
            # Get the selected order
            selected_order_id = df[df["PO Number"] == selected_po]["id"].iloc[0]
            
            # Get the styles for this order
            styles = get_styles_by_order(selected_order_id)
            
            if styles:
                # Create dataframe for styles
                style_data = []
                
                for style in styles:
                    # Parse size breakdown JSON
                    size_breakdown = json.loads(style.size_breakdown) if style.size_breakdown else {}
                    
                    # Flatten size breakdown
                    style_dict = {
                        "Style Number": style.style_number,
                        "Description": style.description,
                        "Category": style.category,
                        "Color": style.color,
                        "Total Quantity": style.quantity,
                        "Status": style.status
                    }
                    
                    # Add sizes if they exist
                    for size, qty in size_breakdown.items():
                        style_dict[f"Size {size}"] = qty
                    
                    style_data.append(style_dict)
                
                # Display styles
                st.dataframe(
                    pd.DataFrame(style_data),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Allow status update for the order
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Update order status
                    new_status = st.selectbox(
                        "Update Order Status",
                        options=["New", "In Progress", "Completed", "Cancelled"],
                        index=["New", "In Progress", "Completed", "Cancelled"].index(
                            df[df["PO Number"] == selected_po]["Status"].iloc[0]
                        )
                    )
                
                with col2:
                    # Update button
                    if st.button("Update Order Status", type="primary"):
                        success = update_order_status(selected_order_id, new_status)
                        if success:
                            st.success(f"Order status updated to {new_status}")
                            st.rerun()
                        else:
                            st.error("Failed to update order status")
            else:
                st.warning("No styles found for this order")
    else:
        st.info("No orders found with the selected filters")

def show_order_editor():
    """Display the order and style editor"""
    st.subheader("Add New Order")
    
    # Get all buyers
    buyers = get_all_buyers()
    
    # Create columns for buyer selection or creation
    col1, col2 = st.columns(2)
    
    with col1:
        buyer_options = ["Select Buyer"] + [buyer.name for buyer in buyers] + ["+ Add New Buyer"]
        selected_buyer_option = st.selectbox("Buyer", buyer_options)
    
    # If adding new buyer
    if selected_buyer_option == "+ Add New Buyer":
        with st.form("add_buyer_form"):
            st.subheader("Add New Buyer")
            
            buyer_name = st.text_input("Buyer Name")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            
            submit_buyer = st.form_submit_button("Add Buyer")
            
            if submit_buyer and buyer_name:
                new_buyer = add_buyer(buyer_name, contact_person, email, phone)
                if new_buyer:
                    st.success(f"Buyer {buyer_name} added successfully")
                    # Refresh the page to update buyer list
                    st.rerun()
                else:
                    st.error("Failed to add buyer")
    
    # Only proceed with order creation if a buyer is selected
    elif selected_buyer_option != "Select Buyer":
        # Find the selected buyer
        selected_buyer = next((buyer for buyer in buyers if buyer.name == selected_buyer_option), None)
        
        if selected_buyer:
            # Order form
            with st.form("add_order_form"):
                st.subheader("Order Details")
                
                po_number = st.text_input("PO Number")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    order_date = st.date_input("Order Date", datetime.now().date())
                
                with col2:
                    delivery_date = st.date_input("Delivery Date", datetime.now().date() + timedelta(days=90))
                
                # Calculate total days for production
                if delivery_date and order_date:
                    production_days = (delivery_date - order_date).days
                    st.info(f"Production window: {production_days} days")
                
                submit_order = st.form_submit_button("Create Order")
                
                if submit_order and po_number:
                    # Check if order with this PO already exists
                    existing_order = get_order_by_po(po_number)
                    
                    if existing_order:
                        st.error(f"Order with PO number {po_number} already exists")
                    else:
                        # Create new order
                        new_order = add_order(po_number, selected_buyer.id, order_date, delivery_date)
                        
                        if new_order:
                            st.success(f"Order {po_number} created successfully")
                            st.session_state.new_order_id = new_order.id
                            st.session_state.add_styles = True
                            st.rerun()
                        else:
                            st.error("Failed to create order")
            
            # If a new order was just created, show the style form
            if hasattr(st.session_state, 'add_styles') and st.session_state.add_styles:
                add_styles_to_order(st.session_state.new_order_id)
    
    # Show existing orders for editing
    st.divider()
    st.subheader("Edit Existing Order")
    
    orders = get_all_orders()
    
    if orders:
        order_options = ["Select Order"] + [f"{order.po_number} - {order.buyer.name}" for order in orders]
        selected_order_option = st.selectbox("Order", order_options)
        
        if selected_order_option != "Select Order":
            # Get the selected order
            po_number = selected_order_option.split(" - ")[0]
            selected_order = get_order_by_po(po_number)
            
            if selected_order:
                # Show the styles for this order
                st.subheader(f"Styles for {selected_order.po_number}")
                
                styles = get_styles_by_order(selected_order.id)
                
                if styles:
                    # Create dataframe for styles
                    style_data = []
                    
                    for style in styles:
                        # Parse size breakdown JSON
                        size_breakdown = json.loads(style.size_breakdown) if style.size_breakdown else {}
                        
                        # Flatten size breakdown
                        style_dict = {
                            "id": style.id,
                            "Style Number": style.style_number,
                            "Description": style.description,
                            "Category": style.category,
                            "Color": style.color,
                            "Total Quantity": style.quantity,
                            "Status": style.status
                        }
                        
                        # Add sizes if they exist
                        for size, qty in size_breakdown.items():
                            style_dict[f"Size {size}"] = qty
                        
                        style_data.append(style_dict)
                    
                    # Display styles
                    style_df = pd.DataFrame(style_data)
                    
                    st.dataframe(
                        style_df.drop(columns=["id"]),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Allow updating style status
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Select style to update
                        style_options = [f"{s['Style Number']} - {s['Description']}" for _, s in style_df.iterrows()]
                        selected_style = st.selectbox("Select Style to Update", style_options)
                        
                        if selected_style:
                            style_number = selected_style.split(" - ")[0]
                            style_id = style_df[style_df["Style Number"] == style_number]["id"].iloc[0]
                            current_status = style_df[style_df["Style Number"] == style_number]["Status"].iloc[0]
                    
                    with col2:
                        # Update style status
                        new_status = st.selectbox(
                            "Update Style Status",
                            options=["New", "In Progress", "Completed"],
                            index=["New", "In Progress", "Completed"].index(current_status)
                        )
                        
                        if st.button("Update Style Status"):
                            success = update_style_status(style_id, new_status)
                            if success:
                                st.success(f"Style status updated to {new_status}")
                                st.rerun()
                            else:
                                st.error("Failed to update style status")
                    
                    # Add more styles to this order
                    if st.button("Add More Styles to This Order"):
                        st.session_state.add_styles = True
                        st.session_state.new_order_id = selected_order.id
                        st.rerun()
                else:
                    st.info("No styles found for this order")
                    
                    # Add styles to this order
                    if st.button("Add Styles to This Order"):
                        st.session_state.add_styles = True
                        st.session_state.new_order_id = selected_order.id
                        st.rerun()
    else:
        st.info("No orders available. Create a new order to get started.")
    
    # If add_styles is true, show the style form
    if hasattr(st.session_state, 'add_styles') and st.session_state.add_styles:
        add_styles_to_order(st.session_state.new_order_id)

def add_styles_to_order(order_id):
    """Show form to add styles to an order"""
    order = get_order_by_id(order_id)
    
    if order:
        st.divider()
        st.subheader(f"Add Styles to Order {order.po_number}")
        
        with st.form("add_style_form"):
            style_number = st.text_input("Style Number")
            description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            
            with col1:
                category = st.selectbox(
                    "Category",
                    options=["T-shirt", "Polo", "Shirt", "Pants", "Jacket", "Sweater", "Dress", "Skirt", "Other"]
                )
            
            with col2:
                color = st.text_input("Color")
            
            # Size breakdown
            st.subheader("Size Breakdown")
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                xs_qty = st.number_input("XS", min_value=0, value=0, step=1)
            
            with col2:
                s_qty = st.number_input("S", min_value=0, value=0, step=1)
            
            with col3:
                m_qty = st.number_input("M", min_value=0, value=0, step=1)
            
            with col4:
                l_qty = st.number_input("L", min_value=0, value=0, step=1)
            
            with col5:
                xl_qty = st.number_input("XL", min_value=0, value=0, step=1)
            
            with col6:
                xxl_qty = st.number_input("XXL", min_value=0, value=0, step=1)
            
            # Calculate total quantity
            total_quantity = xs_qty + s_qty + m_qty + l_qty + xl_qty + xxl_qty
            
            st.metric("Total Quantity", total_quantity)
            
            submit_style = st.form_submit_button("Add Style")
            
            if submit_style and style_number and total_quantity > 0:
                # Create size breakdown dictionary
                size_breakdown = {}
                if xs_qty > 0:
                    size_breakdown["XS"] = xs_qty
                if s_qty > 0:
                    size_breakdown["S"] = s_qty
                if m_qty > 0:
                    size_breakdown["M"] = m_qty
                if l_qty > 0:
                    size_breakdown["L"] = l_qty
                if xl_qty > 0:
                    size_breakdown["XL"] = xl_qty
                if xxl_qty > 0:
                    size_breakdown["XXL"] = xxl_qty
                
                # Add the style
                new_style = add_style(
                    order_id,
                    style_number,
                    description,
                    category,
                    color,
                    size_breakdown,
                    total_quantity
                )
                
                if new_style:
                    st.success(f"Style {style_number} added successfully")
                    
                    # Update order total quantity
                    order = get_order_by_id(order_id)
                    if order:
                        styles = get_styles_by_order(order_id)
                        order_total = sum(style.quantity for style in styles)
                        # Update order with new total
                        db = get_db_session()
                        try:
                            db_order = db.query(Order).filter(Order.id == order_id).first()
                            if db_order:
                                db_order.total_quantity = order_total
                                db.commit()
                        finally:
                            db.close()
                    
                    # Ask if user wants to add another style
                    if st.button("Add Another Style"):
                        st.rerun()
                    else:
                        # Clear session state and return to order editor
                        st.session_state.add_styles = False
                        if hasattr(st.session_state, 'new_order_id'):
                            del st.session_state.new_order_id
                        st.rerun()
                else:
                    st.error("Failed to add style")

def get_order_by_id(order_id):
    """Get an order by ID"""
    db = get_db_session()
    try:
        # Eagerly load buyer relationship to avoid detached instance error
        order = db.query(Order).filter(Order.id == order_id).options(sqlalchemy.orm.joinedload(Order.buyer)).first()
        return order
    finally:
        db.close()

def show_import_export():
    """Display the import/export interface"""
    st.subheader("Import/Export Data")
    
    # Create tabs for import and export
    tab1, tab2 = st.tabs(["📥 Import Data", "📤 Export Data"])
    
    with tab1:
        st.subheader("Import Orders & Styles from Excel")
        
        # Upload file
        uploaded_file = st.file_uploader(
            "Upload Excel file with Orders and Styles",
            type=["xlsx", "xls"],
            help="Excel file should have at least two sheets: 'Orders' and 'Styles'"
        )
        
        # Show template download
        st.markdown("Need a template? [Download Template]()")
        
        if uploaded_file:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name
            
            try:
                # Preview the data
                orders_df = pd.read_excel(temp_path, sheet_name='Orders')
                styles_df = pd.read_excel(temp_path, sheet_name='Styles')
                
                # Show preview
                st.subheader("Orders Preview")
                st.dataframe(orders_df.head(), use_container_width=True)
                
                st.subheader("Styles Preview")
                st.dataframe(styles_df.head(), use_container_width=True)
                
                # Import button
                if st.button("Import Data", type="primary"):
                    success, message = import_orders_from_excel(temp_path)
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
            
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    with tab2:
        st.subheader("Export Data to Excel")
        
        # Export options
        export_type = st.selectbox(
            "Select what to export",
            options=["All Orders and Styles", "Specific Buyer Orders", "Specific Date Range"]
        )
        
        if export_type == "Specific Buyer Orders":
            # Select buyer to export
            buyers = get_all_buyers()
            buyer_options = [buyer.name for buyer in buyers]
            selected_buyer = st.selectbox("Select Buyer", buyer_options)
        
        elif export_type == "Specific Date Range":
            # Select date range
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30))
            
            with col2:
                end_date = st.date_input("End Date", datetime.now().date())
        
        # Export button
        if st.button("Generate Export"):
            # Placeholder for export functionality
            # In a real application, this would generate an Excel file for download
            
            # For now, show a success message
            st.success("Export generated! (Placeholder - actual export not implemented yet)")
            
            # Download button
            st.download_button(
                label="Download Excel File",
                data=b"placeholder",  # This would be the actual file data
                file_name="orders_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                disabled=True  # Disabled for now since we're not generating a real file
            )