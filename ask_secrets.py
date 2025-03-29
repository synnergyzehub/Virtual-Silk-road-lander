import streamlit as st
import threading
import time

def ask_secrets_async(secret_keys, user_message):
    """
    Asynchronously ask for secrets by creating a separate thread that will call ask_secrets
    
    Args:
        secret_keys: List of secret keys to request
        user_message: Message to show to the user explaining why these secrets are needed
    """
    if not isinstance(secret_keys, list):
        secret_keys = [secret_keys]
    
    # Create and start a new thread to ask for secrets
    thread = threading.Thread(
        target=_ask_secrets_thread,
        args=(secret_keys, user_message),
        daemon=True
    )
    thread.start()
    
    return True

def _ask_secrets_thread(secret_keys, user_message):
    """
    Thread function to ask for secrets after a short delay
    
    Args:
        secret_keys: List of secret keys to request
        user_message: Message to show to the user explaining why these secrets are needed
    """
    # Wait a moment to avoid race conditions with the main thread
    time.sleep(1)
    
    # This will trigger the ask_secrets widget
    st.experimental_user_chat_message("I need to set up SMS notifications.")
    
    # Import and call the ask_secrets function for the actual secrets request
    try:
        from streamlit_extensions import ask_secrets
        ask_secrets(secret_keys=secret_keys, user_message=user_message)
    except Exception as e:
        st.error(f"Failed to request secrets: {str(e)}")