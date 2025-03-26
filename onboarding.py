import streamlit as st

def show_onboarding():
    """Display the onboarding process for new users of the Buying House Portal"""
    
    st.title("Welcome to the Buying House Portal")
    
    # Introduction
    st.markdown("""
    ### Ready Styles. Bulk Orders. Tailored For You.
    
    Our platform helps you browse ready-made styles, customize them to your needs, and place bulk orders
    for your business. Follow our guided process to get the most out of this application.
    """)
    
    # Step 1
    with st.expander("Step 1: Browse Product Categories", expanded=True):
        st.markdown("""
        Start by browsing our extensive catalog of menswear products:
        
        - **Tops:** Shirts, T-shirts, Knit tops
        - **Bottoms:** Jeans, Chinos, Joggers
        
        Each category offers various fabrics, styles, and customization options.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/grid.svg", width=50)
    
    # Step 2
    with st.expander("Step 2: Customize Your Selection", expanded=True):
        st.markdown("""
        Customize your selected products with options like:
        
        - Fabric type and composition
        - Wash/finish options
        - Branding and labeling preferences
        - Size distribution and quantities
        
        Our platform allows for detailed customization to meet your exact requirements.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/edit-2.svg", width=50)
    
    # Step 3
    with st.expander("Step 3: Place Your Bulk Order", expanded=True):
        st.markdown("""
        Submit your order with all necessary details:
        
        - Company information
        - Delivery preferences
        - Payment terms
        - Special instructions
        
        We'll confirm your order and keep you updated on production status.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/shopping-bag.svg", width=50)
    
    # Ready to start
    st.markdown("---")
    st.markdown("### Ready to explore our catalog?")
    
    if st.button("Let's Get Started!", use_container_width=True):
        st.session_state.completed_onboarding = True
        st.session_state.page = 'product_catalog'
        st.rerun()
