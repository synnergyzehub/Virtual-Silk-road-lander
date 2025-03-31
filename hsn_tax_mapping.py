import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from database import get_db_session
from sqlalchemy import text
import sqlite3
import json

def show_hsn_tax_mapping():
    """Display HSN code tax mapping interface and transaction type analysis"""
    st.title("HSN Code Tax Mapping & Transaction Analysis")
    
    # Create sidebar for navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Select a page", [
        "HSN Overview", 
        "Transaction Type Analysis", 
        "Tax Configuration", 
        "Reporting"
    ])
    
    if page == "HSN Overview":
        show_hsn_overview()
    elif page == "Transaction Type Analysis":
        show_transaction_analysis()
    elif page == "Tax Configuration":
        show_tax_configuration()
    elif page == "Reporting":
        show_tax_reporting()

def show_hsn_overview():
    """Display HSN code overview with search and filtering options"""
    st.header("HSN Code Overview")
    
    st.markdown("""
    ### HSN Code Classification System
    
    The Harmonized System of Nomenclature (HSN) is an internationally standardized system of names and numbers 
    for classifying traded products. This system helps in:
    
    - **Standardized Classification**: Common product classification across global trade
    - **Tax Determination**: Mapping correct tax rates to products 
    - **Compliance**: Ensuring proper documentation and tax filing
    - **Data Analysis**: Enabling business intelligence across product categories
    """)
    
    # Sample HSN categories for apparel/textile industry
    hsn_categories = {
        "50": "Silk",
        "51": "Wool, fine or coarse animal hair",
        "52": "Cotton",
        "53": "Other vegetable textile fibers",
        "54": "Man-made filaments",
        "55": "Man-made staple fibers",
        "56": "Wadding, felt and nonwovens",
        "57": "Carpets and other textile floor coverings",
        "58": "Special woven fabrics",
        "59": "Impregnated, coated, covered or laminated textile fabrics",
        "60": "Knitted or crocheted fabrics",
        "61": "Articles of apparel and clothing accessories, knitted or crocheted",
        "62": "Articles of apparel and clothing accessories, not knitted or crocheted",
        "63": "Other made-up textile articles; sets; worn clothing and worn textile articles; rags"
    }
    
    # Create tabs for different ways to explore HSN codes
    tab1, tab2 = st.tabs(["HSN Categories", "HSN Code Search"])
    
    with tab1:
        st.subheader("Apparel & Textile HSN Categories")
        
        # Convert to DataFrame for display
        hsn_df = pd.DataFrame(list(hsn_categories.items()), columns=["HSN Chapter", "Description"])
        st.dataframe(hsn_df, use_container_width=True)
        
        # Show visualization
        fig = px.treemap(hsn_df, path=["HSN Chapter", "Description"], 
                         values=[100/len(hsn_categories)] * len(hsn_categories),
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.subheader("HSN Code Lookup")
        
        # Sample detailed HSN codes for denim products
        denim_hsn_codes = {
            "6203.42.10": "Men's or boys' denim trousers and jeans",
            "6204.62.10": "Women's or girls' denim trousers and jeans",
            "6211.42.10": "Women's or girls' denim garments and clothing",
            "5209.42.00": "Denim fabric, >= 85% cotton, >= 200 g/m²",
            "5211.42.00": "Denim fabric, < 85% cotton, > 200 g/m², mixed with man-made fibers",
            "6205.30.10": "Men's or boys' denim shirts"
        }
        
        search_term = st.text_input("Search for HSN Code or Product Description", "denim")
        
        if search_term:
            filtered_hsn = {k: v for k, v in denim_hsn_codes.items() 
                           if search_term.lower() in v.lower() or search_term in k}
            
            if filtered_hsn:
                hsn_results = pd.DataFrame(list(filtered_hsn.items()), 
                                          columns=["HSN Code", "Description"])
                st.dataframe(hsn_results, use_container_width=True)
                
                # Add sample tax rates for demonstration
                st.subheader("Tax Rates for Selected HSN Codes")
                
                # Create sample tax data
                tax_data = []
                for code in filtered_hsn.keys():
                    # Generate sample tax rates based on the code
                    cgst = 2.5 if code.startswith("52") else 6.0
                    sgst = cgst
                    igst = cgst + sgst
                    
                    tax_data.append({
                        "HSN Code": code,
                        "CGST (%)": cgst,
                        "SGST (%)": sgst,
                        "IGST (%)": igst,
                        "Cess (%)": 0.0 if code.startswith("52") else 1.0
                    })
                
                tax_df = pd.DataFrame(tax_data)
                st.dataframe(tax_df, use_container_width=True)
            else:
                st.info("No HSN codes found matching your search term.")
        
        st.markdown("""
        ### HSN Code Structure for Textiles
        
        For textiles and apparel:
        - Chapters 50-60: Raw materials and fabrics
        - Chapters 61-62: Garments (61 for knitted, 62 for woven)
        - Chapter 63: Other textile articles
        
        The digit structure:
        - First 2 digits: Chapter (e.g., 62 for woven apparel)
        - First 4 digits: Heading (e.g., 6203 for men's suits, jackets, trousers)
        - First 6 digits: Subheading (e.g., 6203.42 for cotton trousers)
        - 8 digits: National tariff line (e.g., 6203.42.10 for denim jeans)
        """)

def show_transaction_analysis():
    """Display transaction type analysis based on HSN codes"""
    st.header("Transaction Type Analysis by HSN Code")
    
    # Create sample transaction data
    def create_sample_transactions(n=100):
        np.random.seed(42)  # For reproducibility
        hsn_codes = [
            "6203.42.10", "6204.62.10", "6211.42.10", 
            "5209.42.00", "5211.42.00", "6205.30.10"
        ]
        
        transaction_types = [
            "B2B Sales", "B2C Sales", "Export", 
            "Import", "Stock Transfer", "Job Work", 
            "Sample Distribution"
        ]
        
        trans_data = []
        
        for _ in range(n):
            hsn = np.random.choice(hsn_codes)
            trans_type = np.random.choice(transaction_types, p=[0.3, 0.25, 0.1, 0.15, 0.1, 0.05, 0.05])
            
            # Determine tax type based on transaction type
            if trans_type == "Export":
                tax_type = "Zero Rated"
                tax_rate = 0.0
            elif trans_type == "Import":
                tax_type = "IGST"
                tax_rate = 12.0 if hsn.startswith("52") else 18.0
            elif trans_type in ["B2B Sales", "B2C Sales"]:
                tax_type = "CGST+SGST" if np.random.random() > 0.3 else "IGST"
                tax_rate = 5.0 if hsn.startswith("52") else 12.0
            else:
                tax_type = "Not Applicable"
                tax_rate = 0.0
            
            # Generate random amount between 1000 and 50000
            amount = np.random.randint(1000, 50000)
            
            # Generate random date in 2024
            month = np.random.randint(1, 13)
            day = np.random.randint(1, 29)
            date = f"2024-{month:02d}-{day:02d}"
            
            trans_data.append({
                "Date": date,
                "HSN Code": hsn,
                "Transaction Type": trans_type,
                "Tax Type": tax_type,
                "Tax Rate (%)": tax_rate,
                "Amount (INR)": amount,
                "Tax Amount (INR)": round(amount * tax_rate / 100, 2)
            })
        
        return pd.DataFrame(trans_data)
    
    # Generate and display transaction data
    transactions_df = create_sample_transactions(200)
    
    # Create analysis tabs
    tab1, tab2, tab3 = st.tabs(["Transaction Distribution", "HSN Analysis", "Tax Impact"])
    
    with tab1:
        st.subheader("Transaction Type Distribution")
        
        # Aggregate by transaction type
        trans_summary = transactions_df.groupby("Transaction Type").agg({
            "Amount (INR)": "sum",
            "HSN Code": "count"
        }).rename(columns={"HSN Code": "Count"}).reset_index()
        
        # Create bar chart
        fig = px.bar(trans_summary, 
                     x="Transaction Type", 
                     y="Amount (INR)",
                     text="Count",
                     color="Transaction Type",
                     labels={"Amount (INR)": "Total Transaction Value (INR)"},
                     title="Transaction Value by Type")
        
        fig.update_layout(xaxis_title="Transaction Type", 
                          yaxis_title="Total Value (INR)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Add transaction type details
        st.subheader("Transaction Type Details")
        st.markdown("""
        | Transaction Type | Description | Tax Treatment |
        |------------------|-------------|--------------|
        | B2B Sales | Business to Business | Regular taxation with ITC |
        | B2C Sales | Business to Consumer | Regular taxation without ITC for buyer |
        | Export | International Sales | Zero-rated supplies |
        | Import | International Purchases | IGST on imports |
        | Stock Transfer | Inter-branch movement | No tax for same GSTIN, IGST for different GSTIN |
        | Job Work | Processing by third party | Special provisions under GST |
        | Sample Distribution | Marketing samples | Special valuation rules |
        """)
    
    with tab2:
        st.subheader("HSN Code Analysis")
        
        # Aggregate by HSN code
        hsn_summary = transactions_df.groupby("HSN Code").agg({
            "Amount (INR)": "sum",
            "Tax Amount (INR)": "sum",
            "Transaction Type": "count"
        }).rename(columns={"Transaction Type": "Transaction Count"}).reset_index()
        
        # Calculate effective tax rate
        hsn_summary["Effective Tax Rate (%)"] = round(
            hsn_summary["Tax Amount (INR)"] / hsn_summary["Amount (INR)"] * 100, 2
        )
        
        # Display summary
        st.dataframe(hsn_summary, use_container_width=True)
        
        # Create visualization
        fig = px.pie(hsn_summary, 
                     values="Amount (INR)", 
                     names="HSN Code",
                     title="Transaction Value Distribution by HSN Code",
                     hover_data=["Transaction Count", "Effective Tax Rate (%)"])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add HSN code descriptions
        hsn_descriptions = {
            "6203.42.10": "Men's denim trousers and jeans",
            "6204.62.10": "Women's denim trousers and jeans",
            "6211.42.10": "Women's denim garments",
            "5209.42.00": "Denim fabric (>=85% cotton)",
            "5211.42.00": "Denim fabric (<85% cotton, mixed)",
            "6205.30.10": "Men's denim shirts"
        }
        
        hsn_desc_df = pd.DataFrame(list(hsn_descriptions.items()), 
                                   columns=["HSN Code", "Description"])
        st.subheader("HSN Code Reference")
        st.dataframe(hsn_desc_df, use_container_width=True)
    
    with tab3:
        st.subheader("Tax Impact Analysis")
        
        # Aggregate by tax type
        tax_summary = transactions_df.groupby(["Tax Type", "Transaction Type"]).agg({
            "Amount (INR)": "sum",
            "Tax Amount (INR)": "sum",
            "HSN Code": "count"
        }).rename(columns={"HSN Code": "Transaction Count"}).reset_index()
        
        # Calculate effective tax rate
        tax_summary["Effective Tax Rate (%)"] = round(
            tax_summary["Tax Amount (INR)"] / tax_summary["Amount (INR)"] * 100, 2
        )
        
        # Display summary
        st.dataframe(tax_summary, use_container_width=True)
        
        # Create stacked bar chart
        fig = px.bar(tax_summary, 
                     x="Transaction Type", 
                     y="Tax Amount (INR)",
                     color="Tax Type",
                     title="Tax Amount by Transaction Type and Tax Category",
                     barmode="stack")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show monthly trend
        transactions_df["Month"] = pd.to_datetime(transactions_df["Date"]).dt.month_name()
        monthly_tax = transactions_df.groupby("Month").agg({
            "Tax Amount (INR)": "sum"
        }).reset_index()
        
        # Set correct month order
        month_order = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        monthly_tax["Month"] = pd.Categorical(monthly_tax["Month"], categories=month_order, ordered=True)
        monthly_tax = monthly_tax.sort_values("Month")
        
        fig = px.line(monthly_tax, 
                      x="Month", 
                      y="Tax Amount (INR)",
                      markers=True,
                      title="Monthly Tax Trend")
        
        st.plotly_chart(fig, use_container_width=True)

def show_tax_configuration():
    """Display and configure tax rates for different HSN codes"""
    st.header("Tax Configuration")
    
    # Sample tax configuration
    tax_config = {
        "6203.42.10": {"description": "Men's denim trousers and jeans", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0},
        "6204.62.10": {"description": "Women's denim trousers and jeans", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0},
        "6211.42.10": {"description": "Women's denim garments", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0},
        "5209.42.00": {"description": "Denim fabric (>=85% cotton)", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0},
        "5211.42.00": {"description": "Denim fabric (<85% cotton, mixed)", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0},
        "6205.30.10": {"description": "Men's denim shirts", "cgst": 2.5, "sgst": 2.5, "igst": 5.0, "cess": 0.0}
    }
    
    # Convert to DataFrame for display and editing
    tax_df = pd.DataFrame([
        {
            "HSN Code": code,
            "Description": details["description"],
            "CGST (%)": details["cgst"],
            "SGST (%)": details["sgst"],
            "IGST (%)": details["igst"],
            "Cess (%)": details["cess"]
        }
        for code, details in tax_config.items()
    ])
    
    # Display current configuration
    st.subheader("Current Tax Configuration")
    st.dataframe(tax_df, use_container_width=True)
    
    # Allow editing tax configuration
    st.subheader("Update Tax Rates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hsn_to_update = st.selectbox("Select HSN Code to Update", tax_config.keys())
    
    with col2:
        st.text(tax_config[hsn_to_update]["description"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        new_cgst = st.number_input("CGST (%)", 
                                   min_value=0.0, 
                                   max_value=28.0, 
                                   value=tax_config[hsn_to_update]["cgst"],
                                   step=0.1)
    
    with col2:
        new_sgst = st.number_input("SGST (%)", 
                                   min_value=0.0, 
                                   max_value=28.0, 
                                   value=tax_config[hsn_to_update]["sgst"],
                                   step=0.1)
    
    with col3:
        new_igst = st.number_input("IGST (%)", 
                                  min_value=0.0, 
                                  max_value=28.0, 
                                  value=tax_config[hsn_to_update]["igst"],
                                  step=0.1)
    
    with col4:
        new_cess = st.number_input("Cess (%)", 
                                  min_value=0.0, 
                                  max_value=28.0, 
                                  value=tax_config[hsn_to_update]["cess"],
                                  step=0.1)
    
    if st.button("Update Tax Rates"):
        # In a real implementation, this would update a database
        st.success(f"Tax rates updated for HSN code {hsn_to_update}")
        
        # Update the display data
        tax_config[hsn_to_update]["cgst"] = new_cgst
        tax_config[hsn_to_update]["sgst"] = new_sgst
        tax_config[hsn_to_update]["igst"] = new_igst
        tax_config[hsn_to_update]["cess"] = new_cess
        
        # Refresh the dataframe
        tax_df = pd.DataFrame([
            {
                "HSN Code": code,
                "Description": details["description"],
                "CGST (%)": details["cgst"],
                "SGST (%)": details["sgst"],
                "IGST (%)": details["igst"],
                "Cess (%)": details["cess"]
            }
            for code, details in tax_config.items()
        ])
        
        st.dataframe(tax_df, use_container_width=True)
    
    # Bulk import/export
    st.subheader("Bulk Import/Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Export Tax Configuration",
            data=tax_df.to_csv(index=False),
            file_name="hsn_tax_configuration.csv",
            mime="text/csv"
        )
    
    with col2:
        uploaded_file = st.file_uploader("Import Tax Configuration", type=["csv"])
        
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                st.success("File uploaded successfully! Preview:")
                st.dataframe(imported_df.head())
                
                if st.button("Confirm Import"):
                    # In a real implementation, this would update the database
                    st.success("Tax configuration imported successfully!")
            except Exception as e:
                st.error(f"Error importing file: {e}")

def show_tax_reporting():
    """Display tax reporting dashboards and analytics"""
    st.header("Tax Reporting & Analytics")
    
    # Create sample reporting periods
    reporting_periods = [
        "Q1 2024 (Jan-Mar)", 
        "Q2 2024 (Apr-Jun)", 
        "Q3 2024 (Jul-Sep)", 
        "Q4 2024 (Oct-Dec)"
    ]
    
    selected_period = st.selectbox("Select Reporting Period", reporting_periods)
    
    # Create tabs for different reports
    tab1, tab2, tab3 = st.tabs(["GSTR Summary", "HSN Summary", "Tax Analytics"])
    
    with tab1:
        st.subheader("GSTR Report Summary")
        
        # Create sample GSTR data
        gstr_data = pd.DataFrame({
            "Return Type": ["GSTR-1", "GSTR-3B", "GSTR-9"],
            "Status": ["Filed", "Filed", "Pending"],
            "Filing Date": ["15-04-2024", "20-04-2024", "31-12-2024"],
            "Total Tax (INR)": [125000, 132000, 580000]
        })
        
        st.dataframe(gstr_data, use_container_width=True)
        
        # Show transaction summary
        st.subheader("Transaction Summary")
        
        outward_supply = pd.DataFrame({
            "Supply Type": ["B2B", "B2C (Large)", "B2C (Small)", "Export", "SEZ Supplies"],
            "Invoice Count": [120, 45, 310, 25, 5],
            "Taxable Value (INR)": [980000, 320000, 420000, 250000, 75000],
            "Tax Amount (INR)": [176400, 57600, 75600, 0, 0]
        })
        
        st.dataframe(outward_supply, use_container_width=True)
        
        # Create visualization
        fig = px.bar(outward_supply, 
                     x="Supply Type", 
                     y="Taxable Value (INR)",
                     text="Invoice Count",
                     color="Supply Type",
                     title="Outward Supplies by Type")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("HSN Summary Report")
        
        # Create sample HSN summary
        hsn_summary = pd.DataFrame({
            "HSN Code": ["6203.42.10", "6204.62.10", "5209.42.00", "6205.30.10", "6211.42.10", "5211.42.00"],
            "Description": [
                "Men's denim trousers and jeans",
                "Women's denim trousers and jeans",
                "Denim fabric (>=85% cotton)",
                "Men's denim shirts",
                "Women's denim garments",
                "Denim fabric (<85% cotton, mixed)"
            ],
            "Quantity": [5200, 6800, 15000, 3200, 2100, 8500],
            "UQC": ["PCS", "PCS", "MTR", "PCS", "PCS", "MTR"],
            "Taxable Value (INR)": [2340000, 3060000, 1875000, 1280000, 945000, 1020000],
            "Tax Rate (%)": [5, 5, 5, 5, 5, 5],
            "Tax Amount (INR)": [117000, 153000, 93750, 64000, 47250, 51000]
        })
        
        st.dataframe(hsn_summary, use_container_width=True)
        
        # Create visualization
        fig = px.pie(hsn_summary, 
                     values="Taxable Value (INR)", 
                     names="HSN Code",
                     hover_data=["Description", "Tax Amount (INR)"],
                     title="Distribution of Taxable Value by HSN Code")
        
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        
        # Show UQC distribution
        fig = px.bar(hsn_summary, 
                     x="HSN Code", 
                     y="Quantity",
                     color="UQC",
                     title="Quantity by HSN Code and Unit (UQC)",
                     barmode="group")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Tax Analytics")
        
        # Create tax analytics metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Output Tax", value="₹ 5,26,000", delta="12.3%")
        
        with col2:
            st.metric(label="Total Input Tax Credit", value="₹ 3,94,500", delta="-5.2%")
        
        with col3:
            st.metric(label="Net Tax Liability", value="₹ 1,31,500", delta="8.7%")
        
        # Show monthly trend
        monthly_tax = pd.DataFrame({
            "Month": ["January", "February", "March"],
            "Output Tax": [165000, 172000, 189000],
            "Input Tax": [124000, 130000, 140500],
            "Net Tax": [41000, 42000, 48500]
        })
        
        # Create multi-line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_tax["Month"], y=monthly_tax["Output Tax"],
            mode="lines+markers", name="Output Tax"
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_tax["Month"], y=monthly_tax["Input Tax"],
            mode="lines+markers", name="Input Tax"
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_tax["Month"], y=monthly_tax["Net Tax"],
            mode="lines+markers", name="Net Tax",
            line=dict(dash="dash")
        ))
        
        fig.update_layout(
            title="Monthly Tax Trend",
            xaxis_title="Month",
            yaxis_title="Amount (INR)",
            legend_title="Tax Type"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show HSN-wise tax rate distribution
        tax_rate_dist = pd.DataFrame({
            "Tax Rate (%)": [0, 5, 12, 18, 28],
            "Taxable Value (INR)": [325000, 8645000, 1250000, 750000, 0],
            "Tax Amount (INR)": [0, 432250, 150000, 135000, 0]
        })
        
        fig = px.bar(tax_rate_dist, 
                     x="Tax Rate (%)", 
                     y="Taxable Value (INR)",
                     text="Tax Amount (INR)",
                     title="Distribution by Tax Rate",
                     color="Tax Rate (%)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add tax compliance calendar
        st.subheader("Tax Compliance Calendar")
        
        compliance_calendar = pd.DataFrame({
            "Return": ["GSTR-1", "GSTR-3B", "GSTR-9"],
            "Due Date": ["11th of next month", "20th of next month", "31st December"],
            "Next Filing": ["11-05-2024", "20-05-2024", "31-12-2024"],
            "Status": ["Upcoming", "Upcoming", "Upcoming"]
        })
        
        st.dataframe(compliance_calendar, use_container_width=True)

if __name__ == "__main__":
    show_hsn_tax_mapping()