"""
Genesis Smart Tooltip Generator

This module provides the tooltip content generation for the Genesis Smart Data Validation
Tooltip System, creating context-aware tooltips with validation feedback and guidance.
"""

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