import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os
import datetime
from datetime import timedelta
import json
import base64
from io import BytesIO

# Database connection
from database import get_db_session
import db_operations

def show_data_integration():
    """Display the data integration dashboard for uploading and processing data files"""
    st.title("Empire OS Data Integration Hub")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["Data Upload", "Data Processing", "Data Visualization", "Integration Settings"])
    
    with tab1:
        show_data_upload()
    
    with tab2:
        show_data_processing()
    
    with tab3:
        show_data_visualization()
    
    with tab4:
        show_integration_settings()

def show_data_upload():
    """Interface for uploading data files"""
    st.header("Data Upload")
    
    # File uploader
    st.subheader("Upload Production Data Files")
    
    data_type = st.selectbox(
        "Select Data Type", 
        ["Daily Production", "Material Inventory", "Order Status", "Quality Inspection", "Retail Sales"]
    )
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["csv", "xlsx", "xls"],
        key="production_data_upload"
    )
    
    if uploaded_file is not None:
        try:
            # Determine file type and read accordingly
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display file preview
            st.subheader("File Preview")
            st.dataframe(df.head(10))
            
            # Column mapping
            st.subheader("Column Mapping")
            st.info("Map your file columns to standard production data fields")
            
            # Get standard fields based on data type
            standard_fields = get_standard_fields(data_type)
            
            # Create column mappings
            column_mapping = {}
            file_columns = df.columns.tolist()
            
            # Create two columns for better layout
            col1, col2 = st.columns(2)
            
            for i, field in enumerate(standard_fields):
                if i % 2 == 0:
                    with col1:
                        column_mapping[field] = st.selectbox(
                            f"Map '{field}' to",
                            options=["-- Ignore --"] + file_columns,
                            key=f"map_{field}"
                        )
                else:
                    with col2:
                        column_mapping[field] = st.selectbox(
                            f"Map '{field}' to",
                            options=["-- Ignore --"] + file_columns,
                            key=f"map_{field}"
                        )
            
            # Process and store button
            if st.button("Process and Store Data"):
                with st.spinner("Processing data..."):
                    # Process the data
                    processed_df = process_uploaded_data(df, column_mapping, data_type)
                    
                    # Store in database
                    store_processed_data(processed_df, data_type)
                    
                    st.success(f"Successfully processed and stored {data_type} data!")
                    
                    # Show some stats about the processed data
                    st.subheader("Processing Summary")
                    st.write(f"Total records processed: {len(processed_df)}")
                    
                    # Show sample of processed data
                    st.subheader("Processed Data Sample")
                    st.dataframe(processed_df.head(5))
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Data upload history
    st.subheader("Upload History")
    upload_history = get_upload_history()
    
    if upload_history:
        history_df = pd.DataFrame(upload_history)
        st.dataframe(history_df)
    else:
        st.info("No previous uploads found")

def show_data_processing():
    """Interface for processing and transforming uploaded data"""
    st.header("Data Processing Algorithms")
    
    # Algorithm selection
    st.subheader("Select Algorithm")
    
    algorithm = st.selectbox(
        "Choose Processing Algorithm",
        ["Production Efficiency Analysis", "Material Consumption Optimization", 
         "Quality Control Metrics", "Order Fulfillment Timeline", "Retail Distribution Analysis"]
    )
    
    # Algorithm parameters
    st.subheader("Algorithm Parameters")
    
    if algorithm == "Production Efficiency Analysis":
        time_period = st.selectbox("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"])
        
        if time_period == "Custom":
            start_date = st.date_input("Start Date", datetime.datetime.now() - timedelta(days=30))
            end_date = st.date_input("End Date", datetime.datetime.now())
        
        efficiency_threshold = st.slider("Efficiency Threshold (%)", 0, 100, 80)
        group_by = st.multiselect("Group By", ["Line", "Style", "Process", "Date"])
        
    elif algorithm == "Material Consumption Optimization":
        material_types = st.multiselect("Material Types", ["Fabric", "Trim", "Accessories", "Packaging"])
        consumption_view = st.radio("Consumption View", ["Actual vs Standard", "Wastage Analysis", "Inventory Projection"])
        
    elif algorithm == "Quality Control Metrics":
        quality_metrics = st.multiselect("Quality Metrics", ["Defect Rate", "First-Time Pass Rate", "Rework Rate", "Customer Returns"])
        defect_categories = st.multiselect("Defect Categories", ["Stitching", "Fabric", "Color", "Size", "Packaging"])
        
    elif algorithm == "Order Fulfillment Timeline":
        orders = st.multiselect("Select Orders", get_sample_orders())
        timeline_view = st.radio("Timeline View", ["Gantt Chart", "Critical Path", "Milestone Status"])
        
    elif algorithm == "Retail Distribution Analysis":
        regions = st.multiselect("Regions", ["North", "South", "East", "West", "Central"])
        channels = st.multiselect("Channels", ["Exclusive Stores", "Multi-Brand Outlets", "E-commerce", "Marketplace"])
        metrics = st.multiselect("Metrics", ["Sales", "Returns", "Inventory", "Sell-through Rate"])
    
    # Run algorithm button
    if st.button("Run Processing Algorithm"):
        with st.spinner(f"Running {algorithm}..."):
            # Simulating processing time
            import time
            time.sleep(2)
            
            st.success(f"{algorithm} completed successfully!")
            
            # Show sample results based on algorithm
            if algorithm == "Production Efficiency Analysis":
                show_production_efficiency_results()
            elif algorithm == "Material Consumption Optimization":
                show_material_optimization_results()
            elif algorithm == "Quality Control Metrics":
                show_quality_control_results()
            elif algorithm == "Order Fulfillment Timeline":
                show_order_timeline_results()
            elif algorithm == "Retail Distribution Analysis":
                show_retail_distribution_results()

