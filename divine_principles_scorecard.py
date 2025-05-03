"""
Divine Principles Scorecard

This module provides a dynamic scorecard for evaluating licenses against
divine governance principles, with detailed scoring and visualization capabilities.
"""

import numpy as np
import json
import datetime
import hashlib
import os
from typing import Dict, List, Any, Optional, Tuple, Union

# Define the core divine principles
DIVINE_PRINCIPLES = [
    {
        "id": "transaction_integrity",
        "name": "Transaction Integrity",
        "description": "Ensuring all transactions adhere to ethical pricing and distribution principles",
        "weight": 1.0,
        "factors": [
            {"name": "Pricing Fairness", "weight": 0.3},
            {"name": "Transparency", "weight": 0.3},
            {"name": "Value Distribution", "weight": 0.2},
            {"name": "Customer Value", "weight": 0.2}
        ]
    },
    {
        "id": "resource_optimization",
        "name": "Resource Optimization",
        "description": "Verifying appropriate resource utilization with minimal waste",
        "weight": 1.0,
        "factors": [
            {"name": "Efficiency", "weight": 0.25},
            {"name": "Waste Reduction", "weight": 0.25},
            {"name": "Renewable Usage", "weight": 0.25},
            {"name": "Longevity", "weight": 0.25}
        ]
    },
    {
        "id": "fair_trade",
        "name": "Fair Trade",
        "description": "Confirming compliance with fair trade principles across all operations",
        "weight": 1.0,
        "factors": [
            {"name": "Fair Compensation", "weight": 0.3},
            {"name": "Supply Chain Ethics", "weight": 0.3},
            {"name": "Local Community Impact", "weight": 0.2},
            {"name": "Global Standards Alignment", "weight": 0.2}
        ]
    },
    {
        "id": "transparency",
        "name": "Transparency",
        "description": "Validating accurate and transparent reporting and disclosure",
        "weight": 1.0,
        "factors": [
            {"name": "Data Accuracy", "weight": 0.25},
            {"name": "Reporting Completeness", "weight": 0.25},
            {"name": "Stakeholder Communication", "weight": 0.25},
            {"name": "Audit Traceability", "weight": 0.25}
        ]
    },
    {
        "id": "ethical_conduct",
        "name": "Ethical Conduct",
        "description": "Monitoring overall business conduct alignment with divine principles",
        "weight": 1.0,
        "factors": [
            {"name": "Leadership Integrity", "weight": 0.25},
            {"name": "Decision Framework", "weight": 0.25},
            {"name": "Stakeholder Treatment", "weight": 0.25},
            {"name": "Social Responsibility", "weight": 0.25}
        ]
    },
    {
        "id": "divine_alignment",
        "name": "Divine Alignment",
        "description": "Measuring overall alignment with divine governance frameworks",
        "weight": 1.0,
        "factors": [
            {"name": "Imperial Mandate Alignment", "weight": 0.3},
            {"name": "Divine Guidance Integration", "weight": 0.3},
            {"name": "Harmony Promotion", "weight": 0.2},
            {"name": "Collective Elevation", "weight": 0.2}
        ]
    }
]

