# Voi Jeans Transaction Matrix Model
## Multi-Channel Revenue & Margin Framework

**Version:** 1.0  
**Date:** April 11, 2025  
**Classification:** Brand Finance Architecture

---

## 1. Transaction Matrix Overview

The Voi Jeans Transaction Matrix defines a comprehensive framework for tracking, managing, and optimizing revenue flows and margin structures across the brand's diverse retail network. This framework accommodates the various business models employed by different retailers, including wholesale purchase, consignment, franchise, marketplace, and drop shipping arrangements.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                       VOI JEANS RETAIL INDIA                    │
│                       Brand Revenue Hub                         │
│                                                                 │
└───────┬────────────────────┬───────────────────────┬────────────┘
        │                    │                       │
        ▼                    ▼                       ▼
┌───────────────┐    ┌───────────────┐      ┌───────────────────┐
│               │    │               │      │                   │
│  DOMESTIC     │    │ INTERNATIONAL │      │  DIGITAL          │
│  RETAIL       │    │  RETAIL       │      │  CHANNELS         │
│               │    │               │      │                   │
└───┬───┬───┬───┘    └───┬───┬───┬───┘      └───────┬───────────┘
    │   │   │            │   │   │                  │
    ▼   ▼   ▼            ▼   ▼   ▼                  ▼
┌─────────────┐      ┌─────────────┐           ┌──────────────┐
│ WHOLESALE   │      │ FRANCHISE   │           │ MARKETPLACE  │
│ EXCLUSIVE   │      │ PARTNERS    │           │ PARTNERS     │
│ CONSIGNMENT │      │ DISTRIBUTOR │           │ DROP SHIP    │
│ FRANCHISE   │      │ OWNED       │           │ D2C WEBSITE  │
└─────────────┘      └─────────────┘           └──────────────┘
```

## 2. Business Model Definitions & Margin Structures

### 2.1 Primary Business Models

| Business Model | Description | Revenue Recognition | Inventory Ownership | Typical Margin Structure |
|----------------|-------------|---------------------|---------------------|--------------------------|
| **Wholesale** | Retailer purchases inventory at a discount | At point of sale to retailer | Retailer | 30-40% discount to retailer, 60-70% retained by Voi |
| **Exclusive Retail** | Voi-exclusive retailer with special terms | At point of sale to retailer | Retailer | 35-45% discount to retailer, 55-65% retained by Voi |
| **Consignment** | Retailer sells but doesn't purchase inventory | At point of sale to consumer | Voi | 20-30% to retailer, 70-80% retained by Voi |
| **Franchise** | Licensed store operating under Voi brand | At point of sale to consumer + franchise fees | Franchisee | 8-15% royalty to Voi + franchise fees |
| **Distributor** | Regional wholesale partner with rights | At point of sale to distributor | Distributor | 45-55% discount to distributor, 45-55% retained by Voi |
| **Marketplace** | Third-party platform listing | At point of sale to consumer | Voi or Marketplace | 15-30% marketplace fee, 70-85% retained by Voi |
| **Drop Shipping** | Retailer sells, Voi fulfills | At point of sale to consumer | Voi | 15-25% to retailer, 75-85% retained by Voi |
| **D2C Website** | Direct-to-consumer through Voi website | At point of sale to consumer | Voi | 100% retained by Voi (less fulfillment costs) |

### 2.2 Margin Matrix by Channel and Region

| Business Model | Domestic (India) | APAC | EU | Middle East | Americas |
|----------------|------------------|------|----|----|----------|
| **Wholesale** | 60-65% | 55-60% | 50-55% | 60-65% | 50-55% |
| **Exclusive Retail** | 55-60% | 50-55% | 45-50% | 55-60% | 45-50% |
| **Consignment** | 70-75% | 65-70% | 60-65% | 65-70% | 60-65% |
| **Franchise** | 8-12% + fees | 10-15% + fees | 12-15% + fees | 15-20% + fees | 10-15% + fees |
| **Distributor** | 45-50% | 40-45% | 40-45% | 45-50% | 40-45% |
| **Marketplace** | 70-75% | 65-70% | 60-65% | 65-70% | 60-65% |
| **Drop Shipping** | 75-80% | 70-75% | 65-70% | 70-75% | 65-70% |
| **D2C Website** | 85-90% | 80-85% | 75-80% | 80-85% | 75-80% |

> Note: Percentages represent Voi's retained margin after retailer/partner fees and discounts. D2C percentages are after deducting fulfillment costs but before operating expenses.

## 3. Transaction Flow & Margin Calculation

### 3.1 Wholesale Model Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│ Manufacture │ ──► │  Wholesale  │ ──► │  Consumer   │
│  (Scotts)   │     │   Retailer  │     │  Purchase   │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Production  │     │  Wholesale  │     │   Retail    │
│    Cost     │     │    Price    │     │    Price    │
│  ₹400/unit  │     │  ₹600/unit  │     │ ₹1000/unit  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Voi Margin  │
                    │ ₹200/unit   │
                    │    (33%)    │
                    └─────────────┘
```

