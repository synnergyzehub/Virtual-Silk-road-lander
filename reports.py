import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io
import xlsxwriter
from datetime import datetime, timedelta
import json
from fpdf import FPDF
import base64
import tempfile
import os

from database import get_db_session, Order, Style, Material, ProductionEntry, ProductionLine, LineAllocation
from db_operations import (
    get_all_orders, get_styles_by_order, get_materials_by_style,
    get_production_entries_by_date_range, get_production_entries_by_style,
    get_all_production_lines, get_all_buyers
)

def show_reports():
    """Display the reporting and export interface"""
    st.title("📊 Reports & Export")
    
    # Create tabs for different report types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Order Reports", 
        "🧶 Material Reports", 
        "⏱ Production Reports",
        "📈 Line Performance",
        "📥 Custom Reports"
    ])
    
    with tab1:
        show_order_reports()
    
    with tab2:
        show_material_reports()
    
    with tab3:
        show_production_reports()
    
    with tab4:
        show_line_performance_reports()
    
    with tab5:
        show_custom_reports()

def show_order_reports():
    """Display order-related reports"""
    st.subheader("Order Reports")
    
    # Order report options
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Order Summary",
            "Order Status Report",
            "Buyer-wise Orders",
            "Delivery Timeline",
            "Style Breakdown"
        ]
    )
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Add filter options based on report type
    if report_type == "Buyer-wise Orders":
        # Get all buyers
        buyers = get_all_buyers()
        buyer_options = ["All Buyers"] + [buyer.name for buyer in buyers]
        selected_buyer = st.selectbox("Select Buyer", buyer_options)
        
        if selected_buyer != "All Buyers":
            # Filter orders by buyer
            buyer = next((b for b in buyers if b.name == selected_buyer), None)
            if buyer:
                orders = [order for order in orders if order.buyer_id == buyer.id]
    
    elif report_type in ["Delivery Timeline", "Order Status Report"]:
        # Date range filter
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30))
        
        with col2:
            end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=60))
        
        # Filter orders by date
        orders = [
            order for order in orders 
            if (order.order_date >= start_date and order.order_date <= end_date) or
               (order.delivery_date >= start_date and order.delivery_date <= end_date)
        ]
    
    # Generate report data
    if orders:
        if report_type == "Order Summary":
            # Create order summary data
            order_data = []
            
            for order in orders:
                # Get styles for this order
                styles = get_styles_by_order(order.id)
                
                # Calculate completion percentage
                total_styles = len(styles)
                completed_styles = sum(1 for style in styles if style.status == 'Completed')
                completion = (completed_styles / total_styles * 100) if total_styles > 0 else 0
                
                # Calculate days to delivery
                days_to_delivery = (order.delivery_date - datetime.now().date()).days
                
                order_data.append({
                    "PO Number": order.po_number,
                    "Buyer": order.buyer.name,
                    "Order Date": order.order_date,
                    "Delivery Date": order.delivery_date,
                    "Days to Delivery": days_to_delivery,
                    "Status": order.status,
                    "Styles Count": total_styles,
                    "Total Quantity": order.total_quantity,
                    "Completion %": f"{completion:.1f}%"
                })
            
            # Convert to dataframe
            df = pd.DataFrame(order_data)
            
            # Sort by delivery date
            df = df.sort_values('Days to Delivery')
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualization
            fig = px.bar(
                df,
                x="PO Number",
                y="Total Quantity",
                color="Status",
                hover_data=["Buyer", "Delivery Date", "Completion %"],
                title="Order Quantities by PO Number",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Order Status Report":
            # Create status report data
            status_data = []
            
            for order in orders:
                # Get styles for this order
                styles = get_styles_by_order(order.id)
                
                # Count styles by status
                style_status_counts = {
                    "New": sum(1 for style in styles if style.status == 'New'),
                    "In Progress": sum(1 for style in styles if style.status == 'In Progress'),
                    "Completed": sum(1 for style in styles if style.status == 'Completed')
                }
                
                status_data.append({
                    "PO Number": order.po_number,
                    "Buyer": order.buyer.name,
                    "Order Date": order.order_date,
                    "Delivery Date": order.delivery_date,
                    "Order Status": order.status,
                    "Total Styles": len(styles),
                    "New Styles": style_status_counts["New"],
                    "In Progress Styles": style_status_counts["In Progress"],
                    "Completed Styles": style_status_counts["Completed"],
                    "Completion %": f"{(style_status_counts['Completed'] / len(styles) * 100):.1f}%" if styles else "0%"
                })
            
            # Convert to dataframe
            df = pd.DataFrame(status_data)
            
            # Sort by delivery date
            df = df.sort_values('Delivery Date')
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualization
            df_plot = df.copy()
            df_plot['Completion %'] = df_plot['Completion %'].str.rstrip('%').astype(float)
            
            fig = px.scatter(
                df_plot,
                x="Delivery Date",
                y="Completion %",
                size="Total Styles",
                color="Order Status",
                hover_data=["PO Number", "Buyer"],
                title="Order Completion Status vs. Delivery Date",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Buyer-wise Orders":
            # Create buyer-wise order data
            buyer_data = []
            
            for order in orders:
                # Get styles for this order
                styles = get_styles_by_order(order.id)
                
                buyer_data.append({
                    "Buyer": order.buyer.name,
                    "PO Number": order.po_number,
                    "Order Date": order.order_date,
                    "Delivery Date": order.delivery_date,
                    "Status": order.status,
                    "Total Quantity": order.total_quantity,
                    "Styles Count": len(styles)
                })
            
            # Convert to dataframe
            df = pd.DataFrame(buyer_data)
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualization - buyer-wise order quantities
            buyer_totals = df.groupby("Buyer")["Total Quantity"].sum().reset_index()
            
            fig = px.pie(
                buyer_totals,
                values="Total Quantity",
                names="Buyer",
                title="Order Quantities by Buyer",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Delivery Timeline":
            # Create delivery timeline data
            timeline_data = []
            
            for order in orders:
                timeline_data.append({
                    "PO Number": order.po_number,
                    "Buyer": order.buyer.name,
                    "Order Date": order.order_date,
                    "Delivery Date": order.delivery_date,
                    "Days to Delivery": (order.delivery_date - datetime.now().date()).days,
                    "Status": order.status,
                    "Total Quantity": order.total_quantity
                })
            
            # Convert to dataframe
            df = pd.DataFrame(timeline_data)
            
            # Sort by delivery date
            df = df.sort_values('Delivery Date')
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add timeline visualization
            fig = px.timeline(
                df,
                x_start="Order Date",
                x_end="Delivery Date",
                y="PO Number",
                color="Status",
                hover_data=["Buyer", "Total Quantity"],
                title="Order Timeline by PO Number",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            # Update layout
            fig.update_layout(
                height=500,
                template="plotly_dark",
                yaxis=dict(autorange="reversed")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Style Breakdown":
            # Get all styles from all orders
            all_styles = []
            
            for order in orders:
                styles = get_styles_by_order(order.id)
                
                for style in styles:
                    # Parse size breakdown
                    size_breakdown = json.loads(style.size_breakdown) if style.size_breakdown else {}
                    
                    all_styles.append({
                        "PO Number": order.po_number,
                        "Buyer": order.buyer.name,
                        "Style Number": style.style_number,
                        "Description": style.description,
                        "Category": style.category,
                        "Color": style.color,
                        "Status": style.status,
                        "Total Quantity": style.quantity,
                        "Size Breakdown": size_breakdown
                    })
            
            # Convert to dataframe
            df = pd.DataFrame(all_styles)
            
            # Dynamically expand size breakdown into columns
            if not df.empty:
                size_columns = set()
                
                # Find all size columns
                for breakdown in df["Size Breakdown"]:
                    if breakdown:
                        size_columns.update(breakdown.keys())
                
                # Add size columns to the dataframe
                for size in size_columns:
                    df[f"Size {size}"] = df["Size Breakdown"].apply(
                        lambda x: x.get(size, 0) if x else 0
                    )
                
                # Drop the original size breakdown column
                df = df.drop(columns=["Size Breakdown"])
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualizations
            st.subheader("Style Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Category breakdown
                category_counts = df["Category"].value_counts().reset_index()
                category_counts.columns = ["Category", "Count"]
                
                fig = px.pie(
                    category_counts,
                    values="Count",
                    names="Category",
                    title="Styles by Category",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                fig.update_layout(height=300, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Status breakdown
                status_counts = df["Status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                
                fig = px.bar(
                    status_counts,
                    x="Status",
                    y="Count",
                    title="Styles by Status",
                    color="Status",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                fig.update_layout(height=300, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        # Add export options
        export_format = st.radio("Export Format", options=["Excel", "PDF"])
        
        if st.button("Generate Report"):
            if export_format == "Excel":
                # Create Excel file
                excel_data = export_to_excel(df, report_type)
                
                # Download button
                st.download_button(
                    label="Download Excel Report",
                    data=excel_data,
                    file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                # Create PDF file
                pdf_data = export_to_pdf(df, report_type)
                
                # Download button
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_data,
                    file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("No orders match the selected criteria")

def show_material_reports():
    """Display material-related reports"""
    st.subheader("Material Reports")
    
    # Material report options
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Material Status Summary",
            "Material Delivery Timeline",
            "Material by Type",
            "Material Issuance Report"
        ],
        key="material_report_type"
    )
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Get all materials across all styles
    all_materials = []
    for order in orders:
        styles = get_styles_by_order(order.id)
        
        for style in styles:
            materials = get_materials_by_style(style.id)
            
            for material in materials:
                all_materials.append({
                    "material": material,
                    "style": style,
                    "order": order
                })
    
    if not all_materials:
        st.warning("No materials found.")
        return
    
    # Add filter options
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter by material type
        material_types = ["All Types"] + list(set(m["material"].type for m in all_materials))
        selected_type = st.selectbox("Filter by Material Type", material_types, key="material_type_filter")
    
    with col2:
        # Filter by material status
        material_statuses = ["All Statuses"] + list(set(m["material"].status for m in all_materials))
        selected_status = st.selectbox("Filter by Status", material_statuses, key="material_status_filter")
    
    # Apply filters
    filtered_materials = all_materials
    
    if selected_type != "All Types":
        filtered_materials = [m for m in filtered_materials if m["material"].type == selected_type]
    
    if selected_status != "All Statuses":
        filtered_materials = [m for m in filtered_materials if m["material"].status == selected_status]
    
    # Generate report data
    if filtered_materials:
        if report_type == "Material Status Summary":
            # Create material summary data
            material_data = []
            
            for item in filtered_materials:
                material = item["material"]
                style = item["style"]
                order = item["order"]
                
                material_data.append({
                    "Material Name": material.name,
                    "Type": material.type,
                    "Style": style.style_number,
                    "PO Number": order.po_number,
                    "Required Qty": material.required_quantity,
                    "Received Qty": material.received_quantity,
                    "Issued Qty": material.issued_quantity,
                    "Pending Qty": material.required_quantity - material.received_quantity,
                    "Unit": material.unit,
                    "Status": material.status,
                    "PO Number": material.po_number or "",
                    "PO Date": material.po_date.strftime('%Y-%m-%d') if material.po_date else ""
                })
            
            # Convert to dataframe
            df = pd.DataFrame(material_data)
            
            # Sort by status
            df = df.sort_values('Status')
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualization
            status_counts = df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            
            fig = px.pie(
                status_counts,
                values="Count",
                names="Status",
                title="Materials by Status",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            fig.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Material Delivery Timeline":
            # Create delivery timeline data
            timeline_data = []
            
            for item in filtered_materials:
                material = item["material"]
                style = item["style"]
                order = item["order"]
                
                # Only include materials with delivery dates
                if material.expected_delivery or material.actual_delivery:
                    timeline_data.append({
                        "Material Name": material.name,
                        "Type": material.type,
                        "Style": style.style_number,
                        "PO Number": order.po_number,
                        "Expected Delivery": material.expected_delivery,
                        "Actual Delivery": material.actual_delivery,
                        "Status": material.status,
                        "Required Qty": material.required_quantity,
                        "Unit": material.unit,
                        "Delay (days)": (material.actual_delivery - material.expected_delivery).days if (material.actual_delivery and material.expected_delivery) else None
                    })
            
            # Convert to dataframe
            df = pd.DataFrame(timeline_data)
            
            if not df.empty:
                # Sort by expected delivery date
                df = df.sort_values('Expected Delivery')
                
                # Display the report
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Add visualizations
                st.subheader("Delivery Timeline Analysis")
                
                # Create timeline visualization
                fig = go.Figure()
                
                for idx, row in df.iterrows():
                    # Don't include rows without dates
                    if pd.isna(row["Expected Delivery"]):
                        continue
                    
                    # Add expected delivery point
                    fig.add_trace(go.Scatter(
                        x=[row["Expected Delivery"]],
                        y=[f"{row['Material Name']} ({row['Style']})"],
                        mode="markers",
                        name="Expected",
                        marker=dict(color="blue", size=10, symbol="circle"),
                        showlegend=idx == 0
                    ))
                    
                    # Add actual delivery point if available
                    if not pd.isna(row["Actual Delivery"]):
                        delay = row["Delay (days)"]
                        color = "green" if delay <= 0 else "red"
                        
                        fig.add_trace(go.Scatter(
                            x=[row["Actual Delivery"]],
                            y=[f"{row['Material Name']} ({row['Style']})"],
                            mode="markers",
                            name="Actual",
                            marker=dict(color=color, size=10, symbol="diamond"),
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
                delay_data = df[~df["Delay (days)"].isna()].copy()
                
                if not delay_data.empty:
                    st.subheader("Delivery Delay Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Average delay metric
                        avg_delay = delay_data["Delay (days)"].mean()
                        st.metric(
                            "Average Delay", 
                            f"{avg_delay:.1f} days",
                            delta=None
                        )
                    
                    with col2:
                        # On-time delivery percentage
                        on_time = (delay_data["Delay (days)"] <= 0).sum()
                        total = len(delay_data)
                        on_time_pct = (on_time / total) * 100 if total > 0 else 0
                        
                        st.metric(
                            "On-Time Delivery Rate", 
                            f"{on_time_pct:.1f}%",
                            delta=None
                        )
            else:
                st.info("No materials with delivery dates found")
        
        elif report_type == "Material by Type":
            # Create material type data
            type_data = []
            
            for item in filtered_materials:
                material = item["material"]
                style = item["style"]
                order = item["order"]
                
                type_data.append({
                    "Material Name": material.name,
                    "Type": material.type,
                    "Style": style.style_number,
                    "PO Number": order.po_number,
                    "Required Qty": material.required_quantity,
                    "Received Qty": material.received_quantity,
                    "Issued Qty": material.issued_quantity,
                    "Unit": material.unit,
                    "Status": material.status
                })
            
            # Convert to dataframe
            df = pd.DataFrame(type_data)
            
            # Sort by type
            df = df.sort_values('Type')
            
            # Display the report
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add visualizations
            st.subheader("Material Type Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Type breakdown
                type_counts = df["Type"].value_counts().reset_index()
                type_counts.columns = ["Type", "Count"]
                
                fig = px.pie(
                    type_counts,
                    values="Count",
                    names="Type",
                    title="Materials by Type",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                fig.update_layout(height=300, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Required quantity by type
                type_qty = df.groupby("Type")["Required Qty"].sum().reset_index()
                
                fig = px.bar(
                    type_qty,
                    x="Type",
                    y="Required Qty",
                    title="Required Quantity by Material Type",
                    color="Type",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                fig.update_layout(height=300, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Material Issuance Report":
            # Create material issuance data
            issuance_data = []
            
            for item in filtered_materials:
                material = item["material"]
                style = item["style"]
                order = item["order"]
                
                # Only include materials that have been issued
                if material.issued_quantity > 0:
                    issuance_data.append({
                        "Material Name": material.name,
                        "Type": material.type,
                        "Style": style.style_number,
                        "PO Number": order.po_number,
                        "Required Qty": material.required_quantity,
                        "Received Qty": material.received_quantity,
                        "Issued Qty": material.issued_quantity,
                        "Remaining Qty": material.received_quantity - material.issued_quantity,
                        "Unit": material.unit,
                        "Status": material.status,
                        "Issuance %": (material.issued_quantity / material.required_quantity * 100) if material.required_quantity > 0 else 0
                    })
            
            # Convert to dataframe
            df = pd.DataFrame(issuance_data)
            
            if not df.empty:
                # Format issuance percentage
                df["Issuance %"] = df["Issuance %"].apply(lambda x: f"{x:.1f}%")
                
                # Sort by issuance percentage
                df = df.sort_values('Issued Qty', ascending=False)
                
                # Display the report
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Add visualization
                # Convert percentage back to number for plotting
                df["Issuance Pct"] = df["Issuance %"].str.rstrip("%").astype(float)
                
                fig = px.bar(
                    df,
                    x="Material Name",
                    y="Issued Qty",
                    color="Type",
                    hover_data=["Style", "Required Qty", "Received Qty", "Issuance %"],
                    title="Material Issuance Quantities",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                fig.update_layout(height=400, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No issued materials found")
        
        # Add export options
        export_format = st.radio("Export Format", options=["Excel", "PDF"], key="material_export_format")
        
        if st.button("Generate Report", key="material_generate_report"):
            if export_format == "Excel":
                # Create Excel file
                excel_data = export_to_excel(df, report_type)
                
                # Download button
                st.download_button(
                    label="Download Excel Report",
                    data=excel_data,
                    file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="material_download_excel"
                )
            else:
                # Create PDF file
                pdf_data = export_to_pdf(df, report_type)
                
                # Download button
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_data,
                    file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    key="material_download_pdf"
                )
    else:
        st.info("No materials match the selected criteria")

def show_production_reports():
    """Display production-related reports"""
    st.subheader("Production Reports")
    
    # Production report options
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Daily Production Report",
            "Monthly Production Summary",
            "Style-wise Production",
            "Production Efficiency Analysis"
        ],
        key="production_report_type"
    )
    
    # Get all orders for filtering
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Add filter options based on report type
    if report_type == "Daily Production Report":
        # Date selector for daily report
        selected_date = st.date_input("Select Production Date", datetime.now().date(), key="prod_date")
        
        # Get production entries for the selected date
        production_entries = get_production_entries_by_date_range(selected_date, selected_date)
    
    elif report_type == "Monthly Production Summary":
        # Month selector for monthly report
        col1, col2 = st.columns(2)
        
        with col1:
            selected_month = st.selectbox(
                "Select Month",
                options=list(range(1, 13)),
                index=datetime.now().month - 1,
                format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
                key="prod_month"
            )
        
        with col2:
            selected_year = st.selectbox(
                "Select Year",
                options=list(range(datetime.now().year - 2, datetime.now().year + 1)),
                index=2,
                key="prod_year"
            )
        
        # Calculate start and end dates for the selected month
        start_date = datetime(selected_year, selected_month, 1).date()
        if selected_month == 12:
            end_date = datetime(selected_year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(selected_year, selected_month + 1, 1).date() - timedelta(days=1)
        
        # Get production entries for the selected month
        production_entries = get_production_entries_by_date_range(start_date, end_date)
    
    elif report_type == "Style-wise Production":
        # Order and style selector
        col1, col2 = st.columns(2)
        
        with col1:
            # Order selection
            order_options = [f"{order.po_number} - {order.buyer.name}" for order in orders]
            selected_order = st.selectbox("Select Order", order_options, key="prod_order")
            
            # Get the selected order
            po_number = selected_order.split(" - ")[0]
            order = next((o for o in orders if o.po_number == po_number), None)
            
            if order:
                # Get styles for this order
                styles = get_styles_by_order(order.id)
                
                with col2:
                    # Style selection
                    style_options = [f"{style.style_number} - {style.description}" for style in styles]
                    selected_style = st.selectbox("Select Style", style_options, key="prod_style")
                    
                    # Get the selected style
                    style_number = selected_style.split(" - ")[0]
                    style = next((s for s in styles if s.style_number == style_number), None)
                    
                    if style:
                        # Get production entries for this style
                        production_entries = get_production_entries_by_style(style.id)
                    else:
                        production_entries = []
            else:
                production_entries = []
    
    elif report_type == "Production Efficiency Analysis":
        # Date range selector for efficiency analysis
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30), key="eff_start_date")
        
        with col2:
            end_date = st.date_input("End Date", datetime.now().date(), key="eff_end_date")
        
        # Get production entries for the selected date range
        production_entries = get_production_entries_by_date_range(start_date, end_date)
    
    # Generate report data
    if 'production_entries' in locals() and production_entries:
        # Create a DataFrame with the production entries
        production_data = []
        
        for entry in production_entries:
            # Get style and line information
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == entry.style_id).first()
                line = db.query(ProductionLine).filter(ProductionLine.id == entry.line_id).first()
                order = None
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                
                production_data.append({
                    "Date": entry.date,
                    "Style": style.style_number if style else "Unknown",
                    "PO Number": order.po_number if order else "Unknown",
                    "Process": entry.process,
                    "Line": line.name if line else "Unknown",
                    "Quantity": entry.quantity,
                    "Efficiency": entry.efficiency,
                    "Defects": entry.defects,
                    "Delay Reason": entry.delay_reason or "",
                    "Remarks": entry.remarks or ""
                })
            finally:
                db.close()
        
        # Convert to DataFrame
        df = pd.DataFrame(production_data)
        
        if not df.empty:
            if report_type == "Daily Production Report":
                # Sort by line and process
                df = df.sort_values(['Line', 'Process'])
                
                # Format efficiency as percentage
                df["Efficiency"] = df["Efficiency"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
                
                # Display the report
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Add visualizations
                st.subheader("Daily Production Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Process breakdown
                    process_data = df.groupby("Process")["Quantity"].sum().reset_index()
                    
                    fig = px.bar(
                        process_data,
                        x="Process",
                        y="Quantity",
                        title="Production by Process",
                        color="Process",
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    fig.update_layout(height=300, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Line breakdown
                    line_data = df.groupby("Line")["Quantity"].sum().reset_index()
                    
                    fig = px.pie(
                        line_data,
                        values="Quantity",
                        names="Line",
                        title="Production by Line",
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    fig.update_layout(height=300, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
            
            elif report_type == "Monthly Production Summary":
                # Group by date and process
                daily_data = df.groupby(['Date', 'Process'])['Quantity'].sum().reset_index()
                
                # Pivot the data
                pivot_df = daily_data.pivot(index='Date', columns='Process', values='Quantity').reset_index()
                pivot_df = pivot_df.fillna(0)
                
                # Ensure all processes are in the DataFrame
                for process in ['Cutting', 'Stitching', 'Packing', 'Dispatch']:
                    if process not in pivot_df.columns:
                        pivot_df[process] = 0
                
                # Sort by date
                pivot_df = pivot_df.sort_values('Date')
                
                # Display the report
                st.dataframe(pivot_df, use_container_width=True, hide_index=True)
                
                # Add visualizations
                st.subheader("Monthly Production Analysis")
                
                # Create a line chart for daily production
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Cutting'],
                    mode='lines+markers',
                    name='Cutting',
                    line=dict(color='#636EFA', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Stitching'],
                    mode='lines+markers',
                    name='Stitching',
                    line=dict(color='#EF553B', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Packing'],
                    mode='lines+markers',
                    name='Packing',
                    line=dict(color='#00CC96', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Dispatch'],
                    mode='lines+markers',
                    name='Dispatch',
                    line=dict(color='#AB63FA', width=2)
                ))
                
                fig.update_layout(
                    title="Daily Production Trend",
                    xaxis_title="Date",
                    yaxis_title="Units",
                    height=400,
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Monthly summary metrics
                st.subheader("Monthly Production Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_cutting = pivot_df['Cutting'].sum()
                    st.metric("Total Cutting", total_cutting)
                
                with col2:
                    total_stitching = pivot_df['Stitching'].sum()
                    st.metric("Total Stitching", total_stitching)
                
                with col3:
                    total_packing = pivot_df['Packing'].sum()
                    st.metric("Total Packing", total_packing)
                
                with col4:
                    total_dispatch = pivot_df['Dispatch'].sum()
                    st.metric("Total Dispatch", total_dispatch)
            
            elif report_type == "Style-wise Production":
                # Sort by date and process
                df = df.sort_values(['Date', 'Process'])
                
                # Format efficiency as percentage
                df["Efficiency"] = df["Efficiency"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
                
                # Display the report
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Add style information
                if 'style' in locals() and style:
                    st.subheader(f"Style: {style.style_number}")
                    st.write(f"Description: {style.description}")
                    st.write(f"Category: {style.category}")
                    st.write(f"Color: {style.color}")
                    st.write(f"Total Quantity: {style.quantity}")
                
                # Add visualizations
                st.subheader("Style Production Analysis")
                
                # Calculate process totals
                process_totals = df.groupby("Process")["Quantity"].sum().to_dict()
                total_cutting = process_totals.get('Cutting', 0)
                total_stitching = process_totals.get('Stitching', 0)
                total_packing = process_totals.get('Packing', 0)
                total_dispatch = process_totals.get('Dispatch', 0)
                
                # Display style production metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Cutting",
                        value=total_cutting,
                        delta=f"{(total_cutting/style.quantity)*100:.1f}%" if 'style' in locals() and style and style.quantity > 0 else "0%"
                    )
                
                with col2:
                    st.metric(
                        label="Stitching",
                        value=total_stitching,
                        delta=f"{(total_stitching/style.quantity)*100:.1f}%" if 'style' in locals() and style and style.quantity > 0 else "0%"
                    )
                
                with col3:
                    st.metric(
                        label="Packing",
                        value=total_packing,
                        delta=f"{(total_packing/style.quantity)*100:.1f}%" if 'style' in locals() and style and style.quantity > 0 else "0%"
                    )
                
                with col4:
                    st.metric(
                        label="Dispatch",
                        value=total_dispatch,
                        delta=f"{(total_dispatch/style.quantity)*100:.1f}%" if 'style' in locals() and style and style.quantity > 0 else "0%"
                    )
                
                # Create timeline visualization
                # Group by date and process
                timeline_data = df.groupby(['Date', 'Process'])['Quantity'].sum().reset_index()
                
                # Pivot the data
                pivot_df = timeline_data.pivot(index='Date', columns='Process', values='Quantity').reset_index()
                pivot_df = pivot_df.fillna(0)
                
                # Ensure all processes are in the DataFrame
                for process in ['Cutting', 'Stitching', 'Packing', 'Dispatch']:
                    if process not in pivot_df.columns:
                        pivot_df[process] = 0
                
                # Sort by date
                pivot_df = pivot_df.sort_values('Date')
                
                # Create the timeline chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Cutting'],
                    mode='lines+markers',
                    name='Cutting',
                    line=dict(color='#636EFA', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Stitching'],
                    mode='lines+markers',
                    name='Stitching',
                    line=dict(color='#EF553B', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Packing'],
                    mode='lines+markers',
                    name='Packing',
                    line=dict(color='#00CC96', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_df['Date'], 
                    y=pivot_df['Dispatch'],
                    mode='lines+markers',
                    name='Dispatch',
                    line=dict(color='#AB63FA', width=2)
                ))
                
                fig.update_layout(
                    title="Style Production Timeline",
                    xaxis_title="Date",
                    yaxis_title="Units",
                    height=400,
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif report_type == "Production Efficiency Analysis":
                # Filter entries with efficiency data
                efficiency_df = df[df["Efficiency"].notna()].copy()
                
                if not efficiency_df.empty:
                    # Create efficiency metrics
                    avg_efficiency = efficiency_df["Efficiency"].mean()
                    
                    st.metric(
                        label="Average Efficiency",
                        value=f"{avg_efficiency:.1f}%",
                        delta=None
                    )
                    
                    # Display the report
                    efficiency_df["Efficiency"] = efficiency_df["Efficiency"].apply(lambda x: f"{x:.1f}%")
                    st.dataframe(efficiency_df, use_container_width=True, hide_index=True)
                    
                    # Add visualizations
                    st.subheader("Efficiency Analysis")
                    
                    # Convert efficiency back to numeric for analysis
                    df["Efficiency_Num"] = df["Efficiency"]
                    
                    # Line efficiency
                    line_efficiency = df.groupby("Line")["Efficiency_Num"].mean().reset_index()
                    
                    fig = px.bar(
                        line_efficiency,
                        x="Line",
                        y="Efficiency_Num",
                        title="Average Efficiency by Line",
                        color="Line",
                        labels={"Efficiency_Num": "Efficiency (%)"},
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    # Add a target line at 80%
                    fig.add_shape(
                        type="line",
                        x0=-0.5,
                        y0=80,
                        x1=len(line_efficiency)-0.5,
                        y1=80,
                        line=dict(
                            color="white",
                            width=2,
                            dash="dash",
                        )
                    )
                    
                    fig.update_layout(height=400, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Efficiency trend over time
                    if len(efficiency_df["Date"].unique()) > 1:
                        date_efficiency = df.groupby("Date")["Efficiency_Num"].mean().reset_index()
                        
                        fig = px.line(
                            date_efficiency,
                            x="Date",
                            y="Efficiency_Num",
                            title="Efficiency Trend Over Time",
                            markers=True,
                            labels={"Efficiency_Num": "Efficiency (%)"},
                            color_discrete_sequence=['#00CC96']
                        )
                        
                        # Add a target line at 80%
                        fig.add_shape(
                            type="line",
                            x0=date_efficiency["Date"].min(),
                            y0=80,
                            x1=date_efficiency["Date"].max(),
                            y1=80,
                            line=dict(
                                color="white",
                                width=2,
                                dash="dash",
                            )
                        )
                        
                        fig.update_layout(height=400, template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No efficiency data available for the selected period")
            
            # Add export options
            export_format = st.radio("Export Format", options=["Excel", "PDF"], key="prod_export_format")
            
            if st.button("Generate Report", key="prod_generate_report"):
                if export_format == "Excel":
                    # Create Excel file
                    excel_data = export_to_excel(df, report_type)
                    
                    # Download button
                    st.download_button(
                        label="Download Excel Report",
                        data=excel_data,
                        file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="prod_download_excel"
                    )
                else:
                    # Create PDF file
                    pdf_data = export_to_pdf(df, report_type)
                    
                    # Download button
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="prod_download_pdf"
                    )
        else:
            st.info("No production data available for the selected criteria")
    else:
        st.info("No production entries found for the selected criteria")

def show_line_performance_reports():
    """Display line performance reports"""
    st.subheader("Line Performance Reports")
    
    # Line performance report options
    report_type = st.selectbox(
        "Select Report Type",
        options=[
            "Line Efficiency Report",
            "Line Utilization Analysis",
            "Line Capacity vs. Output"
        ],
        key="line_report_type"
    )
    
    # Get all production lines
    production_lines = get_all_production_lines()
    
    if not production_lines:
        st.warning("No production lines defined.")
        return
    
    # Add filter options
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter by line
        line_options = ["All Lines"] + [line.name for line in production_lines]
        selected_line = st.selectbox("Filter by Line", line_options, key="line_filter")
    
    with col2:
        # Date range filter
        date_options = ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom Range"]
        selected_date_range = st.selectbox("Date Range", date_options, key="line_date_range")
    
    # Set date range based on selection
    end_date = datetime.now().date()
    
    if selected_date_range == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    elif selected_date_range == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif selected_date_range == "Last 90 Days":
        start_date = end_date - timedelta(days=90)
    elif selected_date_range == "Custom Range":
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", end_date - timedelta(days=30), key="line_start_date")
        
        with col2:
            end_date = st.date_input("End Date", end_date, key="line_end_date")
    
    # Get production entries for the selected date range
    production_entries = get_production_entries_by_date_range(start_date, end_date)
    
    # Filter by selected line if not "All Lines"
    if selected_line != "All Lines":
        # Find the selected line
        selected_line_obj = next((line for line in production_lines if line.name == selected_line), None)
        
        if selected_line_obj:
            production_entries = [entry for entry in production_entries if entry.line_id == selected_line_obj.id]
    
    # Generate report data
    if production_entries:
        # Create a DataFrame with the production entries
        production_data = []
        
        for entry in production_entries:
            # Get style and line information
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == entry.style_id).first()
                line = db.query(ProductionLine).filter(ProductionLine.id == entry.line_id).first()
                order = None
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                
                production_data.append({
                    "Date": entry.date,
                    "Line": line.name if line else "Unknown",
                    "Line Capacity": line.capacity if line else 0,
                    "Style": style.style_number if style else "Unknown",
                    "PO Number": order.po_number if order else "Unknown",
                    "Process": entry.process,
                    "Quantity": entry.quantity,
                    "Efficiency": entry.efficiency,
                    "Defects": entry.defects,
                    "Delay Reason": entry.delay_reason or ""
                })
            finally:
                db.close()
        
        # Convert to DataFrame
        df = pd.DataFrame(production_data)
        
        if not df.empty:
            if report_type == "Line Efficiency Report":
                # Filter entries with efficiency data
                efficiency_df = df[df["Efficiency"].notna()].copy()
                
                if not efficiency_df.empty:
                    # Format efficiency as percentage for display
                    efficiency_df["Efficiency_Display"] = efficiency_df["Efficiency"].apply(lambda x: f"{x:.1f}%")
                    
                    # Calculate average efficiency by line
                    line_avg_efficiency = efficiency_df.groupby("Line")["Efficiency"].mean().reset_index()
                    line_avg_efficiency["Efficiency_Display"] = line_avg_efficiency["Efficiency"].apply(lambda x: f"{x:.1f}%")
                    
                    # Display summary table
                    st.subheader("Line Efficiency Summary")
                    st.dataframe(
                        line_avg_efficiency[["Line", "Efficiency_Display"]].rename(
                            columns={"Efficiency_Display": "Average Efficiency"}
                        ),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Calculate efficiency by date and line
                    daily_efficiency = efficiency_df.groupby(["Date", "Line"])["Efficiency"].mean().reset_index()
                    
                    # Display the detailed report
                    st.subheader("Daily Line Efficiency")
                    daily_efficiency["Efficiency"] = daily_efficiency["Efficiency"].apply(lambda x: f"{x:.1f}%")
                    st.dataframe(daily_efficiency, use_container_width=True, hide_index=True)
                    
                    # Add visualizations
                    st.subheader("Line Efficiency Analysis")
                    
                    # Line efficiency comparison
                    fig = px.bar(
                        line_avg_efficiency,
                        x="Line",
                        y="Efficiency",
                        title="Average Efficiency by Line",
                        color="Line",
                        labels={"Efficiency": "Efficiency (%)"},
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    # Add a target line at 80%
                    fig.add_shape(
                        type="line",
                        x0=-0.5,
                        y0=80,
                        x1=len(line_avg_efficiency)-0.5,
                        y1=80,
                        line=dict(
                            color="white",
                            width=2,
                            dash="dash",
                        )
                    )
                    
                    fig.update_layout(height=400, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Efficiency trend over time
                    if len(efficiency_df["Date"].unique()) > 1:
                        # Prepare data for time series plot
                        efficiency_df_numeric = efficiency_df.copy()
                        
                        # Create a line chart for each line
                        fig = go.Figure()
                        
                        for line_name in efficiency_df_numeric["Line"].unique():
                            line_data = efficiency_df_numeric[efficiency_df_numeric["Line"] == line_name]
                            line_daily = line_data.groupby("Date")["Efficiency"].mean().reset_index()
                            
                            fig.add_trace(go.Scatter(
                                x=line_daily["Date"],
                                y=line_daily["Efficiency"],
                                mode="lines+markers",
                                name=line_name,
                                line=dict(width=2)
                            ))
                        
                        # Add a target line at 80%
                        fig.add_shape(
                            type="line",
                            x0=efficiency_df_numeric["Date"].min(),
                            y0=80,
                            x1=efficiency_df_numeric["Date"].max(),
                            y1=80,
                            line=dict(
                                color="white",
                                width=2,
                                dash="dash",
                            )
                        )
                        
                        fig.update_layout(
                            title="Efficiency Trend by Line",
                            xaxis_title="Date",
                            yaxis_title="Efficiency (%)",
                            height=400,
                            template="plotly_dark",
                            margin=dict(l=20, r=20, t=40, b=20),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No efficiency data available for the selected criteria")
            
            elif report_type == "Line Utilization Analysis":
                # Calculate daily output by line
                daily_output = df.groupby(["Date", "Line", "Line Capacity"])["Quantity"].sum().reset_index()
                
                # Calculate utilization percentage
                daily_output["Utilization"] = (daily_output["Quantity"] / daily_output["Line Capacity"]) * 100
                daily_output["Utilization"] = daily_output["Utilization"].apply(lambda x: min(x, 100))  # Cap at 100%
                
                # Calculate average utilization by line
                line_avg_utilization = daily_output.groupby("Line")["Utilization"].mean().reset_index()
                line_avg_utilization["Utilization_Display"] = line_avg_utilization["Utilization"].apply(lambda x: f"{x:.1f}%")
                
                # Display summary table
                st.subheader("Line Utilization Summary")
                st.dataframe(
                    line_avg_utilization[["Line", "Utilization_Display"]].rename(
                        columns={"Utilization_Display": "Average Utilization"}
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Format utilization for display
                daily_output["Utilization_Display"] = daily_output["Utilization"].apply(lambda x: f"{x:.1f}%")
                
                # Display the detailed report
                st.subheader("Daily Line Utilization")
                st.dataframe(
                    daily_output[["Date", "Line", "Quantity", "Line Capacity", "Utilization_Display"]].rename(
                        columns={"Utilization_Display": "Utilization"}
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add visualizations
                st.subheader("Line Utilization Analysis")
                
                # Line utilization comparison
                fig = px.bar(
                    line_avg_utilization,
                    x="Line",
                    y="Utilization",
                    title="Average Utilization by Line",
                    color="Line",
                    labels={"Utilization": "Utilization (%)"},
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                
                # Add a target line at 90%
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=90,
                    x1=len(line_avg_utilization)-0.5,
                    y1=90,
                    line=dict(
                        color="white",
                        width=2,
                        dash="dash",
                    )
                )
                
                fig.update_layout(height=400, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
                # Utilization trend over time
                if len(daily_output["Date"].unique()) > 1:
                    # Create a line chart for each line
                    fig = go.Figure()
                    
                    for line_name in daily_output["Line"].unique():
                        line_data = daily_output[daily_output["Line"] == line_name]
                        
                        fig.add_trace(go.Scatter(
                            x=line_data["Date"],
                            y=line_data["Utilization"],
                            mode="lines+markers",
                            name=line_name,
                            line=dict(width=2)
                        ))
                    
                    # Add a target line at 90%
                    fig.add_shape(
                        type="line",
                        x0=daily_output["Date"].min(),
                        y0=90,
                        x1=daily_output["Date"].max(),
                        y1=90,
                        line=dict(
                            color="white",
                            width=2,
                            dash="dash",
                        )
                    )
                    
                    fig.update_layout(
                        title="Utilization Trend by Line",
                        xaxis_title="Date",
                        yaxis_title="Utilization (%)",
                        height=400,
                        template="plotly_dark",
                        margin=dict(l=20, r=20, t=40, b=20),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            elif report_type == "Line Capacity vs. Output":
                # Calculate daily output by line
                daily_output = df.groupby(["Date", "Line", "Line Capacity"])["Quantity"].sum().reset_index()
                
                # Calculate utilization percentage
                daily_output["Utilization"] = (daily_output["Quantity"] / daily_output["Line Capacity"]) * 100
                
                # Display the detailed report
                st.subheader("Daily Capacity vs. Output")
                st.dataframe(
                    daily_output[["Date", "Line", "Quantity", "Line Capacity", "Utilization"]].rename(
                        columns={"Utilization": "Utilization (%)"}
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Add visualizations
                st.subheader("Capacity vs. Output Analysis")
                
                # Capacity vs. Output Comparison
                line_avg_output = daily_output.groupby("Line")[["Quantity", "Line Capacity"]].mean().reset_index()
                
                fig = go.Figure()
                
                # Add capacity bars
                fig.add_trace(go.Bar(
                    x=line_avg_output["Line"],
                    y=line_avg_output["Line Capacity"],
                    name="Capacity",
                    marker_color="#636EFA"
                ))
                
                # Add output bars
                fig.add_trace(go.Bar(
                    x=line_avg_output["Line"],
                    y=line_avg_output["Quantity"],
                    name="Output",
                    marker_color="#EF553B"
                ))
                
                fig.update_layout(
                    title="Average Daily Capacity vs. Output by Line",
                    xaxis_title="Line",
                    yaxis_title="Units",
                    height=400,
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                    barmode='group'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Output Trend Over Time
                if len(daily_output["Date"].unique()) > 1:
                    # Prepare data for heat map
                    pivot_df = daily_output.pivot(index="Date", columns="Line", values="Quantity")
                    
                    # Create heatmap
                    fig = px.imshow(
                        pivot_df.T,
                        labels=dict(x="Date", y="Line", color="Output"),
                        title="Daily Output Heatmap",
                        color_continuous_scale=px.colors.sequential.Viridis
                    )
                    
                    fig.update_layout(height=400, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Add export options
            export_format = st.radio("Export Format", options=["Excel", "PDF"], key="line_export_format")
            
            if st.button("Generate Report", key="line_generate_report"):
                # Prepare export data based on report type
                if report_type == "Line Efficiency Report" and 'efficiency_df' in locals():
                    export_df = efficiency_df
                elif report_type == "Line Utilization Analysis" and 'daily_output' in locals():
                    export_df = daily_output
                elif report_type == "Line Capacity vs. Output" and 'daily_output' in locals():
                    export_df = daily_output
                else:
                    export_df = df
                
                if export_format == "Excel":
                    # Create Excel file
                    excel_data = export_to_excel(export_df, report_type)
                    
                    # Download button
                    st.download_button(
                        label="Download Excel Report",
                        data=excel_data,
                        file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="line_download_excel"
                    )
                else:
                    # Create PDF file
                    pdf_data = export_to_pdf(export_df, report_type)
                    
                    # Download button
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name=f"{report_type.replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="line_download_pdf"
                    )
        else:
            st.info("No production data available for the selected criteria")
    else:
        st.info("No production entries found for the selected criteria")

def show_custom_reports():
    """Display interface for creating custom reports"""
    st.subheader("Custom Reports")
    
    # Select report entities
    entity_type = st.selectbox(
        "Select Data Entity",
        options=[
            "Orders & Styles",
            "Materials",
            "Production",
            "Line Performance"
        ],
        key="custom_entity"
    )
    
    # Add date filter
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30), key="custom_start_date")
    
    with col2:
        end_date = st.date_input("End Date", datetime.now().date(), key="custom_end_date")
    
    # Add entity-specific filters
    if entity_type == "Orders & Styles":
        # Get all buyers
        buyers = get_all_buyers()
        buyer_options = ["All Buyers"] + [buyer.name for buyer in buyers]
        selected_buyer = st.selectbox("Filter by Buyer", buyer_options, key="custom_buyer")
        
        # Status filter
        status_options = ["All Statuses", "New", "In Progress", "Completed", "Cancelled"]
        selected_status = st.selectbox("Filter by Status", status_options, key="custom_status")
    
    elif entity_type == "Materials":
        # Material type filter
        material_types = ["All Types", "Fabric", "Trim", "Accessories"]
        selected_type = st.selectbox("Filter by Material Type", material_types, key="custom_material_type")
        
        # Material status filter
        material_statuses = ["All Statuses", "Pending", "Ordered", "Received", "Issued"]
        selected_material_status = st.selectbox("Filter by Status", material_statuses, key="custom_material_status")
    
    elif entity_type == "Production":
        # Process filter
        process_options = ["All Processes", "Cutting", "Stitching", "Packing", "Dispatch"]
        selected_process = st.selectbox("Filter by Process", process_options, key="custom_process")
        
        # Get all production lines
        production_lines = get_all_production_lines()
        line_options = ["All Lines"] + [line.name for line in production_lines]
        selected_line = st.selectbox("Filter by Line", line_options, key="custom_line")
    
    # Select fields to include
    st.subheader("Select Fields to Include")
    
    if entity_type == "Orders & Styles":
        # Order fields
        st.write("Order Fields")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_po = st.checkbox("PO Number", value=True)
            include_buyer = st.checkbox("Buyer", value=True)
        
        with col2:
            include_order_date = st.checkbox("Order Date", value=True)
            include_delivery_date = st.checkbox("Delivery Date", value=True)
        
        with col3:
            include_order_status = st.checkbox("Order Status", value=True)
            include_order_quantity = st.checkbox("Order Quantity", value=True)
        
        # Style fields
        st.write("Style Fields")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_style_number = st.checkbox("Style Number", value=True)
            include_description = st.checkbox("Description", value=False)
        
        with col2:
            include_category = st.checkbox("Category", value=True)
            include_color = st.checkbox("Color", value=True)
        
        with col3:
            include_style_status = st.checkbox("Style Status", value=True)
            include_size_breakdown = st.checkbox("Size Breakdown", value=False)
    
    elif entity_type == "Materials":
        # Material fields
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_material_name = st.checkbox("Material Name", value=True)
            include_material_type = st.checkbox("Material Type", value=True)
            include_style = st.checkbox("Style", value=True)
        
        with col2:
            include_required_qty = st.checkbox("Required Quantity", value=True)
            include_received_qty = st.checkbox("Received Quantity", value=True)
            include_issued_qty = st.checkbox("Issued Quantity", value=True)
        
        with col3:
            include_material_status = st.checkbox("Material Status", value=True)
            include_po_info = st.checkbox("PO Information", value=False)
            include_delivery_dates = st.checkbox("Delivery Dates", value=False)
    
    elif entity_type == "Production":
        # Production fields
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_date = st.checkbox("Date", value=True)
            include_prod_style = st.checkbox("Style", value=True)
            include_process = st.checkbox("Process", value=True)
        
        with col2:
            include_line = st.checkbox("Line", value=True)
            include_quantity = st.checkbox("Quantity", value=True)
            include_efficiency = st.checkbox("Efficiency", value=True)
        
        with col3:
            include_defects = st.checkbox("Defects", value=False)
            include_delay = st.checkbox("Delay Reason", value=False)
            include_remarks = st.checkbox("Remarks", value=False)
    
    elif entity_type == "Line Performance":
        # Line performance fields
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_perf_date = st.checkbox("Date", value=True)
            include_perf_line = st.checkbox("Line", value=True)
        
        with col2:
            include_capacity = st.checkbox("Capacity", value=True)
            include_output = st.checkbox("Output", value=True)
        
        with col3:
            include_utilization = st.checkbox("Utilization", value=True)
            include_perf_efficiency = st.checkbox("Efficiency", value=True)
    
    # Select aggregation options
    st.subheader("Aggregation Options")
    
    aggregation_options = ["None", "Daily", "Weekly", "Monthly"]
    selected_aggregation = st.selectbox("Aggregate Data By", aggregation_options, key="custom_aggregation")
    
    if selected_aggregation != "None":
        # Select aggregation functions
        st.write("Select Aggregation Functions")
        
        agg_functions = ["Sum", "Average", "Min", "Max", "Count"]
        selected_agg_functions = st.multiselect("Aggregation Functions", agg_functions, default=["Sum"])
    
    # Generate report button
    if st.button("Generate Custom Report", type="primary", key="generate_custom_report"):
        # This would normally query the database and generate the report
        # For this prototype, we'll display a placeholder
        
        st.info("Custom report generation would go here. This is a placeholder for the actual implementation.")
        
        # Example of data structure for the report
        custom_data = pd.DataFrame({
            "Column1": [1, 2, 3, 4, 5],
            "Column2": ["A", "B", "C", "D", "E"],
            "Column3": [10, 20, 30, 40, 50]
        })
        
        # Display placeholder data
        st.dataframe(custom_data, use_container_width=True, hide_index=True)
        
        # Export options
        st.subheader("Export Options")
        
        export_format = st.radio("Export Format", options=["Excel", "PDF"], key="custom_export_format")
        
        if export_format == "Excel":
            # Create Excel file
            excel_data = export_to_excel(custom_data, "Custom Report")
            
            # Download button
            st.download_button(
                label="Download Excel Report",
                data=excel_data,
                file_name=f"Custom_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="custom_download_excel"
            )
        else:
            # Create PDF file
            pdf_data = export_to_pdf(custom_data, "Custom Report")
            
            # Download button
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=f"Custom_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="custom_download_pdf"
            )

# Helper functions for export
def export_to_excel(df, report_title):
    """Export a dataframe to Excel"""
    output = io.BytesIO()
    
    # Create a workbook
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(report_title[:31])  # Excel worksheet names are limited to 31 chars
    
    # Add a bold format
    bold = workbook.add_format({'bold': True})
    
    # Write the header
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, bold)
    
    # Write the data
    for row_num, row in enumerate(df.values):
        for col_num, value in enumerate(row):
            worksheet.write(row_num + 1, col_num, value)
    
    # Close the workbook
    workbook.close()
    
    # Get the output data
    data = output.getvalue()
    
    return data

def export_to_pdf(df, report_title):
    """Export a dataframe to PDF"""
    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", "B", 16)
    
    # Add title
    pdf.cell(200, 10, txt=report_title, ln=True, align="C")
    
    # Add date
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    
    # Create a table for the data
    pdf.set_font("Arial", "B", 12)
    
    # Calculate column width (evenly distributed)
    col_width = 190 / len(df.columns)
    
    # Add header
    for col in df.columns:
        pdf.cell(col_width, 10, txt=str(col), border=1, align="C")
    pdf.ln()
    
    # Add rows
    pdf.set_font("Arial", "", 10)
    for _, row in df.iterrows():
        for cell in row:
            pdf.cell(col_width, 10, txt=str(cell), border=1, align="C")
        pdf.ln()
    
    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin1")