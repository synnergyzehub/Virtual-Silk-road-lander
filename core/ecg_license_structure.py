"""
ECG License Structure - Master License Data Structures
====================================================

This module defines the core data structures for the Emperor's Computational Governance (ECG)
licensing framework. These structures serve as the foundation for issuing, tracking, and 
verifying compliance with Divine Principles across all licensed entities.

The license structure is hierarchical and reflects the multi-dimensional nature of divine
alignment, allowing for comprehensive governance across People, Planet, and Profit dimensions.
"""

import json
import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any

# Define license status and types
class LicenseStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"

class LicenseType(Enum):
    CORPORATE = "corporate"       # For businesses and organizations
    INDIVIDUAL = "individual"     # For personal use
    GOVERNMENT = "government"     # For government entities
    NONPROFIT = "nonprofit"       # For non-profit organizations
    EDUCATIONAL = "educational"   # For educational institutions
    RESEARCH = "research"         # For research institutions
    DEVELOPER = "developer"       # For software developers

class ComplianceTier(Enum):
    TIER_1 = "tier_1"  # Basic compliance
    TIER_2 = "tier_2"  # Intermediate compliance
    TIER_3 = "tier_3"  # Advanced compliance
    TIER_4 = "tier_4"  # Expert compliance
    TIER_5 = "tier_5"  # Master compliance

class DivinePrinciple(Enum):
    """The 99 names/attributes translated to governance principles"""
    JUSTICE = "justice"           # عدل - Justice
    MERCY = "mercy"               # رحمن - Mercy
    ALL_KNOWING = "all_knowing"   # علیم - All-Knowing
    ALL_SEEING = "all_seeing"     # بصیر - All-Seeing
    MOST_GENEROUS = "most_generous" # کریم - Most Generous
    TRUTH = "truth"               # حق - Truth
    PEACE = "peace"               # سلام - Peace
    PROVIDER = "provider"         # رزاق - Provider
    PRESERVER = "preserver"       # حفيظ - Preserver
    # Additional divine principles can be added as needed

class GovernanceDimension(Enum):
    """The three core dimensions of sustainable governance"""
    PEOPLE = "people"
    PLANET = "planet"
    PROFIT = "profit"

# Core data structures

class DivinePrincipleCompliance:
    """Tracks compliance with a specific divine principle"""
    
    def __init__(
        self,
        principle: DivinePrinciple,
        score: float,  # 0-100 compliance score
        last_evaluated: datetime.datetime,
        evidence: List[str],  # References to evidence of compliance
        improvement_actions: List[str]  # Suggested actions to improve compliance
    ):
        self.principle = principle
        self.score = score
        self.last_evaluated = last_evaluated
        self.evidence = evidence
        self.improvement_actions = improvement_actions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "principle": self.principle.value,
            "score": self.score,
            "last_evaluated": self.last_evaluated.isoformat(),
            "evidence": self.evidence,
            "improvement_actions": self.improvement_actions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DivinePrincipleCompliance':
        """Create from dictionary"""
        return cls(
            principle=DivinePrinciple(data["principle"]),
            score=data["score"],
            last_evaluated=datetime.datetime.fromisoformat(data["last_evaluated"]),
            evidence=data["evidence"],
            improvement_actions=data["improvement_actions"]
        )

class DimensionCompliance:
    """Tracks compliance across a governance dimension (People, Planet, Profit)"""
    
    def __init__(
        self,
        dimension: GovernanceDimension,
        principles: List[DivinePrincipleCompliance],
        overall_score: float,  # Weighted average of principle scores
        weight: float  # Importance weight in overall compliance (0-1)
    ):
        self.dimension = dimension
        self.principles = principles
        self.overall_score = overall_score
        self.weight = weight
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "dimension": self.dimension.value,
            "principles": [p.to_dict() for p in self.principles],
            "overall_score": self.overall_score,
            "weight": self.weight
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DimensionCompliance':
        """Create from dictionary"""
        return cls(
            dimension=GovernanceDimension(data["dimension"]),
            principles=[DivinePrincipleCompliance.from_dict(p) for p in data["principles"]],
            overall_score=data["overall_score"],
            weight=data["weight"]
        )

