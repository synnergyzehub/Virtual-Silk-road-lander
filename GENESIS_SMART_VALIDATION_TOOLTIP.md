# Genesis Smart Data Validation Tooltip System
## Intelligent Input Validation with Context-Aware Guidance

**Version:** 1.0  
**Date:** April 11, 2025  
**Classification:** Data Integrity Component

---

## 1. System Overview

The Genesis Smart Data Validation Tooltip System provides real-time validation of input data with context-aware tooltips that guide users through proper data entry. This system ensures data integrity across the Genesis Ecosystem while enforcing WTO compliance and divine alignment principles.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                  SMART DATA VALIDATION TOOLTIP SYSTEM            │
│                                                                  │
└────────────────┬─────────────────────────────┬──────────────────┘
                 │                             │
                 ▼                             ▼
┌────────────────────────────┐      ┌────────────────────────────┐
│                            │      │                            │
│    VALIDATION ENGINE       │      │    TOOLTIP GENERATOR       │
│                            │      │                            │
│                            │      │                            │
└─────────────┬──────────────┘      └──────────────┬─────────────┘
              │                                     │
              │                                     │
              ▼                                     ▼
┌────────────────────────────┐      ┌────────────────────────────┐
│                            │      │                            │
│   COMPLIANCE CHECKER       │      │   DIVINE ALIGNMENT         │
│                            │      │   VALIDATOR                │
│                            │      │                            │
└────────────────┬───────────┘      └────────────┬───────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                  ┌────────────────────────────┐
                  │                            │
                  │   UI INTEGRATION           │
                  │   LAYER                    │
                  │                            │
                  └────────────────────────────┘
```

## 2. Key Features

The Smart Data Validation Tooltip System provides the following core features:

1. **Real-time Validation**: Validate data as it's entered, providing immediate feedback
2. **Context-Aware Tooltips**: Display tooltips with guidance specific to the data being entered
3. **WTO Compliance Checking**: Ensure data meets regional trade agreements and regulations
4. **Divine Alignment Validation**: Verify data aligns with divine principles and governance requirements
5. **Multi-language Support**: Display tooltips in the user's preferred language
6. **Accessibility Features**: Ensure tooltips are accessible to all users
7. **Customizable Styling**: Allow visual customization to match organization branding
8. **Persistence Options**: Save validation states and user preferences
9. **Integration Hooks**: Easily integrate with existing forms and input components

## 3. Implementation Components

### 3.1 Validation Engine

The Validation Engine is the core component responsible for validating input data against defined rules and constraints:

```python
# validation_engine.py

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
```

### 3.2 Tooltip Generator

The Tooltip Generator creates context-aware tooltips with helpful guidance based on validation results:

```python
# tooltip_generator.py

import json
from typing import Dict, List, Any, Optional
from html import escape

class TooltipStyle:
    """Style configuration for tooltips"""
    
    def __init__(self, 
                 background_color: str = "#f9f9f9",
                 border_color: str = "#cccccc",
                 text_color: str = "#333333",
                 error_color: str = "#e53935",
                 info_color: str = "#2196F3",
                 success_color: str = "#4CAF50",
                 warning_color: str = "#FFC107",
                 font_family: str = "Arial, sans-serif",
                 font_size: str = "14px",
                 border_radius: str = "4px",
                 max_width: str = "300px",
                 arrow_size: str = "8px"):
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
        self.error_color = error_color
        self.info_color = info_color
        self.success_color = success_color
        self.warning_color = warning_color
        self.font_family = font_family
        self.font_size = font_size
        self.border_radius = border_radius
        self.max_width = max_width
        self.arrow_size = arrow_size
    
    def to_css(self) -> str:
        """Generate CSS styles for tooltips"""
        return f"""
        .genesis-tooltip {{
            position: absolute;
            z-index: 1000;
            padding: 10px;
            background-color: {self.background_color};
            border: 1px solid {self.border_color};
            border-radius: {self.border_radius};
            color: {self.text_color};
            font-family: {self.font_family};
            font-size: {self.font_size};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            max-width: {self.max_width};
            transition: opacity 0.2s ease-in-out;
        }}
        
        .genesis-tooltip::before {{
            content: '';
            position: absolute;
            width: 0;
            height: 0;
            border-style: solid;
        }}
        
        .genesis-tooltip[data-position="top"]::before {{
            bottom: 100%;
            left: 50%;
            margin-left: -{self.arrow_size};
            border-width: {self.arrow_size};
            border-color: transparent transparent {self.border_color} transparent;
        }}
        
        .genesis-tooltip[data-position="bottom"]::before {{
            top: 100%;
            left: 50%;
            margin-left: -{self.arrow_size};
            border-width: {self.arrow_size};
            border-color: {self.border_color} transparent transparent transparent;
        }}
        
        .genesis-tooltip[data-position="left"]::before {{
            top: 50%;
            right: 100%;
            margin-top: -{self.arrow_size};
            border-width: {self.arrow_size};
            border-color: transparent {self.border_color} transparent transparent;
        }}
        
        .genesis-tooltip[data-position="right"]::before {{
            top: 50%;
            left: 100%;
            margin-top: -{self.arrow_size};
            border-width: {self.arrow_size};
            border-color: transparent transparent transparent {self.border_color};
        }}
        
        .genesis-tooltip-error {{
            background-color: {self.error_color};
            color: white;
            border-color: {self.error_color};
        }}
        
        .genesis-tooltip-info {{
            background-color: {self.info_color};
            color: white;
            border-color: {self.info_color};
        }}
        
        .genesis-tooltip-success {{
            background-color: {self.success_color};
            color: white;
            border-color: {self.success_color};
        }}
        
        .genesis-tooltip-warning {{
            background-color: {self.warning_color};
            color: white;
            border-color: {self.warning_color};
        }}
        
        .genesis-tooltip-title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .genesis-tooltip-content {{
            margin-bottom: 8px;
        }}
        
        .genesis-tooltip-list {{
            margin: 0;
            padding-left: 20px;
        }}
        
        .genesis-tooltip-list-item {{
            margin-bottom: 3px;
        }}
        
        .genesis-tooltip-icon {{
            margin-right: 5px;
            display: inline-block;
            width: 16px;
            height: 16px;
            text-align: center;
            line-height: 16px;
        }}
        """

