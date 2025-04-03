"""
Realm Scanner Module for Empire OS

- Monitors the health and alignment of a realm
- Tracks metrics across social, economic, and ecological dimensions
- Detects imbalances and provides early warnings
- Validates realm actions against divine principles
"""

import json
import os
from datetime import datetime
import random
import time

# Realm health indicators
HEALTH_INDICATORS = {
    "social": [
        "community_wellbeing",
        "diversity_inclusion",
        "education_access",
        "healthcare_quality",
        "civic_engagement"
    ],
    "economic": [
        "prosperity_distribution",
        "innovation_rate",
        "employment_quality",
        "resource_efficiency",
        "infrastructure_quality"
    ],
    "ecological": [
        "biodiversity_health",
        "air_quality",
        "water_purity",
        "soil_health",
        "waste_management"
    ],
    "spiritual": [
        "purpose_alignment",
        "ethical_behavior",
        "community_harmony",
        "generational_thinking",
        "humility_practice"
    ]
}

# Realm alignment statuses
ALIGNMENT_STATUS = {
    "DIVINE_ALIGNED": "Realm fully aligned with divine principles",
    "GENERALLY_ALIGNED": "Realm largely aligned with minor deviations",
    "PARTIALLY_ALIGNED": "Realm showing significant misalignment in some areas",
    "MISALIGNED": "Realm fundamentally out of alignment",
    "CRITICAL": "Realm in danger of collapse due to severe misalignment"
}

def scan_realm(realm_id, transaction=None):
    """
    Scans a realm to assess its current health and alignment
    
    Args:
        realm_id (str): Identifier for the realm
        transaction (dict, optional): Current transaction details for context
        
    Returns:
        dict: Realm health assessment
    """
    # In a real system, we would query a database of realm metrics
    # For this demo, we're generating a synthetic assessment
    
    # Get realm base data - would be from database in real system
    realm_data = get_realm_data(realm_id)
    
    # Assess each dimension of realm health
    social_health = assess_dimension("social", realm_data, transaction)
    economic_health = assess_dimension("economic", realm_data, transaction)
    ecological_health = assess_dimension("ecological", realm_data, transaction)
    spiritual_health = assess_dimension("spiritual", realm_data, transaction)
    
    # Calculate overall health score (0-100)
    # Weight each dimension equally for now
    overall_score = (
        social_health["score"] +
        economic_health["score"] +
        ecological_health["score"] +
        spiritual_health["score"]
    ) / 4
    
    # Determine alignment status based on score
    alignment_status = determine_alignment_status(overall_score)
    
    # Prepare result
    result = {
        "timestamp": datetime.now().isoformat(),
        "realm_id": realm_id,
        "realm_name": realm_data["name"],
        "social": social_health,
        "economic": economic_health,
        "ecological": ecological_health,
        "spiritual": spiritual_health,
        "overall_score": overall_score,
        "health": get_health_level(overall_score),
        "alignment_status": alignment_status,
        "warnings": generate_warnings(social_health, economic_health, ecological_health, spiritual_health)
    }
    
    # If a transaction is provided, assess its potential impact on realm
    if transaction:
        result["transaction_impact"] = assess_transaction_impact(transaction, result)
    
    # Log the realm scan
    log_realm_scan(result)
    
    return result

