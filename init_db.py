import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import json

from database import create_tables, get_db_session, Buyer, Order, Style, ProductionLine, LineAllocation

def initialize_database():
    """Initialize the database with sample data for demonstration"""
    # Create database tables if they don't exist
    create_tables()
    
    # Check if we already have data in the database
    db = get_db_session()
    try:
        # Check if we have buyers
        buyers_count = db.query(Buyer).count()
        
        # If we already have data, don't reinitialize
        if buyers_count > 0:
            return False
        
        # Add sample buyers
        ecg_buyer = Buyer(
            name="ECG Commune",
            contact_person="John Smith",
            email="john.smith@ecgcommune.com",
            phone="123-456-7890"
        )
        db.add(ecg_buyer)
        
        synergy_buyer = Buyer(
            name="Synergyze Retail",
            contact_person="Sarah Johnson",
            email="sarah.johnson@synergyze.com",
            phone="456-789-0123"
        )
        db.add(synergy_buyer)
        
        woven_buyer = Buyer(
            name="Woven Apparel",
            contact_person="Michael Chang",
            email="michael.chang@wovenapparel.com",
            phone="789-012-3456"
        )
        db.add(woven_buyer)
        
        db.flush()  # Get IDs for the buyers
        
        # Add sample orders
        today = datetime.now().date()
        
        # ECG Order
        ecg_order = Order(
            po_number="ECG-PO-2025-001",
            buyer_id=ecg_buyer.id,
            order_date=today - timedelta(days=15),
            delivery_date=today + timedelta(days=45),
            status="In Progress",
            total_quantity=2000
        )
        db.add(ecg_order)
        
        # Synergyze Order
        synergy_order = Order(
            po_number="SYN-PO-2025-005",
            buyer_id=synergy_buyer.id,
            order_date=today - timedelta(days=7),
            delivery_date=today + timedelta(days=53),
            status="New",
            total_quantity=1500
        )
        db.add(synergy_order)
        
        # Woven Apparel Order
        woven_order = Order(
            po_number="WA-PO-2025-010",
            buyer_id=woven_buyer.id,
            order_date=today - timedelta(days=30),
            delivery_date=today + timedelta(days=15),
            status="In Progress",
            total_quantity=3000
        )
        db.add(woven_order)
        
        db.flush()  # Get IDs for the orders
        
        # Add sample styles
        # ECG Styles
        ecg_style1 = Style(
            order_id=ecg_order.id,
            style_number="ECG-ST-001",
            description="Men's Crew Neck T-Shirt",
            category="T-shirt",
            color="Navy Blue",
            size_breakdown=json.dumps({"S": 200, "M": 300, "L": 300, "XL": 200}),
            quantity=1000,
            status="In Progress"
        )
        db.add(ecg_style1)
        
        ecg_style2 = Style(
            order_id=ecg_order.id,
            style_number="ECG-ST-002",
            description="Women's V-Neck T-Shirt",
            category="T-shirt",
            color="White",
            size_breakdown=json.dumps({"XS": 200, "S": 300, "M": 300, "L": 200}),
            quantity=1000,
            status="In Progress"
        )
        db.add(ecg_style2)
        
        # Synergyze Styles
        synergy_style = Style(
            order_id=synergy_order.id,
            style_number="SYN-ST-005",
            description="Men's Polo Shirt",
            category="Polo",
            color="Black",
            size_breakdown=json.dumps({"S": 300, "M": 400, "L": 500, "XL": 300}),
            quantity=1500,
            status="New"
        )
        db.add(synergy_style)
        
        # Woven Apparel Styles
        woven_style1 = Style(
            order_id=woven_order.id,
            style_number="WA-ST-010",
            description="Men's Casual Shirt",
            category="Shirt",
            color="Light Blue",
            size_breakdown=json.dumps({"S": 300, "M": 400, "L": 300, "XL": 200, "XXL": 100}),
            quantity=1300,
            status="In Progress"
        )
        db.add(woven_style1)
        
        woven_style2 = Style(
            order_id=woven_order.id,
            style_number="WA-ST-011",
            description="Women's Blouse",
            category="Shirt",
            color="Peach",
            size_breakdown=json.dumps({"XS": 200, "S": 400, "M": 600, "L": 400, "XL": 100}),
            quantity=1700,
            status="New"
        )
        db.add(woven_style2)
        
        db.flush()  # Get IDs for the styles
        
        # Add production lines
        line1 = ProductionLine(name="Line 1", capacity=300, supervisor="Robert Chen")
        line2 = ProductionLine(name="Line 2", capacity=350, supervisor="Lisa Wong")
        line3 = ProductionLine(name="Line 3", capacity=400, supervisor="David Park")
        
        db.add(line1)
        db.add(line2)
        db.add(line3)
        
        db.flush()  # Get IDs for the lines
        
        # Add line allocations
        # Allocate ECG Style 1 to Line 1
        allocation1 = LineAllocation(
            line_id=line1.id,
            style_id=ecg_style1.id,
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=5),
            planned_quantity=1000,
            remarks="Priority order for ECG"
        )
        db.add(allocation1)
        
        # Allocate Woven Style 1 to Line 2
        allocation2 = LineAllocation(
            line_id=line2.id,
            style_id=woven_style1.id,
            start_date=today - timedelta(days=10),
            end_date=today + timedelta(days=0),
            planned_quantity=1300,
            remarks="Expedite for early delivery"
        )
        db.add(allocation2)
        
        # Commit all changes
        db.commit()
        
        return True
    except Exception as e:
        # Rollback on error
        db.rollback()
        st.error(f"Error initializing database: {str(e)}")
        return False
    finally:
        db.close()

def show_db_initialization():
    """Show the database initialization interface"""
    st.title("Database Initialization")
    
    # Check if we already have data
    db = get_db_session()
    try:
        # Check if we have buyers
        buyers_count = db.query(Buyer).count()
        
        if buyers_count > 0:
            st.success("Database is already initialized with sample data.")
            
            # Show some statistics
            orders_count = db.query(Order).count()
            styles_count = db.query(Style).count()
            lines_count = db.query(ProductionLine).count()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Buyers", buyers_count)
            
            with col2:
                st.metric("Orders", orders_count)
            
            with col3:
                st.metric("Styles", styles_count)
            
            with col4:
                st.metric("Production Lines", lines_count)
            
            # Option to reset
            if st.button("Reset Database"):
                # Drop all tables and recreate
                from database import Base, engine
                Base.metadata.drop_all(engine)
                create_tables()
                
                # Reinitialize
                if initialize_database():
                    st.success("Database has been reset and reinitialized with fresh sample data.")
                    st.rerun()
                else:
                    st.error("Failed to reinitialize database.")
        else:
            # Initialize the database
            st.info("Database is not initialized yet. Click the button below to initialize with sample data.")
            
            if st.button("Initialize Database with Sample Data"):
                if initialize_database():
                    st.success("Database initialized successfully with sample data.")
                    st.rerun()
                else:
                    st.error("Failed to initialize database.")
    finally:
        db.close()