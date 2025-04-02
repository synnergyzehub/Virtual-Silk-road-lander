import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show_synergyze_landing():
    """Display the public landing page for Synergyze - The licenses sold through the Virtual Silk Road"""
    
    # Create a visually striking header for Synergyze
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, rgba(75,0,130,0.9) 0%, rgba(138,43,226,0.9) 100%); padding: 35px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>⚡ Synergyze</h1>
            <p style='color: #E0E0FF; margin: 15px 0 0 0; font-size: 1.5rem;'>Enterprise License Solutions</p>
            <p style='color: #E0E0FF; margin: 10px 0 0 0; font-style: italic;'>Powered by Empire OS | Distributed on the Virtual Silk Road</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Main value proposition
    st.markdown("""
    ## Transform Your Enterprise with Synergyze Licenses
    
    Synergyze provides a comprehensive suite of enterprise license solutions that bring the power 
    of Empire OS to your organization. Operating exclusively on the Virtual Silk Road network,
    Synergyze licenses deliver unparalleled capabilities for manufacturing, retail, distribution, 
    and management operations.
    """)
    
    # License packages
    st.subheader("License Solutions")
    
    # Create license package cards in three columns
    license_col1, license_col2, license_col3 = st.columns(3)
    
    with license_col1:
        st.markdown("""
        <div style='background-color: rgba(75, 0, 130, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(75, 0, 130, 0.3); height: 400px; position: relative;'>
            <h3 style='color: #4B0082;'>Manufacturing License</h3>
            <p style='font-weight: bold; color: #4B0082;'>Empire-grade production management</p>
            <ul style='padding-left: 20px;'>
                <li>Complete production lifecycle management</li>
                <li>Material procurement optimization</li>
                <li>Cut-Make-Pack (CMP) tracking</li>
                <li>Quality control automation</li>
                <li>HSN code integration for taxation</li>
                <li>Inventory synchronization</li>
                <li>Real-time production analytics</li>
            </ul>
            <div style='position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;'>
                <span style='background-color: #4B0082; color: white; padding: 8px 20px; border-radius: 20px; display: inline-block;'>
                    Request Demo
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with license_col2:
        st.markdown("""
        <div style='background-color: rgba(75, 0, 130, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(75, 0, 130, 0.3); height: 400px; position: relative;'>
            <h3 style='color: #4B0082;'>Retail Distribution License</h3>
            <p style='font-weight: bold; color: #4B0082;'>Emperor-approved distribution networks</p>
            <ul style='padding-left: 20px;'>
                <li>Multi-channel inventory management</li>
                <li>Automated stock distribution</li>
                <li>Point-of-sale integration</li>
                <li>Demand forecasting algorithms</li>
                <li>Logistics optimization</li>
                <li>Retailer performance analytics</li>
                <li>Return merchandise automation</li>
            </ul>
            <div style='position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;'>
                <span style='background-color: #4B0082; color: white; padding: 8px 20px; border-radius: 20px; display: inline-block;'>
                    Request Demo
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with license_col3:
        st.markdown("""
        <div style='background-color: rgba(75, 0, 130, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(75, 0, 130, 0.3); height: 400px; position: relative;'>
            <h3 style='color: #4B0082;'>Management Hub License</h3>
            <p style='font-weight: bold; color: #4B0082;'>Imperial oversight capabilities</p>
            <ul style='padding-left: 20px;'>
                <li>Emperor's dashboard visualization</li>
                <li>CFO financial oversight tools</li>
                <li>CIO data governance interface</li>
                <li>Virtual Silk Road visualization</li>
                <li>Cross-system analytics</li>
                <li>Predictive business intelligence</li>
                <li>Strategic governance controls</li>
            </ul>
            <div style='position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;'>
                <span style='background-color: #4B0082; color: white; padding: 8px 20px; border-radius: 20px; display: inline-block;'>
                    Request Demo
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # License benefits
    st.markdown("## Why Choose Synergyze Licenses?")
    
    benefits_col1, benefits_col2 = st.columns(2)
    
    with benefits_col1:
        st.markdown("""
        ### Enterprise-Grade Capabilities
        
        - **Imperial Integration**: Direct connection to Empire OS through the Virtual Silk Road
        - **Governance Controls**: Built-in compliance with imperial standards
        - **Data Federation**: Cross-license data sharing with proper governance 
        - **Scalability**: Expand your license portfolio as your empire grows
        - **API Access**: Connect to existing systems through secure API gateways
        """)
    
    with benefits_col2:
        st.markdown("""
        ### Democratized Enterprise Solutions
        
        - **Cost-Effective**: 60-80% less than competing solutions
        - **Modular Approach**: Pay only for the licenses you need
        - **Quick Deployment**: Operational within days, not months
        - **No Vendor Lock-in**: Open API standards for integration
        - **Continuous Updates**: New capabilities released quarterly
        """)
    
    # ROI calculator
    st.markdown("## Return on Investment")
    
    roi_col1, roi_col2 = st.columns([2, 1])
    
    with roi_col1:
        st.markdown("### Calculate Your Synergyze ROI")
        
        # Create a simple ROI chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sample ROI data
        months = range(1, 13)
        investment = [5000] * 12
        cumulative_investment = np.cumsum(investment)
        
        # Savings grow over time
        savings = [0, 500, 2000, 4000, 7000, 11000, 16000, 22000, 29000, 37000, 46000, 56000]
        
        # Plot cumulative investment
        ax.plot(months, cumulative_investment, 'r-', linewidth=2, label='Cumulative Investment')
        
        # Plot cumulative savings
        ax.plot(months, savings, 'g-', linewidth=2, label='Cumulative Savings')
        
        # Fill the area where savings exceed investment
        break_even_point = np.argwhere(np.array(savings) >= np.array(cumulative_investment))[0][0]
        ax.fill_between(months[break_even_point:], cumulative_investment[break_even_point:], 
                        savings[break_even_point:], color='green', alpha=0.3)
        
        # Add break-even annotation
        ax.axvline(x=break_even_point + 1, color='black', linestyle='--')
        ax.text(break_even_point + 1.2, max(savings)/2, f'Break Even: Month {break_even_point + 1}', 
                verticalalignment='center')
        
        # Set labels and title
        ax.set_xlabel('Months')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Typical Synergyze License ROI')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Display the chart
        st.pyplot(fig)
    
    with roi_col2:
        st.markdown("### Average Client Results")
        
        # ROI metrics
        st.markdown("""
        <div style="background-color: rgba(75, 0, 130, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h4 style="margin-top: 0; color: #4B0082;">6-Month ROI</h4>
            <h2 style="margin: 0; color: #4B0082;">220%</h2>
            <p style="margin: 0;">Average return on investment</p>
        </div>
        
        <div style="background-color: rgba(75, 0, 130, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h4 style="margin-top: 0; color: #4B0082;">Efficiency Gain</h4>
            <h2 style="margin: 0; color: #4B0082;">35%</h2>
            <p style="margin: 0;">Operational efficiency improvement</p>
        </div>
        
        <div style="background-color: rgba(75, 0, 130, 0.1); padding: 15px; border-radius: 5px;">
            <h4 style="margin-top: 0; color: #4B0082;">Cost Reduction</h4>
            <h2 style="margin: 0; color: #4B0082;">25%</h2>
            <p style="margin: 0;">Average operational cost savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("## Client Testimonials")
    
    # Three-column testimonial layout
    test_col1, test_col2, test_col3 = st.columns(3)
    
    with test_col1:
        st.markdown("""
        <div style="background-color: rgba(75, 0, 130, 0.05); padding: 20px; border-radius: 10px; height: 200px; border-left: 3px solid #4B0082;">
            <p style="font-style: italic;">"The Manufacturing License transformed our production efficiency, reducing material waste by 22% and improving throughput by 30%."</p>
            <p style="text-align: right; font-weight: bold;">— Production Director, Major Apparel Brand</p>
        </div>
        """, unsafe_allow_html=True)
    
    with test_col2:
        st.markdown("""
        <div style="background-color: rgba(75, 0, 130, 0.05); padding: 20px; border-radius: 10px; height: 200px; border-left: 3px solid #4B0082;">
            <p style="font-style: italic;">"Synergyze Retail Distribution License automated our inventory management across 42 stores, eliminating stockouts and reducing overstock by 45%."</p>
            <p style="text-align: right; font-weight: bold;">— VP of Retail Operations, Fashion Retailer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with test_col3:
        st.markdown("""
        <div style="background-color: rgba(75, 0, 130, 0.05); padding: 20px; border-radius: 10px; height: 200px; border-left: 3px solid #4B0082;">
            <p style="font-style: italic;">"The Emperor-level dashboard gives me unprecedented visibility across all operations. I can now make strategic decisions based on real-time data."</p>
            <p style="text-align: right; font-weight: bold;">— CEO, Fashion Manufacturing Group</p>
        </div>
        """, unsafe_allow_html=True)
    
    # License acquisition process
    st.markdown("## License Acquisition Process")
    
    # Create step cards
    process_cols = st.columns(4)
    
    steps = [
        {
            "number": "01",
            "title": "Consultation",
            "description": "Meet with our Marketing Officer to discuss your specific needs and requirements."
        },
        {
            "number": "02",
            "title": "Customization",
            "description": "Receive a customized license package recommendation from the Emperor's advisors."
        },
        {
            "number": "03",
            "title": "Implementation",
            "description": "Quick deployment on the Virtual Silk Road with Empire OS integration."
        },
        {
            "number": "04",
            "title": "Optimization",
            "description": "Ongoing support and optimization to maximize your license ROI."
        }
    ]
    
    for i, col in enumerate(process_cols):
        with col:
            step = steps[i]
            st.markdown(f"""
            <div style="background-color: rgba(75, 0, 130, 0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(75, 0, 130, 0.3); text-align: center; height: 200px;">
                <h2 style="color: #4B0082; font-size: 2.5rem; margin: 0;">{step['number']}</h2>
                <h4 style="color: #4B0082; margin: 10px 0;">{step['title']}</h4>
                <p>{step['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(75,0,130,0.9) 0%, rgba(138,43,226,0.9) 100%); 
                padding: 30px; border-radius: 10px; margin-top: 40px; text-align: center; color: white;">
        <h2 style="color: white; margin-top: 0;">Ready to Synergyze Your Enterprise?</h2>
        <p style="font-size: 1.2em; margin: 20px 0;">
            Contact our Marketing Officer to discover the perfect Synergyze license package for your organization.
        </p>
        <div style="margin: 30px 0 15px 0;">
            <span style="background-color: white; color: #4B0082; padding: 12px 25px; border-radius: 30px; font-weight: bold; display: inline-block; margin-right: 20px;">
                Request Demo & Pricing ➔
            </span>
            <span style="background-color: transparent; color: white; padding: 12px 25px; border-radius: 30px; font-weight: bold; display: inline-block; border: 1px solid white;">
                View License Documentation
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with platform hierarchy
    st.markdown("""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin: 20px 0;">
            <div>
                <p style="font-weight: bold; color: gold; margin: 0;">👑 EMPIRE OS</p>
                <p style="font-size: 0.8em; color: #666; margin: 0;">The Operating System</p>
            </div>
            <div>→</div>
            <div>
                <p style="font-weight: bold; color: #4B0082; margin: 0;">🌏 VIRTUAL SILK ROAD</p>
                <p style="font-size: 0.8em; color: #666; margin: 0;">The Network</p>
            </div>
            <div>→</div>
            <div>
                <p style="font-weight: bold; color: #8A2BE2; margin: 0;">⚡ SYNERGYZE</p>
                <p style="font-size: 0.8em; color: #666; margin: 0;">The Licenses</p>
            </div>
        </div>
        <p style="margin-top: 20px; font-size: 0.8em; color: #888;">
            © 2025 Synergyze. All licenses issued under imperial authority.
        </p>
    </div>
    """, unsafe_allow_html=True)