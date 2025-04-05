import streamlit as st
import pandas as pd
import numpy as np

def main():
    """
    Minimal Voi Jeans Inventory App
    """
    st.set_page_config(
        page_title="Voi Jeans - Inventory Management",
        page_icon="👖",
        layout="wide"
    )
    
    st.title("Voi Jeans Dashboard")
    st.subheader("Inventory Management Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Inventory Value", "₹15,000,000", "+₹200,000")
    
    with col2:
        st.metric("Stock Turnover Rate", "2.75", "+0.25")
    
    with col3:
        st.metric("Active SKUs", "1,200", "+30")
    
    with col4:
        st.metric("Stores Covered", "120", "+2")
    
    # Simple data
    st.header("Inventory Data")
    
    data = pd.DataFrame({
        'Category': ['Jeans', 'T-Shirts', 'Shirts', 'Jackets', 'Accessories'],
        'Inventory Value': [5000000, 3000000, 2500000, 3500000, 1000000]
    })
    
    st.dataframe(data)
    
    st.write("This is a simplified version of the Voi Jeans inventory management app.")

if __name__ == "__main__":
    main()