class TooltipContent:
    """Content structure for tooltips"""
    
    def __init__(self, 
                 title: Optional[str] = None,
                 message: Optional[str] = None,
                 items: Optional[List[str]] = None,
                 type: str = "info",
                 field_name: Optional[str] = None):
        self.title = title
        self.message = message
        self.items = items or []
        self.type = type  # info, error, success, warning
        self.field_name = field_name
    
    def to_html(self) -> str:
        """Generate HTML content for the tooltip"""
        html = ""
        
        if self.title:
            html += f'<div class="genesis-tooltip-title">{escape(self.title)}</div>'
        
        if self.message:
            html += f'<div class="genesis-tooltip-content">{escape(self.message)}</div>'
        
        if self.items:
            html += '<ul class="genesis-tooltip-list">'
            for item in self.items:
                html += f'<li class="genesis-tooltip-list-item">{escape(item)}</li>'
            html += '</ul>'
        
        return html
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tooltip content to dictionary"""
        return {
            "title": self.title,
            "message": self.message,
            "items": self.items,
            "type": self.type,
            "field_name": self.field_name
        }

class TooltipGenerator:
    """Generates tooltips based on validation results"""
    
    def __init__(self, style: Optional[TooltipStyle] = None):
        self.style = style or TooltipStyle()
        self.field_descriptions: Dict[str, str] = {}
        self.field_examples: Dict[str, str] = {}
        self.help_messages: Dict[str, Dict[str, str]] = {}
        
        # Load tooltip content from configuration
        self._load_tooltip_content()
    
    def _load_tooltip_content(self) -> None:
        """Load tooltip content from configuration"""
        # In a real implementation, this would load from a database or config file
        # Here we're using a simplified hardcoded version for illustration
        
        # Field descriptions
        self.field_descriptions = {
            "entity_name": "The legal name of your business entity as registered with authorities",
            "tax_id": "Your organization's tax identification number",
            "gstin": "Goods and Services Tax Identification Number (India)",
            "vat_number": "Value Added Tax registration number",
            "business_registration": "Business registration or incorporation number",
            "contact_email": "Primary contact email for your organization",
            "contact_phone": "Primary contact phone number for your organization",
            "address_line1": "Street address of your organization",
            "postal_code": "Postal or ZIP code",
            "city": "City name",
            "country": "Country name or code",
            "industry_sector": "Primary industry sector of your business",
            "annual_revenue": "Annual revenue in your local currency",
            "employee_count": "Total number of employees",
            "founding_date": "Date when your organization was established",
            "website": "Your organization's website URL",
            "divine_mission": "Statement describing your organization's divine alignment and purpose",
            "sustainable_practices": "Description of your sustainable business practices",
            "community_initiatives": "Description of your community engagement initiatives"
        }
        
        # Field examples
        self.field_examples = {
            "entity_name": "Example: Acme Corporation Pvt Ltd",
            "tax_id": "Example: ABCDE1234F (India), 12-3456789 (US)",
            "gstin": "Example: 27AAPFU0939F1ZV",
            "vat_number": "Example: GB123456789",
            "business_registration": "Example: CIN:U74900TN2018PTC123456",
            "contact_email": "Example: contact@yourcompany.com",
            "contact_phone": "Example: +91 98765 43210",
            "address_line1": "Example: 123 Main Street, Building A, Suite 101",
            "postal_code": "Example: 400001",
            "divine_mission": "Example: Our mission is to provide sustainable products while maintaining ethical business practices and supporting our community",
            "sustainable_practices": "Example: We use recycled materials, renewable energy, and minimize waste in our operations",
            "community_initiatives": "Example: We sponsor local education programs and provide volunteer opportunities for employees"
        }
        
        # Help messages by field and type
        self.help_messages = {
            "entity_name": {
                "info": "Enter the official registered name of your organization",
                "error": "Please enter your organization's registered name exactly as it appears on official documents"
            },
            "tax_id": {
                "info": "Enter your tax identification number in the format required by your country",
                "error": "Tax ID format is invalid. Please check and enter the correct format for your region"
            },
            "gstin": {
                "info": "Enter your 15-character GSTIN",
                "error": "GSTIN must be 15 characters with state code, PAN, entity number and check digit"
            },
            "contact_email": {
                "info": "Enter a valid email address that you check regularly",
                "error": "Please enter a valid email address (e.g., name@company.com)"
            },
            "divine_mission": {
                "info": "Describe how your organization aligns with divine principles",
                "error": "Please ensure your mission statement reflects ethical, sustainable, and community-oriented values"
            }
        }
    
    def get_field_description(self, field_name: str) -> str:
        """Get description for a field"""
        return self.field_descriptions.get(field_name, "")
    
    def get_field_example(self, field_name: str) -> str:
        """Get example for a field"""
        return self.field_examples.get(field_name, "")
    
    def get_help_message(self, field_name: str, message_type: str = "info") -> str:
        """Get help message for a field and type"""
        field_messages = self.help_messages.get(field_name, {})
        return field_messages.get(message_type, "")
    
    def generate_validation_tooltip(self, validation_result: Dict[str, Any]) -> TooltipContent:
        """Generate tooltip based on validation result"""
        field_name = validation_result.get("field", "")
        is_valid = validation_result.get("valid", True)
        errors = validation_result.get("errors", [])
        
        if is_valid:
            # Valid field tooltip
            description = self.get_field_description(field_name)
            example = self.get_field_example(field_name)
            help_message = self.get_help_message(field_name, "info")
            
            message = help_message if help_message else description
            
            content = TooltipContent(
                title=f"{field_name.replace('_', ' ').title()}",
                message=message,
                items=[example] if example else [],
                type="info",
                field_name=field_name
            )
        else:
            # Invalid field tooltip
            help_message = self.get_help_message(field_name, "error")
            
            content = TooltipContent(
                title=f"Invalid {field_name.replace('_', ' ').title()}",
                message=help_message if help_message else "Please correct the following errors:",
                items=errors,
                type="error",
                field_name=field_name
            )
        
        return content
    
    def generate_field_tooltip(self, field_name: str) -> TooltipContent:
        """Generate tooltip for a field (without validation)"""
        description = self.get_field_description(field_name)
        example = self.get_field_example(field_name)
        help_message = self.get_help_message(field_name, "info")
        
        message = help_message if help_message else description
        
        content = TooltipContent(
            title=f"{field_name.replace('_', ' ').title()}",
            message=message,
            items=[example] if example else [],
            type="info",
            field_name=field_name
        )
        
        return content
    
    def generate_divine_alignment_tooltip(self, field_name: str, principle: str) -> TooltipContent:
        """Generate tooltip for divine alignment guidance"""
        principles_guidance = {
            "ethical_conduct": {
                "title": "Ethical Conduct",
                "message": "Ensure your input reflects ethical business practices and integrity",
                "items": [
                    "Use terms that reflect honesty, transparency, and integrity",
                    "Avoid terms related to deception, manipulation, or exploitation",
                    "Consider how your practices align with divine governance principles"
                ]
            },
            "environmental_stewardship": {
                "title": "Environmental Stewardship",
                "message": "Ensure your input reflects sustainable environmental practices",
                "items": [
                    "Use terms related to sustainability, conservation, and eco-friendly practices",
                    "Avoid terms related to pollution, waste, or environmental harm",
                    "Consider how your practices contribute to environmental preservation"
                ]
            },
            "community_welfare": {
                "title": "Community Welfare",
                "message": "Ensure your input reflects positive community impact",
                "items": [
                    "Use terms related to community support, social benefit, and empowerment",
                    "Avoid terms related to exploitation, division, or harm to communities",
                    "Consider how your practices contribute to social well-being"
                ]
            },
            "fair_trade": {
                "title": "Fair Trade Practices",
                "message": "Ensure your input reflects fair and equitable trade practices",
                "items": [
                    "Use terms related to equitable exchange, fair pricing, and ethical sourcing",
                    "Avoid terms related to exploitation, unfair advantage, or deceptive trade",
                    "Consider how your practices promote balanced and just commerce"
                ]
            }
        }
        
        guidance = principles_guidance.get(principle, {
            "title": "Divine Alignment",
            "message": "Ensure your input aligns with divine principles",
            "items": ["Consider ethical, sustainable, and community-oriented values"]
        })
        
        content = TooltipContent(
            title=guidance["title"],
            message=guidance["message"],
            items=guidance["items"],
            type="info",
            field_name=field_name
        )
        
        return content
    
    def generate_wto_compliance_tooltip(self, field_name: str, region_code: str, field_type: str) -> TooltipContent:
        """Generate tooltip for WTO compliance guidance"""
        region_guidance = {
            "REG-SAARC": {
                "tax_id": {
                    "title": "Tax ID Format (SAARC)",
                    "message": "Enter your PAN (Permanent Account Number)",
                    "items": [
                        "Format: 5 letters, 4 numbers, 1 letter (e.g., ABCDE1234F)",
                        "Must be the official PAN issued by tax authorities",
                        "Required for all financial transactions in the SAARC region"
                    ]
                },
                "gstin": {
                    "title": "GSTIN Format (SAARC)",
                    "message": "Enter your 15-character Goods and Services Tax Identification Number",
                    "items": [
                        "Format: 2 digits (state code), 10 characters (PAN), 1 digit (entity number), 1 character (Z), 1 character (check digit)",
                        "Example: 27AAPFU0939F1ZV",
                        "Required for all GST-registered businesses in India"
                    ]
                }
            },
            "REG-EU": {
                "vat": {
                    "title": "VAT Number Format (EU)",
                    "message": "Enter your Value Added Tax identification number",
                    "items": [
                        "Format: 2 letters (country code) followed by 9-12 digits (e.g., DE123456789)",
                        "Must be registered with EU VAT authorities",
                        "Required for intra-EU trade"
                    ]
                },
                "eori": {
                    "title": "EORI Number Format (EU)",
                    "message": "Enter your Economic Operators Registration and Identification number",
                    "items": [
                        "Format: 2 letters (country code) followed by 9-15 digits",
                        "Required for importing/exporting goods in the EU",
                        "Must be registered with customs authorities"
                    ]
                }
            }
        }
        
        # Get region-specific guidance, fall back to generic guidance if not found
        region_field_guidance = region_guidance.get(region_code, {}).get(field_type)
        
        if region_field_guidance:
            content = TooltipContent(
                title=region_field_guidance["title"],
                message=region_field_guidance["message"],
                items=region_field_guidance["items"],
                type="info",
                field_name=field_name
            )
        else:
            # Generic compliance guidance
            content = TooltipContent(
                title=f"{region_code} Compliance",
                message=f"Ensure your input complies with {region_code} standards",
                items=[
                    f"Follow the format required by {region_code} regulations",
                    "Use official identifiers issued by authorized bodies",
                    "Ensure all information is accurate and current"
                ],
                type="info",
                field_name=field_name
            )
        
        return content
    
    def get_css(self) -> str:
        """Get CSS styles for tooltips"""
        return self.style.to_css()
```

### 3.3 UI Integration Layer

The UI Integration Layer makes it easy to add smart tooltips to any Streamlit input:

```python
# smart_tooltip_ui.py

import streamlit as st
import re
import json
from typing import Dict, List, Any, Optional, Callable, Union

from validation_engine import ValidationEngine, RequiredRule, PatternRule, RangeRule
from validation_engine import LengthRule, OptionRule, DateFormatRule, WTOComplianceRule, DivineAlignmentRule
from tooltip_generator import TooltipGenerator, TooltipStyle, TooltipContent

class SmartTooltipUI:
    """UI Integration Layer for Smart Tooltips"""
    
    def __init__(self):
        # Initialize validation engine
        self.validation_engine = ValidationEngine()
        
        # Initialize tooltip generator with default style
        self.tooltip_generator = TooltipGenerator()
        
        # Add CSS to Streamlit
        self._inject_css()
        
        # Initialize session state for validation results if needed
        if "validation_results" not in st.session_state:
            st.session_state.validation_results = {}
    
    def _inject_css(self):
        """Inject CSS styles into Streamlit"""
        css = self.tooltip_generator.get_css()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    def text_input(self, 
                  label: str, 
                  key: str, 
                  form_id: str = "default_form",
                  value: str = "",
                  placeholder: Optional[str] = None,
                  validation_rules: Optional[List[Any]] = None,
                  wto_region: Optional[str] = None,
                  wto_field_type: Optional[str] = None,
                  divine_principle: Optional[str] = None,
                  help_text: Optional[str] = None) -> str:
        """Smart text input with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.text_input(
                label=label,
                value=value,
                key=key,
                placeholder=placeholder,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def number_input(self,
                    label: str,
                    key: str,
                    form_id: str = "default_form",
                    min_value: Optional[float] = None,
                    max_value: Optional[float] = None,
                    value: Optional[float] = None,
                    step: float = 1.0,
                    validation_rules: Optional[List[Any]] = None,
                    wto_region: Optional[str] = None,
                    wto_field_type: Optional[str] = None,
                    divine_principle: Optional[str] = None,
                    help_text: Optional[str] = None) -> float:
        """Smart number input with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add implicit range rule based on min/max values
            if min_value is not None or max_value is not None:
                field_validator.add_rule(RangeRule(min_value, max_value))
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.number_input(
                label=label,
                min_value=min_value,
                max_value=max_value,
                value=value if value is not None else (min_value if min_value is not None else 0.0),
                step=step,
                key=key,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def select_box(self,
                  label: str,
                  options: List[Any],
                  key: str,
                  form_id: str = "default_form",
                  index: int = 0,
                  validation_rules: Optional[List[Any]] = None,
                  wto_region: Optional[str] = None,
                  wto_field_type: Optional[str] = None,
                  divine_principle: Optional[str] = None,
                  help_text: Optional[str] = None) -> Any:
        """Smart select box with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add implicit option rule
            field_validator.add_rule(OptionRule(options))
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.selectbox(
                label=label,
                options=options,
                index=index,
                key=key,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def text_area(self,
                 label: str,
                 key: str,
                 form_id: str = "default_form",
                 value: str = "",
                 height: int = 100,
                 max_chars: Optional[int] = None,
                 validation_rules: Optional[List[Any]] = None,
                 wto_region: Optional[str] = None,
                 wto_field_type: Optional[str] = None,
                 divine_principle: Optional[str] = None,
                 help_text: Optional[str] = None) -> str:
        """Smart text area with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add implicit length rule if max_chars provided
            if max_chars is not None:
                field_validator.add_rule(LengthRule(max_length=max_chars))
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.text_area(
                label=label,
                value=value,
                height=height,
                max_chars=max_chars,
                key=key,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def date_input(self,
                  label: str,
                  key: str,
                  form_id: str = "default_form",
                  value: Any = None,
                  validation_rules: Optional[List[Any]] = None,
                  wto_region: Optional[str] = None,
                  wto_field_type: Optional[str] = None,
                  divine_principle: Optional[str] = None,
                  help_text: Optional[str] = None) -> Any:
        """Smart date input with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.date_input(
                label=label,
                value=value,
                key=key,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def file_uploader(self,
                     label: str,
                     key: str,
                     form_id: str = "default_form",
                     type: Optional[Union[str, List[str]]] = None,
                     accept_multiple_files: bool = False,
                     validation_rules: Optional[List[Any]] = None,
                     wto_region: Optional[str] = None,
                     wto_field_type: Optional[str] = None,
                     divine_principle: Optional[str] = None,
                     help_text: Optional[str] = None) -> Any:
        """Smart file uploader with validation and tooltips"""
        # Create or get form validator
        form_validator = self.validation_engine.get_form_validator(form_id)
        if form_validator is None:
            form_validator = self.validation_engine.create_form_validator(form_id)
        
        # Add field validator if not already present
        if key not in form_validator.field_validators:
            field_validator = form_validator.add_field(key)
            
            # Add validation rules if provided
            if validation_rules:
                for rule in validation_rules:
                    field_validator.add_rule(rule)
            
            # Add WTO compliance rule if region and field type provided
            if wto_region and wto_field_type:
                field_validator.add_rule(WTOComplianceRule(wto_region, wto_field_type))
            
            # Add divine alignment rule if principle provided
            if divine_principle:
                field_validator.add_rule(DivineAlignmentRule(divine_principle))
        
        # Display the input field
        col1, col2 = st.columns([9, 1])
        
        with col1:
            input_value = st.file_uploader(
                label=label,
                type=type,
                accept_multiple_files=accept_multiple_files,
                key=key,
                help=help_text,
                on_change=lambda: self._validate_field(form_id, key, st.session_state[key])
            )
        
        with col2:
            # Add tooltip button
            st.markdown(self._get_tooltip_button_html(key), unsafe_allow_html=True)
        
        # Validate input when component is first rendered
        if key not in st.session_state.validation_results:
            self._validate_field(form_id, key, input_value)
        
        # Display validation feedback
        self._show_validation_feedback(key)
        
        return input_value
    
    def validate_form(self, form_id: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all fields in a form"""
        # Get validator for this form
        validator = self.validation_engine.get_form_validator(form_id)
        if validator is None:
            return {"valid": True, "fields": {}}
        
        # Validate all fields
        result = validator.validate(form_data)
        
        # Update session state with validation results
        for field_name, field_result in result["fields"].items():
            st.session_state.validation_results[field_name] = field_result
        
        return result
    
    def _validate_field(self, form_id: str, field_name: str, value: Any) -> None:
        """Validate a single field"""
        # Validate the field
        result = self.validation_engine.validate_field(form_id, field_name, value)
        
        # Store result in session state
        st.session_state.validation_results[field_name] = result
    
    def _show_validation_feedback(self, field_name: str) -> None:
        """Show validation feedback for a field"""
        # Get validation result from session state
        result = st.session_state.validation_results.get(field_name)
        
        if result and not result.get("valid", True):
            # Show error message
            error_msg = ", ".join(result.get("errors", []))
            st.error(error_msg)
    
    def _get_tooltip_button_html(self, field_name: str) -> str:
        """Generate HTML for tooltip button"""
        # Get validation result from session state
        result = st.session_state.validation_results.get(field_name)
        
        # Generate tooltip content
        if result:
            tooltip_content = self.tooltip_generator.generate_validation_tooltip(result)
        else:
            tooltip_content = self.tooltip_generator.generate_field_tooltip(field_name)
        
        # Convert tooltip content to JSON
        tooltip_json = json.dumps(tooltip_content.to_dict()).replace('"', '&quot;')
        
        # Determine button style based on validation result
        button_style = "color: #FFC107;"  # Default is info/help style
        if result and not result.get("valid", True):
            button_style = "color: #e53935;"  # Error style
        
        # Generate HTML
        html = f"""
        <div class="tooltip-button" style="text-align: center; margin-top: 20px;">
            <span onclick="showTooltip('{field_name}', this)" 
                  style="cursor: pointer; font-size: 24px; {button_style}"
                  data-tooltip='{tooltip_json}'>
                &#9432;
            </span>
        </div>
        
        <script>
        // Script to handle tooltip display
        function showTooltip(fieldName, element) {{
            // Get tooltip data
            var tooltipData = JSON.parse(element.getAttribute('data-tooltip'));
            
            // Remove any existing tooltips
            var existingTooltips = document.querySelectorAll('.genesis-tooltip');
            existingTooltips.forEach(function(tooltip) {{
                tooltip.remove();
            }});
            
            // Create tooltip element
            var tooltip = document.createElement('div');
            tooltip.className = 'genesis-tooltip';
            if (tooltipData.type) {{
                tooltip.className += ' genesis-tooltip-' + tooltipData.type;
            }}
            tooltip.setAttribute('data-position', 'left');
            
            // Set tooltip content
            tooltip.innerHTML = '';
            if (tooltipData.title) {{
                var title = document.createElement('div');
                title.className = 'genesis-tooltip-title';
                title.textContent = tooltipData.title;
                tooltip.appendChild(title);
            }}
            
            if (tooltipData.message) {{
                var message = document.createElement('div');
                message.className = 'genesis-tooltip-content';
                message.textContent = tooltipData.message;
                tooltip.appendChild(message);
            }}
            
            if (tooltipData.items && tooltipData.items.length > 0) {{
                var list = document.createElement('ul');
                list.className = 'genesis-tooltip-list';
                
                tooltipData.items.forEach(function(item) {{
                    var listItem = document.createElement('li');
                    listItem.className = 'genesis-tooltip-list-item';
                    listItem.textContent = item;
                    list.appendChild(listItem);
                }});
                
                tooltip.appendChild(list);
            }}
            
            // Position the tooltip
            element.parentNode.style.position = 'relative';
            element.parentNode.appendChild(tooltip);
            
            // Position to the left of the icon
            tooltip.style.top = '0px';
            tooltip.style.right = '30px';
            
            // Add click handler to close tooltip when clicking outside
            document.addEventListener('click', function closeTooltip(e) {{
                if (!tooltip.contains(e.target) && e.target !== element) {{
                    tooltip.remove();
                    document.removeEventListener('click', closeTooltip);
                }}
            }});
        }}
        </script>
        """
        
        return html
```

### 3.4. Complete Implementation Example

Here's a streamlit app that demonstrates the Smart Data Validation Tooltip System:

```python
# app_with_smart_tooltips.py

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Import Smart Tooltip components
from validation_engine import ValidationEngine, RequiredRule, PatternRule, RangeRule
from validation_engine import LengthRule, OptionRule, DateFormatRule, WTOComplianceRule, DivineAlignmentRule
from tooltip_generator import TooltipGenerator, TooltipStyle, TooltipContent
from smart_tooltip_ui import SmartTooltipUI

# Page setup
st.set_page_config(
    page_title="Genesis Smart Data Validation Demo",
    page_icon="✨",
    layout="wide"
)

# Initialize Smart Tooltip UI
tooltip_ui = SmartTooltipUI()

def main():
    st.title("Genesis Smart Data Validation Tooltip System")
    st.subheader("Intelligent Input Validation with Context-Aware Guidance")
    
    # Create tabs for different demo sections
    tab1, tab2, tab3 = st.tabs([
        "Basic Validation Demo", 
        "WTO Compliance Demo", 
        "Divine Alignment Demo"
    ])
    
    # Tab 1: Basic Validation Demo
    with tab1:
        st.header("Basic Validation Demo")
        st.write("This demo shows basic validation with smart tooltips. Hover over the ⓘ icons for guidance.")
        
        # Basic validation form
        with st.form("basic_validation_form"):
            # Text input with required and pattern validation
            email = tooltip_ui.text_input(
                label="Email Address",
                key="email",
                form_id="basic_validation_form",
                validation_rules=[
                    RequiredRule("Email address is required"),
                    PatternRule(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", "Please enter a valid email address")
                ],
                help_text="Enter your business email address"
            )
            
            # Number input with range validation
            age = tooltip_ui.number_input(
                label="Age",
                key="age",
                form_id="basic_validation_form",
                min_value=18,
                max_value=120,
                validation_rules=[
                    RequiredRule("Age is required")
                ],
                help_text="Enter your age (must be at least 18)"
            )
            
            # Select box with option validation
            country = tooltip_ui.select_box(
                label="Country",
                key="country",
                form_id="basic_validation_form",
                options=["", "India", "United States", "Germany", "Singapore", "United Arab Emirates"],
                validation_rules=[
                    RequiredRule("Country is required")
                ],
                help_text="Select your country of residence"
            )
            
            # Text area with length validation
            bio = tooltip_ui.text_area(
                label="Bio",
                key="bio",
                form_id="basic_validation_form",
                max_chars=200,
                validation_rules=[
                    LengthRule(min_length=10, max_length=200, error_message="Bio must be between 10-200 characters")
                ],
                help_text="Enter a brief description about yourself"
            )
            
            # Date input with validation
            birthdate = tooltip_ui.date_input(
                label="Birth Date",
                key="birthdate",
                form_id="basic_validation_form",
                validation_rules=[
                    RequiredRule("Birth date is required")
                ],
                help_text="Select your date of birth"
            )
            
            # Submit button
            submit_button = st.form_submit_button("Submit Basic Form")
            
            if submit_button:
                # Get form data
                form_data = {
                    "email": email,
                    "age": age,
                    "country": country,
                    "bio": bio,
                    "birthdate": birthdate
                }
                
                # Validate form
                validation_result = tooltip_ui.validate_form("basic_validation_form", form_data)
                
                # Show result
                if validation_result["valid"]:
                    st.success("Form submitted successfully!")
                    st.json(form_data)
                else:
                    st.error("Please fix the errors in the form.")
    
    # Tab 2: WTO Compliance Demo
    with tab2:
        st.header("WTO Compliance Demo")
        st.write("This demo shows validation with WTO regional compliance rules. Each region has specific format requirements.")
        
        # Region selector
        regions = {
            "REG-SAARC": "South Asian Association for Regional Cooperation",
            "REG-EU": "European Union",
            "REG-APAC": "Asia-Pacific Region",
            "REG-AM": "Americas Region",
            "REG-ME": "Middle East Region",
            "REG-GLOBAL": "Global (Default)"
        }
        
        selected_region = st.selectbox(
            "Select WTO Region",
            options=list(regions.keys()),
            format_func=lambda x: regions[x],
            key="wto_region_selector"
        )
        
        st.write(f"You selected: {regions[selected_region]}")
        
        # WTO compliance form
        with st.form("wto_compliance_form"):
            # Tax ID with WTO compliance
            tax_id = tooltip_ui.text_input(
                label="Tax Identification Number",
                key="tax_id_wto",
                form_id="wto_compliance_form",
                validation_rules=[
                    RequiredRule("Tax ID is required")
                ],
                wto_region=selected_region,
                wto_field_type="tax_id",
                help_text="Enter your organization's tax identification number"
            )
            
            # Business registration with WTO compliance
            if selected_region == "REG-EU":
                # EU has VAT and EORI
                vat_number = tooltip_ui.text_input(
                    label="VAT Number",
                    key="vat_number",
                    form_id="wto_compliance_form",
                    validation_rules=[
                        RequiredRule("VAT Number is required")
                    ],
                    wto_region=selected_region,
                    wto_field_type="vat",
                    help_text="Enter your Value Added Tax registration number"
                )
                
                eori_number = tooltip_ui.text_input(
                    label="EORI Number",
                    key="eori_number",
                    form_id="wto_compliance_form",
                    wto_region=selected_region,
                    wto_field_type="eori",
                    help_text="Enter your Economic Operators Registration and Identification number (if applicable)"
                )
            elif selected_region == "REG-SAARC":
                # SAARC has GSTIN for India
                gstin = tooltip_ui.text_input(
                    label="GSTIN",
                    key="gstin",
                    form_id="wto_compliance_form",
                    validation_rules=[
                        RequiredRule("GSTIN is required for Indian businesses")
                    ],
                    wto_region=selected_region,
                    wto_field_type="gstin",
                    help_text="Enter your Goods and Services Tax Identification Number"
                )
            elif selected_region == "REG-ME":
                # Middle East has trade license
                trade_license = tooltip_ui.text_input(
                    label="Trade License Number",
                    key="trade_license",
                    form_id="wto_compliance_form",
                    validation_rules=[
                        RequiredRule("Trade License Number is required")
                    ],
                    wto_region=selected_region,
                    wto_field_type="trade_license",
                    help_text="Enter your trade license or commercial registration number"
                )
            elif selected_region == "REG-APAC":
                # APAC has business ID
                business_id = tooltip_ui.text_input(
                    label="Business Registration ID",
                    key="business_id",
                    form_id="wto_compliance_form",
                    validation_rules=[
                        RequiredRule("Business Registration ID is required")
                    ],
                    wto_region=selected_region,
                    wto_field_type="business_id",
                    help_text="Enter your business registration identifier"
                )
            elif selected_region == "REG-AM":
                # Americas has EIN
                ein = tooltip_ui.text_input(
                    label="Employer Identification Number (EIN)",
                    key="ein",
                    form_id="wto_compliance_form",
                    validation_rules=[
                        RequiredRule("EIN is required for US businesses")
                    ],
                    wto_region=selected_region,
                    wto_field_type="ein",
                    help_text="Enter your Employer Identification Number (Format: XX-XXXXXXX)"
                )
            
            # Phone number with WTO compliance (all regions)
            phone = tooltip_ui.text_input(
                label="Contact Phone Number",
                key="phone_wto",
                form_id="wto_compliance_form",
                validation_rules=[
                    RequiredRule("Phone number is required")
                ],
                wto_region=selected_region,
                wto_field_type="phone",
                help_text="Enter your contact phone number with country code"
            )
            
            # Postal code with WTO compliance (all regions)
            postal_code = tooltip_ui.text_input(
                label="Postal/ZIP Code",
                key="postal_code_wto",
                form_id="wto_compliance_form",
                validation_rules=[
                    RequiredRule("Postal/ZIP code is required")
                ],
                wto_region=selected_region,
                wto_field_type="postal_code",
                help_text="Enter your postal or ZIP code"
            )
            
            # Submit button
            submit_button = st.form_submit_button("Submit WTO Compliance Form")
            
            if submit_button:
                # Get form data
                form_data = {
                    "tax_id": tax_id,
                    "phone": phone,
                    "postal_code": postal_code
                }
                
                # Add region-specific fields
                if selected_region == "REG-EU":
                    form_data["vat_number"] = vat_number
                    form_data["eori_number"] = eori_number
                elif selected_region == "REG-SAARC":
                    form_data["gstin"] = gstin
                elif selected_region == "REG-ME":
                    form_data["trade_license"] = trade_license
                elif selected_region == "REG-APAC":
                    form_data["business_id"] = business_id
                elif selected_region == "REG-AM":
                    form_data["ein"] = ein
                
                # Validate form
                validation_result = tooltip_ui.validate_form("wto_compliance_form", form_data)
                
                # Show result
                if validation_result["valid"]:
                    st.success(f"WTO Compliance Form for {regions[selected_region]} submitted successfully!")
                    st.json(form_data)
                else:
                    st.error("Please fix the errors in the form.")
    
    # Tab 3: Divine Alignment Demo
    with tab3:
        st.header("Divine Alignment Demo")
        st.write("This demo shows validation with divine alignment principles. Ensure your inputs align with ethical, sustainable, and community-oriented values.")
        
        # Divine alignment form
        with st.form("divine_alignment_form"):
            # Mission statement with ethical conduct alignment
            mission = tooltip_ui.text_area(
                label="Organization Mission Statement",
                key="mission",
                form_id="divine_alignment_form",
                height=150,
                validation_rules=[
                    RequiredRule("Mission statement is required"),
                    LengthRule(min_length=20, error_message="Please provide a more detailed mission statement")
                ],
                divine_principle="ethical_conduct",
                help_text="Describe your organization's mission and purpose"
            )
            
            # Environmental practices with environmental stewardship alignment
            environmental = tooltip_ui.text_area(
                label="Environmental Sustainability Practices",
                key="environmental",
                form_id="divine_alignment_form",
                height=150,
                validation_rules=[
                    RequiredRule("Environmental practices description is required"),
                    LengthRule(min_length=20, error_message="Please provide more details about your environmental practices")
                ],
                divine_principle="environmental_stewardship",
                help_text="Describe your organization's environmental sustainability practices"
            )
            
            # Community initiatives with community welfare alignment
            community = tooltip_ui.text_area(
                label="Community Engagement Initiatives",
                key="community",
                form_id="divine_alignment_form",
                height=150,
                validation_rules=[
                    RequiredRule("Community initiatives description is required"),
                    LengthRule(min_length=20, error_message="Please provide more details about your community initiatives")
                ],
                divine_principle="community_welfare",
                help_text="Describe your organization's community engagement initiatives"
            )
            
            # Supplier practices with fair trade alignment
            suppliers = tooltip_ui.text_area(
                label="Supplier Management Practices",
                key="suppliers",
                form_id="divine_alignment_form",
                height=150,
                validation_rules=[
                    RequiredRule("Supplier practices description is required"),
                    LengthRule(min_length=20, error_message="Please provide more details about your supplier practices")
                ],
                divine_principle="fair_trade",
                help_text="Describe your organization's approach to supplier management and fair trade"
            )
            
            # Submit button
            submit_button = st.form_submit_button("Submit Divine Alignment Form")
            
            if submit_button:
                # Get form data
                form_data = {
                    "mission": mission,
                    "environmental": environmental,
                    "community": community,
                    "suppliers": suppliers
                }
                
                # Validate form
                validation_result = tooltip_ui.validate_form("divine_alignment_form", form_data)
                
                # Show result
                if validation_result["valid"]:
                    st.success("Divine Alignment Form submitted successfully!")
                    
                    # Calculate and display divine alignment score
                    alignment_score = 0.85  # Default baseline
                    
                    # Simple scoring based on content length and keywords
                    # In a real system, this would use more sophisticated analysis
                    for field, content in form_data.items():
                        words = content.lower().split()
                        
                        # Check for positive alignment keywords
                        positive_keywords = [
                            "ethical", "sustainable", "eco-friendly", "community", "fair",
                            "transparent", "integrity", "responsible", "equitable", "green",
                            "renewable", "conservation", "biodegradable", "welfare", "charitable"
                        ]
                        
                        # Check for negative alignment keywords
                        negative_keywords = [
                            "exploit", "pollute", "waste", "harmful", "toxic",
                            "unfair", "deceptive", "manipulative", "harmful", "unethical"
                        ]
                        
                        # Count keyword matches
                        positive_count = sum(1 for word in words if any(keyword in word for keyword in positive_keywords))
                        negative_count = sum(1 for word in words if any(keyword in word for keyword in negative_keywords))
                        
                        # Adjust score based on keyword counts
                        field_score = min(1.0, 0.85 + (positive_count * 0.01) - (negative_count * 0.05))
                        alignment_score = (alignment_score + field_score) / 2
                    
                    # Display alignment score and category
                    st.metric("Divine Alignment Score", f"{alignment_score:.2f}")
                    
                    # Determine alignment category
                    if alignment_score >= 0.95:
                        category = "Exceptional Alignment"
                        st.success(f"Alignment Category: {category}")
                    elif alignment_score >= 0.90:
                        category = "Strong Alignment"
                        st.success(f"Alignment Category: {category}")
                    elif alignment_score >= 0.85:
                        category = "Acceptable Alignment"
                        st.info(f"Alignment Category: {category}")
                    elif alignment_score >= 0.80:
                        category = "Borderline Alignment"
                        st.warning(f"Alignment Category: {category}")
                    else:
                        category = "Insufficient Alignment - Requires Improvement"
                        st.error(f"Alignment Category: {category}")
                    
                    # Show data
                    st.subheader("Submitted Data")
                    st.json(form_data)
                else:
                    st.error("Please fix the errors in the form to achieve divine alignment.")

if __name__ == "__main__":
    main()
```

## 4. System Benefits

The Genesis Smart Data Validation Tooltip System provides numerous benefits throughout the Genesis Ecosystem:

1. **Enhanced Data Quality**:
   - Real-time validation prevents incorrect data entry
   - Format checking ensures compliance with regional standards
   - Divine alignment validation maintains ethical data integrity

2. **Improved User Experience**:
   - Context-aware guidance helps users understand requirements
   - Immediate feedback reduces frustration and errors
   - Consistent tooltip styling enhances UI experience

3. **WTO Compliance Enforcement**:
   - Region-specific validation ensures legal compliance
   - Format checking for tax IDs, business registrations, etc.
   - Clear guidance on regional documentation requirements

4. **Divine Alignment Integration**:
   - Content analysis for ethical and sustainable language
   - Principle-based guidance for divine governance
   - Improvement suggestions for better alignment

5. **Operational Efficiency**:
   - Reduced manual validation burden
   - Fewer support requests for data entry questions
   - Lower error rates in submitted data

6. **Adaptability and Extensibility**:
   - Easy to add new validation rules
   - Straightforward to extend to new field types
   - Simple to customize for different applications

## 5. Integration Points

The Smart Data Validation Tooltip System integrates with the following Genesis Ecosystem components:

1. **Genesis Data Intake System**:
   - Document upload validation
   - Financial data format verification
   - WTO compliance checking for submitted documents

2. **License Management System**:
   - License application validation
   - Compliance documentation verification
   - Divine alignment assessment input

3. **Entity Management System**:
   - Entity registration data validation
   - Geographic compliance checking
   - Governance structure validation

4. **Virtual Silk Road**:
   - Transaction data validation
   - Cross-border trade compliance checking
   - Ethical trade practice verification

5. **SynergyzeOS Activation**:
   - License activation code validation
   - System configuration validation
   - Deployment parameter verification

## 6. Deployment Guide

To deploy the Smart Data Validation Tooltip System:

1. **File Structure**:
   - Place the validation_engine.py, tooltip_generator.py, and smart_tooltip_ui.py files in your project's utils directory
   - Import the components as needed in your Streamlit applications

2. **Integration with Existing Forms**:
   - Replace standard Streamlit input components with their smart equivalents
   - Define validation rules for each field
   - Add WTO region and divine principle parameters as needed

3. **Customization**:
   - Modify the TooltipStyle class to match your application's visual style
   - Add custom field descriptions and examples to the TooltipGenerator
   - Create additional validation rules as needed for specialized fields

4. **Testing**:
   - Test with various input values to ensure validation works correctly
   - Verify WTO compliance validation with region-specific sample data
   - Check divine alignment validation with different text inputs

## 7. Conclusion

The Genesis Smart Data Validation Tooltip System represents a significant enhancement to the data integrity mechanisms within the Genesis Ecosystem. By combining real-time validation, context-aware guidance, and divine alignment principles, it ensures that all data entering the system meets the highest standards of quality, compliance, and ethical alignment.

This system supports the Emperor's Computational Governance by enforcing divine principles at the point of data entry, ensuring that all system interactions uphold the foundational values of the Genesis Ecosystem.

---

*Designed with divine mechanics. Implemented with sovereign integrity. Governed by computational alignment.*