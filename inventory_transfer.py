import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

def show_inventory_transfer():
    """Display the inventory transfer wizard interface"""
    
    # Page header with styling
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, #1E3A8A 0%, #4B0082 100%); 
        padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; font-size: 2.2rem;'>🔄 Inventory Transfer Wizard</h1>
            <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0;'>Effortlessly move inventory between locations</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Initialize session state for wizard
    if 'transfer_step' not in st.session_state:
        st.session_state.transfer_step = 1
    
    if 'selected_items' not in st.session_state:
        st.session_state.selected_items = []
    
    if 'source_location' not in st.session_state:
        st.session_state.source_location = None
    
    if 'destination_location' not in st.session_state:
        st.session_state.destination_location = None
    
    if 'transfer_quantity' not in st.session_state:
        st.session_state.transfer_quantity = {}
    
    if 'transfer_date' not in st.session_state:
        st.session_state.transfer_date = datetime.now().strftime("%Y-%m-%d")
    
    if 'transfer_complete' not in st.session_state:
        st.session_state.transfer_complete = False
    
    # Create a progress bar for the wizard
    progress_percentage = (st.session_state.transfer_step - 1) / 4 * 100
    
    # Display step indicator
    st.markdown(f"""
    <div style='margin-bottom: 20px;'>
        <div style='background-color: #f0f0f0; height: 8px; border-radius: 4px; position: relative;'>
            <div style='background: linear-gradient(90deg, #1E3A8A 0%, #4B0082 100%); width: {progress_percentage}%; height: 8px; border-radius: 4px;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; margin-top: 5px;'>
            <span style='font-size: 0.8em; color: {"#4B0082" if st.session_state.transfer_step >= 1 else "#aaa"};'>Select Source</span>
            <span style='font-size: 0.8em; color: {"#4B0082" if st.session_state.transfer_step >= 2 else "#aaa"};'>Choose Items</span>
            <span style='font-size: 0.8em; color: {"#4B0082" if st.session_state.transfer_step >= 3 else "#aaa"};'>Destination</span>
            <span style='font-size: 0.8em; color: {"#4B0082" if st.session_state.transfer_step >= 4 else "#aaa"};'>Confirm</span>
            <span style='font-size: 0.8em; color: {"#4B0082" if st.session_state.transfer_step >= 5 else "#aaa"};'>Complete</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Select source location
    if st.session_state.transfer_step == 1:
        show_source_selection()
        
    # Step 2: Select items to transfer
    elif st.session_state.transfer_step == 2:
        show_item_selection()
        
    # Step 3: Select destination location
    elif st.session_state.transfer_step == 3:
        show_destination_selection()
        
    # Step 4: Confirm transfer details
    elif st.session_state.transfer_step == 4:
        show_transfer_confirmation()
        
    # Step 5: Transfer complete
    elif st.session_state.transfer_step == 5:
        show_transfer_complete()

def show_source_selection():
    """Display the source location selection step"""
    
    st.subheader("Step 1: Select Source Location")
    
    # Sample location data
    location_data = {
        "Location ID": ["LOC001", "LOC002", "LOC003", "LOC004", "LOC005"],
        "Location Name": ["Mumbai Main Warehouse", "Delhi Distribution Center", "Bangalore Fulfillment Hub", "Chennai Storage Facility", "Hyderabad Satellite Warehouse"],
        "Type": ["Main Warehouse", "Distribution Center", "Fulfillment Center", "Storage Facility", "Satellite Warehouse"],
        "Total SKUs": [1245, 867, 932, 543, 421],
        "Available Space (%)": [32, 57, 43, 68, 72]
    }
    
    locations_df = pd.DataFrame(location_data)
    
    # Create two columns for the layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display the locations in a more visual card format
        for i, row in locations_df.iterrows():
            space_color = "green" if row["Available Space (%)"] > 50 else "orange" if row["Available Space (%)"] > 30 else "red"
            
            st.markdown(f"""
            <div style='border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px; 
                        background-color: {"#f8f9fa" if i % 2 == 0 else "white"};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h3 style='margin: 0; font-size: 1.2rem;'>{row["Location Name"]}</h3>
                        <p style='margin: 5px 0 0 0; color: #666; font-size: 0.9em;'>{row["Type"]} • ID: {row["Location ID"]}</p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='margin: 0; font-weight: bold; font-size: 1.1em;'>{row["Total SKUs"]} SKUs</p>
                        <p style='margin: 0; color: {space_color};'>
                            {row["Available Space (%)"]}% Space Available
                        </p>
                    </div>
                </div>
                <div style='margin-top: 10px;'>
                    <button style='background-color: #4B0082; color: white; border: none; padding: 5px 10px; 
                                 border-radius: 3px; cursor: pointer; width: 100%;'
                            onclick="document.dispatchEvent(new CustomEvent('streamlit:selectLocation{i}', {{detail: {{value: true}}}}))">
                        Select Location
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # This is necessary to capture the click events from the HTML button
            if st.button(f"Select {row['Location Name']}", key=f"loc_{i}", use_container_width=True):
                st.session_state.source_location = row["Location Name"]
                st.session_state.transfer_step = 2
                st.rerun()
                
    with col2:
        # Warehouse capacity visualization
        st.subheader("Warehouse Capacity")
        
        fig = go.Figure()
        
        for i, row in locations_df.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Location Name"].split(" ")[0]],  # Use just the first word for brevity
                y=[row["Available Space (%)"]],
                name=row["Location Name"],
                marker_color=['green' if val > 50 else 'orange' if val > 30 else 'red' for val in [row["Available Space (%)"]]]
            ))
        
        fig.update_layout(
            title="Available Space by Location",
            xaxis_title="Location",
            yaxis_title="Available Space (%)",
            yaxis=dict(range=[0, 100]),
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a map visualization placeholder
        st.subheader("Location Map")
        st.image("https://via.placeholder.com/400x250?text=Warehouse+Locations+Map", use_column_width=True)

def show_item_selection():
    """Display the item selection step"""
    
    st.subheader(f"Step 2: Select Items from {st.session_state.source_location}")
    
    # Sample inventory data
    inventory_data = generate_sample_inventory(st.session_state.source_location)
    
    # Search and filter options
    col1, col2, col3 = st.columns([1.5, 1.5, 1])
    
    with col1:
        search_term = st.text_input("Search Items", placeholder="Enter SKU or product name")
    
    with col2:
        categories = ["All Categories"] + sorted(list(set(inventory_data["Category"])))
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col3:
        sort_options = ["Stock Level (High to Low)", "Stock Level (Low to High)", "SKU (A-Z)", "Product Name (A-Z)"]
        sort_by = st.selectbox("Sort By", sort_options)
    
    # Filter the data based on search and category
    filtered_df = inventory_data.copy()
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df["SKU"].str.contains(search_term, case=False) | 
            filtered_df["Product Name"].str.contains(search_term, case=False)
        ]
    
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    
    # Sort the data
    if sort_by == "Stock Level (High to Low)":
        filtered_df = filtered_df.sort_values("Current Stock", ascending=False)
    elif sort_by == "Stock Level (Low to High)":
        filtered_df = filtered_df.sort_values("Current Stock", ascending=True)
    elif sort_by == "SKU (A-Z)":
        filtered_df = filtered_df.sort_values("SKU")
    elif sort_by == "Product Name (A-Z)":
        filtered_df = filtered_df.sort_values("Product Name")
    
    # Selection section
    st.write(f"**{len(filtered_df)} items found**. Select items to transfer:")
    
    # Display items in a grid with selection
    items_per_row = 3
    
    for i in range(0, len(filtered_df), items_per_row):
        cols = st.columns(items_per_row)
        
        for j in range(items_per_row):
            if i + j < len(filtered_df):
                item = filtered_df.iloc[i + j]
                
                with cols[j]:
                    # Card for each item
                    st.markdown(f"""
                    <div style='border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; height: 200px; position: relative;'>
                        <h4 style='margin: 0; font-size: 1rem;'>{item['Product Name']}</h4>
                        <p style='margin: 5px 0; color: #666; font-size: 0.8em;'>SKU: {item['SKU']}</p>
                        <p style='margin: 5px 0; font-size: 0.9em;'>Category: {item['Category']}</p>
                        <div style='position: absolute; bottom: 40px; left: 10px; right: 10px;'>
                            <p style='margin: 0; font-weight: bold;'>Current Stock: {item['Current Stock']} units</p>
                            <div style='height: 5px; background-color: #eee; margin-top: 5px; border-radius: 2px;'>
                                <div style='height: 5px; background-color: {"green" if item["Current Stock"] > 30 else "orange" if item["Current Stock"] > 10 else "red"}; width: {min(100, item["Current Stock"])}%; border-radius: 2px;'></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add selection checkbox below each card
                    selected = st.checkbox(f"Select {item['SKU']}", key=f"item_{item['SKU']}")
                    
                    if selected and item['SKU'] not in st.session_state.selected_items:
                        st.session_state.selected_items.append(item['SKU'])
                        st.session_state.transfer_quantity[item['SKU']] = min(5, item['Current Stock'])
                    elif not selected and item['SKU'] in st.session_state.selected_items:
                        st.session_state.selected_items.remove(item['SKU'])
                        if item['SKU'] in st.session_state.transfer_quantity:
                            del st.session_state.transfer_quantity[item['SKU']]
    
    # Selected items summary
    if st.session_state.selected_items:
        st.divider()
        st.subheader("Selected Items")
        
        selected_df = inventory_data[inventory_data["SKU"].isin(st.session_state.selected_items)]
        
        for i, item in selected_df.iterrows():
            cols = st.columns([3, 1, 1])
            
            with cols[0]:
                st.write(f"**{item['Product Name']}** (SKU: {item['SKU']})")
            
            with cols[1]:
                st.number_input(
                    f"Quantity for {item['SKU']}",
                    min_value=1,
                    max_value=item['Current Stock'],
                    value=st.session_state.transfer_quantity.get(item['SKU'], min(5, item['Current Stock'])),
                    step=1,
                    key=f"qty_{item['SKU']}",
                    on_change=update_quantity,
                    args=(item['SKU'],)
                )
            
            with cols[2]:
                if st.button("Remove", key=f"remove_{item['SKU']}"):
                    st.session_state.selected_items.remove(item['SKU'])
                    if item['SKU'] in st.session_state.transfer_quantity:
                        del st.session_state.transfer_quantity[item['SKU']]
                    st.rerun()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Source Selection", use_container_width=True):
            st.session_state.transfer_step = 1
            st.rerun()
    
    with col3:
        if st.session_state.selected_items:
            if st.button("Continue to Destination →", type="primary", use_container_width=True):
                st.session_state.transfer_step = 3
                st.rerun()
        else:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; color: #6c757d;'>
                Select at least one item to continue
            </div>
            """, unsafe_allow_html=True)

