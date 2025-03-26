import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from visualization import calculate_moving_averages, calculate_rsi, create_candlestick_chart, create_technical_chart, create_rsi_chart

def show_retailer_analysis():
    """Display the ECG Market Health Check for major clothing retailers"""
    
    st.title("ECG Market Health Check")
    
    st.markdown("""
    <div style="background-color: #2E2E2E; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h3 style="color: #1E88E5;">ECG's Proprietary Market Intelligence</h3>
    <p>Access ECG's exclusive market health analysis of major clothing retailers to inform your strategic decisions. 
    Our proprietary insights into market trends and retailer performance help optimize your sourcing, production, and sales strategies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create layout
    tabs = st.tabs(["JC Penney Analysis", "ECG Retailer Comparison", "Industry Market Pulse"])
    
    # JC Penney Analysis tab
    with tabs[0]:
        show_jcpenney_analysis()
    
    # ECG Retailer Comparison tab
    with tabs[1]:
        show_retailer_comparison()
    
    # Industry Market Pulse tab
    with tabs[2]:
        show_industry_trends()
    
    # Market insights
    st.markdown("---")
    st.subheader("ECG's Strategic Market Insights")
    
    st.info("""
    **Strategic Considerations:**
    - Analyze retailer financial health before pursuing large orders
    - Track seasonal performance to understand optimal order timing
    - Monitor inventory levels and sales performance to gauge reorder potential
    """)

def show_jcpenney_analysis():
    """Show JC Penney specific analysis"""
    
    st.subheader("JC Penney Market Analysis")
    
    # Info about JC Penney current status
    st.markdown("""
    **Note:** Following bankruptcy reorganization, JC Penney is now privately held by Simon Property Group and Brookfield Asset Management. 
    This means direct stock data is no longer available through public markets since late 2020.
    
    The analysis below uses:
    1. Historical JC Penney data (when it was publicly traded as JCP)
    2. Simon Property Group data (SPG) as a proxy for current performance
    3. Industry metrics and comparisons with similar retailers
    """)
    
    # Analysis options
    analysis_options = st.radio(
        "Select Analysis Type:",
        ["Historical JCP Performance", "Simon Property Group (SPG) Analysis", "Proxy Analysis: Department Store Index"],
        horizontal=True
    )
    
    if analysis_options == "Historical JCP Performance":
        # Historical JCP data analysis
        st.subheader("JC Penney Historical Stock Performance (Pre-Bankruptcy)")
        
        # Date range selection for historical data
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2015, 1, 1))
        with col2:
            end_date = st.date_input("End Date", datetime(2020, 5, 15))
        
        # Get historical data
        if start_date < end_date:
            with st.spinner("Checking JC Penney data availability..."):
                # Show information about JC Penney's current status
                st.warning("JC Penney (JCP) is no longer publicly traded since their bankruptcy reorganization in 2020.")
                
                st.info("""
                **JC Penney Current Status:**
                
                - JC Penney was acquired by Simon Property Group and Brookfield Asset Management in late 2020
                - The company is now privately held and no longer trades on public markets
                - For current insights, we recommend analyzing the parent companies (Simon Property Group - SPG) 
                  and related department store retailers
                """)
                
                # Show key historical events anyway
                st.subheader("Key Historical Events")
                events = [
                    {"date": "2016-01-01", "event": "JC Penney completes sale-leaseback of home office campus in Plano, Texas"},
                    {"date": "2017-02-24", "event": "Announces plan to close 130-140 stores"},
                    {"date": "2018-05-17", "event": "CEO Marvin Ellison resigns"},
                    {"date": "2018-10-29", "event": "JC Penney names Jill Soltau as new CEO"},
                    {"date": "2019-02-28", "event": "Announces closure of additional 27 stores"},
                    {"date": "2020-05-15", "event": "JC Penney files for Chapter 11 bankruptcy protection"},
                    {"date": "2020-12-07", "event": "Simon Property Group and Brookfield Asset Management complete acquisition of JC Penney"},
                    {"date": "2021-03-02", "event": "JC Penney announces focus on omnichannel retail strategy"},
                    {"date": "2022-05-10", "event": "JC Penney launches new brand identity and store designs"}
                ]
                
                events_df = pd.DataFrame(events)
                events_df['date'] = pd.to_datetime(events_df['date'])
                events_df.set_index('date', inplace=True)
                
                # Display events that are within the selected date range
                filtered_events = events_df.loc[start_date:end_date]
                if not filtered_events.empty:
                    for idx, row in filtered_events.iterrows():
                        st.markdown(f"**{idx.strftime('%Y-%m-%d')}:** {row['event']}")
                else:
                    st.info("No major events in the selected date range.")
                
                # Suggest alternatives
                st.subheader("Suggested Alternatives")
                st.markdown("""
                Since JC Penney is no longer publicly traded, we recommend analyzing:
                
                1. **Simon Property Group (SPG)** - One of JC Penney's owners (select in the tab above)
                2. **Comparable department stores** - Use the "ECG Retailer Comparison" tab to analyze Macy's, Kohl's, etc.
                3. **Industry trends** - View broader retail industry metrics in the "Industry Market Pulse" tab
                """)
                
                # Try to get SPG data as a preview
                try:
                    st.subheader("Simon Property Group (SPG) Preview")
                    st.markdown("**Quick look at JC Penney's parent company performance:**")
                    
                    # Get recent SPG data
                    recent_date = min(end_date, datetime.now().date())
                    start_preview = (datetime.strptime(str(recent_date), "%Y-%m-%d") - timedelta(days=30)).date()
                    
                    spg_preview = yf.download("SPG", start=start_preview, end=recent_date)
                    if not spg_preview.empty:
                        # Create a simple preview chart
                        fig = px.line(
                            spg_preview['Adj Close'], 
                            title="Simon Property Group (SPG) - Recent Performance",
                            labels={"value": "Price ($)", "variable": ""},
                            template="plotly_dark"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.caption("Click 'Simon Property Group (SPG) Analysis' above for detailed analysis")
                except:
                    pass
        else:
            st.error("End date must be after start date.")
    
    elif analysis_options == "Simon Property Group (SPG) Analysis":
        # SPG Analysis (as JCP owner)
        st.subheader("Simon Property Group Analysis (JCP Parent Company)")
        
        # Date range selection for SPG data
        col1, col2 = st.columns(2)
        with col1:
            spg_start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
        with col2:
            spg_end_date = st.date_input("End Date", datetime.now())
        
        # Get SPG data
        if spg_start_date < spg_end_date:
            with st.spinner("Fetching SPG data..."):
                try:
                    # Get SPG data
                    spg_data = yf.download("SPG", start=spg_start_date, end=spg_end_date)
                    
                    if not spg_data.empty:
                        # Display basic info
                        display_stock_info(spg_data, "SPG")
                        
                        # Create technical analysis charts
                        spg_data_ma = calculate_moving_averages(spg_data)
                        spg_data_ma['RSI'] = calculate_rsi(spg_data)
                        
                        # Display charts
                        st.subheader("Technical Analysis")
                        st.plotly_chart(create_candlestick_chart(spg_data, "Simon Property Group Price (SPG)"), use_container_width=True)
                        st.plotly_chart(create_technical_chart(spg_data_ma, "Simon Property Group with Moving Averages"), use_container_width=True)
                        st.plotly_chart(create_rsi_chart(spg_data_ma, "Simon Property Group RSI"), use_container_width=True)
                        
                        # Relationship to JC Penney
                        st.subheader("Relationship to JC Penney")
                        st.markdown("""
                        Simon Property Group, along with Brookfield Asset Management, acquired JC Penney out of bankruptcy
                        in 2020. As a major mall operator, Simon had a vested interest in keeping JC Penney alive as an
                        anchor tenant in many of their properties. SPG's performance can provide insights into the retail
                        real estate market and potential foot traffic for department stores like JC Penney.
                        
                        **Key Considerations:**
                        - SPG's revenue is tied to the success of their mall tenants, including JC Penney stores
                        - Lease renegotiations and property redevelopments affect JC Penney store operations
                        - SPG's occupancy rates indicate overall health of physical retail
                        """)
                    else:
                        st.warning("No data available for SPG in the selected date range.")
                except Exception as e:
                    st.error(f"Error fetching SPG data: {e}")
        else:
            st.error("End date must be after start date.")
    
    else:  # Proxy Analysis: Department Store Index
        st.subheader("Department Store Industry Performance")
        st.markdown("Analyzing similar retailers as a proxy for JC Penney's current performance")
        
        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            proxy_start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
        with col2:
            proxy_end_date = st.date_input("End Date", datetime.now())
        
        # Select comparison retailers
        retailers = st.multiselect(
            "Select retailers for comparison:",
            ["M", "KSS", "DDS", "JWN", "XRT"],
            default=["M", "KSS", "JWN", "XRT"],
            help="M: Macy's, KSS: Kohl's, DDS: Dillard's, JWN: Nordstrom, XRT: S&P Retail ETF"
        )
        
        if retailers:
            # Get data for selected retailers
            if proxy_start_date < proxy_end_date:
                with st.spinner("Fetching retailer data..."):
                    try:
                        # Get data
                        retailer_data = yf.download(retailers, start=proxy_start_date, end=proxy_end_date)['Adj Close']
                        
                        if not retailer_data.empty:
                            # Normalize data
                            normalized_data = retailer_data.copy()
                            for ticker in normalized_data.columns:
                                normalized_data[ticker] = normalized_data[ticker] / normalized_data[ticker].iloc[0] * 100
                            
                            # Create comparison chart
                            fig = px.line(
                                normalized_data,
                                title="Department Store Comparison (Normalized to 100)",
                                labels={"value": "Normalized Price", "variable": "Retailer"},
                                template="plotly_dark"
                            )
                            
                            fig.update_layout(
                                height=500,
                                legend_title="Retailers",
                                hovermode="x unified"
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Industry analysis
                            st.subheader("Department Store Industry Analysis")
                            
                            # Calculate average performance
                            avg_perf = normalized_data.iloc[-1].mean() - 100
                            
                            # Performance metrics
                            st.metric(
                                "Industry Average Performance", 
                                f"{avg_perf:.2f}%", 
                                delta=f"{avg_perf:.2f}%"
                            )
                            
                            # Performance table
                            perf_data = {
                                "Retailer": [],
                                "Performance": [],
                                "Current Price": [],
                                "Volume": []
                            }
                            
                            # Get additional data for each retailer
                            for ticker in retailers:
                                try:
                                    curr_price = retailer_data[ticker].iloc[-1]
                                    perf = (normalized_data[ticker].iloc[-1] - 100)
                                    
                                    # Get volume data
                                    vol_data = yf.download(ticker, start=proxy_end_date - timedelta(days=5), end=proxy_end_date)
                                    avg_vol = vol_data['Volume'].mean() if not vol_data.empty else 0
                                    
                                    # Add to performance data
                                    perf_data["Retailer"].append(ticker)
                                    perf_data["Performance"].append(f"{perf:.2f}%")
                                    perf_data["Current Price"].append(f"${curr_price:.2f}")
                                    perf_data["Volume"].append(f"{int(avg_vol):,}")
                                except:
                                    pass
                            
                            # Display performance table
                            if perf_data["Retailer"]:
                                st.table(pd.DataFrame(perf_data))
                            
                            # JC Penney comparison insights
                            st.markdown("""
                            ### Implications for JC Penney
                            
                            Based on the performance of comparable department stores, we can infer potential trends for JC Penney:
                            
                            1. Department stores are facing significant challenges in the current retail environment
                            2. Online competition continues to put pressure on traditional retailers
                            3. Retailers with strong omnichannel strategies are showing more resilience
                            4. Location and real estate optimization is critical for success
                            
                            As JC Penney continues its post-bankruptcy transformation under Simon and Brookfield ownership,
                            these industry trends provide context for their potential performance and strategies.
                            """)
                        else:
                            st.warning("No data available for selected retailers in the date range.")
                    except Exception as e:
                        st.error(f"Error fetching retailer data: {e}")
            else:
                st.error("End date must be after start date.")
        else:
            st.warning("Please select at least one retailer for comparison.")

def show_retailer_comparison():
    """Show ECG's proprietary comparison between major retailers"""
    
    st.subheader("ECG Retailer Comparison Analysis")
    
    # Select retailers for comparison
    all_retailers = {
        "Department Stores": ["M", "KSS", "DDS", "JWN"],
        "Big Box": ["WMT", "TGT"],
        "Specialty Apparel": ["GPS", "URBN", "ANF", "AEO", "LEVI"],
        "Luxury": ["TPR", "CPRI", "RL"],
        "Off-Price": ["TJX", "ROST", "BURL"],
        "Athletic": ["NKE", "UAA", "LULU"],
        "E-commerce": ["AMZN", "ETSY", "W"],
        "Indices": ["XRT", "RTH", "VCR"]
    }
    
    # Retailer selection
    st.markdown("Select retailers to compare across different categories")
    
    selected_retailers = []
    for category, tickers in all_retailers.items():
        with st.expander(f"{category} Retailers"):
            for ticker in tickers:
                if st.checkbox(ticker, key=f"compare_{ticker}"):
                    selected_retailers.append(ticker)
    
    # Time period selection
    periods = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "Year to Date": "ytd",
        "1 Year": "1y",
        "3 Years": "3y",
        "5 Years": "5y"
    }
    
    selected_period = st.selectbox("Select Time Period", list(periods.keys()))
    period = periods[selected_period]
    
    # Analysis type
    analysis_type = st.radio(
        "Select Analysis Type",
        ["Price Performance", "Key Metrics", "Seasonal Analysis"],
        horizontal=True
    )
    
    if selected_retailers:
        if analysis_type == "Price Performance":
            st.subheader(f"Price Performance - {selected_period}")
            
            with st.spinner("Fetching price data..."):
                try:
                    # Get data
                    price_data = yf.download(selected_retailers, period=period)['Adj Close']
                    
                    if not price_data.empty:
                        # Normalize data for better visualization
                        norm_price_data = price_data.copy()
                        for col in norm_price_data.columns:
                            norm_price_data[col] = norm_price_data[col] / norm_price_data[col].iloc[0] * 100
                        
                        # Plot normalized performance
                        fig = px.line(
                            norm_price_data, 
                            title=f"Relative Price Performance (Base=100)",
                            labels={"value": "Relative Performance", "variable": "Retailer"},
                            template="plotly_dark"
                        )
                        
                        fig.update_layout(
                            height=500,
                            legend_title="Retailers",
                            hovermode="x unified"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Calculate performance metrics
                        returns = price_data.pct_change().dropna()
                        
                        # Volatility
                        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
                        
                        # Total return
                        total_return = (price_data.iloc[-1] / price_data.iloc[0] - 1) * 100
                        
                        # Create metrics table
                        metrics_df = pd.DataFrame({
                            "Total Return (%)": total_return.map(lambda x: f"{x:.2f}%"),
                            "Annualized Volatility (%)": volatility.map(lambda x: f"{x*100:.2f}%"),
                            "Current Price ($)": price_data.iloc[-1].map(lambda x: f"${x:.2f}")
                        })
                        
                        st.table(metrics_df)
                    else:
                        st.warning("No price data available for the selected retailers and time period.")
                except Exception as e:
                    st.error(f"Error fetching price data: {e}")
        
        elif analysis_type == "Key Metrics":
            st.subheader("Key Financial Metrics")
            
            with st.spinner("Fetching financial metrics..."):
                # Create metrics dataframe
                metrics = {
                    "Ticker": [],
                    "Market Cap": [],
                    "P/E Ratio": [],
                    "Dividend Yield (%)": [],
                    "Revenue Growth (%)": [],
                    "Profit Margin (%)": []
                }
                
                for ticker in selected_retailers:
                    try:
                        # Get stock info
                        stock = yf.Ticker(ticker)
                        info = stock.info
                        
                        # Add basic info
                        metrics["Ticker"].append(ticker)
                        
                        # Add market cap
                        market_cap = info.get("marketCap", None)
                        if market_cap:
                            if market_cap >= 1e9:
                                metrics["Market Cap"].append(f"${market_cap/1e9:.2f}B")
                            else:
                                metrics["Market Cap"].append(f"${market_cap/1e6:.2f}M")
                        else:
                            metrics["Market Cap"].append("N/A")
                        
                        # Add P/E
                        pe = info.get("trailingPE", None)
                        metrics["P/E Ratio"].append(f"{pe:.2f}" if pe else "N/A")
                        
                        # Add dividend yield
                        div_yield = info.get("dividendYield", None)
                        metrics["Dividend Yield (%)"].append(f"{div_yield*100:.2f}%" if div_yield else "N/A")
                        
                        # Add revenue growth
                        rev_growth = info.get("revenueGrowth", None)
                        metrics["Revenue Growth (%)"].append(f"{rev_growth*100:.2f}%" if rev_growth else "N/A")
                        
                        # Add profit margin
                        margin = info.get("profitMargins", None)
                        metrics["Profit Margin (%)"].append(f"{margin*100:.2f}%" if margin else "N/A")
                        
                    except Exception as e:
                        # Handle missing data
                        metrics["Ticker"].append(ticker)
                        metrics["Market Cap"].append("Error")
                        metrics["P/E Ratio"].append("Error")
                        metrics["Dividend Yield (%)"].append("Error")
                        metrics["Revenue Growth (%)"].append("Error")
                        metrics["Profit Margin (%)"].append("Error")
                
                # Display metrics table
                if metrics["Ticker"]:
                    metrics_df = pd.DataFrame(metrics)
                    st.table(metrics_df)
                else:
                    st.warning("No metrics data available for the selected retailers.")
        
        else:  # Seasonal Analysis
            st.subheader("Seasonal Performance Analysis")
            
            with st.spinner("Analyzing seasonal patterns..."):
                try:
                    # Get 5 years of historical data for seasonal analysis
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=5*365)
                    
                    seasonal_data = yf.download(selected_retailers, start=start_date, end=end_date)['Adj Close']
                    
                    if not seasonal_data.empty:
                        # Add month column for grouping
                        returns_data = seasonal_data.pct_change().dropna()
                        returns_data['Month'] = returns_data.index.month
                        
                        # Calculate average monthly returns
                        monthly_returns = {}
                        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                        
                        for ticker in selected_retailers:
                            ticker_returns = returns_data.groupby('Month')[ticker].mean() * 100  # Convert to percentage
                            monthly_returns[ticker] = ticker_returns.values
                        
                        # Create seasonal heatmap data
                        seasonal_df = pd.DataFrame(monthly_returns, index=month_names)
                        
                        # Create heatmap
                        fig = px.imshow(
                            seasonal_df.T,
                            labels=dict(x="Month", y="Retailer", color="Avg. Monthly Return (%)"),
                            x=month_names,
                            y=seasonal_df.columns,
                            color_continuous_scale="RdBu_r",
                            title="Average Monthly Returns by Retailer (%)"
                        )
                        
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Quarterly analysis
                        st.subheader("Quarterly Performance Patterns")
                        
                        # Create quarterly data
                        returns_data['Quarter'] = returns_data.index.quarter
                        quarterly_returns = {}
                        quarter_names = ["Q1", "Q2", "Q3", "Q4"]
                        
                        for ticker in selected_retailers:
                            ticker_returns = returns_data.groupby('Quarter')[ticker].mean() * 100
                            quarterly_returns[ticker] = ticker_returns.values
                        
                        quarterly_df = pd.DataFrame(quarterly_returns, index=quarter_names)
                        
                        # Create quarterly bar chart
                        fig = px.bar(
                            quarterly_df,
                            title="Average Quarterly Returns (%)",
                            labels={"value": "Return (%)", "variable": "Retailer"},
                            barmode="group",
                            template="plotly_dark"
                        )
                        
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Seasonal insights
                        st.markdown("""
                        ### Seasonal Retail Insights
                        
                        **Key Observations:**
                        - Q4 typically shows the strongest performance for most retailers due to holiday shopping
                        - Department stores often struggle in Q1 (post-holiday slump)
                        - Back-to-school season (late Q3) is important for apparel retailers
                        - Inventory management is crucial during seasonal transitions
                        
                        For optimal order planning, consider placing bulk orders 4-6 months ahead of peak selling seasons,
                        accounting for production and shipping lead times.
                        """)
                    else:
                        st.warning("Insufficient data for seasonal analysis of the selected retailers.")
                except Exception as e:
                    st.error(f"Error performing seasonal analysis: {e}")
    else:
        st.warning("Please select at least one retailer for comparison.")

