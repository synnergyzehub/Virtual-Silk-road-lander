import streamlit as st
import pandas as pd
import os

# Create necessary data directories
os.makedirs('data/ledger', exist_ok=True)
os.makedirs('data/imported', exist_ok=True)

def main():
    """
    Simplified Empire OS for diagnostic purposes
    """
    st.title("Empire OS - Simple Diagnostic Version")
    
    st.write("This is a simplified version of the app for diagnostic purposes.")
    
    # Test basic component rendering
    st.header("Basic Component Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Metrics Test")
        st.metric("Test Metric", 42, 3)
    
    with col2:
        st.subheader("Input Test")
        name = st.text_input("Enter your name")
        if name:
            st.write(f"Hello, {name}!")
    
    # Test data display
    st.header("Data Display Test")
    
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'London', 'Paris', 'Tokyo']
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df)
    
    # Test system info
    st.header("System Information")
    
    st.write(f"Current directory: {os.getcwd()}")
    import sys
    st.write(f"Python version: {sys.version}")
    
    # List important files
    st.header("Project Files")
    
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    file_df = pd.DataFrame({'Files': files})
    st.dataframe(file_df)
    
    # Show directory structure
    st.header("Directory Structure")
    
    try:
        # Check important directories
        core_exists = os.path.exists('core')
        data_exists = os.path.exists('data')
        modules_exists = os.path.exists('core/modules') if core_exists else False
        
        st.write(f"Core Directory Exists: {'✅' if core_exists else '❌'}")
        st.write(f"Data Directory Exists: {'✅' if data_exists else '❌'}")
        st.write(f"Modules Directory Exists: {'✅' if modules_exists else '❌'}")
    except Exception as e:
        st.error(f"Error checking directory structure: {str(e)}")

if __name__ == "__main__":
    main()