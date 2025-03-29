import pandas as pd
import json
from datetime import datetime, timedelta
from database import (
    get_db_session, Buyer, Order, Style, Material, 
    ProductionLine, LineAllocation, ProductionEntry
)

# ===== Buyer Operations =====
def get_all_buyers():
    """Get all buyers from the database"""
    db = get_db_session()
    try:
        buyers = db.query(Buyer).all()
        return buyers
    finally:
        db.close()

def add_buyer(name, contact_person=None, email=None, phone=None):
    """Add a new buyer to the database"""
    db = get_db_session()
    try:
        buyer = Buyer(name=name, contact_person=contact_person, email=email, phone=phone)
        db.add(buyer)
        db.commit()
        return buyer
    finally:
        db.close()

def get_buyer_by_id(buyer_id):
    """Get a buyer by ID"""
    db = get_db_session()
    try:
        buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
        return buyer
    finally:
        db.close()

# ===== Order Operations =====
def get_all_orders():
    """Get all orders from the database with buyer information"""
    db = get_db_session()
    try:
        orders = db.query(Order).all()
        return orders
    finally:
        db.close()

def get_orders_by_buyer(buyer_id):
    """Get all orders for a specific buyer"""
    db = get_db_session()
    try:
        orders = db.query(Order).filter(Order.buyer_id == buyer_id).all()
        return orders
    finally:
        db.close()

def get_order_by_po(po_number):
    """Get an order by PO number"""
    db = get_db_session()
    try:
        order = db.query(Order).filter(Order.po_number == po_number).first()
        return order
    finally:
        db.close()

def add_order(po_number, buyer_id, order_date, delivery_date, total_quantity=0):
    """Add a new order to the database"""
    db = get_db_session()
    try:
        order = Order(
            po_number=po_number,
            buyer_id=buyer_id,
            order_date=order_date,
            delivery_date=delivery_date,
            total_quantity=total_quantity
        )
        db.add(order)
        db.commit()
        return order
    finally:
        db.close()

def update_order_status(order_id, status):
    """Update the status of an order"""
    db = get_db_session()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            return True
        return False
    finally:
        db.close()

# ===== Style Operations =====
def get_styles_by_order(order_id):
    """Get all styles for a specific order"""
    db = get_db_session()
    try:
        styles = db.query(Style).filter(Style.order_id == order_id).all()
        return styles
    finally:
        db.close()

def add_style(order_id, style_number, description, category, color, size_breakdown, quantity):
    """Add a new style to the database"""
    db = get_db_session()
    try:
        # Convert size breakdown to JSON string if it's not already
        if isinstance(size_breakdown, dict):
            size_breakdown = json.dumps(size_breakdown)
            
        style = Style(
            order_id=order_id,
            style_number=style_number,
            description=description,
            category=category,
            color=color,
            size_breakdown=size_breakdown,
            quantity=quantity
        )
        db.add(style)
        db.commit()
        return style
    finally:
        db.close()

def update_style_status(style_id, status):
    """Update the status of a style"""
    db = get_db_session()
    try:
        style = db.query(Style).filter(Style.id == style_id).first()
        if style:
            style.status = status
            db.commit()
            return True
        return False
    finally:
        db.close()

# ===== Material Operations =====
def get_materials_by_style(style_id):
    """Get all materials for a specific style"""
    db = get_db_session()
    try:
        materials = db.query(Material).filter(Material.style_id == style_id).all()
        return materials
    finally:
        db.close()

def add_material(style_id, name, material_type, unit, required_quantity):
    """Add a new material to the database"""
    db = get_db_session()
    try:
        material = Material(
            style_id=style_id,
            name=name,
            type=material_type,
            unit=unit,
            required_quantity=required_quantity,
            status='Pending'
        )
        db.add(material)
        db.commit()
        return material
    finally:
        db.close()

def update_material_status(material_id, status, **kwargs):
    """Update the status and other fields of a material"""
    db = get_db_session()
    try:
        material = db.query(Material).filter(Material.id == material_id).first()
        if material:
            material.status = status
            # Update other fields if provided
            for key, value in kwargs.items():
                if hasattr(material, key):
                    setattr(material, key, value)
            db.commit()
            return True
        return False
    finally:
        db.close()

# ===== Production Line Operations =====
def get_all_production_lines():
    """Get all production lines from the database"""
    db = get_db_session()
    try:
        lines = db.query(ProductionLine).all()
        return lines
    finally:
        db.close()

def add_production_line(name, capacity, supervisor=None):
    """Add a new production line to the database"""
    db = get_db_session()
    try:
        line = ProductionLine(
            name=name,
            capacity=capacity,
            supervisor=supervisor
        )
        db.add(line)
        db.commit()
        return line
    finally:
        db.close()

# ===== Line Allocation Operations =====
def get_allocations_by_line(line_id):
    """Get all allocations for a specific production line"""
    db = get_db_session()
    try:
        allocations = db.query(LineAllocation).filter(LineAllocation.line_id == line_id).all()
        return allocations
    finally:
        db.close()

