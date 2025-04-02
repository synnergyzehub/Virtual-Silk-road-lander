import streamlit as st

def main():
    st.title("Minimal Streamlit Test")
    st.write("This is a minimal Streamlit app to test if the server can run properly.")
    
    st.write("If you can see this, Streamlit is working correctly!")
    
    st.info("Current configuration:")
    st.code("""
[server]
headless = true
address = "0.0.0.0"
port = 5000
    """)

if __name__ == "__main__":
    main()