"""
Genesis Smart Tooltip UI Integration Layer

This module provides the UI integration layer for the Genesis Smart Data Validation
Tooltip System, making it easy to add smart tooltips to any Streamlit input.
"""

import streamlit as st
import re
import json
from typing import Dict, List, Any, Optional, Callable, Union

from utils.validation_engine import ValidationEngine, RequiredRule, PatternRule, RangeRule
from utils.validation_engine import LengthRule, OptionRule, DateFormatRule, WTOComplianceRule, DivineAlignmentRule
from utils.tooltip_generator import TooltipGenerator, TooltipStyle, TooltipContent

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