import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def calculate_moving_averages(df, windows=[20, 50, 200]):
    """Calculate moving averages for the stock data"""
    result = df.copy()
    for window in windows:
        result[f'MA{window}'] = result['Close'].rolling(window=window).mean()
    return result

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def create_candlestick_chart(df, title):
    """Create an interactive candlestick chart"""
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ))
    
    # Add volume as a bar chart at the bottom
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volume',
        marker=dict(color='rgba(128, 128, 128, 0.5)'),
        yaxis='y2'
    ))
    
    # Layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        height=600,
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[0, df['Volume'].max() * 5]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_technical_chart(df, title):
    """Create technical analysis chart with moving averages"""
    # Calculate moving averages
    df_ma = calculate_moving_averages(df)
    
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df_ma.index,
        y=df_ma['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1E88E5', width=2)
    ))
    
    # Add moving averages
    colors = ['#F44336', '#4CAF50', '#FF9800']
    for i, window in enumerate([20, 50, 200]):
        if f'MA{window}' in df_ma.columns:
            fig.add_trace(go.Scatter(
                x=df_ma.index,
                y=df_ma[f'MA{window}'],
                mode='lines',
                name=f'{window}-day MA',
                line=dict(color=colors[i], width=1.5, dash='dot')
            ))
    
    # Layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_rsi_chart(df, title):
    """Create RSI (Relative Strength Index) chart"""
    # Calculate RSI
    rsi = calculate_rsi(df)
    
    fig = go.Figure()
    
    # Add RSI line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=rsi,
        mode='lines',
        name='RSI',
        line=dict(color='#1E88E5', width=2)
    ))
    
    # Add overbought/oversold thresholds
    fig.add_shape(
        type="line",
        x0=df.index[0],
        y0=70,
        x1=df.index[-1],
        y1=70,
        line=dict(color="red", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=df.index[0],
        y0=30,
        x1=df.index[-1],
        y1=30,
        line=dict(color="green", width=1, dash="dash")
    )
    
    # Layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='RSI',
        template='plotly_dark',
        height=300,
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_returns_chart(df, title):
    """Create returns distribution chart"""
    # Calculate daily returns
    df_returns = df.copy()
    df_returns['Daily_Return'] = df_returns['Close'].pct_change() * 100
    df_returns = df_returns.dropna()
    
    fig = px.histogram(
        df_returns, 
        x='Daily_Return',
        nbins=50,
        title=title,
        labels={'Daily_Return': 'Daily Return (%)'},
        template='plotly_dark',
    )
    
    fig.add_vline(
        x=df_returns['Daily_Return'].mean(), 
        line_dash="dash", 
        line_color="white",
        annotation_text=f"Mean: {df_returns['Daily_Return'].mean():.2f}%",
        annotation_position="top right"
    )
    
    fig.update_layout(height=300)
    
    return fig

def show_visualization():
    """Show the visualization page"""
    if st.session_state.stock_data is None or st.session_state.selected_stock is None:
        st.error("Please select a stock first")
        if st.button("Go to Stock Selection", use_container_width=True):
            st.session_state.page = 'stock_analysis'
            st.rerun()
        return
    
    stock_data = st.session_state.stock_data
    ticker = st.session_state.selected_stock
    historical_data = stock_data["history"]
    
    st.title(f"Visualization: {stock_data['info'].get('shortName', ticker)} ({ticker})")
    
    # Price Chart Section
    st.subheader("Price Analysis")
    
    chart_type = st.radio(
        "Chart Type:", 
        ["Line Chart", "Candlestick Chart"], 
        horizontal=True
    )
    
    if chart_type == "Line Chart":
        fig = create_technical_chart(
            historical_data, 
            f"{ticker} Price with Moving Averages"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = create_candlestick_chart(
            historical_data, 
            f"{ticker} Candlestick Chart"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Technical Indicators Section
    st.subheader("Technical Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rsi_fig = create_rsi_chart(
            historical_data, 
            f"{ticker} RSI (Relative Strength Index)"
        )
        st.plotly_chart(rsi_fig, use_container_width=True)
    
    with col2:
        returns_fig = create_returns_chart(
            historical_data, 
            f"{ticker} Daily Returns Distribution"
        )
        st.plotly_chart(returns_fig, use_container_width=True)
    
    # Performance Summary
    st.subheader("Performance Summary")
    
    # Calculate performance metrics
    try:
        # Get first and last closing prices
        start_price = historical_data['Close'].iloc[0]
        end_price = historical_data['Close'].iloc[-1]
        
        # Calculate performance metrics
        total_return = ((end_price - start_price) / start_price) * 100
        daily_returns = historical_data['Close'].pct_change().dropna()
        annualized_return = daily_returns.mean() * 252 * 100
        volatility = daily_returns.std() * np.sqrt(252) * 100
        sharpe_ratio = annualized_return / volatility if volatility != 0 else 0
        max_drawdown = ((historical_data['Close'].cummax() - historical_data['Close']) / historical_data['Close'].cummax()).max() * 100
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Return", f"{total_return:.2f}%")
            st.metric("Annualized Return", f"{annualized_return:.2f}%")
        
        with col2:
            st.metric("Volatility (Annualized)", f"{volatility:.2f}%")
            st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        
        with col3:
            st.metric("Maximum Drawdown", f"{max_drawdown:.2f}%")
            st.metric("Average Daily Volume", f"{historical_data['Volume'].mean():.0f}")
    
    except Exception as e:
        st.error(f"Error calculating performance metrics: {str(e)}")
    
    # Trading Volume Analysis
    st.subheader("Trading Volume Analysis")
    
    volume_fig = px.bar(
        historical_data, 
        x=historical_data.index, 
        y='Volume',
        title=f"{ticker} Trading Volume",
        template='plotly_dark',
    )
    
    volume_fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Volume',
        height=400
    )
    
    st.plotly_chart(volume_fig, use_container_width=True)
    
    # Comparison option (teaser for future feature)
    st.markdown("---")
    st.info("Want to compare with other stocks or indices? New features coming soon!")