def show_industry_trends():
    """Show ECG's proprietary industry market pulse"""
    
    st.subheader("Industry Market Pulse")
    
    # Industry metrics over time
    st.markdown("""
    ECG's proprietary Industry Market Pulse provides exclusive insights into retail industry trends, 
    helping inform strategic buying decisions and competitive positioning for the upcoming seasons.
    """)
    
    # Trend categories
    trend_categories = st.radio(
        "Select Trend Category:",
        ["Sales Trends", "E-commerce vs. Physical", "Consumer Spending", "Supply Chain Metrics"],
        horizontal=True
    )
    
    if trend_categories == "Sales Trends":
        # Sales trends analysis
        st.subheader("Retail Sales Trends")
        
        # Example retail sales data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Sample data for demonstration
        apparel_sales = {
            "2020": [95, 90, 70, 50, 60, 75, 80, 85, 87, 90, 95, 100],
            "2021": [90, 92, 95, 97, 100, 103, 105, 107, 110, 112, 118, 122],
            "2022": [115, 117, 120, 122, 125, 127, 130, 133, 135, 138, 142, 148],
            "2023": [140, 142, 144, 146, 145, 146, 148, 150, 152, 155, 160, 165],
            "2024": [155, 156, 158, 159, 160, 162, None, None, None, None, None, None]
        }
        
        # Create sales trend visualization
        fig = go.Figure()
        
        for year, sales in apparel_sales.items():
            fig.add_trace(go.Scatter(
                x=months,
                y=sales,
                mode='lines+markers',
                name=year,
                connectgaps=True
            ))
        
        fig.update_layout(
            title="U.S. Apparel Retail Sales Index (2019 = 100)",
            xaxis_title="Month",
            yaxis_title="Sales Index",
            template="plotly_dark",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sales trends by category
        st.subheader("Sales Trends by Category")
        
        # Example category data
        categories = ["Men's Apparel", "Women's Apparel", "Children's", "Accessories", "Footwear", "Athletic Wear"]
        
        category_growth = {
            "YoY Growth (%)": [2.3, 3.5, 4.2, 1.8, 5.6, 7.2],
            "5-Year CAGR (%)": [1.2, 1.8, 2.3, 0.9, 3.2, 5.8]
        }
        
        # Create category bar chart
        cat_df = pd.DataFrame(category_growth, index=categories)
        
        fig = px.bar(
            cat_df,
            title="Growth by Apparel Category",
            labels={"value": "Growth Rate (%)", "variable": "Metric"},
            barmode="group",
            template="plotly_dark"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal sales patterns
        st.subheader("Seasonal Sales Patterns")
        
        seasonal_data = {
            "Q1 (%)": [18, 20, 22, 19, 15, 16],
            "Q2 (%)": [22, 24, 25, 23, 20, 22],
            "Q3 (%)": [28, 26, 30, 24, 30, 32],
            "Q4 (%)": [32, 30, 23, 34, 35, 30]
        }
        
        seasonal_df = pd.DataFrame(seasonal_data, index=categories)
        
        fig = px.imshow(
            seasonal_df,
            labels=dict(x="Quarter", y="Category", color="Sales Distribution (%)"),
            x=list(seasonal_data.keys()),
            y=categories,
            color_continuous_scale="Viridis",
            title="Quarterly Sales Distribution by Category (%)"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    elif trend_categories == "E-commerce vs. Physical":
        # E-commerce trends
        st.subheader("E-commerce vs. Physical Retail Trends")
        
        # Example e-commerce penetration data
        years = list(range(2015, 2025))
        
        ecommerce_share = {
            "Apparel E-commerce Share (%)": [12, 15, 18, 21, 24, 34, 36, 38, 39, 41],
            "Physical Retail Share (%)": [88, 85, 82, 79, 76, 66, 64, 62, 61, 59]
        }
        
        # Create stacked area chart
        ecommerce_df = pd.DataFrame(ecommerce_share, index=years)
        
        fig = px.area(
            ecommerce_df,
            title="Apparel Retail Channel Mix (%)",
            labels={"value": "Share (%)", "variable": "Channel"},
            template="plotly_dark"
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Channel performance
        st.subheader("Channel Performance Metrics")
        
        # Performance metrics by channel
        channels = ["Department Stores", "Specialty Stores", "Off-Price", "Pure E-commerce", "Omnichannel"]
        
        channel_metrics = {
            "YoY Growth (%)": [-2.5, 1.2, 4.5, 6.8, 5.2],
            "Avg. Margin (%)": [30, 40, 25, 35, 38],
            "Customer Retention (%)": [60, 65, 70, 75, 80]
        }
        
        # Create metrics tables
        channel_df = pd.DataFrame(channel_metrics, index=channels)
        st.table(channel_df)
        
        # Omnichannel insights
        st.info("""
        **Omnichannel Strategy Insights:**
        
        The data shows retailers with strong omnichannel strategies (integrated online and physical presence)
        are outperforming pure-play retailers in both channels. JC Penney's post-bankruptcy strategy includes
        significant omnichannel investments, focusing on using stores as fulfillment centers for online orders.
        """)
    
    elif trend_categories == "Consumer Spending":
        # Consumer spending analysis
        st.subheader("Consumer Spending Patterns")
        
        # Consumer confidence vs. apparel spending
        quarters = ["2020 Q1", "2020 Q2", "2020 Q3", "2020 Q4", 
                   "2021 Q1", "2021 Q2", "2021 Q3", "2021 Q4",
                   "2022 Q1", "2022 Q2", "2022 Q3", "2022 Q4",
                   "2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4",
                   "2024 Q1", "2024 Q2"]
        
        confidence = [110, 85, 90, 95, 100, 105, 110, 115, 110, 105, 100, 95, 90, 85, 88, 90, 92, 95]
        spending = [100, 75, 85, 95, 100, 105, 110, 120, 115, 110, 108, 110, 105, 103, 105, 110, 108, 110]
        
        # Create dual-axis chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=quarters,
            y=confidence,
            name="Consumer Confidence Index",
            mode="lines+markers",
            line=dict(color="#1976D2")
        ))
        
        fig.add_trace(go.Scatter(
            x=quarters,
            y=spending,
            name="Apparel Spending Index",
            mode="lines+markers",
            line=dict(color="#43A047")
        ))
        
        fig.update_layout(
            title="Consumer Confidence vs. Apparel Spending",
            template="plotly_dark",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Income group spending analysis
        st.subheader("Spending by Income Segment")
        
        income_segments = ["Low Income", "Lower Middle", "Upper Middle", "High Income", "Luxury"]
        
        segment_trends = {
            "2020": [85, 82, 88, 90, 75],
            "2021": [90, 95, 100, 105, 95],
            "2022": [92, 97, 105, 110, 115],
            "2023": [95, 100, 108, 115, 120],
            "2024 YTD": [94, 98, 106, 112, 118]
        }
        
        # Create grouped bar chart
        segment_df = pd.DataFrame(segment_trends, index=income_segments)
        
        fig = px.bar(
            segment_df,
            title="Apparel Spending by Income Segment (Index: 2019=100)",
            labels={"value": "Spending Index", "variable": "Year"},
            barmode="group",
            template="plotly_dark"
        )
        
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        # Consumer behavior insights
        st.markdown("""
        ### Key Consumer Trends Impacting Retailers
        
        1. **Value-consciousness:** Even as the economy recovers, consumers remain price-sensitive
        2. **Quality over quantity:** Consumers buying fewer but better quality items
        3. **Sustainability focus:** Growing interest in sustainable and ethical production
        4. **Experiential retail:** Demand for enhanced in-store experiences
        5. **Personalization:** Expectation for customized products and experiences
        
        These trends affect product development, pricing strategies, and inventory planning
        for retailers like JC Penney, which is repositioning to attract mid-market consumers.
        """)
    
    else:  # Supply Chain Metrics
        # Supply chain analysis
        st.subheader("Supply Chain & Inventory Metrics")
        
        # Inventory trends
        quarters = ["2020 Q1", "2020 Q2", "2020 Q3", "2020 Q4", 
                   "2021 Q1", "2021 Q2", "2021 Q3", "2021 Q4",
                   "2022 Q1", "2022 Q2", "2022 Q3", "2022 Q4",
                   "2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4",
                   "2024 Q1", "2024 Q2"]
        
        inventory = [110, 130, 120, 100, 95, 100, 105, 95, 100, 110, 120, 125, 120, 110, 105, 100, 102, 105]
        turns = [3.8, 3.0, 3.2, 4.0, 4.2, 4.0, 3.8, 4.2, 4.0, 3.8, 3.6, 3.5, 3.6, 3.8, 4.0, 4.2, 4.1, 4.0]
        
        # Create dual-axis chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=quarters,
            y=inventory,
            name="Inventory Index",
            marker_color="#1976D2"
        ))
        
        fig.add_trace(go.Scatter(
            x=quarters,
            y=turns,
            name="Inventory Turns",
            mode="lines+markers",
            line=dict(color="#E53935"),
            yaxis="y2"
        ))
        
        fig.update_layout(
            title="Apparel Retailer Inventory Metrics",
            template="plotly_dark",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            yaxis=dict(title="Inventory Index (2019=100)"),
            yaxis2=dict(title="Inventory Turns", overlaying="y", side="right")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Lead time analysis
        st.subheader("Production & Shipping Lead Times")
        
        # Lead time data
        lead_times = {
            "Category": ["Standard Production", "Quick Response", "Shipping - Asia", "Shipping - LATAM", "Distribution"],
            "2019 (days)": [60, 30, 30, 15, 7],
            "2020 (days)": [90, 45, 45, 20, 10],
            "2021 (days)": [75, 40, 40, 18, 9],
            "2022 (days)": [65, 35, 35, 16, 8],
            "2023 (days)": [60, 30, 32, 15, 7],
            "2024 YTD (days)": [58, 28, 30, 14, 7]
        }
        
        lead_df = pd.DataFrame(lead_times)
        lead_df.set_index("Category", inplace=True)
        
        # Display lead time table
        st.table(lead_df)
        
        # Sourcing trends
        st.subheader("Sourcing Region Trends")
        
        # Sourcing data
        regions = ["China", "Vietnam", "Bangladesh", "India", "Indonesia", "LATAM", "Domestic"]
        
        region_share = {
            "2020 (%)": [35, 15, 12, 10, 8, 5, 15],
            "2021 (%)": [32, 16, 13, 11, 8, 5, 15],
            "2022 (%)": [30, 17, 14, 12, 8, 6, 13],
            "2023 (%)": [28, 18, 15, 12, 8, 7, 12],
            "2024 (%)": [25, 18, 16, 13, 9, 8, 11]
        }
        
        # Create stacked bar chart
        region_df = pd.DataFrame(region_share, index=regions)
        
        fig = px.bar(
            region_df,
            title="Apparel Sourcing by Region",
            labels={"value": "Share (%)", "variable": "Year"},
            template="plotly_dark"
        )
        
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        # Supply chain insights
        st.info("""
        **Supply Chain Strategy Insights:**
        
        1. Retailers are diversifying sourcing away from China to reduce risk
        2. Near-shoring (LATAM production) is growing to reduce lead times
        3. Post-pandemic logistics have stabilized but costs remain elevated
        4. Inventory management has become more critical for profitability
        5. Technology adoption in supply chain tracking is increasing
        
        These trends affect production planning, supplier selection, and overall supply chain strategy
        for retailers like JC Penney, which is balancing cost efficiency with speed-to-market.
        """)

def display_stock_info(stock_data, ticker):
    """Display basic stock information"""
    
    # Calculate key metrics
    current_price = stock_data['Adj Close'][-1]
    previous_price = stock_data['Adj Close'][-2]
    price_change = current_price - previous_price
    price_change_pct = (price_change / previous_price) * 100
    
    # 52-week high and low
    high_52week = stock_data['High'].rolling(window=252).max().iloc[-1]
    low_52week = stock_data['Low'].rolling(window=252).min().iloc[-1]
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"{ticker} Last Price",
            value=f"${current_price:.2f}",
            delta=f"{price_change:.2f} ({price_change_pct:.2f}%)"
        )
    
    with col2:
        vol = stock_data['Volume'][-1]
        avg_vol = stock_data['Volume'].rolling(window=10).mean().iloc[-1]
        vol_change = vol / avg_vol - 1
        
        st.metric(
            label="Volume",
            value=f"{int(vol):,}",
            delta=f"{vol_change:.2f}%"
        )
    
    with col3:
        st.metric(
            label="52-Week High",
            value=f"${high_52week:.2f}"
        )
    
    with col4:
        st.metric(
            label="52-Week Low",
            value=f"${low_52week:.2f}"
        )