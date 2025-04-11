"""
Genesis Smart Data Validation Engine

This module provides the validation rules and engine for the Genesis Smart Data Validation
Tooltip System, ensuring data meets both technical requirements and divine alignment principles.
"""

import re
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Union, Any, Callable, Optional

class ValidationRule:
    """Base class for validation rules"""
    
    def __init__(self, error_message: str):
        self.error_message = error_message
    
    def validate(self, value: Any) -> bool:
        """Validate the value against this rule"""
        raise NotImplementedError("Subclasses must implement validate()")
    
    def get_error_message(self) -> str:
        """Get the error message for this rule"""
        return self.error_message

class RequiredRule(ValidationRule):
    """Rule to check if a value is present"""
    
    def __init__(self, error_message: str = "This field is required"):
        super().__init__(error_message)
    
    def validate(self, value: Any) -> bool:
        """Check if value is not None and not empty"""
        if value is None:
            return False
        
        if isinstance(value, str) and value.strip() == "":
            return False
            
        return True

class PatternRule(ValidationRule):
    """Rule to check if a value matches a regex pattern"""
    
    def __init__(self, pattern: str, error_message: str = "Invalid format"):
        super().__init__(error_message)
        self.pattern = pattern
        self.regex = re.compile(pattern)
    
    def validate(self, value: Any) -> bool:
        """Check if value matches the pattern"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
        
        if not isinstance(value, str):
            value = str(value)
            
        return bool(self.regex.match(value))

class RangeRule(ValidationRule):
    """Rule to check if a numeric value is within a specified range"""
    
    def __init__(self, 
                 min_value: Optional[float] = None, 
                 max_value: Optional[float] = None, 
                 error_message: Optional[str] = None):
        if error_message is None:
            if min_value is not None and max_value is not None:
                error_message = f"Value must be between {min_value} and {max_value}"
            elif min_value is not None:
                error_message = f"Value must be greater than or equal to {min_value}"
            elif max_value is not None:
                error_message = f"Value must be less than or equal to {max_value}"
            else:
                error_message = "Invalid value"
                
        super().__init__(error_message)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> bool:
        """Check if value is within the specified range"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
        
        try:
            # Convert to float for comparison
            num_value = float(value)
            
            if self.min_value is not None and num_value < self.min_value:
                return False
                
            if self.max_value is not None and num_value > self.max_value:
                return False
                
            return True
        except (ValueError, TypeError):
            return False

class LengthRule(ValidationRule):
    """Rule to check if a string value has a valid length"""
    
    def __init__(self, 
                 min_length: Optional[int] = None, 
                 max_length: Optional[int] = None, 
                 error_message: Optional[str] = None):
        if error_message is None:
            if min_length is not None and max_length is not None:
                error_message = f"Length must be between {min_length} and {max_length} characters"
            elif min_length is not None:
                error_message = f"Length must be at least {min_length} characters"
            elif max_length is not None:
                error_message = f"Length must be at most {max_length} characters"
            else:
                error_message = "Invalid length"
                
        super().__init__(error_message)
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> bool:
        """Check if value length is within the specified range"""
        if value is None:
            return self.min_length is None  # Only valid if no minimum length
        
        if not isinstance(value, str):
            value = str(value)
            
        length = len(value)
        
        if self.min_length is not None and length < self.min_length:
            return False
            
        if self.max_length is not None and length > self.max_length:
            return False
            
        return True