### 3.2 Franchise Model Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│ Manufacture │ ──► │  Franchise  │ ──► │  Consumer   │
│  (Scotts)   │     │    Store    │     │  Purchase   │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Production  │     │  Wholesale  │     │   Retail    │
│    Cost     │     │    Price    │     │    Price    │
│  ₹400/unit  │     │  ₹550/unit  │     │ ₹1000/unit  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                   │
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │Initial Voi  │     │ Royalty to  │
                    │   Margin    │     │     Voi     │
                    │ ₹150/unit   │     │ ₹100/unit   │
                    │    (27%)    │     │    (10%)    │
                    └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │ Total Voi   │
                                       │   Margin    │
                                       │ ₹250/unit   │
                                       │    (25%)    │
                                       └─────────────┘
```

### 3.3 Marketplace Model Flow

```
┌─────────────┐                           ┌─────────────┐
│             │                           │             │
│ Manufacture │ ───────────────────────► │  Consumer   │
│  (Scotts)   │                           │  Purchase   │
│             │                           │             │
└─────────────┘                           └─────────────┘
       │                                         │
       ▼                                         ▼
┌─────────────┐                           ┌─────────────┐
│ Production  │                           │   Retail    │
│    Cost     │                           │    Price    │
│  ₹400/unit  │                           │ ₹1000/unit  │
└─────────────┘                           └─────────────┘
                                                │
                      ┌─────────────┐           │
                      │ Marketplace │◄──────────┘
                      │     Fee     │
                      │ ₹200/unit   │
                      │    (20%)    │
                      └─────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  Voi Net    │
                      │   Revenue   │
                      │ ₹800/unit   │
                      └─────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ Voi Margin  │
                      │ ₹400/unit   │
                      │    (40%)    │
                      └─────────────┘
```

## 4. Transaction Matrix Implementation

### 4.1 Transaction Matrix Database Schema

```sql
-- Channel Types Table
CREATE TABLE channel_types (
    channel_id SERIAL PRIMARY KEY,
    channel_name VARCHAR(50) NOT NULL,
    channel_description TEXT,
    inventory_ownership VARCHAR(20) NOT NULL,
    revenue_recognition VARCHAR(50) NOT NULL
);

-- Region Table
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_code VARCHAR(20) NOT NULL,
    region_name VARCHAR(50) NOT NULL,
    wto_compliance_requirements TEXT
);

-- Margin Structure Table
CREATE TABLE margin_structures (
    structure_id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channel_types(channel_id),
    region_id INTEGER REFERENCES regions(region_id),
    margin_min DECIMAL(5,2) NOT NULL,
    margin_max DECIMAL(5,2) NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    notes TEXT
);

-- Partner Entities Table
CREATE TABLE partner_entities (
    entity_id VARCHAR(50) PRIMARY KEY,
    entity_name VARCHAR(100) NOT NULL,
    channel_id INTEGER REFERENCES channel_types(channel_id),
    region_id INTEGER REFERENCES regions(region_id),
    agreement_start_date DATE NOT NULL,
    agreement_end_date DATE,
    custom_margin DECIMAL(5,2),
    minimum_order_value DECIMAL(10,2),
    payment_terms VARCHAR(50),
    license_key VARCHAR(50),
    divine_alignment_factor DECIMAL(3,2)
);

