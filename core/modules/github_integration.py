"""
GitHub Integration Module for Empire OS

- Connects with GitHub repositories for code management
- Manages repository floors (hierarchical organization)
- Integrates with license flow for code access control
- Tracks contributions aligned with divine principles
"""

import os
import json
import requests
from datetime import datetime
import hashlib
import random

# Repository floors structure
REPOSITORY_FLOORS = {
    "Floor1": {
        "name": "Divine Core Infrastructure",
        "description": "Foundational infrastructure and core CCPC modules",
        "license_level_required": 4,  # Emperor access only
        "repositories": [
            {"name": "CCPC-001", "description": "Central Computational Processing Core Unit 001"},
            {"name": "RiverOS-Core", "description": "Divine simulation engine core"},
            {"name": "Divine-Mechanics", "description": "Core computational mechanics library"}
        ]
    },
    "Floor2": {
        "name": "Federal Alignment Protocol",
        "description": "Governance and cross-realm alignment systems",
        "license_level_required": 3,  # Governor access
        "repositories": [
            {"name": "Realm-Governance", "description": "Realm governance framework"},
            {"name": "Cross-Realm-Protocol", "description": "Inter-realm communication protocols"},
            {"name": "Balance-Metrics", "description": "Realm balance measurement tools"}
        ]
    },
    "Floor3": {
        "name": "Divine Alignment Layer",
        "description": "Ethical and principle alignment systems",
        "license_level_required": 3,  # Governor access
        "repositories": [
            {"name": "Divine-Principles", "description": "Implementation of divine principle algorithms"},
            {"name": "ESG-Metrics", "description": "ESG impact assessment tools"},
            {"name": "Ethical-Filters", "description": "Decision ethics validation modules"}
        ]
    },
    "Floor4": {
        "name": "Enterprise Operations",
        "description": "Day-to-day operational modules",
        "license_level_required": 2,  # Operator access
        "repositories": [
            {"name": "Inventory-System", "description": "Inventory management modules"},
            {"name": "Transaction-Engine", "description": "Enterprise transaction processing"},
            {"name": "Supply-Chain", "description": "Supply chain management tools"}
        ]
    },
    "Floor5": {
        "name": "Application Layer",
        "description": "User-facing applications and interfaces",
        "license_level_required": 1,  # Viewer access
        "repositories": [
            {"name": "Empire-OS-Dashboard", "description": "Main user dashboard"},
            {"name": "Virtual-Silk-Road", "description": "Marketplace interface"},
            {"name": "Mobile-Interfaces", "description": "Mobile device interfaces"}
        ]
    }
}

