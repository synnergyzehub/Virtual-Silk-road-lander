"""
Subscription Manager for Empire OS

This module handles the subscription management system for Empire OS,
providing a freemium model with multiple tiers of access to the system's features.

Tiers:
- Free Demo: Limited access to visualize sample data flow and basic insights
- Basic Subscription: Data integration and organization with monthly insights
- Premium Subscription: Full system access with advanced analytics and governance
"""

import os
import json
from datetime import datetime, timedelta
from enum import Enum

class SubscriptionTier(Enum):
    """Subscription tier levels"""
    FREE_DEMO = "free_demo"
    BASIC = "basic"
    PREMIUM = "premium"

class FeatureAccess(Enum):
    """Feature access levels"""
    NONE = 0
    LIMITED = 1
    PARTIAL = 2
    FULL = 3

class SubscriptionManager:
    """Manages user subscriptions and feature access"""
    
    def __init__(self, data_dir='data/subscriptions'):
        """Initialize the subscription manager"""
        self.data_dir = data_dir
        self._ensure_data_dir()
        self.feature_matrix = self._init_feature_matrix()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _init_feature_matrix(self):
        """Initialize the feature access matrix"""
        return {
            # Data Visualization Features
            "factory_visualization": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "distribution_visualization": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "retail_visualization": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "consumer_visualization": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            
            # Analytics Features
            "basic_insights": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.FULL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "advanced_analytics": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "predictive_insights": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.NONE,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            
            # Data Integration Features
            "data_import": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.FULL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "data_export": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "multi_source_integration": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.NONE,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            
            # Divine Mechanics Features
            "river_os_simulation": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "divine_alignment_score": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.LIMITED,
                SubscriptionTier.BASIC: FeatureAccess.PARTIAL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "governance_recommendations": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.LIMITED,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            
            # Reporting Features
            "standard_reports": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.FULL,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "custom_reports": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.NONE,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            },
            "automated_reporting": {
                SubscriptionTier.FREE_DEMO: FeatureAccess.NONE,
                SubscriptionTier.BASIC: FeatureAccess.LIMITED,
                SubscriptionTier.PREMIUM: FeatureAccess.FULL
            }
        }
    
    def create_subscription(self, client_id, tier=SubscriptionTier.FREE_DEMO.value, 
                          duration_days=30, contact_email=None):
        """Create a new subscription for a client"""
        today = datetime.now()
        expiry_date = today + timedelta(days=duration_days)
        
        subscription = {
            "client_id": client_id,
            "tier": tier,
            "start_date": today.isoformat(),
            "expiry_date": expiry_date.isoformat(),
            "status": "active",
            "contact_email": contact_email,
            "features_used": {},
            "last_updated": today.isoformat()
        }
        
        # Save to file
        file_path = os.path.join(self.data_dir, f"{client_id}.json")
        with open(file_path, 'w') as f:
            json.dump(subscription, f, indent=2)
            
        return subscription
    
    def get_subscription(self, client_id):
        """Get the subscription details for a client"""
        file_path = os.path.join(self.data_dir, f"{client_id}.json")
        try:
            with open(file_path, 'r') as f:
                subscription = json.load(f)
            return subscription
        except FileNotFoundError:
            return None
    
    def update_subscription(self, client_id, tier=None, extend_days=None):
        """Update a client's subscription tier or extend duration"""
        subscription = self.get_subscription(client_id)
        if not subscription:
            return None
        
        if tier:
            subscription["tier"] = tier
        
        if extend_days:
            expiry_date = datetime.fromisoformat(subscription["expiry_date"])
            new_expiry = expiry_date + timedelta(days=extend_days)
            subscription["expiry_date"] = new_expiry.isoformat()
        
        subscription["last_updated"] = datetime.now().isoformat()
        
        # Save to file
        file_path = os.path.join(self.data_dir, f"{client_id}.json")
        with open(file_path, 'w') as f:
            json.dump(subscription, f, indent=2)
            
        return subscription
    
    def check_feature_access(self, client_id, feature_name):
        """Check if a client has access to a specific feature"""
        subscription = self.get_subscription(client_id)
        if not subscription:
            return FeatureAccess.NONE
        
        tier = subscription["tier"]
        if tier not in [t.value for t in SubscriptionTier]:
            return FeatureAccess.NONE
        
        if subscription["status"] != "active":
            return FeatureAccess.NONE
            
        if feature_name not in self.feature_matrix:
            return FeatureAccess.NONE
            
        # Log feature usage
        if "features_used" not in subscription:
            subscription["features_used"] = {}
        
        if feature_name not in subscription["features_used"]:
            subscription["features_used"][feature_name] = 0
        
        subscription["features_used"][feature_name] += 1
        
        # Save updated usage
        file_path = os.path.join(self.data_dir, f"{client_id}.json")
        with open(file_path, 'w') as f:
            json.dump(subscription, f, indent=2)
        
        # Return access level
        tier_enum = SubscriptionTier(tier)
        return self.feature_matrix[feature_name][tier_enum]
    
    def list_accessible_features(self, client_id):
        """List all features a client has access to based on their subscription"""
        subscription = self.get_subscription(client_id)
        if not subscription:
            return []
        
        if subscription["status"] != "active":
            return []
            
        tier = SubscriptionTier(subscription["tier"])
        accessible = []
        
        for feature, access_levels in self.feature_matrix.items():
            if access_levels[tier] != FeatureAccess.NONE:
                accessible.append({
                    "feature": feature,
                    "access_level": access_levels[tier].name,
                    "access_value": access_levels[tier].value
                })
                
        return accessible
    
    def get_tier_comparison(self):
        """Get a comparison of features across subscription tiers"""
        comparison = {}
        
        for feature, access_levels in self.feature_matrix.items():
            comparison[feature] = {
                tier.name: level.name 
                for tier, level in access_levels.items()
            }
            
        return comparison


# Pricing information for the subscription tiers
SUBSCRIPTION_PRICING = {
    SubscriptionTier.FREE_DEMO.value: {
        "monthly": 0,
        "annual": 0,
        "setup_fee": 0,
        "description": "Experience the power of data visualization and divine mechanics with our free demo."
    },
    SubscriptionTier.BASIC.value: {
        "monthly": 499,
        "annual": 4999,
        "setup_fee": 999,
        "description": "Organize your data and gain basic insights with our simplified integration and reporting."
    },
    SubscriptionTier.PREMIUM.value: {
        "monthly": 1999,
        "annual": 19999,
        "setup_fee": 4999,
        "description": "Unlock the full potential of divine governance with complete data integration and advanced analytics."
    }
}