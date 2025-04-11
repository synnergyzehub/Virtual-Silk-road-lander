"""
Genesis Stack License Manager

Core module for the Genesis Stack licensing system, providing license creation,
validation, and management capabilities with divine governance integration.
"""

import os
import json
import uuid
import hashlib
import hmac
import base64
import datetime
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from enum import Enum
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("genesis_license.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("genesis_license")

# License status enumeration
class LicenseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"
    SUSPENDED = "suspended"

# License type enumeration
class LicenseType(str, Enum):
    ENTERPRISE = "enterprise"
    REGIONAL = "regional"
    COUNTRY = "country"
    DIVISION = "division"
    SUBSIDIARY = "subsidiary"
    
    SYNNERGYZE_OS = "synnergyze_os"
    WOVEN_SUPPLY = "woven_supply"
    COMMUNE_CONNECT = "commune_connect"
    VIRTUAL_SILK_ROAD = "virtual_silk_road"
    RIVER_OS = "river_os"
    
    DIVINE_GOVERNANCE = "divine_governance"
    WTO_COMPLIANCE = "wto_compliance"
    FEDERAL_ALIGNMENT = "federal_alignment"
    EMPEROR_OVERSIGHT = "emperor_oversight"
    INTEGRATION_HUB = "integration_hub"
    
    DEVELOPMENT = "development"
    EDUCATIONAL = "educational"
    COMMUNITY = "community"
    EVALUATION = "evaluation"
    PARTNER = "partner"

# Governance level enumeration
class GovernanceLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    ENHANCED = "enhanced"
    MAXIMUM = "maximum"

# License manager class
class GenesisLicenseManager:
    """
    Core license management system for the Genesis Stack.
    Handles license creation, validation, and management with divine governance.
    """
    
    def __init__(self, config_file: Optional[str] = None, storage_dir: Optional[str] = None):
        """
        Initialize the Genesis License Manager.
        
        Args:
            config_file: Optional path to configuration file
            storage_dir: Optional directory for license storage
        """
        # Default configuration
        self.config = {
            "secret_key": os.environ.get("GENESIS_LICENSE_SECRET", "emperorkey123"),
            "license_version": "1.0",
            "default_validity_days": 365,
            "min_divine_alignment": 80.0,
            "governance_level": GovernanceLevel.ENHANCED,
            "verification_interval": 86400,  # 24 hours in seconds
            "require_divine_verification": True,
            "auto_renew_threshold_days": 30,
            "license_format": "genesis_v1",
            "wto_compliance": True
        }
        
        # Load configuration from file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        
        # Set up storage directory
        self.storage_dir = storage_dir or os.path.join(os.getcwd(), "licenses")
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Load existing licenses
        self.licenses = {}
        self._load_licenses()
        
        logger.info(f"Genesis License Manager initialized with {len(self.licenses)} licenses")
    
    def _load_licenses(self) -> None:
        """Load all licenses from the storage directory."""
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.storage_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            license_data = json.load(f)
                            license_id = license_data.get('id')
                            if license_id:
                                self.licenses[license_id] = license_data
                    except Exception as e:
                        logger.error(f"Error loading license from {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading licenses: {str(e)}")
    
    def _save_license(self, license_data: Dict) -> bool:
        """
        Save a license to storage.
        
        Args:
            license_data: License data to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            license_id = license_data.get('id')
            if not license_id:
                logger.error("Cannot save license without ID")
                return False
            
            file_path = os.path.join(self.storage_dir, f"{license_id}.json")
            with open(file_path, 'w') as f:
                json.dump(license_data, f, indent=2)
            
            # Update in-memory cache
            self.licenses[license_id] = license_data
            
            logger.info(f"Saved license {license_id} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving license: {str(e)}")
            return False
    
    def _generate_license_id(self) -> str:
        """
        Generate a unique license ID.
        
        Returns:
            str: Unique license ID
        """
        return f"GEN-{uuid.uuid4()}"
    
    def _calculate_signature(self, license_data: Dict) -> str:
        """
        Calculate a cryptographic signature for a license.
        
        Args:
            license_data: License data to sign
            
        Returns:
            str: Base64-encoded signature
        """
        # Create a copy without the signature field
        data_to_sign = license_data.copy()
        data_to_sign.pop('signature', None)
        
        # Convert to stable string representation
        data_string = json.dumps(data_to_sign, sort_keys=True)
        
        # Create HMAC signature using secret key
        key = self.config["secret_key"].encode('utf-8')
        h = hmac.new(key, data_string.encode('utf-8'), hashlib.sha256)
        
        # Return base64 encoded signature
        return base64.b64encode(h.digest()).decode('utf-8')
    
    def _verify_signature(self, license_data: Dict) -> bool:
        """
        Verify the cryptographic signature of a license.
        
        Args:
            license_data: License data with signature to verify
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if 'signature' not in license_data:
            return False
        
        expected_signature = license_data['signature']
        actual_signature = self._calculate_signature(license_data)
        
        return hmac.compare_digest(expected_signature, actual_signature)
    
    def _calculate_divine_alignment(self, license_data: Dict) -> float:
        """
        Calculate the divine alignment score for a license.
        
        Args:
            license_data: License data to evaluate
            
        Returns:
            float: Divine alignment score (0-100)
        """
        # Base alignment score - default is high for official licenses
        alignment = 90.0
        
        # Adjust based on license attributes
        if license_data.get('type') == LicenseType.DEVELOPMENT:
            alignment -= 5  # Development licenses have slightly lower divine alignment
        
        if license_data.get('governance_level') == GovernanceLevel.MAXIMUM:
            alignment += 5  # Maximum governance has higher alignment
        elif license_data.get('governance_level') == GovernanceLevel.BASIC:
            alignment -= 5  # Basic governance has lower alignment
        
        # Check for ethical compliance components
        if license_data.get('wto_compliance') is True:
            alignment += 2
        
        if 'permissions' in license_data:
            permissions = license_data['permissions']
            # More permissions slightly reduce alignment due to complexity
            if len(permissions) > 10:
                alignment -= 2
        
        # Ensure score is within bounds
        alignment = max(0, min(100, alignment))
        
        return alignment
    
    def _is_license_valid(self, license_data: Dict) -> Tuple[bool, str]:
        """
        Check if a license is valid.
        
        Args:
            license_data: License data to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, reason)
        """
        # Check if license has all required fields
        required_fields = ['id', 'type', 'issuer', 'holder', 'issued_at', 'expires_at', 'signature']
        for field in required_fields:
            if field not in license_data:
                return False, f"Missing required field: {field}"
        
        # Verify signature
        if not self._verify_signature(license_data):
            return False, "Invalid signature"
        
        # Check expiration
        expires_at = datetime.datetime.fromisoformat(license_data['expires_at'].replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        if expires_at < now:
            return False, "License expired"
        
        # Check status
        if license_data.get('status') != LicenseStatus.ACTIVE:
            return False, f"License status is {license_data.get('status')}"
        
        # Check divine alignment if required
        if self.config["require_divine_verification"]:
            verification = license_data.get('divine_verification', {})
            alignment = verification.get('alignment_score', 0)
            
            if alignment < self.config["min_divine_alignment"]:
                return False, f"Divine alignment too low: {alignment}"
            
            # Check verification timestamp if available
            if 'verification_timestamp' in verification:
                verification_time = datetime.datetime.fromisoformat(
                    verification['verification_timestamp'].replace('Z', '+00:00')
                )
                verification_age = (now - verification_time).total_seconds()
                
                if verification_age > self.config["verification_interval"]:
                    return False, "Divine verification expired"
        
        return True, "License is valid"
    
    def create_license(self, license_type: Union[LicenseType, str], holder: Dict, 
                     validity_days: Optional[int] = None,
                     permissions: Optional[List[str]] = None,
                     metadata: Optional[Dict] = None) -> Dict:
        """
        Create a new license.
        
        Args:
            license_type: Type of license to create
            holder: Information about the license holder
            validity_days: Number of days the license is valid for (default: config value)
            permissions: List of permission identifiers
            metadata: Additional license metadata
            
        Returns:
            Dict: Created license data
        """
        # Convert string license type to enum if needed
        if isinstance(license_type, str):
            license_type = LicenseType(license_type)
        
        # Generate a unique license ID
        license_id = self._generate_license_id()
        
        # Calculate validity period
        validity_days = validity_days or self.config["default_validity_days"]
        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = now + datetime.timedelta(days=validity_days)
        
        # Create license data
        license_data = {
            'id': license_id,
            'type': license_type,
            'format': self.config["license_format"],
            'version': self.config["license_version"],
            'issuer': {
                'name': "Genesis Ecosystem",
                'id': "GENESIS-ISSUER-001"
            },
            'holder': holder,
            'status': LicenseStatus.ACTIVE,
            'issued_at': now.isoformat(),
            'expires_at': expires_at.isoformat(),
            'permissions': permissions or [],
            'governance_level': self.config["governance_level"],
            'wto_compliance': self.config["wto_compliance"],
            'metadata': metadata or {}
        }
        
        # Add divine verification
        license_data['divine_verification'] = {
            'alignment_score': self._calculate_divine_alignment(license_data),
            'verification_timestamp': now.isoformat(),
            'verification_authority': "Divine Governance Layer"
        }
        
        # Add signature
        license_data['signature'] = self._calculate_signature(license_data)
        
        # Save the license
        self._save_license(license_data)
        
        logger.info(f"Created license {license_id} of type {license_type} for {holder.get('name')}")
        
        return license_data
    
    def verify_license(self, license_id: str) -> Dict:
        """
        Verify a license by ID.
        
        Args:
            license_id: ID of the license to verify
            
        Returns:
            Dict: Verification result
        """
        # Check if license exists
        if license_id not in self.licenses:
            return {
                'valid': False,
                'reason': "License not found",
                'license_id': license_id
            }
        
        license_data = self.licenses[license_id]
        
        # Check license validity
        is_valid, reason = self._is_license_valid(license_data)
        
        # Perform divine verification
        now = datetime.datetime.now(datetime.timezone.utc)
        divine_alignment = self._calculate_divine_alignment(license_data)
        
        # Update divine verification data
        license_data['divine_verification'] = {
            'alignment_score': divine_alignment,
            'verification_timestamp': now.isoformat(),
            'verification_authority': "Divine Governance Layer"
        }
        
        # Check if alignment meets threshold
        if divine_alignment < self.config["min_divine_alignment"]:
            is_valid = False
            reason = f"Divine alignment too low: {divine_alignment}"
        
        # Save the updated license with fresh verification
        self._save_license(license_data)
        
        logger.info(f"Verified license {license_id}: valid={is_valid}, reason={reason}")
        
        # Create verification result
        verification_result = {
            'valid': is_valid,
            'reason': reason,
            'license_id': license_id,
            'license_type': license_data['type'],
            'holder': license_data['holder'],
            'expires_at': license_data['expires_at'],
            'divine_alignment': divine_alignment,
            'verification_timestamp': now.isoformat()
        }
        
        return verification_result
    
    def get_license(self, license_id: str) -> Optional[Dict]:
        """
        Get a license by ID.
        
        Args:
            license_id: ID of the license to retrieve
            
        Returns:
            Optional[Dict]: License data or None if not found
        """
        return self.licenses.get(license_id)
    
    def update_license(self, license_id: str, updates: Dict) -> Optional[Dict]:
        """
        Update a license by ID.
        
        Args:
            license_id: ID of the license to update
            updates: Dictionary of fields to update
            
        Returns:
            Optional[Dict]: Updated license data or None if not found/error
        """
        # Check if license exists
        if license_id not in self.licenses:
            logger.error(f"License {license_id} not found for update")
            return None
        
        # Get current license data
        license_data = self.licenses[license_id].copy()
        
        # Fields that cannot be updated
        protected_fields = ['id', 'issued_at', 'issuer', 'signature', 'format', 'version']
        
        # Apply updates
        for key, value in updates.items():
            if key in protected_fields:
                logger.warning(f"Attempted to update protected field: {key}")
                continue
            
            license_data[key] = value
        
        # Update divine verification
        now = datetime.datetime.now(datetime.timezone.utc)
        license_data['divine_verification'] = {
            'alignment_score': self._calculate_divine_alignment(license_data),
            'verification_timestamp': now.isoformat(),
            'verification_authority': "Divine Governance Layer"
        }
        
        # Update signature
        license_data['signature'] = self._calculate_signature(license_data)
        
        # Save the updated license
        if self._save_license(license_data):
            logger.info(f"Updated license {license_id}")
            return license_data
        else:
            logger.error(f"Failed to save updated license {license_id}")
            return None
    
    def revoke_license(self, license_id: str, reason: str) -> bool:
        """
        Revoke a license by ID.
        
        Args:
            license_id: ID of the license to revoke
            reason: Reason for revocation
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if license exists
        if license_id not in self.licenses:
            logger.error(f"License {license_id} not found for revocation")
            return False
        
        # Get current license data
        license_data = self.licenses[license_id].copy()
        
        # Update status and add revocation info
        license_data['status'] = LicenseStatus.REVOKED
        license_data['revocation'] = {
            'reason': reason,
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        # Update divine verification
        now = datetime.datetime.now(datetime.timezone.utc)
        license_data['divine_verification'] = {
            'alignment_score': self._calculate_divine_alignment(license_data),
            'verification_timestamp': now.isoformat(),
            'verification_authority': "Divine Governance Layer"
        }
        
        # Update signature
        license_data['signature'] = self._calculate_signature(license_data)
        
        # Save the updated license
        if self._save_license(license_data):
            logger.info(f"Revoked license {license_id}: {reason}")
            return True
        else:
            logger.error(f"Failed to save revoked license {license_id}")
            return False
    
    def list_licenses(self, filter_params: Optional[Dict] = None) -> List[Dict]:
        """
        List licenses with optional filtering.
        
        Args:
            filter_params: Optional parameters to filter licenses
            
        Returns:
            List[Dict]: List of matching licenses
        """
        results = []
        
        # Apply filters if provided
        if filter_params:
            for license_id, license_data in self.licenses.items():
                match = True
                
                for key, value in filter_params.items():
                    # Special handling for nested fields
                    if '.' in key:
                        parts = key.split('.')
                        obj = license_data
                        for part in parts[:-1]:
                            if part in obj:
                                obj = obj[part]
                            else:
                                match = False
                                break
                        
                        if match and parts[-1] in obj and obj[parts[-1]] != value:
                            match = False
                    
                    # Direct field comparison
                    elif key in license_data and license_data[key] != value:
                        match = False
                
                if match:
                    results.append(license_data)
        else:
            # No filters, return all licenses
            results = list(self.licenses.values())
        
        logger.info(f"Listed {len(results)} licenses")
        return results
    
    def check_renewal_needed(self, license_id: str) -> Dict:
        """
        Check if a license needs renewal.
        
        Args:
            license_id: ID of the license to check
            
        Returns:
            Dict: Renewal status information
        """
        # Check if license exists
        if license_id not in self.licenses:
            return {
                'license_id': license_id,
                'renewal_needed': False,
                'reason': "License not found"
            }
        
        license_data = self.licenses[license_id]
        
        # Check expiration date
        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = datetime.datetime.fromisoformat(license_data['expires_at'].replace('Z', '+00:00'))
        days_until_expiry = (expires_at - now).days
        
        renewal_threshold = self.config["auto_renew_threshold_days"]
        renewal_needed = days_until_expiry <= renewal_threshold
        
        return {
            'license_id': license_id,
            'renewal_needed': renewal_needed,
            'days_until_expiry': days_until_expiry,
            'renewal_threshold': renewal_threshold,
            'expires_at': license_data['expires_at']
        }
    
    def renew_license(self, license_id: str, validity_days: Optional[int] = None) -> Optional[Dict]:
        """
        Renew a license by extending its expiration date.
        
        Args:
            license_id: ID of the license to renew
            validity_days: Number of days to extend the license by (default: config value)
            
        Returns:
            Optional[Dict]: Renewed license data or None if not found/error
        """
        # Check if license exists
        if license_id not in self.licenses:
            logger.error(f"License {license_id} not found for renewal")
            return None
        
        # Get current license data
        license_data = self.licenses[license_id].copy()
        
        # Calculate new expiration date
        validity_days = validity_days or self.config["default_validity_days"]
        
        # Determine starting point for renewal
        expires_at = datetime.datetime.fromisoformat(license_data['expires_at'].replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # If already expired, start from now; otherwise extend from current expiration
        if expires_at < now:
            new_expires_at = now + datetime.timedelta(days=validity_days)
        else:
            new_expires_at = expires_at + datetime.timedelta(days=validity_days)
        
        # Update license data
        license_data['expires_at'] = new_expires_at.isoformat()
        license_data['status'] = LicenseStatus.ACTIVE  # Ensure status is active
        
        # Add renewal information
        if 'renewals' not in license_data:
            license_data['renewals'] = []
        
        license_data['renewals'].append({
            'timestamp': now.isoformat(),
            'previous_expiry': expires_at.isoformat(),
            'new_expiry': new_expires_at.isoformat()
        })
        
        # Update divine verification
        license_data['divine_verification'] = {
            'alignment_score': self._calculate_divine_alignment(license_data),
            'verification_timestamp': now.isoformat(),
            'verification_authority': "Divine Governance Layer"
        }
        
        # Update signature
        license_data['signature'] = self._calculate_signature(license_data)
        
        # Save the updated license
        if self._save_license(license_data):
            logger.info(f"Renewed license {license_id} until {new_expires_at.isoformat()}")
            return license_data
        else:
            logger.error(f"Failed to save renewed license {license_id}")
            return None
    
    def generate_license_key(self, license_id: str) -> str:
        """
        Generate a license key for a given license ID.
        
        Args:
            license_id: ID of the license
            
        Returns:
            str: License key
        """
        if license_id not in self.licenses:
            logger.error(f"License {license_id} not found for key generation")
            raise ValueError(f"License {license_id} not found")
        
        license_data = self.licenses[license_id]
        
        # Create a string with key license info
        key_base = f"{license_id}:{license_data['holder']['id']}:{license_data['expires_at']}"
        
        # Apply HMAC with the secret key
        key = self.config["secret_key"].encode('utf-8')
        h = hmac.new(key, key_base.encode('utf-8'), hashlib.sha256)
        digest = h.digest()
        
        # Encode with base64 and format for readability
        encoded = base64.b64encode(digest).decode('utf-8')
        formatted_key = f"GEN-{encoded[:12]}-{encoded[12:24]}-{encoded[24:36]}-{encoded[36:48]}"
        
        return formatted_key
    
    def verify_license_key(self, license_id: str, license_key: str) -> bool:
        """
        Verify a license key against a license ID.
        
        Args:
            license_id: ID of the license
            license_key: License key to verify
            
        Returns:
            bool: True if the key is valid, False otherwise
        """
        try:
            # Generate the expected key
            expected_key = self.generate_license_key(license_id)
            
            # Compare with provided key
            return hmac.compare_digest(expected_key, license_key)
        except Exception as e:
            logger.error(f"Error verifying license key: {str(e)}")
            return False


# Main execution
if __name__ == "__main__":
    # Create license manager
    license_manager = GenesisLicenseManager()
    
    # Create a sample license
    sample_license = license_manager.create_license(
        license_type=LicenseType.ENTERPRISE,
        holder={
            "id": "VOI-JEANS-001",
            "name": "VOI Jeans Retail India PVT LTD",
            "contact": "admin@voijeans.com"
        },
        validity_days=365,
        permissions=[
            "transaction_governance",
            "channel_management",
            "inventory_sync",
            "financial_reporting",
            "compliance_management"
        ],
        metadata={
            "organization_size": "Enterprise",
            "industry": "Retail",
            "region": "Asia",
            "country": "India"
        }
    )
    
    # Print the created license
    print(f"Created license: {sample_license['id']}")
    
    # Verify the license
    verification = license_manager.verify_license(sample_license['id'])
    print(f"License verification: {verification['valid']} - {verification['reason']}")
    
    # Generate license key
    license_key = license_manager.generate_license_key(sample_license['id'])
    print(f"License key: {license_key}")