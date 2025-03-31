import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
import datetime
from io import BytesIO
import os
import base64
from PIL import Image
import matplotlib.pyplot as plt

# Define badge data structure and milestone achievements
MILESTONE_BADGES = {
    "investment_milestones": [
        {
            "id": "first_investment",
            "name": "First Investment",
            "description": "Made your first investment",
            "icon": "🏅",
            "criteria": "Complete your first investment transaction",
            "points": 10,
            "category": "Beginner",
            "color": "#4CAF50"  # Green
        },
        {
            "id": "diversify_portfolio",
            "name": "Portfolio Diversifier",
            "description": "Invest in at least 3 different asset classes",
            "icon": "🌈",
            "criteria": "Hold investments across 3+ asset types (stocks, bonds, etc.)",
            "points": 20,
            "category": "Intermediate",
            "color": "#2196F3"  # Blue
        },
        {
            "id": "six_month_holder",
            "name": "Patient Investor",
            "description": "Hold investments for over 6 months",
            "icon": "⏱️",
            "criteria": "Maintain investment positions for 180+ days",
            "points": 15,
            "category": "Intermediate",
            "color": "#FFC107"  # Amber
        },
        {
            "id": "profit_maker",
            "name": "Profit Maker",
            "description": "Achieve positive returns on investments",
            "icon": "📈",
            "criteria": "Generate positive returns on any investment",
            "points": 25,
            "category": "Intermediate",
            "color": "#9C27B0"  # Purple
        },
        {
            "id": "milestone_1k",
            "name": "₹1,000 Milestone",
            "description": "Grow your portfolio to ₹1,000",
            "icon": "💰",
            "criteria": "Total portfolio value reaches ₹1,000",
            "points": 15,
            "category": "Beginner",
            "color": "#FF5722"  # Deep Orange
        },
        {
            "id": "milestone_10k",
            "name": "₹10,000 Club",
            "description": "Grow your portfolio to ₹10,000",
            "icon": "💎",
            "criteria": "Total portfolio value reaches ₹10,000",
            "points": 30,
            "category": "Intermediate",
            "color": "#673AB7"  # Deep Purple
        },
        {
            "id": "milestone_100k",
            "name": "₹100,000 Elite",
            "description": "Grow your portfolio to ₹100,000",
            "icon": "👑",
            "criteria": "Total portfolio value reaches ₹100,000",
            "points": 50,
            "category": "Advanced",
            "color": "#F44336"  # Red
        },
        {
            "id": "milestone_1m",
            "name": "₹1 Million Maestro",
            "description": "Achieve millionaire status with ₹1,000,000 portfolio",
            "icon": "🏆",
            "criteria": "Total portfolio value reaches ₹1,000,000",
            "points": 100,
            "category": "Expert",
            "color": "#E91E63"  # Pink
        }
    ],
    "value_creation": [
        {
            "id": "value_creator",
            "name": "Value Creator",
            "description": "Create measurable business value",
            "icon": "🚀",
            "criteria": "Document value creation of at least ₹50,000",
            "points": 25,
            "category": "Advanced",
            "color": "#3F51B5"  # Indigo
        },
        {
            "id": "cost_optimizer",
            "name": "Cost Optimizer",
            "description": "Successfully reduce business costs",
            "icon": "✂️",
            "criteria": "Implement cost saving measures totaling ₹25,000+",
            "points": 20,
            "category": "Intermediate",
            "color": "#009688"  # Teal
        },
        {
            "id": "revenue_booster",
            "name": "Revenue Booster",
            "description": "Drive significant revenue increase",
            "icon": "💵",
            "criteria": "Contribute to ₹100,000+ in additional revenue",
            "points": 30,
            "category": "Advanced",
            "color": "#8BC34A"  # Light Green
        }
    ],
    "business_goals": [
        {
            "id": "goal_achiever",
            "name": "Goal Achiever",
            "description": "Meet all quarterly business targets",
            "icon": "🎯",
            "criteria": "Successfully hit 100% of quarterly goals",
            "points": 25,
            "category": "Intermediate",
            "color": "#FF9800"  # Orange
        },
        {
            "id": "growth_driver",
            "name": "Growth Driver",
            "description": "Drive exceptional business growth",
            "icon": "📈",
            "criteria": "Help achieve 25%+ year-over-year growth",
            "points": 35,
            "category": "Advanced",
            "color": "#607D8B"  # Blue Grey
        },
        {
            "id": "expansion_leader",
            "name": "Expansion Leader",
            "description": "Lead expansion into new markets",
            "icon": "🌍",
            "criteria": "Successfully enter new market or territory",
            "points": 40,
            "category": "Expert",
            "color": "#CDDC39"  # Lime
        }
    ],
    "financial_literacy": [
        {
            "id": "learning_starter",
            "name": "Financial Learner",
            "description": "Begin your financial education journey",
            "icon": "📚",
            "criteria": "Complete first financial literacy module",
            "points": 10,
            "category": "Beginner",
            "color": "#00BCD4"  # Cyan
        },
        {
            "id": "knowledge_builder",
            "name": "Knowledge Builder",
            "description": "Expand your financial knowledge",
            "icon": "🧠",
            "criteria": "Complete 5+ financial literacy modules",
            "points": 20,
            "category": "Intermediate",
            "color": "#9E9E9E"  # Grey
        },
        {
            "id": "finance_master",
            "name": "Finance Master",
            "description": "Achieve mastery of financial concepts",
            "icon": "🎓",
            "criteria": "Complete all financial literacy modules",
            "points": 30,
            "category": "Advanced", 
            "color": "#795548"  # Brown
        }
    ]
}

