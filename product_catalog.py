import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def show_product_catalog():
    """Display the product catalog page"""
    
    st.title("Product Catalog")
    
    # Interactive filters section with enhanced UI
    st.markdown("""
    <div style="background-color: #2E2E2E; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h3 style="color: #1E88E5;">Browse Our Catalog</h3>
    <p>Explore our extensive range of ready-made styles for bulk ordering. Use the filters below to find exactly what you need.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main filters in a visually appealing layout
    filter_col1, filter_col2 = st.columns([2, 3])
    
    with filter_col1:
        # Category selection with custom styling
        st.markdown("### Select Product Category")
        
        # Interactive category buttons with icons
        category_col1, category_col2 = st.columns(2)
        with category_col1:
            tops_selected = st.button(
                "👕 Tops", 
                help="Shirts, T-shirts, and other upper body garments",
                use_container_width=True,
                key="tops_button"
            )
        with category_col2:
            bottoms_selected = st.button(
                "👖 Bottoms", 
                help="Jeans, Trousers, Shorts and other lower body garments",
                use_container_width=True,
                key="bottoms_button"
            )
        
        # Set category based on button selection
        if 'catalog_category' not in st.session_state:
            st.session_state.catalog_category = "Tops"  # Default
        
        if tops_selected:
            st.session_state.catalog_category = "Tops"
        elif bottoms_selected:
            st.session_state.catalog_category = "Bottoms"
        
        category = st.session_state.catalog_category
        
        # Highlight selected category
        st.markdown(f"**Selected Category:** {category}")
        
        # Sub-category based on main category with more visually appealing UI
        st.markdown("### Select Sub-Category")
        
        if category == "Tops":
            subcategories = ["Denims", "Non-Denims", "Knits"]
        else:  # Bottoms
            subcategories = ["Denims", "Non-Denims", "Knits"]
        
        # Radio buttons with better spacing and styling
        subcategory = st.radio(
            "Filter by Material Type",
            subcategories,
            horizontal=True,
            label_visibility="collapsed"
        )
    
    with filter_col2:
        # Visual guide for what types of products are in each category
        st.markdown("### Product Guide")
        
        # Create a categorical color map
        if category == "Tops":
            guide_data = {
                "Type": ["Shirts", "T-Shirts", "Jackets", "Polos", "Henleys"],
                "Sub-Category": ["Non-Denims", "Knits", "Denims", "Knits", "Knits"],
                "Value": [30, 40, 20, 25, 15]  # For sizing circles
            }
            title = "Top Types by Sub-Category"
        else:  # Bottoms
            guide_data = {
                "Type": ["Jeans", "Chinos", "Shorts", "Joggers", "Cargo"],
                "Sub-Category": ["Denims", "Non-Denims", "Denims", "Knits", "Non-Denims"],
                "Value": [35, 25, 20, 30, 15]  # For sizing circles
            }
            title = "Bottom Types by Sub-Category"
        
        # Create interactive bubble chart
        fig = px.scatter(
            guide_data,
            x="Type",
            y="Sub-Category",
            size="Value",
            color="Sub-Category",
            color_discrete_map={"Denims": "#1976D2", "Non-Denims": "#43A047", "Knits": "#E53935"},
            size_max=50,
            hover_name="Type",
            title=title
        )
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(l=10, r=10, t=40, b=20),
            font=dict(size=12),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Get product types based on filters
    product_types = get_product_types(category, subcategory)
    
    # Create a metrics section to show available products
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric(label="Available Products", value=len(product_types))
    with metric_cols[1]:
        avg_moq = int(np.mean([p["moq"] for p in product_types]))
        st.metric(label="Average MOQ", value=f"{avg_moq} pcs")
    with metric_cols[2]:
        delivery_time = "30-45 days"
        st.metric(label="Avg. Production Time", value=delivery_time)
    with metric_cols[3]:
        st.metric(label="Customization Options", value="100%")
    
    # Create grid layout for products
    st.markdown("---")
    st.subheader(f"{category} - {subcategory}")
    
    # Enhanced product display with more interactive elements
    for i in range(0, len(product_types), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(product_types):
                product = product_types[i + j]
                with cols[j]:
                    # Create a card-like element
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                        <h3 style="color: #1E88E5;">{product['name']}</h3>
                        <p>ID: {product['id']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Use better images with proper sizing
                    st.image(product['image'], use_container_width=True)
                    
                    # More detailed product info with better formatting
                    st.markdown(f"""
                    <div style="background-color: #2E2E2E; padding: 10px; border-radius: 5px; margin: 10px 0;">
                        <p><b>Base Fabric:</b> {product['fabric']}</p>
                        <p><b>MOQ:</b> {product['moq']} pcs</p>
                        <p><b>Price Range:</b> {product['price_range']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quick preview of options
                    if 'wash_options' in product:
                        options = product['wash_options']
                        option_type = "Wash Options"
                    elif 'color_options' in product:
                        options = product['color_options']
                        option_type = "Color Options"
                    else:
                        options = []
                        option_type = ""
                    
                    if options:
                        st.markdown(f"**{option_type}:**")
                        option_cols = st.columns(len(options[:4]))  # Show up to 4 options
                        for k, option in enumerate(options[:4]):
                            option_cols[k].markdown(f"<div style='text-align: center; padding: 5px; background-color: #333; border-radius: 5px;'>{option}</div>", unsafe_allow_html=True)
                    
                    # Interactive buttons
                    button_cols = st.columns(2)
                    with button_cols[0]:
                        if st.button(f"🔍 View Details", key=f"view_{i+j}"):
                            st.session_state.selected_product = product
                            st.session_state.page = 'product_detail'
                            st.rerun()
                    
                    with button_cols[1]:
                        st.button(f"❤️ Save", key=f"save_{i+j}", help="Save this item to your favorites")
    
    # Advanced filtering options with more interactivity
    st.markdown("---")
    st.markdown("## Advanced Search & Filters")
    
    with st.expander("Show Advanced Filters", expanded=False):
        filter_cols = st.columns(3)
        
        with filter_cols[0]:
            st.markdown("### Fabric & Materials")
            
            fabric_types = st.multiselect(
                "Fabric Types:",
                ["Cotton", "Polyester", "Cotton-Poly Blend", "Denim", "Twill", "Jersey", 
                 "Linen", "Canvas", "French Terry", "Fleece"],
                help="Select multiple fabric types to filter products"
            )
            
            st.markdown("### Price Range")
            price_range = st.slider(
                "Price per piece (USD):",
                min_value=5,
                max_value=50,
                value=(10, 30),
                step=5,
                help="Filter products by price range"
            )
        
        with filter_cols[1]:
            st.markdown("### Production Specs")
            
            finish_types = st.multiselect(
                "Available Finishes:",
                ["Stone Wash", "Enzyme Wash", "Garment Dye", "Pigment Dye", "Raw/Unwashed",
                 "Acid Wash", "Bleach Wash", "Vintage Wash", "Distressed"],
                help="Select finishing options available for products"
            )
            
            moq_range = st.slider(
                "MOQ Range (pieces):",
                min_value=100,
                max_value=1000,
                value=(100, 500),
                step=50,
                help="Filter by minimum order quantity requirements"
            )
        
        with filter_cols[2]:
            st.markdown("### Additional Options")
            
            st.selectbox(
                "Sort By:",
                ["Popularity", "Price: Low to High", "Price: High to Low", "MOQ: Low to High", "Newest First"],
                help="Choose how to sort the product listing"
            )
            
            st.selectbox(
                "Customization Level:",
                ["All", "Basic", "Standard", "Premium", "Full Custom"],
                help="Filter by level of customization available"
            )
            
            st.checkbox("Only show in-stock fabrics", help="Show only products with immediately available fabrics")
            st.checkbox("Show eco-friendly options", help="Display only environmentally friendly product options")
    
    # Market trends section for added value
    st.markdown("---")
    st.subheader("Market Trends & Popular Choices")
    
    # Create a simple market trends visualization
    trend_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Denim": [100, 120, 140, 150, 170, 190],
        "Knits": [150, 140, 160, 170, 180, 200],
        "Non-Denim": [80, 100, 110, 120, 130, 135]
    }
    
    df_trends = pd.DataFrame(trend_data)
    df_trends_melted = pd.melt(
        df_trends, 
        id_vars=["Month"],
        value_vars=["Denim", "Knits", "Non-Denim"],
        var_name="Category",
        value_name="Orders"
    )
    
    fig = px.line(
        df_trends_melted,
        x="Month",
        y="Orders",
        color="Category",
        title="Product Category Trends (Last 6 Months)",
        color_discrete_map={"Denim": "#1976D2", "Knits": "#E53935", "Non-Denim": "#43A047"}
    )
    
    fig.update_layout(
        height=300,
        template="plotly_dark",
        xaxis_title="",
        yaxis_title="Order Volume (Normalized)",
        legend_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calendar hint for seasonal planning
    st.info("💡 **Seasonal Planning Tip:** Now is the perfect time to place orders for the Summer/Fall collection to ensure timely delivery.")
    
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