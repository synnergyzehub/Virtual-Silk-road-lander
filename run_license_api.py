"""
Run Script for Secure Empire License API

This script starts the secure license API server on port 5001.
"""

import os
import sys
import subprocess

# Set the API key for testing
os.environ["EMPIRE_API_KEY"] = "emperorkey123"

def main():
    """Start the license API server"""
    print("Starting Secure Empire License API on port 5001...")
    
    try:
        # Run the server
        subprocess.run(["python", "secure_empire_license_api.py"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())