# Sample user data - In a real application, this would come from a database
def load_user_passport_data():
    """
    Load user's milestone passport data from session state or initialize if not exists
    """
    if 'milestone_passport' not in st.session_state:
        # Initialize with some earned badges for demonstration
        sample_earned = [
            {"badge_id": "first_investment", "date_earned": "2024-12-15", "details": "Initial investment of ₹5,000 in VOI growth fund"},
            {"badge_id": "milestone_1k", "date_earned": "2024-12-20", "details": "Portfolio reached ₹1,000 milestone"},
            {"badge_id": "learning_starter", "date_earned": "2024-12-10", "details": "Completed 'Investment Basics' module"}
        ]
        
        # Initialize user passport data
        st.session_state.milestone_passport = {
            "user_id": "VOI1001",
            "name": "Voi Jeans Finance Manager",
            "email": "finance@voijeans.com",
            "points_total": sum(get_badge_points(badge["badge_id"]) for badge in sample_earned),
            "badges_earned": sample_earned,
            "progress": {
                "investment_milestones": 2,
                "value_creation": 0,
                "business_goals": 0,
                "financial_literacy": 1
            },
            "level": "Beginner",
            "joined_date": "2024-12-01"
        }
    
    return st.session_state.milestone_passport

def get_badge_points(badge_id):
    """Get points for a specific badge"""
    for category in MILESTONE_BADGES:
        for badge in MILESTONE_BADGES[category]:
            if badge["id"] == badge_id:
                return badge["points"]
    return 0

def get_badge_by_id(badge_id):
    """Get badge details by ID"""
    for category in MILESTONE_BADGES:
        for badge in MILESTONE_BADGES[category]:
            if badge["id"] == badge_id:
                return badge
    return None

def get_earned_badges(user_data):
    """Get list of earned badges with full details"""
    earned_badges = []
    for earned in user_data["badges_earned"]:
        badge = get_badge_by_id(earned["badge_id"])
        if badge:
            # Combine badge details with earning date
            full_badge = badge.copy()
            full_badge["date_earned"] = earned["date_earned"]
            full_badge["details"] = earned["details"]
            earned_badges.append(full_badge)
    
    # Sort by date earned, newest first
    earned_badges.sort(key=lambda x: x["date_earned"], reverse=True)
    return earned_badges

def get_available_badges(user_data):
    """Get list of available badges (not yet earned)"""
    earned_ids = [badge["badge_id"] for badge in user_data["badges_earned"]]
    available_badges = []
    
    for category in MILESTONE_BADGES:
        for badge in MILESTONE_BADGES[category]:
            if badge["id"] not in earned_ids:
                badge_copy = badge.copy()
                badge_copy["category_name"] = category.replace("_", " ").title()
                available_badges.append(badge_copy)
    
    return available_badges