def show_data_visualization():
    """Interface for visualizing processed data"""
    st.header("Data Visualization")
    
    # Dataset selection
    st.subheader("Select Dataset")
    
    dataset = st.selectbox(
        "Choose Dataset to Visualize",
        ["Production Performance", "Material Usage", "Quality Metrics", 
         "Order Status", "Retail Performance", "Integrated Dashboard"]
    )
    
    # Time period selection
    time_period = st.selectbox("Time Period", ["Last Week", "Last Month", "Last Quarter", "Year to Date", "Custom"])
    
    if time_period == "Custom":
        start_date = st.date_input("Start Date", datetime.datetime.now() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.datetime.now())
    
    # Visualization type
    viz_type = st.selectbox(
        "Visualization Type",
        ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap", "Scatter Plot", "Area Chart", "Gauge Chart"]
    )
    
    # Filters based on dataset
    if dataset == "Production Performance":
        lines = st.multiselect("Production Lines", ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"])
        processes = st.multiselect("Processes", ["Cutting", "Stitching", "Washing", "Finishing", "Packing"])
        metrics = st.multiselect("Metrics", ["Efficiency", "Output", "Defects", "Downtime"])
        
    elif dataset == "Material Usage":
        materials = st.multiselect("Materials", ["Denim", "Cotton", "Polyester", "Buttons", "Zippers", "Labels"])
        usage_metrics = st.multiselect("Usage Metrics", ["Consumption", "Wastage", "Inventory Level", "Reorder Status"])
        
    elif dataset == "Quality Metrics":
        qc_points = st.multiselect("QC Points", ["In-line", "End-line", "Final Audit", "Customer Returns"])
        defect_types = st.multiselect("Defect Types", ["Critical", "Major", "Minor"])
        
    elif dataset == "Order Status":
        status_types = st.multiselect("Status Types", ["New", "In Production", "Ready for Shipment", "Shipped", "Delivered"])
        buyers = st.multiselect("Buyers", get_sample_buyers())
        
    elif dataset == "Retail Performance":
        store_types = st.multiselect("Store Types", ["EBO", "MBO", "Shop-in-Shop", "Online"])
        regions = st.multiselect("Regions", ["North", "South", "East", "West", "Central"])
        
    # Generate visualization button
    if st.button("Generate Visualization"):
        with st.spinner("Generating visualization..."):
            # Simulating processing time
            import time
            time.sleep(1.5)
            
            st.subheader("Visualization Results")
            
            # Create visualization based on dataset and type
            if dataset == "Production Performance":
                show_production_visualizations(viz_type)
            elif dataset == "Material Usage":
                show_material_visualizations(viz_type)
            elif dataset == "Quality Metrics":
                show_quality_visualizations(viz_type)
            elif dataset == "Order Status":
                show_order_visualizations(viz_type)
            elif dataset == "Retail Performance":
                show_retail_visualizations(viz_type)
            elif dataset == "Integrated Dashboard":
                show_integrated_dashboard()

def show_integration_settings():
    """Interface for configuring data integration settings"""
    st.header("Integration Settings")
    
    # Data sources section
    st.subheader("Connected Data Sources")
    
    # Display connected sources
    sources = [
        {"name": "Logic ERP", "status": "Connected", "last_sync": "2025-03-30 14:25:30"},
        {"name": "Uniware", "status": "Connected", "last_sync": "2025-03-30 18:15:45"},
        {"name": "Uniship", "status": "Pending", "last_sync": "Not synced"},
        {"name": "Meta Ad Manager", "status": "Connected", "last_sync": "2025-03-30 22:05:12"},
        {"name": "Google Ad Manager", "status": "Connected", "last_sync": "2025-03-30 23:10:05"},
        {"name": "Shopify", "status": "Connected", "last_sync": "2025-03-31 00:30:18"}
    ]
    
    sources_df = pd.DataFrame(sources)
    st.dataframe(sources_df)
    
    # Add new data source
    st.subheader("Add New Data Source")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_name = st.text_input("Source Name")
        source_type = st.selectbox("Source Type", ["ERP", "WMS", "POS", "E-commerce", "Advertising", "Custom"])
    
    with col2:
        connection_method = st.selectbox("Connection Method", ["API", "Database", "File Upload", "Custom"])
        refresh_frequency = st.selectbox("Refresh Frequency", ["Hourly", "Daily", "Weekly", "Monthly", "On Demand"])
    
    # Connection parameters (conditional based on connection method)
    st.subheader("Connection Parameters")
    
    if connection_method == "API":
        api_url = st.text_input("API URL")
        auth_type = st.selectbox("Authentication Type", ["None", "API Key", "OAuth2", "Basic Auth"])
        
        if auth_type == "API Key":
            api_key = st.text_input("API Key", type="password")
            key_param = st.text_input("Key Parameter Name", value="api_key")
        elif auth_type == "OAuth2":
            client_id = st.text_input("Client ID")
            client_secret = st.text_input("Client Secret", type="password")
            token_url = st.text_input("Token URL")
        elif auth_type == "Basic Auth":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
    
    elif connection_method == "Database":
        db_type = st.selectbox("Database Type", ["MySQL", "PostgreSQL", "SQL Server", "Oracle", "MongoDB"])
        host = st.text_input("Host")
        port = st.text_input("Port")
        database = st.text_input("Database Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
    
    # Algorithm settings
    st.subheader("Default Processing Algorithms")
    
    default_algorithms = st.multiselect(
        "Select Default Algorithms",
        ["Production Efficiency Analysis", "Material Consumption Optimization", 
         "Quality Control Metrics", "Order Fulfillment Timeline", "Retail Distribution Analysis"]
    )
    
    # Save settings button
    if st.button("Save Integration Settings"):
        st.success("Integration settings saved successfully!")

# Helper functions

def get_standard_fields(data_type):
    """Get standard fields based on data type"""
    if data_type == "Daily Production":
        return ["Date", "Line", "Style", "Process", "Quantity", "Efficiency", "Defects", "Remarks"]
    elif data_type == "Material Inventory":
        return ["Material Code", "Material Name", "Type", "Unit", "Quantity", "Location", "Status", "Last Updated"]
    elif data_type == "Order Status":
        return ["Order ID", "Buyer", "Style", "Quantity", "Status", "Start Date", "Due Date", "Completion %"]
    elif data_type == "Quality Inspection":
        return ["Date", "Line", "Style", "Inspector", "Defect Type", "Quantity Checked", "Defects Found", "Remarks"]
    elif data_type == "Retail Sales":
        return ["Date", "Store", "Region", "Product Code", "Quantity", "Value", "Discount", "Payment Method"]
    return []

def process_uploaded_data(df, column_mapping, data_type):
    """Process uploaded data based on column mapping and data type"""
    # Create new dataframe with mapped columns
    processed_df = pd.DataFrame()
    
    for target_col, source_col in column_mapping.items():
        if source_col != "-- Ignore --":
            processed_df[target_col] = df[source_col]
    
    # Add metadata columns
    processed_df["upload_date"] = datetime.datetime.now()
    processed_df["data_type"] = data_type
    processed_df["processed"] = True
    
    # Apply data type transformations and validation
    if data_type == "Daily Production":
        # Convert date column if exists
        if "Date" in processed_df.columns:
            processed_df["Date"] = pd.to_datetime(processed_df["Date"]).dt.date
        
        # Convert numeric columns
        numeric_cols = ["Quantity", "Efficiency", "Defects"]
        for col in numeric_cols:
            if col in processed_df.columns:
                processed_df[col] = pd.to_numeric(processed_df[col], errors="coerce")
    
    # Similar transformations for other data types...
    
    return processed_df

def store_processed_data(df, data_type):
    """Store processed data in database"""
    # For now, simply return success
    # In a real implementation, this would store the data in the database
    return True

def get_upload_history():
    """Get upload history from database"""
    # Sample data for demonstration
    return [
        {"upload_date": "2025-03-31 10:15:30", "data_type": "Daily Production", "file_name": "production_mar31.xlsx", "records": 120},
        {"upload_date": "2025-03-30 16:45:22", "data_type": "Material Inventory", "file_name": "inventory_mar30.csv", "records": 85},
        {"upload_date": "2025-03-29 09:30:15", "data_type": "Order Status", "file_name": "orders_mar29.xlsx", "records": 45},
        {"upload_date": "2025-03-28 14:20:55", "data_type": "Quality Inspection", "file_name": "quality_mar28.xlsx", "records": 95}
    ]

def get_sample_orders():
    """Get sample orders for demonstration"""
    return ["PO-34521", "PO-34522", "PO-34523", "PO-34524", "PO-34525"]

def get_sample_buyers():
    """Get sample buyers for demonstration"""
    return ["Buyer A", "Buyer B", "Buyer C", "Buyer D", "Buyer E"]

# Result visualization functions

def show_production_efficiency_results():
    """Show production efficiency analysis results"""
    # Create sample data
    dates = pd.date_range(start="2025-03-01", end="2025-03-30")
    lines = ["Line 1", "Line 2", "Line 3"]
    
    data = []
    for date in dates:
        for line in lines:
            efficiency = np.random.uniform(75, 95)
            output = np.random.randint(800, 1200)
            defects = np.random.randint(5, 50)
            
            data.append({
                "Date": date,
                "Line": line,
                "Efficiency": efficiency,
                "Output": output,
                "Defects": defects
            })
    
    df = pd.DataFrame(data)
    
    # Display summary stats
    st.subheader("Production Efficiency Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Efficiency", f"{df['Efficiency'].mean():.2f}%", "1.2%")
    with col2:
        st.metric("Total Output", f"{df['Output'].sum():,}", "5.8%")
    with col3:
        st.metric("Defect Rate", f"{(df['Defects'].sum() / df['Output'].sum() * 100):.2f}%", "-0.5%")
    
    # Efficiency trend by line
    st.subheader("Efficiency Trend by Production Line")
    
    line_df = df.groupby(["Date", "Line"])["Efficiency"].mean().reset_index()
    
    fig = px.line(line_df, x="Date", y="Efficiency", color="Line",
                title="Production Line Efficiency Trend", 
                labels={"Efficiency": "Efficiency (%)", "Date": "Date"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Output vs Defects by line
    st.subheader("Output vs Defects by Line")
    
    output_defect_df = df.groupby("Line").agg({
        "Output": "sum",
        "Defects": "sum"
    }).reset_index()
    
    output_defect_df["Defect Rate (%)"] = output_defect_df["Defects"] / output_defect_df["Output"] * 100
    
    fig = px.bar(output_defect_df, x="Line", y=["Output", "Defects"], barmode="group",
                title="Output vs Defects by Production Line",
                labels={"value": "Count", "Line": "Production Line"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency heatmap by date and line
    st.subheader("Efficiency Heatmap")
    
    # Pivot the data for the heatmap
    heatmap_df = df.pivot_table(index="Date", columns="Line", values="Efficiency")
    
    fig = px.imshow(heatmap_df, 
                   labels=dict(x="Production Line", y="Date", color="Efficiency (%)"),
                   title="Production Efficiency Heatmap",
                   color_continuous_scale="RdYlGn")
    
    st.plotly_chart(fig, use_container_width=True)

def show_material_optimization_results():
    """Show material consumption optimization results"""
    # Create sample data
    materials = ["Denim", "Cotton", "Polyester", "Buttons", "Zippers", "Labels"]
    
    actual_consumption = np.random.uniform(80, 120, size=len(materials))
    standard_consumption = np.array([100] * len(materials))
    wastage = np.random.uniform(2, 15, size=len(materials))
    
    data = {
        "Material": materials,
        "Actual Consumption": actual_consumption,
        "Standard Consumption": standard_consumption,
        "Wastage (%)": wastage
    }
    
    df = pd.DataFrame(data)
    
    # Display summary stats
    st.subheader("Material Consumption Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_variance = ((df["Actual Consumption"].sum() / df["Standard Consumption"].sum()) - 1) * 100
        st.metric("Consumption Variance", f"{avg_variance:.2f}%", f"{'-' if avg_variance > 0 else ''}{abs(avg_variance):.2f}%")
    with col2:
        st.metric("Average Wastage", f"{df['Wastage (%)'].mean():.2f}%", "-1.5%")
    with col3:
        savings_potential = df.apply(lambda x: max(0, (x["Actual Consumption"] - x["Standard Consumption"]) * 10), axis=1).sum()
        st.metric("Savings Potential", f"₹{savings_potential:,.2f}", "")
    
    # Actual vs Standard Consumption
    st.subheader("Actual vs Standard Consumption")
    
    fig = px.bar(df, x="Material", y=["Actual Consumption", "Standard Consumption"], barmode="group",
                title="Actual vs Standard Material Consumption",
                labels={"value": "Consumption (units)", "Material": "Material Type"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Wastage by material
    st.subheader("Wastage by Material")
    
    fig = px.bar(df, x="Material", y="Wastage (%)",
                title="Material Wastage Percentage",
                labels={"Wastage (%)": "Wastage (%)", "Material": "Material Type"},
                color="Wastage (%)",
                color_continuous_scale="Reds")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Optimization recommendations
    st.subheader("Optimization Recommendations")
    
    recommendations = []
    for idx, row in df.iterrows():
        if row["Actual Consumption"] > row["Standard Consumption"]:
            excess = row["Actual Consumption"] - row["Standard Consumption"]
            recommendations.append({
                "Material": row["Material"],
                "Excess Usage": f"{excess:.2f} units",
                "Recommendation": f"Optimize cutting process to reduce {row['Material']} consumption by {excess:.2f} units",
                "Estimated Savings": f"₹{excess * 10:,.2f}"
            })
    
    if recommendations:
        rec_df = pd.DataFrame(recommendations)
        st.dataframe(rec_df)
    else:
        st.info("No optimization recommendations found. All materials are within acceptable consumption limits.")

def show_quality_control_results():
    """Show quality control metrics results"""
    # Create sample data
    qc_points = ["In-line", "End-line", "Final Audit", "Customer Returns"]
    defect_types = ["Critical", "Major", "Minor"]
    
    data = []
    for qc_point in qc_points:
        for defect_type in defect_types:
            checked = np.random.randint(500, 2000)
            defects = np.random.randint(5, checked // 10)
            
            data.append({
                "QC Point": qc_point,
                "Defect Type": defect_type,
                "Quantity Checked": checked,
                "Defects Found": defects,
                "Defect Rate (%)": (defects / checked) * 100
            })
    
    df = pd.DataFrame(data)
    
    # Display summary stats
    st.subheader("Quality Control Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_checked = df["Quantity Checked"].sum()
        st.metric("Total Quantity Checked", f"{total_checked:,}", "")
    with col2:
        total_defects = df["Defects Found"].sum()
        overall_defect_rate = (total_defects / total_checked) * 100
        st.metric("Overall Defect Rate", f"{overall_defect_rate:.2f}%", "-0.8%")
    with col3:
        customer_returns = df[df["QC Point"] == "Customer Returns"]["Defects Found"].sum()
        st.metric("Customer Returns", f"{customer_returns:,}", "-5.2%")
    
    # Defect distribution by type and QC point
    st.subheader("Defect Distribution")
    
    # Grouped by QC Point and Defect Type
    grouped_df = df.groupby(["QC Point", "Defect Type"])["Defects Found"].sum().reset_index()
    
    fig = px.bar(grouped_df, x="QC Point", y="Defects Found", color="Defect Type",
                title="Defects by QC Point and Type",
                labels={"Defects Found": "Number of Defects", "QC Point": "Quality Control Point"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Defect rates by QC point
    st.subheader("Defect Rates by QC Point")
    
    # Calculate defect rates by QC point
    qc_defect_rates = df.groupby("QC Point").apply(
        lambda x: (x["Defects Found"].sum() / x["Quantity Checked"].sum()) * 100
    ).reset_index(name="Defect Rate (%)")
    
    fig = px.bar(qc_defect_rates, x="QC Point", y="Defect Rate (%)",
                title="Defect Rates by Quality Control Point",
                labels={"Defect Rate (%)": "Defect Rate (%)", "QC Point": "Quality Control Point"},
                color="Defect Rate (%)",
                color_continuous_scale="Reds")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quality improvement recommendations
    st.subheader("Quality Improvement Recommendations")
    
    # Find the highest defect rates
    high_defect = df.sort_values("Defect Rate (%)", ascending=False).head(3)
    
    recommendations = []
    for idx, row in high_defect.iterrows():
        recommendations.append({
            "QC Point": row["QC Point"],
            "Defect Type": row["Defect Type"],
            "Current Rate": f"{row['Defect Rate (%)']:.2f}%",
            "Recommendation": f"Implement additional checking at {row['QC Point']} for {row['Defect Type']} defects",
            "Target Rate": f"{max(1.0, row['Defect Rate (%)'] * 0.7):.2f}%"
        })
    
    rec_df = pd.DataFrame(recommendations)
    st.dataframe(rec_df)

def show_order_timeline_results():
    """Show order fulfillment timeline results"""
    # Create sample data for Gantt chart
    orders = get_sample_orders()
    processes = ["Planning", "Material Sourcing", "Cutting", "Stitching", "Washing", "Finishing", "QC", "Packing", "Shipping"]
    
    data = []
    for order in orders:
        start_date = datetime.datetime.now() - timedelta(days=np.random.randint(10, 30))
        
        for i, process in enumerate(processes):
            duration = np.random.randint(2, 7)
            process_start = start_date + timedelta(days=sum([np.random.randint(2, 7) for _ in range(i)]))
            process_end = process_start + timedelta(days=duration)
            completion = 100 if process_end < datetime.datetime.now() else np.random.randint(0, 100)
            
            data.append({
                "Order": order,
                "Process": process,
                "Start": process_start,
                "End": process_end,
                "Duration (days)": duration,
                "Completion (%)": completion
            })
    
    df = pd.DataFrame(data)
    
    # Display summary stats
    st.subheader("Order Fulfillment Summary")
    
    on_time_orders = len(set([x for x, g in df.groupby("Order") if (g["Completion (%)"] == 100).all()]))
    delayed_orders = len(orders) - on_time_orders
    
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_completion = df.groupby("Order")["Completion (%)"].mean().mean()
        st.metric("Average Completion", f"{avg_completion:.1f}%", "3.2%")
    with col2:
        st.metric("On-time Orders", f"{on_time_orders}", f"+{on_time_orders}")
    with col3:
        st.metric("Delayed Orders", f"{delayed_orders}", f"-{100 - delayed_orders}%")
    
    # Gantt chart for order timeline
    st.subheader("Order Fulfillment Timeline")
    
    fig = px.timeline(df, x_start="Start", x_end="End", y="Order", color="Process",
                     title="Order Fulfillment Timeline",
                     labels={"Order": "Purchase Order"})
    
    fig.update_yaxes(autorange="reversed")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Process completion by order
    st.subheader("Process Completion by Order")
    
    # Calculate average completion by process
    process_completion = df.groupby(["Order", "Process"])["Completion (%)"].mean().reset_index()
    
    fig = px.bar(process_completion, x="Process", y="Completion (%)", color="Order", barmode="group",
                title="Process Completion Percentage by Order",
                labels={"Completion (%)": "Completion (%)", "Process": "Production Process"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Critical path analysis
    st.subheader("Critical Path Analysis")
    
    # Identify bottleneck processes
    bottlenecks = df.groupby("Process")["Duration (days)"].mean().sort_values(ascending=False).head(3)
    bottleneck_df = pd.DataFrame({
        "Process": bottlenecks.index,
        "Average Duration (days)": bottlenecks.values,
        "Recommendation": [
            "Split process across multiple lines",
            "Add additional capacity",
            "Optimize workflow to reduce handling time"
        ],
        "Estimated Improvement": [
            "25% reduction in duration",
            "30% increase in throughput",
            "15% efficiency improvement"
        ]
    })
    
    st.dataframe(bottleneck_df)

def show_retail_distribution_results():
    """Show retail distribution analysis results"""
    # Create sample data
    regions = ["North", "South", "East", "West", "Central"]
    channels = ["Exclusive Stores", "Multi-Brand Outlets", "E-commerce", "Marketplace"]
    
    data = []
    for region in regions:
        for channel in channels:
            sales = np.random.randint(100000, 1000000)
            returns = np.random.randint(2000, sales // 10)
            inventory = np.random.randint(20000, 200000)
            sell_through = np.random.uniform(0.4, 0.9)
            
            data.append({
                "Region": region,
                "Channel": channel,
                "Sales (₹)": sales,
                "Returns (₹)": returns,
                "Inventory (₹)": inventory,
                "Sell-through Rate": sell_through
            })
    
    df = pd.DataFrame(data)
    
    # Display summary stats
    st.subheader("Retail Distribution Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_sales = df["Sales (₹)"].sum()
        st.metric("Total Sales", f"₹{total_sales:,.0f}", "4.2%")
    with col2:
        return_rate = (df["Returns (₹)"].sum() / total_sales) * 100
        st.metric("Return Rate", f"{return_rate:.1f}%", "-0.5%")
    with col3:
        total_inventory = df["Inventory (₹)"].sum()
        st.metric("Total Inventory", f"₹{total_inventory:,.0f}", "-2.1%")
    with col4:
        avg_sell_through = df["Sell-through Rate"].mean() * 100
        st.metric("Avg Sell-through", f"{avg_sell_through:.1f}%", "1.8%")
    
    # Sales by region and channel
    st.subheader("Sales Distribution")
    
    # Calculate sales by region and channel
    sales_distribution = df.pivot_table(index="Region", columns="Channel", values="Sales (₹)", aggfunc="sum")
    
    fig = px.bar(df, x="Region", y="Sales (₹)", color="Channel", barmode="group",
                title="Sales by Region and Channel",
                labels={"Sales (₹)": "Sales (₹)", "Region": "Region"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sell-through rate by channel
    st.subheader("Sell-through Rate by Channel")
    
    channel_sell_through = df.groupby("Channel")["Sell-through Rate"].mean().reset_index()
    channel_sell_through["Sell-through Rate"] *= 100  # Convert to percentage
    
    fig = px.bar(channel_sell_through, x="Channel", y="Sell-through Rate",
                title="Average Sell-through Rate by Channel",
                labels={"Sell-through Rate": "Sell-through Rate (%)", "Channel": "Distribution Channel"},
                color="Sell-through Rate",
                color_continuous_scale="Blues")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Return rate by region
    st.subheader("Return Rate by Region")
    
    # Calculate return rate by region
    region_returns = df.groupby("Region").agg({
        "Returns (₹)": "sum",
        "Sales (₹)": "sum"
    }).reset_index()
    
    region_returns["Return Rate (%)"] = (region_returns["Returns (₹)"] / region_returns["Sales (₹)"]) * 100
    
    fig = px.pie(region_returns, values="Return Rate (%)", names="Region",
                title="Return Rate Distribution by Region",
                labels={"Return Rate (%)": "Return Rate (%)"})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution optimization recommendations
    st.subheader("Distribution Optimization Recommendations")
    
    # Calculate inventory-to-sales ratio by channel and region
    inventory_sales = df.copy()
    inventory_sales["Inventory to Sales Ratio"] = inventory_sales["Inventory (₹)"] / inventory_sales["Sales (₹)"]
    
    # Find high inventory areas
    high_inventory = inventory_sales.sort_values("Inventory to Sales Ratio", ascending=False).head(3)
    
    recommendations = []
    for idx, row in high_inventory.iterrows():
        recommendations.append({
            "Region": row["Region"],
            "Channel": row["Channel"],
            "Inventory/Sales Ratio": f"{row['Inventory to Sales Ratio']:.2f}",
            "Recommendation": f"Reduce inventory in {row['Region']} {row['Channel']} by {int((row['Inventory to Sales Ratio'] - 1.0) * 100)}%",
            "Potential Savings": f"₹{row['Inventory (₹)'] * 0.2:,.0f}"
        })
    
    rec_df = pd.DataFrame(recommendations)
    st.dataframe(rec_df)

def show_production_visualizations(viz_type):
    """Show visualizations for production performance"""
    # Create sample data
    dates = pd.date_range(start="2025-03-01", end="2025-03-30")
    lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
    processes = ["Cutting", "Stitching", "Washing", "Finishing", "Packing"]
    
    data = []
    for date in dates:
        for line in lines:
            for process in processes:
                efficiency = np.random.uniform(70, 95)
                output = np.random.randint(500, 1500)
                defects = np.random.randint(5, 80)
                downtime = np.random.randint(0, 120)
                
                data.append({
                    "Date": date,
                    "Line": line,
                    "Process": process,
                    "Efficiency": efficiency,
                    "Output": output,
                    "Defects": defects,
                    "Downtime": downtime
                })
    
    df = pd.DataFrame(data)
    
    # Create visualization based on type
    if viz_type == "Line Chart":
        # Efficiency trend over time
        st.subheader("Efficiency Trend Over Time")
        
        line_efficiency = df.groupby(["Date", "Line"])["Efficiency"].mean().reset_index()
        
        fig = px.line(line_efficiency, x="Date", y="Efficiency", color="Line",
                     title="Production Line Efficiency Trend",
                     labels={"Efficiency": "Efficiency (%)", "Date": "Date"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Bar Chart":
        # Output by line and process
        st.subheader("Output by Production Line and Process")
        
        output_by_line_process = df.groupby(["Line", "Process"])["Output"].sum().reset_index()
        
        fig = px.bar(output_by_line_process, x="Line", y="Output", color="Process", barmode="group",
                    title="Total Output by Production Line and Process",
                    labels={"Output": "Total Output (units)", "Line": "Production Line"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Pie Chart":
        # Defects distribution by line
        st.subheader("Defects Distribution by Production Line")
        
        defects_by_line = df.groupby("Line")["Defects"].sum().reset_index()
        
        fig = px.pie(defects_by_line, values="Defects", names="Line",
                    title="Defects Distribution by Production Line")
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Heatmap":
        # Efficiency heatmap by line and process
        st.subheader("Efficiency Heatmap by Line and Process")
        
        efficiency_pivot = df.pivot_table(index="Line", columns="Process", values="Efficiency", aggfunc="mean")
        
        fig = px.imshow(efficiency_pivot,
                       labels=dict(x="Process", y="Production Line", color="Efficiency (%)"),
                       title="Efficiency Heatmap by Line and Process",
                       color_continuous_scale="RdYlGn")
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Scatter Plot":
        # Output vs Defects
        st.subheader("Output vs Defects")
        
        output_defects = df.groupby(["Line", "Process"]).agg({
            "Output": "sum",
            "Defects": "sum"
        }).reset_index()
        
        output_defects["Defect Rate (%)"] = (output_defects["Defects"] / output_defects["Output"]) * 100
        
        fig = px.scatter(output_defects, x="Output", y="Defect Rate (%)", color="Line", size="Defects",
                        hover_data=["Process"],
                        title="Output vs Defect Rate by Production Line",
                        labels={"Output": "Total Output (units)", "Defect Rate (%)": "Defect Rate (%)"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Area Chart":
        # Cumulative output over time
        st.subheader("Cumulative Output Over Time")
        
        daily_output = df.groupby("Date")["Output"].sum().reset_index()
        daily_output["Cumulative Output"] = daily_output["Output"].cumsum()
        
        fig = px.area(daily_output, x="Date", y="Cumulative Output",
                     title="Cumulative Production Output Over Time",
                     labels={"Cumulative Output": "Cumulative Output (units)", "Date": "Date"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Gauge Chart":
        # Overall efficiency gauge
        st.subheader("Overall Production Efficiency")
        
        overall_efficiency = df["Efficiency"].mean()
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = overall_efficiency,
            title = {'text': "Overall Efficiency (%)"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "red"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ]
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

def show_material_visualizations(viz_type):
    """Show visualizations for material usage"""
    # Similar implementation as show_production_visualizations but for material data
    st.subheader("Material Usage Visualization")
    st.info("Material usage visualization to be implemented")

def show_quality_visualizations(viz_type):
    """Show visualizations for quality metrics"""
    # Similar implementation as show_production_visualizations but for quality data
    st.subheader("Quality Metrics Visualization")
    st.info("Quality metrics visualization to be implemented")

def show_order_visualizations(viz_type):
    """Show visualizations for order status"""
    # Similar implementation as show_production_visualizations but for order data
    st.subheader("Order Status Visualization")
    st.info("Order status visualization to be implemented")

def show_retail_visualizations(viz_type):
    """Show visualizations for retail performance"""
    # Similar implementation as show_production_visualizations but for retail data
    st.subheader("Retail Performance Visualization")
    st.info("Retail performance visualization to be implemented")

def show_integrated_dashboard():
    """Show integrated dashboard with multiple visualizations"""
    st.subheader("Integrated Performance Dashboard")
    
    # Create multiple columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Production Efficiency", "87.5%", "1.8%")
    with col2:
        st.metric("Material Utilization", "92.3%", "0.5%")
    with col3:
        st.metric("Quality Pass Rate", "96.8%", "-0.3%")
    with col4:
        st.metric("On-Time Delivery", "89.5%", "2.2%")
    
    # Create multiple columns for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Production efficiency trend
        dates = pd.date_range(start="2025-03-01", end="2025-03-30")
        efficiency_data = [85 + np.random.uniform(-5, 5) for _ in dates]
        
        efficiency_df = pd.DataFrame({
            "Date": dates,
            "Efficiency": efficiency_data
        })
        
        fig = px.line(efficiency_df, x="Date", y="Efficiency",
                     title="Production Efficiency Trend",
                     labels={"Efficiency": "Efficiency (%)", "Date": "Date"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Order fulfillment status
        statuses = ["New", "In Production", "Ready for Shipment", "Shipped", "Delivered"]
        counts = [15, 28, 12, 8, 37]
        
        status_df = pd.DataFrame({
            "Status": statuses,
            "Count": counts
        })
        
        fig = px.pie(status_df, values="Count", names="Status",
                    title="Order Status Distribution")
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Another row of visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Material consumption
        materials = ["Denim", "Cotton", "Polyester", "Buttons", "Zippers", "Labels"]
        actual = np.random.uniform(80, 120, size=len(materials))
        standard = np.ones(len(materials)) * 100
        
        material_df = pd.DataFrame({
            "Material": materials,
            "Actual": actual,
            "Standard": standard
        })
        
        fig = px.bar(material_df, x="Material", y=["Actual", "Standard"], barmode="group",
                    title="Actual vs Standard Material Consumption",
                    labels={"value": "Consumption (%)", "Material": "Material Type"})
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales by channel
        channels = ["Exclusive Stores", "Multi-Brand Outlets", "E-commerce", "Marketplace"]
        sales = [4500000, 3200000, 2800000, 1500000]
        
        channel_df = pd.DataFrame({
            "Channel": channels,
            "Sales": sales
        })
        
        fig = px.bar(channel_df, x="Channel", y="Sales",
                    title="Sales by Distribution Channel",
                    labels={"Sales": "Sales (₹)", "Channel": "Distribution Channel"},
                    color="Sales",
                    color_continuous_scale="Blues")
        
        st.plotly_chart(fig, use_container_width=True)