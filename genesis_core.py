"""
Genesis Empowerment Matrix & Virtual Silk Road Core

This module defines the core configuration and functionality for the
Genesis Empowerment Matrix and Virtual Silk Road simulation system.
"""

import logging
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("genesis_core")

# --- CONFIG: Minimum Requirements for License Operability ---
MIN_DATASETS_REQUIRED = 300
DEPARTMENT_SCORE_THRESHOLD = 70.0  # Minimum average score per department

# Governance level weights (optional)
GOVERNANCE_WEIGHTS = {
    "policy": 1.5,
    "strategic": 1.2,
    "operational": 1.0
}

class SilkRoadStage(Enum):
    """
    Enumeration of Virtual Silk Road progression stages.
    Each department progresses through these stages in the gamified system.
    """
    CHECKPOINT_ENTRY = "checkpoint_entry"
    CHECKPOINT_REVIEW = "checkpoint_review"
    ASSEMBLY_RITUAL = "assembly_ritual"
    GOVERNANCE_GRANT = "governance_grant"
    OPERABILITY_UNLOCK = "operability_unlock"

# List of stage values for easy iteration
SILK_ROAD_STAGES = [stage.value for stage in SilkRoadStage]

class DepartmentType(Enum):
    """Department types in the organization structure"""
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    DISTRIBUTION = "distribution"
    FINANCE = "finance"
    GOVERNANCE = "governance"
    TECHNOLOGY = "technology"
    DESIGN = "design"

class GovernanceLevel(Enum):
    """Governance levels for organizational entities"""
    POLICY = "policy"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"


class GenesisMatrix:
    """
    Core class for handling the Genesis Empowerment Matrix calculations
    and Virtual Silk Road progression tracking.
    """
    
    def __init__(self, realm_id: str, license_id: str):
        """
        Initialize a new Genesis Matrix instance.
        
        Args:
            realm_id: The identifier for the realm (organizational unit)
            license_id: The associated license identifier
        """
        self.realm_id = realm_id
        self.license_id = license_id
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.departments = {}
        self.dataset_count = 0
        self.operability_status = False
        
        logger.info(f"Genesis Matrix initialized for realm {realm_id} with license {license_id}")
    
    def add_department(self, 
                      name: str, 
                      dept_type: DepartmentType,
                      governance_level: GovernanceLevel) -> bool:
        """
        Add a new department to the matrix.
        
        Args:
            name: Department name
            dept_type: Department type from DepartmentType enum
            governance_level: Governance level from GovernanceLevel enum
            
        Returns:
            bool: Success status
        """
        if name in self.departments:
            logger.warning(f"Department {name} already exists in realm {self.realm_id}")
            return False
        
        # Create new department record
        self.departments[name] = {
            "type": dept_type.value,
            "governance_level": governance_level.value,
            "score": 0.0,
            "datasets": 0,
            "silk_road_stage": SilkRoadStage.CHECKPOINT_ENTRY.value,
            "users": [],
            "modules": []
        }
        
        self.last_updated = datetime.now()
        logger.info(f"Department {name} added to realm {self.realm_id}")
        return True
    
    def update_department_score(self, department: str, score: float) -> bool:
        """
        Update a department's score.
        
        Args:
            department: Department name
            score: New score (0-100)
            
        Returns:
            bool: Success status
        """
        if department not in self.departments:
            logger.error(f"Department {department} not found in realm {self.realm_id}")
            return False
        
        # Validate score
        if not 0 <= score <= 100:
            logger.error(f"Invalid score {score} for department {department}. Must be 0-100.")
            return False
        
        self.departments[department]["score"] = score
        self.last_updated = datetime.now()
        
        # Check if this enables progression in the Silk Road
        self._check_stage_progression(department)
        
        logger.info(f"Updated score for department {department} to {score}")
        return True
    
    def add_dataset(self, department: str) -> bool:
        """
        Register a new dataset for a department.
        
        Args:
            department: Department name
            
        Returns:
            bool: Success status
        """
        if department not in self.departments:
            logger.error(f"Department {department} not found in realm {self.realm_id}")
            return False
        
        self.departments[department]["datasets"] += 1
        self.dataset_count += 1
        self.last_updated = datetime.now()
        
        # Check if this enables progression in the Silk Road
        self._check_stage_progression(department)
        
        logger.info(f"Added dataset to department {department}. Total: {self.departments[department]['datasets']}")
        return True
    
    def _check_stage_progression(self, department: str) -> None:
        """
        Check if a department can progress to the next Silk Road stage.
        
        Args:
            department: Department name
        """
        if department not in self.departments:
            return
        
        dept = self.departments[department]
        current_stage = dept["silk_road_stage"]
        
        # Find current stage index
        try:
            current_index = SILK_ROAD_STAGES.index(current_stage)
        except ValueError:
            logger.error(f"Unknown silk road stage: {current_stage}")
            return
        
        # If already at the last stage, no progression possible
        if current_index >= len(SILK_ROAD_STAGES) - 1:
            return
        
        # Determine if conditions are met for progression
        can_progress = False
        
        if current_stage == SilkRoadStage.CHECKPOINT_ENTRY.value:
            # Progress to CHECKPOINT_REVIEW if score exceeds threshold
            can_progress = dept["score"] >= DEPARTMENT_SCORE_THRESHOLD
        
        elif current_stage == SilkRoadStage.CHECKPOINT_REVIEW.value:
            # Progress to ASSEMBLY_RITUAL if enough datasets
            min_dept_datasets = MIN_DATASETS_REQUIRED // max(1, len(self.departments))
            can_progress = dept["datasets"] >= min_dept_datasets
        
        elif current_stage == SilkRoadStage.ASSEMBLY_RITUAL.value:
            # Progress to GOVERNANCE_GRANT if users are assigned
            can_progress = len(dept["users"]) > 0
        
        elif current_stage == SilkRoadStage.GOVERNANCE_GRANT.value:
            # Progress to OPERABILITY_UNLOCK if modules are assigned
            can_progress = len(dept["modules"]) > 0
        
        # Perform progression if conditions are met
        if can_progress:
            next_stage = SILK_ROAD_STAGES[current_index + 1]
            dept["silk_road_stage"] = next_stage
            logger.info(f"Department {department} progressed to {next_stage}")
            
            # Check if realm is now operable
            self._check_realm_operability()
    
    def _check_realm_operability(self) -> None:
        """Check if the entire realm meets operability requirements"""
        if not self.departments:
            return
        
        # Check total dataset count
        if self.dataset_count < MIN_DATASETS_REQUIRED:
            return
        
        # Check if all departments exceed score threshold
        avg_score = sum(dept["score"] for dept in self.departments.values()) / len(self.departments)
        if avg_score < DEPARTMENT_SCORE_THRESHOLD:
            return
        
        # Check if all departments have reached at least GOVERNANCE_GRANT stage
        governance_stage_index = SILK_ROAD_STAGES.index(SilkRoadStage.GOVERNANCE_GRANT.value)
        min_required_stage = SILK_ROAD_STAGES[governance_stage_index]
        
        for dept in self.departments.values():
            current_index = SILK_ROAD_STAGES.index(dept["silk_road_stage"])
            required_index = SILK_ROAD_STAGES.index(min_required_stage)
            
            if current_index < required_index:
                return
        
        # All conditions are met
        self.operability_status = True
        logger.info(f"Realm {self.realm_id} has achieved operability status")
    
    def get_weighted_score(self) -> float:
        """
        Calculate the weighted score for the realm based on governance levels.
        
        Returns:
            float: Weighted score
        """
        if not self.departments:
            return 0.0
        
        total_weight = 0
        weighted_sum = 0
        
        for dept in self.departments.values():
            level = dept["governance_level"]
            score = dept["score"]
            weight = GOVERNANCE_WEIGHTS.get(level, 1.0)
            
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    def get_silk_road_progress(self) -> Dict[str, Dict]:
        """
        Get a summary of Silk Road progress for all departments.
        
        Returns:
            Dict: Department progress information
        """
        progress = {}
        
        for name, dept in self.departments.items():
            current_stage = dept["silk_road_stage"]
            current_index = SILK_ROAD_STAGES.index(current_stage)
            total_stages = len(SILK_ROAD_STAGES)
            
            progress[name] = {
                "current_stage": current_stage,
                "progress_pct": (current_index / (total_stages - 1)) * 100,
                "next_stage": SILK_ROAD_STAGES[current_index + 1] if current_index < total_stages - 1 else None
            }
        
        return progress
    
    def get_matrix_summary(self) -> Dict:
        """
        Get a complete summary of the Genesis Matrix status.
        
        Returns:
            Dict: Complete matrix status
        """
        return {
            "realm_id": self.realm_id,
            "license_id": self.license_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "department_count": len(self.departments),
            "dataset_count": self.dataset_count,
            "operability_status": self.operability_status,
            "avg_score": sum(d["score"] for d in self.departments.values()) / max(1, len(self.departments)),
            "weighted_score": self.get_weighted_score(),
            "silk_road_progress": self.get_silk_road_progress()
        }


