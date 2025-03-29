import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import tempfile
import os

from database import get_db_session, Order, Style, ProductionEntry, ProductionLine
from db_operations import (
    get_all_orders, get_styles_by_order, get_production_entries_by_style,
    get_production_entries_by_date_range, add_production_entry,
    get_all_production_lines, import_production_from_excel
)

def show_production_timeline():
    """Display the production timeline interface"""
    st.title("⏱ Production Timeline")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Daily Production", 
        "📈 Monthly Overview", 
        "🔍 Style Tracking",
        "📥 Import/Export"
    ])
    
    with tab1:
        show_daily_production()
    
    with tab2:
        show_monthly_overview()
    
    with tab3:
        show_style_tracking()
    
    with tab4:
        show_production_import_export()

def show_daily_production():
    """Display daily production data and entry form"""
    st.subheader("Daily Production")
    
    # Create a date selector for the production day
    selected_date = st.date_input("Select Production Date", datetime.now().date())
    
    # Get production data for the selected date
    production_entries = get_production_entries_by_date_range(selected_date, selected_date)
    
    # Get all production lines
    production_lines = get_all_production_lines()
    
    # Get all active styles
    active_styles = []
    db = get_db_session()
    try:
        # Get styles that are in progress
        styles = db.query(Style).filter(Style.status == "In Progress").all()
        active_styles = styles
        
        # Also get styles from orders that are in progress
        orders = db.query(Order).filter(Order.status == "In Progress").all()
        for order in orders:
            styles = db.query(Style).filter(Style.order_id == order.id).all()
            for style in styles:
                if style not in active_styles:
                    active_styles.append(style)
    finally:
        db.close()
    
    # Create metrics for the day's production
    if production_entries:
        # Calculate total production by process
        total_cutting = sum(entry.quantity for entry in production_entries if entry.process == 'Cutting')
        total_stitching = sum(entry.quantity for entry in production_entries if entry.process == 'Stitching')
        total_packing = sum(entry.quantity for entry in production_entries if entry.process == 'Packing')
        total_dispatch = sum(entry.quantity for entry in production_entries if entry.process == 'Dispatch')
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Cutting",
                value=total_cutting,
                delta=None
            )
        
        with col2:
            st.metric(
                label="Stitching",
                value=total_stitching,
                delta=None
            )
        
        with col3:
            st.metric(
                label="Packing",
                value=total_packing,
                delta=None
            )
        
        with col4:
            st.metric(
                label="Dispatch",
                value=total_dispatch,
                delta=None
            )
        
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
                    "id": entry.id,
                    "Date": entry.date,
                    "Style": style.style_number if style else "Unknown",
                    "PO Number": order.po_number if order else "Unknown",
                    "Process": entry.process,
                    "Line": line.name if line else "Unknown",
                    "Quantity": entry.quantity,
                    "Efficiency": f"{entry.efficiency:.1f}%" if entry.efficiency else "N/A",
                    "Defects": entry.defects,
                    "Delay Reason": entry.delay_reason or "",
                    "Remarks": entry.remarks or ""
                })
            finally:
                db.close()
        
        # Convert to DataFrame
        df = pd.DataFrame(production_data)
        
        # Display the production data in a table
        st.dataframe(
            df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )
        
        # Create visualization of the day's production
        st.subheader("Daily Production Visualization")
        
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
        fig.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # Line efficiency comparison if there's efficiency data
        if "Efficiency" in df.columns and df["Efficiency"].any() and df["Efficiency"].iloc[0] != "N/A":
            # Convert efficiency from string to number
            df["Efficiency_Value"] = df["Efficiency"].str.rstrip("%").astype(float)
            
            line_efficiency = df.groupby("Line")["Efficiency_Value"].mean().reset_index()
            
            fig = px.bar(
                line_efficiency,
                x="Line",
                y="Efficiency_Value",
                title="Line Efficiency",
                color="Line",
                labels={"Efficiency_Value": "Efficiency (%)"},
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
            
            fig.update_layout(height=350, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No production entries for {selected_date}")
    
    # Form to add new production entry
    st.divider()
    st.subheader("Add Production Entry")
    
    if not active_styles:
        st.warning("No active styles found. Please activate styles in Order & Style Management.")
        return
    
    if not production_lines:
        st.warning("No production lines defined. Please add production lines first.")
        return
    
    with st.form("add_production_entry"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Select style
            style_options = [f"{style.style_number} - {style.description}" for style in active_styles]
            selected_style = st.selectbox("Style", style_options)
            
            # Get the selected style
            style_number = selected_style.split(" - ")[0]
            selected_style_obj = next((s for s in active_styles if s.style_number == style_number), None)
        
        with col2:
            # Select production line
            line_options = [f"{line.name} (Capacity: {line.capacity})" for line in production_lines]
            selected_line = st.selectbox("Production Line", line_options)
            
            # Get the selected line
            line_name = selected_line.split(" (")[0]
            selected_line_obj = next((l for l in production_lines if l.name == line_name), None)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Select process
            process_options = ["Cutting", "Stitching", "Packing", "Dispatch"]
            selected_process = st.selectbox("Process", process_options)
        
        with col2:
            # Enter quantity
            quantity = st.number_input("Quantity", min_value=1, value=100)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enter efficiency (optional)
            efficiency = st.number_input("Efficiency (%)", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
        
        with col2:
            # Enter defects (optional)
            defects = st.number_input("Defects", min_value=0, value=0)
        
        # Enter delay reason (if any)
        delay_reason = st.text_input("Delay Reason (if any)")
        
        # Enter remarks (optional)
        remarks = st.text_area("Remarks")
        
        # Submit button
        submit_entry = st.form_submit_button("Add Production Entry")
        
        if submit_entry and selected_style_obj and selected_line_obj:
            # Add the production entry
            success = add_production_entry(
                selected_date,
                selected_style_obj.id,
                selected_line_obj.id,
                selected_process,
                quantity,
                efficiency,
                defects,
                delay_reason,
                remarks
            )
            
            if success:
                st.success(f"Production entry added successfully")
                st.rerun()
            else:
                st.error("Failed to add production entry")

def show_monthly_overview():
    """Display monthly production overview and analytics"""
    st.subheader("Monthly Production Overview")
    
    # Create month selector
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_month = st.selectbox(
            "Select Month",
            options=list(range(1, 13)),
            index=current_month - 1,
            format_func=lambda x: datetime(2000, x, 1).strftime('%B')
        )
    
    with col2:
        selected_year = st.selectbox(
            "Select Year",
            options=list(range(current_year - 2, current_year + 1)),
            index=2
        )
    
    # Calculate start and end dates for the selected month
    start_date = datetime(selected_year, selected_month, 1).date()
    if selected_month == 12:
        end_date = datetime(selected_year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(selected_year, selected_month + 1, 1).date() - timedelta(days=1)
    
    # Get production entries for the selected month
    production_entries = get_production_entries_by_date_range(start_date, end_date)
    
    if production_entries:
        # Create summary metrics for the month
        total_cutting = sum(entry.quantity for entry in production_entries if entry.process == 'Cutting')
        total_stitching = sum(entry.quantity for entry in production_entries if entry.process == 'Stitching')
        total_packing = sum(entry.quantity for entry in production_entries if entry.process == 'Packing')
        total_dispatch = sum(entry.quantity for entry in production_entries if entry.process == 'Dispatch')
        
        # Calculate average efficiency
        efficiencies = [entry.efficiency for entry in production_entries if entry.efficiency is not None]
        avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Cutting",
                value=total_cutting,
                delta=None
            )
        
        with col2:
            st.metric(
                label="Stitching",
                value=total_stitching,
                delta=None
            )
        
        with col3:
            st.metric(
                label="Packing",
                value=total_packing,
                delta=None
            )
        
        with col4:
            st.metric(
                label="Dispatch",
                value=total_dispatch,
                delta=None
            )
        
        with col5:
            st.metric(
                label="Avg. Efficiency",
                value=f"{avg_efficiency:.1f}%",
                delta=None
            )
        
        # Create a DataFrame for daily production in the month
        daily_production = {}
        current_date = start_date
        while current_date <= end_date:
            daily_entries = [entry for entry in production_entries if entry.date == current_date]
            
            daily_production[current_date.strftime('%Y-%m-%d')] = {
                'date': current_date,
                'Cutting': sum(entry.quantity for entry in daily_entries if entry.process == 'Cutting'),
                'Stitching': sum(entry.quantity for entry in daily_entries if entry.process == 'Stitching'),
                'Packing': sum(entry.quantity for entry in daily_entries if entry.process == 'Packing'),
                'Dispatch': sum(entry.quantity for entry in daily_entries if entry.process == 'Dispatch')
            }
            
            current_date += timedelta(days=1)
        
        # Convert to DataFrame
        daily_df = pd.DataFrame.from_dict(daily_production, orient='index')
        
        # Create a daily production chart
        st.subheader("Daily Production Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_df['date'], 
            y=daily_df['Cutting'],
            mode='lines+markers',
            name='Cutting',
            line=dict(color='#636EFA', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_df['date'], 
            y=daily_df['Stitching'],
            mode='lines+markers',
            name='Stitching',
            line=dict(color='#EF553B', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_df['date'], 
            y=daily_df['Packing'],
            mode='lines+markers',
            name='Packing',
            line=dict(color='#00CC96', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_df['date'], 
            y=daily_df['Dispatch'],
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
        
        # Create production data by style and by line
        st.subheader("Production Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Production by style
            style_production = {}
            
            for entry in production_entries:
                db = get_db_session()
                try:
                    style = db.query(Style).filter(Style.id == entry.style_id).first()
                    if style:
                        if style.style_number not in style_production:
                            style_production[style.style_number] = {
                                'Cutting': 0,
                                'Stitching': 0,
                                'Packing': 0,
                                'Dispatch': 0
                            }
                        
                        style_production[style.style_number][entry.process] += entry.quantity
                finally:
                    db.close()
            
            # Convert to DataFrame
            style_df = pd.DataFrame.from_dict(style_production, orient='index')
            style_df['Style'] = style_df.index
            
            # Create a grouped bar chart
            fig = px.bar(
                style_df,
                x='Style',
                y=['Cutting', 'Stitching', 'Packing', 'Dispatch'],
                title="Production by Style",
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=350, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Production by line
            line_production = {}
            
            for entry in production_entries:
                db = get_db_session()
                try:
                    line = db.query(ProductionLine).filter(ProductionLine.id == entry.line_id).first()
                    if line:
                        if line.name not in line_production:
                            line_production[line.name] = 0
                        
                        line_production[line.name] += entry.quantity
                finally:
                    db.close()
            
            # Convert to DataFrame
            line_df = pd.DataFrame(list(line_production.items()), columns=['Line', 'Quantity'])
            
            # Create a pie chart
            fig = px.pie(
                line_df,
                values='Quantity',
                names='Line',
                title="Production by Line",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig.update_layout(height=350, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        # Efficiency analysis
        st.subheader("Efficiency Analysis")
        
        # Create data for line efficiency over time
        line_efficiency = {}
        
        for entry in production_entries:
            if entry.efficiency is not None:
                db = get_db_session()
                try:
                    line = db.query(ProductionLine).filter(ProductionLine.id == entry.line_id).first()
                    if line:
                        date_str = entry.date.strftime('%Y-%m-%d')
                        if line.name not in line_efficiency:
                            line_efficiency[line.name] = {}
                        
                        if date_str not in line_efficiency[line.name]:
                            line_efficiency[line.name][date_str] = {
                                'efficiencies': [],
                                'date': entry.date
                            }
                        
                        line_efficiency[line.name][date_str]['efficiencies'].append(entry.efficiency)
                finally:
                    db.close()
        
        # Calculate average efficiency for each line and date
        efficiency_data = []
        
        for line_name, dates in line_efficiency.items():
            for date_str, data in dates.items():
                avg_eff = sum(data['efficiencies']) / len(data['efficiencies'])
                efficiency_data.append({
                    'Line': line_name,
                    'Date': data['date'],
                    'Efficiency': avg_eff
                })
        
        # Convert to DataFrame
        efficiency_df = pd.DataFrame(efficiency_data)
        
        if not efficiency_df.empty:
            # Create a line chart for efficiency trends
            fig = px.line(
                efficiency_df,
                x='Date',
                y='Efficiency',
                color='Line',
                title="Line Efficiency Trends",
                markers=True,
                labels={'Efficiency': 'Efficiency (%)'},
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            # Add a target line at 80%
            fig.add_shape(
                type="line",
                x0=start_date,
                y0=80,
                x1=end_date,
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
        st.info(f"No production entries found for {datetime(selected_year, selected_month, 1).strftime('%B %Y')}")

def show_style_tracking():
    """Display style-specific production tracking"""
    st.subheader("Style Production Tracking")
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available.")
        return
    
    # Create filter for order selection
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
                # Create style selection
                style_options = [f"{style.style_number} - {style.description}" for style in styles]
                selected_style = st.selectbox("Select Style", style_options)
                
                if selected_style:
                    # Get the selected style
                    style_number = selected_style.split(" - ")[0]
                    style = next((s for s in styles if s.style_number == style_number), None)
                    
                    if style:
                        # Display style info
                        st.write(f"### Style: {style.style_number}")
                        st.write(f"Description: {style.description}")
                        st.write(f"Category: {style.category}")
                        st.write(f"Color: {style.color}")
                        st.write(f"Status: {style.status}")
                        
                        # Parse size breakdown
                        size_breakdown = json.loads(style.size_breakdown) if style.size_breakdown else {}
                        
                        # Display size breakdown
                        if size_breakdown:
                            st.subheader("Size Breakdown")
                            
                            # Create size breakdown chart
                            sizes = list(size_breakdown.keys())
                            quantities = list(size_breakdown.values())
                            
                            fig = px.bar(
                                x=sizes,
                                y=quantities,
                                title="Size Breakdown",
                                labels={'x': 'Size', 'y': 'Quantity'},
                                color_discrete_sequence=['#00CC96']
                            )
                            fig.update_layout(height=300, template="plotly_dark")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Get production entries for this style
                        production_entries = get_production_entries_by_style(style.id)
                        
                        if production_entries:
                            # Create a DataFrame for the production entries
                            production_data = []
                            
                            for entry in production_entries:
                                db = get_db_session()
                                try:
                                    line = db.query(ProductionLine).filter(ProductionLine.id == entry.line_id).first()
                                    
                                    production_data.append({
                                        "Date": entry.date,
                                        "Process": entry.process,
                                        "Line": line.name if line else "Unknown",
                                        "Quantity": entry.quantity,
                                        "Efficiency": f"{entry.efficiency:.1f}%" if entry.efficiency else "N/A",
                                        "Defects": entry.defects,
                                        "Delay Reason": entry.delay_reason or ""
                                    })
                                finally:
                                    db.close()
                            
                            # Convert to DataFrame
                            df = pd.DataFrame(production_data)
                            
                            # Sort by date
                            df = df.sort_values('Date')
                            
                            # Calculate process totals
                            cutting_total = sum(entry.quantity for entry in production_entries if entry.process == 'Cutting')
                            stitching_total = sum(entry.quantity for entry in production_entries if entry.process == 'Stitching')
                            packing_total = sum(entry.quantity for entry in production_entries if entry.process == 'Packing')
                            dispatch_total = sum(entry.quantity for entry in production_entries if entry.process == 'Dispatch')
                            
                            # Display style production metrics
                            st.subheader("Production Progress")
                            
                            col1, col2, col3, col4, col5 = st.columns(5)
                            
                            with col1:
                                st.metric(
                                    label="Total",
                                    value=style.quantity,
                                    delta=None
                                )
                            
                            with col2:
                                st.metric(
                                    label="Cutting",
                                    value=cutting_total,
                                    delta=f"{(cutting_total/style.quantity)*100:.1f}%" if style.quantity > 0 else "0%"
                                )
                            
                            with col3:
                                st.metric(
                                    label="Stitching",
                                    value=stitching_total,
                                    delta=f"{(stitching_total/style.quantity)*100:.1f}%" if style.quantity > 0 else "0%"
                                )
                            
                            with col4:
                                st.metric(
                                    label="Packing",
                                    value=packing_total,
                                    delta=f"{(packing_total/style.quantity)*100:.1f}%" if style.quantity > 0 else "0%"
                                )
                            
                            with col5:
                                st.metric(
                                    label="Dispatch",
                                    value=dispatch_total,
                                    delta=f"{(dispatch_total/style.quantity)*100:.1f}%" if style.quantity > 0 else "0%"
                                )
                            
                            # Create progress bars
                            st.subheader("Production Process Progress")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Cutting progress
                                cutting_pct = (cutting_total / style.quantity) * 100 if style.quantity > 0 else 0
                                st.progress(min(cutting_pct / 100, 1.0), text=f"Cutting: {cutting_pct:.1f}%")
                                
                                # Stitching progress
                                stitching_pct = (stitching_total / style.quantity) * 100 if style.quantity > 0 else 0
                                st.progress(min(stitching_pct / 100, 1.0), text=f"Stitching: {stitching_pct:.1f}%")
                            
                            with col2:
                                # Packing progress
                                packing_pct = (packing_total / style.quantity) * 100 if style.quantity > 0 else 0
                                st.progress(min(packing_pct / 100, 1.0), text=f"Packing: {packing_pct:.1f}%")
                                
                                # Dispatch progress
                                dispatch_pct = (dispatch_total / style.quantity) * 100 if style.quantity > 0 else 0
                                st.progress(min(dispatch_pct / 100, 1.0), text=f"Dispatch: {dispatch_pct:.1f}%")
                            
                            # Display production entries
                            st.subheader("Production Entries")
                            
                            # Display the production data
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # Create a timeline visualization
                            st.subheader("Production Timeline")
                            
                            # Prepare data for timeline visualization
                            timeline_df = df.copy()
                            
                            # Group by date and process
                            timeline_data = timeline_df.groupby(['Date', 'Process'])['Quantity'].sum().reset_index()
                            
                            # Pivot the data
                            pivot_df = timeline_data.pivot(index='Date', columns='Process', values='Quantity').reset_index()
                            pivot_df = pivot_df.fillna(0)
                            
                            # Ensure all processes are in the DataFrame
                            for process in ['Cutting', 'Stitching', 'Packing', 'Dispatch']:
                                if process not in pivot_df.columns:
                                    pivot_df[process] = 0
                            
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
                                title="Production Timeline",
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
                            
                            # Calculate WIP (Work in Progress)
                            wip = cutting_total - stitching_total
                            stitch_wip = stitching_total - packing_total
                            pack_wip = packing_total - dispatch_total
                            
                            # Display WIP metrics
                            st.subheader("Work in Progress (WIP)")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(
                                    label="Cut WIP",
                                    value=wip,
                                    delta=None
                                )
                            
                            with col2:
                                st.metric(
                                    label="Stitch WIP",
                                    value=stitch_wip,
                                    delta=None
                                )
                            
                            with col3:
                                st.metric(
                                    label="Pack WIP",
                                    value=pack_wip,
                                    delta=None
                                )
                        else:
                            st.info("No production entries found for this style")
                    else:
                        st.error("Style not found")
            else:
                st.warning("No styles found for this order")
        else:
            st.error("Order not found")

def show_production_import_export():
    """Display the production import/export interface"""
    st.subheader("Import/Export Production Data")
    
    # Create tabs for import and export
    tab1, tab2 = st.tabs(["📥 Import Production Data", "📤 Export Production Data"])
    
    with tab1:
        st.subheader("Import Production Data from Excel")
        
        # Upload file
        uploaded_file = st.file_uploader(
            "Upload Excel file with Production Data",
            type=["xlsx", "xls"],
            help="Excel file should have a sheet named 'Production'"
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
                production_df = pd.read_excel(temp_path, sheet_name='Production')
                
                # Show preview
                st.subheader("Production Data Preview")
                st.dataframe(production_df.head(), use_container_width=True)
                
                # Import button
                if st.button("Import Production Data", type="primary"):
                    success, message = import_production_from_excel(temp_path)
                    
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
        st.subheader("Export Production Data to Excel")
        
        # Export options
        export_type = st.selectbox(
            "Select what to export",
            options=["Daily Production", "Monthly Production", "Style Production"]
        )
        
        if export_type == "Daily Production":
            # Select date to export
            export_date = st.date_input("Select Date", datetime.now().date())
        
        elif export_type == "Monthly Production":
            # Select month to export
            col1, col2 = st.columns(2)
            
            with col1:
                export_month = st.selectbox(
                    "Select Month",
                    options=list(range(1, 13)),
                    index=datetime.now().month - 1,
                    format_func=lambda x: datetime(2000, x, 1).strftime('%B')
                )
            
            with col2:
                export_year = st.selectbox(
                    "Select Year",
                    options=list(range(datetime.now().year - 2, datetime.now().year + 1)),
                    index=2
                )
        
        elif export_type == "Style Production":
            # Select order and style to export
            orders = get_all_orders()
            if orders:
                order_options = [f"{order.po_number} - {order.buyer.name}" for order in orders]
                export_order = st.selectbox("Select Order", order_options)
                
                if export_order:
                    # Get the selected order
                    po_number = export_order.split(" - ")[0]
                    order = next((o for o in orders if o.po_number == po_number), None)
                    
                    if order:
                        # Get styles for this order
                        styles = get_styles_by_order(order.id)
                        
                        if styles:
                            # Create style selection
                            style_options = [f"{style.style_number} - {style.description}" for style in styles]
                            export_style = st.selectbox("Select Style", style_options)
        
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
                file_name="production_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                disabled=True  # Disabled for now since we're not generating a real file
            )