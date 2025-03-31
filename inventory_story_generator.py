import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import datetime
import random
from sqlalchemy import create_engine, text
import os
from database import get_db_session

def show_inventory_story_generator():
    """
    Main function to display the Inventory Movement Story Generator
    Provides narrative insights from stock patterns
    """
    st.title("Inventory Movement Story Generator")
    st.subheader("Narrative Insights from Stock Patterns")
    
    # Sidebar filters
    with st.sidebar:
        st.subheader("Story Configuration")
        
        # Time period selection
        time_period = st.selectbox(
            "Analysis Period",
            ["Last 7 days", "Last 30 days", "Last Quarter", "Year-to-Date", "Custom Range"],
            index=1
        )
        
        if time_period == "Custom Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
            with col2:
                end_date = st.date_input("End Date", value=datetime.date.today())
        
        # Focus area selection
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Inventory Turnover", "Stock Movements", "Critical Stock Patterns", 
             "Value Fluctuations", "Seasonal Trends", "Location Comparisons",
             "Top Performers", "Sluggish Items", "Supply Chain Bottlenecks"],
            default=["Inventory Turnover", "Stock Movements", "Critical Stock Patterns"]
        )
        
        # Location types filter
        location_types = st.multiselect(
            "Location Types",
            ["Factory", "Warehouse", "Store"],
            default=["Factory", "Warehouse", "Store"]
        )
        
        # Story format options
        st.subheader("Story Format")
        narrative_style = st.select_slider(
            "Narrative Style",
            options=["Concise", "Balanced", "Detailed"],
            value="Balanced"
        )
        
        include_visuals = st.checkbox("Include Visuals", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
        include_predictions = st.checkbox("Include Predictions", value=True)
        
        # Generate story button
        generate_btn = st.button("Generate Inventory Story", type="primary", use_container_width=True)
    
    # Main content area - Tabs
    tabs = st.tabs(["Executive Summary", "Detailed Analysis", "Visualizations", "Recommendations"])
    
    # If generate button is clicked, create and display the story
    if "generate_story" not in st.session_state:
        st.session_state.generate_story = False
        
    if generate_btn:
        st.session_state.generate_story = True
        st.session_state.focus_areas = focus_areas
        st.session_state.location_types = location_types
        st.session_state.narrative_style = narrative_style
        st.session_state.include_visuals = include_visuals
        st.session_state.include_recommendations = include_recommendations
        st.session_state.include_predictions = include_predictions
        
        if time_period == "Custom Range":
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
        else:
            if time_period == "Last 7 days":
                st.session_state.start_date = datetime.date.today() - datetime.timedelta(days=7)
            elif time_period == "Last 30 days":
                st.session_state.start_date = datetime.date.today() - datetime.timedelta(days=30)
            elif time_period == "Last Quarter":
                st.session_state.start_date = datetime.date.today() - datetime.timedelta(days=90)
            elif time_period == "Year-to-Date":
                st.session_state.start_date = datetime.date(datetime.date.today().year, 1, 1)
            st.session_state.end_date = datetime.date.today()
    
    if st.session_state.get("generate_story", False):
        # Generate all the story components
        executive_summary = generate_executive_summary(
            st.session_state.start_date,
            st.session_state.end_date,
            st.session_state.focus_areas,
            st.session_state.location_types,
            st.session_state.narrative_style
        )
        
        detailed_analysis = generate_detailed_analysis(
            st.session_state.start_date,
            st.session_state.end_date,
            st.session_state.focus_areas,
            st.session_state.location_types,
            st.session_state.narrative_style
        )
        
        recommendations = generate_recommendations(
            st.session_state.start_date,
            st.session_state.end_date,
            st.session_state.focus_areas,
            st.session_state.location_types
        ) if st.session_state.include_recommendations else None
        
        predictions = generate_predictions(
            st.session_state.start_date,
            st.session_state.end_date,
            st.session_state.focus_areas,
            st.session_state.location_types
        ) if st.session_state.include_predictions else None
        
        # Executive Summary Tab
        with tabs[0]:
            st.markdown(f"### Executive Summary ({st.session_state.start_date} to {st.session_state.end_date})")
            st.markdown(executive_summary)
            
            if st.session_state.include_visuals:
                # Key metrics visualization
                st.subheader("Key Metrics Overview")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Inventory Turnover", "4.2", "+0.3")
                with col2:
                    st.metric("Average Days in Inventory", "32", "-3")
                with col3:
                    st.metric("Stock Outs", "12", "-5")
                with col4:
                    st.metric("Excess Stock Value", "₹48L", "-12%")
                
                # Summary chart
                st.subheader("Stock Health Trend")
                dates = pd.date_range(st.session_state.start_date, st.session_state.end_date, freq='D')
                optimal = [random.randint(45, 55) for _ in range(len(dates))]
                excess = [random.randint(20, 30) for _ in range(len(dates))]
                low = [random.randint(10, 20) for _ in range(len(dates))]
                critical = [random.randint(5, 10) for _ in range(len(dates))]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=optimal, stackgroup='one', name='Optimal', line=dict(width=0), fillcolor='rgba(0, 204, 150, 0.8)'))
                fig.add_trace(go.Scatter(x=dates, y=excess, stackgroup='one', name='Excess', line=dict(width=0), fillcolor='rgba(99, 110, 250, 0.8)'))
                fig.add_trace(go.Scatter(x=dates, y=low, stackgroup='one', name='Low', line=dict(width=0), fillcolor='rgba(255, 165, 0, 0.8)'))
                fig.add_trace(go.Scatter(x=dates, y=critical, stackgroup='one', name='Critical', line=dict(width=0), fillcolor='rgba(255, 75, 75, 0.8)'))
                
                fig.update_layout(
                    title='Stock Health Distribution Over Time',
                    xaxis_title='Date',
                    yaxis_title='Percentage of SKUs',
                    legend=dict(
                        y=1.1,
                        x=0.5,
                        xanchor='center',
                        orientation='h'
                    ),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Print report options
            cols = st.columns(2)
            with cols[0]:
                if st.button("Download Full Report", use_container_width=True):
                    st.info("Preparing PDF report for download...")
            with cols[1]:
                if st.button("Share Report", use_container_width=True):
                    st.info("Preparing report for sharing...")
        
        # Detailed Analysis Tab
        with tabs[1]:
            st.markdown("### Detailed Analysis")
            
            # Create sections based on focus areas
            for area in st.session_state.focus_areas:
                with st.expander(area, expanded=True):
                    # Get the relevant section of the detailed analysis
                    section_text = detailed_analysis.get(area, "No analysis available for this focus area.")
                    st.markdown(section_text)
                    
                    if st.session_state.include_visuals:
                        # Generate a visualization specific to this focus area
                        if area == "Inventory Turnover":
                            show_inventory_turnover_chart()
                        elif area == "Stock Movements":
                            show_stock_movement_chart()
                        elif area == "Critical Stock Patterns":
                            show_critical_stock_chart()
                        elif area == "Value Fluctuations":
                            show_value_fluctuation_chart()
                        elif area == "Location Comparisons":
                            show_location_comparison_chart()
        
        # Visualizations Tab
        with tabs[2]:
            st.markdown("### Visual Insights")
            
            if st.session_state.include_visuals:
                # Visualization selection
                viz_type = st.selectbox(
                    "Select Visualization Type",
                    ["Inventory Flow", "Stock Health by Location", "Time Series Analysis", 
                     "Value Distribution", "Movement Patterns", "Comparison Matrix"]
                )
                
                if viz_type == "Inventory Flow":
                    show_inventory_flow_sankey()
                elif viz_type == "Stock Health by Location":
                    show_stock_health_by_location()
                elif viz_type == "Time Series Analysis":
                    show_time_series_analysis()
                elif viz_type == "Value Distribution":
                    show_value_distribution()
                elif viz_type == "Movement Patterns":
                    show_movement_patterns()
                elif viz_type == "Comparison Matrix":
                    show_comparison_matrix()
            else:
                st.info("Visuals are disabled. Enable them in the sidebar to see visualizations.")
        
        # Recommendations Tab
        with tabs[3]:
            st.markdown("### Recommendations & Predictions")
            
            if st.session_state.include_recommendations:
                st.subheader("Recommended Actions")
                for category, recs in recommendations.items():
                    with st.expander(f"{category} Recommendations", expanded=True):
                        for i, rec in enumerate(recs, 1):
                            st.markdown(f"**{i}. {rec['title']}**")
                            st.markdown(rec['description'])
                            
                            # Priority indicator
                            priority_color = {
                                "High": "🔴", 
                                "Medium": "🟠", 
                                "Low": "🟢"
                            }
                            st.markdown(f"**Priority:** {priority_color.get(rec['priority'], '⚪')} {rec['priority']}")
                            
                            # Estimated impact
                            if 'impact' in rec:
                                st.markdown(f"**Estimated Impact:** {rec['impact']}")
                            
                            st.markdown("---")
            
            if st.session_state.include_predictions:
                st.subheader("Future Predictions")
                
                # Show predictions
                for prediction in predictions:
                    with st.expander(prediction['title'], expanded=True):
                        st.markdown(prediction['description'])
                        
                        # Confidence level
                        confidence = prediction.get('confidence', 'Medium')
                        st.progress(
                            0.9 if confidence == 'High' else 0.6 if confidence == 'Medium' else 0.3,
                            text=f"Confidence: {confidence}"
                        )
                        
                        # Timeframe
                        if 'timeframe' in prediction:
                            st.markdown(f"**Expected Timeframe:** {prediction['timeframe']}")
                        
                        # Visual if available
                        if 'visual' in prediction and st.session_state.include_visuals:
                            if prediction['visual'] == 'trend_forecast':
                                show_trend_forecast_chart()
                            elif prediction['visual'] == 'stock_projection':
                                show_stock_projection_chart()
                
                # Prediction accuracy disclaimer
                st.info(
                    "Note: Predictions are based on historical data patterns and current trends. "
                    "Actual outcomes may vary based on market conditions and unexpected events."
                )

def generate_executive_summary(start_date, end_date, focus_areas, location_types, narrative_style):
    """Generate an executive summary based on the selected parameters"""
    
    # Note: In a real implementation, this would analyze actual data
    # Here we're generating a template-based summary
    
    # Format the date range
    date_range = f"{start_date.strftime('%d %b')} to {end_date.strftime('%d %b, %Y')}"
    
    # Create a summary based on the narrative style
    if narrative_style == "Concise":
        summary = f"""
        During the period of **{date_range}**, your inventory showed distinct patterns across {len(location_types)} location types. 
        
        **Key Findings:**
        
        * Inventory turnover increased 7.1% with most improvement in Stores
        * 3 critical stock situations prevented, saving est. ₹12L in potential lost sales
        * Excess stock reduced by 12% in Warehouses, improving liquidity
        * Factory-to-Store direct shipments reduced avg fulfillment time by 23%
        
        **Financial Impact:** Improved inventory management added ₹32L to available working capital.
        """
    else:  # Balanced or Detailed
        summary = f"""
        ## Inventory Movement Analysis: {date_range}

        During this period, your inventory management demonstrated several noteworthy patterns across {len(location_types)} location types ({', '.join(location_types)}). The analysis focused on {len(focus_areas)} key areas, revealing significant insights for operational and financial decision-making.
        
        ### Key Performance Highlights
        
        * **Inventory Turnover:** Increased by 7.1% compared to the previous period, with most significant improvement in retail stores (9.3%). Factory inventory turnover remained consistent at 4.2x.
        
        * **Stock Health:** Successfully prevented 3 critical stock situations through proactive monitoring, saving an estimated ₹12L in potential lost sales. Overall optimal stock levels improved from 62% to 71%.
        
        * **Capital Efficiency:** Excess stock was reduced by 12% in warehouse locations, improving liquidity and freeing up approximately ₹32L in working capital.
        
        * **Supply Chain Velocity:** Factory-to-Store direct shipments increased by 18%, reducing average fulfillment time by 23% and improving cash conversion cycle by 4 days.
        
        * **Transaction Volume:** Processed 253 inventory movements between locations, a 15% increase from the previous period, with 98.4% accuracy in record-keeping.
        
        The most significant improvements were observed in {location_types[0] if location_types else "Warehouses"}, while {location_types[-1] if len(location_types) > 1 else "Stores"} show opportunity for optimization.
        """
        
        # Add more details for the detailed narrative style
        if narrative_style == "Detailed":
            summary += """
            
            ### Financial Implications
            
            The improved inventory management has resulted in several financial benefits:
            
            * **Working Capital Improvement:** ₹32L reduction in capital tied to excess inventory
            * **Carrying Cost Reduction:** Approximately ₹4.8L saved in monthly storage and handling costs
            * **Stockout Prevention:** ₹12L in potential lost sales avoided through critical stock monitoring
            * **Cash Flow Benefit:** Faster inventory turnover has improved cash availability by ₹21L
            
            ### Supply Chain Resilience
            
            The inventory system has demonstrated enhanced resilience through:
            
            * Earlier detection of supply delays (avg. 3.2 days faster)
            * Reduction in emergency shipping requirements by 43%
            * Improved forecasting accuracy (MAPE reduced from 32% to 24%)
            * Enhanced visibility across all location types
            
            These improvements have positioned your inventory operations for more efficient capital utilization and improved customer satisfaction through consistent product availability.
            """
    
    return summary

def generate_detailed_analysis(start_date, end_date, focus_areas, location_types, narrative_style):
    """Generate detailed analysis for each focus area"""
    
    # Create a dictionary to hold the analysis for each focus area
    analysis = {}
    
    # Inventory Turnover Analysis
    if "Inventory Turnover" in focus_areas:
        analysis["Inventory Turnover"] = """
        ### Inventory Turnover Analysis
        
        The inventory turnover rate showed significant improvement during this period, increasing from 3.9 to 4.2 turns annually. This represents a 7.1% improvement in how efficiently your capital invested in inventory is generating sales.
        
        **Location-specific turnover rates:**
        
        * **Factories:** 4.2x (unchanged)
        * **Warehouses:** 3.8x (up from 3.5x, +8.6%)
        * **Stores:** 5.7x (up from 5.2x, +9.3%)
        
        The improved turnover in stores is primarily attributable to better replenishment timing based on the automated push system. Warehouses showed moderate improvement due to more efficient cross-docking procedures, while factories maintained consistent performance.
        
        **Product categories with highest turnover improvement:**
        
        1. Men's Slim Fit Jeans: +18%
        2. Women's Skinny Jeans: +12%
        3. Logo T-shirts: +10%
        
        **Product categories with declining turnover:**
        
        1. Denim Jackets: -5%
        2. Accessories: -3%
        
        The capital efficiency gained through improved turnover has freed up approximately ₹32L in working capital, which can now be allocated to growth initiatives or held as improved liquidity.
        """
    
    # Stock Movements Analysis
    if "Stock Movements" in focus_areas:
        analysis["Stock Movements"] = """
        ### Stock Movement Patterns
        
        During this period, 253 inventory movements were recorded between locations, representing a 15% increase in transaction volume. Several distinct patterns emerged:
        
        **Movement Flow Analysis:**
        
        * **Factory → Warehouse:** 112 movements (44% of total)
        * **Warehouse → Store:** 86 movements (34% of total)
        * **Factory → Store (Direct):** 24 movements (9% of total, +18% vs previous period)
        * **Store → Warehouse (Returns):** 18 movements (7% of total)
        * **Warehouse → Factory (Material Returns):** 8 movements (3% of total)
        * **Store → Store (Transfers):** 5 movements (2% of total)
        
        The increase in direct Factory-to-Store shipments is particularly noteworthy, reducing fulfillment times by 23% for those orders and improving cash conversion cycle by 4 days.
        
        **Movement Timing Analysis:**
        
        Movements showed clear weekly patterns:
        * Monday-Tuesday: Highest volume of Factory→Warehouse transfers (46% of such movements)
        * Thursday-Friday: Peak Warehouse→Store movements (58% of such movements)
        * Weekends: Minimal movement activity (4% of total movements)
        
        This pattern suggests optimization opportunities for logistics scheduling and labor allocation.
        
        **Unusual Movement Patterns:**
        
        Three instances of unusual movement patterns were identified:
        1. Rapid Store→Warehouse→Store cycles for premium denim jeans (potential inventory record issues)
        2. Multiple small-volume transfers from Warehouse A to Warehouse B (inefficient split shipments)
        3. High-frequency movements of accessories inventory (potential planning inefficiency)
        
        Addressing these unusual patterns could improve logistics efficiency by an estimated 8%.
        """
    
    # Critical Stock Patterns Analysis
    if "Critical Stock Patterns" in focus_areas:
        analysis["Critical Stock Patterns"] = """
        ### Critical Stock Pattern Analysis
        
        The inventory system identified and helped prevent 3 critical stock situations during this period, saving an estimated ₹12L in potential lost sales. Analysis of critical stock incidents reveals several important patterns:
        
        **Critical Stock Triggers:**
        
        * **Unexpected Demand Spikes:** 62% of critical stock situations
          - Primarily affected slim fit jeans and logo t-shirts
          - Often correlated with untracked marketing promotions
        
        * **Supply Chain Delays:** 28% of critical stock situations
          - Most commonly affected imported accessories and specialized fabrics
          - Average delay: 8.2 days beyond expected delivery
        
        * **Inventory Record Discrepancies:** 10% of critical stock situations
          - Physical inventory counts differing from system records
          - Highest discrepancy rates in Store locations (3.2%)
        
        **Early Warning Effectiveness:**
        
        The early warning system successfully identified 87% of potential critical stock situations at least 3 days before they would have occurred, allowing for corrective action. This represents a 23% improvement over the previous period.
        
        **Location-specific Critical Stock Patterns:**
        
        * **Factories:** Minimal critical stock incidents (2% of total)
        * **Warehouses:** Moderate critical stock incidents (36% of total)
        * **Stores:** Highest critical stock incidents (62% of total)
        
        Store #4 (Mumbai) and Store #2 (Delhi) accounted for 43% of all critical stock situations, suggesting focused improvement efforts should target these locations.
        
        **Seasonal Factors:**
        
        Critical stock incidents showed a 28% increase during the first week of the month, correlating with salary cycles and increased consumer spending. This pattern suggests an opportunity for more dynamic safety stock levels based on calendar effects.
        """
    
    # Value Fluctuations Analysis
    if "Value Fluctuations" in focus_areas:
        analysis["Value Fluctuations"] = """
        ### Inventory Value Fluctuation Analysis
        
        Total inventory value across all locations fluctuated between ₹3.2 Cr and ₹3.8 Cr during the analysis period, with several notable patterns:
        
        **Value Distribution by Location Type:**
        
        * **Factories:** 32% of total inventory value (₹1.12 Cr average)
          - Primarily raw materials and work-in-progress
          - Relatively stable value (±5% fluctuation)
        
        * **Warehouses:** 48% of total inventory value (₹1.68 Cr average)
          - Highest overall value concentration
          - Moderate fluctuation (±12%)
          - Excess value reduced by 12% from period start to end
        
        * **Stores:** 20% of total inventory value (₹0.70 Cr average)
          - Highest value per square foot (₹4,200/sq.ft)
          - Most volatile value fluctuation (±18%)
        
        **Value Tied to Stock Health Categories:**
        
        * **Critical Stock:** 4% of inventory value (high risk to sales)
        * **Low Stock:** 15% of inventory value (moderate risk)
        * **Optimal Stock:** 62% of inventory value (target zone)
        * **Excess Stock:** 19% of inventory value (capital efficiency opportunity)
        
        The reduction in excess stock value from 31% to 19% during this period represents the most significant improvement in capital efficiency, freeing up approximately ₹32L in working capital.
        
        **Value Movement Patterns:**
        
        Inventory value tended to build up at month-end in Warehouses (+14% above average), likely due to pre-positioning for beginning-of-month demand spikes. This pattern creates a working capital opportunity through more gradual inventory building strategies.
        
        **Product Category Value Analysis:**
        
        * **Highest Value Categories:** Premium denim jeans (34% of total value)
        * **Fastest-Growing Value Categories:** Denim shirts (+18% value growth)
        * **Declining Value Categories:** Basic t-shirts (-12% value reduction)
        
        The shift toward higher-value product categories indicates a potential inventory mix optimization opportunity for improved gross margin performance.
        """
    
    # Location Comparisons Analysis
    if "Location Comparisons" in focus_areas:
        analysis["Location Comparisons"] = """
        ### Location Comparison Analysis
        
        Significant performance variations were observed across different locations within each type:
        
        **Factory Locations:**
        
        * **Factory Tirupur:** Highest efficiency (inventory turnover 4.8x)
          - Lowest days-on-hand for raw materials (18 days vs. 26 day average)
          - Best record accuracy (99.2%)
          - Lowest critical stock incidents (1)
        
        * **Factory Delhi:** Medium efficiency (inventory turnover 4.0x)
          - Average performance across most metrics
          - Highest improvement trajectory (+12% in material flow efficiency)
        
        * **Factory Mumbai:** Lowest efficiency (inventory turnover 3.7x)
          - Highest raw material holding (32 days vs. 26 day average)
          - Most movement transaction errors (3.8%)
          - Opportunity for process standardization
        
        **Warehouse Locations:**
        
        * **Central Warehouse:** Best overall performance
          - Highest throughput (43% of all movements)
          - Lowest excess inventory (8% vs. 19% average)
          - Most efficient space utilization (92% of capacity)
        
        * **North Warehouse:** Poorest performance
          - Highest excess inventory (32% vs. 19% average)
          - Longest dwell time for items (42 days vs. 28 day average)
          - Clear opportunity for inventory rationalization
        
        **Store Locations:**
        
        * **Store Bangalore:** Best performer
          - Highest sales:inventory ratio (6.2x)
          - Lowest stockout rate (0.8%)
          - Most efficient replenishment cycle (98% on-time)
        
        * **Store Chennai:** Poorest performer
          - Lowest sales:inventory ratio (3.8x)
          - Highest excess inventory (28%)
          - Most stockouts (7 incidents)
          - Priority location for improvement
        
        **Cross-location performance correlation:**
        
        A clear correlation was observed between the frequency of automated inventory data updates and overall location performance. Locations with real-time or hourly data updates outperformed those with daily or weekly updates by an average of 18% across all KPIs.
        
        This finding strongly supports the value of the new multi-location push system implementation, projecting an estimated ₹48L in working capital efficiency if all locations implement real-time data synchronization.
        """
    
    # Add other focus areas as needed
    if "Seasonal Trends" in focus_areas:
        analysis["Seasonal Trends"] = "Seasonal trend analysis content here..."
    
    if "Top Performers" in focus_areas:
        analysis["Top Performers"] = "Top performers analysis content here..."
    
    if "Sluggish Items" in focus_areas:
        analysis["Sluggish Items"] = "Sluggish items analysis content here..."
    
    if "Supply Chain Bottlenecks" in focus_areas:
        analysis["Supply Chain Bottlenecks"] = "Supply chain bottlenecks analysis content here..."
    
    return analysis

def generate_recommendations(start_date, end_date, focus_areas, location_types):
    """Generate actionable recommendations based on the analysis"""
    
    # Create recommendations organized by category
    recommendations = {
        "Inventory Optimization": [
            {
                "title": "Reduce Excess Stock at North Warehouse",
                "description": "Implement a targeted reduction strategy for the North Warehouse, which currently holds 32% excess inventory (vs. 19% average). Transfer slow-moving items to locations with higher demand or consider clearance strategies for aged inventory.",
                "priority": "High",
                "impact": "Potential to free up ₹18L in working capital"
            },
            {
                "title": "Rebalance Store Inventory in Chennai",
                "description": "Store Chennai shows the lowest sales:inventory ratio (3.8x) and highest excess inventory (28%). Conduct a full inventory review and transfer excess stock to better-performing locations.",
                "priority": "Medium",
                "impact": "Could improve location turnover by up to 35%"
            },
            {
                "title": "Adjust Safety Stock Levels for First Week of Month",
                "description": "Analysis shows 28% higher demand in the first week of each month. Increase safety stock calculation temporarily for this period to prevent the pattern of critical stock situations.",
                "priority": "Medium",
                "impact": "Potential to prevent ₹8L in lost sales per month"
            }
        ],
        "Process Improvement": [
            {
                "title": "Standardize Factory Mumbai Inventory Processes",
                "description": "Factory Mumbai shows the highest movement transaction error rate (3.8%) and longest raw material holding time. Implement the standardized processes from Factory Tirupur, which demonstrates best practices.",
                "priority": "High",
                "impact": "Could reduce working capital requirement by ₹12L"
            },
            {
                "title": "Eliminate Split Warehousing Shipments",
                "description": "Analysis identified inefficient split shipments between warehouses. Consolidate orders below ₹50,000 value to eliminate multiple small-volume transfers.",
                "priority": "Low",
                "impact": "Estimated ₹2.4L annual logistics savings"
            },
            {
                "title": "Align Movement Schedule with Staffing",
                "description": "Movement data shows clear weekly patterns with Monday-Tuesday being highest for Factory→Warehouse transfers. Align staffing and transportation schedules with these patterns.",
                "priority": "Medium",
                "impact": "Potential 15% improvement in labor efficiency"
            }
        ],
        "Technology Utilization": [
            {
                "title": "Accelerate Real-time Push Adoption",
                "description": "Locations with real-time or hourly data updates outperformed those with daily or weekly updates by 18%. Prioritize upgrading all critical locations to real-time or hourly data synchronization.",
                "priority": "High",
                "impact": "Projected ₹48L improvement in working capital efficiency"
            },
            {
                "title": "Implement RFID Tracking at Store Locations",
                "description": "Store locations show the highest inventory record discrepancies (3.2%). Pilot RFID tracking at the two locations with highest discrepancies to improve accuracy.",
                "priority": "Medium",
                "impact": "Could reduce inventory record errors by 80%"
            },
            {
                "title": "Enable Auto-replenishment for Top 20% of SKUs",
                "description": "Configure the system to automatically generate replenishment orders for the top 20% of SKUs by volume, based on actual consumption data rather than manual ordering.",
                "priority": "Medium",
                "impact": "Potential to reduce stockouts by 45%"
            }
        ]
    }
    
    return recommendations

def generate_predictions(start_date, end_date, focus_areas, location_types):
    """Generate predictions based on the observed data patterns"""
    
    # Create a list of predictions
    predictions = [
        {
            "title": "Inventory Value Projection",
            "description": "Based on current patterns, total inventory value is projected to decrease by 7-9% over the next quarter while maintaining or improving service levels. This will be driven primarily by continued reduction of excess stock in warehouses (-15%) and improved turnover at store locations (+8%).",
            "confidence": "High",
            "timeframe": "Next 90 days",
            "visual": "trend_forecast"
        },
        {
            "title": "Critical Stock Risk Assessment",
            "description": "Without adjusting safety stock levels for seasonal patterns, we project 7-9 critical stock situations in the coming month, particularly affecting high-velocity items during the first week of the month, potentially resulting in ₹15-18L in lost sales.",
            "confidence": "Medium",
            "timeframe": "Next 30 days",
            "visual": "stock_projection"
        },
        {
            "title": "Working Capital Opportunity",
            "description": "Full implementation of real-time inventory push across all locations is projected to release ₹45-55L in working capital over the next 120 days through improved inventory deployment and reduced safety stock requirements.",
            "confidence": "High",
            "timeframe": "Next 120 days"
        },
        {
            "title": "Turnover Rate Forecast",
            "description": "Overall inventory turnover is projected to increase from the current 4.2x to 4.8-5.0x annually within six months if recommended actions are implemented, placing the operation in the top quartile of industry performance.",
            "confidence": "Medium",
            "timeframe": "Next 180 days"
        },
        {
            "title": "Location Performance Convergence",
            "description": "The performance gap between best and worst performing locations is expected to narrow by 40-50% as standardized processes and real-time data availability drive improvement at underperforming locations.",
            "confidence": "Medium",
            "timeframe": "Next 90-120 days"
        }
    ]
    
    return predictions

# Chart functions for different visualizations

def show_inventory_turnover_chart():
    """Display inventory turnover visualization"""
    # Sample data for turnover by location
    locations = ["Factory Tirupur", "Factory Delhi", "Factory Mumbai", 
                 "Central Warehouse", "North Warehouse", "South Warehouse",
                 "Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai"]
    current_turnover = [4.8, 4.0, 3.7, 5.1, 2.9, 3.5, 6.2, 5.8, 5.5, 3.8]
    previous_turnover = [4.6, 3.8, 3.6, 4.8, 2.7, 3.4, 5.9, 5.4, 5.1, 3.6]
    
    # Create the figure
    fig = go.Figure()
    
    # Add current period bar
    fig.add_trace(go.Bar(
        x=locations,
        y=current_turnover,
        name='Current Period',
        marker_color='rgb(26, 118, 255)'
    ))
    
    # Add previous period bar
    fig.add_trace(go.Bar(
        x=locations,
        y=previous_turnover,
        name='Previous Period',
        marker_color='rgba(58, 71, 80, 0.6)'
    ))
    
    # Update layout
    fig.update_layout(
        title='Inventory Turnover by Location',
        xaxis_tickangle=-45,
        barmode='group',
        xaxis_title='Location',
        yaxis_title='Turnover Rate (x per year)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_stock_movement_chart():
    """Display stock movement visualization"""
    # Sample data for movement types
    movement_types = ["Factory → Warehouse", "Warehouse → Store", "Factory → Store", 
                      "Store → Warehouse", "Warehouse → Factory", "Store → Store"]
    current_counts = [112, 86, 24, 18, 8, 5]
    previous_counts = [98, 76, 18, 21, 10, 4]
    
    # Percent changes
    percent_changes = [(curr - prev) / prev * 100 for curr, prev in zip(current_counts, previous_counts)]
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add bars for current period
    fig.add_trace(go.Bar(
        x=movement_types,
        y=current_counts,
        name='Current Period',
        marker_color='rgb(26, 118, 255)'
    ))
    
    # Add bars for previous period
    fig.add_trace(go.Bar(
        x=movement_types,
        y=previous_counts,
        name='Previous Period',
        marker_color='rgba(58, 71, 80, 0.6)'
    ))
    
    # Add line for percent change
    fig.add_trace(go.Scatter(
        x=movement_types,
        y=percent_changes,
        mode='lines+markers',
        name='% Change',
        yaxis='y2',
        line=dict(color='rgb(255, 127, 14)', width=3),
        marker=dict(size=8)
    ))
    
    # Update layout with secondary y-axis
    fig.update_layout(
        title='Stock Movement Transactions by Type',
        xaxis_tickangle=-45,
        barmode='group',
        xaxis_title='Movement Type',
        yaxis=dict(
            title='Number of Movements',
            titlefont=dict(color='rgb(26, 118, 255)'),
            tickfont=dict(color='rgb(26, 118, 255)')
        ),
        yaxis2=dict(
            title='Percent Change (%)',
            titlefont=dict(color='rgb(255, 127, 14)'),
            tickfont=dict(color='rgb(255, 127, 14)'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            y=1.15,
            x=0.5,
            xanchor='center',
            orientation='h'
        ),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_critical_stock_chart():
    """Display critical stock patterns visualization"""
    # Sample data for critical stock incidents by cause and location
    causes = ["Demand Spike", "Supply Delay", "Record Discrepancy"]
    factory_incidents = [1, 2, 0]
    warehouse_incidents = [8, 4, 1]
    store_incidents = [15, 3, 3]
    
    # Create the figure
    fig = go.Figure()
    
    # Add traces for each location type
    fig.add_trace(go.Bar(
        x=causes,
        y=factory_incidents,
        name='Factory',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.add_trace(go.Bar(
        x=causes,
        y=warehouse_incidents,
        name='Warehouse',
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.add_trace(go.Bar(
        x=causes,
        y=store_incidents,
        name='Store',
        marker_color='rgb(15, 171, 255)'
    ))
    
    # Update layout
    fig.update_layout(
        title='Critical Stock Incidents by Cause and Location Type',
        xaxis_title='Cause of Critical Stock',
        yaxis_title='Number of Incidents',
        barmode='stack',
        legend=dict(
            y=0.9,
            x=0.9
        ),
        annotations=[
            dict(
                x=1.15,
                y=0.5,
                showarrow=False,
                text="Total: 37 incidents",
                xref="paper",
                yref="paper",
                font=dict(size=14)
            )
        ],
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_value_fluctuation_chart():
    """Display inventory value fluctuation visualization"""
    # Sample data for inventory value over time by location type
    dates = pd.date_range(start='2025-03-01', end='2025-03-31', freq='D')
    
    # Generate some sample value data with fluctuations
    np.random.seed(42)
    factory_values = 112000000 + np.random.normal(0, 3000000, len(dates)) + np.sin(np.arange(len(dates))/5) * 2000000
    warehouse_values = 168000000 + np.random.normal(0, 6000000, len(dates)) + np.sin(np.arange(len(dates))/4) * 5000000
    store_values = 70000000 + np.random.normal(0, 4000000, len(dates)) + np.sin(np.arange(len(dates))/3) * 3000000
    
    # Create the figure
    fig = go.Figure()
    
    # Add traces for each location type
    fig.add_trace(go.Scatter(
        x=dates,
        y=factory_values,
        name='Factory',
        line=dict(color='rgb(55, 83, 109)', width=2),
        stackgroup='one'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=warehouse_values,
        name='Warehouse',
        line=dict(color='rgb(26, 118, 255)', width=2),
        stackgroup='one'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=store_values,
        name='Store',
        line=dict(color='rgb(15, 171, 255)', width=2),
        stackgroup='one'
    ))
    
    # Update layout
    fig.update_layout(
        title='Inventory Value Fluctuation by Location Type',
        xaxis_title='Date',
        yaxis_title='Inventory Value (₹)',
        yaxis=dict(
            tickformat='.2s',
            hoverformat='.2s'
        ),
        hovermode='x unified',
        legend=dict(
            y=0.9,
            x=0.1
        ),
        height=500
    )
    
    # Add annotations for significant events
    fig.add_annotation(
        x=dates[7],
        y=sum([factory_values[7], warehouse_values[7], store_values[7]]) + 10000000,
        text="Bulk shipment received",
        showarrow=True,
        arrowhead=1
    )
    
    fig.add_annotation(
        x=dates[15],
        y=sum([factory_values[15], warehouse_values[15], store_values[15]]) + 10000000,
        text="Month mid-point<br>stock correction",
        showarrow=True,
        arrowhead=1
    )
    
    fig.add_annotation(
        x=dates[22],
        y=sum([factory_values[22], warehouse_values[22], store_values[22]]) + 10000000,
        text="Store promotion<br>depletion",
        showarrow=True,
        arrowhead=1
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_location_comparison_chart():
    """Display location comparison visualization"""
    # Sample data for location comparison on multiple metrics
    locations = ["Factory Tirupur", "Factory Delhi", "Factory Mumbai", 
                 "Central Warehouse", "North Warehouse", "Store Bangalore", "Store Chennai"]
    
    # Metrics for each location (scaled 0-100)
    turnover_score = [90, 75, 65, 85, 40, 95, 45]
    accuracy_score = [95, 80, 70, 90, 75, 85, 65]
    days_on_hand = [75, 65, 55, 70, 30, 85, 40]  # Inverted: higher is better (fewer days)
    space_util = [80, 75, 70, 92, 65, 80, 60]
    stockout_prev = [85, 80, 75, 90, 65, 95, 50]  # Higher is better prevention
    
    # Create radar chart
    categories = ['Turnover', 'Accuracy', 'Days on Hand', 'Space Utilization', 'Stockout Prevention']
    
    fig = go.Figure()
    
    # Add a trace for each location
    colors = px.colors.qualitative.Plotly
    for i, location in enumerate(locations):
        fig.add_trace(go.Scatterpolar(
            r=[turnover_score[i], accuracy_score[i], days_on_hand[i], space_util[i], stockout_prev[i]],
            theta=categories,
            fill='toself',
            name=location,
            line_color=colors[i % len(colors)]
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Location Performance Comparison",
        showlegend=True,
        legend=dict(
            y=0.5,
            x=1.1
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_inventory_flow_sankey():
    """Display inventory flow using Sankey diagram"""
    # Sample data for Sankey diagram
    nodes = ["Factory Tirupur", "Factory Delhi", "Factory Mumbai", 
             "Central Warehouse", "North Warehouse", "South Warehouse",
             "Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai"]
    
    # Source, target, value for flows
    sources = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 7]
    targets = [3, 4, 5, 3, 4, 5, 3, 5, 6, 7, 8, 9, 7, 8, 6, 9, 3, 4]
    values = [50, 20, 15, 30, 25, 20, 35, 15, 30, 25, 20, 15, 15, 10, 10, 15, 5, 8]
    
    # Colors based on flow type
    colors = []
    for s, t in zip(sources, targets):
        if s < 3 and t >= 3 and t <= 5:  # Factory to Warehouse
            colors.append("rgba(31, 119, 180, 0.8)")
        elif s >= 3 and s <= 5 and t >= 6:  # Warehouse to Store
            colors.append("rgba(255, 127, 14, 0.8)")
        elif s < 3 and t >= 6:  # Factory to Store
            colors.append("rgba(44, 160, 44, 0.8)")
        elif s >= 6 and t >= 3 and t <= 5:  # Store to Warehouse
            colors.append("rgba(214, 39, 40, 0.8)")
        else:  # Other flows
            colors.append("rgba(148, 103, 189, 0.8)")
    
    # Create the figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="rgba(150, 150, 150, 0.8)"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors
        )
    )])
    
    # Update layout
    fig.update_layout(
        title="Inventory Flow Between Locations",
        font=dict(size=12),
        height=700
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_stock_health_by_location():
    """Display stock health by location"""
    # Sample data for stock health by location
    locations = ["Factory Tirupur", "Factory Delhi", "Factory Mumbai", 
                 "Central Warehouse", "North Warehouse", "South Warehouse",
                 "Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai"]
    
    # Health percentages for each location [critical, low, optimal, excess]
    health_data = [
        [2, 8, 75, 15],  # Factory Tirupur
        [3, 12, 70, 15],  # Factory Delhi
        [5, 15, 65, 15],  # Factory Mumbai
        [4, 10, 78, 8],  # Central Warehouse
        [6, 16, 46, 32],  # North Warehouse
        [5, 12, 65, 18],  # South Warehouse
        [2, 8, 82, 8],  # Store Bangalore
        [3, 10, 77, 10],  # Store Delhi
        [4, 12, 74, 10],  # Store Mumbai
        [8, 16, 48, 28]   # Store Chennai
    ]
    
    # Create the figure
    fig = go.Figure()
    
    # Add bars for each health status
    fig.add_trace(go.Bar(
        x=locations,
        y=[data[0] for data in health_data],
        name='Critical',
        marker_color='rgb(255, 75, 75)'
    ))
    
    fig.add_trace(go.Bar(
        x=locations,
        y=[data[1] for data in health_data],
        name='Low',
        marker_color='rgb(255, 165, 0)'
    ))
    
    fig.add_trace(go.Bar(
        x=locations,
        y=[data[2] for data in health_data],
        name='Optimal',
        marker_color='rgb(0, 204, 150)'
    ))
    
    fig.add_trace(go.Bar(
        x=locations,
        y=[data[3] for data in health_data],
        name='Excess',
        marker_color='rgb(99, 110, 250)'
    ))
    
    # Update layout
    fig.update_layout(
        title='Stock Health Distribution by Location',
        xaxis_tickangle=-45,
        xaxis_title='Location',
        yaxis_title='Percentage of SKUs',
        barmode='stack',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_time_series_analysis():
    """Display time series analysis of key metrics"""
    # Sample data for time series
    dates = pd.date_range(start='2025-03-01', end='2025-03-31', freq='D')
    
    # Generate sample data for key metrics
    np.random.seed(42)
    turnover = 4.0 + np.cumsum(np.random.normal(0, 0.03, len(dates))) / 100 + 0.2 * (1 - np.exp(-np.arange(len(dates))/20))
    days_inventory = 33 - np.cumsum(np.random.normal(0, 0.05, len(dates))) / 15 - 0.1 * (1 - np.exp(-np.arange(len(dates))/20))
    stockouts = np.random.poisson(0.8, len(dates))
    stockouts_cumulative = np.cumsum(stockouts)
    critical_incidents = np.random.poisson(0.4, len(dates))
    critical_incidents_cumulative = np.cumsum(critical_incidents)
    
    # Create the figure with multiple y-axes
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Inventory Performance Metrics", "Incident Tracking"),
                        vertical_spacing=0.1,
                        row_heights=[0.7, 0.3])
    
    # Add traces for inventory metrics
    fig.add_trace(
        go.Scatter(x=dates, y=turnover, name='Inventory Turnover', mode='lines', line=dict(color='blue')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=dates, y=days_inventory, name='Days in Inventory', mode='lines', line=dict(color='red'), yaxis='y2'),
        row=1, col=1
    )
    
    # Add traces for incidents
    fig.add_trace(
        go.Bar(x=dates, y=stockouts, name='Daily Stockouts', marker_color='orange'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(x=dates, y=critical_incidents, name='Critical Incidents', marker_color='red'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=dates, y=stockouts_cumulative, name='Cumulative Stockouts', 
                   mode='lines', line=dict(color='orange', dash='dot'), yaxis='y4'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=dates, y=critical_incidents_cumulative, name='Cumulative Critical', 
                   mode='lines', line=dict(color='red', dash='dot'), yaxis='y4'),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        title='Time Series Analysis of Inventory Performance',
        xaxis_title='Date',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Inventory Turnover", row=1, col=1)
    fig.update_yaxes(title_text="Days in Inventory", row=1, col=1, overlaying='y', side='right')
    fig.update_yaxes(title_text="Daily Incidents", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative Incidents", row=2, col=1, overlaying='y3', side='right')
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    
    # Use st.plotly_chart to display the figure
    st.plotly_chart(fig, use_container_width=True)

def show_value_distribution():
    """Display value distribution across different dimensions"""
    # Sample data for value distribution
    categories = ["Denim Jeans", "Denim Shirts", "Denim Jackets", "T-shirts", "Accessories"]
    factory_values = [38, 21, 15, 12, 14]
    warehouse_values = [32, 20, 18, 14, 16]
    store_values = [30, 20, 22, 15, 13]
    
    # Create sunburst chart for hierarchical value distribution
    location_types = ["Factory", "Warehouse", "Store"]
    
    # Prepare data for sunburst
    labels = ["All Inventory"] + location_types + categories * 3
    parents = [""] + ["All Inventory"] * 3 + ["Factory"] * 5 + ["Warehouse"] * 5 + ["Store"] * 5
    values = [100] + [32, 48, 20] + factory_values + warehouse_values + store_values
    
    # Create colors
    colors = ['lightgray'] + ['rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)'] + \
             ['#1f77b4'] * 5 + ['#ff7f0e'] * 5 + ['#2ca02c'] * 5
    
    # Create sunburst figure
    fig1 = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>Value: %{value}%<br>of parent: %{parent}<extra></extra>',
        maxdepth=2
    ))
    
    fig1.update_layout(
        title="Inventory Value Distribution by Location and Category",
        margin=dict(t=60, l=0, r=0, b=0),
        height=600
    )
    
    # Create treemap for alternative view
    fig2 = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>Value: %{value}%<br>of parent: %{parent}<extra></extra>',
        maxdepth=2
    ))
    
    fig2.update_layout(
        title="Inventory Value Distribution (Treemap View)",
        margin=dict(t=60, l=0, r=0, b=0),
        height=600
    )
    
    # Create tabs for different visualizations
    view_tabs = st.tabs(["Sunburst View", "Treemap View"])
    
    with view_tabs[0]:
        st.plotly_chart(fig1, use_container_width=True)
    
    with view_tabs[1]:
        st.plotly_chart(fig2, use_container_width=True)

def show_movement_patterns():
    """Display movement patterns analysis"""
    # Sample data for movement patterns
    dates = pd.date_range(start='2025-03-01', end='2025-03-31', freq='D')
    days = [date.strftime('%a') for date in dates]
    
    # Movement counts by day of week
    day_counts = {}
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        day_counts[day] = days.count(day)
    
    # Generate movement data by day and type
    factory_warehouse = [8 if day in ['Mon', 'Tue'] else 4 if day in ['Wed'] else 2 for day in days]
    warehouse_store = [3 if day in ['Mon', 'Tue'] else 6 if day in ['Thu', 'Fri'] else 1 for day in days]
    factory_store = [1 if day in ['Wed', 'Thu'] else 0 for day in days]
    returns = [0 if day in ['Sat', 'Sun'] else np.random.randint(0, 3) for day in days]
    
    # Create heatmap data
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    movement_types = ['Factory → Warehouse', 'Warehouse → Store', 'Factory → Store', 'Returns']
    
    heatmap_data = np.zeros((len(movement_types), len(day_names)))
    
    for i, day in enumerate(days):
        if day == 'Mon':
            heatmap_data[0, 0] += factory_warehouse[i]
            heatmap_data[1, 0] += warehouse_store[i]
            heatmap_data[2, 0] += factory_store[i]
            heatmap_data[3, 0] += returns[i]
        elif day == 'Tue':
            heatmap_data[0, 1] += factory_warehouse[i]
            heatmap_data[1, 1] += warehouse_store[i]
            heatmap_data[2, 1] += factory_store[i]
            heatmap_data[3, 1] += returns[i]
        elif day == 'Wed':
            heatmap_data[0, 2] += factory_warehouse[i]
            heatmap_data[1, 2] += warehouse_store[i]
            heatmap_data[2, 2] += factory_store[i]
            heatmap_data[3, 2] += returns[i]
        elif day == 'Thu':
            heatmap_data[0, 3] += factory_warehouse[i]
            heatmap_data[1, 3] += warehouse_store[i]
            heatmap_data[2, 3] += factory_store[i]
            heatmap_data[3, 3] += returns[i]
        elif day == 'Fri':
            heatmap_data[0, 4] += factory_warehouse[i]
            heatmap_data[1, 4] += warehouse_store[i]
            heatmap_data[2, 4] += factory_store[i]
            heatmap_data[3, 4] += returns[i]
        elif day == 'Sat':
            heatmap_data[0, 5] += factory_warehouse[i]
            heatmap_data[1, 5] += warehouse_store[i]
            heatmap_data[2, 5] += factory_store[i]
            heatmap_data[3, 5] += returns[i]
        elif day == 'Sun':
            heatmap_data[0, 6] += factory_warehouse[i]
            heatmap_data[1, 6] += warehouse_store[i]
            heatmap_data[2, 6] += factory_store[i]
            heatmap_data[3, 6] += returns[i]
    
    # Create heatmap figure
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=day_names,
        y=movement_types,
        colorscale='YlOrRd',
        hovertemplate='Day: %{x}<br>Movement: %{y}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Movement Patterns by Day of Week',
        xaxis_title='Day of Week',
        yaxis_title='Movement Type',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Movement patterns over the month
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=dates, y=factory_warehouse, 
        name='Factory → Warehouse',
        line=dict(color='blue', width=2)
    ))
    
    fig2.add_trace(go.Scatter(
        x=dates, y=warehouse_store, 
        name='Warehouse → Store',
        line=dict(color='orange', width=2)
    ))
    
    fig2.add_trace(go.Scatter(
        x=dates, y=factory_store, 
        name='Factory → Store',
        line=dict(color='green', width=2)
    ))
    
    fig2.add_trace(go.Scatter(
        x=dates, y=returns, 
        name='Returns',
        line=dict(color='red', width=2)
    ))
    
    fig2.update_layout(
        title='Movement Patterns Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Movements',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)

def show_comparison_matrix():
    """Display comparison matrix for locations"""
    # Sample data for comparison matrix
    locations = ["Factory Tirupur", "Factory Delhi", "Factory Mumbai", 
                "Central Warehouse", "North Warehouse", "South Warehouse",
                "Store Bangalore", "Store Delhi", "Store Mumbai", "Store Chennai"]
    
    # Generate sample performance scores (0-100)
    np.random.seed(42)
    inventory_turnover = [90, 75, 65, 85, 40, 75, 95, 85, 80, 45]
    days_on_hand = [85, 70, 60, 80, 35, 70, 90, 80, 75, 50]  # Higher is better (fewer days)
    record_accuracy = [95, 85, 70, 90, 75, 85, 85, 80, 80, 70]
    space_utilization = [85, 80, 75, 92, 65, 80, 85, 80, 75, 65]
    stockout_prevention = [90, 85, 75, 90, 70, 80, 95, 85, 80, 60]
    excess_reduction = [80, 75, 70, 95, 40, 75, 90, 85, 80, 45]
    
    # Calculate overall score
    overall = [(a + b + c + d + e + f) / 6 for a, b, c, d, e, f in 
              zip(inventory_turnover, days_on_hand, record_accuracy, space_utilization, stockout_prevention, excess_reduction)]
    
    # Create dataframe
    df = pd.DataFrame({
        'Location': locations,
        'Inventory Turnover': inventory_turnover,
        'Days on Hand': days_on_hand,
        'Record Accuracy': record_accuracy,
        'Space Utilization': space_utilization,
        'Stockout Prevention': stockout_prevention,
        'Excess Reduction': excess_reduction,
        'Overall Score': overall
    })
    
    # Sort by overall score
    df = df.sort_values('Overall Score', ascending=False)
    
    # Create parallel coordinates plot
    dimensions = [
        dict(range=[0, 100], label='Inventory Turnover', values=df['Inventory Turnover']),
        dict(range=[0, 100], label='Days on Hand', values=df['Days on Hand']),
        dict(range=[0, 100], label='Record Accuracy', values=df['Record Accuracy']),
        dict(range=[0, 100], label='Space Utilization', values=df['Space Utilization']),
        dict(range=[0, 100], label='Stockout Prevention', values=df['Stockout Prevention']),
        dict(range=[0, 100], label='Excess Reduction', values=df['Excess Reduction']),
        dict(range=[0, 100], label='Overall Score', values=df['Overall Score'])
    ]
    
    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=df['Overall Score'],
            colorscale='Viridis',
            showscale=True,
            cmin=0,
            cmax=100
        ),
        dimensions=dimensions,
        labelangle=30,
        labelside='bottom'
    ))
    
    fig.update_layout(
        title='Location Performance Comparison Matrix',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show the table with conditional formatting
    st.subheader("Location Performance Scores")
    
    # Function to color code cells
    def color_scale(val):
        """Color scale for the dataframe"""
        if val >= 90:
            color = 'background-color: #00CC96; color: white'  # Excellent
        elif val >= 75:
            color = 'background-color: #39A9DB; color: white'  # Good
        elif val >= 60:
            color = 'background-color: #FFA15A; color: white'  # Average
        else:
            color = 'background-color: #FF6692; color: white'  # Poor
        return color
    
    # Apply styling and display
    df_display = df.copy()
    display_cols = ['Location', 'Inventory Turnover', 'Days on Hand', 'Record Accuracy', 
                    'Space Utilization', 'Stockout Prevention', 'Excess Reduction', 'Overall Score']
    
    # Format the dataframe
    df_styled = df_display[display_cols].style.applymap(
        color_scale, 
        subset=display_cols[1:]  # Apply to all columns except Location
    )
    
    st.dataframe(df_styled, use_container_width=True)

def show_trend_forecast_chart():
    """Display trend forecast visualization"""
    # Sample data for trend forecast
    dates = pd.date_range(start='2025-03-01', end='2025-06-30', freq='D')
    split_date = datetime.date(2025, 3, 31)
    
    # Historical inventory value
    np.random.seed(42)
    historical_value = []
    for i in range(len(dates)):
        if dates[i].date() <= split_date:
            # Actual data with some random fluctuation
            base = 350000000 - i * 300000  # Slight downward trend
            fluctuation = np.random.normal(0, 5000000)
            weekly = 10000000 * np.sin(i * 2 * np.pi / 7)  # Weekly cycle
            historical_value.append(base + fluctuation + weekly)
        else:
            # After the split date, set to NaN for historical
            historical_value.append(np.nan)
    
    # Forecast inventory value
    forecast_value = []
    forecast_upper = []
    forecast_lower = []
    
    for i in range(len(dates)):
        if dates[i].date() <= split_date:
            # Before the split date, set to NaN for forecast
            forecast_value.append(np.nan)
            forecast_upper.append(np.nan)
            forecast_lower.append(np.nan)
        else:
            # Forecast with decreasing trend and increasing uncertainty
            days_in_future = (dates[i].date() - split_date).days
            base = 330000000 - days_in_future * 300000  # Continuing downward trend
            weekly = 8000000 * np.sin(i * 2 * np.pi / 7)  # Weekly cycle with less amplitude
            forecast_value.append(base + weekly)
            
            # Uncertainty bands
            uncertainty = 5000000 + days_in_future * 100000  # Increasing uncertainty over time
            forecast_upper.append(base + weekly + uncertainty)
            forecast_lower.append(base + weekly - uncertainty)
    
    # Create the figure
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=dates, 
        y=historical_value,
        name='Historical Value',
        line=dict(color='blue', width=2)
    ))
    
    # Add forecast
    fig.add_trace(go.Scatter(
        x=dates,
        y=forecast_value,
        name='Forecast Value',
        line=dict(color='red', width=2, dash='dot')
    ))
    
    # Add uncertainty bands
    fig.add_trace(go.Scatter(
        x=dates,
        y=forecast_upper,
        name='Upper 95% CI',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=forecast_lower,
        name='Lower 95% CI',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.1)',
        showlegend=False
    ))
    
    # Add vertical line at split date
    fig.add_vline(
        x=split_date, 
        line_dash="dash", 
        line_color="black",
        annotation_text="Forecast Start",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        title='Inventory Value Forecast',
        xaxis_title='Date',
        yaxis_title='Inventory Value (₹)',
        yaxis=dict(
            tickformat='.2s',
            hoverformat='.2s'
        ),
        hovermode='x unified',
        height=500
    )
    
    # Add annotations
    fig.add_annotation(
        x=dates[len(dates)//2 + 30],
        y=forecast_value[len(dates)//2 + 30] + 20000000,
        text="Projected 7-9% Reduction<br>in Inventory Value",
        showarrow=True,
        arrowhead=1
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_stock_projection_chart():
    """Display stock health projection visualization"""
    # Sample data for stock health projection
    dates = pd.date_range(start='2025-03-01', end='2025-04-30', freq='D')
    split_date = datetime.date(2025, 3, 31)
    
    # Historical stock health
    np.random.seed(43)
    
    # Generate historical data (as percentages)
    historical_critical = []
    historical_low = []
    historical_optimal = []
    historical_excess = []
    
    # Forecast data
    forecast_critical = []
    forecast_low = []
    forecast_optimal = []
    forecast_excess = []
    
    # Generate data with weekly patterns
    for i, date in enumerate(dates):
        is_historical = date.date() <= split_date
        
        # Base values with some weekly pattern
        day_of_week = date.weekday()  # 0 = Monday, 6 = Sunday
        
        # First week of month effect (higher critical, lower optimal)
        is_first_week = date.day <= 7
        first_week_factor = 1.5 if is_first_week else 1.0
        
        if is_historical:
            # Historical data
            base_critical = 6 + 2 * np.sin(day_of_week * np.pi / 3) * first_week_factor
            base_low = 12 + 3 * np.sin(day_of_week * np.pi / 3)
            base_excess = 19 - 2 * np.sin(day_of_week * np.pi / 6)
            
            # Add some random fluctuation
            critical = max(0, base_critical + np.random.normal(0, 1))
            low = max(0, base_low + np.random.normal(0, 1.5))
            excess = max(0, base_excess + np.random.normal(0, 2))
            
            # Optimal is the remainder
            optimal = max(0, 100 - critical - low - excess)
            
            historical_critical.append(critical)
            historical_low.append(low)
            historical_optimal.append(optimal)
            historical_excess.append(excess)
            
            # Set forecast values to NaN
            forecast_critical.append(np.nan)
            forecast_low.append(np.nan)
            forecast_optimal.append(np.nan)
            forecast_excess.append(np.nan)
        else:
            # Forecast data - continue the patterns but with increasing critical/low in first week
            future_days = (date.date() - split_date).days
            
            # Increase critical situations in first week of April if no adjustment made
            base_critical = (8 + 2 * np.sin(day_of_week * np.pi / 3)) * first_week_factor * 1.2
            base_low = (14 + 3 * np.sin(day_of_week * np.pi / 3)) * first_week_factor * 1.1
            base_excess = 17 - 2 * np.sin(day_of_week * np.pi / 6)
            
            critical = max(0, base_critical)
            low = max(0, base_low)
            excess = max(0, base_excess)
            
            # Optimal is the remainder
            optimal = max(0, 100 - critical - low - excess)
            
            # Set historical values to NaN
            historical_critical.append(np.nan)
            historical_low.append(np.nan)
            historical_optimal.append(np.nan)
            historical_excess.append(np.nan)
            
            forecast_critical.append(critical)
            forecast_low.append(low)
            forecast_optimal.append(optimal)
            forecast_excess.append(excess)
    
    # Create the figure
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=dates, y=historical_critical, stackgroup='historical',
        name='Historical Critical', line=dict(width=0.5), fillcolor='rgba(255, 75, 75, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=historical_low, stackgroup='historical',
        name='Historical Low', line=dict(width=0.5), fillcolor='rgba(255, 165, 0, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=historical_optimal, stackgroup='historical',
        name='Historical Optimal', line=dict(width=0.5), fillcolor='rgba(0, 204, 150, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=historical_excess, stackgroup='historical',
        name='Historical Excess', line=dict(width=0.5), fillcolor='rgba(99, 110, 250, 0.8)'
    ))
    
    # Forecast data
    fig.add_trace(go.Scatter(
        x=dates, y=forecast_critical, stackgroup='forecast',
        name='Forecast Critical', line=dict(width=0.5, dash='dot'), fillcolor='rgba(255, 75, 75, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=forecast_low, stackgroup='forecast',
        name='Forecast Low', line=dict(width=0.5, dash='dot'), fillcolor='rgba(255, 165, 0, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=forecast_optimal, stackgroup='forecast',
        name='Forecast Optimal', line=dict(width=0.5, dash='dot'), fillcolor='rgba(0, 204, 150, 0.8)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=forecast_excess, stackgroup='forecast',
        name='Forecast Excess', line=dict(width=0.5, dash='dot'), fillcolor='rgba(99, 110, 250, 0.8)'
    ))
    
    # Add vertical line at split date
    fig.add_vline(
        x=split_date, 
        line_dash="dash", 
        line_color="black",
        annotation_text="Forecast Start",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        title='Stock Health Projection',
        xaxis_title='Date',
        yaxis_title='Percentage of Inventory',
        hovermode='x unified',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    # Add annotation for first week of April
    first_week_april = datetime.date(2025, 4, 5)
    fig.add_annotation(
        x=first_week_april,
        y=90,
        text="Projected 7-9 critical stock situations<br>in first week of April",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Import required for the time series analysis visualization
from plotly.subplots import make_subplots