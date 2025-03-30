import os
import streamlit as st
import pandas as pd
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Get Twilio credentials from environment or session state
def get_twilio_credentials():
    """Get Twilio credentials from environment or session state"""
    # First check session state
    if 'twilio_credentials' in st.session_state:
        return (
            st.session_state.twilio_credentials.get('account_sid'),
            st.session_state.twilio_credentials.get('auth_token'),
            st.session_state.twilio_credentials.get('phone_number')
        )
    
    # Then check environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    # Store in session state if all variables are available
    if account_sid and auth_token and phone_number:
        if 'twilio_credentials' not in st.session_state:
            st.session_state.twilio_credentials = {}
        st.session_state.twilio_credentials['account_sid'] = account_sid
        st.session_state.twilio_credentials['auth_token'] = auth_token
        st.session_state.twilio_credentials['phone_number'] = phone_number
    
    return account_sid, auth_token, phone_number

def check_twilio_credentials():
    """Check if Twilio credentials are set"""
    account_sid, auth_token, phone_number = get_twilio_credentials()
    if not account_sid or not auth_token or not phone_number:
        return False
    return True

def send_sms_notification(to_phone, message):
    """Send SMS notification using Twilio"""
    # Get credentials
    account_sid, auth_token, phone_number = get_twilio_credentials()
    
    if not account_sid or not auth_token or not phone_number:
        st.error("Twilio credentials are not configured. Please configure them in the notification settings.")
        return False, "Missing Twilio credentials"
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=phone_number,
            to=to_phone
        )
        
        return True, message.sid
    except TwilioRestException as e:
        return False, str(e)

def format_phone_number(phone):
    """Format phone number to E.164 format"""
    # Remove any non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone))
    
    # Add country code if it doesn't exist (assuming India +91 as default)
    if len(digits_only) == 10:  # Standard Indian phone without country code
        return f"+91{digits_only}"
    elif not digits_only.startswith("+"):
        return f"+{digits_only}"
    return digits_only