class ComplianceAudit:
    """Represents a compliance audit event"""
    
    def __init__(
        self,
        audit_id: str,
        timestamp: datetime.datetime,
        auditor: str,  # Who performed the audit
        dimensions: List[DimensionCompliance],
        overall_score: float,
        findings: List[str],
        recommendations: List[str],
        next_audit_date: datetime.datetime
    ):
        self.audit_id = audit_id
        self.timestamp = timestamp
        self.auditor = auditor
        self.dimensions = dimensions
        self.overall_score = overall_score
        self.findings = findings
        self.recommendations = recommendations
        self.next_audit_date = next_audit_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp.isoformat(),
            "auditor": self.auditor,
            "dimensions": [d.to_dict() for d in self.dimensions],
            "overall_score": self.overall_score,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "next_audit_date": self.next_audit_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ComplianceAudit':
        """Create from dictionary"""
        return cls(
            audit_id=data["audit_id"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            auditor=data["auditor"],
            dimensions=[DimensionCompliance.from_dict(d) for d in data["dimensions"]],
            overall_score=data["overall_score"],
            findings=data["findings"],
            recommendations=data["recommendations"],
            next_audit_date=datetime.datetime.fromisoformat(data["next_audit_date"])
        )

class License:
    """The core license structure issued by ECG"""
    
    def __init__(
        self,
        license_id: str,
        entity_name: str,
        entity_id: str,
        license_type: LicenseType,
        issue_date: datetime.datetime,
        expiry_date: datetime.datetime,
        status: LicenseStatus,
        compliance_tier: ComplianceTier,
        current_compliance_score: float,
        compliance_history: List[ComplianceAudit],
        authorized_modules: List[str],  # Modules/features this license authorizes
        restrictions: List[str],  # Any specific restrictions on use
        digital_signature: str,  # Emperor's digital signature
        meta: Dict[str, Any]  # Additional metadata
    ):
        self.license_id = license_id
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.license_type = license_type
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.status = status
        self.compliance_tier = compliance_tier
        self.current_compliance_score = current_compliance_score
        self.compliance_history = compliance_history
        self.authorized_modules = authorized_modules
        self.restrictions = restrictions
        self.digital_signature = digital_signature
        self.meta = meta
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "license_id": self.license_id,
            "entity_name": self.entity_name,
            "entity_id": self.entity_id,
            "license_type": self.license_type.value,
            "issue_date": self.issue_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat(),
            "status": self.status.value,
            "compliance_tier": self.compliance_tier.value,
            "current_compliance_score": self.current_compliance_score,
            "compliance_history": [ch.to_dict() for ch in self.compliance_history],
            "authorized_modules": self.authorized_modules,
            "restrictions": self.restrictions,
            "digital_signature": self.digital_signature,
            "meta": self.meta
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'License':
        """Create from dictionary"""
        return cls(
            license_id=data["license_id"],
            entity_name=data["entity_name"],
            entity_id=data["entity_id"],
            license_type=LicenseType(data["license_type"]),
            issue_date=datetime.datetime.fromisoformat(data["issue_date"]),
            expiry_date=datetime.datetime.fromisoformat(data["expiry_date"]),
            status=LicenseStatus(data["status"]),
            compliance_tier=ComplianceTier(data["compliance_tier"]),
            current_compliance_score=data["current_compliance_score"],
            compliance_history=[ComplianceAudit.from_dict(ch) for ch in data["compliance_history"]],
            authorized_modules=data["authorized_modules"],
            restrictions=data["restrictions"],
            digital_signature=data["digital_signature"],
            meta=data["meta"]
        )
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'License':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))
    
    @property
    def is_valid(self) -> bool:
        """Check if license is currently valid"""
        now = datetime.datetime.now()
        return (
            self.status == LicenseStatus.ACTIVE and
            self.issue_date <= now <= self.expiry_date
        )
    
    def get_latest_audit(self) -> Optional[ComplianceAudit]:
        """Get the most recent compliance audit"""
        if not self.compliance_history:
            return None
        return max(self.compliance_history, key=lambda audit: audit.timestamp)


