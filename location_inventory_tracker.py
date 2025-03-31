import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import datetime
from sqlalchemy import create_engine, text
import os
from database import get_db_session

# Constants
LOCATION_TYPES = ["Factory", "Warehouse", "Store"]
PUSH_FREQUENCIES = ["Real-time", "Hourly", "Daily", "Weekly"]
DEFAULT_FREQUENCY = "Daily"

# Sample data structure for location inventory
SAMPLE_LOCATIONS = {
    "Factory": ["Factory Tirupur", "Factory Delhi", "Factory Mumbai"],
    "Warehouse": ["Central Warehouse", "North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse"],
    "Store": ["Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai", "Store Hyderabad", "Store Kolkata"]
}

def show_location_inventory_tracker():
    """
    Main function to display the Location Inventory Tracker
    """
    st.title("Location Inventory Tracker")
    
    # Sidebar filters
    with st.sidebar:
        st.subheader("Filter Options")
        
        # Location type filter
        loc_types = st.multiselect("Location Types", LOCATION_TYPES, default=LOCATION_TYPES)
        
        # Location selection based on type
        selected_locations = []
        for loc_type in loc_types:
            locs = st.multiselect(
                f"Select {loc_type}s", 
                SAMPLE_LOCATIONS.get(loc_type, []),
                default=SAMPLE_LOCATIONS.get(loc_type, [])
            )
            selected_locations.extend(locs)
        
        # Material category filter
        material_categories = ["Fabric", "Trim", "Accessories", "Finished Goods"]
        selected_categories = st.multiselect("Material Categories", material_categories, default=material_categories)
        
        # Stock health filter
        stock_health_options = ["All", "Critical", "Low", "Optimal", "Excess"]
        selected_health = st.selectbox("Stock Health", stock_health_options, index=0)
        
        # Push frequency configuration
        st.subheader("Push Configuration")
        default_frequency = st.selectbox("Default Push Frequency", PUSH_FREQUENCIES, 
                                        index=PUSH_FREQUENCIES.index(DEFAULT_FREQUENCY))
        
        # Push now button
        if st.button("Push All Inventory Now"):
            st.success("Manual inventory push initiated for all locations!")
    
    # Main content - Tabs
    tabs = st.tabs(["Dashboard", "Location Details", "Inventory Movement", "Configuration"])
    
    # Dashboard Tab
    with tabs[0]:
        show_inventory_dashboard(selected_locations, selected_categories, selected_health)
    
    # Location Details Tab
    with tabs[1]:
        show_location_details(selected_locations)
    
    # Inventory Movement Tab
    with tabs[2]:
        show_inventory_movement(selected_locations)
    
    # Configuration Tab
    with tabs[3]:
        show_push_configuration()