class GitHubIntegration:
    def __init__(self, token=None):
        """Initialize with optional GitHub API token"""
        self.api_base = "https://api.github.com"
        self.token = token
        self.headers = {}
        if token:
            self.headers = {"Authorization": f"Bearer {token}"}
        
        # Ensure data directories exist
        os.makedirs('data/github', exist_ok=True)
    
    def get_repository_floors(self, license_level):
        """
        Get accessible repository floors based on license level
        
        Args:
            license_level (int): User's license level
            
        Returns:
            dict: Accessible floors and repositories
        """
        accessible_floors = {}
        
        for floor_id, floor_data in REPOSITORY_FLOORS.items():
            if floor_data["license_level_required"] <= license_level:
                accessible_floors[floor_id] = floor_data
        
        return accessible_floors
    
    def create_repository(self, name, description, floor_id, license_context):
        """
        Create a new repository (simulated) and assign to a floor
        
        Args:
            name (str): Repository name
            description (str): Repository description
            floor_id (str): Floor to assign repository to
            license_context (dict): License context for validation
            
        Returns:
            dict: Result of repository creation
        """
        # Validate license has appropriate level
        license_level = license_context.get("license_level", 0)
        required_level = REPOSITORY_FLOORS.get(floor_id, {}).get("license_level_required", 4)
        
        if license_level < required_level:
            return {
                "success": False,
                "message": f"Insufficient license level. Required: {required_level}, Current: {license_level}"
            }
        
        # In a real implementation, this would call GitHub API
        # For simulation, we'll add to our floors data
        
        # Generate repository ID
        repo_id = hashlib.md5(f"{name}-{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # Create repository record
        repo_data = {
            "id": repo_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "floor_id": floor_id,
            "created_by": license_context.get("role", "unknown"),
            "divine_principle_alignment": self._assign_divine_principle()
        }
        
        # Log the creation
        self._log_repository_action("create", repo_data)
        
        return {
            "success": True,
            "message": f"Repository {name} created on floor {floor_id}",
            "repository": repo_data
        }
    
    def link_external_repository(self, github_url, floor_id, license_context):
        """
        Link an existing external GitHub repository
        
        Args:
            github_url (str): URL to GitHub repository
            floor_id (str): Floor to assign repository to
            license_context (dict): License context for validation
            
        Returns:
            dict: Result of repository linking
        """
        # Validate license has appropriate level
        license_level = license_context.get("license_level", 0)
        required_level = REPOSITORY_FLOORS.get(floor_id, {}).get("license_level_required", 4)
        
        if license_level < required_level:
            return {
                "success": False,
                "message": f"Insufficient license level. Required: {required_level}, Current: {license_level}"
            }
        
        # In a real implementation, this would validate the GitHub URL
        # and pull repository information via GitHub API
        
        # Extract repository name from URL (simplified)
        repo_name = github_url.strip('/').split('/')[-1]
        
        # Generate repository ID
        repo_id = hashlib.md5(f"{github_url}-{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        # Create repository record
        repo_data = {
            "id": repo_id,
            "name": repo_name,
            "external_url": github_url,
            "description": f"External repository: {repo_name}",
            "linked_at": datetime.now().isoformat(),
            "floor_id": floor_id,
            "linked_by": license_context.get("role", "unknown"),
            "divine_principle_alignment": self._assign_divine_principle()
        }
        
        # Log the linking
        self._log_repository_action("link", repo_data)
        
        return {
            "success": True,
            "message": f"External repository {repo_name} linked on floor {floor_id}",
            "repository": repo_data
        }
    
    def get_contribution_metrics(self, repo_id, time_period="last_month"):
        """
        Get contribution metrics for a repository
        
        Args:
            repo_id (str): Repository identifier
            time_period (str): Time period for metrics
            
        Returns:
            dict: Contribution metrics
        """
        # In a real implementation, this would fetch data from GitHub API
        # For simulation, generate plausible metrics
        
        # Contributors (simulated)
        num_contributors = random.randint(3, 15)
        contributors = []
        
        roles = ["factory-operator", "developer", "realm-governor", "tester", "documentation", "architect"]
        
        for i in range(num_contributors):
            contributors.append({
                "name": f"Contributor-{i+1}",
                "role": random.choice(roles),
                "commits": random.randint(5, 100),
                "additions": random.randint(200, 5000),
                "deletions": random.randint(50, 2000),
                "divine_alignment_score": random.randint(70, 99)
            })
        
        # Sort by commits
        contributors.sort(key=lambda x: x["commits"], reverse=True)
        
        # Overall metrics
        total_commits = sum(c["commits"] for c in contributors)
        total_additions = sum(c["additions"] for c in contributors)
        total_deletions = sum(c["deletions"] for c in contributors)
        
        # Calculate divine alignment
        alignment_scores = [c["divine_alignment_score"] for c in contributors]
        avg_alignment = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0
        
        metrics = {
            "repository_id": repo_id,
            "time_period": time_period,
            "total_commits": total_commits,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "contributors": contributors,
            "divine_principle_alignment": {
                "score": avg_alignment,
                "level": self._get_alignment_level(avg_alignment),
                "dominant_principle": self._assign_divine_principle()
            }
        }
        
        return metrics
    
    def _assign_divine_principle(self):
        """Assign a divine principle based on repository characteristics"""
        principles = [
            "Al-Adl (Justice)",
            "Ar-Rahman (Mercy)",
            "Al-Hakim (Wisdom)",
            "Al-Alim (Knowledge)",
            "Al-Muqsit (Equity)"
        ]
        return random.choice(principles)
    
    def _get_alignment_level(self, score):
        """Convert numeric alignment score to level"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Satisfactory"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Critical Misalignment"
    
    def _log_repository_action(self, action, data):
        """Log repository actions to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "repository": data.get("name"),
            "floor_id": data.get("floor_id"),
            "actor": data.get("created_by") or data.get("linked_by", "unknown"),
            "divine_principle_alignment": data.get("divine_principle_alignment")
        }
        
        # Append to log file
        with open('data/github/repository_ledger.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# For testing
if __name__ == "__main__":
    # Test with Emperor-level license
    license_context = {
        "role": "emperor",
        "license_level": 4
    }
    
    github = GitHubIntegration()
    
    # Get accessible floors
    floors = github.get_repository_floors(license_context["license_level"])
    print(f"Accessible floors: {len(floors)}")
    
    # Create a test repository
    result = github.create_repository(
        "Divine-Test-Repo",
        "A test repository for divine mechanics",
        "Floor1",
        license_context
    )
    print(json.dumps(result, indent=2))
    
    # Get contribution metrics
    metrics = github.get_contribution_metrics("test-repo-id")
    print(f"Total commits: {metrics['total_commits']}")
    print(f"Divine alignment: {metrics['divine_principle_alignment']['score']} ({metrics['divine_principle_alignment']['level']})")