import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_product_catalog():
    """Display the product catalog page"""
    
    st.title("Product Catalog")
    
    st.markdown("""
    Browse our catalog of ready-made styles for bulk ordering. Select a category and product type to explore options.
    All products can be customized to meet your specific requirements.
    """)
    
    # Category filter
    category = st.radio(
        "Select Category:",
        ["Tops", "Bottoms"],
        horizontal=True
    )
    
    # Sub-category based on main category
    if category == "Tops":
        subcategories = ["Denims", "Non-Denims", "Knits"]
    else:  # Bottoms
        subcategories = ["Denims", "Non-Denims", "Knits"]
    
    subcategory = st.selectbox("Select Sub-Category:", subcategories)
    
    # Product type based on category and subcategory
    product_types = get_product_types(category, subcategory)
    
    # Create grid layout for products
    st.subheader(f"{category} - {subcategory}")
    
    # Display products in a grid (3 columns)
    cols = st.columns(3)
    
    for i, product in enumerate(product_types):
        with cols[i % 3]:
            st.write(f"### {product['name']}")
            st.image(product['image'], use_column_width=True)
            st.write(f"**Base Fabric:** {product['fabric']}")
            st.write(f"**MOQ:** {product['moq']} pcs")
            
            if st.button(f"View Details", key=f"view_{i}"):
                st.session_state.selected_product = product
                st.session_state.page = 'product_detail'
                st.rerun()
            
            st.markdown("---")

    # Quick filters
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.multiselect(
                "Fabric Types:",
                ["Cotton", "Polyester", "Cotton-Poly Blend", "Denim", "Twill", "Jersey"]
            )
            
            st.slider(
                "Price Range (per piece):",
                min_value=5,
                max_value=50,
                value=(10, 30),
                step=5
            )
        
        with col2:
            st.multiselect(
                "Available Finishes:",
                ["Stone Wash", "Enzyme Wash", "Garment Dye", "Pigment Dye", "Raw/Unwashed"]
            )
            
            st.slider(
                "MOQ Range:",
                min_value=100,
                max_value=1000,
                value=(100, 500),
                step=100
            )
    