def show_inventory_dashboard(locations, categories, health_filter):
    """Display the main inventory dashboard with visualizations"""
    # Header with key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Locations", len(locations), "+2 from last week")
    with col2:
        st.metric("Total SKUs", "2,543", "+126 from last month")
    with col3:
        st.metric("Critical Stock Items", "43", "-12 from yesterday")
    with col4:
        st.metric("Inventory Value", "₹2.45 Cr", "+8% from last month")
    
    # Stock health distribution
    st.subheader("Stock Health Distribution by Location Type")
    
    # Generate sample data for the visualization
    location_types = []
    health_statuses = []
    counts = []
    
    for loc_type in LOCATION_TYPES:
        for status in ["Critical", "Low", "Optimal", "Excess"]:
            location_types.append(loc_type)
            health_statuses.append(status)
            if status == "Critical":
                counts.append(np.random.randint(10, 30))
            elif status == "Low":
                counts.append(np.random.randint(30, 100))
            elif status == "Optimal":
                counts.append(np.random.randint(200, 500))
            else:  # Excess
                counts.append(np.random.randint(50, 150))
    
    # Create dataframe for visualization
    df_health = pd.DataFrame({
        "Location Type": location_types,
        "Stock Status": health_statuses,
        "Count": counts
    })
    
    # Set up color mapping
    color_map = {
        "Critical": "#FF4B4B",
        "Low": "#FFA500",
        "Optimal": "#00CC96",
        "Excess": "#636EFA"
    }
    
    # Create the visualization
    fig = px.bar(
        df_health, 
        x="Location Type", 
        y="Count",
        color="Stock Status",
        barmode="group",
        color_discrete_map=color_map,
        title="Stock Health Status by Location Type"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Material category distribution
    st.subheader("Inventory by Material Category")
    
    # Generate sample data
    materials = []
    location_types = []
    quantities = []
    
    for material in ["Fabric", "Trim", "Accessories", "Finished Goods"]:
        for loc_type in LOCATION_TYPES:
            materials.append(material)
            location_types.append(loc_type)
            if loc_type == "Factory":
                if material == "Fabric":
                    quantities.append(np.random.randint(5000, 10000))
                elif material == "Trim":
                    quantities.append(np.random.randint(2000, 5000))
                elif material == "Accessories":
                    quantities.append(np.random.randint(1000, 3000))
                else:  # Finished goods
                    quantities.append(np.random.randint(500, 2000))
            elif loc_type == "Warehouse":
                if material == "Fabric":
                    quantities.append(np.random.randint(1000, 3000))
                elif material == "Trim":
                    quantities.append(np.random.randint(500, 2000))
                elif material == "Accessories":
                    quantities.append(np.random.randint(300, 1000))
                else:  # Finished goods
                    quantities.append(np.random.randint(3000, 8000))
            else:  # Store
                if material == "Fabric":
                    quantities.append(np.random.randint(0, 100))
                elif material == "Trim":
                    quantities.append(np.random.randint(0, 50))
                elif material == "Accessories":
                    quantities.append(np.random.randint(100, 300))
                else:  # Finished goods
                    quantities.append(np.random.randint(1000, 3000))
    
    # Create dataframe
    df_materials = pd.DataFrame({
        "Material Category": materials,
        "Location Type": location_types,
        "Quantity": quantities
    })
    
    # Create the visualization
    fig2 = px.bar(
        df_materials,
        x="Material Category",
        y="Quantity",
        color="Location Type",
        barmode="group",
        title="Inventory Quantity by Material Category and Location Type"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Map visualization of inventory locations
    st.subheader("Inventory Locations Map")
    
    # Sample location data with coordinates (using India coordinates)
    map_data = pd.DataFrame({
        "Location": [
            "Factory Tirupur", "Factory Delhi", "Factory Mumbai",
            "Central Warehouse", "North Warehouse", "South Warehouse", "East Warehouse", "West Warehouse",
            "Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai", "Store Hyderabad", "Store Kolkata"
        ],
        "Latitude": [
            11.1085, 28.7041, 19.0760,  # Factories
            22.5726, 28.7041, 13.0827, 22.5726, 19.0760,  # Warehouses
            12.9716, 28.7041, 19.0760, 13.0827, 17.3850, 22.5726  # Stores
        ],
        "Longitude": [
            77.3411, 77.1025, 72.8777,  # Factories
            88.3639, 77.1025, 80.2707, 88.3639, 72.8777,  # Warehouses
            77.5946, 77.1025, 72.8777, 80.2707, 78.4867, 88.3639  # Stores
        ],
        "Type": [
            "Factory", "Factory", "Factory",
            "Warehouse", "Warehouse", "Warehouse", "Warehouse", "Warehouse",
            "Store", "Store", "Store", "Store", "Store", "Store"
        ],
        "Stock Health": [
            "Optimal", "Low", "Optimal",
            "Optimal", "Excess", "Low", "Critical", "Optimal",
            "Low", "Optimal", "Optimal", "Critical", "Optimal", "Low"
        ],
        "SKU Count": [
            345, 289, 412,
            1242, 865, 932, 754, 1103,
            312, 287, 345, 231, 276, 298
        ]
    })
    
    # Filter locations based on selected locations
    if locations:
        map_data = map_data[map_data["Location"].isin(locations)]
    
    # Color mapping for health status
    color_discrete_map = {
        "Critical": "red",
        "Low": "orange",
        "Optimal": "green",
        "Excess": "blue"
    }
    
    # Create the map
    fig3 = px.scatter_mapbox(
        map_data,
        lat="Latitude",
        lon="Longitude",
        color="Stock Health",
        size="SKU Count",
        hover_name="Location",
        hover_data=["Type", "SKU Count"],
        color_discrete_map=color_discrete_map,
        zoom=4,
        height=600,
        title="Inventory Location Map with Stock Health"
    )
    
    fig3.update_layout(mapbox_style="open-street-map")
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Last update information
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"Last inventory data push: {current_time}")
    st.caption("Next scheduled push: Daily at 23:00 IST")

def show_location_details(selected_locations):
    """Display detailed inventory information for selected locations"""
    st.subheader("Location Inventory Details")
    
    if not selected_locations:
        st.warning("Please select at least one location from the sidebar.")
        return
    
    # Location selector
    location = st.selectbox("Select Location", selected_locations)
    
    # Get location type from the location name
    location_type = None
    for loc_type, locs in SAMPLE_LOCATIONS.items():
        if location in locs:
            location_type = loc_type
            break
    
    # Display location information
    st.write(f"**Location Type:** {location_type}")
    st.write(f"**Location Manager:** {'Raj Sharma' if 'Delhi' in location else 'Priya Singh' if 'Mumbai' in location else 'Arun Kumar'}")
    
    # Generate sample inventory data
    np.random.seed(42)  # For reproducibility
    
    # Different product types based on location type
    if location_type == "Factory":
        products = ["Fabric Roll - Denim", "Fabric Roll - Cotton", "Buttons", "Zippers", "Thread Spools", 
                   "Labels", "Rivets", "Leather Patches", "Denim Jeans - WIP", "Denim Shirts - WIP"]
    elif location_type == "Warehouse":
        products = ["Denim Jeans - Men", "Denim Jeans - Women", "Denim Shirts", "Denim Jackets", 
                   "T-shirts", "Denim Shorts", "Fabric Rolls", "Accessories Pack", "Return Stock", "Season Collections"]
    else:  # Store
        products = ["Slim Fit Jeans - Men", "Skinny Jeans - Women", "Classic Denim Shirt", "Vintage Denim Jacket", 
                   "Logo T-shirt", "Denim Shorts - Summer", "Accessories - Belts", "Caps", "Bags", "Gift Sets"]
    
    # Generate random data
    categories = np.random.choice(["Fabric", "Trim", "Accessories", "Finished Goods"], len(products))
    quantities = np.random.randint(10, 1000, len(products))
    reorder_points = np.random.randint(5, 100, len(products))
    max_stock = np.random.randint(500, 2000, len(products))
    last_updated = [
        (datetime.datetime.now() - datetime.timedelta(hours=np.random.randint(1, 72))).strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(len(products))
    ]
    
    # Calculate stock status
    stock_status = []
    for qty, reorder, max_qty in zip(quantities, reorder_points, max_stock):
        ratio = qty / reorder
        if ratio < 0.5:
            stock_status.append("Critical")
        elif ratio < 1:
            stock_status.append("Low")
        elif qty > 0.8 * max_qty:
            stock_status.append("Excess")
        else:
            stock_status.append("Optimal")
    
    # Create dataframe
    df = pd.DataFrame({
        "Product": products,
        "Category": categories,
        "Quantity": quantities,
        "Reorder Point": reorder_points,
        "Max Stock": max_stock,
        "Stock Status": stock_status,
        "Last Updated": last_updated
    })
    
    # Add color to the stock status
    def color_status(val):
        if val == "Critical":
            return "background-color: #FF4B4B; color: white"
        elif val == "Low":
            return "background-color: #FFA500; color: white"
        elif val == "Optimal":
            return "background-color: #00CC96; color: white"
        else:  # Excess
            return "background-color: #636EFA; color: white"
    
    # Display the dataframe with styling
    st.dataframe(df.style.applymap(color_status, subset=["Stock Status"]), use_container_width=True)
    
    # Add action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Request Stock Push"):
            st.success(f"Stock push requested for {location}")
    with col2:
        if st.button("Export Data"):
            st.info("Exporting data...")
    with col3:
        if st.button("Print Inventory Report"):
            st.info("Generating report...")

def show_inventory_movement(selected_locations):
    """Display inventory movement analytics between locations"""
    st.subheader("Inventory Movement Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.date.today())
    
    # Movement type selector
    movement_types = ["All Movements", "Inbound", "Outbound", "Transfers", "Returns"]
    movement_type = st.selectbox("Movement Type", movement_types)
    
    # Generate sample movement data
    np.random.seed(43)  # For reproducibility
    
    dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    dates = np.random.choice(dates, 100)  # 100 random movements
    
    from_locations = []
    to_locations = []
    all_locations = []
    for loc_type in LOCATION_TYPES:
        all_locations.extend(SAMPLE_LOCATIONS.get(loc_type, []))
    
    # Distribution of movement types depends on location pairs
    for _ in range(100):
        from_loc_type = np.random.choice(LOCATION_TYPES)
        to_loc_type = np.random.choice(LOCATION_TYPES)
        
        if from_loc_type == "Factory" and to_loc_type == "Warehouse":
            # Factory to Warehouse: finished goods
            from_loc = np.random.choice(SAMPLE_LOCATIONS["Factory"])
            to_loc = np.random.choice(SAMPLE_LOCATIONS["Warehouse"])
        elif from_loc_type == "Warehouse" and to_loc_type == "Store":
            # Warehouse to Store: retail distribution
            from_loc = np.random.choice(SAMPLE_LOCATIONS["Warehouse"])
            to_loc = np.random.choice(SAMPLE_LOCATIONS["Store"])
        elif from_loc_type == "Store" and to_loc_type == "Warehouse":
            # Store to Warehouse: returns
            from_loc = np.random.choice(SAMPLE_LOCATIONS["Store"])
            to_loc = np.random.choice(SAMPLE_LOCATIONS["Warehouse"])
        else:
            # Random movement
            from_loc = np.random.choice(all_locations)
            to_loc = np.random.choice(all_locations)
            while from_loc == to_loc:  # Ensure different locations
                to_loc = np.random.choice(all_locations)
        
        from_locations.append(from_loc)
        to_locations.append(to_loc)
    
    # Product categories
    categories = np.random.choice(["Fabric", "Trim", "Accessories", "Finished Goods"], 100)
    
    # Quantities moved
    quantities = np.random.choice([10, 20, 50, 100, 200, 500], 100)
    
    # Movement types
    mov_types = []
    for from_loc, to_loc in zip(from_locations, to_locations):
        if "Factory" in from_loc and "Warehouse" in to_loc:
            mov_types.append("Production Transfer")
        elif "Warehouse" in from_loc and "Store" in to_loc:
            mov_types.append("Retail Distribution")
        elif "Store" in from_loc and "Warehouse" in to_loc:
            mov_types.append("Return")
        elif "Warehouse" in from_loc and "Factory" in to_loc:
            mov_types.append("Material Issue")
        else:
            mov_types.append("Internal Transfer")
    
    # Create movement dataframe
    df_movement = pd.DataFrame({
        "Date": dates,
        "From Location": from_locations,
        "To Location": to_locations,
        "Category": categories,
        "Quantity": quantities,
        "Movement Type": mov_types
    })
    
    # Sort by date
    df_movement = df_movement.sort_values(by="Date")
    
    # Filter based on selected movement type
    if movement_type != "All Movements":
        mapping = {
            "Inbound": ["Production Transfer", "Material Issue"],
            "Outbound": ["Retail Distribution"],
            "Transfers": ["Internal Transfer"],
            "Returns": ["Return"]
        }
        df_movement = df_movement[df_movement["Movement Type"].isin(mapping.get(movement_type, []))]
    
    # Filter based on selected locations
    if selected_locations:
        df_movement = df_movement[
            (df_movement["From Location"].isin(selected_locations)) | 
            (df_movement["To Location"].isin(selected_locations))
        ]
    
    # Display movement summary
    st.write(f"Showing {len(df_movement)} inventory movements")
    
    # Movement over time visualization
    st.subheader("Inventory Movement Over Time")
    
    # Aggregate data by date and movement type
    df_agg = df_movement.groupby(["Date", "Movement Type"])["Quantity"].sum().reset_index()
    
    # Create time series chart
    fig = px.line(
        df_agg,
        x="Date",
        y="Quantity",
        color="Movement Type",
        title="Daily Inventory Movement by Type"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Flow diagram between location types
    st.subheader("Inventory Flow Between Location Types")
    
    # Prepare data for Sankey diagram
    df_flow = df_movement.copy()
    
    # Extract location types from location names
    df_flow["From Type"] = df_flow["From Location"].apply(
        lambda x: "Factory" if "Factory" in x else "Warehouse" if "Warehouse" in x else "Store"
    )
    df_flow["To Type"] = df_flow["To Location"].apply(
        lambda x: "Factory" if "Factory" in x else "Warehouse" if "Warehouse" in x else "Store"
    )
    
    # Aggregate flow between location types
    flow_agg = df_flow.groupby(["From Type", "To Type"])["Quantity"].sum().reset_index()
    
    # Create nodes and links for Sankey diagram
    all_nodes = list(set(flow_agg["From Type"].tolist() + flow_agg["To Type"].tolist()))
    node_indices = {node: i for i, node in enumerate(all_nodes)}
    
    links = {"source": [], "target": [], "value": [], "color": []}
    for _, row in flow_agg.iterrows():
        links["source"].append(node_indices[row["From Type"]])
        links["target"].append(node_indices[row["To Type"]])
        links["value"].append(row["Quantity"])
        
        # Color based on source
        if row["From Type"] == "Factory":
            links["color"].append("rgba(31, 119, 180, 0.8)")  # Blue
        elif row["From Type"] == "Warehouse":
            links["color"].append("rgba(255, 127, 14, 0.8)")  # Orange
        else:
            links["color"].append("rgba(44, 160, 44, 0.8)")  # Green
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="rgba(150, 150, 150, 0.8)"
        ),
        link=dict(
            source=links["source"],
            target=links["target"],
            value=links["value"],
            color=links["color"]
        )
    )])
    
    fig.update_layout(title_text="Inventory Flow Between Location Types", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the movement details table
    st.subheader("Movement Details")
    st.dataframe(df_movement, use_container_width=True)

def show_push_configuration():
    """Display and configure inventory push settings"""
    st.subheader("Inventory Push Configuration")
    
    # Global push settings
    st.write("### Global Push Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        default_frequency = st.selectbox(
            "Default Push Frequency",
            PUSH_FREQUENCIES,
            index=PUSH_FREQUENCIES.index(DEFAULT_FREQUENCY)
        )
    with col2:
        push_time = st.time_input("Default Push Time", value=datetime.time(23, 0))
    
    # Push settings by location type
    st.write("### Location Type Push Settings")
    
    for loc_type in LOCATION_TYPES:
        with st.expander(f"{loc_type} Push Settings"):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox(
                    f"{loc_type} Push Frequency",
                    PUSH_FREQUENCIES,
                    index=PUSH_FREQUENCIES.index(DEFAULT_FREQUENCY),
                    key=f"freq_{loc_type}"
                )
            with col2:
                st.time_input(f"{loc_type} Push Time", value=push_time, key=f"time_{loc_type}")
            
            # Special settings based on location type
            if loc_type == "Store":
                st.checkbox("Push after each transaction", value=False, key=f"realtime_{loc_type}")
                st.checkbox("Push after daily closing", value=True, key=f"close_{loc_type}")
            elif loc_type == "Factory":
                st.checkbox("Push after production milestone", value=True, key=f"milestone_{loc_type}")
            elif loc_type == "Warehouse":
                st.checkbox("Push after receiving shipment", value=True, key=f"receive_{loc_type}")
                st.checkbox("Push after dispatch", value=True, key=f"dispatch_{loc_type}")
    
    # Individual location settings
    st.write("### Individual Location Settings")
    
    all_locations = []
    for loc_type in LOCATION_TYPES:
        all_locations.extend(SAMPLE_LOCATIONS.get(loc_type, []))
    
    location = st.selectbox("Select Location for Custom Settings", all_locations)
    
    with st.expander(f"Custom Settings for {location}"):
        st.checkbox("Override default settings", key=f"override_{location}")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                "Push Frequency",
                PUSH_FREQUENCIES,
                key=f"custom_freq_{location}"
            )
        with col2:
            st.time_input("Push Time", value=push_time, key=f"custom_time_{location}")
        
        st.number_input("Critical Stock Threshold (%)", value=20, min_value=5, max_value=50, key=f"critical_{location}")
        st.number_input("Low Stock Threshold (%)", value=40, min_value=10, max_value=70, key=f"low_{location}")
        st.number_input("Excess Stock Threshold (%)", value=80, min_value=50, max_value=95, key=f"excess_{location}")
    
    # Connection settings
    st.write("### Connection Settings")
    
    # API endpoints
    with st.expander("API Endpoints"):
        st.text_input("Logic ERP API Endpoint", value="https://api.logicerp.com/inventory", key="api_logic")
        st.text_input("Uniware API Endpoint", value="https://api.uniware.com/stock", key="api_uniware")
        st.text_input("Store POS API Endpoint", value="https://api.voi-pos.com/inventory", key="api_pos")
    
    # Authentication
    with st.expander("Authentication Settings"):
        st.text_input("API Key Name", value="X-API-KEY", key="api_key_name")
        st.text_input("API Key", value="********", type="password", key="api_key")
        st.checkbox("Use OAuth Authentication", value=False, key="use_oauth")
    
    # Error handling
    with st.expander("Error Handling"):
        st.checkbox("Retry Failed Pushes", value=True, key="retry_push")
        st.number_input("Max Retry Attempts", value=3, min_value=1, max_value=10, key="max_retry")
        st.number_input("Retry Interval (minutes)", value=5, min_value=1, max_value=60, key="retry_interval")
        st.checkbox("Send Error Notifications", value=True, key="error_notify")
    
    # Save buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Configuration"):
            st.success("Push configuration saved successfully!")
    with col2:
        if st.button("Reset to Defaults"):
            st.info("Configuration reset to defaults.")
    
    # Status of last pushes
    st.write("### Push Status")
    
    status_data = []
    for loc_type in LOCATION_TYPES:
        for location in SAMPLE_LOCATIONS.get(loc_type, []):
            last_push = datetime.datetime.now() - datetime.timedelta(hours=np.random.randint(1, 24))
            status = np.random.choice(["Success", "Failed", "Pending"], p=[0.8, 0.1, 0.1])
            items_pushed = np.random.randint(10, 500) if status == "Success" else 0
            
            status_data.append({
                "Location": location,
                "Type": loc_type,
                "Last Push": last_push.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": status,
                "Items Pushed": items_pushed,
                "Next Scheduled": (datetime.datetime.now() + datetime.timedelta(hours=np.random.randint(1, 24))).strftime("%Y-%m-%d %H:%M:%S")
            })
    
    df_status = pd.DataFrame(status_data)
    
    # Add color to the status
    def color_push_status(val):
        if val == "Success":
            return "background-color: #00CC96; color: white"
        elif val == "Failed":
            return "background-color: #FF4B4B; color: white"
        else:  # Pending
            return "background-color: #FFA500; color: white"
    
    # Display the status table with styling
    st.dataframe(df_status.style.applymap(color_push_status, subset=["Status"]), use_container_width=True)

