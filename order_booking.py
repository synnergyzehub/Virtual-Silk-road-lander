import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_order_booking():
    """Display the order booking page"""
    
    if not st.session_state.cart:
        st.error("Your order is empty. Please add products to your order first.")
        if st.button("Browse Products", use_container_width=True):
            st.session_state.page = 'product_catalog'
            st.rerun()
        return
    
    st.title("Order Summary & Booking")
    
    # Display order items
    st.subheader("Order Items")
    
    for i, item in enumerate(st.session_state.cart):
        with st.expander(f"{item['product_name']} (Qty: {item['total_quantity']})", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write(f"**Product ID:** {item['product_id']}")
                st.write(f"**Base Price:** {item['base_price']}")
                st.write(f"**Quantity:** {item['total_quantity']} pcs")
            
            with col2:
                st.write(f"**Fabric:** {item['fabric']}")
                
                if 'wash' in item:
                    st.write(f"**Wash/Finish:** {item['wash']}")
                elif 'color' in item:
                    st.write(f"**Color:** {item['color']}")
                
                st.write(f"**Branding:** {item['branding']}")
            
            # Size breakdown if available
            if item['sizes']:
                st.write("**Size Distribution:**")
                sizes_df = pd.DataFrame({
                    'Size': list(item['sizes'].keys()),
                    'Quantity': list(item['sizes'].values())
                })
                sizes_df = sizes_df[sizes_df['Quantity'] > 0]  # Show only sizes with quantities
                st.table(sizes_df)
            
            if item['special_instructions']:
                st.write(f"**Special Instructions:** {item['special_instructions']}")
            
            # Option to remove item
            if st.button(f"Remove Item", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    # Order summary
    st.markdown("---")
    st.subheader("Order Summary")
    
    total_quantity = sum(item['total_quantity'] for item in st.session_state.cart)
    total_items = len(st.session_state.cart)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Items", f"{total_items}")
    
    with col2:
        st.metric("Total Quantity", f"{total_quantity} pcs")
    
    with col3:
        st.metric("Estimated Production Time", "30-45 days")
    
    # Company information form
    st.markdown("---")
    st.subheader("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input("Company Name*")
        contact_person = st.text_input("Contact Person*")
        email = st.text_input("Email Address*")
    
    with col2:
        phone = st.text_input("Phone Number*")
        address = st.text_area("Business Address*", height=100)
    
    # Delivery preferences
    st.markdown("---")
    st.subheader("Delivery Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        shipping_method = st.selectbox(
            "Shipping Method*",
            ["Standard Sea Freight", "Express Air Freight (Additional Charges)", "Customer's Freight Forwarder"]
        )
        
        # Calculate default date (45 days from now)
        default_date = datetime.now() + timedelta(days=45)
        requested_delivery = st.date_input(
            "Requested Delivery Date*",
            value=default_date,
            min_value=datetime.now() + timedelta(days=30)
        )
    
    with col2:
        incoterms = st.selectbox(
            "Incoterms*",
            ["FOB", "CIF", "EXW", "DDP"]
        )
        
        destination_port = st.text_input("Destination Port/Address*")
    
    # Payment terms
    st.markdown("---")
    st.subheader("Payment Terms")
    
    payment_terms = st.selectbox(
        "Payment Terms*",
        ["30% Advance, 70% Before Shipment", "50% Advance, 50% Before Shipment", "100% LC at Sight", "Payment Against Documents"]
    )
    
    payment_method = st.selectbox(
        "Payment Method*",
        ["Bank Transfer", "Letter of Credit", "Bank Guarantee"]
    )
    
    # Additional comments
    st.markdown("---")
    additional_comments = st.text_area("Additional Comments or Special Requirements", height=100)
    
    # Terms and conditions checkbox
    st.markdown("---")
    terms_accepted = st.checkbox("I accept the terms and conditions for bulk ordering")
    
    # Submit button
    if st.button("Submit Order Inquiry", disabled=not terms_accepted, use_container_width=True):
        # Basic form validation
        if not (company_name and contact_person and email and phone and address and destination_port):
            st.error("Please fill in all required fields marked with *")
        else:
            # Save order details to session state
            st.session_state.order_details = {
                "company_name": company_name,
                "contact_person": contact_person,
                "email": email,
                "phone": phone,
                "address": address,
                "shipping_method": shipping_method,
                "requested_delivery": requested_delivery.strftime("%Y-%m-%d"),
                "incoterms": incoterms,
                "destination_port": destination_port,
                "payment_terms": payment_terms,
                "payment_method": payment_method,
                "additional_comments": additional_comments,
                "order_date": datetime.now().strftime("%Y-%m-%d"),
                "order_id": f"BH-{datetime.now().strftime('%Y%m%d')}-{total_items}"
            }
            
            st.session_state.order_submitted = True
            st.session_state.page = 'order_confirmation'
            st.rerun()
    
    # Continue shopping button
    st.markdown("---")
    if st.button("Add More Products", use_container_width=True):
        st.session_state.page = 'product_catalog'
        st.rerun()