def get_realm_data(realm_id):
    """
    Retrieve realm data from database (simulated)
    
    Args:
        realm_id (str): Realm identifier
        
    Returns:
        dict: Realm base data
    """
    # Simulate realm database
    realms = {
        "RealmOne": {
            "id": "RealmOne",
            "name": "Realm One: Justice & Mercy Cohort",
            "description": "First realm stack simulation governed by Adl (Justice) and Rahma (Mercy)",
            "created_at": "2025-01-01T00:00:00Z",
            "governor": "realm-governor",
            "base_metrics": {
                "social": {
                    "community_wellbeing": 75,
                    "diversity_inclusion": 80,
                    "education_access": 70,
                    "healthcare_quality": 65,
                    "civic_engagement": 60
                },
                "economic": {
                    "prosperity_distribution": 65,
                    "innovation_rate": 75,
                    "employment_quality": 70,
                    "resource_efficiency": 60,
                    "infrastructure_quality": 65
                },
                "ecological": {
                    "biodiversity_health": 55,
                    "air_quality": 60,
                    "water_purity": 70,
                    "soil_health": 65,
                    "waste_management": 60
                },
                "spiritual": {
                    "purpose_alignment": 85,
                    "ethical_behavior": 80,
                    "community_harmony": 75,
                    "generational_thinking": 65,
                    "humility_practice": 70
                }
            }
        },
        "RealmTwo": {
            "id": "RealmTwo",
            "name": "Realm Two: Wisdom & Knowledge Hub",
            "description": "Second realm focused on Al-Hakim (Wisdom) and Al-Alim (Knowledge)",
            "created_at": "2025-02-01T00:00:00Z",
            "governor": "realm-governor-two",
            "base_metrics": {
                "social": {
                    "community_wellbeing": 65,
                    "diversity_inclusion": 70,
                    "education_access": 85,
                    "healthcare_quality": 60,
                    "civic_engagement": 55
                },
                "economic": {
                    "prosperity_distribution": 60,
                    "innovation_rate": 85,
                    "employment_quality": 65,
                    "resource_efficiency": 70,
                    "infrastructure_quality": 75
                },
                "ecological": {
                    "biodiversity_health": 50,
                    "air_quality": 55,
                    "water_purity": 60,
                    "soil_health": 55,
                    "waste_management": 65
                },
                "spiritual": {
                    "purpose_alignment": 75,
                    "ethical_behavior": 70,
                    "community_harmony": 65,
                    "generational_thinking": 80,
                    "humility_practice": 60
                }
            }
        }
    }
    
    # Return realm data if exists, otherwise return default
    if realm_id in realms:
        return realms[realm_id]
    else:
        # Return a default realm with average metrics
        return {
            "id": realm_id,
            "name": f"Realm {realm_id}",
            "description": "Default realm template",
            "created_at": datetime.now().isoformat(),
            "governor": "system",
            "base_metrics": {
                "social": {k: 60 for k in HEALTH_INDICATORS["social"]},
                "economic": {k: 60 for k in HEALTH_INDICATORS["economic"]},
                "ecological": {k: 60 for k in HEALTH_INDICATORS["ecological"]},
                "spiritual": {k: 60 for k in HEALTH_INDICATORS["spiritual"]}
            }
        }

def assess_dimension(dimension, realm_data, transaction=None):
    """
    Assess the health of a specific dimension of realm health
    
    Args:
        dimension (str): Dimension to assess ('social', 'economic', etc.)
        realm_data (dict): Base realm data
        transaction (dict, optional): Current transaction for context
        
    Returns:
        dict: Dimension health assessment
    """
    # Get base metrics for this dimension
    base_metrics = realm_data.get("base_metrics", {}).get(dimension, {})
    
    # Calculate current metrics - in a real system, this would include
    # recent transaction history, external data feeds, etc.
    current_metrics = {}
    for indicator in HEALTH_INDICATORS.get(dimension, []):
        base_value = base_metrics.get(indicator, 60)  # Default to 60 if not found
        
        # Adjust slightly to simulate natural fluctuations
        current_value = max(0, min(100, base_value + random.uniform(-5, 5)))
        current_metrics[indicator] = current_value
    
    # Calculate dimension score (average of all indicators)
    score = sum(current_metrics.values()) / len(current_metrics) if current_metrics else 0
    
    # Determine health level
    health = get_health_level(score)
    
    # Identify strongest and weakest indicators
    if current_metrics:
        strongest = max(current_metrics.items(), key=lambda x: x[1])
        weakest = min(current_metrics.items(), key=lambda x: x[1])
    else:
        strongest = ("none", 0)
        weakest = ("none", 0)
    
    return {
        "score": score,
        "health": health,
        "metrics": current_metrics,
        "strongest": {
            "indicator": strongest[0],
            "value": strongest[1]
        },
        "weakest": {
            "indicator": weakest[0],
            "value": weakest[1]
        }
    }

def determine_alignment_status(overall_score):
    """
    Determine the realm's alignment status based on overall score
    
    Args:
        overall_score (float): Overall health score (0-100)
        
    Returns:
        str: Alignment status key
    """
    if overall_score >= 85:
        return "DIVINE_ALIGNED"
    elif overall_score >= 70:
        return "GENERALLY_ALIGNED"
    elif overall_score >= 50:
        return "PARTIALLY_ALIGNED"
    elif overall_score >= 30:
        return "MISALIGNED"
    else:
        return "CRITICAL"

