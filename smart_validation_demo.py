"""
Genesis Smart Data Validation Tooltip System Demo

This Streamlit application demonstrates the Smart Data Validation Tooltip System
with various use cases including basic validation, WTO compliance, and divine alignment.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Import Smart Tooltip components
from utils.validation_engine import ValidationEngine, RequiredRule, PatternRule, RangeRule
from utils.validation_engine import LengthRule, OptionRule, DateFormatRule, WTOComplianceRule, DivineAlignmentRule
from utils.tooltip_generator import TooltipGenerator, TooltipStyle, TooltipContent
from utils.smart_tooltip_ui import SmartTooltipUI

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
    
    st.markdown("""
    This demo showcases the Smart Data Validation Tooltip System for the Genesis Ecosystem.
    Hover over the **ⓘ** icons next to any input field for guidance and validation details.
    """)
    
    # Create tabs for different demo sections
    tab1, tab2, tab3 = st.tabs([
        "📋 Basic Validation Demo", 
        "🌎 WTO Compliance Demo", 
        "✨ Divine Alignment Demo"
    ])
    
    # Tab 1: Basic Validation Demo
    with tab1:
        st.header("Basic Validation Demo")
        st.write("This demo shows basic validation with smart tooltips. Click on the info icons for guidance.")
        
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
            annual_revenue = tooltip_ui.number_input(
                label="Annual Revenue (in Crores)",
                key="annual_revenue",
                form_id="basic_validation_form",
                min_value=0.1,
                max_value=10000.0,
                value=1.0,
                step=0.1,
                validation_rules=[
                    RequiredRule("Annual revenue is required")
                ],
                help_text="Enter your organization's annual revenue in crores"
            )
            
            # Select box with option validation
            industry = tooltip_ui.select_box(
                label="Industry Sector",
                key="industry",
                form_id="basic_validation_form",
                options=["", "Manufacturing", "Retail", "Technology", "Finance", "Healthcare", "Other"],
                validation_rules=[
                    RequiredRule("Industry sector is required")
                ],
                help_text="Select your primary industry sector"
            )
            
            # Text area with length validation
            company_description = tooltip_ui.text_area(
                label="Company Description",
                key="company_description",
                form_id="basic_validation_form",
                max_chars=500,
                validation_rules=[
                    LengthRule(min_length=50, max_length=500, error_message="Description must be between 50-500 characters")
                ],
                help_text="Provide a brief description of your organization"
            )
            
            # Date input with validation
            founding_date = tooltip_ui.date_input(
                label="Founding Date",
                key="founding_date",
                form_id="basic_validation_form",
                validation_rules=[
                    RequiredRule("Founding date is required")
                ],
                help_text="Select your organization's founding date"
            )
            
            # Submit button
            submit_button = st.form_submit_button("Submit Basic Form")
            
            if submit_button:
                # Get form data
                form_data = {
                    "email": email,
                    "annual_revenue": annual_revenue,
                    "industry": industry,
                    "company_description": company_description,
                    "founding_date": founding_date
                }
                
                # Validate form
                validation_result = tooltip_ui.validate_form("basic_validation_form", form_data)
                
                # Show result
                if validation_result["valid"]:
                    st.success("Form submitted successfully!")
                    
                    # Show data
                    st.subheader("Submitted Data")
                    display_data = {
                        "Email Address": email,
                        "Annual Revenue": f"₹{annual_revenue} Crores",
                        "Industry Sector": industry,
                        "Company Description": company_description[:100] + "..." if len(company_description) > 100 else company_description,
                        "Founding Date": founding_date.strftime("%Y-%m-%d")
                    }
                    
                    # Create two columns for display
                    col1, col2 = st.columns(2)
                    
                    # Display formatted data in first column
                    with col1:
                        for key, value in display_data.items():
                            st.markdown(f"**{key}:** {value}")
                    
                    # Display raw data as JSON in second column
                    with col2:
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
                    "postal_code": postal_code,
                    "wto_region": selected_region
                }
                
                # Add region-specific fields
                if selected_region == "REG-EU":
                    form_data["vat_number"] = vat_number
                    if eori_number:
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
                    
                    # Display submitted data
                    st.subheader("Submitted WTO Compliance Data")
                    st.json(form_data)
                    
                    # Show compliance certificate
                    st.subheader("WTO Compliance Certificate")
                    
                    # Create a styled certificate
                    certificate_html = f"""
                    <div style="border: 2px solid #1E3A8A; border-radius: 10px; padding: 20px; background-color: #F8FAFC; font-family: Arial, sans-serif;">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <h2 style="color: #1E3A8A; margin-bottom: 5px;">WTO COMPLIANCE CERTIFICATE</h2>
                            <p style="color: #64748B; margin: 0;">Emperor's Computational Governance</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <p>This certifies that the entity with identification <strong>{tax_id}</strong> has been verified for compliance with WTO regulations in the <strong>{regions[selected_region]}</strong> region.</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h3 style="color: #1E3A8A; margin-bottom: 10px;">Compliance Details</h3>
                            <ul style="list-style-type: none; padding-left: 0;">
                                <li style="margin-bottom: 5px;">✓ Documentation Requirements</li>
                                <li style="margin-bottom: 5px;">✓ Regional Trade Agreement Compliance</li>
                                <li style="margin-bottom: 5px;">✓ Tax Regulations Compliance</li>
                                <li style="margin-bottom: 5px;">✓ Export Control Compliance</li>
                            </ul>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h3 style="color: #1E3A8A; margin-bottom: 10px;">Verification Details</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; width: 40%;"><strong>Certificate ID:</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">WTO-{selected_region}-{datetime.now().strftime('%Y%m%d')}-{tax_id[:4]}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Issue Date:</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{datetime.now().strftime('%Y-%m-%d')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Expiry Date:</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{(datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Verification Authority:</strong></td>
                                    <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">Emperor's Computational Governance</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <p style="font-size: 12px; color: #64748B;">This certificate was automatically generated by the Genesis Smart Validation System.</p>
                            <p style="font-size: 12px; color: #64748B;">Verified with divine mechanics and computational alignment.</p>
                        </div>
                    </div>
                    """
                    
                    st.markdown(certificate_html, unsafe_allow_html=True)
                else:
                    st.error("Please fix the errors in the form to achieve WTO compliance.")
    
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
                    # This is a simplified calculation for demonstration purposes
                    # In a real implementation, this would use more sophisticated analysis
                    
                    # Check for positive alignment keywords
                    positive_keywords = {
                        "mission": ["ethical", "sustainable", "eco-friendly", "community", "fair",
                                   "transparent", "integrity", "responsible", "equitable", "green",
                                   "renewable", "conservation", "biodegradable", "welfare", "charitable"],
                        "environmental": ["sustainable", "eco-friendly", "green", "renewable", "conservation", 
                                         "biodegradable", "environmental", "recycled", "natural", "organic", 
                                         "clean", "ecological"],
                        "community": ["community", "social", "welfare", "charitable", "nonprofit", 
                                     "humanitarian", "philanthropic", "giving", "supporting", "uplifting", 
                                     "empowering", "collaborative"],
                        "suppliers": ["fair-trade", "equitable", "just", "ethical-trade", "balanced", 
                                     "fair-wage", "responsible", "sustainable-trade", "ethical-sourcing"]
                    }
                    
                    # Check for negative alignment keywords
                    negative_keywords = {
                        "mission": ["exploit", "manipulate", "deceive", "corrupt", "illegal"],
                        "environmental": ["polluting", "toxic", "harmful", "wasteful", "destructive"],
                        "community": ["exploitative", "unfair", "harmful", "discriminatory", "exclusionary"],
                        "suppliers": ["sweatshop", "underpaid", "exploitative", "unfair", "deceptive"]
                    }
                    
                    # Calculate scores for each field
                    field_scores = {}
                    overall_score = 0.0
                    
                    for field, content in form_data.items():
                        content_lower = content.lower()
                        words = content_lower.split()
                        
                        # Count keyword matches
                        positive_count = sum(1 for word in words if any(keyword in word for keyword in positive_keywords[field]))
                        negative_count = sum(1 for word in words if any(keyword in word for keyword in negative_keywords[field]))
                        
                        # Basic score calculation - this would be more sophisticated in a real implementation
                        base_score = 0.85  # Start with a good baseline score
                        keyword_score = min(0.15, 0.01 * positive_count)  # Positive keywords can add up to 0.15
                        penalty = min(0.50, 0.10 * negative_count)  # Negative keywords can reduce score by up to 0.50
                        
                        field_score = min(1.0, base_score + keyword_score - penalty)
                        field_scores[field] = field_score
                        overall_score += field_score
                    
                    # Calculate average score
                    overall_score = overall_score / len(field_scores)
                    
                    # Display the alignment scores
                    st.subheader("Divine Alignment Assessment")
                    
                    # Create two columns - one for the overall score gauge and one for field scores
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        # Create a simple gauge chart
                        gauge_html = f"""
                        <div style="text-align: center;">
                            <h3 style="margin-bottom: 5px;">Overall Divine Alignment</h3>
                            <div style="margin: 0 auto; width: 200px; height: 200px; position: relative;">
                                <svg width="200" height="200" viewBox="0 0 200 200">
                                    <!-- Background arc -->
                                    <path d="M 20 180 A 90 90 0 0 1 180 180" fill="none" stroke="#e0e0e0" stroke-width="20" />
                                    
                                    <!-- Value arc (dynamic based on score) -->
                                    <path d="M 20 180 A 90 90 0 0 1 {20 + 160 * overall_score} {180 - 160 * overall_score}" fill="none" stroke="{
                                        '#e53935' if overall_score < 0.8 else
                                        '#FFA726' if overall_score < 0.85 else
                                        '#66BB6A' if overall_score < 0.9 else
                                        '#43A047' if overall_score < 0.95 else
                                        '#1E88E5'
                                    }" stroke-width="20" />
                                    
                                    <!-- Centerpoint -->
                                    <circle cx="100" cy="100" r="80" fill="white" />
                                    
                                    <!-- Value text -->
                                    <text x="100" y="100" font-family="Arial" font-size="30" text-anchor="middle" alignment-baseline="middle">{overall_score:.2f}</text>
                                    
                                    <!-- Category text -->
                                    <text x="100" y="130" font-family="Arial" font-size="14" text-anchor="middle" alignment-baseline="middle" fill="{
                                        '#e53935' if overall_score < 0.8 else
                                        '#FFA726' if overall_score < 0.85 else
                                        '#66BB6A' if overall_score < 0.9 else
                                        '#43A047' if overall_score < 0.95 else
                                        '#1E88E5'
                                    }">{
                                        'Insufficient' if overall_score < 0.8 else
                                        'Borderline' if overall_score < 0.85 else
                                        'Acceptable' if overall_score < 0.9 else
                                        'Strong' if overall_score < 0.95 else
                                        'Exceptional'
                                    }</text>
                                </svg>
                            </div>
                        </div>
                        """
                        
                        st.markdown(gauge_html, unsafe_allow_html=True)
                    
                    with col2:
                        # Display component scores
                        st.markdown("### Component Scores")
                        
                        # Display each field score with a progress bar
                        for field, score in field_scores.items():
                            field_name = field.replace("_", " ").title()
                            
                            # Determine color based on score
                            if score < 0.8:
                                color = "red"
                            elif score < 0.85:
                                color = "orange"
                            elif score < 0.9:
                                color = "lightgreen"
                            elif score < 0.95:
                                color = "green"
                            else:
                                color = "blue"
                            
                            # Create a styled progress bar
                            st.markdown(f"""
                            <div style="margin-bottom: 15px;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <span>{field_name}</span>
                                    <span>{score:.2f}</span>
                                </div>
                                <div style="width: 100%; background-color: #e0e0e0; border-radius: 10px; height: 10px;">
                                    <div style="width: {score * 100}%; background-color: {color}; border-radius: 10px; height: 10px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Display alignment category explanation
                    if overall_score >= 0.95:
                        category = "Exceptional Alignment"
                        explanation = "Your organization demonstrates exceptional alignment with divine principles. Your practices reflect a deep commitment to ethical conduct, environmental stewardship, community welfare, and fair trade."
                    elif overall_score >= 0.90:
                        category = "Strong Alignment"
                        explanation = "Your organization demonstrates strong alignment with divine principles. Your practices reflect a solid commitment to ethical conduct, environmental stewardship, community welfare, and fair trade."
                    elif overall_score >= 0.85:
                        category = "Acceptable Alignment"
                        explanation = "Your organization demonstrates acceptable alignment with divine principles. Your practices reflect a basic commitment to ethical conduct, environmental stewardship, community welfare, and fair trade."
                    elif overall_score >= 0.80:
                        category = "Borderline Alignment"
                        explanation = "Your organization demonstrates borderline alignment with divine principles. Consider strengthening your commitment to ethical conduct, environmental stewardship, community welfare, and fair trade."
                    else:
                        category = "Insufficient Alignment - Requires Improvement"
                        explanation = "Your organization's alignment with divine principles requires significant improvement. Please review and enhance your practices related to ethical conduct, environmental stewardship, community welfare, and fair trade."
                    
                    st.markdown(f"""
                    ### Alignment Category: {category}
                    
                    {explanation}
                    """)
                    
                    # Provide recommendations for improvement
                    st.subheader("Recommendations for Divine Alignment Improvement")
                    
                    # Generate recommendations based on lowest scoring components
                    sorted_scores = sorted(field_scores.items(), key=lambda x: x[1])
                    
                    recommendations = []
                    
                    for field, score in sorted_scores:
                        if field == "mission" and score < 0.9:
                            recommendations.append("• Strengthen your mission statement with more explicit references to ethical business practices, transparency, and integrity.")
                        elif field == "environmental" and score < 0.9:
                            recommendations.append("• Enhance your environmental sustainability practices by focusing on specific conservation efforts, renewable resources, and waste reduction initiatives.")
                        elif field == "community" and score < 0.9:
                            recommendations.append("• Develop more robust community engagement initiatives with measurable impact goals and regular community feedback mechanisms.")
                        elif field == "suppliers" and score < 0.9:
                            recommendations.append("• Improve your supplier management practices by implementing fair trade principles, ethical sourcing verification, and supplier diversity programs.")
                    
                    # Add general recommendations if needed
                    if not recommendations:
                        recommendations.append("• Continue maintaining your strong divine alignment by regularly reviewing and enhancing your practices.")
                        recommendations.append("• Consider documenting and sharing your alignment practices to inspire other organizations.")
                    elif len(recommendations) < 2:
                        recommendations.append("• Regularly review and update your alignment practices to ensure continued divine alignment.")
                    
                    for recommendation in recommendations:
                        st.markdown(recommendation)
                    
                    # Option to generate Divine Alignment Certificate
                    if overall_score >= 0.85:
                        st.subheader("Divine Alignment Certificate")
                        
                        # Create a styled certificate
                        certificate_html = f"""
                        <div style="border: 2px solid #1E3A8A; border-radius: 10px; padding: 20px; background-color: #F8FAFC; font-family: Arial, sans-serif;">
                            <div style="text-align: center; margin-bottom: 20px;">
                                <h2 style="color: #1E3A8A; margin-bottom: 5px;">DIVINE ALIGNMENT CERTIFICATE</h2>
                                <p style="color: #64748B; margin: 0;">Emperor's Computational Governance</p>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <p>This certifies that the organization has been assessed for divine alignment and demonstrates <strong>{category}</strong> with a score of <strong>{overall_score:.2f}</strong>.</p>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <h3 style="color: #1E3A8A; margin-bottom: 10px;">Alignment Components</h3>
                                <ul style="list-style-type: none; padding-left: 0;">
                                    <li style="margin-bottom: 5px;">{'✓' if field_scores['mission'] >= 0.85 else '○'} Ethical Conduct: {field_scores['mission']:.2f}</li>
                                    <li style="margin-bottom: 5px;">{'✓' if field_scores['environmental'] >= 0.85 else '○'} Environmental Stewardship: {field_scores['environmental']:.2f}</li>
                                    <li style="margin-bottom: 5px;">{'✓' if field_scores['community'] >= 0.85 else '○'} Community Welfare: {field_scores['community']:.2f}</li>
                                    <li style="margin-bottom: 5px;">{'✓' if field_scores['suppliers'] >= 0.85 else '○'} Fair Trade Practices: {field_scores['suppliers']:.2f}</li>
                                </ul>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <h3 style="color: #1E3A8A; margin-bottom: 10px;">Certificate Details</h3>
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0; width: 40%;"><strong>Certificate ID:</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">DIV-ALIGN-{datetime.now().strftime('%Y%m%d')}-{hash(mission)%10000:04d}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Issue Date:</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{datetime.now().strftime('%Y-%m-%d')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Expiry Date:</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">{(datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d')}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;"><strong>Verification Authority:</strong></td>
                                        <td style="padding: 8px; border-bottom: 1px solid #E2E8F0;">Emperor's Computational Governance</td>
                                    </tr>
                                </table>
                            </div>
                            
                            <div style="text-align: center; margin-top: 30px;">
                                <p style="font-size: 12px; color: #64748B;">This certificate was automatically generated by the Genesis Smart Validation System.</p>
                                <p style="font-size: 12px; color: #64748B;">Verified with divine mechanics and computational alignment.</p>
                            </div>
                        </div>
                        """
                        
                        st.markdown(certificate_html, unsafe_allow_html=True)
                    else:
                        st.warning("A Divine Alignment Certificate is available for organizations with an Acceptable Alignment score (0.85) or higher. Please review the recommendations to improve your alignment.")
                else:
                    st.error("Please fix the errors in the form to achieve divine alignment.")

    # Additional information section at the bottom
    st.markdown("---")
    st.markdown("""
    ### About the Smart Data Validation Tooltip System
    
    The Genesis Smart Data Validation Tooltip System provides real-time validation of input data with context-aware tooltips that guide users through proper data entry. This ensures data integrity across the Genesis Ecosystem while enforcing WTO compliance and divine alignment principles.
    
    **Key Features:**
    - Real-time validation with immediate feedback
    - Context-aware tooltips with helpful guidance
    - WTO regional compliance checking
    - Divine alignment validation for ethical input
    - Multi-language support for global deployment
    
    For more information, refer to the [Genesis Smart Data Validation Tooltip System Documentation](GENESIS_SMART_VALIDATION_TOOLTIP.md).
    """)

if __name__ == "__main__":
    main()