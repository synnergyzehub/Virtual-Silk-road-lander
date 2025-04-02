import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def show_merchandiser_agent():
    """Display the merchandiser agent interface"""
    
    # Initialize merchandiser data if not already in session state
    if 'merchandiser' not in st.session_state:
        # Assign a random merchandiser from our team
        merchandisers = [
            {
                "id": "MER001",
                "name": "Alex Chen",
                "avatar": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/user.svg",
                "specialization": "Denim Specialist",
                "experience": "7 years",
                "languages": ["English", "Mandarin", "Spanish"],
                "expertise": ["Sustainable Sourcing", "Quality Control", "Technical Design"],
                "email": "alex.chen@buyinghouse.com",
                "phone": "+1 (555) 123-4567",
                "time_zone": "GMT+8",
                "availability": "Mon-Fri, 9am-5pm GMT+8",
                "last_active": "Just now"
            },
            {
                "id": "MER002",
                "name": "Sarah Johnson",
                "avatar": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/user.svg",
                "specialization": "Knits Expert",
                "experience": "5 years",
                "languages": ["English", "French"],
                "expertise": ["Material Innovation", "Color Management", "Production Optimization"],
                "email": "sarah.johnson@buyinghouse.com",
                "phone": "+1 (555) 987-6543",
                "time_zone": "GMT-5",
                "availability": "Mon-Fri, 8am-4pm GMT-5",
                "last_active": "30 minutes ago"
            },
            {
                "id": "MER003",
                "name": "Rahul Patel",
                "avatar": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/user.svg",
                "specialization": "Technical Fabrics",
                "experience": "9 years",
                "languages": ["English", "Hindi", "Gujarati"],
                "expertise": ["Performance Textiles", "Compliance Documentation", "Factory Audits"],
                "email": "rahul.patel@buyinghouse.com",
                "phone": "+1 (555) 234-5678",
                "time_zone": "GMT+5:30",
                "availability": "Mon-Sat, 10am-6pm GMT+5:30",
                "last_active": "1 hour ago"
            },
            {
                "id": "MER004",
                "name": "Maria Garcia",
                "avatar": "https://cdn.jsdelivr.net/gh/feathericons/feather@master/icons/user.svg",
                "specialization": "Sustainable Fashion",
                "experience": "6 years",
                "languages": ["English", "Spanish", "Portuguese"],
                "expertise": ["Eco-Friendly Materials", "Ethical Production", "Certification Management"],
                "email": "maria.garcia@buyinghouse.com",
                "phone": "+1 (555) 876-5432",
                "time_zone": "GMT-6",
                "availability": "Mon-Fri, 9am-5pm GMT-6",
                "last_active": "Just now"
            }
        ]
        
        # Assign a random merchandiser
        st.session_state.merchandiser = random.choice(merchandisers)
        
        # Initialize conversation history
        st.session_state.conversation = []
        
        # Add welcome message
        st.session_state.conversation.append({
            "sender": "agent",
            "message": f"Hello! I'm {st.session_state.merchandiser['name']}, your dedicated merchandiser for this order. I'll assist you throughout the entire process from product selection to delivery. Feel free to ask me any questions about our products, customization options, or ordering process.",
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        
        # Initialize schedule
        next_week = datetime.now() + timedelta(days=7)
        st.session_state.scheduled_meetings = [
            {
                "title": "Initial Consultation",
                "date": next_week.strftime("%Y-%m-%d"),
                "time": "10:00 AM",
                "duration": "30 minutes",
                "status": "Scheduled",
                "notes": "Discuss product requirements and customization options"
            }
        ]
        
        # Initialize tasks
        st.session_state.merchandiser_tasks = [
            {
                "title": "Send Fabric Swatches",
                "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "status": "Pending",
                "priority": "High"
            },
            {
                "title": "Provide Cost Breakdown",
                "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "status": "Not Started",
                "priority": "Medium"
            }
        ]
    
    # Layout with tabs
    st.title("Your Merchandiser Agent")
    
    # Main tabs for different sections
    tabs = st.tabs(["Agent Dashboard", "Live Chat", "Meetings & Schedule", "Order Support"])
    
    # Dashboard Tab
    with tabs[0]:
        show_agent_dashboard()
    
    # Live Chat Tab
    with tabs[1]:
        show_live_chat()
    
    # Meetings & Schedule Tab
    with tabs[2]:
        show_meetings_schedule()
    
    # Order Support Tab
    with tabs[3]:
        show_order_support()

def show_agent_dashboard():
    """Display the merchandiser dashboard with key information"""
    
    merchandiser = st.session_state.merchandiser
    
    # Profile section with merchandiser details
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(merchandiser["avatar"], width=150)
        status_color = "green" if "Just now" in merchandiser["last_active"] else "orange"
        st.markdown(f"<div style='background-color:{status_color}; width:15px; height:15px; border-radius:50%; display:inline-block; margin-right:5px;'></div> <span>Active {merchandiser['last_active']}</span>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"## {merchandiser['name']}")
        st.markdown(f"**Specialization:** {merchandiser['specialization']}")
        st.markdown(f"**Experience:** {merchandiser['experience']}")
        
        # Contact details
        st.markdown("### Contact Details")
        st.markdown(f"📧 **Email:** {merchandiser['email']}")
        st.markdown(f"📱 **Phone:** {merchandiser['phone']}")
        st.markdown(f"🕒 **Time Zone:** {merchandiser['time_zone']}")
        st.markdown(f"📅 **Availability:** {merchandiser['availability']}")
    
    # Expertise and Skills
    st.markdown("### Expertise and Skills")
    
    # Show expertise as progress bars
    expertise_areas = {
        "Material Knowledge": random.randint(85, 98),
        "Pricing Negotiation": random.randint(80, 95),
        "Technical Specifications": random.randint(75, 95),
        "Quality Assurance": random.randint(85, 99),
        "Production Management": random.randint(80, 95)
    }
    
    # Create 2 columns
    exp_cols = st.columns(2)
    
    # Display expertise in columns
    for i, (area, level) in enumerate(expertise_areas.items()):
        with exp_cols[i % 2]:
            st.markdown(f"**{area}**")
            st.progress(level/100)
            st.markdown(f"<small>{level}%</small>", unsafe_allow_html=True)
    
    # Language proficiency
    st.markdown("### Language Proficiency")
    
    lang_cols = st.columns(len(merchandiser["languages"]))
    for i, lang in enumerate(merchandiser["languages"]):
        with lang_cols[i]:
            proficiency = "Native" if i == 0 else "Fluent" if i == 1 else "Conversational"
            st.markdown(f"**{lang}**")
            st.markdown(f"<small>{proficiency}</small>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### Order Statistics")
    
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.metric("Orders Managed", str(random.randint(120, 200)))
    with stat_cols[1]:
        st.metric("Client Satisfaction", f"{random.randint(92, 99)}%")
    with stat_cols[2]:
        st.metric("Avg. Response Time", f"{random.randint(15, 45)} min")

def show_live_chat():
    """Display the live chat interface with the merchandiser"""
    
    st.markdown("### Live Chat with Your Merchandiser")
    st.markdown(f"You're chatting with **{st.session_state.merchandiser['name']}**, your dedicated merchandiser")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.conversation:
            alignment = "left" if message["sender"] == "agent" else "right"
            background = "#1E3A8A" if message["sender"] == "agent" else "#2E7D32"
            
            st.markdown(f"""
            <div style='margin-bottom: 10px; text-align: {alignment};'>
                <div style='display: inline-block; background-color: {background}; padding: 10px; border-radius: 10px; max-width: 80%;'>
                    {message["message"]}
                    <div style='font-size: 0.8em; opacity: 0.7; text-align: right;'>{message["timestamp"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    message = st.text_input("Type your message here...", key="chat_input")
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        if st.button("Send Message", use_container_width=True):
            if message:
                # Add user message to conversation
                st.session_state.conversation.append({
                    "sender": "user",
                    "message": message,
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                
                # Generate agent response based on user query
                agent_response = generate_agent_response(message)
                
                # Add agent response to conversation
                st.session_state.conversation.append({
                    "sender": "agent",
                    "message": agent_response,
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                
                # Clear input
                st.session_state.chat_input = ""
                
                # Rerun to update chat display
                st.rerun()
    
    with col2:
        st.button("Attach File", use_container_width=True)
    
    with col3:
        if st.button("Schedule Call", use_container_width=True):
            st.info("Video call scheduling feature will be available soon.")

def generate_agent_response(user_message):
    """Generate agent response based on user message"""
    
    # Simple response logic based on keywords in user message
    user_message = user_message.lower()
    
    if any(word in user_message for word in ["hi", "hello", "hey"]):
        return f"Hello! How can I help you with your order today?"
    
    elif any(word in user_message for word in ["sample", "samples"]):
        return "I'd be happy to arrange sample shipping for you. We typically send physical samples within 5-7 business days. Would you like me to prepare some for your review?"
    
    elif any(word in user_message for word in ["price", "cost", "pricing"]):
        return "Our pricing is based on order volume, fabric selection, and customization requirements. I can prepare a detailed quote for you. Could you share more details about your specific needs?"
    
    elif any(word in user_message for word in ["delivery", "shipping", "timeline"]):
        return "Standard production time is 30-45 days after order confirmation, with shipping taking an additional 5-15 days depending on your location. I can work with you on expedited options if needed."
    
    elif any(word in user_message for word in ["fabric", "material"]):
        return "We offer a wide range of fabrics including cotton, polyester blends, denim, and performance materials. I can send you our fabric catalog with swatches if you'd like to see and feel the options."
    
    elif any(word in user_message for word in ["custom", "customization", "customize"]):
        return "We offer extensive customization options including fabric selection, colors, washes, trims, and packaging. What specific customizations are you interested in for your order?"
    
    elif any(word in user_message for word in ["minimum", "moq"]):
        return "Our standard MOQ is 300 pieces per style, but this can vary by product type. For specialized items or custom developments, the MOQ might be higher. I can discuss options for smaller test orders if needed."
    
    elif any(word in user_message for word in ["payment", "terms", "invoice"]):
        return "Our standard payment terms are 30% deposit at order confirmation, with the remaining 70% due before shipping. We accept wire transfers and letters of credit for international orders."
    
    elif any(word in user_message for word in ["thank", "thanks"]):
        return "You're welcome! I'm here to help with anything else you might need."
    
    else:
        return "Thank you for your message. I'll look into this and get back to you shortly. In the meantime, is there anything specific about our products or ordering process that you'd like to know?"

def show_meetings_schedule():
    """Display the meetings and schedule interface"""
    
    st.markdown("### Your Schedule with Merchandiser")
    
    # Upcoming meetings
    st.subheader("Upcoming Meetings")
    
    if st.session_state.scheduled_meetings:
        for meeting in st.session_state.scheduled_meetings:
            with st.expander(f"{meeting['title']} - {meeting['date']} at {meeting['time']}"):
                st.markdown(f"**Duration:** {meeting['duration']}")
                st.markdown(f"**Status:** {meeting['status']}")
                st.markdown(f"**Notes:** {meeting['notes']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Join Meeting", key=f"join_{meeting['title']}", use_container_width=True)
                with col2:
                    st.button("Reschedule", key=f"reschedule_{meeting['title']}", use_container_width=True)
    else:
        st.info("No upcoming meetings scheduled.")
    
    # Schedule a new meeting
    st.markdown("---")
    st.subheader("Schedule a New Meeting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_title = st.text_input("Meeting Title", value="Order Discussion")
        meeting_date = st.date_input("Meeting Date", min_value=datetime.now().date())
    
    with col2:
        meeting_time = st.selectbox("Meeting Time", 
                                   ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", 
                                    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM"])
        meeting_duration = st.selectbox("Duration", ["15 minutes", "30 minutes", "45 minutes", "60 minutes"])
    
    meeting_notes = st.text_area("Meeting Notes/Agenda", height=100)
    
    if st.button("Schedule Meeting", use_container_width=True):
        new_meeting = {
            "title": meeting_title,
            "date": meeting_date.strftime("%Y-%m-%d"),
            "time": meeting_time,
            "duration": meeting_duration,
            "status": "Scheduled",
            "notes": meeting_notes
        }
        
        st.session_state.scheduled_meetings.append(new_meeting)
        st.success(f"Meeting scheduled for {meeting_date.strftime('%Y-%m-%d')} at {meeting_time}")
        st.balloons()

def show_order_support():
    """Display order support information and tools"""
    
    st.markdown("### Order Support Tools")
    
    # Create tabs for different support tools
    support_tabs = st.tabs(["Task Tracker", "Document Exchange", "Quality Checkpoints"])
    
    # Task Tracker Tab
    with support_tabs[0]:
        st.subheader("Task Tracker")
        st.markdown("Track tasks and action items for your order")
        
        # Display existing tasks
        for i, task in enumerate(st.session_state.merchandiser_tasks):
            with st.expander(f"{task['title']} (Due: {task['due_date']})"):
                st.markdown(f"**Status:** {task['status']}")
                st.markdown(f"**Priority:** {task['priority']}")
                
                # Update task status
                new_status = st.selectbox("Update Status", 
                                        ["Not Started", "Pending", "In Progress", "Completed"], 
                                        ["Not Started", "Pending", "In Progress", "Completed"].index(task['status']),
                                        key=f"status_{i}")
                
                if new_status != task['status']:
                    st.session_state.merchandiser_tasks[i]['status'] = new_status
                    st.success(f"Task '{task['title']}' updated to '{new_status}'")
        
        # Add new task
        st.markdown("---")
        st.subheader("Add New Task")
        
        new_task_title = st.text_input("Task Title")
        col1, col2 = st.columns(2)
        
        with col1:
            new_task_due = st.date_input("Due Date", min_value=datetime.now().date())
        
        with col2:
            new_task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        if st.button("Add Task", use_container_width=True):
            if new_task_title:
                new_task = {
                    "title": new_task_title,
                    "due_date": new_task_due.strftime("%Y-%m-%d"),
                    "status": "Not Started",
                    "priority": new_task_priority
                }
                
                st.session_state.merchandiser_tasks.append(new_task)
                st.success(f"Task '{new_task_title}' added successfully")
                st.rerun()
    
    # Document Exchange Tab
    with support_tabs[1]:
        st.subheader("Document Exchange")
        st.markdown("Share and receive important documents")
        
        # Document categories
        doc_types = ["Technical Specifications", "Price Quotes", "Fabric Swatches", "Sample Approvals", "Production Updates"]
        
        for doc_type in doc_types:
            with st.expander(doc_type):
                st.file_uploader(f"Upload {doc_type}", key=f"upload_{doc_type}")
                st.markdown("**Shared Documents:**")
                
                if doc_type == "Price Quotes":
                    st.markdown("- Price_Quote_March_2025.pdf (Shared 2 days ago)")
                elif doc_type == "Fabric Swatches":
                    st.markdown("- Denim_Fabric_Options.pdf (Shared 1 day ago)")
                else:
                    st.markdown("No documents shared yet")
                
                st.button("Request Document", key=f"request_{doc_type}", use_container_width=True)
    
    # Quality Checkpoints Tab
    with support_tabs[2]:
        st.subheader("Quality Checkpoints")
        st.markdown("Monitor quality control throughout production")
        
        # Sample quality control timeline
        quality_stages = [
            {"stage": "Pre-Production Sample", "status": "Approved", "date": "Mar 15, 2025", "notes": "Sample approved with minor adjustments to collar"},
            {"stage": "Initial Production Run", "status": "Pending", "date": "Apr 5, 2025", "notes": "First 10% of production to be reviewed"},
            {"stage": "Mid-Production Check", "status": "Not Started", "date": "Apr 20, 2025", "notes": "Quality check at 50% production completion"},
            {"stage": "Final Inspection", "status": "Not Started", "date": "May 10, 2025", "notes": "Pre-shipping inspection of finished goods"}
        ]
        
        # Visual progress indicator
        progress_val = 25  # 25% if first stage complete
        st.progress(progress_val/100)
        st.markdown(f"<div style='text-align:center'>Production Quality Progress: {progress_val}%</div>", unsafe_allow_html=True)
        
        # Quality stages as timeline
        for i, stage in enumerate(quality_stages):
            if i < len(quality_stages) - 1:
                col1, col2 = st.columns([1, 10])
                with col1:
                    if stage["status"] == "Approved":
                        st.markdown("✅")
                    elif stage["status"] == "Pending":
                        st.markdown("⏳")
                    else:
                        st.markdown("⏱️")
                
                with col2:
                    with st.expander(f"{stage['stage']} - {stage['date']} ({stage['status']})"):
                        st.markdown(f"**Notes:** {stage['notes']}")
                        
                        if stage["status"] != "Approved":
                            if st.button("Request Update", key=f"update_{i}", use_container_width=True):
                                st.success(f"Update requested for {stage['stage']}")
            else:
                # Last stage
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.markdown("⏱️")
                
                with col2:
                    with st.expander(f"{stage['stage']} - {stage['date']} ({stage['status']})"):
                        st.markdown(f"**Notes:** {stage['notes']}")