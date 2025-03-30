import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def show_retail_distribution():
    """Display the Voi Jeans Retail Distribution Dashboard"""
    
    st.title("Voi Jeans Retail Distribution")
    
    # Introduction section with key metrics
    st.markdown("""
    <div style="background-color: #2E2E2E; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h3 style="color: #1E88E5;">Retail Distribution Dashboard</h3>
    <p>Manage your retail distribution network and analyze sales performance across all Voi Jeans retail locations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different retail sections
    tabs = st.tabs(["Store Network", "Sales Performance", "E-Wards Loyalty", "Consumer Insights"])
    
    # Store Network tab
    with tabs[0]:
        show_store_network()
    
    # Sales Performance tab
    with tabs[1]:
        show_sales_performance()
    
    # E-Wards Loyalty Program tab
    with tabs[2]:
        show_loyalty_program()
    
    # Consumer Insights tab
    with tabs[3]:
        show_consumer_insights()

def show_store_network():
    """Show the store network visualization and management"""
    
    st.subheader("Voi Jeans Retail Store Network")
    
    # Store metrics overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Stores", value="20")
    with col2:
        st.metric(label="Active Stores", value="18", delta="2 in setup")
    with col3:
        st.metric(label="Top Performing", value="Delhi-NCR")
    with col4:
        st.metric(label="Avg Monthly Sales", value="₹24.5L")
    
    # Store network map placeholder (using a table for now)
    st.markdown("### Store Locations")
    
    # Sample store data
    store_data = {
        "Store ID": ["VOI001", "VOI002", "VOI003", "VOI004", "VOI005"],
        "Location": ["Delhi - Sarojini", "Mumbai Hub", "Bangalore Central", "Chennai T. Nagar", "Delhi - Select Citywalk"],
        "Size (sq ft)": [1200, 1500, 1000, 1100, 2000],
        "Monthly Sales (₹)": ["32.5L", "28.7L", "22.1L", "18.5L", "36.2L"],
        "Status": ["Active", "Active", "Active", "Active", "Active"]
    }
    
    df_stores = pd.DataFrame(store_data)
    st.dataframe(df_stores, use_container_width=True)
    
    # Store fixture management
    st.markdown("### Store Fixture Management")
    st.markdown("Manage your store fixtures and product placement across all locations.")
    
    fixture_types = ["Wall Units", "Center Tables", "Hanging Rails", "Mannequins", "Window Displays"]
    fixture_counts = [120, 85, 210, 60, 20]
    
    # Create a horizontal bar chart for fixtures
    fig = px.bar(
        x=fixture_counts, 
        y=fixture_types, 
        orientation='h',
        color=fixture_counts,
        color_continuous_scale='Blues',
        title="Fixture Distribution Across Stores"
    )
    
    fig.update_layout(
        xaxis_title="Number of Units",
        yaxis_title="",
        height=350,
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Store Operations Form
    st.markdown("### Store Operations")
    with st.expander("Store Operations Management", expanded=False):
        # Two columns for the form
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Select Store", df_stores["Location"], index=0)
            st.date_input("Select Date", datetime.now())
            st.selectbox("Operation Type", ["Inventory Update", "Visual Merchandising", "Staff Allocation", "Promotion Setup"])
        
        with col2:
            st.text_area("Operation Details", height=100)
            st.file_uploader("Upload Related Documents", type=["pdf", "docx", "xlsx"])
            st.button("Schedule Operation", use_container_width=True)

def show_sales_performance():
    """Show the sales performance analysis"""
    
    st.subheader("Sales Performance Analytics")
    
    # Date range selector for analysis
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Metrics row for key performance indicators
    st.markdown("### Key Performance Metrics")
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric(label="Total Sales", value="₹3.24 Cr", delta="+8.2%")
    with metric_cols[1]:
        st.metric(label="Units Sold", value="12,450", delta="+12%")
    with metric_cols[2]:
        st.metric(label="Avg. Transaction", value="₹2,600", delta="-2.1%")
    with metric_cols[3]:
        st.metric(label="Conversion Rate", value="22%", delta="+1.5%")
    
    # Create a tab layout for different performance views
    perf_tabs = st.tabs(["Daily Performance", "Category Analysis", "Store Comparison"])
    
    # Daily Performance Tab
    with perf_tabs[0]:
        st.markdown("### Daily Sales vs Target")
        
        # Sample data for daily sales vs target
        dates = pd.date_range(start=start_date, end=end_date)
        daily_sales = np.random.randint(200000, 500000, size=len(dates))
        daily_target = np.random.randint(300000, 400000, size=len(dates))
        
        daily_data = pd.DataFrame({
            "Date": dates,
            "Sales": daily_sales,
            "Target": daily_target
        })
        
        # Create a line chart with both sales and target
        fig = px.line(
            daily_data, 
            x="Date", 
            y=["Sales", "Target"],
            title="Daily Sales Performance vs Target",
            labels={"value": "Amount (₹)", "variable": "Metric"},
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance vs target table
        st.markdown("#### Performance Summary")
        
        # Calculate performance metrics
        total_sales = daily_sales.sum()
        total_target = daily_target.sum()
        achievement = (total_sales / total_target) * 100
        
        summary_data = {
            "Metric": ["Total Sales", "Total Target", "Achievement", "Variance"],
            "Value": [f"₹{total_sales/100000:.2f}L", f"₹{total_target/100000:.2f}L", 
                      f"{achievement:.1f}%", f"₹{(total_sales-total_target)/100000:.2f}L"]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df)
    
    # Category Analysis Tab
    with perf_tabs[1]:
        st.markdown("### Product Category Analysis")
        
        # Sample data for category analysis
        categories = ["Denim Jeans", "Shirts", "T-Shirts", "Jackets", "Accessories"]
        category_sales = [1200000, 800000, 650000, 350000, 240000]
        
        # Create a pie chart for category distribution
        fig = px.pie(
            names=categories,
            values=category_sales,
            title="Sales by Product Category",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Category performance table
        category_data = {
            "Category": categories,
            "Sales (₹)": [f"₹{s/100000:.2f}L" for s in category_sales],
            "Units Sold": [3200, 2400, 2100, 800, 1950],
            "Avg. Price": ["₹3,750", "₹3,333", "₹3,095", "₹4,375", "₹1,231"]
        }
        
        category_df = pd.DataFrame(category_data)
        st.dataframe(category_df, use_container_width=True)
    
    # Store Comparison Tab
    with perf_tabs[2]:
        st.markdown("### Store Performance Comparison")
        
        # Sample data for store comparison
        stores = ["Delhi - Sarojini", "Mumbai Hub", "Bangalore Central", "Chennai T. Nagar", "Delhi - Select Citywalk"]
        store_sales = [3250000, 2870000, 2210000, 1850000, 3620000]
        store_targets = [3000000, 3000000, 2500000, 2000000, 3500000]
        
        # Calculate performance vs target
        performance_pct = [(s/t)*100 for s, t in zip(store_sales, store_targets)]
        
        # Create a horizontal bar chart comparing performance
        comparison_data = pd.DataFrame({
            "Store": stores,
            "Sales": store_sales,
            "Target": store_targets,
            "Achievement": performance_pct
        })
        
        fig = px.bar(
            comparison_data,
            y="Store",
            x="Achievement",
            orientation='h',
            title="Store Performance vs Target (%)",
            color="Achievement",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[80, 120],
            text=comparison_data["Achievement"].apply(lambda x: f"{x:.1f}%")
        )
        
        fig.update_layout(
            xaxis_title="Achievement (%)",
            yaxis_title="",
            height=400,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Store performance detailed table
        st.markdown("#### Detailed Store Performance")
        
        comparison_data["Sales"] = comparison_data["Sales"].apply(lambda x: f"₹{x/100000:.2f}L")
        comparison_data["Target"] = comparison_data["Target"].apply(lambda x: f"₹{x/100000:.2f}L")
        comparison_data["Achievement"] = comparison_data["Achievement"].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(comparison_data, use_container_width=True)

def show_loyalty_program():
    """Show the E-Wards Loyalty Program management"""
    
    st.subheader("E-Wards Loyalty Program")
    
    st.markdown("""
    Manage and analyze the Voi Jeans E-Wards Loyalty Program across all retail locations. 
    The program rewards customers for purchases and encourages repeat business through 
    a tiered reward system.
    """)
    
    # Program performance metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Members", value="24,850", delta="+1,200")
    with col2:
        st.metric(label="Active Members", value="18,620", delta="+850")
    with col3:
        st.metric(label="Redemption Rate", value="62%", delta="+5%")
    with col4:
        st.metric(label="Avg Points/Member", value="2,480", delta="+120")
    
    # Loyalty tiers visualization
    st.markdown("### Member Tier Distribution")
    
    # Sample data for loyalty tiers
    tiers = ["Silver", "Gold", "Platinum", "Diamond"]
    members = [12500, 8200, 3100, 1050]
    colors = ["#C0C0C0", "#FFD700", "#E5E4E2", "#B9F2FF"]
    
    # Create a funnel chart for tier distribution
    fig = go.Figure(go.Funnel(
        y=tiers,
        x=members,
        textinfo="value+percent initial",
        marker={"color": colors}
    ))
    
    fig.update_layout(
        title="Loyalty Tier Distribution",
        template="plotly_dark",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Program benefits overview
    st.markdown("### E-Wards Program Benefits")
    
    # Create a table for program benefits
    benefits_data = {
        "Tier": tiers,
        "Min. Purchase (₹)": ["0", "₹10,000", "₹25,000", "₹50,000"],
        "Points per ₹100": ["5", "7", "10", "15"],
        "Birthday Gift": ["Yes", "Yes", "Yes", "Yes"],
        "Exclusive Discounts": ["5%", "10%", "15%", "20%"],
        "Early Access": ["No", "Yes", "Yes", "Yes"],
        "Personal Stylist": ["No", "No", "Yes", "Yes"],
        "Free Alterations": ["No", "No", "No", "Yes"]
    }
    
    benefits_df = pd.DataFrame(benefits_data)
    st.table(benefits_df)
    
    # Campaign management section
    st.markdown("### Loyalty Campaigns")
    
    with st.expander("Create New Campaign", expanded=False):
        # Campaign creation form
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Campaign Name", "Summer Double Points")
            st.date_input("Start Date", datetime.now())
            st.date_input("End Date", datetime.now() + timedelta(days=30))
            st.multiselect("Target Tiers", tiers, default=["Silver", "Gold"])
        
        with col2:
            st.text_area("Campaign Description", "Earn double points on all purchases during the summer sale.")
            st.number_input("Points Multiplier", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
            st.selectbox("Campaign Type", ["Points Multiplier", "Bonus Points", "Discount", "Free Gift"])
            st.button("Create Campaign", use_container_width=True)
    
    # Active campaigns table
    st.markdown("#### Active Campaigns")
    
    campaigns_data = {
        "Campaign": ["Summer Double Points", "Birthday Month Bonus", "New Collection Launch", "Referral Rewards"],
        "Type": ["Points Multiplier", "Bonus Points", "Free Gift", "Bonus Points"],
        "Target Tiers": ["All Tiers", "Gold+", "Platinum+", "All Tiers"],
        "Status": ["Active", "Active", "Starting Soon", "Active"],
        "Period": ["Jun 1-30", "Monthly", "Jul 15-31", "Ongoing"]
    }
    
    campaigns_df = pd.DataFrame(campaigns_data)
    st.dataframe(campaigns_df, use_container_width=True)

def show_consumer_insights():
    """Show consumer behavior insights and trends"""
    
    st.subheader("Consumer Behavior Insights")
    
    st.markdown("""
    Analyze consumer behavior trends and preferences to inform merchandising, 
    marketing, and product development strategies.
    """)
    
    # Create tabs for different types of insights
    insight_tabs = st.tabs(["Gender & Age Analysis", "Shopping Preferences", "Style Preferences", "Market Trends"])
    
    # Gender & Age Analysis Tab
    with insight_tabs[0]:
        st.markdown("### Customer Demographics")
        
        # Gender distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Gender Distribution")
            
            # Sample data for gender distribution
            genders = ["Women", "Men"]
            gender_distribution = [61, 39]
            
            # Create a simple pie chart for gender distribution
            fig = px.pie(
                names=genders,
                values=gender_distribution,
                title="Gender Distribution",
                template="plotly_dark",
                color_discrete_sequence=["#FF9AA2", "#86C7F3"]
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Age Distribution")
            
            # Sample data for age distribution
            age_groups = ["Teenagers (13-19)", "Young Adults (20-35)", "Middle-Aged Adults (36-50)", "Seniors (50+)"]
            age_distribution = [23, 37, 26, 14]
            
            # Create a bar chart for age distribution
            fig = px.bar(
                x=age_groups,
                y=age_distribution,
                title="Age Distribution",
                template="plotly_dark",
                text=age_distribution
            )
            
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Percentage (%)",
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Fashion category popularity by gender
        st.markdown("### Fashion Category Popularity by Gender")
        
        # Sample data for category popularity by gender
        categories = ["Ethnic Wear", "Casual Clothing", "Formal Clothes", "Athleisure/Sportswear", "Accessories"]
        men_preferences = [12, 34, 24, 21, 7]
        women_preferences = [36, 26, 12, 11, 17]
        
        # Create a grouped bar chart
        category_data = pd.DataFrame({
            "Category": categories + categories,
            "Preference": men_preferences + women_preferences,
            "Gender": ["Men"] * len(categories) + ["Women"] * len(categories)
        })
        
        fig = px.bar(
            category_data,
            x="Category",
            y="Preference",
            color="Gender",
            barmode="group",
            title="Fashion Category Popularity by Gender",
            template="plotly_dark",
            color_discrete_sequence=["#86C7F3", "#FF9AA2"]
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Percentage (%)",
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Shopping Preferences Tab
    with insight_tabs[1]:
        st.markdown("### Shopping Channel Preferences")
        
        # Shopping channel preferences data
        channels = ["Offline Shopping", "Hybrid Shopping", "Online Shopping"]
        channel_preferences = [47, 40, 13]
        
        # Create a horizontal bar chart
        fig = px.bar(
            y=channels,
            x=channel_preferences,
            orientation='h',
            title="Shopping Channel Preferences",
            template="plotly_dark",
            text=[f"{p}%" for p in channel_preferences],
            color=channel_preferences,
            color_continuous_scale="Blues"
        )
        
        fig.update_layout(
            xaxis_title="Percentage (%)",
            yaxis_title="",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Purchase triggers and barriers
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Purchase Triggers")
            
            # Sample data for purchase triggers
            triggers = ["Fit & Comfort", "Price", "Brand", "Quality", "Style", "Sustainability"]
            trigger_values = [32, 30, 18, 12, 4, 4]
            
            # Create a pie chart for purchase triggers
            fig = px.pie(
                names=triggers,
                values=trigger_values,
                title="What Drives Purchase Decisions",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Purchase Barriers")
            
            # Sample data for purchase barriers
            barriers = ["Price Sensitivity", "Fit Issues", "Quality Concerns", "Limited Options", "Sustainability"]
            barrier_values = [30, 28, 24, 16, 2]
            
            # Create a pie chart for purchase barriers
            fig = px.pie(
                names=barriers,
                values=barrier_values,
                title="What Prevents Purchases",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        # Consumer segmentation
        st.markdown("### Consumer Psychographic Segmentation")
        
        # Sample data for consumer segmentation
        segments = ["Aspirational Trendsetters", "Value-Conscious Shoppers", "Digital-Savvy Consumers", 
                    "Cultural Traditionalists", "Casual Comfort Seekers"]
        segment_values = [31, 24, 23, 11, 11]
        
        # Create a horizontal bar chart
        fig = px.bar(
            y=segments,
            x=segment_values,
            orientation='h',
            title="Consumer Psychographic Segments",
            template="plotly_dark",
            text=[f"{v}%" for v in segment_values],
            color=segment_values,
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(
            xaxis_title="Percentage (%)",
            yaxis_title="",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Style Preferences Tab
    with insight_tabs[2]:
        st.markdown("### Style Preferences Analysis")
        
        # Create a radar chart for style preferences
        # Sample data for style preferences
        categories = ['Comfort', 'Trendy', 'Classic', 'Vibrant Colors', 'Patterns', 'Minimalist']
        
        men_values = [85, 60, 75, 50, 55, 70]
        women_values = [80, 85, 65, 75, 70, 65]
        
        # Create a radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=men_values,
            theta=categories,
            fill='toself',
            name='Men'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=women_values,
            theta=categories,
            fill='toself',
            name='Women'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Style Preference Analysis by Gender",
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Product details popularity
        st.markdown("### Popular Product Details")
        
        # Create two columns for men and women
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Popular Details - Men's Clothing")
            
            # Sample data for men's popular details
            men_details = {
                "Jeans": ["Slim Fit", "Distressed Finish", "Stretch Fabric", "Dark Wash", "Regular Rise"],
                "Popularity": [85, 70, 65, 60, 55]
            }
            
            # Create a bar chart
            fig = px.bar(
                x=men_details["Jeans"],
                y=men_details["Popularity"],
                title="Popular Jeans Details - Men",
                template="plotly_dark",
                color=men_details["Popularity"],
                color_continuous_scale="Blues"
            )
            
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Popularity Score",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Popular Details - Women's Clothing")
            
            # Sample data for women's popular details
            women_details = {
                "Jeans": ["High Rise", "Skinny Fit", "Ankle Length", "Stretch Fabric", "Light Wash"],
                "Popularity": [90, 75, 70, 65, 60]
            }
            
            # Create a bar chart
            fig = px.bar(
                x=women_details["Jeans"],
                y=women_details["Popularity"],
                title="Popular Jeans Details - Women",
                template="plotly_dark",
                color=women_details["Popularity"],
                color_continuous_scale="Reds"
            )
            
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Popularity Score",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal trends
        st.markdown("### Seasonal Style Trends")
        
        # Sample data for seasonal trends
        seasons = ["Spring", "Summer", "Monsoon", "Autumn", "Winter"]
        styles = ["Light Wash Denim", "Bright Colored Tops", "Water-Resistant Wear", "Layered Outfits", "Heavy Denim & Jackets"]
        popularity = [75, 85, 65, 70, 80]
        
        # Create a seasonal trends dataframe
        seasonal_data = pd.DataFrame({
            "Season": seasons,
            "Top Style": styles,
            "Popularity": popularity
        })
        
        # Display as an interactive table
        st.dataframe(seasonal_data, use_container_width=True)
        
        # Create a line chart showing seasonal popularity
        fig = px.line(
            seasonal_data,
            x="Season",
            y="Popularity",
            title="Seasonal Style Popularity",
            template="plotly_dark",
            markers=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Market Trends Tab
    with insight_tabs[3]:
        st.markdown("### Retail Fashion Market Trends")
        
        # Key insights from consumer behavior trends
        st.info("""
        ### Key Consumer Trends
        
        1. **The "Reverse Traditional Wear Paradox"**
           - Women embrace ethnic wear (36% preference) and can wear it professionally
           - Men face workplace restrictions on traditional clothing
           - Opportunity for "modern professional ethnic wear" for men
        
        2. **The "Sustainability Paradox"**
           - Despite discussions about sustainability importance, it ranks low (4% as purchase trigger)
           - Represents a "values-action gap" - consumers care in theory but don't act on it
           - Opportunity to make sustainable choices easier and more automatic
        
        3. **The "Touch-and-Feel Premium"**
           - Strong preference for offline shopping (47%) and hybrid shopping (40%)
           - Pure online shopping at only 13% indicates tactile experience still important
           - Opportunity for "touch-and-feel samples" for online shoppers
        
        4. **The Aspiration-Value Tension**
           - Largest segment is "Aspirational Trendsetters" (31%)
           - Yet price sensitivity remains high (30% cite it as barrier)
           - Market ripe for "accessible luxury" positioning
        """)
        
        # Success tracking metrics
        st.markdown("### Success Tracking Metrics")
        
        # Success metrics data
        metrics_data = {
            "Metric": ["Adoption Rate", "CAC Reduction", "Inventory Aging Reduction", 
                       "Employee Incentive Utilization", "Feedback Scores"],
            "Definition": ["Percentage of team actively using the system", 
                          "Decrease in customer acquisition costs", 
                          "Reduction in aging inventory (>60 days)", 
                          "Incentives distributed based on sales performance", 
                          "Employee satisfaction and usability feedback"],
            "Target Goal": ["90% within 6 weeks", "10-15% reduction in 3 months", 
                           "20% improvement in inventory turnover", 
                           "80% of incentives claimed", 
                           "4.5/5 average feedback score"]
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.table(metrics_df)
        
        # CAC tracking model
        st.markdown("### Customer Acquisition Cost (CAC) Tracking")
        
        # CAC data
        cac_data = {
            "Channel": ["Online (Google Ads)", "Online (Social Media)", "Offline (Store Events)", "Other Marketing", "Total"],
            "Marketing & Sales Expenses (₹)": ["15,00,000", "10,00,000", "20,00,000", "5,00,000", "50,00,000"],
            "New Customers Acquired": [300, 200, 400, 100, 1000],
            "CAC (₹)": ["5,000", "5,000", "5,000", "5,000", "5,000"]
        }
        
        cac_df = pd.DataFrame(cac_data)
        st.dataframe(cac_df, use_container_width=True)
        
        # Marketing scope
        st.markdown("### Marketing Activities Scope")
        
        marketing_scope = [
            "Google Display Network Ads Servicing",
            "Google Ads Pixel Installation",
            "Google Retargeting Ads",
            "Landing Page Optimisation",
            "Facebook Sales Ads Campaigns",
            "Facebook Engagement Boost Campaign",
            "Facebook Retargeting Ads",
            "Facebook Lookalike Audience Ads",
            "Facebook & Instagram Pixel Installation",
            "Instagram Sales Ads Servicing",
            "Instagram Retargeting Ads",
            "Instagram Lookalike Audience Ads",
            "Instagram Follower Growth Ad Campaign",
            "Online Reputation Management"
        ]
        
        # Display as checklist items
        st.markdown("#### Monthly Marketing Activities")
        for activity in marketing_scope:
            st.checkbox(activity, value=True, disabled=True)

if __name__ == "__main__":
    show_retail_distribution()