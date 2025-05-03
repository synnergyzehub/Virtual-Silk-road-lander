"""
ECG License API - Simplified Interface for License Operations
============================================================

This module provides a simplified API for interacting with the ECG License system.
It abstracts away the complexities of the underlying implementation and provides
a clean, easy-to-use interface for applications built on Empire OS.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from .ecg_license_manager import ECGLicenseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("license_api")

class LicenseAPI:
    """
    A simplified API for interacting with the ECG License system.
    This class provides a clean interface for applications to perform
    license operations without dealing with the underlying complexities.
    """
    
    @staticmethod
    def get_manager() -> ECGLicenseManager:
        """Get the ECG License Manager singleton instance"""
        return ECGLicenseManager()
    
    @staticmethod
    def issue_license(
        entity_name: str,
        entity_id: str,
        license_type: str,
        validity_days: int,
        compliance_tier: str,
        modules: List[str],
        restrictions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Issue a new license with the given parameters.
        
        Parameters:
        -----------
        entity_name : str
            Name of the entity receiving the license
        entity_id : str
            Unique identifier for the entity
        license_type : str
            Type of license (corporate, individual, government, etc.)
        validity_days : int
            Number of days the license is valid for
        compliance_tier : str
            Compliance tier (tier_1, tier_2, etc.)
        modules : List[str]
            List of authorized modules/features
        restrictions : List[str], optional
            List of restrictions on the license
        metadata : Dict[str, Any], optional
            Additional metadata for the license
            
        Returns:
        --------
        Dict[str, Any]
            The newly issued license data
        """
        try:
            manager = LicenseAPI.get_manager()
            
            # Handle optional parameters
            restrictions_param = restrictions if restrictions is not None else []
            metadata_param = metadata if metadata is not None else {}
            
            return manager.issue_new_license(
                entity_name=entity_name,
                entity_id=entity_id,
                license_type_str=license_type,
                validity_days=validity_days,
                compliance_tier_str=compliance_tier,
                modules=modules,
                restrictions=restrictions_param,
                metadata=metadata_param
            )
        except Exception as e:
            logger.error(f"Failed to issue license: {e}")
            raise
    
    @staticmethod
    def validate_license(license_id: str) -> Dict[str, Any]:
        """
        Validate a license and return the validation result.
        
        Parameters:
        -----------
        license_id : str
            The ID of the license to validate
            
        Returns:
        --------
        Dict[str, Any]
            Validation result containing is_valid, message, and other details
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.validate_license(license_id)
        except Exception as e:
            logger.error(f"Failed to validate license: {e}")
            return {
                "license_id": license_id,
                "is_valid": False,
                "message": f"Error during validation: {str(e)}",
                "timestamp": "N/A"
            }
    
    @staticmethod
    def perform_audit(
        license_id: str,
        auditor: str,
        dimension_scores: Dict[str, Dict[str, float]],
        findings: List[str],
        recommendations: List[str]
    ) -> Dict[str, Any]:
        """
        Perform a compliance audit for a license.
        
        Parameters:
        -----------
        license_id : str
            The ID of the license to audit
        auditor : str
            Name of the person/system performing the audit
        dimension_scores : Dict[str, Dict[str, float]]
            A nested dictionary mapping dimension names to principle scores
            e.g., {"people": {"justice": 85, "mercy": 90}, "planet": {...}}
        findings : List[str]
            List of audit findings
        recommendations : List[str]
            List of recommendations based on the audit
            
        Returns:
        --------
        Dict[str, Any]
            The audit results
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.perform_compliance_audit(
                license_id=license_id,
                auditor=auditor,
                dimension_scores=dimension_scores,
                findings=findings,
                recommendations=recommendations
            )
        except Exception as e:
            logger.error(f"Failed to perform audit: {e}")
            raise
    
    @staticmethod
    def get_license_details(license_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a license.
        
        Parameters:
        -----------
        license_id : str
            The ID of the license to get details for
            
        Returns:
        --------
        Dict[str, Any]
            Detailed license information or error message if not found
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.get_license_details(license_id)
        except Exception as e:
            logger.error(f"Failed to get license details: {e}")
            return {"error": f"Failed to get license details: {str(e)}"}
    
    @staticmethod
    def list_licenses() -> List[Dict[str, Any]]:
        """
        List all licenses in the system with basic details.
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of licenses with basic details
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.list_all_licenses()
        except Exception as e:
            logger.error(f"Failed to list licenses: {e}")
            return []
    
    @staticmethod
    def update_license_status(license_id: str, new_status: str) -> Dict[str, Any]:
        """
        Update the status of a license.
        
        Parameters:
        -----------
        license_id : str
            The ID of the license to update
        new_status : str
            New status (pending, active, suspended, revoked, expired)
            
        Returns:
        --------
        Dict[str, Any]
            Result of the update operation
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.update_license_status(license_id, new_status)
        except Exception as e:
            logger.error(f"Failed to update license status: {e}")
            return {"error": f"Failed to update license status: {str(e)}"}
    
    @staticmethod
    def get_compliance_history(license_id: str) -> List[Dict[str, Any]]:
        """
        Get the compliance audit history for a license.
        
        Parameters:
        -----------
        license_id : str
            The ID of the license to get compliance history for
            
        Returns:
        --------
        List[Dict[str, Any]]
            List of compliance audits for the license
        """
        try:
            manager = LicenseAPI.get_manager()
            return manager.get_compliance_history(license_id)
        except Exception as e:
            logger.error(f"Failed to get compliance history: {e}")
            return []
    
    @staticmethod
    def get_license_status_distribution() -> Dict[str, int]:
        """
        Get the distribution of licenses by status.
        
        Returns:
        --------
        Dict[str, int]
            Count of licenses by status
        """
        try:
            licenses = LicenseAPI.list_licenses()
            status_counts = {}
            
            for license in licenses:
                status = license.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return status_counts
        except Exception as e:
            logger.error(f"Failed to get license status distribution: {e}")
            return {}
    
    @staticmethod
    def get_compliance_statistics() -> Dict[str, Any]:
        """
        Get statistical information about license compliance.
        
        Returns:
        --------
        Dict[str, Any]
            Statistical information about compliance scores
        """
        try:
            licenses = LicenseAPI.list_licenses()
            if not licenses:
                return {
                    "avg_compliance": 0,
                    "min_compliance": 0,
                    "max_compliance": 0,
                    "total_licenses": 0,
                    "compliant_count": 0,
                    "compliance_rate": 0
                }
            
            compliance_scores = [l.get("compliance_score", 0) for l in licenses]
            compliant_count = sum(1 for score in compliance_scores if score >= 60)
            
            return {
                "avg_compliance": sum(compliance_scores) / len(compliance_scores),
                "min_compliance": min(compliance_scores),
                "max_compliance": max(compliance_scores),
                "total_licenses": len(licenses),
                "compliant_count": compliant_count,
                "compliance_rate": (compliant_count / len(licenses)) * 100
            }
        except Exception as e:
            logger.error(f"Failed to get compliance statistics: {e}")
            return {}