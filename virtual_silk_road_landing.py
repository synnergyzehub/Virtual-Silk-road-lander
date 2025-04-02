import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show_virtual_silk_road_landing():
    """Display the public landing page for Virtual Silk Road - Marketing focused"""
    
    # Create a visually striking header for marketing appeal
    st.markdown(
        """
        <div style='background: linear-gradient(90deg, rgba(30,58,138,1) 0%, rgba(123,104,238,1) 100%); padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>🏙️ Virtual Silk Road</h1>
            <p style='color: #E0E0FF; margin: 15px 0 0 0; font-size: 1.5rem;'>The Digital Twin for Enterprise Governance</p>
            <p style='color: #E0E0FF; margin: 10px 0 0 0; font-style: italic;'>Powered by Empire OS</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Hero section with main value proposition
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## Enterprise Governance Reimagined
        
        Virtual Silk Road creates a complete digital twin of your enterprise ecosystem, 
        connecting manufacturing, retail, and management operations through a 
        unified governance framework.
        
        ### Democratizing Enterprise Governance
        While competitors charge **$20,000+** for similar solutions, our modular license 
        model makes enterprise-grade governance accessible to businesses of all sizes.
        
        **"The equivalent of Simulink for your business operations."**
        """)
        
        # Call-to-action button
        st.markdown("""
        <div style='background-color: #4B0082; color: white; padding: 15px; border-radius: 5px; text-align: center; margin: 25px 0; cursor: pointer;'>
            <h3 style='margin: 0; color: white;'>Request Demo Access</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Add note about Emperor access
        st.info("👑 **Emperor's Note**: For the comprehensive governance visualization with real-time controls and detailed analytics, request Emperor-level access to view the private Virtual Silk Road Command Center.")
    
    with col2:
        # Create a simple visual representation
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Create concentric circles
        circle1 = plt.Circle((0.5, 0.5), 0.4, color='#1E3A8A', alpha=0.7)
        circle2 = plt.Circle((0.5, 0.5), 0.3, color='#7B68EE', alpha=0.7)
        circle3 = plt.Circle((0.5, 0.5), 0.2, color='#990099', alpha=0.9)
        circle4 = plt.Circle((0.5, 0.5), 0.1, color='gold', alpha=1)
        
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        ax.add_patch(circle4)
        
        # Add text labels
        ax.text(0.5, 0.9, "Empire OS Ecosystem", ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(0.5, 0.5, "Virtual\nSilk Road", ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Add connecting points around the circles
        for i in range(8):
            angle = i * np.pi/4
            x = 0.5 + 0.45 * np.cos(angle)
            y = 0.5 + 0.45 * np.sin(angle)
            ax.plot([0.5, x], [0.5, y], 'k-', alpha=0.3, linewidth=1)
            ax.plot(x, y, 'o', color='white', markersize=6)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        st.pyplot(fig)
    
    # External system integration
    st.markdown("## Integrated Ecosystem")
    st.markdown("Virtual Silk Road connects seamlessly with your existing infrastructure:")
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("""
        <div style='background-color: rgba(30, 58, 138, 0.1); padding: 15px; border-radius: 5px; height: 200px; border: 1px solid #1E3A8A;'>
            <h3 style='color: #1E3A8A; margin-top: 0;'>Empire OS</h3>
            <p>The central operating system that manages licenses, user permissions, and governance controls.</p>
            <p style='position: absolute; bottom: 15px;'><a href='https://empire-os.replit.app/auth'>Learn More →</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style='background-color: rgba(153, 0, 153, 0.1); padding: 15px; border-radius: 5px; height: 200px; border: 1px solid #990099;'>
            <h3 style='color: #990099; margin-top: 0;'>Synergyze</h3>
            <p>SAAS platform providing specialized modules for manufacturing, retail, and management operations.</p>
            <p style='position: absolute; bottom: 15px;'><a href='https://synnergyze.com/'>Learn More →</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div style='background-color: rgba(255, 69, 0, 0.1); padding: 15px; border-radius: 5px; height: 200px; border: 1px solid #FF4500;'>
            <h3 style='color: #FF4500; margin-top: 0;'>Fashion Renderer</h3>
            <p>Specialized visualization tool for product design rendering and virtual showrooms.</p>
            <p style='position: absolute; bottom: 15px;'><a href='https://fashion-renderer-faiz32.replit.app/'>Learn More →</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key features
    st.markdown("## Key Features")
    
    features = [
        {
            "title": "Emperor-Level Oversight",
            "icon": "👑",
            "description": "Complete visibility across all operations and functions for leadership"
        },
        {
            "title": "HSN Code Integration",
            "icon": "💲",
            "description": "Automated taxation using Harmonized System of Nomenclature codes"
        },
        {
            "title": "API-Driven Architecture",
            "icon": "🔌",
            "description": "Connect to any existing system through our comprehensive API gateway"
        },
        {
            "title": "Customizable License Structure",
            "icon": "🔑",
            "description": "Modular licensing allows you to pay only for what you need"
        }
    ]
    
    # Two columns for features
    col1, col2 = st.columns(2)
    
    # First two features in first column
    with col1:
        for feature in features[:2]:
            st.markdown(f"""
            <div style='background-color: rgba(123, 104, 238, 0.05); padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #7B68EE'>
                <h3>{feature['icon']} {feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Last two features in second column
    with col2:
        for feature in features[2:]:
            st.markdown(f"""
            <div style='background-color: rgba(123, 104, 238, 0.05); padding: 15px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #7B68EE'>
                <h3>{feature['icon']} {feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Benefits comparison
    st.markdown("## Why Choose Virtual Silk Road?")
    
    # Comparison table
    comparison_data = {
        'Feature': [
            'Unified Governance View',
            'Real-time Supply Chain Insights',
            'HSN Code Integration',
            'Emperor-level Oversight',
            'Marketing & Sales Portal',
            'Custom License Templates',
            'API-driven Architecture',
            'ROI Analytics'
        ],
        'Virtual Silk Road': [
            '✅ Included',
            '✅ Included',
            '✅ Included',
            '✅ Included',
            '✅ Included',
            '✅ Included',
            '✅ Included',
            '✅ Included'
        ],
        'Competitors': [
            '✅ $20,000+',
            '❌ Extra Module',
            '❌ Not Available',
            '❌ Limited Access',
            '❌ Separate System',
            '❌ Fixed Templates',
            '⚠️ Limited APIs',
            '⚠️ Basic Only'
        ]
    }
    
    # Create DataFrame
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display comparison
    st.dataframe(df_comparison, hide_index=True)
    
    # Pricing advantage message
    st.markdown("""
    <div style="background-color: rgba(50, 205, 50, 0.1); padding: 15px; border-radius: 5px; border-left: 5px solid #32CD32; margin: 20px 0;">
        <h3 style="color: #32CD32; margin-top: 0;">💰 Price Advantage</h3>
        <p style="font-size: 1.1em;">Our modular licensing approach provides enterprise-grade governance at <b>60-80% less</b> than competing solutions, democratizing access for businesses of all sizes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonial section
    st.markdown("## From Our Clients")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: rgba(30, 58, 138, 0.05); padding: 20px; border-radius: 5px; border: 1px solid #1E3A8A; height: 200px;">
            <p style="font-style: italic; font-size: 1.1em;">"Virtual Silk Road has transformed how we manage our supply chain. The Emperor-level view gives our leadership unprecedented visibility across operations."</p>
            <p style="text-align: right;"><b>— CFO, Major Apparel Brand</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(30, 58, 138, 0.05); padding: 20px; border-radius: 5px; border: 1px solid #1E3A8A; height: 200px;">
            <p style="font-style: italic; font-size: 1.1em;">"The HSN code integration alone saved us countless hours in tax compliance. The entire system pays for itself within months."</p>
            <p style="text-align: right;"><b>— COO, Retail Distribution Network</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final call-to-action
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(75,0,130,0.9) 0%, rgba(123,104,238,0.9) 100%); 
                padding: 30px; border-radius: 10px; margin-top: 40px; text-align: center; color: white;">
        <h2 style="color: white; margin-top: 0;">Ready to Transform Your Enterprise Governance?</h2>
        <p style="font-size: 1.2em; margin: 20px 0;">
            Contact our Marketing Officer to discover the perfect license package for your organization.
        </p>
        <div style="margin: 30px 0 15px 0;">
            <span style="background-color: white; color: #4B0082; padding: 12px 25px; border-radius: 30px; font-weight: bold; display: inline-block; margin-right: 20px;">
                Request Demo & Pricing ➔
            </span>
            <span style="background-color: transparent; color: white; padding: 12px 25px; border-radius: 30px; font-weight: bold; display: inline-block; border: 1px solid white;">
                View Documentation
            </span>
        </div>
        <p style="font-size: 0.9em; margin-top: 20px; opacity: 0.8;">
            Democratizing enterprise governance through the Empire OS ecosystem
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with links to other ecosystem components
    st.markdown("""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center;">
        <p>Part of the Empire OS Ecosystem</p>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px;">
            <a href="https://empire-os.replit.app/auth" style="text-decoration: none; color: #1E3A8A;">Empire OS</a>
            <a href="https://synnergyze.com/" style="text-decoration: none; color: #990099;">Synergyze</a>
            <a href="https://fashion-renderer-faiz32.replit.app/" style="text-decoration: none; color: #FF4500;">Fashion Renderer</a>
        </div>
        <p style="margin-top: 20px; font-size: 0.8em; color: #888;">
            © 2025 Virtual Silk Road. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)