def allocate_style_to_line(line_id, style_id, start_date, end_date, planned_quantity, remarks=None):
    """Allocate a style to a production line"""
    db = get_db_session()
    try:
        allocation = LineAllocation(
            line_id=line_id,
            style_id=style_id,
            start_date=start_date,
            end_date=end_date,
            planned_quantity=planned_quantity,
            remarks=remarks
        )
        db.add(allocation)
        db.commit()
        return allocation
    finally:
        db.close()

# ===== Production Entry Operations =====
def get_production_entries_by_date_range(start_date, end_date):
    """Get all production entries within a date range"""
    db = get_db_session()
    try:
        entries = db.query(ProductionEntry).filter(
            ProductionEntry.date >= start_date,
            ProductionEntry.date <= end_date
        ).all()
        return entries
    finally:
        db.close()

def get_production_entries_by_style(style_id):
    """Get all production entries for a specific style"""
    db = get_db_session()
    try:
        entries = db.query(ProductionEntry).filter(ProductionEntry.style_id == style_id).all()
        return entries
    finally:
        db.close()

def add_production_entry(date, style_id, line_id, process, quantity, efficiency=None, defects=0, delay_reason=None, remarks=None):
    """Add a new production entry to the database"""
    db = get_db_session()
    try:
        entry = ProductionEntry(
            date=date,
            style_id=style_id,
            line_id=line_id,
            process=process,
            quantity=quantity,
            efficiency=efficiency,
            defects=defects,
            delay_reason=delay_reason,
            remarks=remarks
        )
        db.add(entry)
        db.commit()
        return entry
    finally:
        db.close()

# ===== Dashboard Operations =====
def get_dashboard_data():
    """Get aggregate data for the dashboard"""
    db = get_db_session()
    try:
        # Total orders
        total_orders = db.query(Order).count()
        
        # Orders by status
        orders_by_status = db.query(Order.status, db.func.count(Order.id)).group_by(Order.status).all()
        orders_by_status_dict = {status: count for status, count in orders_by_status}
        
        # Production data for the last 30 days
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        production_entries = db.query(ProductionEntry).filter(
            ProductionEntry.date >= thirty_days_ago,
            ProductionEntry.date <= today
        ).all()
        
        # Aggregated production metrics
        total_cutting = sum(entry.quantity for entry in production_entries if entry.process == 'Cutting')
        total_stitching = sum(entry.quantity for entry in production_entries if entry.process == 'Stitching')
        total_packing = sum(entry.quantity for entry in production_entries if entry.process == 'Packing')
        total_dispatch = sum(entry.quantity for entry in production_entries if entry.process == 'Dispatch')
        
        # Calculate daily production for the last 30 days
        daily_production = {}
        for i in range(30):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            daily_entries = [entry for entry in production_entries if entry.date == date]
            
            daily_production[date_str] = {
                'Cutting': sum(entry.quantity for entry in daily_entries if entry.process == 'Cutting'),
                'Stitching': sum(entry.quantity for entry in daily_entries if entry.process == 'Stitching'),
                'Packing': sum(entry.quantity for entry in daily_entries if entry.process == 'Packing'),
                'Dispatch': sum(entry.quantity for entry in daily_entries if entry.process == 'Dispatch')
            }
        
        # Line efficiency data
        line_efficiency = {}
        lines = db.query(ProductionLine).all()
        for line in lines:
            line_entries = [entry for entry in production_entries if entry.line_id == line.id]
            if line_entries:
                avg_efficiency = sum(entry.efficiency or 0 for entry in line_entries) / len(line_entries)
                line_efficiency[line.name] = avg_efficiency
            else:
                line_efficiency[line.name] = 0
        
        # Material status
        material_status_counts = db.query(Material.status, db.func.count(Material.id)).group_by(Material.status).all()
        material_status_dict = {status: count for status, count in material_status_counts}
        
        return {
            'total_orders': total_orders,
            'orders_by_status': orders_by_status_dict,
            'production_summary': {
                'total_cutting': total_cutting,
                'total_stitching': total_stitching,
                'total_packing': total_packing,
                'total_dispatch': total_dispatch
            },
            'daily_production': daily_production,
            'line_efficiency': line_efficiency,
            'material_status': material_status_dict
        }
    finally:
        db.close()

