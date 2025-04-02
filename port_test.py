import streamlit as st

def main():
    st.title("Streamlit Port 8080 Test")
    st.write("This is a Streamlit app running on port 8080.")
    
    st.write("If you can see this, Streamlit is working correctly on port 8080!")
    
    st.info("Current configuration: Running on port 8080")

if __name__ == "__main__":
    main()