class OptionRule(ValidationRule):
    """Rule to check if a value is one of the allowed options"""
    
    def __init__(self, options: List[Any], error_message: Optional[str] = None):
        if error_message is None:
            error_message = f"Value must be one of: {', '.join(str(o) for o in options)}"
            
        super().__init__(error_message)
        self.options = options
    
    def validate(self, value: Any) -> bool:
        """Check if value is in the list of allowed options"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
            
        return value in self.options

class CustomRule(ValidationRule):
    """Rule using a custom validation function"""
    
    def __init__(self, validator_fn: Callable[[Any], bool], error_message: str):
        super().__init__(error_message)
        self.validator_fn = validator_fn
    
    def validate(self, value: Any) -> bool:
        """Run the custom validation function"""
        return self.validator_fn(value)

class DateFormatRule(ValidationRule):
    """Rule to check if a string value is a valid date in specified format"""
    
    def __init__(self, 
                 date_format: str = "%Y-%m-%d", 
                 error_message: Optional[str] = None):
        if error_message is None:
            error_message = f"Date must be in format: {date_format}"
            
        super().__init__(error_message)
        self.date_format = date_format
    
    def validate(self, value: Any) -> bool:
        """Check if value is a valid date in the specified format"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
        
        if not isinstance(value, str):
            return False
            
        try:
            datetime.strptime(value, self.date_format)
            return True
        except ValueError:
            return False

