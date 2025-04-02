import streamlit as st

def main():
    st.title("Simple Test App")
    st.write("This is a basic Streamlit app with minimal dependencies.")
    
    if st.button("Click Me"):
        st.success("Button clicked successfully!")
    
    value = st.slider("Select a value", 0, 100, 50)
    st.write(f"Selected value: {value}")
    
    option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
    st.write(f"Selected option: {option}")

if __name__ == "__main__":
    main()