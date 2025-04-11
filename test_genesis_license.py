#!/usr/bin/env python3
"""
Genesis Stack License API Test Client

This script tests the Genesis Stack License API by creating, retrieving,
verifying, and managing licenses.
"""

import requests
import json
import time
import argparse
from datetime import datetime

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Genesis Stack License API Test Client")
    
    parser.add_argument(
        "--host", 
        default="localhost",
        help="API host (default: localhost)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=5001,
        help="API port (default: 5001)"
    )
    
    parser.add_argument(
        "--api-key",
        default="emperorkey123",
        help="API key for authentication"
    )
    
    return parser.parse_args()

class GenesisLicenseClient:
    """Client for interacting with the Genesis License API"""
    
    def __init__(self, host, port, api_key):
        """Initialize the client with connection details"""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}/api/v1"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def health_check(self):
        """Check if the API is healthy"""
        url = f"http://{self.host}:{self.port}/health"
        response = requests.get(url)
        return response.json()
    
    def create_license(self, license_type, holder, permissions, validity_days=None, metadata=None):
        """Create a new license"""
        url = f"{self.base_url}/licenses"
        
        data = {
            "type": license_type,
            "holder": holder,
            "permissions": permissions
        }
        
        if validity_days:
            data["validity_days"] = validity_days
            
        if metadata:
            data["metadata"] = metadata
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_license(self, license_id):
        """Get a license by ID"""
        url = f"{self.base_url}/licenses/{license_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def verify_license(self, license_id):
        """Verify a license by ID"""
        url = f"{self.base_url}/licenses/{license_id}/verify"
        response = requests.post(url, headers=self.headers)
        return response.json()
    
    def update_license(self, license_id, updates):
        """Update a license by ID"""
        url = f"{self.base_url}/licenses/{license_id}"
        response = requests.patch(url, json=updates, headers=self.headers)
        return response.json()
    
    def revoke_license(self, license_id, reason):
        """Revoke a license by ID"""
        url = f"{self.base_url}/licenses/{license_id}/revoke"
        data = {"reason": reason}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def renew_license(self, license_id, validity_days=None):
        """Renew a license by ID"""
        url = f"{self.base_url}/licenses/{license_id}/renew"
        data = {}
        if validity_days:
            data["validity_days"] = validity_days
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def check_renewal_needed(self, license_id):
        """Check if a license needs renewal"""
        url = f"{self.base_url}/licenses/{license_id}/check-renewal"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_license_key(self, license_id):
        """Get the license key for a license"""
        url = f"{self.base_url}/licenses/{license_id}/key"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def verify_license_key(self, license_id, license_key):
        """Verify a license key against a license ID"""
        url = f"{self.base_url}/licenses/{license_id}/verify-key"
        data = {"license_key": license_key}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def list_licenses(self, filters=None):
        """List licenses with optional filtering"""
        url = f"{self.base_url}/licenses"
        
        params = {}
        if filters:
            params.update(filters)
        
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()
    
    def list_license_types(self):
        """List available license types"""
        url = f"{self.base_url}/license-types"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_divine_governance(self):
        """Get information about divine governance"""
        url = f"{self.base_url}/divine-governance"
        response = requests.get(url, headers=self.headers)
        return response.json()

def print_section(title):
    """Print a section title"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_json(data):
    """Print JSON data in a formatted way"""
    print(json.dumps(data, indent=2))

def main():
    """Main function to test the license API"""
    args = parse_arguments()
    
    # Create client
    client = GenesisLicenseClient(args.host, args.port, args.api_key)
    
    # Health check
    print_section("Health Check")
    health = client.health_check()
    print_json(health)
    
    # Get divine governance information
    print_section("Divine Governance Information")
    governance = client.get_divine_governance()
    print_json(governance)
    
    # Get available license types
    print_section("Available License Types")
    license_types = client.list_license_types()
    print_json(license_types)
    
    # Create a VOI Jeans Enterprise license
    print_section("Creating VOI Jeans Enterprise License")
    voi_license = client.create_license(
        license_type="enterprise",
        holder={
            "id": "VOI-JEANS-001",
            "name": "VOI Jeans Retail India PVT LTD",
            "contact": "admin@voijeans.com"
        },
        permissions=[
            "transaction_governance",
            "channel_management",
            "inventory_sync", 
            "financial_reporting",
            "compliance_management"
        ],
        validity_days=365,
        metadata={
            "organization_size": "Enterprise",
            "industry": "Retail",
            "region": "Asia",
            "country": "India"
        }
    )
    print_json(voi_license)
    
    # Store license ID and key for later use
    license_id = voi_license["license"]["id"]
    license_key = voi_license["license_key"]
    
    print(f"\nCreated license ID: {license_id}")
    print(f"License Key: {license_key}")
    
    # Wait a moment before continuing
    time.sleep(1)
    
    # Get the license details
    print_section("License Details")
    license_details = client.get_license(license_id)
    print_json(license_details)
    
    # Verify the license
    print_section("License Verification")
    verification = client.verify_license(license_id)
    print_json(verification)
    
    # Verify the license key
    print_section("License Key Verification")
    key_verification = client.verify_license_key(license_id, license_key)
    print_json(key_verification)
    
    # Update the license
    print_section("Updating License")
    updated_license = client.update_license(license_id, {
        "metadata": {
            "organization_size": "Enterprise",
            "industry": "Retail",
            "region": "Asia",
            "country": "India",
            "stores": 25,
            "employees": 500
        }
    })
    print_json(updated_license)
    
    # Check if renewal is needed
    print_section("Renewal Check")
    renewal_check = client.check_renewal_needed(license_id)
    print_json(renewal_check)
    
    # List all licenses
    print_section("All Licenses")
    all_licenses = client.list_licenses()
    print_json(all_licenses)
    
    # Renew the license
    print_section("Renewing License")
    renewed_license = client.renew_license(license_id, validity_days=730)  # 2 years
    print_json(renewed_license)
    
    # Optionally revoke the license
    if False:  # Set to True to test revocation
        print_section("Revoking License")
        revoked_license = client.revoke_license(license_id, "License terms violation")
        print_json(revoked_license)
    
    print("\nLicense API Test Completed Successfully!")

if __name__ == "__main__":
    main()