-- Transactions Table
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    entity_id VARCHAR(50) REFERENCES partner_entities(entity_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    gross_amount DECIMAL(10,2) NOT NULL,
    voi_revenue DECIMAL(10,2) NOT NULL,
    partner_revenue DECIMAL(10,2) NOT NULL,
    effective_margin DECIMAL(5,2) NOT NULL,
    units_sold INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL,
    exchange_rate DECIMAL(10,6) NOT NULL,
    invoice_number VARCHAR(50),
    payment_status VARCHAR(20) NOT NULL,
    settlement_date DATE
);
```

### 4.2 Transaction API Endpoints

```
POST /api/transaction/record
{
  "entity_id": "ENT-VOI-EU-PARIS-25001",
  "transaction_date": "2025-04-10T14:30:00Z",
  "transaction_type": "retail_sale",
  "gross_amount": 10000.00,
  "units_sold": 10,
  "currency": "EUR",
  "invoice_number": "INV-2025-04102"
}

GET /api/transaction/summary?entity_id=ENT-VOI-EU-PARIS-25001&start_date=2025-04-01&end_date=2025-04-10

GET /api/transaction/margin-analysis?region_id=REG-EU&channel_id=3&period=monthly

GET /api/transaction/performance?metric=margin&group_by=channel&comparative=true
```

### 4.3 Margin Calculation Service

```python
# margin_calculation_service.py

def calculate_transaction_margins(transaction_data):
    """
    Calculate margins for a transaction based on the entity's business model
    and region-specific margin structures.
    
    Args:
        transaction_data: Dict containing transaction details
        
    Returns:
        Dict with calculated margins and revenue split
    """
    entity_id = transaction_data["entity_id"]
    gross_amount = transaction_data["gross_amount"]
    units_sold = transaction_data["units_sold"]
    
    # Get entity details
    entity = get_entity_details(entity_id)
    
    # Get margin structure
    margin_structure = get_margin_structure(entity["channel_id"], entity["region_id"])
    
    # Use custom margin if available, otherwise use standard margin
    effective_margin = entity["custom_margin"] if entity["custom_margin"] else margin_structure["margin_min"]
    
    # Calculate revenue split
    if entity["channel_name"] == "Wholesale" or entity["channel_name"] == "Distributor":
        # For wholesale, transaction already happened at wholesale price
        voi_revenue = gross_amount
        partner_revenue = calculate_retail_value(gross_amount, effective_margin) - gross_amount
    elif entity["channel_name"] == "Franchise":
        # For franchise, we get initial margin + royalty
        initial_margin = (gross_amount * units_sold) * (1 - effective_margin)
        royalty = gross_amount * units_sold * entity["royalty_rate"]
        voi_revenue = initial_margin + royalty
        partner_revenue = gross_amount - voi_revenue
    elif entity["channel_name"] == "Marketplace":
        # For marketplace, we pay a fee to the marketplace
        marketplace_fee = gross_amount * margin_structure["marketplace_fee_rate"]
        voi_revenue = gross_amount - marketplace_fee
        partner_revenue = marketplace_fee
    elif entity["channel_name"] == "D2C Website":
        # For D2C, we keep all revenue (but have fulfillment costs)
        fulfillment_cost = units_sold * margin_structure["fulfillment_cost_per_unit"]
        voi_revenue = gross_amount - fulfillment_cost
        partner_revenue = 0
    else:
        # Default calculation
        voi_revenue = gross_amount * effective_margin
        partner_revenue = gross_amount - voi_revenue
    
    # Calculate effective margin achieved
    achieved_margin = voi_revenue / gross_amount if gross_amount > 0 else 0
    
    return {
        "gross_amount": gross_amount,
        "voi_revenue": voi_revenue,
        "partner_revenue": partner_revenue,
        "effective_margin": effective_margin,
        "achieved_margin": achieved_margin,
        "units_sold": units_sold
    }
