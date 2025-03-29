import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

from database import get_db_session, Order, Style, ProductionLine, LineAllocation
from db_operations import (
    get_all_orders, get_styles_by_order, get_all_production_lines,
    get_allocations_by_line, allocate_style_to_line
)

def show_line_plan():
    """Display the line planning interface for production scheduling"""
    st.title("📅 Line Plan Interface")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs([
        "📋 Line Planning View", 
        "🔧 Line Setup & Allocation"
    ])
    
    with tab1:
        show_line_planning_view()
    
    with tab2:
        show_line_setup()

def show_line_planning_view():
    """Display the line planning view with interactive controls"""
    st.subheader("Line Planning Calendar")
    
    # Get all production lines
    production_lines = get_all_production_lines()
    
    if not production_lines:
        st.warning("No production lines defined. Please add production lines first.")
        return
    
    # Create date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date())
    
    with col2:
        # Default to 4 weeks view
        end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=27))
    
    # Calculate the number of days in the range
    days_range = (end_date - start_date).days + 1
    
    # Check if range is too large
    if days_range > 90:
        st.warning("Date range too large. Please select a range of 90 days or less.")
        return
    
    # Get line allocations for all lines
    line_allocations = []
    line_data = {}
    
    for line in production_lines:
        allocations = get_allocations_by_line(line.id)
        
        # Filter allocations within the date range
        filtered_allocations = [
            alloc for alloc in allocations 
            if (alloc.end_date >= start_date and alloc.start_date <= end_date)
        ]
        
        line_allocations.extend(filtered_allocations)
        
        # Store line data for each allocation
        for alloc in filtered_allocations:
            alloc.line_name = line.name
            alloc.line_capacity = line.capacity
    
    # Create a calendar-style visualization
    st.subheader("Line Allocation Calendar")
    
    if line_allocations:
        # Create a calendar dataframe
        # First, create date range
        dates = [start_date + timedelta(days=i) for i in range(days_range)]
        
        # Create the basic calendar structure
        calendar_data = {}
        
        for line in production_lines:
            calendar_data[line.name] = {date.strftime('%Y-%m-%d'): '' for date in dates}
        
        # Fill in allocation data
        for alloc in line_allocations:
            # Get style information
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == alloc.style_id).first()
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                    
                    # Determine date range for this allocation
                    alloc_start = max(alloc.start_date, start_date)
                    alloc_end = min(alloc.end_date, end_date)
                    
                    # Fill in the calendar for these dates
                    current_date = alloc_start
                    while current_date <= alloc_end:
                        date_str = current_date.strftime('%Y-%m-%d')
                        
                        # Create allocation info
                        allocation_info = f"{style.style_number} ({order.po_number if order else 'Unknown'})"
                        
                        calendar_data[alloc.line_name][date_str] = allocation_info
                        
                        current_date += timedelta(days=1)
            finally:
                db.close()
        
        # Create a dataframe for display
        calendar_rows = []
        
        for line_name, line_dates in calendar_data.items():
            row = {'Line': line_name}
            row.update(line_dates)
            calendar_rows.append(row)
        
        calendar_df = pd.DataFrame(calendar_rows)
        
        # Display the calendar
        # Only show a subset of dates if there are too many
        if days_range > 14:
            # Show week headers
            week_headers = []
            current_date = start_date
            week_num = 1
            
            while current_date <= end_date:
                # Get the week start and end
                week_start = current_date
                week_end = min(current_date + timedelta(days=6), end_date)
                
                # Create week header
                week_header = f"Week {week_num}: {week_start.strftime('%d %b')} - {week_end.strftime('%d %b')}"
                week_headers.append(week_header)
                
                # Move to next week
                current_date = week_end + timedelta(days=1)
                week_num += 1
            
            # Display week headers
            st.write(" | ".join(week_headers))
            
            # Use an expander for the full calendar
            with st.expander("View Full Calendar"):
                st.dataframe(calendar_df, use_container_width=True, hide_index=True)
            
            # Create weekly views
            current_date = start_date
            week_num = 1
            
            while current_date <= end_date:
                # Get the week dates
                week_dates = []
                week_start = current_date
                for i in range(7):
                    if current_date + timedelta(days=i) <= end_date:
                        week_dates.append((current_date + timedelta(days=i)).strftime('%Y-%m-%d'))
                
                # Create week dataframe
                week_columns = ['Line'] + week_dates
                week_df = calendar_df[week_columns] if all(col in calendar_df.columns for col in week_columns) else None
                
                if week_df is not None:
                    # Display week dataframe
                    st.subheader(f"Week {week_num}: {week_start.strftime('%d %b')} to {(week_start + timedelta(days=len(week_dates)-1)).strftime('%d %b')}")
                    st.dataframe(week_df, use_container_width=True, hide_index=True)
                
                # Move to next week
                current_date = current_date + timedelta(days=7)
                week_num += 1
        else:
            # If date range is small enough, just show the full calendar
            st.dataframe(calendar_df, use_container_width=True, hide_index=True)
        
        # Create a Gantt chart visualization
        st.subheader("Line Allocation Gantt Chart")
        
        # Prepare data for Gantt chart
        gantt_data = []
        
        for alloc in line_allocations:
            db = get_db_session()
            try:
                style = db.query(Style).filter(Style.id == alloc.style_id).first()
                if style:
                    order = db.query(Order).filter(Order.id == style.order_id).first()
                    
                    gantt_data.append({
                        'Line': alloc.line_name,
                        'Style': style.style_number,
                        'PO': order.po_number if order else 'Unknown',
                        'Start': alloc.start_date,
                        'End': alloc.end_date,
                        'Planned Quantity': alloc.planned_quantity,
                        'Task': f"{style.style_number} ({order.po_number if order else 'Unknown'})"
                    })
            finally:
                db.close()
        
        if gantt_data:
            # Convert to dataframe
            df = pd.DataFrame(gantt_data)
            
            # Create figure
            fig = px.timeline(
                df, 
                x_start="Start", 
                x_end="End", 
                y="Line",
                color="Task",
                hover_name="Style",
                hover_data=["PO", "Planned Quantity"],
                title="Line Allocation Gantt Chart",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            # Update layout
            fig.update_layout(
                height=400,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            # Update yaxis
            fig.update_yaxes(autorange="reversed")
            
            # Show figure
            st.plotly_chart(fig, use_container_width=True)
        
        # Line load analysis
        st.subheader("Line Load Analysis")
        
        # Calculate line load percentages
        line_load = {}
        
        for line in production_lines:
            # Initialize with 0% load for all dates
            line_load[line.name] = {date.strftime('%Y-%m-%d'): 0 for date in dates}
        
        # Fill in with allocation data
        for alloc in line_allocations:
            # Get the date range
            alloc_start = max(alloc.start_date, start_date)
            alloc_end = min(alloc.end_date, end_date)
            
            # Calculate daily quantity
            days_allocated = (alloc.end_date - alloc.start_date).days + 1
            daily_quantity = alloc.planned_quantity / days_allocated if days_allocated > 0 else 0
            
            # Fill in the load
            current_date = alloc_start
            while current_date <= alloc_end:
                date_str = current_date.strftime('%Y-%m-%d')
                
                if date_str in line_load[alloc.line_name]:
                    # Calculate load percentage based on line capacity
                    if alloc.line_capacity > 0:
                        load_percentage = (daily_quantity / alloc.line_capacity) * 100
                        line_load[alloc.line_name][date_str] = load_percentage
                
                current_date += timedelta(days=1)
        
        # Create dataframe for heatmap
        load_rows = []
        
        for line_name, line_dates in line_load.items():
            row = {'Line': line_name}
            row.update(line_dates)
            load_rows.append(row)
        
        load_df = pd.DataFrame(load_rows)
        
        # Create heatmap
        date_columns = [date.strftime('%Y-%m-%d') for date in dates]
        z_data = []
        
        for _, row in load_df.iterrows():
            z_data.append([row[date] for date in date_columns])
        
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=date_columns,
            y=load_df['Line'],
            colorscale=[
                [0, 'rgb(0, 0, 100)'],
                [0.4, 'rgb(0, 0, 255)'],
                [0.5, 'rgb(0, 255, 255)'],
                [0.8, 'rgb(255, 255, 0)'],
                [1, 'rgb(255, 0, 0)']
            ],
            hoverongaps=False,
            colorbar=dict(
                title='Load %',
                titleside='right'
            )
        ))
        
        fig.update_layout(
            title='Line Load Heatmap (% of Capacity)',
            height=400,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add some explanations
        with st.expander("💡 Understanding the Line Plan"):
            st.markdown("""
            ### Line Planning Calendar
            This calendar shows the allocation of styles to production lines over time. Each cell represents a day for a specific line, and contains the style number and PO number if a style is allocated for that day.
            
            ### Line Allocation Gantt Chart
            The Gantt chart provides a visual representation of style allocations across lines over time. Each bar represents a style allocation, with the start and end dates shown on the timeline.
            
            ### Line Load Heatmap
            The heatmap shows the load percentage for each line on each day. The color scale ranges from blue (low load) to red (high load). A load of 100% means the line is operating at full capacity.
            
            - **Blue**: Low load (< 50% of capacity)
            - **Cyan**: Moderate load (around 50% of capacity)
            - **Yellow**: High load (around 80% of capacity)
            - **Red**: Overload (> 100% of capacity)
            """)
    else:
        st.info("No line allocations found for the selected date range")

def show_line_setup():
    """Display the line setup and allocation interface"""
    st.subheader("Production Line Setup")
    
    # Get all production lines
    production_lines = get_all_production_lines()
    
    # Display existing lines
    if production_lines:
        # Create a dataframe for the lines
        line_data = []
        
        for line in production_lines:
            line_data.append({
                "Line Name": line.name,
                "Capacity (pcs/day)": line.capacity,
                "Supervisor": line.supervisor or "Not Assigned",
                "Active": "Yes" if line.active else "No"
            })
        
        # Display the lines
        st.dataframe(
            pd.DataFrame(line_data),
            use_container_width=True,
            hide_index=True
        )
    
    # Form to add a new production line
    with st.expander("Add New Production Line"):
        with st.form("add_line_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                line_name = st.text_input("Line Name")
            
            with col2:
                capacity = st.number_input("Capacity (pcs/day)", min_value=1, value=300)
            
            supervisor = st.text_input("Supervisor (optional)")
            
            submit_line = st.form_submit_button("Add Production Line")
            
            if submit_line and line_name:
                # Add the production line
                from db_operations import add_production_line
                new_line = add_production_line(line_name, capacity, supervisor)
                
                if new_line:
                    st.success(f"Production line {line_name} added successfully")
                    st.rerun()
                else:
                    st.error("Failed to add production line")
    
    # Line allocation section
    st.divider()
    st.subheader("Style Allocation to Lines")
    
    # Get all orders
    orders = get_all_orders()
    
    if not orders:
        st.warning("No orders available. Please create orders first.")
        return
    
    if not production_lines:
        st.warning("No production lines defined. Please add production lines first.")
        return
    
    # Create order and style selection
    col1, col2 = st.columns(2)
    
    with col1:
        # Order selection
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
                    # Style selection
                    style_options = [f"{style.style_number} - {style.description}" for style in styles]
                    selected_style = st.selectbox("Select Style", style_options)
                    
                    if selected_style:
                        # Get the selected style
                        style_number = selected_style.split(" - ")[0]
                        style = next((s for s in styles if s.style_number == style_number), None)
                else:
                    st.warning("No styles found for this order")
    
    with col2:
        # Line selection
        line_options = [f"{line.name} (Capacity: {line.capacity})" for line in production_lines]
        selected_line = st.selectbox("Select Production Line", line_options)
        
        if selected_line:
            # Get the selected line
            line_name = selected_line.split(" (")[0]
            line = next((l for l in production_lines if l.name == line_name), None)
    
    # If both style and line are selected, show allocation form
    if 'style' in locals() and style and 'line' in locals() and line:
        st.subheader(f"Allocate Style {style.style_number} to Line {line.name}")
        
        with st.form("allocate_style_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Start Date", datetime.now().date())
            
            with col2:
                # Default to 5 days
                end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=4))
            
            # Calculate total days
            days = (end_date - start_date).days + 1
            
            # Planned quantity
            col1, col2 = st.columns(2)
            
            with col1:
                planned_quantity = st.number_input("Planned Quantity", min_value=1, value=style.quantity)
            
            with col2:
                # Calculate and display daily output
                daily_output = planned_quantity / days if days > 0 else 0
                st.metric("Daily Output", f"{daily_output:.0f} pcs/day")
            
            # Check if the planned quantity exceeds line capacity
            if daily_output > line.capacity:
                st.warning(f"Daily output exceeds line capacity ({line.capacity} pcs/day)")
            
            # Remarks
            remarks = st.text_area("Remarks")
            
            submit_allocation = st.form_submit_button("Allocate Style to Line")
            
            if submit_allocation:
                # Check date range
                if end_date < start_date:
                    st.error("End date cannot be before start date")
                else:
                    # Check for overlapping allocations
                    existing_allocations = get_allocations_by_line(line.id)
                    
                    overlap = False
                    for alloc in existing_allocations:
                        if (alloc.start_date <= end_date and alloc.end_date >= start_date):
                            overlap = True
                            break
                    
                    if overlap:
                        st.warning("This allocation overlaps with an existing allocation on this line. Check the Line Planning Calendar for details.")
                    
                    # Add the allocation
                    new_allocation = allocate_style_to_line(
                        line.id,
                        style.id,
                        start_date,
                        end_date,
                        planned_quantity,
                        remarks
                    )
                    
                    if new_allocation:
                        st.success(f"Style {style.style_number} allocated to Line {line.name} successfully")
                        st.rerun()
                    else:
                        st.error("Failed to allocate style to line")
    
    # Display existing allocations
    st.divider()
    st.subheader("Edit Existing Allocations")
    
    # Create a line selector for viewing allocations
    line_view_options = ["Select Line"] + [line.name for line in production_lines]
    selected_view_line = st.selectbox("Select Line to View Allocations", line_view_options)
    
    if selected_view_line != "Select Line":
        # Get the selected line
        view_line = next((l for l in production_lines if l.name == selected_view_line), None)
        
        if view_line:
            # Get allocations for this line
            allocations = get_allocations_by_line(view_line.id)
            
            if allocations:
                # Create a dataframe for the allocations
                allocation_data = []
                
                for alloc in allocations:
                    db = get_db_session()
                    try:
                        style = db.query(Style).filter(Style.id == alloc.style_id).first()
                        if style:
                            order = db.query(Order).filter(Order.id == style.order_id).first()
                            
                            allocation_data.append({
                                "id": alloc.id,
                                "Style": style.style_number,
                                "PO Number": order.po_number if order else "Unknown",
                                "Start Date": alloc.start_date,
                                "End Date": alloc.end_date,
                                "Days": (alloc.end_date - alloc.start_date).days + 1,
                                "Planned Quantity": alloc.planned_quantity,
                                "Daily Output": alloc.planned_quantity / ((alloc.end_date - alloc.start_date).days + 1) if (alloc.end_date - alloc.start_date).days + 1 > 0 else 0,
                                "Remarks": alloc.remarks or ""
                            })
                    finally:
                        db.close()
                
                # Convert to dataframe
                df = pd.DataFrame(allocation_data)
                
                # Sort by start date
                df = df.sort_values('Start Date')
                
                # Display the allocations
                st.dataframe(
                    df.drop(columns=["id"]),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Allow editing allocations
                st.subheader("Edit Allocation")
                
                # Select allocation to edit
                allocation_options = [f"{row['Style']} ({row['Start Date']} to {row['End Date']})" for _, row in df.iterrows()]
                selected_allocation = st.selectbox("Select Allocation to Edit", allocation_options)
                
                if selected_allocation:
                    # Get allocation ID
                    style_info = selected_allocation.split(" (")[0]
                    date_info = selected_allocation.split("(")[1].replace(")", "")
                    start_date_str = date_info.split(" to ")[0]
                    
                    # Find the allocation in the dataframe
                    alloc_row = df[(df["Style"] == style_info) & (df["Start Date"].astype(str) == start_date_str)]
                    
                    if not alloc_row.empty:
                        alloc_id = alloc_row["id"].iloc[0]
                        
                        # Edit form
                        with st.form("edit_allocation_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                new_start_date = st.date_input(
                                    "Start Date", 
                                    alloc_row["Start Date"].iloc[0]
                                )
                            
                            with col2:
                                new_end_date = st.date_input(
                                    "End Date", 
                                    alloc_row["End Date"].iloc[0]
                                )
                            
                            # Calculate total days
                            days = (new_end_date - new_start_date).days + 1
                            
                            # Planned quantity
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                new_planned_quantity = st.number_input(
                                    "Planned Quantity", 
                                    min_value=1, 
                                    value=int(alloc_row["Planned Quantity"].iloc[0])
                                )
                            
                            with col2:
                                # Calculate and display daily output
                                daily_output = new_planned_quantity / days if days > 0 else 0
                                st.metric("Daily Output", f"{daily_output:.0f} pcs/day")
                            
                            # Check if the planned quantity exceeds line capacity
                            if daily_output > view_line.capacity:
                                st.warning(f"Daily output exceeds line capacity ({view_line.capacity} pcs/day)")
                            
                            # Remarks
                            new_remarks = st.text_area(
                                "Remarks", 
                                value=alloc_row["Remarks"].iloc[0]
                            )
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                submit_edit = st.form_submit_button("Update Allocation")
                            
                            with col2:
                                delete_allocation = st.form_submit_button("Delete Allocation")
                            
                            if submit_edit:
                                # Check date range
                                if new_end_date < new_start_date:
                                    st.error("End date cannot be before start date")
                                else:
                                    # Check for overlapping allocations (excluding this one)
                                    existing_allocations = [a for a in get_allocations_by_line(view_line.id) if a.id != alloc_id]
                                    
                                    overlap = False
                                    for alloc in existing_allocations:
                                        if (alloc.start_date <= new_end_date and alloc.end_date >= new_start_date):
                                            overlap = True
                                            break
                                    
                                    if overlap:
                                        st.warning("This allocation overlaps with an existing allocation on this line. Check the Line Planning Calendar for details.")
                                    
                                    # Update the allocation
                                    db = get_db_session()
                                    try:
                                        allocation = db.query(LineAllocation).filter(LineAllocation.id == alloc_id).first()
                                        if allocation:
                                            allocation.start_date = new_start_date
                                            allocation.end_date = new_end_date
                                            allocation.planned_quantity = new_planned_quantity
                                            allocation.remarks = new_remarks
                                            db.commit()
                                            
                                            st.success("Allocation updated successfully")
                                            st.rerun()
                                        else:
                                            st.error("Allocation not found")
                                    except Exception as e:
                                        st.error(f"Error updating allocation: {str(e)}")
                                    finally:
                                        db.close()
                            
                            elif delete_allocation:
                                # Delete the allocation
                                db = get_db_session()
                                try:
                                    allocation = db.query(LineAllocation).filter(LineAllocation.id == alloc_id).first()
                                    if allocation:
                                        db.delete(allocation)
                                        db.commit()
                                        
                                        st.success("Allocation deleted successfully")
                                        st.rerun()
                                    else:
                                        st.error("Allocation not found")
                                except Exception as e:
                                    st.error(f"Error deleting allocation: {str(e)}")
                                finally:
                                    db.close()
            else:
                st.info(f"No allocations found for line {view_line.name}")
        else:
            st.error("Production line not found")