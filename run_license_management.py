"""
Run Script for License Management Interface

This script starts the license management Streamlit interface on port 8505.
"""

import os
import sys
import subprocess

# Set the API key for testing
os.environ["EMPIRE_API_KEY"] = "emperorkey123"

def main():
    """Start the license management interface"""
    print("Starting License Management Interface on port 8505...")
    
    try:
        # Run the Streamlit app
        subprocess.run(["streamlit", "run", "license_management.py", "--server.port", "8505"], check=True)
    except KeyboardInterrupt:
        print("\nInterface stopped by user.")
    except Exception as e:
        print(f"Error starting interface: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())