class WTOComplianceRule(ValidationRule):
    """Rule to check if a value complies with WTO regional requirements"""
    
    def __init__(self, 
                 region_code: str,
                 field_type: str,
                 error_message: Optional[str] = None):
        if error_message is None:
            error_message = f"Value does not meet {region_code} compliance requirements"
            
        super().__init__(error_message)
        self.region_code = region_code
        self.field_type = field_type
        
        # Load region-specific validation patterns
        self.region_validators = self._load_region_validators()
    
    def _load_region_validators(self) -> Dict:
        """Load region-specific validation patterns"""
        # In a real implementation, this would load from a database or config file
        # Here we're using a simplified hardcoded version for illustration
        return {
            "REG-SAARC": {
                "tax_id": {"pattern": r"^[A-Z]{5}\d{4}[A-Z]{1}$", "example": "ABCDE1234F"},
                "gstin": {"pattern": r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$", "example": "27AAPFU0939F1ZV"},
                "phone": {"pattern": r"^(\+91|0)?[6-9]\d{9}$", "example": "+919876543210"},
                "postal_code": {"pattern": r"^\d{6}$", "example": "400001"}
            },
            "REG-EU": {
                "vat": {"pattern": r"^[A-Z]{2}\d{9}$", "example": "DE123456789"},
                "eori": {"pattern": r"^[A-Z]{2}\d{9,15}$", "example": "DE1234567890123"},
                "phone": {"pattern": r"^\+[1-9]\d{1,14}$", "example": "+491234567890"},
                "postal_code": {"pattern": r"^[A-Z0-9]{3,10}$", "example": "10115"}
            },
            "REG-APAC": {
                "tax_id": {"pattern": r"^[A-Z0-9\-]{6,15}$", "example": "T-1234567-B"},
                "business_id": {"pattern": r"^[A-Z0-9\-]{6,12}$", "example": "2020-12345-X"},
                "phone": {"pattern": r"^\+[1-9]\d{6,14}$", "example": "+6512345678"},
                "postal_code": {"pattern": r"^\d{4,8}$", "example": "123456"}
            },
            "REG-AM": {
                "ein": {"pattern": r"^\d{2}-\d{7}$", "example": "12-3456789"},
                "ssn": {"pattern": r"^\d{3}-\d{2}-\d{4}$", "example": "123-45-6789"},
                "phone": {"pattern": r"^\+1\d{10}$", "example": "+14155552671"},
                "postal_code": {"pattern": r"^\d{5}(-\d{4})?$", "example": "94107-1234"}
            },
            "REG-ME": {
                "tax_id": {"pattern": r"^[A-Z0-9]{10,15}$", "example": "TAX1234567AE"},
                "trade_license": {"pattern": r"^[A-Z0-9\-]{5,15}$", "example": "TRADE-12345"},
                "phone": {"pattern": r"^\+[1-9]\d{8,12}$", "example": "+97143216789"},
                "postal_code": {"pattern": r"^[A-Z0-9\-]{3,10}$", "example": "12345"}
            },
            "REG-GLOBAL": {
                "tax_id": {"pattern": r"^[A-Z0-9\-]{4,20}$", "example": "TAX-ID-12345"},
                "phone": {"pattern": r"^\+[1-9]\d{6,14}$", "example": "+12345678901"},
                "postal_code": {"pattern": r"^[A-Z0-9\-]{3,12}$", "example": "12345"}
            }
        }
    
    def validate(self, value: Any) -> bool:
        """Check if value complies with WTO regional requirements"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
        
        # Get region validators
        region_data = self.region_validators.get(self.region_code, self.region_validators["REG-GLOBAL"])
        
        # Get validator for specified field type
        field_validator = region_data.get(self.field_type)
        
        if field_validator is None:
            # If no specific validator exists for this field type, return True
            return True
        
        # Validate against the pattern
        pattern = field_validator["pattern"]
        return bool(re.match(pattern, str(value)))
    
    def get_error_message(self) -> str:
        """Get enhanced error message with example"""
        # Get region validators
        region_data = self.region_validators.get(self.region_code, self.region_validators["REG-GLOBAL"])
        
        # Get validator for specified field type
        field_validator = region_data.get(self.field_type)
        
        if field_validator and "example" in field_validator:
            return f"{self.error_message} (example: {field_validator['example']})"
        
        return self.error_message

class DivineAlignmentRule(ValidationRule):
    """Rule to check if a value aligns with divine principles"""
    
    def __init__(self, 
                 principle: str,
                 min_alignment: float = 0.7,
                 error_message: Optional[str] = None):
        if error_message is None:
            error_message = f"Value does not align with divine principle: {principle}"
            
        super().__init__(error_message)
        self.principle = principle
        self.min_alignment = min_alignment
        
        # Initialize divine alignment keywords and prohibited terms
        self.divine_keywords = self._load_divine_keywords()
        self.prohibited_terms = self._load_prohibited_terms()
    
    def _load_divine_keywords(self) -> Dict[str, Dict[str, float]]:
        """Load divine alignment keywords by principle"""
        # In a real implementation, this would load from a database or config file
        # Here we're using a simplified hardcoded version for illustration
        return {
            "ethical_conduct": {
                "ethical": 0.9, "fair": 0.8, "honest": 0.9, "transparent": 0.8,
                "integrity": 0.9, "moral": 0.8, "righteous": 0.7, "virtuous": 0.7,
                "principled": 0.8, "honorable": 0.7, "truthful": 0.9, "sincere": 0.8
            },
            "environmental_stewardship": {
                "sustainable": 0.9, "eco-friendly": 0.8, "green": 0.7, "renewable": 0.8,
                "conservation": 0.8, "biodegradable": 0.7, "environmental": 0.8, "recycled": 0.7,
                "natural": 0.6, "organic": 0.6, "clean": 0.7, "ecological": 0.8
            },
            "community_welfare": {
                "community": 0.8, "social": 0.7, "welfare": 0.8, "charitable": 0.8,
                "nonprofit": 0.7, "humanitarian": 0.8, "philanthropic": 0.7, "giving": 0.6,
                "supporting": 0.6, "uplifting": 0.7, "empowering": 0.7, "collaborative": 0.6
            },
            "fair_trade": {
                "fair-trade": 0.9, "equitable": 0.8, "just": 0.7, "ethical-trade": 0.8,
                "balanced": 0.6, "fair-wage": 0.8, "responsible": 0.7, "sustainable-trade": 0.8,
                "ethical-sourcing": 0.8, "transparent-trade": 0.7, "fair-price": 0.8
            }
        }
    
    def _load_prohibited_terms(self) -> Dict[str, List[str]]:
        """Load prohibited terms by principle"""
        # In a real implementation, this would load from a database or config file
        # Here we're using a simplified hardcoded version for illustration
        return {
            "ethical_conduct": [
                "bribe", "corrupt", "fraud", "deceive", "manipulate", "mislead",
                "cheat", "exploit", "dishonest", "unethical", "illegal"
            ],
            "environmental_stewardship": [
                "polluting", "toxic", "harmful", "wasteful", "destructive",
                "unsustainable", "depleting", "damaging", "contaminating"
            ],
            "community_welfare": [
                "exploitative", "unfair", "harmful", "discriminatory", "exclusionary",
                "divisive", "prejudicial", "biased", "unjust"
            ],
            "fair_trade": [
                "sweatshop", "underpaid", "exploitative", "unfair", "one-sided",
                "manipulative", "deceptive", "unethical-sourcing"
            ]
        }
    
    def validate(self, value: Any) -> bool:
        """Check if value aligns with divine principles"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True  # Skip validation if empty (handled by RequiredRule)
        
        if not isinstance(value, str):
            return True  # Non-string values aren't evaluated for divine alignment
            
        value_lower = value.lower()
        
        # Check prohibited terms first
        prohibited = self.prohibited_terms.get(self.principle, [])
        for term in prohibited:
            if term in value_lower:
                return False
        
        # If no prohibited terms, consider it valid for short inputs
        if len(value_lower.split()) <= 3:
            return True
        
        # For longer inputs, check for positive alignment
        alignment_score = self._calculate_alignment(value_lower)
        return alignment_score >= self.min_alignment
    
    def _calculate_alignment(self, text: str) -> float:
        """Calculate divine alignment score for text"""
        keywords = self.divine_keywords.get(self.principle, {})
        if not keywords:
            return 1.0  # If no keywords defined, assume alignment
        
        words = text.split()
        total_score = 0
        matches = 0
        
        for word in words:
            if word in keywords:
                total_score += keywords[word]
                matches += 1
        
        # Return average score if matches found, otherwise neutral score
        return total_score / matches if matches > 0 else 0.5

class FieldValidator:
    """Validates a single field using multiple rules"""
    
    def __init__(self, field_name: str):
        self.field_name = field_name
        self.rules: List[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule) -> 'FieldValidator':
        """Add a validation rule"""
        self.rules.append(rule)
        return self
    
    def validate(self, value: Any) -> Dict[str, Any]:
        """Validate value against all rules"""
        result = {
            "field": self.field_name,
            "valid": True,
            "errors": []
        }
        
        for rule in self.rules:
            if not rule.validate(value):
                result["valid"] = False
                result["errors"].append(rule.get_error_message())
        
        return result

class FormValidator:
    """Validates a complete form with multiple fields"""
    
    def __init__(self):
        self.field_validators: Dict[str, FieldValidator] = {}
    
    def add_field(self, field_name: str) -> FieldValidator:
        """Add a field validator"""
        validator = FieldValidator(field_name)
        self.field_validators[field_name] = validator
        return validator
    
    def validate(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate entire form data"""
        result = {
            "valid": True,
            "fields": {}
        }
        
        for field_name, validator in self.field_validators.items():
            field_value = form_data.get(field_name)
            field_result = validator.validate(field_value)
            
            result["fields"][field_name] = field_result
            
            if not field_result["valid"]:
                result["valid"] = False
        
        return result

class ValidationEngine:
    """Core engine for validating data against rules"""
    
    def __init__(self):
        self.form_validators: Dict[str, FormValidator] = {}
    
    def create_form_validator(self, form_id: str) -> FormValidator:
        """Create a new form validator"""
        validator = FormValidator()
        self.form_validators[form_id] = validator
        return validator
    
    def get_form_validator(self, form_id: str) -> Optional[FormValidator]:
        """Get an existing form validator"""
        return self.form_validators.get(form_id)
    
    def validate_field(self, form_id: str, field_name: str, value: Any) -> Dict[str, Any]:
        """Validate a single field"""
        validator = self.get_form_validator(form_id)
        
        if validator is None or field_name not in validator.field_validators:
            return {"valid": True, "errors": []}
        
        return validator.field_validators[field_name].validate(value)
    
    def validate_form(self, form_id: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an entire form"""
        validator = self.get_form_validator(form_id)
        
        if validator is None:
            return {"valid": True, "fields": {}}
        
        return validator.validate(form_data)