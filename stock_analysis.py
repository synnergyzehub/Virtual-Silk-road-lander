import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

def fetch_stock_data(ticker, period="1y"):
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        # Get general info
        info = stock.info
        
        # Get historical data
        hist = stock.history(period=period)
        
        return {
            "info": info,
            "history": hist,
            "ticker": ticker
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def display_stock_info(stock_data):
    """Display basic stock information"""
    info = stock_data["info"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${info.get('currentPrice', info.get('regularMarketPrice', 'N/A')):.2f}",
            f"{info.get('regularMarketChangePercent', 0):.2f}%"
        )
    
    with col2:
        st.metric(
            "Market Cap", 
            f"${info.get('marketCap', 0) / 1_000_000_000:.2f}B"
        )
    
    with col3:
        st.metric(
            "52 Week Range", 
            f"${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f}"
        )
    
    # More detailed information
    col1, col2 = st.columns(2)
    
    with col1:
        metrics = {
            "P/E Ratio": info.get('trailingPE', 'N/A'),
            "EPS": info.get('trailingEps', 'N/A'),
            "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A',
            "Volume": f"{info.get('volume', 0):,}"
        }
        
        for label, value in metrics.items():
            st.text(f"{label}: {value}")
    
    with col2:
        metrics = {
            "Open": f"${info.get('regularMarketOpen', 'N/A')}",
            "High": f"${info.get('regularMarketDayHigh', 'N/A')}",
            "Low": f"${info.get('regularMarketDayLow', 'N/A')}",
            "Beta": info.get('beta', 'N/A'),
        }
        
        for label, value in metrics.items():
            st.text(f"{label}: {value}")

def show_stock_analysis():
    """Show the stock analysis page"""
    st.title("Stock Analysis")
    
    st.markdown("""
    Search for a stock by its ticker symbol to view financial data and metrics.
    
    Examples: AAPL (Apple), MSFT (Microsoft), AMZN (Amazon), GOOGL (Google), TSLA (Tesla)
    """)
    
    # Popular stocks for quick selection
    popular_stocks = {
        "Apple": "AAPL", 
        "Microsoft": "MSFT", 
        "Amazon": "AMZN", 
        "Google": "GOOGL", 
        "Tesla": "TSLA",
        "Netflix": "NFLX",
        "Meta": "META"
    }
    
    # Search/select stocks
    col1, col2 = st.columns([2, 3])
    
    with col1:
        selected_ticker = st.selectbox(
            "Select from popular stocks:",
            options=list(popular_stocks.keys()),
            format_func=lambda x: f"{x} ({popular_stocks[x]})"
        )
        ticker = popular_stocks[selected_ticker]
    
    with col2:
        custom_ticker = st.text_input("Or enter a custom ticker symbol:", "")
        if custom_ticker:
            ticker = custom_ticker.upper()
    
    # Time period selection
    period = st.select_slider(
        "Select time period:",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
        value="1y"
    )
    
    # Fetch data button
    if st.button("Analyze Stock", use_container_width=True):
        with st.spinner(f"Fetching data for {ticker}..."):
            stock_data = fetch_stock_data(ticker, period)
            
            if stock_data:
                st.session_state.stock_data = stock_data
                st.session_state.selected_stock = ticker
                
                # Display company name and summary
                st.subheader(f"{stock_data['info'].get('shortName', ticker)}")
                st.markdown(f"**Sector:** {stock_data['info'].get('sector', 'N/A')} | **Industry:** {stock_data['info'].get('industry', 'N/A')}")
                
                with st.expander("Company Summary", expanded=False):
                    st.markdown(stock_data['info'].get('longBusinessSummary', 'No summary available'))
                
                # Display financial info
                st.subheader("Key Financial Metrics")
                display_stock_info(stock_data)
                
                # Stock price chart
                st.subheader("Stock Price History")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=stock_data["history"].index,
                    y=stock_data["history"]["Close"],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='#1E88E5', width=2)
                ))
                
                fig.update_layout(
                    title=f"{ticker} Stock Price - {period}",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_dark",
                    height=500,
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Option to proceed to visualizations
                st.success("Stock data loaded successfully. Proceed to visualizations for more detailed analysis.")
                if st.button("Proceed to Visualizations", use_container_width=True):
                    st.session_state.page = 'visualization'
                    st.rerun()
