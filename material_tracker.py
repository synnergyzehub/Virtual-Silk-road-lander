import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px
import json
import tempfile
import os

from database import get_db_session, Material, Style, Order
from db_operations import (
    get_all_orders, get_styles_by_order, get_materials_by_style,
    add_material, update_material_status, import_materials_from_excel
)

def show_material_tracker():
    """Display the material tracking system interface"""
    st.title("🧶 Material Tracker")
    
    # Create tabs for different views of the material tracker
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🧾 Requisition", 
        "📦 Receiving & Issuance",
        "📥 Import/Export"
    ])
    
    with tab1:
        show_material_overview()
    
    with tab2:
        show_material_requisition()
    
    with tab3:
        show_material_receiving_issuance()
    
    with tab4:
        show_material_import_export()

def show_material_overview():
    """Display an overview of all materials with filtering and search"""
    st.subheader("Materials Overview")
    
    # Get all orders to build the filter options
    orders = get_all_orders()
    
    # Filter options in a sidebar container
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filter by order/PO
            order_options = ["All Orders"] + [order.po_number for order in orders]
            selected_order = st.selectbox("Filter by PO Number", order_options)
        
        with col2:
            # Filter by material type
            material_types = ["All Types", "Fabric", "Trim", "Accessories"]
            selected_type = st.selectbox("Filter by Material Type", material_types)
        
        with col3:
            # Filter by status
            status_options = ["All Statuses", "Pending", "Ordered", "Received", "Issued"]
            selected_status = st.selectbox("Filter by Status", status_options)
    
    # Get materials based on filters
    materials = []
    
    if selected_order == "All Orders":
        # Get all styles across all orders
        all_styles = []
        for order in orders:
            styles = get_styles_by_order(order.id)
            all_styles.extend(styles)
        
        # Get materials for all styles
        for style in all_styles:
            style_materials = get_materials_by_style(style.id)
            
            # Apply material type filter
            if selected_type != "All Types":
                style_materials = [m for m in style_materials if m.type == selected_type]
            
            # Apply status filter
            if selected_status != "All Statuses":
                style_materials = [m for m in style_materials if m.status == selected_status]
            
            materials.extend(style_materials)
    else:
        # Get the selected order
        selected_order_obj = next((o for o in orders if o.po_number == selected_order), None)
        
        if selected_order_obj:
            # Get styles for this order
            styles = get_styles_by_order(selected_order_obj.id)
            
            # Get materials for these styles
            for style in styles:
                style_materials = get_materials_by_style(style.id)
                
                # Apply material type filter
                if selected_type != "All Types":
                    style_materials = [m for m in style_materials if m.type == selected_type]
                
                # Apply status filter
                if selected_status != "All Statuses":
                    style_materials = [m for m in style_materials if m.status == selected_status]
                
                materials.extend(style_materials)
    
    # Display material summary metrics
    if materials:
        # Create metrics for material status
        col1, col2, col3, col4 = st.columns(4)
        
        pending_count = sum(1 for m in materials if m.status == "Pending")
        ordered_count = sum(1 for m in materials if m.status == "Ordered")
        received_count = sum(1 for m in materials if m.status == "Received")
        issued_count = sum(1 for m in materials if m.status == "Issued")
        
        with col1:
            st.metric("Pending", pending_count)
        
        with col2:
            st.metric("Ordered", ordered_count)
        
        with col3:
            st.metric("Received", received_count)
        
        with col4:
            st.metric("Issued", issued_count)
        
        # Create material dataframe for display
        material_data = []
        
        for material in materials:
            # Get the style for this material
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == material.style_id).first()
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                    
                    material_data.append({
                        "id": material.id,
                        "Material Name": material.name,
                        "Type": material.type,
                        "Style": style.style_number,
                        "PO Number": order.po_number if order else "Unknown",
                        "Required Qty": material.required_quantity,
                        "Received Qty": material.received_quantity,
                        "Issued Qty": material.issued_quantity,
                        "Unit": material.unit,
                        "Status": material.status,
                        "PO Date": material.po_date.strftime('%Y-%m-%d') if material.po_date else "",
                        "Expected Delivery": material.expected_delivery.strftime('%Y-%m-%d') if material.expected_delivery else "",
                        "Actual Delivery": material.actual_delivery.strftime('%Y-%m-%d') if material.actual_delivery else "",
                        "Remarks": material.remarks or ""
                    })
            finally:
                db.close()
        
        # Convert to dataframe
        df = pd.DataFrame(material_data)
        
        # Display materials in an interactive table
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Material analysis charts
        st.subheader("Material Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Material status chart
            status_counts = df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            
            fig = px.pie(
                status_counts, 
                values="Count", 
                names="Status",
                title="Materials by Status",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Material type breakdown
            type_counts = df["Type"].value_counts().reset_index()
            type_counts.columns = ["Type", "Count"]
            
            fig = px.bar(
                type_counts,
                y="Type",
                x="Count",
                title="Materials by Type",
                orientation='h',
                color="Type",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        # Expected vs. Actual Delivery Analysis
        if "Expected Delivery" in df.columns and df["Expected Delivery"].any():
            st.subheader("Delivery Timeline")
            
            # Prepare data for timeline
            timeline_data = df[df["Expected Delivery"] != ""].copy()
            
            if not timeline_data.empty:
                # Convert date strings to datetime
                timeline_data["Expected Delivery"] = pd.to_datetime(timeline_data["Expected Delivery"])
                timeline_data["Actual Delivery"] = pd.to_datetime(timeline_data["Actual Delivery"], errors='coerce')
                
                # Calculate delay (in days) for items with actual delivery
                timeline_data["Delay"] = np.nan
                mask = ~timeline_data["Actual Delivery"].isna()
                timeline_data.loc[mask, "Delay"] = (timeline_data.loc[mask, "Actual Delivery"] - 
                                                   timeline_data.loc[mask, "Expected Delivery"]).dt.days
                
                # Create a delivery timeline visualization
                fig = go.Figure()
                
                for idx, row in timeline_data.iterrows():
                    # Add expected delivery point
                    fig.add_trace(go.Scatter(
                        x=[row["Expected Delivery"]],
                        y=[row["Material Name"]],
                        mode="markers",
                        name="Expected",
                        marker=dict(color="blue", size=10, symbol="circle"),
                        showlegend=idx == 0
                    ))
                    
                    # Add actual delivery point if available
                    if not pd.isna(row["Actual Delivery"]):
                        fig.add_trace(go.Scatter(
                            x=[row["Actual Delivery"]],
                            y=[row["Material Name"]],
                            mode="markers",
                            name="Actual",
                            marker=dict(color="green" if row["Delay"] <= 0 else "red", 
                                       size=10, 
                                       symbol="diamond"),
                            showlegend=idx == 0
                        ))
                
                fig.update_layout(
                    title="Material Delivery Timeline",
                    xaxis_title="Date",
                    yaxis_title="Material",
                    height=400,
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Delay analysis
                delay_data = timeline_data[~timeline_data["Delay"].isna()].copy()
                
                if not delay_data.empty:
                    st.subheader("Delivery Delay Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Average delay metric
                        avg_delay = delay_data["Delay"].mean()
                        st.metric(
                            "Average Delay", 
                            f"{avg_delay:.1f} days",
                            delta=None
                        )
                    
                    with col2:
                        # On-time delivery percentage
                        on_time = (delay_data["Delay"] <= 0).sum()
                        total = len(delay_data)
                        on_time_pct = (on_time / total) * 100 if total > 0 else 0
                        
                        st.metric(
                            "On-Time Delivery Rate", 
                            f"{on_time_pct:.1f}%",
                            delta=None
                        )
    else:
        st.info("No materials found with the selected filters")

def show_material_requisition():
    """Display the material requisition interface for creating and tracking material requirements"""
    st.subheader("Material Requisition")
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available. Please create orders first.")
        return
    
    # Select order to create requisition for
    order_options = [f"{order.po_number} - {order.buyer.name}" for order in orders]
    selected_order = st.selectbox("Select Order", order_options)
    
    if selected_order:
        # Get the selected order
        po_number = selected_order.split(" - ")[0]
        order = next((o for o in orders if o.po_number == po_number), None)
        
        if order:
            # Get styles for this order
            styles = get_styles_by_order(order.id)
            
            if styles:
                # Create a container for the style selection
                st.subheader("Select Style for Material Requisition")
                
                # Create style selection
                style_options = [f"{style.style_number} - {style.description}" for style in styles]
                selected_style = st.selectbox("Select Style", style_options)
                
                if selected_style:
                    # Get the selected style
                    style_number = selected_style.split(" - ")[0]
                    style = next((s for s in styles if s.style_number == style_number), None)
                    
                    if style:
                        # Show existing materials for this style
                        st.write(f"### Materials for Style: {style.style_number}")
                        
                        existing_materials = get_materials_by_style(style.id)
                        
                        if existing_materials:
                            # Create material dataframe
                            material_data = []
                            
                            for material in existing_materials:
                                material_data.append({
                                    "Material Name": material.name,
                                    "Type": material.type,
                                    "Required Qty": material.required_quantity,
                                    "Unit": material.unit,
                                    "Status": material.status,
                                    "PO Number": material.po_number or "",
                                    "Expected Delivery": material.expected_delivery.strftime('%Y-%m-%d') if material.expected_delivery else ""
                                })
                            
                            # Display materials
                            st.dataframe(
                                pd.DataFrame(material_data),
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.info("No materials created for this style yet.")
                        
                        # Form to add new material
                        st.divider()
                        st.subheader("Add New Material")
                        
                        with st.form("add_material_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                material_name = st.text_input("Material Name")
                            
                            with col2:
                                material_type = st.selectbox(
                                    "Material Type",
                                    options=["Fabric", "Trim", "Accessories"]
                                )
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                required_qty = st.number_input("Required Quantity", min_value=0.0, value=0.0, step=0.1)
                            
                            with col2:
                                unit = st.selectbox(
                                    "Unit",
                                    options=["Meters", "Yards", "Pieces", "Kg", "Dozen"]
                                )
                            
                            submit_material = st.form_submit_button("Add Material")
                            
                            if submit_material and material_name and required_qty > 0:
                                # Add the material
                                new_material = add_material(
                                    style.id,
                                    material_name,
                                    material_type,
                                    unit,
                                    required_qty
                                )
                                
                                if new_material:
                                    st.success(f"Material {material_name} added successfully")
                                    st.rerun()
                                else:
                                    st.error("Failed to add material")
                    else:
                        st.error("Style not found")
                
                # Create a bulk material creation form as an expander
                with st.expander("Bulk Material Creation"):
                    st.write("Use this form to create multiple materials at once")
                    
                    # Create a dynamic form with add/remove capability
                    if 'materials' not in st.session_state:
                        st.session_state.materials = [{}]
                    
                    # Add button to add a new material entry
                    if st.button("Add Material Entry"):
                        st.session_state.materials.append({})
                        st.rerun()
                    
                    # Create form for bulk upload
                    with st.form("bulk_material_form"):
                        for i, material in enumerate(st.session_state.materials):
                            st.subheader(f"Material {i+1}")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                material['name'] = st.text_input(f"Material Name {i+1}", key=f"name_{i}")
                            
                            with col2:
                                material['type'] = st.selectbox(
                                    f"Material Type {i+1}",
                                    options=["Fabric", "Trim", "Accessories"],
                                    key=f"type_{i}"
                                )
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                material['qty'] = st.number_input(
                                    f"Required Quantity {i+1}", 
                                    min_value=0.0, 
                                    value=0.0, 
                                    step=0.1,
                                    key=f"qty_{i}"
                                )
                            
                            with col2:
                                material['unit'] = st.selectbox(
                                    f"Unit {i+1}",
                                    options=["Meters", "Yards", "Pieces", "Kg", "Dozen"],
                                    key=f"unit_{i}"
                                )
                            
                            if i > 0:  # Add remove button after the first entry
                                if st.button(f"Remove Material {i+1}", key=f"remove_{i}"):
                                    st.session_state.materials.pop(i)
                                    st.rerun()
                            
                            st.divider()
                        
                        # Submit button for bulk creation
                        submit_bulk = st.form_submit_button("Create All Materials")
                        
                        if submit_bulk:
                            # Filter out empty entries
                            valid_materials = [m for m in st.session_state.materials 
                                              if m.get('name') and m.get('qty', 0) > 0]
                            
                            if valid_materials:
                                success_count = 0
                                
                                for material in valid_materials:
                                    # Add each material
                                    new_material = add_material(
                                        style.id,
                                        material['name'],
                                        material['type'],
                                        material['unit'],
                                        material['qty']
                                    )
                                    
                                    if new_material:
                                        success_count += 1
                                
                                if success_count > 0:
                                    st.success(f"Added {success_count} materials successfully")
                                    # Reset the form
                                    st.session_state.materials = [{}]
                                    st.rerun()
                                else:
                                    st.error("Failed to add materials")
                            else:
                                st.warning("No valid materials to add")
            else:
                st.warning("No styles found for this order. Please add styles first.")
        else:
            st.error("Order not found")

def show_material_receiving_issuance():
    """Display the material receiving and issuance interface"""
    st.subheader("Material Receiving & Issuance")
    
    # Create tabs for receiving and issuance
    tab1, tab2 = st.tabs(["📦 Material Receiving", "🔄 Material Issuance"])
    
    with tab1:
        show_material_receiving()
    
    with tab2:
        show_material_issuance()

def show_material_receiving():
    """Display the material receiving interface"""
    st.subheader("Material Receiving")
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter by order/PO
        order_options = ["All Orders"] + [order.po_number for order in orders]
        selected_order = st.selectbox("Filter by PO Number", order_options, key="receive_po")
    
    with col2:
        # Filter by status
        status_options = ["Pending", "Ordered"]
        selected_status = st.selectbox("Filter by Status", status_options, key="receive_status")
    
    # Get materials based on filters
    materials = []
    
    if selected_order == "All Orders":
        # Get all styles across all orders
        all_styles = []
        for order in orders:
            styles = get_styles_by_order(order.id)
            all_styles.extend(styles)
        
        # Get materials for all styles
        for style in all_styles:
            style_materials = get_materials_by_style(style.id)
            
            # Filter by status
            style_materials = [m for m in style_materials if m.status == selected_status]
            
            materials.extend(style_materials)
    else:
        # Get the selected order
        selected_order_obj = next((o for o in orders if o.po_number == selected_order), None)
        
        if selected_order_obj:
            # Get styles for this order
            styles = get_styles_by_order(selected_order_obj.id)
            
            # Get materials for these styles
            for style in styles:
                style_materials = get_materials_by_style(style.id)
                
                # Filter by status
                style_materials = [m for m in style_materials if m.status == selected_status]
                
                materials.extend(style_materials)
    
    if materials:
        # Create material dataframe for display
        material_data = []
        
        for material in materials:
            # Get the style for this material
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == material.style_id).first()
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                    
                    material_data.append({
                        "id": material.id,
                        "Material Name": material.name,
                        "Type": material.type,
                        "Style": style.style_number,
                        "PO Number": order.po_number if order else "Unknown",
                        "Required Qty": material.required_quantity,
                        "Unit": material.unit,
                        "Status": material.status,
                        "Material PO": material.po_number or ""
                    })
            finally:
                db.close()
        
        # Convert to dataframe
        df = pd.DataFrame(material_data)
        
        # Display materials in an interactive table
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Select material to receive
        selected_material = st.selectbox(
            "Select Material to Receive",
            options=[f"{m['Material Name']} ({m['Style']})" for _, m in df.iterrows()]
        )
        
        if selected_material:
            # Get material name and style
            material_name = selected_material.split(" (")[0]
            style_number = selected_material.split("(")[1].replace(")", "")
            
            # Find the material
            material_id = df[(df["Material Name"] == material_name) & (df["Style"] == style_number)]["id"].iloc[0]
            material_row = df[(df["Material Name"] == material_name) & (df["Style"] == style_number)].iloc[0]
            
            # Show material details
            st.write(f"### Receiving: {material_name}")
            st.write(f"Required Quantity: {material_row['Required Qty']} {material_row['Unit']}")
            
            # Create a form for receiving the material
            with st.form("receive_material_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if material_row["Status"] == "Pending":
                        po_number = st.text_input("Material PO Number")
                        po_date = st.date_input("PO Date", datetime.datetime.now().date())
                    else:
                        po_number = st.text_input("Material PO Number", value=material_row["Material PO"], disabled=True)
                        # Use the existing PO date or today
                        db = get_db_session()
                        try:
                            material = db.query(Material).filter(Material.id == material_id).first()
                            po_date = st.date_input("PO Date", material.po_date or datetime.datetime.now().date())
                        finally:
                            db.close()
                
                with col2:
                    received_qty = st.number_input(
                        "Received Quantity", 
                        min_value=0.0, 
                        max_value=float(material_row["Required Qty"]),
                        value=0.0, 
                        step=0.1
                    )
                    
                    actual_delivery = st.date_input("Delivery Date", datetime.datetime.now().date())
                
                remarks = st.text_area("Remarks")
                
                submit_receiving = st.form_submit_button("Record Material Receipt")
                
                if submit_receiving and received_qty > 0:
                    # Determine the status based on received quantity
                    if received_qty >= material_row["Required Qty"]:
                        new_status = "Received"
                    else:
                        new_status = "Ordered"  # Partial receipt keeps the status as ordered
                    
                    # Update the material status
                    success = update_material_status(
                        material_id,
                        new_status,
                        po_number=po_number,
                        po_date=po_date,
                        received_quantity=received_qty,
                        actual_delivery=actual_delivery,
                        remarks=remarks
                    )
                    
                    if success:
                        st.success(f"Material receipt recorded successfully")
                        st.rerun()
                    else:
                        st.error("Failed to record material receipt")
    else:
        st.info(f"No {selected_status.lower()} materials found with the selected filters")

def show_material_issuance():
    """Display the material issuance interface"""
    st.subheader("Material Issuance")
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter by order/PO
        order_options = ["All Orders"] + [order.po_number for order in orders]
        selected_order = st.selectbox("Filter by PO Number", order_options, key="issue_po")
    
    with col2:
        # Only show received materials that can be issued
        status_options = ["Received"]
        selected_status = st.selectbox("Status", status_options, key="issue_status", disabled=True)
    
    # Get materials based on filters
    materials = []
    
    if selected_order == "All Orders":
        # Get all styles across all orders
        all_styles = []
        for order in orders:
            styles = get_styles_by_order(order.id)
            all_styles.extend(styles)
        
        # Get materials for all styles
        for style in all_styles:
            style_materials = get_materials_by_style(style.id)
            
            # Filter by status
            style_materials = [m for m in style_materials if m.status == "Received"]
            
            materials.extend(style_materials)
    else:
        # Get the selected order
        selected_order_obj = next((o for o in orders if o.po_number == selected_order), None)
        
        if selected_order_obj:
            # Get styles for this order
            styles = get_styles_by_order(selected_order_obj.id)
            
            # Get materials for these styles
            for style in styles:
                style_materials = get_materials_by_style(style.id)
                
                # Filter by status
                style_materials = [m for m in style_materials if m.status == "Received"]
                
                materials.extend(style_materials)
    
    if materials:
        # Create material dataframe for display
        material_data = []
        
        for material in materials:
            # Get the style for this material
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == material.style_id).first()
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                    
                    material_data.append({
                        "id": material.id,
                        "Material Name": material.name,
                        "Type": material.type,
                        "Style": style.style_number,
                        "PO Number": order.po_number if order else "Unknown",
                        "Required Qty": material.required_quantity,
                        "Received Qty": material.received_quantity,
                        "Issued Qty": material.issued_quantity,
                        "Available Qty": material.received_quantity - material.issued_quantity,
                        "Unit": material.unit,
                        "Status": material.status
                    })
            finally:
                db.close()
        
        # Convert to dataframe
        df = pd.DataFrame(material_data)
        
        # Display materials in an interactive table
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Select material to issue
        available_materials = df[df["Available Qty"] > 0]
        
        if not available_materials.empty:
            selected_material = st.selectbox(
                "Select Material to Issue",
                options=[f"{m['Material Name']} ({m['Style']}) - {m['Available Qty']} {m['Unit']} available" 
                        for _, m in available_materials.iterrows()]
            )
            
            if selected_material:
                # Get material name and style
                material_info = selected_material.split(" (")[0]
                style_info = selected_material.split("(")[1].split(")")[0]
                
                # Find the material
                material_id = df[(df["Material Name"] == material_info) & (df["Style"] == style_info)]["id"].iloc[0]
                material_row = df[(df["Material Name"] == material_info) & (df["Style"] == style_info)].iloc[0]
                
                # Show material details
                st.write(f"### Issuing: {material_info}")
                st.write(f"Available Quantity: {material_row['Available Qty']} {material_row['Unit']}")
                
                # Create a form for issuing the material
                with st.form("issue_material_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        issue_qty = st.number_input(
                            "Issue Quantity", 
                            min_value=0.0, 
                            max_value=float(material_row["Available Qty"]),
                            value=0.0, 
                            step=0.1
                        )
                    
                    with col2:
                        issue_date = st.date_input("Issue Date", datetime.datetime.now().date())
                    
                    issue_to = st.text_input("Issue To (Department/Section)")
                    remarks = st.text_area("Remarks")
                    
                    submit_issuance = st.form_submit_button("Record Material Issuance")
                    
                    if submit_issuance and issue_qty > 0:
                        # Calculate new issued quantity
                        new_issued_qty = material_row["Issued Qty"] + issue_qty
                        
                        # Determine if all material has been issued
                        new_status = "Issued" if new_issued_qty >= material_row["Required Qty"] else "Received"
                        
                        # Update the material
                        success = update_material_status(
                            material_id,
                            new_status,
                            issued_quantity=new_issued_qty,
                            remarks=f"{remarks}\nIssued {issue_qty} {material_row['Unit']} to {issue_to} on {issue_date}"
                        )
                        
                        if success:
                            st.success(f"Material issuance recorded successfully")
                            st.rerun()
                        else:
                            st.error("Failed to record material issuance")
        else:
            st.info("No materials available for issuance")
    else:
        st.info("No received materials found with the selected filters")

def show_material_import_export():
    """Display the material import/export interface"""
    st.subheader("Import/Export Materials")
    
    # Create tabs for import and export
    tab1, tab2 = st.tabs(["📥 Import Materials", "📤 Export Materials"])
    
    with tab1:
        st.subheader("Import Materials from Excel")
        
        # Upload file
        uploaded_file = st.file_uploader(
            "Upload Excel file with Materials",
            type=["xlsx", "xls"],
            help="Excel file should have a sheet named 'Materials'"
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
                materials_df = pd.read_excel(temp_path, sheet_name='Materials')
                
                # Show preview
                st.subheader("Materials Preview")
                st.dataframe(materials_df.head(), use_container_width=True)
                
                # Import button
                if st.button("Import Materials", type="primary"):
                    success, message = import_materials_from_excel(temp_path)
                    
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
        st.subheader("Export Materials to Excel")
        
        # Export options
        export_type = st.selectbox(
            "Select what to export",
            options=["All Materials", "Materials by Order", "Materials by Status"]
        )
        
        if export_type == "Materials by Order":
            # Select order to export
            orders = get_all_orders()
            if orders:
                order_options = [order.po_number for order in orders]
                selected_order = st.selectbox("Select Order", order_options)
            else:
                st.warning("No orders available.")
                return
        
        elif export_type == "Materials by Status":
            # Select status to export
            status_options = ["Pending", "Ordered", "Received", "Issued"]
            selected_status = st.selectbox("Select Status", status_options)
        
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
                file_name="materials_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                disabled=True  # Disabled for now since we're not generating a real file
            )