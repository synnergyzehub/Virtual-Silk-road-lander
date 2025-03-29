import streamlit as st

# Force navigation to the notification settings page
st.session_state.page = 'notification_settings'

# Reload the page
st.rerun()