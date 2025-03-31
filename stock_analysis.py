import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
from sqlalchemy import func, text
from database import get_db_session, Material, Style, Order, ProductionEntry, LineAllocation

def get_material_stock_data():
    """Get material inventory data from the database"""
    try:
        session = get_db_session()
        
        # Get all materials with their status and quantities
        materials = session.query(
            Material.id,
            Material.name,
            Material.type,
            Material.unit,
            Material.required_quantity,
            Material.received_quantity,
            Material.issued_quantity,
            Material.status,
            Style.style_number,
            Style.category,
            Order.po_number
        ).join(
            Style, Material.style_id == Style.id
        ).join(
            Order, Style.order_id == Order.id
        ).all()
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame([
            {
                'id': m[0],
                'name': m[1],
                'type': m[2],
                'unit': m[3],
                'required_quantity': m[4],
                'received_quantity': m[5],
                'issued_quantity': m[6],
                'status': m[7],
                'style_number': m[8],
                'category': m[9],
                'po_number': m[10],
                'remaining_quantity': m[5] - m[6] if m[5] is not None and m[6] is not None else 0,
                'fulfillment_rate': (m[5] / m[4] * 100) if m[4] and m[5] else 0,
                'utilization_rate': (m[6] / m[5] * 100) if m[5] and m[6] else 0
            } for m in materials
        ])
        
        return df
    except Exception as e:
        st.error(f"Error fetching inventory data: {str(e)}")
        # Return empty DataFrame with the expected structure for graceful failure
        return pd.DataFrame(columns=[
            'id', 'name', 'type', 'unit', 'required_quantity', 'received_quantity',
            'issued_quantity', 'status', 'style_number', 'category', 'po_number',
            'remaining_quantity', 'fulfillment_rate', 'utilization_rate'
        ])

def display_inventory_health_metrics(df):
    """Display key inventory health metrics"""
    if df.empty:
        st.warning("No inventory data available")
        return
    
    # Calculate key metrics
    total_materials = len(df)
    total_types = df['type'].nunique()
    avg_fulfillment = df['fulfillment_rate'].mean()
    avg_utilization = df['utilization_rate'].mean()
    critical_items = len(df[df['remaining_quantity'] <= 0])
    healthy_items = len(df[df['remaining_quantity'] > 0])
    
    # Display metrics in a 3x2 grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Material Types", 
            f"{total_types}",
            f"{total_materials} items"
        )
    
    with col2:
        st.metric(
            "Avg. Stock Fulfillment", 
            f"{avg_fulfillment:.1f}%",
            help="Average percentage of required materials received"
        )
    
    with col3:
        st.metric(
            "Avg. Stock Utilization", 
            f"{avg_utilization:.1f}%",
            help="Average percentage of received materials issued to production"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Critical Stock Items", 
            f"{critical_items}",
            delta=f"{critical_items/total_materials*100:.1f}% of inventory" if total_materials else "N/A",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Healthy Stock Items", 
            f"{healthy_items}",
            delta=f"{healthy_items/total_materials*100:.1f}% of inventory" if total_materials else "N/A"
        )
    
    with col3:
        # Stock health score (0-100)
        health_score = int(min(100, max(0, 
            (avg_fulfillment * 0.4) + 
            (avg_utilization * 0.2) + 
            ((healthy_items/total_materials) * 100 * 0.4) if total_materials else 0
        )))
        
        st.metric(
            "Stock Health Score", 
            f"{health_score}/100",
            help="Combined score of fulfillment, utilization, and critical stock levels"
        )