def update_quantity(sku):
    """Update the transfer quantity for a specific SKU"""
    st.session_state.transfer_quantity[sku] = st.session_state[f"qty_{sku}"]

def show_destination_selection():
    """Display the destination location selection step"""
    
    st.subheader("Step 3: Select Destination Location")
    
    # Cannot transfer to the same location
    st.info(f"Selected source: **{st.session_state.source_location}**. Please select a different location as the destination.")
    
    # Sample location data excluding the source
    location_data = {
        "Location ID": ["LOC001", "LOC002", "LOC003", "LOC004", "LOC005"],
        "Location Name": ["Mumbai Main Warehouse", "Delhi Distribution Center", "Bangalore Fulfillment Hub", "Chennai Storage Facility", "Hyderabad Satellite Warehouse"],
        "Type": ["Main Warehouse", "Distribution Center", "Fulfillment Center", "Storage Facility", "Satellite Warehouse"],
        "Available Space (%)": [32, 57, 43, 68, 72],
        "Distance (km)": [0, 1400, 980, 1350, 650]  # Distance from Mumbai as reference
    }
    
    locations_df = pd.DataFrame(location_data)
    
    # Filter out the source location
    locations_df = locations_df[locations_df["Location Name"] != st.session_state.source_location]
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display each location as a card with metrics
        for i, row in locations_df.iterrows():
            space_color = "green" if row["Available Space (%)"] > 50 else "orange" if row["Available Space (%)"] > 30 else "red"
            
            st.markdown(f"""
            <div style='border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px; 
                        background-color: {"#f8f9fa" if i % 2 == 0 else "white"};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h3 style='margin: 0; font-size: 1.2rem;'>{row["Location Name"]}</h3>
                        <p style='margin: 5px 0 0 0; color: #666; font-size: 0.9em;'>{row["Type"]} • ID: {row["Location ID"]}</p>
                        <p style='margin: 5px 0 0 0; font-size: 0.9em;'>Distance: {row["Distance (km)"]} km from source</p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='margin: 0; color: {space_color}; font-weight: bold;'>{row["Available Space (%)"]}% Space Available</p>
                        <p style='margin: 5px 0 0 0; font-size: 0.9em;'>Est. Arrival: {(datetime.now() + timedelta(days=1 + row["Distance (km)"]/500)).strftime("%d %b %Y")}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # This is necessary to capture the selection
            if st.button(f"Select {row['Location Name']} as Destination", key=f"dest_{i}"):
                st.session_state.destination_location = row["Location Name"]
                st.session_state.transfer_step = 4
                st.rerun()
    
    with col2:
        # Transfer time estimation
        st.subheader("Estimated Transfer Times")
        
        # Calculate estimated days based on distance
        locations_df["Est. Days"] = 1 + (locations_df["Distance (km)"] / 500).round(1)
        
        fig = px.bar(
            locations_df,
            x="Location Name",
            y="Est. Days",
            color="Est. Days",
            color_continuous_scale="Viridis",
            labels={"Est. Days": "Estimated Days", "Location Name": "Destination"},
            height=300
        )
        
        fig.update_layout(
            title="Transfer Time Estimates",
            xaxis_tickangle=-45,
            xaxis_title=None,
            margin=dict(l=10, r=10, t=50, b=50)
        )
        
        # Add text labels
        fig.update_traces(
            text=locations_df["Est. Days"],
            textposition="outside"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add transfer cost estimation
        st.subheader("Transfer Cost Estimation")
        
        # Calculate cost based on distance and items
        locations_df["Est. Cost"] = 1000 + (locations_df["Distance (km)"] * 0.5 * len(st.session_state.selected_items))
        
        fig = px.bar(
            locations_df,
            x="Location Name",
            y="Est. Cost",
            color="Est. Cost",
            color_continuous_scale="Viridis",
            labels={"Est. Cost": "Estimated Cost (₹)", "Location Name": "Destination"},
            height=300
        )
        
        fig.update_layout(
            title="Transfer Cost Estimates",
            xaxis_tickangle=-45,
            xaxis_title=None,
            margin=dict(l=10, r=10, t=50, b=50)
        )
        
        # Add text labels
        fig.update_traces(
            text=["₹" + str(int(cost)) for cost in locations_df["Est. Cost"]],
            textposition="outside"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to Item Selection", use_container_width=True):
            st.session_state.transfer_step = 2
            st.rerun()

def show_transfer_confirmation():
    """Display the transfer confirmation step"""
    
    st.subheader("Step 4: Confirm Transfer Details")
    
    # Transfer summary box
    st.markdown(f"""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
        <h3 style='margin-top: 0;'>Transfer Summary</h3>
        <table style='width: 100%;'>
            <tr>
                <td style='padding: 8px 0; width: 40%;'><strong>From:</strong></td>
                <td style='padding: 8px 0;'>{st.session_state.source_location}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>To:</strong></td>
                <td style='padding: 8px 0;'>{st.session_state.destination_location}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>Number of Items:</strong></td>
                <td style='padding: 8px 0;'>{len(st.session_state.selected_items)} unique SKUs</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>Total Quantity:</strong></td>
                <td style='padding: 8px 0;'>{sum(st.session_state.transfer_quantity.values())} units</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Selected items summary
    st.subheader("Items to Transfer")
    
    # Sample inventory data
    inventory_data = generate_sample_inventory(st.session_state.source_location)
    selected_df = inventory_data[inventory_data["SKU"].isin(st.session_state.selected_items)].copy()
    
    # Add transfer quantity column
    selected_df["Transfer Quantity"] = selected_df["SKU"].map(st.session_state.transfer_quantity)
    selected_df["Remaining Stock"] = selected_df["Current Stock"] - selected_df["Transfer Quantity"]
    
    # Display as a table
    st.dataframe(
        selected_df[["SKU", "Product Name", "Category", "Current Stock", "Transfer Quantity", "Remaining Stock"]],
        use_container_width=True,
        hide_index=True
    )
    
    # Transfer settings
    st.subheader("Transfer Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        transfer_date = st.date_input(
            "Transfer Date",
            value=datetime.strptime(st.session_state.transfer_date, "%Y-%m-%d"),
            min_value=datetime.now(),
            format="YYYY-MM-DD"
        )
        st.session_state.transfer_date = transfer_date.strftime("%Y-%m-%d")
    
    with col2:
        priority_options = ["Normal", "High Priority", "Urgent"]
        priority = st.selectbox("Transfer Priority", priority_options)
    
    transport_options = ["Road Transport", "Rail Transport", "Air Freight", "Sea Freight", "Combined"]
    transport_method = st.selectbox("Transport Method", transport_options)
    
    special_instructions = st.text_area("Special Instructions", placeholder="Add any special handling instructions...")
    
    # Display estimated costs
    st.subheader("Estimated Costs and Timeline")
    
    # Calculate variables based on selections
    total_quantity = sum(st.session_state.transfer_quantity.values())
    distance = 1000  # Placeholder distance in km
    
    base_cost = 1000
    item_cost = 50 * len(st.session_state.selected_items)
    quantity_cost = 5 * total_quantity
    distance_cost = 0.5 * distance
    
    if transport_method == "Air Freight":
        transport_multiplier = 2.5
        days_multiplier = 0.3
    elif transport_method == "Sea Freight":
        transport_multiplier = 0.8
        days_multiplier = 2.0
    elif transport_method == "Rail Transport":
        transport_multiplier = 0.9
        days_multiplier = 1.0
    elif transport_method == "Combined":
        transport_multiplier = 1.2
        days_multiplier = 1.1
    else:  # Road Transport
        transport_multiplier = 1.0
        days_multiplier = 1.0
    
    priority_multiplier = 1.0 if priority == "Normal" else 1.3 if priority == "High Priority" else 1.8
    
    total_cost = (base_cost + item_cost + quantity_cost + distance_cost) * transport_multiplier * priority_multiplier
    estimated_days = (1 + distance / 500) * days_multiplier
    if priority == "Urgent":
        estimated_days *= 0.6
    elif priority == "High Priority":
        estimated_days *= 0.8
    
    arrival_date = (datetime.strptime(st.session_state.transfer_date, "%Y-%m-%d") + timedelta(days=estimated_days)).strftime("%d %b %Y")
    
    # Create cost breakdown
    cost_data = {
        "Cost Component": ["Base Processing Fee", "Item Handling", "Quantity Charge", "Distance Fee", "Transport Premium", "Priority Adjustment", "Total Cost"],
        "Amount (₹)": [
            base_cost,
            item_cost,
            quantity_cost,
            distance_cost,
            f"{(transport_multiplier - 1) * 100:.0f}% Premium",
            f"{(priority_multiplier - 1) * 100:.0f}% Premium",
            f"₹{total_cost:.2f}"
        ]
    }
    
    cost_df = pd.DataFrame(cost_data)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.dataframe(cost_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown(f"""
        <div style='background-color: #f0f7ff; padding: 15px; border-radius: 5px; height: 100%;'>
            <h4 style='margin-top: 0;'>Transfer Timeline</h4>
            <p><strong>Departure Date:</strong> {st.session_state.transfer_date}</p>
            <p><strong>Estimated Arrival:</strong> {arrival_date}</p>
            <p><strong>Estimated Transit Time:</strong> {estimated_days:.1f} days</p>
            <p><strong>Status Updates:</strong> Real-time tracking available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Destination", use_container_width=True):
            st.session_state.transfer_step = 3
            st.rerun()
    
    with col3:
        if st.button("Complete Transfer →", type="primary", use_container_width=True):
            # Show a processing spinner
            with st.spinner("Processing inventory transfer..."):
                # Simulate processing time
                time.sleep(2)
                st.session_state.transfer_step = 5
                st.session_state.transfer_complete = True
                st.rerun()

def show_transfer_complete():
    """Display the transfer completion confirmation screen"""
    
    if not st.session_state.transfer_complete:
        st.session_state.transfer_step = 1
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <div style='font-size: 80px; margin-bottom: 20px; color: #4CAF50;'>✓</div>
        <h1 style='margin-bottom: 20px;'>Transfer Successfully Initiated!</h1>
        <p style='font-size: 1.2em; margin-bottom: 30px;'>Your inventory transfer request has been processed and is now underway.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Transfer details summary
    st.markdown(f"""
    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px;'>
        <h3 style='margin-top: 0;'>Transfer Details</h3>
        <table style='width: 100%;'>
            <tr>
                <td style='padding: 8px 0; width: 40%;'><strong>Transfer ID:</strong></td>
                <td style='padding: 8px 0;'>TRF-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>From:</strong></td>
                <td style='padding: 8px 0;'>{st.session_state.source_location}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>To:</strong></td>
                <td style='padding: 8px 0;'>{st.session_state.destination_location}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>Items:</strong></td>
                <td style='padding: 8px 0;'>{len(st.session_state.selected_items)} SKUs, {sum(st.session_state.transfer_quantity.values())} units</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>Initiated On:</strong></td>
                <td style='padding: 8px 0;'>{datetime.now().strftime("%d %b %Y, %H:%M")}</td>
            </tr>
            <tr>
                <td style='padding: 8px 0;'><strong>Current Status:</strong></td>
                <td style='padding: 8px 0;'><span style='color: #4CAF50;'>●</span> Processing at source location</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Current status with timeline
    st.subheader("Transfer Timeline")
    
    # Status timeline
    status_steps = [
        {"status": "Initiated", "completed": True, "date": datetime.now().strftime("%d %b, %H:%M")},
        {"status": "Processing", "completed": True, "date": datetime.now().strftime("%d %b, %H:%M")},
        {"status": "Picked", "completed": False, "date": "Pending"},
        {"status": "In Transit", "completed": False, "date": "Pending"},
        {"status": "Delivered", "completed": False, "date": "Pending"},
        {"status": "Verified", "completed": False, "date": "Pending"}
    ]
    
    st.markdown("""
    <div style='margin: 20px 0;'>
        <div style='display: flex; justify-content: space-between; position: relative;'>
            <div style='position: absolute; top: 15px; left: 0; right: 0; height: 4px; background-color: #e0e0e0; z-index: 1;'></div>
    """, unsafe_allow_html=True)
    
    status_html = ""
    for i, step in enumerate(status_steps):
        color = "#4CAF50" if step["completed"] else "#e0e0e0"
        status_html += f"""
        <div style='position: relative; z-index: 2; text-align: center; width: {100/len(status_steps)}%;'>
            <div style='width: 30px; height: 30px; background-color: {color}; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>
                {i+1}
            </div>
            <div style='margin-top: 10px; font-weight: {"bold" if step["completed"] else "normal"};'>{step["status"]}</div>
            <div style='font-size: 0.8em; color: {"#4CAF50" if step["completed"] else "#999"};'>{step["date"]}</div>
        </div>
        """
    
    st.markdown(status_html + "</div></div>", unsafe_allow_html=True)
    
    # Next steps and recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Next Steps")
        st.markdown("""
        - Track your transfer through the "Transfer History" dashboard
        - Inventory at the source location has been adjusted
        - You will receive email notifications at each status change
        - A final confirmation will be sent once items arrive at the destination
        """)
    
    with col2:
        st.subheader("Need Help?")
        st.markdown("""
        - Contact Logistics Support at logistics@voijeans.com
        - Reference your Transfer ID for faster support
        - View detailed progress in the Transfer Tracking Portal
        - Download the transfer documents from your account
        """)
    
    # Actions
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("📋 View Details", use_container_width=True):
            st.toast("Transfer details view is not implemented in this demo")
    
    with col2:
        if st.button("📊 Track Progress", use_container_width=True):
            st.toast("Transfer tracking is not implemented in this demo")
    
    with col3:
        if st.button("📄 Print Documents", use_container_width=True):
            st.toast("Document printing is not implemented in this demo")
    
    with col4:
        if st.button("🔄 New Transfer", type="primary", use_container_width=True):
            # Reset session state for a new transfer
            for key in ['transfer_step', 'selected_items', 'source_location', 
                       'destination_location', 'transfer_quantity', 'transfer_date', 
                       'transfer_complete']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def generate_sample_inventory(location_name):
    """Generate sample inventory data based on location"""
    
    # Base SKUs for different categories
    categories = {
        "Denim": ["DNM", ["Jeans", "Jackets", "Skirts", "Shorts"]],
        "T-Shirts": ["TST", ["Round Neck", "V-Neck", "Polo", "Graphic"]],
        "Shirts": ["SHT", ["Casual", "Formal", "Slim Fit", "Regular Fit"]],
        "Accessories": ["ACC", ["Belts", "Caps", "Socks", "Bags"]]
    }
    
    # Generate randomized inventory
    inventory = []
    
    # Set a seed based on location name for consistent results
    seed = sum(ord(c) for c in location_name)
    random.seed(seed)
    np.random.seed(seed)
    
    for category, (prefix, types) in categories.items():
        for i in range(3):  # 3 items per type in each category
            for type_name in types:
                sku = f"{prefix}-{type_name[:3].upper()}-{random.randint(1000, 9999)}"
                
                product_name = f"VOI {type_name} {['Premium', 'Classic', 'Essential', 'Signature'][i % 4]}"
                
                if "Mumbai" in location_name:
                    stock = random.randint(20, 100)
                elif "Delhi" in location_name:
                    stock = random.randint(15, 80)
                elif "Bangalore" in location_name:
                    stock = random.randint(10, 60)
                else:
                    stock = random.randint(5, 40)
                
                inventory.append({
                    "SKU": sku,
                    "Product Name": product_name,
                    "Category": category,
                    "Type": type_name,
                    "Current Stock": stock,
                    "Unit Price": random.choice([499, 699, 999, 1299, 1499, 1999])
                })
    
    # Convert to DataFrame
    return pd.DataFrame(inventory)