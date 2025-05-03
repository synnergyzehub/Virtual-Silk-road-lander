#!/usr/bin/env python3
"""
Genesis Stack License API Runner

Script to start the Genesis Stack license API service.
"""

import os
import argparse
import logging
from genesis_license_api import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("license_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("license_api_runner")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Genesis Stack License API Runner")
    
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host to run the server on (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=5001,
        help="Port to run the server on (default: 5001)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Run in debug mode"
    )
    
    parser.add_argument(
        "--api-key",
        help="API key for authentication (default: from environment variable)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Set environment variables from arguments
    if args.api_key:
        os.environ["GENESIS_API_KEY"] = args.api_key
        
    # Log startup information
    logger.info(f"Starting Secure Empire License API on port {args.port}...")
    
    # Run the application
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

if __name__ == "__main__":
    main()