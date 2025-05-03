"""
Genesis Stack License API

RESTful API for the Genesis Stack licensing system, providing endpoints for license
creation, validation, and management with divine governance integration.
"""

import os
import json
import datetime
import logging
from typing import Dict, List, Optional, Any, Union
from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import HTTPException
import time
import uuid

# Import the license manager and divine principles scorecard
from genesis_license_manager import (
    GenesisLicenseManager,
    LicenseType,
    LicenseStatus,
    GovernanceLevel
)
from divine_principles_scorecard import DivinePrinciplesScorecard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("genesis_license_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("genesis_license_api")

# Initialize Flask app
app = Flask(__name__)

# Configuration
API_KEY = os.environ.get("GENESIS_API_KEY", "emperorkey123")
API_VERSION = "v1"
BASE_PATH = f"/api/{API_VERSION}"

# Initialize license manager and divine principles scorecard
license_manager = GenesisLicenseManager()
divine_scorecard = DivinePrinciplesScorecard()

# Helper functions

def validate_api_key() -> bool:
    """
    Validate the API key in the request.
    
    Returns:
        bool: True if the API key is valid, False otherwise
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    
    # Extract API key from Authorization header
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return False
    
    api_key = parts[1]
    return api_key == API_KEY

def require_api_key(func):
    """
    Decorator to require a valid API key for a route.
    """
    def wrapper(*args, **kwargs):
        if not validate_api_key():
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid API key required'
            }), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def validate_required_fields(data: Dict, required_fields: List[str]) -> Optional[Dict]:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data: Data to validate
        required_fields: List of field names that must be present
        
    Returns:
        Optional[Dict]: Error response if validation fails, None if successful
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {
            'error': 'Bad Request',
            'message': f"Missing required fields: {', '.join(missing_fields)}"
        }, 400
    return None

def log_request(endpoint: str, request_data: Any = None) -> None:
    """
    Log a request to the API.
    
    Args:
        endpoint: API endpoint
        request_data: Request data (optional)
    """
    client_ip = request.remote_addr
    method = request.method
    
    log_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'client_ip': client_ip,
        'method': method,
        'endpoint': endpoint,
        'user_agent': request.headers.get('User-Agent')
    }
    
    if request_data:
        log_data['request_data'] = request_data
    
    logger.info(f"API Request: {method} {endpoint} from {client_ip}")
    
    # Save to request log
    try:
        with open('api_request_log.jsonl', 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        logger.error(f"Error writing to request log: {str(e)}")

def add_divine_headers(response: Response) -> Response:
    """
    Add divine governance headers to a response.
    
    Args:
        response: Flask response object
        
    Returns:
        Response: Response with added headers
    """
    response.headers['X-Divine-Alignment'] = 'true'
    response.headers['X-Divine-Governance-Level'] = 'enhanced'
    response.headers['X-Divine-Verification-Authority'] = 'Genesis Ecosystem'
    return response

# Error handling

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions"""
    response = jsonify({
        'error': e.name,
        'message': e.description
    })
    response.status_code = e.code
    return response

@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Handle generic exceptions"""
    logger.error(f"Unhandled exception: {str(e)}")
    response = jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    })
    response.status_code = 500
    return response

# Health check endpoint

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Genesis License API',
        'version': API_VERSION,
        'timestamp': datetime.datetime.now().isoformat()
    })

# API routes

@app.route(f'{BASE_PATH}/divine-scorecard/<license_id>', methods=['GET'])
@require_api_key
def get_divine_scorecard(license_id):
    """Get a divine principles scorecard for a license"""
    log_request(f'/divine-scorecard/{license_id}')
    
    # Get the license data
    license_data = license_manager.get_license(license_id)
    
    if not license_data:
        return jsonify({
            'error': 'Not Found',
            'message': f"License {license_id} not found"
        }), 404
    
    # Generate the scorecard
    scorecard = divine_scorecard.evaluate_license(license_data)
    
    # Generate recommendations
    recommendations = divine_scorecard.generate_recommendations(scorecard)
    
    # Generate visualization data
    visualization_data = divine_scorecard.get_divine_visualization_data(scorecard)
    
    # Prepare response
    response_data = {
        'scorecard': scorecard,
        'recommendations': recommendations,
        'visualization_data': visualization_data
    }
    
    response = jsonify(response_data)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/divine-scorecard/save/<license_id>', methods=['POST'])
@require_api_key
def save_divine_scorecard(license_id):
    """Save a divine principles scorecard for a license to the filesystem"""
    from divine_principles_scorecard import save_scorecard
    
    log_request(f'/divine-scorecard/save/{license_id}')
    
    # Get the license data
    license_data = license_manager.get_license(license_id)
    
    if not license_data:
        return jsonify({
            'error': 'Not Found',
            'message': f"License {license_id} not found"
        }), 404
    
    # Generate the scorecard
    scorecard = divine_scorecard.evaluate_license(license_data)
    
    # Save the scorecard
    try:
        output_dir = request.args.get('output_dir', 'scorecards')
        output_path = save_scorecard(scorecard, output_dir)
        
        return jsonify({
            'success': True,
            'message': f"Scorecard saved to {output_path}",
            'file_path': output_path
        }), 200
    
    except Exception as e:
        logger.error(f"Error saving scorecard: {str(e)}")
        return jsonify({
            'error': 'Scorecard Save Failed',
            'message': str(e)
        }), 500

@app.route(f'{BASE_PATH}/licenses', methods=['POST'])
@require_api_key
def create_license():
    """Create a new license"""
    data = request.json
    log_request('/licenses', data)
    
    # Validate required fields
    required_fields = ['type', 'holder', 'permissions']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error
    
    try:
        # Extract license parameters
        license_type = data['type']
        holder = data['holder']
        permissions = data['permissions']
        validity_days = data.get('validity_days')
        metadata = data.get('metadata', {})
        
        # Create the license
        license_data = license_manager.create_license(
            license_type=license_type,
            holder=holder,
            validity_days=validity_days,
            permissions=permissions,
            metadata=metadata
        )
        
        # Generate license key
        license_key = license_manager.generate_license_key(license_data['id'])
        
        # Prepare response
        response_data = {
            'license': license_data,
            'license_key': license_key
        }
        
        response = jsonify(response_data)
        return add_divine_headers(response), 201
    
    except Exception as e:
        logger.error(f"Error creating license: {str(e)}")
        return jsonify({
            'error': 'License Creation Failed',
            'message': str(e)
        }), 500

@app.route(f'{BASE_PATH}/licenses/<license_id>', methods=['GET'])
@require_api_key
def get_license(license_id):
    """Get a license by ID"""
    log_request(f'/licenses/{license_id}')
    
    license_data = license_manager.get_license(license_id)
    
    if not license_data:
        return jsonify({
            'error': 'Not Found',
            'message': f"License {license_id} not found"
        }), 404
    
    response = jsonify(license_data)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>/verify', methods=['POST'])
@require_api_key
def verify_license(license_id):
    """Verify a license by ID"""
    log_request(f'/licenses/{license_id}/verify')
    
    verification = license_manager.verify_license(license_id)
    
    response = jsonify(verification)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>', methods=['PATCH'])
@require_api_key
def update_license(license_id):
    """Update a license by ID"""
    data = request.json
    log_request(f'/licenses/{license_id}', data)
    
    updated_license = license_manager.update_license(license_id, data)
    
    if not updated_license:
        return jsonify({
            'error': 'Update Failed',
            'message': f"Failed to update license {license_id}"
        }), 404
    
    response = jsonify(updated_license)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>/revoke', methods=['POST'])
@require_api_key
def revoke_license(license_id):
    """Revoke a license by ID"""
    data = request.json
    log_request(f'/licenses/{license_id}/revoke', data)
    
    # Validate required fields
    required_fields = ['reason']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error
    
    reason = data['reason']
    result = license_manager.revoke_license(license_id, reason)
    
    if not result:
        return jsonify({
            'error': 'Revocation Failed',
            'message': f"Failed to revoke license {license_id}"
        }), 404
    
    response = jsonify({
        'license_id': license_id,
        'status': 'revoked',
        'reason': reason,
        'timestamp': datetime.datetime.now().isoformat()
    })
    
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>/renew', methods=['POST'])
@require_api_key
def renew_license(license_id):
    """Renew a license by ID"""
    data = request.json or {}
    log_request(f'/licenses/{license_id}/renew', data)
    
    validity_days = data.get('validity_days')
    renewed_license = license_manager.renew_license(license_id, validity_days)
    
    if not renewed_license:
        return jsonify({
            'error': 'Renewal Failed',
            'message': f"Failed to renew license {license_id}"
        }), 404
    
    # Generate new license key
    license_key = license_manager.generate_license_key(renewed_license['id'])
    
    response_data = {
        'license': renewed_license,
        'license_key': license_key
    }
    
    response = jsonify(response_data)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>/check-renewal', methods=['GET'])
@require_api_key
def check_renewal_needed(license_id):
    """Check if a license needs renewal"""
    log_request(f'/licenses/{license_id}/check-renewal')
    
    renewal_info = license_manager.check_renewal_needed(license_id)
    
    response = jsonify(renewal_info)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses/<license_id>/key', methods=['GET'])
@require_api_key
def get_license_key(license_id):
    """Get the license key for a license"""
    log_request(f'/licenses/{license_id}/key')
    
    try:
        license_key = license_manager.generate_license_key(license_id)
        
        response = jsonify({
            'license_id': license_id,
            'license_key': license_key
        })
        
        return add_divine_headers(response), 200
    
    except ValueError as e:
        return jsonify({
            'error': 'Not Found',
            'message': str(e)
        }), 404
    
    except Exception as e:
        logger.error(f"Error generating license key: {str(e)}")
        return jsonify({
            'error': 'License Key Generation Failed',
            'message': 'Failed to generate license key'
        }), 500

@app.route(f'{BASE_PATH}/licenses/<license_id>/verify-key', methods=['POST'])
@require_api_key
def verify_license_key(license_id):
    """Verify a license key against a license ID"""
    data = request.json
    log_request(f'/licenses/{license_id}/verify-key', data)
    
    # Validate required fields
    required_fields = ['license_key']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error
    
    license_key = data['license_key']
    is_valid = license_manager.verify_license_key(license_id, license_key)
    
    response = jsonify({
        'license_id': license_id,
        'valid': is_valid
    })
    
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/licenses', methods=['GET'])
@require_api_key
def list_licenses():
    """List licenses with optional filtering"""
    log_request('/licenses')
    
    # Extract filter parameters from query string
    filter_params = {}
    for key, value in request.args.items():
        if key not in ['limit', 'offset']:
            filter_params[key] = value
    
    # Get licenses with filtering
    licenses = license_manager.list_licenses(filter_params)
    
    # Apply pagination if requested
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)
    
    total_count = len(licenses)
    
    if limit is not None:
        licenses = licenses[offset:offset + limit]
    
    response = jsonify({
        'licenses': licenses,
        'total': total_count,
        'limit': limit,
        'offset': offset
    })
    
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/license-types', methods=['GET'])
@require_api_key
def list_license_types():
    """List available license types"""
    log_request('/license-types')
    
    # Get all license types from the enum
    license_types = [lt.value for lt in LicenseType]
    
    response = jsonify({
        'license_types': license_types
    })
    
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/divine-governance', methods=['GET'])
@require_api_key
def get_divine_governance():
    """Get information about divine governance"""
    log_request('/divine-governance')
    
    # Get the divine principles from the scorecard
    divine_principles = []
    for principle in divine_scorecard.principles:
        principle_data = {
            'id': principle['id'],
            'name': principle['name'],
            'description': principle['description'],
            'weight': principle['weight'],
            'factors': []
        }
        
        # Include factors information
        for factor in principle.get('factors', []):
            principle_data['factors'].append({
                'name': factor['name'],
                'weight': factor['weight']
            })
            
        divine_principles.append(principle_data)
    
    governance_info = {
        'governance_levels': [level.value for level in GovernanceLevel],
        'default_level': license_manager.config["governance_level"],
        'min_divine_alignment': license_manager.config["min_divine_alignment"],
        'verification_interval': license_manager.config["verification_interval"],
        'divine_principles': divine_principles,
        'scorecard_version': '1.0'
    }
    
    response = jsonify(governance_info)
    return add_divine_headers(response), 200

@app.route(f'{BASE_PATH}/divine-alignment', methods=['POST'])
@require_api_key
def calculate_divine_alignment():
    """Calculate divine alignment for license data"""
    data = request.json
    log_request('/divine-alignment', data)
    
    # Legacy calculation for backward compatibility
    legacy_alignment_score = license_manager._calculate_divine_alignment(data)
    
    # Use the new Divine Principles Scorecard
    scorecard_results = divine_scorecard.evaluate_license(data)
    
    response = jsonify({
        'alignment_score': scorecard_results['overall_score'],
        'legacy_alignment_score': legacy_alignment_score,
        'principle_scores': scorecard_results['principle_scores'],
        'verification_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'verification_authority': "Divine Governance Layer"
    })
    
    return add_divine_headers(response), 200

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting secure license API with key: {API_KEY}")
    
    # Add divine scorecard endpoints before running the app
    @app.route(f'{BASE_PATH}/divine-scorecard/<license_id>', methods=['GET'])
    @require_api_key
    def get_divine_scorecard(license_id):
        """Get a divine principles scorecard for a license"""
        log_request(f'/divine-scorecard/{license_id}')
        
        # Check if the license exists
        license_data = license_manager.get_license(license_id)
        if not license_data:
            return jsonify({'error': f'License not found: {license_id}'}), 404
        
        # Generate the scorecard
        scorecard = divine_scorecard.evaluate_license(license_data)
        
        # Add license metadata to the scorecard
        scorecard['license_id'] = license_id
        scorecard['license_type'] = license_data.get('type', '')
        scorecard['holder_name'] = license_data.get('holder', {}).get('name', '')
        
        # Generate recommendations based on the scorecard
        recommendations = divine_scorecard.generate_recommendations(scorecard)
        scorecard['recommendations'] = recommendations
        
        response = jsonify(scorecard)
        return add_divine_headers(response), 200
    
    @app.route(f'{BASE_PATH}/divine-scorecard/save/<license_id>', methods=['POST'])
    @require_api_key
    def save_divine_scorecard(license_id):
        """Save a divine principles scorecard for a license to the filesystem"""
        log_request(f'/divine-scorecard/save/{license_id}')
        
        # Get output directory from query parameters
        output_dir = request.args.get('output_dir', 'scorecards')
        
        # Check if the license exists
        license_data = license_manager.get_license(license_id)
        if not license_data:
            return jsonify({'error': f'License not found: {license_id}'}), 404
        
        # Generate the scorecard
        scorecard = divine_scorecard.evaluate_license(license_data)
        
        # Add license metadata to the scorecard
        scorecard['license_id'] = license_id
        scorecard['license_type'] = license_data.get('type', '')
        scorecard['holder_name'] = license_data.get('holder', {}).get('name', '')
        
        # Generate recommendations
        recommendations = divine_scorecard.generate_recommendations(scorecard)
        scorecard['recommendations'] = recommendations
        
        # Save the scorecard to filesystem
        try:
            from divine_principles_scorecard import save_scorecard
            path = save_scorecard(scorecard, output_dir)
            
            response = jsonify({
                'status': 'success',
                'message': f'Scorecard saved to {path}',
                'path': path
            })
            return add_divine_headers(response), 200
        except Exception as e:
            return jsonify({'error': f'Failed to save scorecard: {str(e)}'}), 500
    
    app.run(host=host, port=port, debug=debug)