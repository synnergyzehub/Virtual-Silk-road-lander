import streamlit as st
import json
import datetime
import os
from typing import Dict, Any

# Import the ECG license structures
try:
    from core.ecg_license_structure import (
        License, LicenseStatus, LicenseType, ComplianceTier,
        DivinePrinciple, GovernanceDimension
    )
    from core.ecg_license_manager import ECGLicenseManager
    license_imports_success = True
except Exception as e:
    license_imports_success = False
    import_error = str(e)

def main():
    """ECG License System Test Application"""
    st.set_page_config(
        page_title="ECG License Tester",
        page_icon="🔑",
        layout="wide"
    )
    
    st.title("ECG License System Test")
    st.markdown("This application tests the Emperor's Computational Governance (ECG) License System.")
    
    if not license_imports_success:
        st.error(f"Failed to import license modules: {import_error}")
        st.markdown("Please make sure the following files exist:")
        st.markdown("- core/ecg_license_structure.py")
        st.markdown("- core/ecg_license_manager.py")
        return
    
    # Ensure directory structure exists
    os.makedirs("data", exist_ok=True)
    os.makedirs("core", exist_ok=True)
    
    # Get license manager singleton
    try:
        license_manager = ECGLicenseManager()
        st.success("✅ Successfully initialized ECGLicenseManager")
    except Exception as e:
        st.error(f"Failed to initialize license manager: {str(e)}")
        return
    
    # Test functions
    st.markdown("## License System Tests")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Test License Issuance"):
            test_license_issuance(license_manager)
    
    with col2:
        if st.button("Test License Validation"):
            test_license_validation(license_manager)
    
    with col3:
        if st.button("Test Compliance Audit"):
            test_compliance_audit(license_manager)
    
    # Display current licenses
    st.markdown("## Current Licenses")
    
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        st.info("No licenses have been issued yet.")
    else:
        for license_data in licenses:
            with st.expander(f"{license_data['entity_name']} ({license_data['license_id']})"):
                st.json(license_data)

def test_license_issuance(license_manager: ECGLicenseManager):
    """Test the license issuance functionality"""
    st.markdown("### Testing License Issuance")
    
    try:
        # Issue a test license
        new_license = license_manager.issue_new_license(
            entity_name="Test Corporation",
            entity_id="TEST-CORP-001",
            license_type_str="corporate",
            validity_days=365,
            compliance_tier_str="tier_3",
            modules=["inventory_management", "reporting_module"],
            restrictions=["Test restriction"],
            metadata={"test_key": "test_value"}
        )
        
        st.success(f"✅ Successfully issued license: {new_license['license_id']}")
        
        # Display the license
        st.json(new_license)
        
        return new_license["license_id"]
    
    except Exception as e:
        st.error(f"❌ Failed to issue license: {str(e)}")
        return None

def test_license_validation(license_manager: ECGLicenseManager):
    """Test the license validation functionality"""
    st.markdown("### Testing License Validation")
    
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        license_id = test_license_issuance(license_manager)
        if not license_id:
            st.error("❌ Cannot test validation without a license")
            return
    else:
        license_id = licenses[0]["license_id"]
    
    try:
        # Validate the license
        validation_result = license_manager.validate_license(license_id)
        
        if validation_result["is_valid"]:
            st.success(f"✅ License is valid: {validation_result['message']}")
        else:
            st.warning(f"⚠️ License is not valid: {validation_result['message']}")
        
        # Display the validation result
        st.json(validation_result)
        
        # Test validation for non-existent license
        invalid_result = license_manager.validate_license("NON-EXISTENT")
        
        if not invalid_result["is_valid"]:
            st.success("✅ Correctly identified non-existent license as invalid")
        else:
            st.error("❌ Failed to identify non-existent license as invalid")
        
        st.json(invalid_result)
    
    except Exception as e:
        st.error(f"❌ Failed to validate license: {str(e)}")

def test_compliance_audit(license_manager: ECGLicenseManager):
    """Test the compliance audit functionality"""
    st.markdown("### Testing Compliance Audit")
    
    licenses = license_manager.list_all_licenses()
    
    if not licenses:
        license_id = test_license_issuance(license_manager)
        if not license_id:
            st.error("❌ Cannot test audit without a license")
            return
    else:
        license_id = licenses[0]["license_id"]
    
    try:
        # Current license details
        license_details = license_manager.get_license_details(license_id)
        st.markdown(f"Current compliance score: {license_details['current_compliance_score']}")
        
        # Create test audit data
        dimension_scores = {
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
        }
        
        findings = [
            "Test finding 1",
            "Test finding 2"
        ]
        
        recommendations = [
            "Test recommendation 1",
            "Test recommendation 2"
        ]
        
        # Perform the audit
        audit_result = license_manager.perform_compliance_audit(
            license_id=license_id,
            auditor="Test Auditor",
            dimension_scores=dimension_scores,
            findings=findings,
            recommendations=recommendations
        )
        
        st.success(f"✅ Successfully performed audit with score: {audit_result['overall_score']}")
        
        # Display the audit result
        st.json(audit_result)
        
        # Check compliance history
        history = license_manager.get_compliance_history(license_id)
        st.markdown(f"License now has {len(history)} audit(s) in history")
        
        # Validate that compliance score was updated
        updated_license = license_manager.get_license_details(license_id)
        st.markdown(f"Updated compliance score: {updated_license['current_compliance_score']}")
        
        if updated_license['current_compliance_score'] != license_details['current_compliance_score']:
            st.success("✅ Compliance score was updated correctly")
        else:
            st.error("❌ Compliance score was not updated")
    
    except Exception as e:
        st.error(f"❌ Failed to perform audit: {str(e)}")

if __name__ == "__main__":
    main()