def show_notification_settings():
    """Display notification settings UI"""
    st.title("🔔 Notification Settings")
    
    st.markdown("""
    Configure notifications for different departments and events in the Voi Jeans ecosystem.
    SMS notifications will be sent to the designated personnel for each department.
    """)
    
    # Twilio Credentials Section
    st.subheader("Twilio Credentials Setup")
    
    # Initialize the twilio_credentials in session state if it doesn't exist
    if 'twilio_credentials' not in st.session_state:
        st.session_state.twilio_credentials = {
            'account_sid': os.environ.get("TWILIO_ACCOUNT_SID", ""),
            'auth_token': os.environ.get("TWILIO_AUTH_TOKEN", ""),
            'phone_number': os.environ.get("TWILIO_PHONE_NUMBER", "")
        }
    
    # Create a form for Twilio credentials
    with st.form("twilio_credentials_form"):
        st.markdown("""
        ### Set Twilio Credentials
        
        Configure the Twilio credentials to enable SMS notifications. These credentials 
        will be stored in the session state and used to send SMS notifications to the 
        department contacts.
        
        You can get these credentials by signing up at [Twilio](https://www.twilio.com/).
        """)
        
        account_sid = st.text_input(
            "Twilio Account SID", 
            value=st.session_state.twilio_credentials.get('account_sid', ''),
            placeholder="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Your Twilio Account SID (starts with 'AC')"
        )
        
        auth_token = st.text_input(
            "Twilio Auth Token", 
            value=st.session_state.twilio_credentials.get('auth_token', ''),
            type="password",
            placeholder="Enter your Twilio Auth Token",
            help="Your Twilio Auth Token (keep this secure)"
        )
        
        phone_number = st.text_input(
            "Twilio Phone Number", 
            value=st.session_state.twilio_credentials.get('phone_number', ''),
            placeholder="+1xxxxxxxxxx",
            help="Your Twilio Phone Number in E.164 format (+1XXXXXXXXXX)"
        )
        
        # Format the phone number
        if phone_number and not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        # Submit button
        submitted = st.form_submit_button("Save Credentials")
        
        if submitted:
            # Update session state with new values
            st.session_state.twilio_credentials['account_sid'] = account_sid
            st.session_state.twilio_credentials['auth_token'] = auth_token
            st.session_state.twilio_credentials['phone_number'] = phone_number
            
            # Check if credentials are valid
            if account_sid and auth_token and phone_number:
                st.success("Twilio credentials saved successfully!")
            else:
                st.warning("Some credentials are missing. SMS notifications may not work properly.")
    
    # Check if Twilio credentials are set
    if not check_twilio_credentials():
        st.warning("""
        ⚠️ Twilio credentials are not fully configured. SMS notifications will not be sent.
        Please provide all required Twilio credentials above.
        """)
    
    # Initialize notification settings in session state if not exists
    if 'notification_settings' not in st.session_state or not isinstance(st.session_state.notification_settings, dict):
        st.session_state.notification_settings = {
            "Design Team": {
                "enabled": True,
                "phone": "+919876543210",
                "events": ["New order created", "Sample approval required"]
            },
            "Production Planning": {
                "enabled": True,
                "phone": "+919876543211",
                "events": ["Material shortage", "Production delay", "Quality issue"]
            },
            "Scotts Garments": {
                "enabled": True,
                "phone": "+919876543212",
                "events": ["New production order", "Material received", "Production milestone"]
            },
            "Retail Operations": {
                "enabled": True,
                "phone": "+919876543213",
                "events": ["Low inventory alert", "New shipment received", "Sales target achieved"]
            },
            "Finance": {
                "enabled": True,
                "phone": "+919876543214",
                "events": ["Payment due", "Invoice generated", "Budget exception"]
            }
        }
    
    # Display department notification settings
    st.subheader("Department Notification Settings")
    
    # Create tabs for each department
    tabs = st.tabs(list(st.session_state.notification_settings.keys()))
    
    for i, (department, tab) in enumerate(zip(st.session_state.notification_settings.keys(), tabs)):
        with tab:
            settings = st.session_state.notification_settings[department]
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Enable/disable notifications for this department
                enabled = st.toggle("Enable Notifications", settings["enabled"], key=f"toggle_{department}")
                st.session_state.notification_settings[department]["enabled"] = enabled
            
            with col2:
                # Phone number input with formatting
                phone = st.text_input(
                    "Notification Phone Number", 
                    settings["phone"],
                    key=f"phone_{department}",
                    disabled=not enabled
                )
                
                # Format and save the phone number
                formatted_phone = format_phone_number(phone)
                if formatted_phone != phone:
                    st.info(f"Phone number will be formatted as: {formatted_phone}")
                
                st.session_state.notification_settings[department]["phone"] = formatted_phone
            
            # Event selection
            all_events = [
                "New order created",
                "Sample approval required",
                "Material shortage",
                "Production delay",
                "Quality issue",
                "New production order",
                "Material received",
                "Production milestone",
                "Low inventory alert",
                "New shipment received",
                "Sales target achieved",
                "Payment due",
                "Invoice generated",
                "Budget exception"
            ]
            
            selected_events = st.multiselect(
                "Events to Notify", 
                options=all_events,
                default=settings["events"],
                key=f"events_{department}",
                disabled=not enabled
            )
            
            st.session_state.notification_settings[department]["events"] = selected_events
            
            # Test notification
            if st.button("Test Notification", key=f"test_{department}", disabled=not enabled):
                if not check_twilio_credentials():
                    st.error("Cannot send test notification: Twilio credentials not configured.")
                else:
                    success, message = send_sms_notification(
                        formatted_phone,
                        f"This is a test notification for {department} from Voi Jeans Synergyze platform."
                    )
                    
                    if success:
                        st.success(f"Test notification sent to {formatted_phone}. Message SID: {message}")
                    else:
                        st.error(f"Failed to send test notification: {message}")
    
    # Event log section
    st.subheader("Notification Event Log")
    
    # Initialize notification log in session state if not exists
    if 'notification_log' not in st.session_state:
        st.session_state.notification_log = []
    
    # Display notification log
    if not st.session_state.notification_log:
        st.info("No notifications have been sent yet.")
    else:
        log_df = pd.DataFrame(st.session_state.notification_log)
        st.dataframe(log_df, use_container_width=True)

def send_department_notification(department, event, custom_message=None):
    """Send notification to a department based on an event"""
    if 'notification_settings' not in st.session_state:
        return False, "Notification settings not initialized"
    
    if department not in st.session_state.notification_settings:
        return False, f"Department {department} not found in notification settings"
    
    settings = st.session_state.notification_settings[department]
    
    if not settings["enabled"]:
        return False, f"Notifications are disabled for {department}"
    
    if event not in settings["events"]:
        return False, f"Event {event} is not configured for {department}"
    
    # Prepare message
    if custom_message:
        message = custom_message
    else:
        message = f"Voi Jeans notification for {department}: {event}"
    
    # Send notification
    phone = settings["phone"]
    success, result = send_sms_notification(phone, message)
    
    # Log notification
    if 'notification_log' not in st.session_state:
        st.session_state.notification_log = []
    
    st.session_state.notification_log.append({
        "timestamp": pd.Timestamp.now(),
        "department": department,
        "event": event,
        "phone": phone,
        "message": message,
        "status": "Sent" if success else "Failed",
        "details": result
    })
    
    return success, result

if __name__ == "__main__":
    show_notification_settings()