# Scorecard class
class DivinePrinciplesScorecard:
    """
    Dynamic scorecard for evaluating license data against divine principles.
    """
    
    def __init__(self, principles: Optional[List[Dict]] = None):
        """
        Initialize the divine principles scorecard.
        
        Args:
            principles: Optional custom principles (defaults to predefined DIVINE_PRINCIPLES)
        """
        self.principles = principles or DIVINE_PRINCIPLES
        self.scores_cache = {}
    
    def _calculate_principle_score(self, principle: Dict, license_data: Dict) -> Dict:
        """
        Calculate the score for a single divine principle.
        
        Args:
            principle: The principle definition
            license_data: The license data to evaluate
            
        Returns:
            Dict: Score details for the principle
        """
        # Start with base score influenced by license type and metadata
        principle_id = principle["id"]
        base_score = 85.0  # Default base score
        
        # Adjust based on license type
        license_type = license_data.get("type", "").lower()
        if license_type == "enterprise":
            base_score += 3
        elif license_type == "evaluation":
            base_score -= 5
            
        # Adjust based on permissions
        permissions = license_data.get("permissions", [])
        if principle_id in permissions:
            base_score += 5
        
        # Additional adjustments based on metadata
        metadata = license_data.get("metadata", {})
        
        # Industry-specific adjustments
        industry = metadata.get("industry", "").lower()
        if industry in ["retail", "education", "healthcare", "public_service"]:
            base_score += 2
        elif industry in ["finance", "defense", "energy"]:
            base_score -= 2
            
        # Specific principle adjustments
        if principle_id == "resource_optimization":
            if "resource_policies" in metadata:
                base_score += 3
                
        elif principle_id == "fair_trade":
            if "supply_chain_verification" in metadata:
                base_score += 4
            if metadata.get("organization_size") == "Global":
                base_score -= 3  # Global operations face more fair trade challenges
                
        elif principle_id == "transparency":
            if "public_reporting" in metadata:
                base_score += 5
                
        elif principle_id == "ethical_conduct":
            if "ethics_training" in metadata:
                base_score += 3
                
        elif principle_id == "divine_alignment":
            governance_level = license_data.get("governance_level", "").lower()
            if governance_level == "maximum":
                base_score += 7
            elif governance_level == "enhanced":
                base_score += 3
                
        # Calculate factor scores
        factors = principle.get("factors", [])
        factor_scores = []
        
        for factor in factors:
            factor_name = factor["name"]
            factor_weight = factor["weight"]
            
            # Calculate score for this factor (default to base score with some variance)
            factor_score = max(0, min(100, base_score + np.random.normal(0, 3)))
            
            # Add factor score
            factor_scores.append({
                "name": factor_name,
                "score": factor_score,
                "weight": factor_weight
            })
        
        # Calculate weighted average of factor scores
        if factor_scores:
            total_weight = sum(f["weight"] for f in factor_scores)
            weighted_score = sum(f["score"] * f["weight"] for f in factor_scores) / total_weight
        else:
            weighted_score = base_score
            
        # Apply final normalization
        weighted_score = max(0, min(100, weighted_score))
        
        return {
            "principle_id": principle_id,
            "principle_name": principle["name"],
            "description": principle["description"],
            "overall_score": weighted_score,
            "factors": factor_scores,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    
    def evaluate_license(self, license_data: Dict) -> Dict:
        """
        Evaluate a license against all divine principles.
        
        Args:
            license_data: The license data to evaluate
            
        Returns:
            Dict: Complete scorecard results
        """
        # Check if we already have cached results
        license_id = license_data.get("id")
        cache_key = None
        
        if license_id:
            # Create a cache key based on license ID and a hash of the license data
            license_hash = hashlib.md5(json.dumps(license_data, sort_keys=True).encode()).hexdigest()
            cache_key = f"{license_id}:{license_hash}"
            
            # Return cached results if available and not expired
            if cache_key in self.scores_cache:
                cached = self.scores_cache[cache_key]
                # Cache expires after 1 hour
                cache_time = datetime.datetime.fromisoformat(cached["timestamp"].replace('Z', '+00:00'))
                if (datetime.datetime.now(datetime.timezone.utc) - cache_time).total_seconds() < 3600:
                    return cached
        
        # Calculate scores for each principle
        principle_scores = []
        for principle in self.principles:
            score_data = self._calculate_principle_score(principle, license_data)
            principle_scores.append(score_data)
        
        # Calculate overall divine alignment score (weighted average of principle scores)
        total_weight = sum(p["weight"] for p in self.principles)
        overall_score = sum(s["overall_score"] * p["weight"] for s, p in zip(principle_scores, self.principles)) / total_weight
        
        # Create result object
        result = {
            "license_id": license_data.get("id", "unknown"),
            "license_type": license_data.get("type", "unknown"),
            "holder_name": license_data.get("holder", {}).get("name", "unknown"),
            "overall_score": overall_score,
            "principle_scores": principle_scores,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "scorecard_version": "1.0"
        }
        
        # Cache the results if we have a license ID
        if cache_key:
            self.scores_cache[cache_key] = result
        
        return result
    
    def generate_recommendations(self, scorecard: Dict) -> List[Dict]:
        """
        Generate recommendations based on scorecard results.
        
        Args:
            scorecard: Scorecard data from evaluate_license
            
        Returns:
            List[Dict]: List of recommendations
        """
        recommendations = []
        principle_scores = scorecard.get("principle_scores", [])
        
        # Find the lowest scoring principles
        sorted_principles = sorted(principle_scores, key=lambda x: x["overall_score"])
        
        # Generate recommendations for the lowest scoring principles
        for principle in sorted_principles[:3]:  # Focus on the 3 lowest scores
            principle_id = principle["principle_id"]
            principle_name = principle["principle_name"]
            score = principle["overall_score"]
            
            # Find the lowest scoring factors
            factors = principle.get("factors", [])
            sorted_factors = sorted(factors, key=lambda x: x["score"])
            
            if sorted_factors:
                lowest_factor = sorted_factors[0]
                
                # Generate recommendation based on principle and lowest factor
                recommendation = {
                    "principle_id": principle_id,
                    "principle_name": principle_name,
                    "current_score": score,
                    "target_area": lowest_factor["name"],
                    "priority": "High" if score < 70 else "Medium" if score < 85 else "Low",
                    "recommendation": self._get_recommendation_text(principle_id, lowest_factor["name"], score)
                }
                
                recommendations.append(recommendation)
        
        return recommendations
    
    def _get_recommendation_text(self, principle_id: str, factor_name: str, score: float) -> str:
        """
        Get recommendation text based on principle, factor and score.
        
        Args:
            principle_id: The principle ID
            factor_name: The factor name
            score: The current score
            
        Returns:
            str: Recommendation text
        """
        # Recommendation templates
        templates = {
            "transaction_integrity": {
                "Pricing Fairness": "Implement a price transparency policy that ensures consistent and fair pricing across all distribution channels.",
                "Transparency": "Enhance transaction documentation with clear itemization of all costs and fees to improve customer trust.",
                "Value Distribution": "Review value chain to ensure all participants receive equitable value from transactions.",
                "Customer Value": "Develop metrics to measure and improve customer value realization from purchases."
            },
            "resource_optimization": {
                "Efficiency": "Conduct an efficiency audit to identify and address resource utilization gaps.",
                "Waste Reduction": "Implement a formal waste reduction program with measurable targets.",
                "Renewable Usage": "Increase the percentage of renewable resources used in operations and products.",
                "Longevity": "Design products and services with extended lifecycles to reduce resource consumption."
            },
            "fair_trade": {
                "Fair Compensation": "Audit compensation practices across supply chain to ensure fair wages for all contributors.",
                "Supply Chain Ethics": "Implement a supply chain verification protocol with regular audits and certifications.",
                "Local Community Impact": "Develop community impact assessments for all operational locations.",
                "Global Standards Alignment": "Align all trade practices with international fair trade standards and certifications."
            },
            "transparency": {
                "Data Accuracy": "Implement additional verification steps to ensure all reported data meets accuracy standards.",
                "Reporting Completeness": "Expand reporting to include all material aspects of business operations and impacts.",
                "Stakeholder Communication": "Create a formal stakeholder communication program with regular updates and feedback channels.",
                "Audit Traceability": "Enhance data systems to provide complete audit trails for all transactions and decisions."
            },
            "ethical_conduct": {
                "Leadership Integrity": "Establish a formal ethics training program for all leadership positions.",
                "Decision Framework": "Implement an ethical decision framework that integrates divine principles into all major decisions.",
                "Stakeholder Treatment": "Review and enhance policies for fair and respectful treatment of all stakeholders.",
                "Social Responsibility": "Develop a comprehensive social responsibility program aligned with divine governance principles."
            },
            "divine_alignment": {
                "Imperial Mandate Alignment": "Conduct a formal review of operations against the Imperial Mandate principles.",
                "Divine Guidance Integration": "Establish a divine guidance council to oversee integration of divine principles.",
                "Harmony Promotion": "Develop programs that actively promote harmony among all stakeholders and communities.",
                "Collective Elevation": "Implement initiatives that contribute to the collective elevation of society."
            }
        }
        
        # Return specific recommendation if available, otherwise generic
        if principle_id in templates and factor_name in templates[principle_id]:
            return templates[principle_id][factor_name]
        
        # Generic recommendation based on score
        if score < 70:
            return f"Significantly improve {factor_name} to better align with {principle_id.replace('_', ' ')} principles."
        elif score < 85:
            return f"Enhance {factor_name} practices to strengthen {principle_id.replace('_', ' ')} alignment."
        else:
            return f"Maintain and continue to refine {factor_name} excellence in support of {principle_id.replace('_', ' ')}."
    
    def get_divine_visualization_data(self, scorecard: Dict) -> Dict:
        """
        Generate data for visualizing divine alignment.
        
        Args:
            scorecard: Scorecard data from evaluate_license
            
        Returns:
            Dict: Visualization data
        """
        principle_scores = scorecard.get("principle_scores", [])
        
        # Extract categories and values for radar chart
        categories = [p["principle_name"] for p in principle_scores]
        values = [p["overall_score"] for p in principle_scores]
        
        # Generate color scale based on scores
        colors = []
        for score in values:
            if score < 70:
                colors.append("#EF4444")  # Red
            elif score < 80:
                colors.append("#F59E0B")  # Amber
            elif score < 90:
                colors.append("#10B981")  # Green
            else:
                colors.append("#6366F1")  # Indigo (exemplary)
        
        # Factor details for each principle
        factor_details = []
        for principle in principle_scores:
            factors = principle.get("factors", [])
            
            factor_detail = {
                "principle_name": principle["principle_name"],
                "factor_names": [f["name"] for f in factors],
                "factor_scores": [f["score"] for f in factors],
                "factor_weights": [f["weight"] for f in factors]
            }
            
            factor_details.append(factor_detail)
        
        return {
            "overall_score": scorecard.get("overall_score", 0),
            "categories": categories,
            "values": values,
            "colors": colors,
            "factor_details": factor_details,
            "timestamp": scorecard.get("timestamp")
        }

# Helper functions
def save_scorecard(scorecard: Dict, output_dir: str = "scorecards") -> str:
    """
    Save a scorecard to the filesystem.
    
    Args:
        scorecard: Scorecard data to save
        output_dir: Directory to save scorecard files
        
    Returns:
        str: Path to saved scorecard file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename based on license ID and timestamp
    license_id = scorecard.get("license_id", "unknown")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{license_id}_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(scorecard, f, indent=2)
    
    return output_path

def load_scorecard(scorecard_path: str) -> Dict:
    """
    Load a scorecard from the filesystem.
    
    Args:
        scorecard_path: Path to scorecard file
        
    Returns:
        Dict: Loaded scorecard data
    """
    with open(scorecard_path, 'r') as f:
        return json.load(f)

# Main function for testing
if __name__ == "__main__":
    # Create a sample license for testing
    sample_license = {
        "id": "GEN-12345",
        "type": "enterprise",
        "holder": {
            "id": "VOI-JEANS-001",
            "name": "VOI Jeans Retail India PVT LTD",
            "contact": "admin@voijeans.com"
        },
        "status": "active",
        "governance_level": "enhanced",
        "permissions": [
            "transaction_governance",
            "channel_management",
            "inventory_sync",
            "financial_reporting",
            "compliance_management",
            "resource_optimization"
        ],
        "metadata": {
            "organization_size": "Enterprise",
            "industry": "Retail",
            "region": "Asia",
            "country": "India",
            "public_reporting": True
        }
    }
    
    # Create scorecard
    scorecard = DivinePrinciplesScorecard()
    
    # Evaluate license
    results = scorecard.evaluate_license(sample_license)
    
    # Print results
    print(f"Overall Score: {results['overall_score']:.2f}")
    print("\nPrinciple Scores:")
    for p in results["principle_scores"]:
        print(f"  {p['principle_name']}: {p['overall_score']:.2f}")
    
    # Generate recommendations
    recommendations = scorecard.generate_recommendations(results)
    
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"  {rec['principle_name']} ({rec['priority']} Priority)")
        print(f"    Target Area: {rec['target_area']}")
        print(f"    Recommendation: {rec['recommendation']}")
        print()
    
    # Save scorecard
    output_path = save_scorecard(results)
    print(f"\nScorecard saved to: {output_path}")