def get_health_level(score):
    """
    Convert a numeric score to a health level label
    
    Args:
        score (float): Health score (0-100)
        
    Returns:
        str: Health level label
    """
    if score >= 85:
        return "excellent"
    elif score >= 70:
        return "good"
    elif score >= 50:
        return "fair"
    elif score >= 30:
        return "poor"
    else:
        return "critical"

def generate_warnings(social, economic, ecological, spiritual):
    """
    Generate warnings based on dimension assessments
    
    Args:
        social (dict): Social health assessment
        economic (dict): Economic health assessment
        ecological (dict): Ecological health assessment
        spiritual (dict): Spiritual health assessment
        
    Returns:
        list: Warning messages
    """
    warnings = []
    
    # Check for critical or poor health in any dimension
    dimensions = [
        ("social", social),
        ("economic", economic),
        ("ecological", ecological),
        ("spiritual", spiritual)
    ]
    
    for name, dimension in dimensions:
        if dimension["health"] == "critical":
            warnings.append({
                "level": "critical",
                "dimension": name,
                "message": f"Critical imbalance in {name} dimension requires immediate attention"
            })
        elif dimension["health"] == "poor":
            warnings.append({
                "level": "warning",
                "dimension": name,
                "message": f"Poor health in {name} dimension requires intervention"
            })
    
    # Check for specific indicators in critical condition
    for name, dimension in dimensions:
        weakest = dimension["weakest"]
        if weakest["value"] < 30:
            warnings.append({
                "level": "critical",
                "dimension": name,
                "indicator": weakest["indicator"],
                "message": f"Critical status for {weakest['indicator']} ({weakest['value']:.1f}/100)"
            })
    
    return warnings

def assess_transaction_impact(transaction, realm_health):
    """
    Assess the potential impact of a transaction on realm health
    
    Args:
        transaction (dict): Transaction details
        realm_health (dict): Current realm health assessment
        
    Returns:
        dict: Transaction impact assessment
    """
    # Extract transaction details
    transaction_type = transaction.get('type', '')
    quantity = transaction.get('quantity', 0)
    model = transaction.get('model', '')
    urgency = transaction.get('urgency', 'low')
    
    # Initialize impact assessment
    impact = {
        "social": "neutral",
        "economic": "positive",  # Assume economic benefit by default
        "ecological": "neutral",
        "spiritual": "neutral",
        "overall": "neutral"
    }
    
    # Adjust based on transaction details
    if quantity > 5000:
        impact["ecological"] = "negative"
    
    if transaction_type == "license-request":
        impact["social"] = "positive"  # Licensing creates accountability
    
    # Consider realm's current weakest dimensions
    weakest_dimension = min([
        ("social", realm_health["social"]["score"]),
        ("economic", realm_health["economic"]["score"]),
        ("ecological", realm_health["ecological"]["score"]),
        ("spiritual", realm_health["spiritual"]["score"])
    ], key=lambda x: x[1])[0]
    
    # If transaction could further harm the weakest dimension, flag it
    if impact[weakest_dimension] == "negative":
        impact["warning"] = f"Transaction may further weaken realm's {weakest_dimension} dimension"
    
    # Determine overall impact (simple heuristic for demo)
    impact_values = {"positive": 1, "neutral": 0, "negative": -1}
    overall_value = sum(impact_values.get(impact[dim], 0) for dim in ["social", "economic", "ecological", "spiritual"])
    
    if overall_value > 1:
        impact["overall"] = "positive"
    elif overall_value < -1:
        impact["overall"] = "negative"
    
    return impact

def log_realm_scan(scan_result):
    """Log realm scan to file"""
    # Ensure data directory exists
    os.makedirs('data/ledger', exist_ok=True)
    
    # Create log entry
    log_entry = {
        "timestamp": scan_result.get("timestamp"),
        "action": "realm_scan",
        "realm_id": scan_result.get("realm_id"),
        "overall_score": scan_result.get("overall_score"),
        "health": scan_result.get("health"),
        "alignment_status": scan_result.get("alignment_status"),
        "warning_count": len(scan_result.get("warnings", []))
    }
    
    # Append to log file
    with open('data/ledger/realm_ledger.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

# For testing
if __name__ == "__main__":
    # Test transaction
    test_transaction = {
        "type": "license-request",
        "model": "CMP",
        "quantity": 10000,
        "urgency": "medium",
        "impact": "medium"
    }
    
    # Scan realm
    result = scan_realm("RealmOne", test_transaction)
    print(json.dumps(result, indent=2))