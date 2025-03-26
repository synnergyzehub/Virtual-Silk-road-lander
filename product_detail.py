import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_product_detail():
    """Display the product detail page"""
    
    if st.session_state.selected_product is None:
        st.error("Please select a product first")
        if st.button("Go to Product Catalog", use_container_width=True):
            st.session_state.page = 'product_catalog'
            st.rerun()
        return
    
    product = st.session_state.selected_product
    
    # Product header
    st.title(f"{product['name']} (ID: {product['id']})")
    
    # Layout with two columns
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Product image
        st.image(product['image'], use_column_width=True)
        
        # Quick specs as key-value pairs
        st.subheader("Product Specifications")
        st.write(f"**Base Fabric:** {product['fabric']}")
        st.write(f"**Minimum Order Quantity:** {product['moq']} pieces")
        st.write(f"**Price Range:** {product['price_range']} per piece")
        
        # Additional product details
        with st.expander("Product Description", expanded=True):
            st.write(product['description'])
    
    with col2:
        # Customization options
        st.subheader("Customize Your Order")
        
        # Fabric selection
        st.markdown("#### Fabric Options")
        fabric_options = ["Standard (as described)", "Premium Upgrade (+10%)", "Eco-Friendly Option (+15%)"]
        selected_fabric = st.selectbox("Select Fabric Type:", fabric_options)
        
        # Initialize variables to avoid LSP warnings
        selected_wash = None
        selected_color = None
        
        # Wash/Finish selection (if applicable)
        if 'wash_options' in product:
            st.markdown("#### Wash/Finish Options")
            selected_wash = st.selectbox("Select Wash/Finish:", product['wash_options'])
            # Store in session state
            st.session_state.current_selected_wash = selected_wash
        elif 'color_options' in product:
            st.markdown("#### Color Options")
            selected_color = st.selectbox("Select Base Color:", product['color_options'])
            # Store in session state
            st.session_state.current_selected_color = selected_color
        
        # Branding options
        st.markdown("#### Branding Options")
        branding_option = st.radio(
            "Select Branding Type:",
            ["Standard Woven Label", "Custom Branded Label (+$0.50/pc)", "No Branding (-$0.25/pc)"]
        )
        
        # Size & Quantity Grid
        st.markdown("#### Size Distribution")
        st.write("Enter quantity for each size (minimum total: " + str(product['moq']) + " pcs)")
        
        # Initialize variables to avoid LSP warnings
        size_quantities = {}
        total_quantity = product['moq']  # Default value
        
        # Create size distribution form
        if 'available_sizes' in product:
            sizes = product['available_sizes']
            
            # Create columns for size inputs
            size_cols = st.columns(len(sizes))
            
            # Create quantity input for each size
            for i, size in enumerate(sizes):
                with size_cols[i]:
                    size_quantities[size] = st.number_input(
                        size, 
                        min_value=0, 
                        value=int(product['moq'] / len(sizes)) if size in ['M', 'L', '34', '36'] else 0, 
                        step=10
                    )
            
            # Calculate total quantity
            total_quantity = sum(size_quantities.values())
            
            # Store in session state for access elsewhere
            st.session_state.current_size_quantities = size_quantities
            st.session_state.current_total_quantity = total_quantity
            
            # Show total with validation
            if total_quantity < product['moq']:
                st.warning(f"Total quantity ({total_quantity}) is below the minimum order quantity ({product['moq']}).")
            else:
                st.success(f"Total quantity: {total_quantity} pcs")
        
        # Special instructions
        st.markdown("#### Special Instructions")
        special_instructions = st.text_area("Add any special requirements or notes for this order:", height=100)
        
        # Add to cart button
        if st.button("Add to Order", use_container_width=True):
            # Create order item
            order_item = {
                "product_id": product['id'],
                "product_name": product['name'],
                "fabric": selected_fabric,
                "branding": branding_option,
                "sizes": size_quantities if 'available_sizes' in product else {},
                "total_quantity": total_quantity if 'available_sizes' in product else product['moq'],
                "special_instructions": special_instructions,
                "base_price": product['price_range']
            }
            
            # Add wash/color if applicable
            if 'wash_options' in product:
                order_item["wash"] = selected_wash
            elif 'color_options' in product:
                order_item["color"] = selected_color
            
            # Add to cart
            if 'cart' not in st.session_state:
                st.session_state.cart = []
            
            st.session_state.cart.append(order_item)
            st.session_state.page = 'order_booking'
            st.rerun()
    
    # Product details and specs section
    st.markdown("---")
    st.subheader("Detailed Specifications")
    
    tabs = st.tabs(["Materials & Construction", "Sizing Guide", "Production Timeline"])
    
    with tabs[0]:
        st.markdown("""
        ### Materials & Construction
        
        **Main Fabric:**
        - Type: """ + product['fabric'] + """
        - Composition: Varies based on selected option
        - Origin: Imported or locally sourced depending on availability
        
        **Construction Details:**
        - Industry standard stitching with reinforced seams
        - Double-needle construction for durability
        - Pre-shrunk fabric available on request
        """)
    
    with tabs[1]:
        # Sample size chart based on product type
        if any(x in product['id'] for x in ['T', 'TK']):  # Tops
            size_data = {
                "Size": ["S", "M", "L", "XL", "XXL"],
                "Chest (inches)": [38, 40, 42, 44, 46],
                "Length (inches)": [27, 28, 29, 30, 31],
                "Sleeve (inches)": [8, 8.5, 9, 9.5, 10]
            }
        else:  # Bottoms
            size_data = {
                "Size": ["30", "32", "34", "36", "38", "40"],
                "Waist (inches)": [30, 32, 34, 36, 38, 40],
                "Hip (inches)": [38, 40, 42, 44, 46, 48],
                "Inseam (inches)": [30, 31, 32, 33, 34, 34]
            }
        
        st.table(pd.DataFrame(size_data))
        
        st.markdown("""
        **Size Customization:**
        Custom sizing available for orders above 1000 pieces per size. Contact customer service for details.
        """)
    
    with tabs[2]:
        st.markdown("""
        ### Production & Delivery Timeline
        
        **Standard Production Timeline:**
        - Order confirmation: 2-3 business days
        - Sample approval: 7-10 business days
        - Production: 30-45 business days based on quantity
        - Quality check & packaging: 5-7 business days
        - Shipping: Depends on destination (typically 5-15 days)
        
        **Express Production:**
        Available for select products with a 20% rush fee. Reduces production time by 30%.
        """)
    
    # Related products
    st.markdown("---")
    st.subheader("You May Also Like")
    
    # Display related products in a row
    cols = st.columns(3)
    
    # Get product category and subcategory
    category = "Tops" if product['id'][0] == "T" else "Bottoms"
    subcategory = "Denims" if product['id'][1] == "D" else "Non-Denims" if product['id'][1] == "N" else "Knits"
    
    # Get related products (excluding current one)
    related_products = [p for p in get_related_products(category, subcategory) if p['id'] != product['id']][:3]
    
    for i, related in enumerate(related_products):
        with cols[i]:
            st.write(f"**{related['name']}**")
            st.image(related['image'], width=100)
            if st.button(f"View", key=f"related_{i}"):
                st.session_state.selected_product = related
                st.rerun()

def get_related_products(category, subcategory):
    """Get related products based on category and subcategory"""
    # For simplicity, we're using the same function from product_catalog.py
    from product_catalog import get_product_types
    return get_product_types(category, subcategory)