def get_product_types(category, subcategory):
    """Get product types based on category and subcategory"""
    
    # Mock product data for demonstration
    if category == "Tops":
        if subcategory == "Denims":
            return [
                {
                    "id": "TD001",
                    "name": "Classic Denim Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "10oz Indigo Denim",
                    "moq": 300,
                    "description": "Classic denim shirt with button-down front and collar. Available in various washes.",
                    "price_range": "$15-20",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "wash_options": ["Stone Wash", "Acid Wash", "Raw Denim"]
                },
                {
                    "id": "TD002",
                    "name": "Western Denim Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "8oz Light Denim",
                    "moq": 250,
                    "description": "Western style denim shirt with snap buttons and yoke detail.",
                    "price_range": "$18-22",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "wash_options": ["Stone Wash", "Bleach Wash"]
                },
                {
                    "id": "TD003",
                    "name": "Denim Jacket",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "12oz Heavy Denim",
                    "moq": 200,
                    "description": "Classic denim jacket with button front and chest pockets.",
                    "price_range": "$25-30",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "wash_options": ["Stone Wash", "Acid Wash", "Raw Denim", "Distressed"]
                }
            ]
        elif subcategory == "Non-Denims":
            return [
                {
                    "id": "TN001",
                    "name": "Oxford Button-Down Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "100% Cotton Oxford",
                    "moq": 300,
                    "description": "Classic oxford button-down shirt suitable for casual and semi-formal wear.",
                    "price_range": "$12-16",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["White", "Blue", "Pink", "Grey"]
                },
                {
                    "id": "TN002",
                    "name": "Flannel Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "Cotton Flannel",
                    "moq": 250,
                    "description": "Brushed cotton flannel shirt with button front, perfect for cooler weather.",
                    "price_range": "$14-18",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "pattern_options": ["Check", "Plaid", "Solid"]
                },
                {
                    "id": "TN003",
                    "name": "Linen Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "100% Linen",
                    "moq": 200,
                    "description": "Lightweight linen shirt, perfect for summer collections.",
                    "price_range": "$18-22",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["White", "Beige", "Light Blue", "Olive"]
                }
            ]
        else:  # Knits
            return [
                {
                    "id": "TK001",
                    "name": "Basic Crew Neck T-Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "180 GSM Cotton Jersey",
                    "moq": 500,
                    "description": "Essential crew neck t-shirt in regular fit.",
                    "price_range": "$6-9",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["White", "Black", "Grey", "Navy", "More"]
                },
                {
                    "id": "TK002",
                    "name": "Polo Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "220 GSM Pique Knit",
                    "moq": 300,
                    "description": "Classic polo shirt with collar and button placket.",
                    "price_range": "$10-14",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["White", "Black", "Navy", "Red", "More"]
                },
                {
                    "id": "TK003",
                    "name": "Henley Neck T-Shirt",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "200 GSM Cotton Slub",
                    "moq": 300,
                    "description": "Henley style t-shirt with button placket detail.",
                    "price_range": "$8-12",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["White", "Black", "Grey", "Olive", "More"]
                }
            ]
    else:  # Bottoms
        if subcategory == "Denims":
            return [
                {
                    "id": "BD001",
                    "name": "Classic 5-Pocket Jeans",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "12oz Stretch Denim",
                    "moq": 300,
                    "description": "Traditional 5-pocket jeans in straight fit design.",
                    "price_range": "$15-20",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "wash_options": ["Stone Wash", "Acid Wash", "Raw Denim", "Rinse Wash"]
                },
                {
                    "id": "BD002",
                    "name": "Slim Fit Jeans",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "10oz Comfort Stretch Denim",
                    "moq": 300,
                    "description": "Modern slim fit jeans with slight stretch for comfort.",
                    "price_range": "$16-22",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "wash_options": ["Stone Wash", "Acid Wash", "Vintage Wash"]
                },
                {
                    "id": "BD003",
                    "name": "Denim Shorts",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "10oz Denim",
                    "moq": 250,
                    "description": "Classic denim shorts in mid-length style.",
                    "price_range": "$12-16",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "wash_options": ["Stone Wash", "Bleach Wash", "Distressed"]
                }
            ]
        elif subcategory == "Non-Denims":
            return [
                {
                    "id": "BN001",
                    "name": "Chino Pants",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "Cotton Twill",
                    "moq": 300,
                    "description": "Classic chino pants in regular fit with flat front.",
                    "price_range": "$14-18",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "color_options": ["Khaki", "Navy", "Olive", "Grey", "Black"]
                },
                {
                    "id": "BN002",
                    "name": "Cargo Pants",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "Cotton Canvas",
                    "moq": 250,
                    "description": "Utility cargo pants with side pockets and relaxed fit.",
                    "price_range": "$18-24",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "color_options": ["Khaki", "Olive", "Black", "Grey"]
                },
                {
                    "id": "BN003",
                    "name": "Drawstring Linen Pants",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "Cotton-Linen Blend",
                    "moq": 200,
                    "description": "Lightweight casual pants with drawstring waist in linen blend fabric.",
                    "price_range": "$16-20",
                    "available_sizes": ["30", "32", "34", "36", "38", "40"],
                    "color_options": ["White", "Beige", "Light Blue", "Grey"]
                }
            ]
        else:  # Knits
            return [
                {
                    "id": "BK001",
                    "name": "Jersey Joggers",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "300 GSM Cotton Fleece",
                    "moq": 300,
                    "description": "Classic joggers with elastic waistband and cuffs.",
                    "price_range": "$12-16",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["Grey Melange", "Black", "Navy", "Charcoal"]
                },
                {
                    "id": "BK002",
                    "name": "Sweatpants",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "320 GSM Brushed Fleece",
                    "moq": 250,
                    "description": "Comfortable sweatpants with drawstring waist and side pockets.",
                    "price_range": "$14-18",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["Grey Melange", "Black", "Navy", "Olive"]
                },
                {
                    "id": "BK003",
                    "name": "Knit Shorts",
                    "image": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg",
                    "fabric": "240 GSM French Terry",
                    "moq": 300,
                    "description": "Casual knit shorts with elastic waistband and drawstring.",
                    "price_range": "$10-14",
                    "available_sizes": ["S", "M", "L", "XL", "XXL"],
                    "color_options": ["Grey Melange", "Black", "Navy", "Olive"]
                }
            ]