def get_location_inventory_data(location=None, category=None, date_range=None):
    """
    Get location inventory data from database
    In a real implementation, this would query the database for inventory data
    """
    # This is a placeholder for database interaction
    return None

def push_inventory_data(location=None, manual=False):
    """
    Push inventory data from source systems
    In a real implementation, this would call APIs to pull data from source systems
    """
    # This is a placeholder for API interaction
    return True

def create_location_tables():
    """Create database tables for location inventory tracking"""
    session = get_db_session()
    try:
        # This would create the necessary tables in a real implementation
        # Check if tables exist first
        session.execute(text("""
        CREATE TABLE IF NOT EXISTS inventory_locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            location_type VARCHAR(50) NOT NULL,
            manager VARCHAR(100),
            address TEXT,
            latitude FLOAT,
            longitude FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        session.execute(text("""
        CREATE TABLE IF NOT EXISTS location_inventory (
            id SERIAL PRIMARY KEY,
            location_id INTEGER REFERENCES inventory_locations(id),
            product_id VARCHAR(50) NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            quantity INTEGER DEFAULT 0,
            reorder_point INTEGER DEFAULT 0,
            max_stock INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        session.execute(text("""
        CREATE TABLE IF NOT EXISTS inventory_movements (
            id SERIAL PRIMARY KEY,
            movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            from_location_id INTEGER REFERENCES inventory_locations(id),
            to_location_id INTEGER REFERENCES inventory_locations(id),
            product_id VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL,
            movement_type VARCHAR(50),
            reference VARCHAR(100),
            notes TEXT
        )
        """))
        
        session.execute(text("""
        CREATE TABLE IF NOT EXISTS push_configuration (
            id SERIAL PRIMARY KEY,
            location_id INTEGER REFERENCES inventory_locations(id),
            push_frequency VARCHAR(20) NOT NULL,
            push_time TIME NOT NULL,
            critical_threshold INTEGER DEFAULT 20,
            low_threshold INTEGER DEFAULT 40,
            excess_threshold INTEGER DEFAULT 80,
            override_defaults BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        session.execute(text("""
        CREATE TABLE IF NOT EXISTS push_logs (
            id SERIAL PRIMARY KEY,
            location_id INTEGER REFERENCES inventory_locations(id),
            push_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL,
            items_pushed INTEGER DEFAULT 0,
            error_message TEXT,
            duration_seconds INTEGER
        )
        """))
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error creating location tables: {str(e)}")
        return False
    finally:
        session.close()

# Run table creation when module is imported
# create_location_tables()