def award_badge(badge_id, details):
    """Award a new badge to the user"""
    if 'milestone_passport' not in st.session_state:
        load_user_passport_data()
    
    user_data = st.session_state.milestone_passport
    
    # Check if badge is already earned
    for badge in user_data["badges_earned"]:
        if badge["badge_id"] == badge_id:
            return False
    
    # Add new badge
    badge = get_badge_by_id(badge_id)
    if badge:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        user_data["badges_earned"].append({
            "badge_id": badge_id,
            "date_earned": today,
            "details": details
        })
        
        # Update points
        user_data["points_total"] += badge["points"]
        
        # Update category progress
        for category in MILESTONE_BADGES:
            if any(b["id"] == badge_id for b in MILESTONE_BADGES[category]):
                user_data["progress"][category] += 1
                break
        
        # Update level based on points
        if user_data["points_total"] >= 100:
            user_data["level"] = "Expert"
        elif user_data["points_total"] >= 50:
            user_data["level"] = "Advanced"
        elif user_data["points_total"] >= 20:
            user_data["level"] = "Intermediate"
        else:
            user_data["level"] = "Beginner"
        
        return True
    
    return False

def render_badge_card(badge, earned=False):
    """Render a single badge card"""
    if earned:
        date_text = f"🏆 Earned on {badge['date_earned']}"
        details = badge.get("details", "")
    else:
        date_text = "🔒 Not yet earned"
        details = "Complete the criteria to earn this badge"
    
    # Create a card with the badge details
    st.markdown(f"""
    <div style="background-color: {badge['color']}20; border-left: 5px solid {badge['color']}; 
         padding: 15px; border-radius: 5px; margin-bottom: 10px;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2em; margin-right: 15px;">{badge['icon']}</div>
            <div>
                <h3 style="margin: 0;">{badge['name']}</h3>
                <p style="margin: 0; opacity: 0.7; font-size: 0.9em;">{badge['category']} Level</p>
                <p style="margin: 5px 0;">{badge['description']}</p>
                <p style="margin: 0; font-size: 0.8em; opacity: 0.9;">{date_text}</p>
                <p style="margin: 0; font-size: 0.8em;">{details}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_progress_chart(user_data):
    """Create a radar chart showing progress in different categories"""
    categories = list(user_data["progress"].keys())
    values = list(user_data["progress"].values())
    
    # Get maximum possible in each category
    max_values = [len(MILESTONE_BADGES[cat]) for cat in categories]
    
    # Calculate percentages
    percentages = [int(100 * values[i] / max_values[i]) if max_values[i] > 0 else 0 for i in range(len(values))]
    
    # Create formatted category labels
    labels = [cat.replace("_", " ").title() for cat in categories]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=percentages,
        theta=labels,
        fill='toself',
        name='Progress',
        line_color='#1E88E5',
        fillcolor='rgba(30, 136, 229, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Milestone Progress by Category (%)",
        height=400
    )
    
    return fig

def create_badges_summary_chart(user_data):
    """Create a horizontal bar chart showing badges earned by category"""
    # Count badges in each category
    category_counts = {category: 0 for category in MILESTONE_BADGES.keys()}
    
    for earned in user_data["badges_earned"]:
        for category, badges in MILESTONE_BADGES.items():
            if any(badge["id"] == earned["badge_id"] for badge in badges):
                category_counts[category] += 1
                break
    
    # Prepare data for chart
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    
    # Format category labels
    labels = [cat.replace("_", " ").title() for cat in categories]
    
    # Create bar chart
    colors = ['#1E88E5', '#43A047', '#FB8C00', '#E53935']
    
    fig = go.Figure(go.Bar(
        x=counts,
        y=labels,
        orientation='h',
        marker_color=colors[:len(counts)],
        text=counts,
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Badges Earned by Category",
        xaxis_title="Number of Badges",
        height=300,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig

def show_investment_milestone_passport():
    """Main function to display the Investment Milestone Passport interface"""
    st.title("Investment Milestone Passport 🪪")
    
    # Load user data
    user_data = load_user_passport_data()
    earned_badges = get_earned_badges(user_data)
    available_badges = get_available_badges(user_data)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 My Badges", "📊 Progress", "🎯 Available Milestones", "⚙️ Admin"])
    
    with tab1:
        st.subheader("My Earned Badges")
        
        # User summary
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.metric("Total Points", user_data["points_total"])
        with col2:
            st.metric("Badges Earned", len(earned_badges))
        with col3:
            st.metric("Current Level", user_data["level"])
        
        # Show all earned badges
        if earned_badges:
            st.write("---")
            for badge in earned_badges:
                render_badge_card(badge, earned=True)
        else:
            st.info("You haven't earned any badges yet. Check the 'Available Milestones' tab to see what you can achieve!")
    
    with tab2:
        st.subheader("My Investment Milestone Progress")
        
        # Progress charts
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Radar chart for category progress
            progress_chart = create_progress_chart(user_data)
            st.plotly_chart(progress_chart, use_container_width=True)
        
        with col2:
            # Bar chart for badges summary
            badges_chart = create_badges_summary_chart(user_data)
            st.plotly_chart(badges_chart, use_container_width=True)
        
        # Progress stats
        st.write("---")
        st.subheader("Growth Statistics")
        
        # Calculate completion percentage
        total_badges = sum(len(badges) for badges in MILESTONE_BADGES.values())
        completion_pct = int(100 * len(earned_badges) / total_badges)
        
        # Progress bar
        st.progress(completion_pct / 100)
        st.write(f"Overall Completion: {completion_pct}% ({len(earned_badges)} of {total_badges} badges)")
        
        # Next level calculation
        points_needed = 0
        next_level = ""
        
        if user_data["level"] == "Beginner":
            points_needed = 20 - user_data["points_total"]
            next_level = "Intermediate"
        elif user_data["level"] == "Intermediate":
            points_needed = 50 - user_data["points_total"]
            next_level = "Advanced"
        elif user_data["level"] == "Advanced":
            points_needed = 100 - user_data["points_total"]
            next_level = "Expert"
        
        if points_needed > 0:
            st.info(f"You need {points_needed} more points to reach {next_level} level!")
        else:
            st.success("You've reached the highest level! Keep collecting badges to increase your total score.")
    
    with tab3:
        st.subheader("Available Milestone Badges")
        
        # Filter options
        category_filter = st.multiselect(
            "Filter by Category:",
            options=list(MILESTONE_BADGES.keys()),
            format_func=lambda x: x.replace("_", " ").title(),
            default=list(MILESTONE_BADGES.keys())
        )
        
        # Filter badges by selected categories
        filtered_badges = [badge for badge in available_badges 
                         if any(cat == badge["category_name"].lower().replace(" ", "_") for cat in category_filter)]
        
        # Group badges by category
        for category in category_filter:
            category_badges = [badge for badge in filtered_badges 
                             if badge["category_name"].lower().replace(" ", "_") == category]
            
            if category_badges:
                st.write(f"### {category.replace('_', ' ').title()}")
                
                for badge in category_badges:
                    # Display badge with criteria
                    st.markdown(f"""
                    <div style="background-color: {badge['color']}10; border-left: 5px solid {badge['color']}; 
                         padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center;">
                            <div style="font-size: 2em; margin-right: 15px;">{badge['icon']}</div>
                            <div>
                                <h3 style="margin: 0;">{badge['name']} ({badge['points']} pts)</h3>
                                <p style="margin: 0; opacity: 0.7; font-size: 0.9em;">{badge['category']} Level</p>
                                <p style="margin: 5px 0;">{badge['description']}</p>
                                <p style="margin: 0; font-size: 0.8em;"><strong>How to earn:</strong> {badge['criteria']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        if not filtered_badges:
            st.info("No badges available in the selected categories. Try selecting different categories or you may have earned them all!")
    
    with tab4:
        st.subheader("Badge Administration")
        st.info("Admin tools for manually awarding badges to users")
        
        # Badge award form
        with st.form("award_badge_form"):
            st.write("Manually Award a Badge")
            
            # Select badge to award
            badge_options = [(badge["id"], f"{badge['name']} ({badge['category_name']})") for badge in available_badges]
            selected_badge_id = st.selectbox(
                "Select Badge to Award:",
                options=[option[0] for option in badge_options],
                format_func=lambda x: next((option[1] for option in badge_options if option[0] == x), x)
            )
            
            # Details about achievement
            achievement_details = st.text_area(
                "Achievement Details",
                placeholder="Enter details about how this badge was earned..."
            )
            
            # Submit button
            submitted = st.form_submit_button("Award Badge")
            
            if submitted and selected_badge_id and achievement_details:
                success = award_badge(selected_badge_id, achievement_details)
                if success:
                    st.success(f"Badge successfully awarded!")
                    # Force refresh
                    st.rerun()
                else:
                    st.error("Failed to award badge. It may already be earned.")

def add_section_to_management_hub():
    """
    This function is used to add the Investment Milestone Passport
    section to the Management Hub sidebar navigation
    """
    return """
    # Investment Milestones section
    st.markdown("#### Investment Milestones")
    if st.button("🪪 Investment Milestone Passport", use_container_width=True, key="milestone_passport", help="Collect digital badges for financial milestones"):
        st.session_state.page = 'investment_milestone_passport'
    """

if __name__ == "__main__":
    show_investment_milestone_passport()