# Utility functions
def calculate_divine_alignment(matrix: GenesisMatrix) -> float:
    """
    Calculate the divine alignment score for a Genesis Matrix.
    This represents how well the realm aligns with divine governance principles.
    
    Args:
        matrix: The Genesis Matrix to analyze
        
    Returns:
        float: Divine alignment score (0-100)
    """
    if not matrix.departments:
        return 0.0
    
    # Base calculations
    weighted_score = matrix.get_weighted_score()
    
    # Department stage balance (reward even progression)
    stage_counts = {}
    for dept in matrix.departments.values():
        stage = dept["silk_road_stage"]
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
    
    # Penalize uneven distribution across stages
    stage_balance = 100.0
    if stage_counts:
        ideal_count = len(matrix.departments) / len(SILK_ROAD_STAGES)
        variance = sum((count - ideal_count) ** 2 for count in stage_counts.values())
        stage_balance = max(0, 100 - (variance * 10))
    
    # Calculate divine alignment score
    divine_alignment = (weighted_score * 0.7) + (stage_balance * 0.3)
    
    return min(100.0, max(0.0, divine_alignment))


def check_license_validity(matrix: GenesisMatrix) -> Tuple[bool, str]:
    """
    Check if a license is valid based on matrix status.
    
    Args:
        matrix: The Genesis Matrix to check
        
    Returns:
        Tuple[bool, str]: (is_valid, reason)
    """
    if not matrix.operability_status:
        return False, "Matrix has not achieved operability status"
    
    # Check if score exceeds threshold
    weighted_score = matrix.get_weighted_score()
    if weighted_score < DEPARTMENT_SCORE_THRESHOLD:
        return False, f"Weighted score {weighted_score:.1f} below threshold {DEPARTMENT_SCORE_THRESHOLD}"
    
    divine_alignment = calculate_divine_alignment(matrix)
    if divine_alignment < 60.0:
        return False, f"Divine alignment score {divine_alignment:.1f} below acceptable threshold"
    
    return True, "License is valid and in good standing"