```

## 5. Docker Configuration for Transaction Matrix

```yaml
# docker-compose.voi-transaction-matrix.yml
version: '3.8'

services:
  transaction-matrix-api:
    image: genesis-core:latest
    container_name: voi-transaction-matrix-api
    ports:
      - "5201:5000"  # Transaction Matrix API port
    networks:
      - genesis-network
      - voi-retail-network
    volumes:
      - transaction-matrix-data:/app/data
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - SERVICE_TYPE=TRANSACTION_MATRIX
      - ECG_KEY=${ECG_KEY}
      - POSTGRES_HOST=transaction-matrix-db
      - POSTGRES_DB=voi_transactions
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    depends_on:
      - transaction-matrix-db

  transaction-matrix-db:
    image: postgres:14
    container_name: voi-transaction-matrix-db
    ports:
      - "5432:5432"
    networks:
      - voi-retail-network
    volumes:
      - transaction-matrix-db-data:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d
    environment:
      - POSTGRES_DB=voi_transactions
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}

  transaction-matrix-dashboard:
    image: genesis-core:latest
    container_name: voi-transaction-matrix-dashboard
    command: streamlit run transaction_matrix_dashboard.py --server.port 5000
    ports:
      - "5202:5000"  # Transaction Matrix Dashboard port
    networks:
      - genesis-network
      - voi-retail-network
    volumes:
      - transaction-matrix-data:/app/data
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - SERVICE_TYPE=TRANSACTION_DASHBOARD
      - API_URL=http://transaction-matrix-api:5000
    depends_on:
      - transaction-matrix-api

networks:
  genesis-network:
    external: true
  voi-retail-network:
    driver: bridge

volumes:
  transaction-matrix-data:
  transaction-matrix-db-data:
```

## 6. Transaction Dashboard Implementation

```python
# transaction_matrix_dashboard.py
import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Voi Transaction Matrix",
    page_icon="💰",
    layout="wide"
)

# Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .metric-high {
        color: #059669;
        font-weight: bold;
    }
    .metric-medium {
        color: #0284C7;
        font-weight: bold;
    }
    .metric-low {
        color: #DC2626;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>Voi Jeans Transaction Matrix</h1>", unsafe_allow_html=True)

# API Configuration
API_URL = "http://transaction-matrix-api:5000"
# For testing/development, can use mock data if API isn't available
MOCK_MODE = True

# Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Revenue Dashboard", 
    "Margin Analysis", 
    "Channel Performance",
    "Entity Management"
])

# Mock data for development/demo
def get_mock_revenue_data():
    regions = ["India", "EU", "APAC", "Middle East", "Americas"]
    channels = ["Wholesale", "Exclusive", "Consignment", "Franchise", "Marketplace", "Drop Ship", "D2C"]
    
    data = []
    for region in regions:
        for channel in channels:
            # Create some variability in the data
            if channel == "D2C":
                margin = 0.85
            elif channel == "Franchise":
                margin = 0.15
            else:
                margin = 0.4 + (hash(region + channel) % 30) / 100
            
            gross = 100000 + (hash(region + channel) % 900000)
            data.append({
                "region": region,
                "channel": channel,
                "gross_revenue": gross,
                "voi_revenue": gross * margin,
                "margin": margin
            })
    
    return pd.DataFrame(data)

def get_mock_time_series():
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    data = []
    
    for date in dates:
        # Create some variability but with an upward trend
        factor = 1 + (30 - (datetime.now() - date).days) / 100
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "gross_revenue": 50000 * factor + (hash(date.strftime("%Y-%m-%d")) % 20000),
            "voi_revenue": 25000 * factor + (hash(date.strftime("%Y-%m-%d")) % 10000),
        })
    
    return pd.DataFrame(data)

