import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

from database import get_db_session, create_tables
from db_operations import get_dashboard_data, get_all_orders, get_styles_by_order

def show_manufacturing_dashboard():
    """Display the manufacturing dashboard with key metrics and visualizations"""
    st.title("🏭 Manufacturing Lifecycle Dashboard")
    
    # Create tables if they don't exist
    create_tables()
    
    # Fetch dashboard data
    dashboard_data = get_dashboard_data()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Orders", 
            value=dashboard_data['total_orders'],
            delta=None
        )
    
    with col2:
        total_wip = dashboard_data.get('orders_by_status', {}).get('In Progress', 0)
        st.metric(
            label="Work In Progress", 
            value=total_wip,
            delta=None
        )
    
    with col3:
        total_dispatch = dashboard_data['production_summary']['total_dispatch']
        st.metric(
            label="Dispatched Units", 
            value=total_dispatch,
            delta=None
        )
    
    with col4:
        avg_efficiency = np.mean(list(dashboard_data['line_efficiency'].values())) if dashboard_data['line_efficiency'] else 0
        st.metric(
            label="Avg. Line Efficiency", 
            value=f"{avg_efficiency:.1f}%",
            delta=None
        )
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Production Summary")
        
        # Create data for production summary chart
        prod_summary = dashboard_data['production_summary']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Cutting', 'Stitching', 'Packing', 'Dispatch'],
            y=[prod_summary['total_cutting'], 
               prod_summary['total_stitching'], 
               prod_summary['total_packing'], 
               prod_summary['total_dispatch']],
            marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        ))
        
        fig.update_layout(
            title="Last 30 Days Production",
            xaxis_title="Process",
            yaxis_title="Units",
            height=400,
            template="plotly_dark",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Production Lines Efficiency")
        
        # Create data for line efficiency chart
        line_efficiency = dashboard_data['line_efficiency']
        
        if line_efficiency:
            lines = list(line_efficiency.keys())
            efficiencies = list(line_efficiency.values())
            
            # Create a color scale based on efficiency values
            colors = ['#EF553B' if e < 50 else '#FFAA00' if e < 75 else '#00CC96' for e in efficiencies]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=lines,
                y=efficiencies,
                marker_color=colors
            ))
            
            fig.update_layout(
                title="Average Line Efficiency (%)",
                xaxis_title="Production Line",
                yaxis_title="Efficiency (%)",
                height=400,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            
            # Add a horizontal line at 80% (target efficiency)
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=80,
                x1=len(lines)-0.5,
                y1=80,
                line=dict(
                    color="white",
                    width=2,
                    dash="dash",
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No production line efficiency data available yet.")
    
    # Daily Production Timeline
    st.subheader("Daily Production Timeline")
    
    daily_prod = dashboard_data.get('daily_production', {})
    if daily_prod:
        # Convert to DataFrame for easier plotting
        dates = list(daily_prod.keys())
        dates.sort()  # Sort dates
        
        df = pd.DataFrame(index=dates)
        df['Cutting'] = [daily_prod[date]['Cutting'] for date in dates]
        df['Stitching'] = [daily_prod[date]['Stitching'] for date in dates]
        df['Packing'] = [daily_prod[date]['Packing'] for date in dates]
        df['Dispatch'] = [daily_prod[date]['Dispatch'] for date in dates]
        
        # Create the line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Cutting'],
            mode='lines+markers',
            name='Cutting',
            line=dict(color='#636EFA', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Stitching'],
            mode='lines+markers',
            name='Stitching',
            line=dict(color='#EF553B', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Packing'],
            mode='lines+markers',
            name='Packing',
            line=dict(color='#00CC96', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Dispatch'],
            mode='lines+markers',
            name='Dispatch',
            line=dict(color='#AB63FA', width=2)
        ))
        
        fig.update_layout(
            title="Daily Production by Process",
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
    else:
        st.info("No daily production data available yet.")
    
    # Create two columns for order status and material status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Status")
        
        # Create pie chart for order status
        order_status = dashboard_data.get('orders_by_status', {})
        
        if order_status:
            labels = list(order_status.keys())
            values = list(order_status.values())
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values,
                hole=.4,
                marker_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFAA00']
            )])
            
            fig.update_layout(
                title="Orders by Status",
                height=300,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order status data available yet.")
    
    with col2:
        st.subheader("Material Status")
        
        # Create pie chart for material status
        material_status = dashboard_data.get('material_status', {})
        
        if material_status:
            labels = list(material_status.keys())
            values = list(material_status.values())
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values,
                hole=.4,
                marker_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFAA00']
            )])
            
            fig.update_layout(
                title="Materials by Status",
                height=300,
                template="plotly_dark",
                margin=dict(l=20, r=20, t=40, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No material status data available yet.")
    
    # Display recent orders
    st.subheader("Recent Orders")
    orders = get_all_orders()
    
    if orders:
        # Sort orders by date (most recent first)
        orders.sort(key=lambda x: x.order_date, reverse=True)
        
        # Display only the most recent 5 orders
        recent_orders = orders[:5]
        
        # Create a list to store order data
        order_data = []
        
        for order in recent_orders:
            # Get all styles for this order
            styles = get_styles_by_order(order.id)
            
            # Calculate progress percentage based on style statuses
            total_styles = len(styles)
            completed_styles = sum(1 for style in styles if style.status == 'Completed')
            progress = (completed_styles / total_styles * 100) if total_styles > 0 else 0
            
            # Add to order data
            order_data.append({
                "PO Number": order.po_number,
                "Buyer": order.buyer.name,
                "Order Date": order.order_date.strftime('%Y-%m-%d'),
                "Delivery Date": order.delivery_date.strftime('%Y-%m-%d'),
                "Status": order.status,
                "Progress": f"{progress:.0f}%"
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(order_data)
        
        # Display as table
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No orders available yet.")
        
    # Add some helpful explanations at the bottom
    with st.expander("💡 Understanding the Dashboard"):
        st.markdown("""
        This dashboard provides a comprehensive overview of the manufacturing process:
        
        - **Total Orders**: The total number of purchase orders in the system.
        - **Work In Progress**: Orders currently in the production phase.
        - **Dispatched Units**: The total number of units that have been dispatched.
        - **Avg. Line Efficiency**: The average efficiency percentage across all production lines.
        
        **Production Summary** shows the total units processed at each stage of production over the last 30 days.
        
        **Production Lines Efficiency** displays the efficiency of each production line, with the dashed line indicating the target efficiency of 80%.
        
        **Daily Production Timeline** shows the daily output of each production process, helping identify trends and bottlenecks.
        
        **Order Status and Material Status** charts provide a quick overview of the current state of orders and materials.
        
        **Recent Orders** displays the most recent orders with their current status and progress.
        """)