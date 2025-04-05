"""
ECG License Manager - License Issuance and Management System
===========================================================

This module implements the license management system for the Emperor's Computational Governance (ECG)
framework. It provides functionality for issuing, validating, and auditing licenses based on divine
principles and governance dimensions.

The module serves as the interface between the Emperor's governance directives and the operational
systems that implement them.
"""

import os
import json
import datetime
import hashlib
import uuid
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

from core.ecg_license_structure import (
    License, LicenseStatus, LicenseType, ComplianceTier,
    DivinePrinciple, GovernanceDimension, 
    DivinePrincipleCompliance, DimensionCompliance, ComplianceAudit,
    LicenseManager
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ecg_license_manager")

class ECGLicenseManager:
    """
    Singleton class for managing ECG licenses across the system.
    This is the primary interface for license operations in Empire OS.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ECGLicenseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.manager = LicenseManager()
        self.license_db_path = os.path.join("data", "licenses.json")
        self.audit_log_path = os.path.join("data", "audit_logs.json")
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.license_db_path), exist_ok=True)
        
        # Load existing licenses if available
        if os.path.exists(self.license_db_path):
            try:
                self.manager.load_licenses(self.license_db_path)
                logger.info(f"Loaded {len(self.manager.licenses)} licenses from database")
            except Exception as e:
                logger.error(f"Failed to load licenses: {e}")
        else:
            logger.info("No existing license database found. Starting with empty database.")
    
    def issue_new_license(
        self,
        entity_name: str,
        entity_id: str,
        license_type_str: str,
        validity_days: int,
        compliance_tier_str: str,
        modules: List[str],
        restrictions: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Issue a new license with the given parameters.
        Returns the license data as a dictionary.
        """
        # Initialize default values for optional parameters
        if restrictions is None:
            restrictions = []
        if metadata is None:
            metadata = {}
        try:
            # Convert string parameters to enum values
            license_type = LicenseType(license_type_str)
            compliance_tier = ComplianceTier(compliance_tier_str)
            
            # Calculate expiry date
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=validity_days)
            
            # Issue the license
            license = self.manager.issue_license(
                entity_name=entity_name,
                entity_id=entity_id,
                license_type=license_type,
                expiry_date=expiry_date,
                compliance_tier=compliance_tier,
                authorized_modules=modules,
                restrictions=restrictions,
                meta=metadata
            )
            
            # Save updated license database
            self._save_licenses()
            
            logger.info(f"Issued new license {license.license_id} to {entity_name}")
            
            # Return the license data
            return license.to_dict()
        
        except Exception as e:
            logger.error(f"Failed to issue license: {e}")
            raise
    
    def validate_license(self, license_id: str) -> Dict[str, Any]:
        """
        Validate a license and return the validation result.
        """
        try:
            is_valid, message = self.manager.validate_license(license_id)
            
            result = {
                "license_id": license_id,
                "is_valid": is_valid,
                "message": message,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # If license exists, add more details
            if license_id in self.manager.licenses:
                license = self.manager.licenses[license_id]
                result.update({
                    "entity_name": license.entity_name,
                    "status": license.status.value,
                    "compliance_score": license.current_compliance_score,
                    "expiry_date": license.expiry_date.isoformat()
                })
            
            # Log the validation
            self._log_license_validation(license_id, is_valid, message)
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to validate license {license_id}: {e}")
            return {
                "license_id": license_id,
                "is_valid": False,
                "message": f"Error during validation: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def perform_compliance_audit(
        self,
        license_id: str,
        auditor: str,
        dimension_scores: Dict[str, Dict[str, float]],
        findings: List[str],
        recommendations: List[str]
    ) -> Dict[str, Any]:
        """
        Perform a compliance audit for a license and return the audit results.
        
        dimension_scores: A nested dictionary mapping dimension names to principle scores
            e.g., {"people": {"justice": 85, "mercy": 90}, "planet": {...}}
        """
        try:
            # Validate input format
            self._validate_audit_input(dimension_scores)
            
            # Perform the audit
            audit = self.manager.perform_audit(
                license_id=license_id,
                auditor=auditor,
                dimension_scores=dimension_scores,
                findings=findings,
                recommendations=recommendations
            )
            
            # Save updated license database
            self._save_licenses()
            
            # Log the audit
            self._log_audit(license_id, audit)
            
            logger.info(f"Performed compliance audit for license {license_id}")
            
            return audit.to_dict()
        
        except Exception as e:
            logger.error(f"Failed to perform audit for license {license_id}: {e}")
            raise
    
    def get_license_details(self, license_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a license.
        """
        if license_id not in self.manager.licenses:
            logger.warning(f"License {license_id} not found")
            return {"error": f"License {license_id} not found"}
        
        license = self.manager.licenses[license_id]
        return license.to_dict()
    
    def list_all_licenses(self) -> List[Dict[str, Any]]:
        """
        List all licenses in the system with basic details.
        """
        result = []
        
        for license_id, license in self.manager.licenses.items():
            result.append({
                "license_id": license_id,
                "entity_name": license.entity_name,
                "entity_id": license.entity_id,
                "license_type": license.license_type.value,
                "status": license.status.value,
                "compliance_tier": license.compliance_tier.value,
                "compliance_score": license.current_compliance_score,
                "issue_date": license.issue_date.isoformat(),
                "expiry_date": license.expiry_date.isoformat()
            })
        
        return result
    
    def update_license_status(self, license_id: str, new_status_str: str) -> Dict[str, Any]:
        """
        Update the status of a license.
        """
        if license_id not in self.manager.licenses:
            logger.warning(f"License {license_id} not found")
            return {"error": f"License {license_id} not found"}
        
        try:
            new_status = LicenseStatus(new_status_str)
            license = self.manager.licenses[license_id]
            
            # Record the previous status for logging
            prev_status = license.status
            
            # Update the status
            license.status = new_status
            
            # Save updated license database
            self._save_licenses()
            
            logger.info(f"Updated license {license_id} status from {prev_status.value} to {new_status.value}")
            
            return {
                "license_id": license_id,
                "entity_name": license.entity_name,
                "previous_status": prev_status.value,
                "new_status": new_status.value,
                "timestamp": datetime.datetime.now().isoformat()
            }
        
        except ValueError:
            logger.error(f"Invalid status value: {new_status_str}")
            return {"error": f"Invalid status value: {new_status_str}"}
        
        except Exception as e:
            logger.error(f"Failed to update license status: {e}")
            return {"error": f"Failed to update license status: {str(e)}"}
    
    def get_compliance_history(self, license_id: str) -> List[Dict[str, Any]]:
        """
        Get the compliance audit history for a license.
        """
        if license_id not in self.manager.licenses:
            logger.warning(f"License {license_id} not found")
            return []
        
        license = self.manager.licenses[license_id]
        return [audit.to_dict() for audit in license.compliance_history]
    
    def _save_licenses(self) -> None:
        """
        Save all licenses to the database file.
        """
        try:
            self.manager.save_licenses(self.license_db_path)
            logger.info(f"Saved {len(self.manager.licenses)} licenses to database")
        except Exception as e:
            logger.error(f"Failed to save licenses: {e}")
            raise
    
    def _log_license_validation(self, license_id: str, is_valid: bool, message: str) -> None:
        """
        Log a license validation event.
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": "license_validation",
            "license_id": license_id,
            "is_valid": is_valid,
            "message": message
        }
        
        self._append_to_audit_log(log_entry)
    
    def _log_audit(self, license_id: str, audit: ComplianceAudit) -> None:
        """
        Log a compliance audit event.
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": "compliance_audit",
            "license_id": license_id,
            "audit_id": audit.audit_id,
            "auditor": audit.auditor,
            "overall_score": audit.overall_score
        }
        
        self._append_to_audit_log(log_entry)
    
    def _append_to_audit_log(self, log_entry: Dict[str, Any]) -> None:
        """
        Append an entry to the audit log.
        """
        try:
            # Load existing logs
            logs = []
            if os.path.exists(self.audit_log_path):
                with open(self.audit_log_path, 'r') as f:
                    logs = json.load(f)
            
            # Append new log entry
            logs.append(log_entry)
            
            # Save updated logs
            with open(self.audit_log_path, 'w') as f:
                json.dump(logs, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to append to audit log: {e}")
    
    def _validate_audit_input(self, dimension_scores: Dict[str, Dict[str, float]]) -> None:
        """
        Validate the format of dimension scores input for an audit.
        """
        # Check dimensions
        for dim_name in dimension_scores:
            try:
                GovernanceDimension(dim_name)
            except ValueError:
                valid_dims = [d.value for d in GovernanceDimension]
                raise ValueError(f"Invalid dimension: {dim_name}. Valid dimensions are: {valid_dims}")
            
            # Check principles for this dimension
            for principle_name in dimension_scores[dim_name]:
                try:
                    DivinePrinciple(principle_name)
                except ValueError:
                    valid_principles = [p.value for p in DivinePrinciple]
                    raise ValueError(f"Invalid principle: {principle_name}. Valid principles are: {valid_principles}")
                
                # Check score value
                score = dimension_scores[dim_name][principle_name]
                if not isinstance(score, (int, float)) or score < 0 or score > 100:
                    raise ValueError(f"Invalid score for {dim_name}.{principle_name}: {score}. Must be a number between 0 and 100.")

# Example usage in Empire OS
def sample_license_operations():
    """Demonstrate the usage of the ECG License Manager in Empire OS."""
    # Get the singleton instance
    license_manager = ECGLicenseManager()
    
    # Issue a new license
    new_license = license_manager.issue_new_license(
        entity_name="Voi Jeans Retail India Pvt Ltd",
        entity_id="VOI-JEANS-001",
        license_type_str="corporate",
        validity_days=365,
        compliance_tier_str="tier_3",
        modules=[
            "inventory_management",
            "supply_chain_optimization",
            "retail_analytics",
            "manufacturing_insights",
            "distribution_planning"
        ],
        restrictions=[
            "No modification of core governance algorithms",
            "Data must remain within authorized territories"
        ],
        metadata={
            "industry": "Retail & Manufacturing",
            "primary_contact": "John Doe",
            "region": "Asia-Pacific",
            "employees": 500
        }
    )
    
    license_id = new_license["license_id"]
    
    # Validate the license
    validation_result = license_manager.validate_license(license_id)
    
    # Perform a compliance audit
    audit_result = license_manager.perform_compliance_audit(
        license_id=license_id,
        auditor="Emperor's Governance Team",
        dimension_scores={
            "people": {
                "justice": 85,
                "mercy": 90,
                "all_knowing": 75
            },
            "planet": {
                "justice": 80,
                "mercy": 85,
                "all_knowing": 70
            },
            "profit": {
                "justice": 90,
                "mercy": 80,
                "all_knowing": 85
            }
        },
        findings=[
            "Strong commitment to ethical labor practices",
            "Environmental initiatives exceed industry standards",
            "Profit sharing mechanisms align with justice principles"
        ],
        recommendations=[
            "Enhance data collection for better visibility",
            "Implement advanced training on divine principles",
            "Extend governance practices to supplier network"
        ]
    )
    
    # Get license details
    license_details = license_manager.get_license_details(license_id)
    
    # Print results
    print(f"New License ID: {license_id}")
    print(f"Validation Result: {validation_result['is_valid']} - {validation_result['message']}")
    print(f"Audit Score: {audit_result['overall_score']}")
    
    return license_details

if __name__ == "__main__":
    # Run the example operations
    license_details = sample_license_operations()
    print(json.dumps(license_details, indent=2))