def create_stock_radar_chart(df):
    """Create a radar chart showing stock health by material type"""
    if df.empty:
        return None
        
    # Aggregate by material type
    type_metrics = df.groupby('type').agg({
        'required_quantity': 'sum',
        'received_quantity': 'sum',
        'issued_quantity': 'sum',
        'remaining_quantity': 'sum',
        'fulfillment_rate': 'mean',
        'utilization_rate': 'mean'
    }).reset_index()
    
    # Calculate radar metrics (scale 0-100)
    type_metrics['stock_level'] = (type_metrics['remaining_quantity'] / type_metrics['required_quantity'] * 100).fillna(0).clip(0, 100)
    type_metrics['fulfillment'] = type_metrics['fulfillment_rate'].clip(0, 100)
    type_metrics['utilization'] = type_metrics['utilization_rate'].clip(0, 100)
    
    # Prepare data for radar chart
    categories = ['Stock Level', 'Fulfillment', 'Utilization', 'Turnover']
    
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    
    # Add a trace for each material type
    for i, (_, row) in enumerate(type_metrics.iterrows()):
        # Calculate turnover (simplified model)
        turnover = min(100, row['utilization_rate'] * 0.8)
        
        fig.add_trace(go.Scatterpolar(
            r=[row['stock_level'], row['fulfillment'], row['utilization'], turnover],
            theta=categories,
            fill='toself',
            name=row['type'],
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Stock Health Radar by Material Type",
        height=500,
        template="plotly_dark"
    )
    
    return fig

def create_stock_timeline(df):
    """Create a timeline projection of stock levels based on current rates"""
    if df.empty:
        return None
    
    # Sample dates for the timeline (next 8 weeks)
    today = datetime.datetime.now().date()
    dates = [today + datetime.timedelta(days=7*i) for i in range(9)]
    
    # Aggregate by material type
    type_metrics = df.groupby('type').agg({
        'remaining_quantity': 'sum',
        'issued_quantity': 'sum'
    }).reset_index()
    
    # Calculate weekly usage rate (simple estimate based on issued quantities)
    # Assuming issued_quantity represents total used over approximately 8 weeks
    type_metrics['weekly_usage'] = type_metrics['issued_quantity'] / 8
    
    # Generate projected stock levels for each material type
    projections = []
    
    for _, row in type_metrics.iterrows():
        material_type = row['type']
        starting_stock = row['remaining_quantity']
        weekly_usage = row['weekly_usage'] if row['weekly_usage'] > 0 else 1  # Prevent division by zero
        
        for i, date in enumerate(dates):
            projected_stock = max(0, starting_stock - (weekly_usage * i))
            projections.append({
                'date': date,
                'material_type': material_type,
                'projected_stock': projected_stock,
                'weeks_remaining': projected_stock / weekly_usage if weekly_usage > 0 else 0
            })
    
    projection_df = pd.DataFrame(projections)
    
    # Create the visualization
    fig = px.line(
        projection_df, 
        x='date', 
        y='projected_stock', 
        color='material_type',
        title='Stock Level Projection (8 Weeks)',
        labels={'date': 'Date', 'projected_stock': 'Projected Stock', 'material_type': 'Material Type'}
    )
    
    fig.update_layout(
        height=400,
        template="plotly_dark",
        hovermode="x unified"
    )
    
    return fig

def show_stock_analysis():
    """Show the inventory stock analysis page"""
    st.title("Stock Inventory Health Radar")
    
    st.markdown("""
    This dashboard provides a visual analysis of your inventory stock levels, fulfillment rates, and utilization metrics.
    The Stock Health Radar helps identify material categories that need attention, while the projection chart forecasts
    future stock levels based on current usage patterns.
    """)
    
    # Load inventory data
    with st.spinner("Loading inventory data..."):
        stock_data = get_material_stock_data()
    
    # Show inventory health metrics
    st.subheader("Inventory Health Overview")
    display_inventory_health_metrics(stock_data)
    
    # Display radar chart
    st.subheader("Stock Health Radar")
    radar_chart = create_stock_radar_chart(stock_data)
    if radar_chart:
        st.plotly_chart(radar_chart, use_container_width=True)
    else:
        st.warning("Insufficient data to generate the Stock Health Radar")
    
    # Display stock projection timeline
    st.subheader("Stock Level Projection")
    timeline_chart = create_stock_timeline(stock_data)
    if timeline_chart:
        st.plotly_chart(timeline_chart, use_container_width=True)
    else:
        st.warning("Insufficient data to generate the Stock Projection Timeline")
    
    # Material-specific analytics
    st.subheader("Material-Specific Analysis")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        material_types = ['All Types'] + sorted(stock_data['type'].unique().tolist())
        selected_type = st.selectbox("Filter by Material Type:", material_types)
    
    with col2:
        status_options = ['All Statuses'] + sorted(stock_data['status'].unique().tolist())
        selected_status = st.selectbox("Filter by Status:", status_options)
    
    # Apply filters
    filtered_data = stock_data.copy()
    if selected_type != 'All Types':
        filtered_data = filtered_data[filtered_data['type'] == selected_type]
    if selected_status != 'All Statuses':
        filtered_data = filtered_data[filtered_data['status'] == selected_status]
    
    # Display filtered data
    if not filtered_data.empty:
        # Create a heatmap of material status
        status_data = filtered_data.pivot_table(
            index='name',
            columns='status',
            values='remaining_quantity',
            aggfunc='sum',
            fill_value=0
        )
        
        # Material stock level visualization (horizontal bar chart)
        fig = px.bar(
            filtered_data,
            y='name',
            x='remaining_quantity',
            color='status',
            title=f"Current Stock Levels ({selected_type if selected_type != 'All Types' else 'All Material Types'})",
            labels={'name': 'Material', 'remaining_quantity': 'Remaining Quantity'},
            orientation='h',
            height=max(400, len(filtered_data) * 25)  # Dynamic height based on number of materials
        )
        
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table with important metrics
        st.subheader("Detailed Inventory Data")
        display_cols = [
            'name', 'type', 'status', 'required_quantity', 
            'received_quantity', 'issued_quantity', 'remaining_quantity',
            'style_number', 'po_number'
        ]
        st.dataframe(filtered_data[display_cols], use_container_width=True)
    else:
        st.warning("No data available with the selected filters")