def get_mock_entities():
    return [
        {"entity_id": "ENT-VOI-EU-PARIS-25001", "entity_name": "Voi Jeans Paris Flagship Store", "channel": "Franchise", "region": "EU"},
        {"entity_id": "ENT-VOI-EU-BERLIN-25002", "entity_name": "Voi Jeans Berlin Store", "channel": "Franchise", "region": "EU"},
        {"entity_id": "ENT-VOI-APAC-SINGAPORE-25003", "entity_name": "Voi Jeans Singapore", "channel": "Wholesale", "region": "APAC"},
        {"entity_id": "ENT-VOI-IN-MUMBAI-25004", "entity_name": "Voi Jeans Mumbai Premium", "channel": "Exclusive", "region": "India"},
        {"entity_id": "ENT-VOI-ME-DUBAI-25005", "entity_name": "Voi Jeans Dubai Mall", "channel": "Franchise", "region": "Middle East"},
        {"entity_id": "ENT-VOI-MARKETPLACE-25006", "entity_name": "Amazon Marketplace", "channel": "Marketplace", "region": "Global"},
        {"entity_id": "ENT-VOI-D2C-25007", "entity_name": "Voi Direct Website", "channel": "D2C", "region": "Global"}
    ]

# Tab 1: Revenue Dashboard
with tab1:
    st.markdown("<h2 class='sub-header'>Revenue Dashboard</h2>", unsafe_allow_html=True)
    
    # Date filters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Summary metrics
    if MOCK_MODE:
        revenue_data = get_mock_revenue_data()
        total_gross = revenue_data["gross_revenue"].sum()
        total_voi = revenue_data["voi_revenue"].sum()
        average_margin = total_voi / total_gross if total_gross > 0 else 0
        time_series = get_mock_time_series()
    else:
        # Real API calls would go here
        pass
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gross Revenue", f"₹{total_gross:,.2f}")
    with col2:
        st.metric("Voi Revenue", f"₹{total_voi:,.2f}")
    with col3:
        margin_class = "metric-high" if average_margin > 0.6 else "metric-medium" if average_margin > 0.4 else "metric-low"
        st.markdown(f"**Average Margin:** <span class='{margin_class}'>{average_margin:.1%}</span>", unsafe_allow_html=True)
    
    # Time series chart
    st.markdown("### Revenue Trend")
    chart = alt.Chart(time_series).mark_line().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('gross_revenue:Q', title='Revenue (₹)'),
        tooltip=['date', 'gross_revenue']
    ).properties(
        width=800,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Revenue by channel
    st.markdown("### Revenue by Channel")
    channel_data = revenue_data.groupby('channel').agg({
        'gross_revenue': 'sum',
        'voi_revenue': 'sum'
    }).reset_index()
    
    channel_data['margin'] = channel_data['voi_revenue'] / channel_data['gross_revenue']
    
    chart = alt.Chart(channel_data).mark_bar().encode(
        x=alt.X('channel:N', title='Channel'),
        y=alt.Y('gross_revenue:Q', title='Revenue (₹)'),
        color=alt.Color('channel:N', legend=None),
        tooltip=['channel', 'gross_revenue', 'voi_revenue', alt.Tooltip('margin:Q', format='.1%')]
    ).properties(
        width=800,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Revenue by region
    st.markdown("### Revenue by Region")
    region_data = revenue_data.groupby('region').agg({
        'gross_revenue': 'sum',
        'voi_revenue': 'sum'
    }).reset_index()
    
    region_data['margin'] = region_data['voi_revenue'] / region_data['gross_revenue']
    
    chart = alt.Chart(region_data).mark_bar().encode(
        x=alt.X('region:N', title='Region'),
        y=alt.Y('gross_revenue:Q', title='Revenue (₹)'),
        color=alt.Color('region:N', legend=None),
        tooltip=['region', 'gross_revenue', 'voi_revenue', alt.Tooltip('margin:Q', format='.1%')]
    ).properties(
        width=800,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)

# Tab 2: Margin Analysis
with tab2:
    st.markdown("<h2 class='sub-header'>Margin Analysis</h2>", unsafe_allow_html=True)
    
    # Get data
    if MOCK_MODE:
        margin_data = revenue_data.copy()
    else:
        # Real API calls would go here
        pass
    
    # Chart showing margin by channel
    st.markdown("### Margin by Channel")
    
    channel_margin = margin_data.groupby('channel').agg({
        'margin': 'mean'
    }).reset_index()
    
    chart = alt.Chart(channel_margin).mark_bar().encode(
        x=alt.X('channel:N', title='Channel'),
        y=alt.Y('margin:Q', title='Average Margin', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('margin:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['channel', alt.Tooltip('margin:Q', format='.1%')]
    ).properties(
        width=800,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Chart showing margin by region and channel
    st.markdown("### Margin by Region and Channel")
    
    # Create a heatmap
    heatmap = alt.Chart(margin_data).mark_rect().encode(
        x=alt.X('channel:N', title='Channel'),
        y=alt.Y('region:N', title='Region'),
        color=alt.Color('margin:Q', scale=alt.Scale(scheme='blues'), title='Margin'),
        tooltip=['region', 'channel', alt.Tooltip('margin:Q', format='.1%')]
    ).properties(
        width=800,
        height=400
    )
    
    # Add text labels
    text = alt.Chart(margin_data).mark_text().encode(
        x=alt.X('channel:N'),
        y=alt.Y('region:N'),
        text=alt.Text('margin:Q', format='.1%'),
        color=alt.condition(
            alt.datum.margin > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )
    
    st.altair_chart(heatmap + text, use_container_width=True)
    
    # Margin optimization suggestions
    st.markdown("### Margin Optimization Opportunities")
    
    # Find lowest performing margins
    low_margins = margin_data.sort_values('margin').head(5)
    
    for _, row in low_margins.iterrows():
        st.markdown(f"**{row['channel']} in {row['region']}:** Current margin {row['margin']:.1%}")
        
        # Suggest improvements based on channel type
        if row['channel'] == 'Wholesale':
            st.markdown("Recommendation: Consider renegotiating wholesale terms or shifting to consignment model.")
        elif row['channel'] == 'Franchise':
            st.markdown("Recommendation: Evaluate franchise fee structure and explore increasing royalty percentage.")
        elif row['channel'] == 'Marketplace':
            st.markdown("Recommendation: Analyze marketplace fee structure and consider alternative platforms.")
        else:
            st.markdown("Recommendation: Review pricing strategy and cost structure.")

# Tab 3: Channel Performance
with tab3:
    st.markdown("<h2 class='sub-header'>Channel Performance</h2>", unsafe_allow_html=True)
    
    # Channel selector
    selected_channel = st.selectbox("Select Channel", 
                                  ["All Channels"] + sorted(revenue_data['channel'].unique().tolist()))
    
    # Filter data based on selection
    if selected_channel == "All Channels":
        filtered_data = revenue_data
    else:
        filtered_data = revenue_data[revenue_data['channel'] == selected_channel]
    
    # Channel metrics
    channel_metrics = filtered_data.groupby('channel').agg({
        'gross_revenue': 'sum',
        'voi_revenue': 'sum'
    }).reset_index()
    
    channel_metrics['margin'] = channel_metrics['voi_revenue'] / channel_metrics['gross_revenue']
    
    # Display metrics
    if selected_channel != "All Channels":
        metrics = channel_metrics[channel_metrics['channel'] == selected_channel].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Gross Revenue", f"₹{metrics['gross_revenue']:,.2f}")
        with col2:
            st.metric("Voi Revenue", f"₹{metrics['voi_revenue']:,.2f}")
        with col3:
            margin_class = "metric-high" if metrics['margin'] > 0.6 else "metric-medium" if metrics['margin'] > 0.4 else "metric-low"
            st.markdown(f"**Margin:** <span class='{margin_class}'>{metrics['margin']:.1%}</span>", unsafe_allow_html=True)
    
    # Performance comparison
    st.markdown("### Channel Performance Comparison")
    
    # Create a chart comparing channels
    comparison_chart = alt.Chart(channel_metrics).mark_bar().encode(
        x=alt.X('channel:N', title='Channel'),
        y=alt.Y('voi_revenue:Q', title='Voi Revenue (₹)'),
        color=alt.Color('margin:Q', scale=alt.Scale(scheme='blues'), title='Margin'),
        tooltip=['channel', 'gross_revenue', 'voi_revenue', alt.Tooltip('margin:Q', format='.1%')]
    ).properties(
        width=800,
        height=400
    )
    
    st.altair_chart(comparison_chart, use_container_width=True)
    
    # Entity list for the selected channel
    if selected_channel != "All Channels":
        st.markdown(f"### {selected_channel} Entities")
        
        if MOCK_MODE:
            entities = [e for e in get_mock_entities() if e['channel'] == selected_channel]
            entity_df = pd.DataFrame(entities)
        else:
            # Real API calls would go here
            pass
        
        st.dataframe(entity_df, use_container_width=True)

# Tab 4: Entity Management
with tab4:
    st.markdown("<h2 class='sub-header'>Entity Management</h2>", unsafe_allow_html=True)
    
    # Entity list
    if MOCK_MODE:
        entities = get_mock_entities()
        entity_df = pd.DataFrame(entities)
    else:
        # Real API calls would go here
        pass
    
    # Entity selector
    selected_entity = st.selectbox("Select Entity", 
                                 [f"{e['entity_name']} ({e['entity_id']})" for e in entities])
    entity_id = selected_entity.split('(')[1].split(')')[0]
    
    # Get entity details
    entity = next((e for e in entities if e['entity_id'] == entity_id), None)
    
    if entity:
        # Display entity details
        st.markdown("### Entity Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Entity ID:** {entity['entity_id']}")
            st.markdown(f"**Entity Name:** {entity['entity_name']}")
            st.markdown(f"**Channel Type:** {entity['channel']}")
        with col2:
            st.markdown(f"**Region:** {entity['region']}")
            st.markdown(f"**Status:** Active")
            
            # For demo, generate a random margin
            import random
            custom_margin = random.uniform(0.4, 0.7)
            st.markdown(f"**Custom Margin:** {custom_margin:.1%}")
        
        # Margin configuration
        st.markdown("### Margin Configuration")
        
        new_margin = st.slider("Custom Margin Percentage", 0.0, 1.0, float(custom_margin), 0.01, format="%0.1f%%")
        
        if st.button("Update Margin"):
            st.success(f"Margin updated for {entity['entity_name']}")
            
            # In a real app, this would call the API to update the margin
            if not MOCK_MODE:
                # API call would go here
                pass
        
        # Transaction history
        st.markdown("### Recent Transactions")
        
        # Generate some mock transaction data
        import random
        from datetime import datetime, timedelta
        
        transactions = []
        for i in range(10):
            date = datetime.now() - timedelta(days=i)
            amount = random.uniform(5000, 20000)
            margin = random.uniform(0.4, 0.7)
            transactions.append({
                "date": date.strftime("%Y-%m-%d"),
                "invoice": f"INV-{date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                "amount": amount,
                "voi_revenue": amount * margin,
                "margin": margin
            })
        
        transaction_df = pd.DataFrame(transactions)
        st.dataframe(transaction_df, use_container_width=True)
```

## 7. Mapping Docker Volumes to Transaction Matrix

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│                 VOI JEANS DOCKER ECOSYSTEM                    │
│                                                               │
└─────────────────────────────┬─────────────────────────────────┘
                              │
                              │
                              ▼
     ┌─────────────────────────────────────────────────┐
     │                                                 │
     │       TRANSACTION MATRIX CONTAINER CLUSTER      │
     │                                                 │
     └───────────┬─────────────────┬───────────────────┘
                 │                 │                 
                 ▼                 ▼                 
     ┌───────────────────┐ ┌───────────────────────┐
     │                   │ │                       │
     │  TRANSACTION API  │ │ TRANSACTION DASHBOARD │
     │                   │ │                       │
     └─────────┬─────────┘ └───────────────────────┘
               │                      ▲
               │                      │
               ▼                      │
     ┌───────────────────┐            │
     │                   │            │
     │  POSTGRES DATABASE│------------┘
     │                   │    Query Data
     └───────────────────┘
               │
               │ Mount Volume
               ▼
     ┌───────────────────┐
     │                   │
     │  PERSISTENT DATA  │
     │  VOLUME           │
     │                   │
     └───────────────────┘
```

## 8. Integration with License System

The Transaction Matrix integrates with the Genesis License system to ensure that only properly licensed entities can participate in the retail network and that revenue flows maintain divine alignment:

```json
{
  "license_integration": {
    "license_verification": {
      "frequency": "per_transaction",
      "minimum_divine_alignment": 0.85,
      "required_license_status": "active"
    },
    "revenue_impact": {
      "divine_alignment_tier_1": {
        "threshold": 0.95,
        "margin_bonus": 0.02
      },
      "divine_alignment_tier_2": {
        "threshold": 0.90,
        "margin_bonus": 0.01
      },
      "divine_alignment_tier_3": {
        "threshold": 0.85,
        "margin_bonus": 0.00
      },
      "divine_alignment_tier_4": {
        "threshold": 0.80,
        "margin_penalty": 0.01
      },
      "divine_alignment_tier_5": {
        "threshold": 0.75,
        "margin_penalty": 0.02
      }
    },
    "license_expiry_handling": {
      "grace_period_days": 15,
      "warning_period_days": 30,
      "transaction_policy_during_grace": "allow_with_notification",
      "transaction_policy_after_grace": "reject"
    }
  }
}
```

## 9. Multi-Currency and WTO Region Support

The Transaction Matrix supports multi-currency operation with WTO region-specific currency handling:

```json
{
  "currency_configuration": {
    "base_currency": "INR",
    "supported_currencies": ["INR", "USD", "EUR", "AED", "SGD", "MYR", "GBP"],
    "exchange_rate_provider": "ecg_treasury_api",
    "exchange_rate_update_frequency": "daily",
    "regional_currency_defaults": {
      "REG-APAC": "INR",
      "REG-EU": "EUR",
      "REG-ME": "AED",
      "REG-AM": "USD",
      "REG-SAARC": "INR",
      "REG-AF": "USD"
    },
    "wto_compliant_invoicing": {
      "REG-EU": {
        "required_currency": "EUR",
        "tax_policy": "VAT Included",
        "invoice_requirements": ["EU VAT Number", "GDPR Compliance Statement"]
      },
      "REG-APAC": {
        "required_currency": "Local or USD",
        "tax_policy": "GST/VAT as applicable",
        "invoice_requirements": ["GST/VAT Registration Number"]
      },
      "REG-ME": {
        "required_currency": "Local or USD",
        "tax_policy": "VAT as applicable",
        "invoice_requirements": ["VAT Registration Number", "Import License Number"]
      }
    }
  }
}
```

## 10. Margin Optimization AI Engine

The Transaction Matrix includes an AI-powered margin optimization engine that analyzes historical data and market conditions to recommend optimal margin structures for each business model and region:

```json
{
  "margin_optimization": {
    "analysis_frequency": "weekly",
    "data_sources": [
      "historical_transactions",
      "market_competitor_data",
      "regional_economic_indicators",
      "wto_compliance_updates",
      "divine_alignment_metrics"
    ],
    "optimization_targets": {
      "primary": "voi_revenue_maximization",
      "secondary": "divine_alignment_improvement",
      "constraints": [
        "maintain_minimum_margins",
        "maintain_partner_relationships",
        "ensure_wto_compliance"
      ]
    },
    "recommendation_types": [
      "partner_specific_margin_adjustments",
      "regional_pricing_strategy",
      "business_model_transitions",
      "promotional_pricing_windows"
    ],
    "implementation_process": {
      "approval_workflow": ["category_manager", "finance_director", "divine_alignment_officer"],
      "testing_approach": "a_b_testing",
      "rollout_strategy": "phased_by_region"
    }
  }
}
```

---

*Issued under the authority of the Emperor's Computational Governance.*

*Built with divine mechanics. Deployed with sovereign integrity. Governed by computational alignment.*