class LicenseManager:
    """Manages license issuance, validation, and compliance tracking"""
    
    def __init__(self):
        self.licenses: Dict[str, License] = {}  # license_id -> License
    
    def issue_license(
        self,
        entity_name: str,
        entity_id: str,
        license_type: LicenseType,
        expiry_date: datetime.datetime,
        compliance_tier: ComplianceTier,
        authorized_modules: List[str],
        restrictions: List[str] = None,
        meta: Dict[str, Any] = None
    ) -> License:
        """Issue a new license"""
        # Initialize default values for optional parameters
        if restrictions is None:
            restrictions = []
        if meta is None:
            meta = {}
        from uuid import uuid4
        import hashlib
        
        license_id = f"ECG-{uuid4().hex[:8].upper()}"
        issue_date = datetime.datetime.now()
        
        # Create a digital signature (simplified for demonstration)
        signature_data = f"{license_id}:{entity_id}:{issue_date.isoformat()}:{expiry_date.isoformat()}"
        digital_signature = hashlib.sha256(signature_data.encode()).hexdigest()
        
        # Create initial compliance audit
        initial_audit = self._create_initial_audit(entity_id)
        
        license = License(
            license_id=license_id,
            entity_name=entity_name,
            entity_id=entity_id,
            license_type=license_type,
            issue_date=issue_date,
            expiry_date=expiry_date,
            status=LicenseStatus.ACTIVE,
            compliance_tier=compliance_tier,
            current_compliance_score=initial_audit.overall_score,
            compliance_history=[initial_audit],
            authorized_modules=authorized_modules,
            restrictions=restrictions or [],
            digital_signature=digital_signature,
            meta=meta or {}
        )
        
        self.licenses[license_id] = license
        return license
    
    def _create_initial_audit(self, entity_id: str) -> ComplianceAudit:
        """Create an initial compliance audit"""
        from uuid import uuid4
        
        audit_id = f"AUDIT-{uuid4().hex[:8].upper()}"
        now = datetime.datetime.now()
        next_audit = now + datetime.timedelta(days=90)  # Default to quarterly audits
        
        # Create principle compliances for each dimension
        dimensions = []
        
        for dimension in GovernanceDimension:
            principles = []
            
            # Create principle compliances for each dimension
            for principle in [DivinePrinciple.JUSTICE, DivinePrinciple.MERCY, DivinePrinciple.ALL_KNOWING]:
                # Initial scores are set at baseline compliance (70%)
                principles.append(DivinePrincipleCompliance(
                    principle=principle,
                    score=70.0,  # Initial baseline compliance score
                    last_evaluated=now,
                    evidence=["Initial assessment"],
                    improvement_actions=["Establish baseline metrics", "Develop compliance roadmap"]
                ))
            
            # Dimension overall score is average of principle scores
            overall_score = sum(p.score for p in principles) / len(principles)
            
            # Dimension weights (simplified)
            weight = 1.0 / len(GovernanceDimension)
            
            dimensions.append(DimensionCompliance(
                dimension=dimension,
                principles=principles,
                overall_score=overall_score,
                weight=weight
            ))
        
        # Overall audit score is weighted average of dimension scores
        overall_score = sum(d.overall_score * d.weight for d in dimensions)
        
        return ComplianceAudit(
            audit_id=audit_id,
            timestamp=now,
            auditor="ECG Automated System",
            dimensions=dimensions,
            overall_score=overall_score,
            findings=["Initial compliance assessment"],
            recommendations=["Establish governance framework", "Implement monitoring systems"],
            next_audit_date=next_audit
        )
    
    def validate_license(self, license_id: str) -> tuple[bool, str]:
        """Validate a license and return (is_valid, message)"""
        if license_id not in self.licenses:
            return False, "License not found"
        
        license = self.licenses[license_id]
        
        if not license.is_valid:
            return False, f"License is not valid. Status: {license.status.value}"
        
        # Check if license is expired
        now = datetime.datetime.now()
        if now > license.expiry_date:
            license.status = LicenseStatus.EXPIRED
            return False, "License has expired"
        
        # Check minimum compliance score
        if license.current_compliance_score < 60:  # Minimum compliance threshold
            license.status = LicenseStatus.SUSPENDED
            return False, f"License compliance score ({license.current_compliance_score}) is below minimum threshold"
        
        return True, "License is valid"
    
    def perform_audit(
        self, 
        license_id: str,
        auditor: str,
        dimension_scores: Dict[str, Dict[str, float]],  # dimension -> principle -> score
        findings: List[str],
        recommendations: List[str]
    ) -> ComplianceAudit:
        """Perform a compliance audit for a license"""
        from uuid import uuid4
        
        if license_id not in self.licenses:
            raise ValueError(f"License {license_id} not found")
        
        license = self.licenses[license_id]
        now = datetime.datetime.now()
        audit_id = f"AUDIT-{uuid4().hex[:8].upper()}"
        next_audit = now + datetime.timedelta(days=90)  # Default to quarterly audits
        
        # Create dimension compliances based on provided scores
        dimensions = []
        
        for dim_name, principle_scores in dimension_scores.items():
            dimension = GovernanceDimension(dim_name)
            principles = []
            
            for principle_name, score in principle_scores.items():
                principle = DivinePrinciple(principle_name)
                
                # Find improvement actions based on score
                improvement_actions = []
                if score < 60:
                    improvement_actions.append("Critical improvement needed")
                elif score < 80:
                    improvement_actions.append("Room for improvement")
                else:
                    improvement_actions.append("Maintain current practices")
                
                principles.append(DivinePrincipleCompliance(
                    principle=principle,
                    score=score,
                    last_evaluated=now,
                    evidence=[f"Audit by {auditor}"],
                    improvement_actions=improvement_actions
                ))
            
            # Calculate dimension overall score
            overall_score = sum(p.score for p in principles) / len(principles)
            
            # Use existing weights if available
            previous_audit = license.get_latest_audit()
            weight = 1.0 / len(GovernanceDimension)  # Default
            
            if previous_audit:
                for dim in previous_audit.dimensions:
                    if dim.dimension == dimension:
                        weight = dim.weight
                        break
            
            dimensions.append(DimensionCompliance(
                dimension=dimension,
                principles=principles,
                overall_score=overall_score,
                weight=weight
            ))
        
        # Overall audit score is weighted average of dimension scores
        overall_score = sum(d.overall_score * d.weight for d in dimensions)
        
        audit = ComplianceAudit(
            audit_id=audit_id,
            timestamp=now,
            auditor=auditor,
            dimensions=dimensions,
            overall_score=overall_score,
            findings=findings,
            recommendations=recommendations,
            next_audit_date=next_audit
        )
        
        # Update license with new audit
        license.compliance_history.append(audit)
        license.current_compliance_score = overall_score
        
        # Update license status based on compliance score
        if overall_score < 40:
            license.status = LicenseStatus.REVOKED
        elif overall_score < 60:
            license.status = LicenseStatus.SUSPENDED
        else:
            license.status = LicenseStatus.ACTIVE
        
        return audit
    
    def save_licenses(self, filepath: str) -> None:
        """Save all licenses to a JSON file"""
        data = {license_id: license.to_dict() for license_id, license in self.licenses.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_licenses(self, filepath: str) -> None:
        """Load licenses from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.licenses = {
            license_id: License.from_dict(license_data)
            for license_id, license_data in data.items()
        }

# Example usage:
def create_sample_license() -> License:
    """Create a sample license for demonstration purposes"""
    manager = LicenseManager()
    
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=365)
    
    return manager.issue_license(
        entity_name="Voi Jeans Retail India Pvt Ltd",
        entity_id="VOI-JEANS-001",
        license_type=LicenseType.CORPORATE,
        expiry_date=expiry_date,
        compliance_tier=ComplianceTier.TIER_3,
        authorized_modules=[
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
        meta={
            "industry": "Retail & Manufacturing",
            "primary_contact": "John Doe",
            "region": "Asia-Pacific",
            "employees": 500
        }
    )

if __name__ == "__main__":
    # Create and print a sample license
    sample_license = create_sample_license()
    print(sample_license.to_json())