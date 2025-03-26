import streamlit as st

def show_onboarding():
    """Display the onboarding process for new users"""
    
    st.title("Welcome to the Stock Analysis Tool")
    
    # Introduction
    st.markdown("""
    ### Your path to smarter stock analysis
    
    This tool helps you analyze stocks with real-time data from Yahoo Finance.
    Follow our guided process to get the most out of this application.
    """)
    
    # Step 1
    with st.expander("Step 1: Search for Stocks", expanded=True):
        st.markdown("""
        Begin by searching for stocks using their ticker symbols (e.g., AAPL for Apple, MSFT for Microsoft).
        
        Our tool will fetch the latest financial data and show you key metrics to help you understand the company's performance.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/search.svg", width=50)
    
    # Step 2
    with st.expander("Step 2: Analyze Interactive Charts", expanded=True):
        st.markdown("""
        Explore interactive charts showing historical stock price trends.
        
        You can zoom, pan, and hover over data points to get detailed information.
        Compare performance over different time periods to spot trends.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/bar-chart-2.svg", width=50)
    
    # Step 3
    with st.expander("Step 3: Review Financial Indicators", expanded=True):
        st.markdown("""
        Dive deeper into financial indicators like:
        - Price-to-Earnings Ratio
        - Earnings Per Share
        - Market Capitalization
        - Volume
        
        These metrics help you make more informed investment decisions.
        """)
        st.image("https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/activity.svg", width=50)
    
    # Ready to start
    st.markdown("---")
    st.markdown("### Ready to explore?")
    
    if st.button("Let's Get Started!", use_container_width=True):
        st.session_state.completed_onboarding = True
        st.session_state.page = 'stock_analysis'
        st.rerun()
