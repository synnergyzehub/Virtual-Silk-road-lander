"""
Woven Supply - Supply Chain Transparency Platform

This module implements the Woven Supply platform of the Genesis Ecosystem,
providing divinely aligned supply chain management and verification features.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import numpy as np

def show_woven_supply():
    """Display the Woven Supply interface"""
    st.title("Woven Supply")
    st.subheader("Divine Supply Chain Transparency Platform")
    
    # Description
    st.markdown("""
    Woven Supply provides divine verification of supply chains, ensuring ethical sourcing, 
    transparent production, and righteous commercial relationships throughout the value network.
    """)
    
    # Main navigation tabs
    tabs = st.tabs([
        "Supply Dashboard", 
        "Supplier Directory", 
        "Ethical Sourcing", 
        "Divine Verification", 
        "Supply Intelligence"
    ])
    
    # Tab 1: Supply Dashboard
    with tabs[0]:
        show_supply_dashboard()
    
    # Tab 2: Supplier Directory
    with tabs[1]:
        show_supplier_directory()
    
    # Tab 3: Ethical Sourcing
    with tabs[2]:
        show_ethical_sourcing()
    
    # Tab 4: Divine Verification
    with tabs[3]:
        show_divine_verification()
    
    # Tab 5: Supply Intelligence
    with tabs[4]:
        show_supply_intelligence()

def show_supply_dashboard():
    """Display the Supply Dashboard tab"""
    st.header("Supply Dashboard")
    
    # Supply Chain Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Verified Suppliers", f"{random.randint(120, 250)}", f"+{random.randint(5, 15)}")
    
    with col2:
        st.metric("Avg. Divine Alignment", f"{random.randint(83, 92)}%", f"+{random.randint(1, 3)}%")
    
    with col3:
        st.metric("Ethical Score", f"{random.randint(85, 95)}/100", f"+{random.randint(1, 4)}")
    
    with col4:
        st.metric("Supply Risk Index", f"{random.randint(15, 30)}%", f"-{random.randint(1, 5)}%")
    
    # Supply Chain Map
    st.subheader("Divine Supply Network Map")
    
    # This would be a placeholder for an actual map visualization
    # In a real implementation, this would use a mapping library to show
    # the geographic distribution of suppliers with divine alignment overlays
    
    # For illustration, create a simple map placeholder
    map_placeholder = st.container()
    with map_placeholder:
        st.markdown("""
        <div style="background-color: #f0f2f6; height: 400px; display: flex; 
                   align-items: center; justify-content: center; border-radius: 10px;">
            <div style="text-align: center;">
                <h3>Divine Supply Network Visualization</h3>
                <p>Global view of your supply chain with divine alignment indicators</p>
                <p>(Interactive map would appear here in the actual implementation)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Supply Chain Health
    st.subheader("Supply Chain Health")
    
    # Create columns for KPIs
    col1, col2 = st.columns(2)
    
    with col1:
        # Supply risk by category
        risk_categories = ["Raw Materials", "Manufacturing", "Logistics", "Distribution", "Retail"]
        risk_values = [random.randint(10, 40) for _ in range(len(risk_categories))]
        
        df_risk = pd.DataFrame({
            "Category": risk_categories,
            "Risk Level": risk_values
        })
        
        fig = px.bar(
            df_risk,
            x="Category",
            y="Risk Level",
            title="Supply Risk by Category (%)",
            color="Risk Level",
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Divine alignment by region
        regions = ["North America", "Europe", "Asia", "South America", "Africa"]
        alignment_values = [random.randint(75, 95) for _ in range(len(regions))]
        
        df_alignment = pd.DataFrame({
            "Region": regions,
            "Divine Alignment": alignment_values
        })
        
        fig = px.bar(
            df_alignment,
            x="Region",
            y="Divine Alignment",
            title="Divine Alignment by Region (%)",
            color="Divine Alignment",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Supply Chain Events
    st.subheader("Recent Supply Chain Events")
    
    # Generate sample events
    events = []
    event_types = ["New Supplier Verified", "Compliance Issue Detected", "Alignment Improvement", 
                  "Material Shortage Risk", "Delivery Delay", "Divine Audit Completed"]
    
    for i in range(8):
        event_type = random.choice(event_types)
        date = (datetime.now() - timedelta(hours=random.randint(1, 168))).strftime("%Y-%m-%d %H:%M")
        supplier = f"Supplier-{random.randint(1000, 9999)}"
        impact = random.choice(["High", "Medium", "Low"])
        alignment_change = random.randint(-5, 10)
        alignment_icon = "📈" if alignment_change >= 0 else "📉"
        
        events.append({
            "Date": date,
            "Event Type": event_type,
            "Supplier": supplier,
            "Impact": impact,
            "Alignment Change": f"{alignment_icon} {alignment_change}%"
        })
    
    df_events = pd.DataFrame(events)
    
    # Display events table
    st.dataframe(df_events, use_container_width=True)
    
    # Call to Action
    st.success("💡 Tip: Improve your supply chain's divine alignment by conducting ethical audits on high-risk suppliers.")

def show_supplier_directory():
    """Display the Supplier Directory tab"""
    st.header("Supplier Directory")
    
    # Supplier Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Supplier Category", ["All Categories", "Raw Materials", "Manufacturing", "Packaging", "Logistics", "Services"])
    
    with col2:
        st.selectbox("Divine Alignment", ["All Levels", "Exceptional (90-100%)", "Strong (80-89%)", "Moderate (70-79%)", "Needs Improvement (<70%)"])
    
    with col3:
        st.selectbox("Region", ["All Regions", "North America", "Europe", "Asia", "South America", "Africa", "Australia"])
    
    # Supplier Directory Table
    st.subheader("Verified Suppliers")
    
    # Generate sample supplier data
    suppliers = []
    categories = ["Raw Materials", "Manufacturing", "Packaging", "Logistics", "Services"]
    regions = ["North America", "Europe", "Asia", "South America", "Africa", "Australia"]
    
    for i in range(15):
        supplier_id = f"SUP-{random.randint(10000, 99999)}"
        name = f"Supplier {random.randint(100, 999)}"
        category = random.choice(categories)
        region = random.choice(regions)
        divine_alignment = random.randint(65, 98)
        ethical_score = random.randint(70, 95)
        risk_level = random.choice(["Low", "Medium", "High"])
        last_audit = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
        
        suppliers.append({
            "ID": supplier_id,
            "Name": name,
            "Category": category,
            "Region": region,
            "Divine Alignment": divine_alignment,
            "Ethical Score": ethical_score,
            "Risk Level": risk_level,
            "Last Audit": last_audit
        })
    
    df_suppliers = pd.DataFrame(suppliers)
    
    # Custom formatting for the dataframe
    def highlight_alignment(val):
        if val >= 90:
            color = 'green'
        elif val >= 80:
            color = 'lightgreen'
        elif val >= 70:
            color = 'yellow'
        else:
            color = 'red'
        return f'background-color: {color}'
    
    # Display the suppliers
    st.dataframe(df_suppliers.style.applymap(highlight_alignment, subset=['Divine Alignment']), use_container_width=True)
    
    # Supplier management actions
    st.subheader("Supplier Management Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Add New Supplier")
    
    with col2:
        st.button("Generate Alignment Report")
    
    with col3:
        st.button("Schedule Divine Audit")
    
    # Supplier distribution visualization
    st.subheader("Supplier Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by category
        category_counts = {}
        for category in categories:
            category_counts[category] = len(df_suppliers[df_suppliers["Category"] == category])
        
        df_categories = pd.DataFrame({
            "Category": list(category_counts.keys()),
            "Count": list(category_counts.values())
        })
        
        fig = px.pie(df_categories, values="Count", names="Category", title="Suppliers by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution by alignment level
        alignment_levels = {
            "Exceptional (90-100%)": len(df_suppliers[df_suppliers["Divine Alignment"] >= 90]),
            "Strong (80-89%)": len(df_suppliers[(df_suppliers["Divine Alignment"] >= 80) & (df_suppliers["Divine Alignment"] < 90)]),
            "Moderate (70-79%)": len(df_suppliers[(df_suppliers["Divine Alignment"] >= 70) & (df_suppliers["Divine Alignment"] < 80)]),
            "Needs Improvement (<70%)": len(df_suppliers[df_suppliers["Divine Alignment"] < 70])
        }
        
        df_alignment = pd.DataFrame({
            "Alignment Level": list(alignment_levels.keys()),
            "Count": list(alignment_levels.values())
        })
        
        fig = px.pie(df_alignment, values="Count", names="Alignment Level", title="Suppliers by Divine Alignment")
        st.plotly_chart(fig, use_container_width=True)

def show_ethical_sourcing():
    """Display the Ethical Sourcing tab"""
    st.header("Ethical Sourcing")
    
    # Introduction
    st.markdown("""
    The Ethical Sourcing module helps ensure all materials and services in your supply chain
    are ethically sourced according to divine principles. Monitor ethical practices, identify
    improvement opportunities, and maintain a righteous supply chain.
    """)
    
    # Ethical sourcing metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Ethical Sourcing Score", f"{random.randint(82, 92)}%", f"+{random.randint(1, 3)}%")
    
    with col2:
        st.metric("Fair Labor Compliance", f"{random.randint(85, 95)}%", f"+{random.randint(1, 4)}%")
    
    with col3:
        st.metric("Environmental Compliance", f"{random.randint(80, 90)}%", f"+{random.randint(1, 5)}%")
    
    with col4:
        st.metric("Verified Ethical Materials", f"{random.randint(75, 90)}%", f"+{random.randint(2, 6)}%")
    
    # Ethical dimensions assessment
    st.subheader("Ethical Dimensions Assessment")
    
    # Generate ethical dimensions data
    dimensions = [
        "Fair Labor Practices",
        "Environmental Responsibility",
        "Ethical Material Sourcing",
        "Community Impact",
        "Transparency",
        "Animal Welfare",
        "Anti-Corruption Practices"
    ]
    
    current_scores = [random.randint(70, 95) for _ in range(len(dimensions))]
    target_scores = [min(current + random.randint(5, 15), 100) for current in current_scores]
    
    df_dimensions = pd.DataFrame({
        "Dimension": dimensions,
        "Current Score": current_scores,
        "Target Score": target_scores
    })
    
    # Create a horizontal bar chart with current and target scores
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_dimensions["Dimension"],
        x=df_dimensions["Current Score"],
        name="Current Score",
        orientation='h',
        marker=dict(color='rgba(50, 171, 96, 0.7)')
    ))
    
    fig.add_trace(go.Bar(
        y=df_dimensions["Dimension"],
        x=df_dimensions["Target Score"],
        name="Target Score",
        orientation='h',
        marker=dict(color='rgba(50, 171, 96, 0.3)')
    ))
    
    fig.update_layout(
        title="Ethical Sourcing Dimensions",
        xaxis_title="Score",
        barmode='overlay',
        height=400,
        xaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Material ethical verification
    st.subheader("Material Ethical Verification Status")
    
    # Create sample data for material verification
    materials = [
        "Cotton",
        "Polyester",
        "Wool",
        "Silk",
        "Leather",
        "Metal Components",
        "Packaging Materials",
        "Dyes and Chemicals"
    ]
    
    verification_statuses = [
        "Fully Verified",
        "Partially Verified",
        "Verification in Progress",
        "Fully Verified",
        "Partially Verified",
        "Fully Verified",
        "Fully Verified",
        "Verification in Progress"
    ]
    
    ethical_scores = [
        random.randint(90, 98),
        random.randint(75, 85),
        random.randint(60, 70),
        random.randint(90, 98),
        random.randint(75, 85),
        random.randint(90, 98),
        random.randint(90, 98),
        random.randint(60, 70)
    ]
    
    verification_dates = [
        (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        for _ in range(len(materials))
    ]
    
    df_materials = pd.DataFrame({
        "Material": materials,
        "Verification Status": verification_statuses,
        "Ethical Score": ethical_scores,
        "Last Verified": verification_dates
    })
    
    # Display the materials verification table
    st.dataframe(df_materials, use_container_width=True)
    
    # Ethical improvement plan
    st.subheader("Ethical Sourcing Improvement Plan")
    
    # Identify areas for improvement (lowest scores)
    low_scoring = df_dimensions.sort_values("Current Score").head(3)
    
    for _, row in low_scoring.iterrows():
        dimension = row["Dimension"]
        current = row["Current Score"]
        target = row["Target Score"]
        
        st.markdown(f"#### {dimension}: {current}% → {target}%")
        
        if dimension == "Fair Labor Practices":
            st.markdown("""
            **Improvement Actions:**
            - Conduct divine labor audits for all Tier 1 suppliers
            - Implement fair wage verification program
            - Establish worker well-being monitoring system
            """)
        elif dimension == "Environmental Responsibility":
            st.markdown("""
            **Improvement Actions:**
            - Implement environmental impact assessments for all suppliers
            - Develop supplier environmental improvement program
            - Establish resource conservation targets
            """)
        elif dimension == "Ethical Material Sourcing":
            st.markdown("""
            **Improvement Actions:**
            - Complete material traceability for all primary materials
            - Implement ethical certification requirements
            - Develop alternative sourcing for high-risk materials
            """)
        elif dimension == "Community Impact":
            st.markdown("""
            **Improvement Actions:**
            - Assess community impact of major suppliers
            - Develop community benefit requirements
            - Implement community development programs
            """)
        elif dimension == "Transparency":
            st.markdown("""
            **Improvement Actions:**
            - Implement supplier transparency requirements
            - Develop public reporting standards
            - Create supply chain visibility tools
            """)
        elif dimension == "Animal Welfare":
            st.markdown("""
            **Improvement Actions:**
            - Implement animal welfare verification
            - Develop alternative material strategy
            - Establish animal-free certification program
            """)
        elif dimension == "Anti-Corruption Practices":
            st.markdown("""
            **Improvement Actions:**
            - Implement anti-corruption verification
            - Develop ethical business practice training
            - Establish whistleblower protection program
            """)

def show_divine_verification():
    """Display the Divine Verification tab"""
    st.header("Divine Verification")
    
    # Introduction
    st.markdown("""
    The Divine Verification module provides righteous verification of your entire supply chain,
    ensuring alignment with divine principles at every stage. Use divine verification to ensure
    your supply chain honors ethical values and righteous practices.
    """)
    
    # Verification process
    st.subheader("Divine Verification Process")
    
    # Sample verification stages visualization
    stages = ["Initial Assessment", "Document Review", "Divine Audit", "Verification", "Continuous Monitoring"]
    
    # Create a visualization of the verification process
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 30px;">
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px;">
                Initial Assessment
            </div>
            <div style="font-size: 24px; margin-top: 5px;">↓</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px;">
                Document Review
            </div>
            <div style="font-size: 24px; margin-top: 5px;">↓</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px;">
                Divine Audit
            </div>
            <div style="font-size: 24px; margin-top: 5px;">↓</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px;">
                Verification
            </div>
            <div style="font-size: 24px; margin-top: 5px;">↓</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px;">
                Continuous Monitoring
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Fully Verified Suppliers", f"{random.randint(70, 90)}%", f"+{random.randint(2, 5)}%")
    
    with col2:
        st.metric("Verification Depth", f"{random.randint(2, 4)} Tiers", f"+{random.randint(0, 1)} Tier")
    
    with col3:
        st.metric("Avg. Verification Score", f"{random.randint(85, 95)}/100", f"+{random.randint(1, 3)}")
    
    with col4:
        st.metric("Divine Audits Completed", f"{random.randint(40, 80)}", f"+{random.randint(5, 10)}")
    
    # Divine verification status
    st.subheader("Divine Verification Status")
    
    # Create sample verification status data
    supplier_categories = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]
    
    verified_percentages = [
        random.randint(85, 95),
        random.randint(70, 85),
        random.randint(40, 60),
        random.randint(20, 40)
    ]
    
    in_progress_percentages = [
        random.randint(5, 15),
        random.randint(10, 20),
        random.randint(20, 40),
        random.randint(30, 50)
    ]
    
    not_started_percentages = []
    for i in range(len(supplier_categories)):
        not_started_percentages.append(100 - verified_percentages[i] - in_progress_percentages[i])
    
    # Create DataFrame
    df_status = pd.DataFrame({
        "Category": supplier_categories,
        "Verified": verified_percentages,
        "In Progress": in_progress_percentages,
        "Not Started": not_started_percentages
    })
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_status["Category"],
        x=df_status["Verified"],
        name="Verified",
        orientation='h',
        marker=dict(color='#4CAF50')
    ))
    
    fig.add_trace(go.Bar(
        y=df_status["Category"],
        x=df_status["In Progress"],
        name="In Progress",
        orientation='h',
        marker=dict(color='#FFC107')
    ))
    
    fig.add_trace(go.Bar(
        y=df_status["Category"],
        x=df_status["Not Started"],
        name="Not Started",
        orientation='h',
        marker=dict(color='#E53935')
    ))
    
    fig.update_layout(
        title="Verification Status by Supplier Tier",
        barmode='stack',
        height=400,
        xaxis=dict(range=[0, 100], title="Percentage")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Divine verification results
    st.subheader("Recent Divine Verification Results")
    
    # Generate sample verification results
    verifications = []
    
    for i in range(10):
        supplier_id = f"SUP-{random.randint(10000, 99999)}"
        supplier_name = f"Supplier {random.randint(100, 999)}"
        tier = random.choice(["Tier 1", "Tier 2", "Tier 3"])
        divine_score = random.randint(70, 98)
        status = "Verified" if divine_score >= 80 else "Conditional" if divine_score >= 70 else "Failed"
        verification_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        
        verifications.append({
            "Supplier ID": supplier_id,
            "Supplier Name": supplier_name,
            "Tier": tier,
            "Divine Score": divine_score,
            "Status": status,
            "Verification Date": verification_date
        })
    
    df_verifications = pd.DataFrame(verifications)
    
    # Display verification results
    st.dataframe(df_verifications, use_container_width=True)
    
    # Verification actions
    st.subheader("Divine Verification Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Schedule New Verification")
    
    with col2:
        st.button("Generate Verification Report")
    
    with col3:
        st.button("View Verification History")

def show_supply_intelligence():
    """Display the Supply Intelligence tab"""
    st.header("Supply Intelligence")
    
    # Introduction
    st.markdown("""
    The Supply Intelligence module provides divine insight into your supply chain performance,
    risks, and opportunities. Use supply intelligence to make righteous decisions and ensure
    divine alignment throughout your supply network.
    """)
    
    # Performance metrics
    st.subheader("Supply Chain Performance Metrics")
    
    # Create columns for KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("On-Time Delivery", f"{random.randint(90, 98)}%", f"+{random.randint(1, 3)}%")
    
    with col2:
        st.metric("Quality Compliance", f"{random.randint(92, 99)}%", f"+{random.randint(1, 2)}%")
    
    with col3:
        st.metric("Cost Efficiency", f"{random.randint(85, 95)}%", f"+{random.randint(1, 4)}%")
    
    with col4:
        st.metric("Responsiveness", f"{random.randint(88, 96)}%", f"+{random.randint(1, 3)}%")
    
    # Performance trends
    st.subheader("Performance Trends")
    
    # Date selection
    date_range = st.selectbox(
        "Time Period",
        ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last 12 Months"]
    )
    
    # Generate sample time series data
    if date_range == "Last 30 Days":
        dates = pd.date_range(end=datetime.now(), periods=30).tolist()
    elif date_range == "Last 90 Days":
        dates = pd.date_range(end=datetime.now(), periods=90).tolist()
    elif date_range == "Last 6 Months":
        dates = pd.date_range(end=datetime.now(), periods=6, freq='M').tolist()
    else:
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M').tolist()
    
    # Create sample performance metrics over time
    on_time = [random.randint(85, 98) for _ in range(len(dates))]
    quality = [random.randint(90, 99) for _ in range(len(dates))]
    
    df_trends = pd.DataFrame({
        "Date": dates,
        "On-Time Delivery": on_time,
        "Quality Compliance": quality
    })
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_trends["Date"],
        y=df_trends["On-Time Delivery"],
        mode="lines+markers",
        name="On-Time Delivery",
        line=dict(color="#1f77b4")
    ))
    
    fig.add_trace(go.Scatter(
        x=df_trends["Date"],
        y=df_trends["Quality Compliance"],
        mode="lines+markers",
        name="Quality Compliance",
        line=dict(color="#ff7f0e")
    ))
    
    fig.update_layout(
        title="Supply Chain Performance Trends",
        xaxis_title="Date",
        yaxis_title="Percentage",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        yaxis=dict(range=[80, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk assessment
    st.subheader("Divine Risk Assessment")
    
    # Create sample risk data
    risk_categories = [
        "Supply Disruption",
        "Quality Issues",
        "Ethical Violations",
        "Price Volatility",
        "Environmental Impact",
        "Labor Practices",
        "Regulatory Compliance"
    ]
    
    risk_probabilities = [
        random.randint(10, 40),
        random.randint(5, 30),
        random.randint(5, 20),
        random.randint(20, 50),
        random.randint(10, 30),
        random.randint(5, 25),
        random.randint(5, 20)
    ]
    
    risk_impacts = [
        random.randint(30, 80),
        random.randint(40, 70),
        random.randint(60, 90),
        random.randint(30, 60),
        random.randint(50, 80),
        random.randint(60, 90),
        random.randint(50, 80)
    ]
    
    risk_scores = []
    for i in range(len(risk_categories)):
        risk_scores.append((risk_probabilities[i] * risk_impacts[i]) / 100)
    
    df_risks = pd.DataFrame({
        "Risk Category": risk_categories,
        "Probability": risk_probabilities,
        "Impact": risk_impacts,
        "Risk Score": risk_scores
    })
    
    # Create risk matrix
    fig = px.scatter(
        df_risks,
        x="Probability",
        y="Impact",
        text="Risk Category",
        size="Risk Score",
        color="Risk Score",
        color_continuous_scale=px.colors.sequential.Reds,
        title="Divine Risk Matrix",
        size_max=25
    )
    
    fig.update_traces(textposition="top center")
    
    fig.update_layout(
        xaxis=dict(range=[0, 100], title="Probability"),
        yaxis=dict(range=[0, 100], title="Impact"),
        height=500
    )
    
    # Add quadrant lines
    fig.add_shape(
        type="line",
        x0=50, y0=0,
        x1=50, y1=100,
        line=dict(color="gray", dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=0, y0=50,
        x1=100, y1=50,
        line=dict(color="gray", dash="dash")
    )
    
    # Add quadrant labels
    fig.add_annotation(x=25, y=75, text="High Impact<br>Low Probability", showarrow=False)
    fig.add_annotation(x=75, y=75, text="High Impact<br>High Probability", showarrow=False)
    fig.add_annotation(x=25, y=25, text="Low Impact<br>Low Probability", showarrow=False)
    fig.add_annotation(x=75, y=25, text="Low Impact<br>High Probability", showarrow=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Supply chain insights
    st.subheader("Divine Supply Insights")
    
    # Create sample insights
    insights = [
        {
            "title": "Ethical Compliance Improvement Opportunity",
            "description": "Tier 2 suppliers in Asia region show 15% lower ethical compliance scores compared to other regions. Divine audit recommended.",
            "impact": "Medium",
            "recommendation": "Conduct targeted divine audits and implement improvement program."
        },
        {
            "title": "Supply Disruption Risk Increasing",
            "description": "Raw material suppliers reporting capacity constraints due to regional economic conditions. Potential delivery delays in Q3.",
            "impact": "High",
            "recommendation": "Identify alternative sources and increase safety stock levels."
        },
        {
            "title": "Divine Alignment Enhancement",
            "description": "Suppliers implementing enhanced labor practices showing 12% higher divine alignment scores. Opportunity to scale practices.",
            "impact": "Medium",
            "recommendation": "Share best practices across supplier network and implement incentive program."
        }
    ]
    
    # Display insights
    for i, insight in enumerate(insights, 1):
        with st.expander(f"{i}. {insight['title']} (Impact: {insight['impact']})"):
            st.markdown(f"**Description:** {insight['description']}")
            st.markdown(f"**Recommendation:** {insight['recommendation']}")

if __name__ == "__main__":
    show_woven_supply()