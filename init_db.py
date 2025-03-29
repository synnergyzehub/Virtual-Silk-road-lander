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
        
        # Add sample buyers for Voi Jeans
        voi_buyer = Buyer(
            name="Voi Jeans Retail India Pvt Ltd",
            contact_person="Ravi Sharma",
            email="ravi.sharma@voijeans.com",
            phone="981-234-5678"
        )
        db.add(voi_buyer)
        
        scotts_buyer = Buyer(
            name="Scotts Garments (CMP)",
            contact_person="Anjali Patel",
            email="anjali.patel@scottsgarments.com",
            phone="892-567-3456"
        )
        db.add(scotts_buyer)
        
        denim_buyer = Buyer(
            name="Voi Jeans Flagship Store",
            contact_person="Vikram Mehta",
            email="vikram.mehta@voijeans.com",
            phone="765-432-1098"
        )
        db.add(denim_buyer)
        
        db.flush()  # Get IDs for the buyers
        
        # Add sample orders
        today = datetime.now().date()
        
        # Voi Jeans SS25 Order
        voi_order = Order(
            po_number="VOI-SS25-001",
            buyer_id=voi_buyer.id,
            order_date=today - timedelta(days=15),
            delivery_date=today + timedelta(days=45),
            status="In Progress",
            total_quantity=2000
        )
        db.add(voi_order)
        
        # Scotts Garments Order
        scotts_order = Order(
            po_number="SCOTTS-CMP-2025-005",
            buyer_id=scotts_buyer.id,
            order_date=today - timedelta(days=7),
            delivery_date=today + timedelta(days=53),
            status="New",
            total_quantity=1500
        )
        db.add(scotts_order)
        
        # Voi Flagship Store Order
        flagship_order = Order(
            po_number="VOI-FS-2025-010",
            buyer_id=denim_buyer.id,
            order_date=today - timedelta(days=30),
            delivery_date=today + timedelta(days=15),
            status="In Progress",
            total_quantity=3000
        )
        db.add(flagship_order)
        
        db.flush()  # Get IDs for the orders
        
        # Add sample styles
        # Voi Jeans Styles
        voi_style1 = Style(
            order_id=voi_order.id,
            style_number="VOI-DENIM-001",
            description="Men's Slim Fit Denim Jeans",
            category="Denim",
            color="Indigo Blue",
            size_breakdown=json.dumps({"30": 200, "32": 300, "34": 300, "36": 200}),
            quantity=1000,
            status="In Progress"
        )
        db.add(voi_style1)
        
        voi_style2 = Style(
            order_id=voi_order.id,
            style_number="VOI-DENIM-002",
            description="Women's Straight Leg Denim",
            category="Denim",
            color="Dark Wash",
            size_breakdown=json.dumps({"28": 200, "30": 300, "32": 300, "34": 200}),
            quantity=1000,
            status="In Progress"
        )
        db.add(voi_style2)
        
        # Scotts Garments Styles
        scotts_style = Style(
            order_id=scotts_order.id,
            style_number="SCOTTS-SS25-001",
            description="Men's Bootcut Jeans",
            category="Denim",
            color="Vintage Wash",
            size_breakdown=json.dumps({"30": 300, "32": 400, "34": 500, "36": 300}),
            quantity=1500,
            status="New"
        )
        db.add(scotts_style)
        
        # Flagship Store Styles
        flagship_style1 = Style(
            order_id=flagship_order.id,
            style_number="VOI-FS-010",
            description="Men's Denim Jacket",
            category="Outerwear",
            color="Light Blue",
            size_breakdown=json.dumps({"S": 300, "M": 400, "L": 300, "XL": 200, "XXL": 100}),
            quantity=1300,
            status="In Progress"
        )
        db.add(flagship_style1)
        
        flagship_style2 = Style(
            order_id=flagship_order.id,
            style_number="VOI-FS-011",
            description="Women's Denim Skirt",
            category="Skirt",
            color="Stonewash",
            size_breakdown=json.dumps({"XS": 200, "S": 400, "M": 600, "L": 400, "XL": 100}),
            quantity=1700,
            status="New"
        )
        db.add(flagship_style2)
        
        db.flush()  # Get IDs for the styles
        
        # Add production lines for Scotts Garments
        line1 = ProductionLine(name="Scotts Line 1", capacity=300, supervisor="Rajesh Kumar")
        line2 = ProductionLine(name="Scotts Line 2", capacity=350, supervisor="Priya Patel")
        line3 = ProductionLine(name="Scotts Line 3", capacity=400, supervisor="Amit Singh")
        
        db.add(line1)
        db.add(line2)
        db.add(line3)
        
        db.flush()  # Get IDs for the lines
        
        # Add line allocations
        # Allocate Voi Style 1 to Line 1
        allocation1 = LineAllocation(
            line_id=line1.id,
            style_id=voi_style1.id,
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=5),
            planned_quantity=1000,
            remarks="Priority order for SS25 Collection"
        )
        db.add(allocation1)
        
        # Allocate Flagship Style 1 to Line 2
        allocation2 = LineAllocation(
            line_id=line2.id,
            style_id=flagship_style1.id,
            start_date=today - timedelta(days=10),
            end_date=today + timedelta(days=0),
            planned_quantity=1300,
            remarks="Expedite for early delivery to flagship store"
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