# ===== Excel Import Functions =====
def import_orders_from_excel(file_path):
    """Import orders and styles from an Excel file"""
    try:
        # Read the Excel file
        orders_df = pd.read_excel(file_path, sheet_name='Orders')
        styles_df = pd.read_excel(file_path, sheet_name='Styles')
        
        # Process orders
        db = get_db_session()
        try:
            for _, row in orders_df.iterrows():
                # Check if buyer exists, create if not
                buyer = db.query(Buyer).filter(Buyer.name == row['buyer_name']).first()
                if not buyer:
                    buyer = Buyer(name=row['buyer_name'])
                    db.add(buyer)
                    db.flush()  # Get the buyer ID
                
                # Check if order already exists
                existing_order = db.query(Order).filter(Order.po_number == row['po_number']).first()
                if not existing_order:
                    order = Order(
                        po_number=row['po_number'],
                        buyer_id=buyer.id,
                        order_date=row['order_date'],
                        delivery_date=row['delivery_date'],
                        total_quantity=row['total_quantity'],
                        status=row['status']
                    )
                    db.add(order)
                    db.flush()  # Get the order ID
                else:
                    order = existing_order
                
                # Process styles for this order
                order_styles = styles_df[styles_df['po_number'] == row['po_number']]
                for _, style_row in order_styles.iterrows():
                    # Check if style already exists
                    existing_style = db.query(Style).filter(
                        (Style.order_id == order.id) & 
                        (Style.style_number == style_row['style_number'])
                    ).first()
                    
                    if not existing_style:
                        # Convert size_breakdown to a JSON string
                        size_breakdown = {}
                        for size_col in ['XS', 'S', 'M', 'L', 'XL', 'XXL']:
                            if size_col in style_row and not pd.isna(style_row[size_col]):
                                size_breakdown[size_col] = int(style_row[size_col])
                        
                        style = Style(
                            order_id=order.id,
                            style_number=style_row['style_number'],
                            description=style_row['description'],
                            category=style_row['category'],
                            color=style_row['color'],
                            size_breakdown=json.dumps(size_breakdown),
                            quantity=style_row['quantity'],
                            status=style_row['status']
                        )
                        db.add(style)
            
            db.commit()
            return True, "Orders and styles imported successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error importing data: {str(e)}"
        finally:
            db.close()
    except Exception as e:
        return False, f"Error reading Excel file: {str(e)}"

def import_materials_from_excel(file_path):
    """Import materials from an Excel file"""
    try:
        # Read the Excel file
        materials_df = pd.read_excel(file_path, sheet_name='Materials')
        
        # Process materials
        db = get_db_session()
        try:
            for _, row in materials_df.iterrows():
                # Get the style
                style = db.query(Style).filter(Style.style_number == row['style_number']).first()
                if not style:
                    continue  # Skip if style doesn't exist
                
                # Check if material already exists
                existing_material = db.query(Material).filter(
                    (Material.style_id == style.id) & 
                    (Material.name == row['material_name']) & 
                    (Material.type == row['material_type'])
                ).first()
                
                if not existing_material:
                    material = Material(
                        style_id=style.id,
                        name=row['material_name'],
                        type=row['material_type'],
                        unit=row['unit'],
                        required_quantity=row['required_quantity'],
                        received_quantity=row.get('received_quantity', 0),
                        issued_quantity=row.get('issued_quantity', 0),
                        status=row['status'],
                        po_number=row.get('po_number'),
                        po_date=row.get('po_date'),
                        expected_delivery=row.get('expected_delivery'),
                        actual_delivery=row.get('actual_delivery'),
                        remarks=row.get('remarks')
                    )
                    db.add(material)
            
            db.commit()
            return True, "Materials imported successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error importing materials: {str(e)}"
        finally:
            db.close()
    except Exception as e:
        return False, f"Error reading Excel file: {str(e)}"

def import_production_from_excel(file_path):
    """Import production entries from an Excel file"""
    try:
        # Read the Excel file
        production_df = pd.read_excel(file_path, sheet_name='Production')
        
        # Process production entries
        db = get_db_session()
        try:
            for _, row in production_df.iterrows():
                # Get the style
                style = db.query(Style).filter(Style.style_number == row['style_number']).first()
                if not style:
                    continue  # Skip if style doesn't exist
                
                # Get the production line
                line = db.query(ProductionLine).filter(ProductionLine.name == row['line_name']).first()
                if not line:
                    # Create the line if it doesn't exist
                    line = ProductionLine(
                        name=row['line_name'],
                        capacity=row.get('capacity', 0)
                    )
                    db.add(line)
                    db.flush()  # Get the line ID
                
                # Check if entry already exists
                existing_entry = db.query(ProductionEntry).filter(
                    (ProductionEntry.date == row['date']) & 
                    (ProductionEntry.style_id == style.id) & 
                    (ProductionEntry.line_id == line.id) & 
                    (ProductionEntry.process == row['process'])
                ).first()
                
                if not existing_entry:
                    entry = ProductionEntry(
                        date=row['date'],
                        style_id=style.id,
                        line_id=line.id,
                        process=row['process'],
                        quantity=row['quantity'],
                        efficiency=row.get('efficiency'),
                        defects=row.get('defects', 0),
                        delay_reason=row.get('delay_reason'),
                        remarks=row.get('remarks')
                    )
                    db.add(entry)
            
            db.commit()
            return True, "Production entries imported successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error importing production entries: {str(e)}"
        finally:
            db.close()
    except Exception as e:
        return False, f"Error reading Excel file: {str(e)}"