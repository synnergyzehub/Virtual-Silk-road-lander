import streamlit as st

def main():
    """
    Super Simple Test App
    """
    st.title("Voi Jeans Inventory Management")
    st.write("A simple test of the Streamlit platform")
    
    # Simple interactive elements
    name = st.text_input("Enter your name:")
    if name:
        st.write(f"Hello, {name}!")
    
    st.write("---")
    
    # Simple dashboard display
    st.subheader("Sample Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Inventory", value="1,204 units", delta="43")
    with col2:
        st.metric(label="Sales", value="₹52,000", delta="-18%")
    with col3:
        st.metric(label="Returns", value="13", delta="-4")
    
    # Simple button
    if st.button("Generate Report"):
        st.success("Sample report generated!")

if __name__ == "__main__":
    main()