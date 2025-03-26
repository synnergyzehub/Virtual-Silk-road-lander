import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_order_confirmation():
    """Display the order confirmation page"""
    
    if not st.session_state.order_submitted or not hasattr(st.session_state, 'order_details'):
        st.error("No order has been submitted. Please complete the order booking process.")
        if st.button("Go to Product Catalog", use_container_width=True):
            st.session_state.page = 'product_catalog'
            st.rerun()
        return
    
    # Order confirmation header with success message
    st.success("Thank you! Your order inquiry has been submitted successfully.")
    
    # Display order details
    st.title("Order Confirmation")
    st.subheader(f"Order ID: {st.session_state.order_details['order_id']}")
    st.write(f"**Order Date:** {st.session_state.order_details['order_date']}")
    
    # Company information
    st.markdown("---")
    st.subheader("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Company Name:** {st.session_state.order_details['company_name']}")
        st.write(f"**Contact Person:** {st.session_state.order_details['contact_person']}")
        st.write(f"**Email:** {st.session_state.order_details['email']}")
    
    with col2:
        st.write(f"**Phone:** {st.session_state.order_details['phone']}")
        st.write(f"**Address:** {st.session_state.order_details['address']}")
    
    # Order summary
    st.markdown("---")
    st.subheader("Order Summary")
    
    # Create a summary table of ordered items
    order_items = []
    for item in st.session_state.cart:
        order_items.append({
            "Product ID": item['product_id'],
            "Product Name": item['product_name'],
            "Quantity": item['total_quantity'],
            "Base Price": item['base_price'],
            "Fabric Option": item['fabric']
        })
    
    if order_items:
        st.table(pd.DataFrame(order_items))
    
    # Calculate totals
    total_quantity = sum(item['total_quantity'] for item in st.session_state.cart)
    total_items = len(st.session_state.cart)
    
    # Delivery and payment info
    st.markdown("---")
    st.subheader("Delivery & Payment Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Shipping Method:** {st.session_state.order_details['shipping_method']}")
        st.write(f"**Incoterms:** {st.session_state.order_details['incoterms']}")
        st.write(f"**Destination:** {st.session_state.order_details['destination_port']}")
        st.write(f"**Requested Delivery:** {st.session_state.order_details['requested_delivery']}")
    
    with col2:
        st.write(f"**Payment Terms:** {st.session_state.order_details['payment_terms']}")
        st.write(f"**Payment Method:** {st.session_state.order_details['payment_method']}")
    
    if st.session_state.order_details['additional_comments']:
        st.markdown("---")
        st.subheader("Additional Comments")
        st.write(st.session_state.order_details['additional_comments'])
    
    # Next steps and timeline
    st.markdown("---")
    st.subheader("Next Steps")
    
    # Timeline visualization using Plotly
    timeline_dates = {
        "Order Received": datetime.now(),
        "Order Review": datetime.now() + timedelta(days=2),
        "Sample Production": datetime.now() + timedelta(days=10),
        "Sample Approval": datetime.now() + timedelta(days=17),
        "Production Start": datetime.now() + timedelta(days=20),
        "Production Complete": datetime.now() + timedelta(days=40),
        "Quality Check": datetime.now() + timedelta(days=45),
        "Ready for Shipment": datetime.now() + timedelta(days=50)
    }
    
    # Create the timeline chart
    fig = go.Figure()
    
    # Add events as markers
    fig.add_trace(go.Scatter(
        x=list(timeline_dates.values()),
        y=[1] * len(timeline_dates),
        mode="markers+text",
        marker=dict(symbol="circle", size=20, color="#1E88E5"),
        text=list(timeline_dates.keys()),
        textposition="bottom center",
        hoverinfo="text+x",
        hovertext=[f"{event}: {date.strftime('%Y-%m-%d')}" for event, date in timeline_dates.items()]
    ))
    
    # Add a line connecting all events
    fig.add_trace(go.Scatter(
        x=list(timeline_dates.values()),
        y=[1] * len(timeline_dates),
        mode="lines",
        line=dict(color="#1E88E5", width=2),
        hoverinfo="none"
    ))
    
    # Configure the layout
    fig.update_layout(
        title="Estimated Production Timeline",
        xaxis=dict(
            title="Date",
            type="date",
            tickformat="%Y-%m-%d",
            tickangle=45
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        height=300,
        margin=dict(l=20, r=20, t=60, b=120),
        showlegend=False,
        template="plotly_dark"
    )
    
    # Display the timeline
    st.plotly_chart(fig, use_container_width=True)
    
    # Information about what happens next
    st.markdown("""
    ### What Happens Next?
    
    1. **Order Review (1-2 business days):**
       Our team will review your order and contact you to confirm details.
    
    2. **Sample Production (7-10 business days):**
       We will produce samples of your selected items with your customizations.
    
    3. **Sample Approval:**
       Samples will be sent for your approval before full production begins.
    
    4. **Production:**
       Once samples are approved, full production will begin.
    
    5. **Quality Check & Packaging:**
       Rigorous quality checks before packaging and shipment.
    
    6. **Shipment:**
       Products will be shipped according to your selected method and incoterms.
    """)
    
    # Contact information
    st.markdown("---")
    st.subheader("Need Assistance?")
    st.write("For any questions regarding your order, please contact:")
    st.write("**Email:** orders@buyinghouse.com")
    st.write("**Phone:** +1-800-555-0123")
    st.write("**Order Reference:** Please mention your Order ID in all communications.")
    
    # Return to home or place new order
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Home", use_container_width=True):
            # Reset only order details but keep user as onboarded
            st.session_state.page = 'product_catalog'
            st.session_state.selected_product = None
            st.session_state.cart = []
            st.session_state.order_submitted = False
            if hasattr(st.session_state, 'order_details'):
                delattr(st.session_state, 'order_details')
            st.rerun()
            
    with col2:
        if st.button("Place Another Order", use_container_width=True):
            # Keep user onboarded but reset order details
            st.session_state.page = 'product_catalog'
            st.session_state.selected_product = None
            st.session_state.cart = []
            st.session_state.order_submitted = False
            if hasattr(st.session_state, 'order_details'):
                delattr(st.session_state, 'order_details')
            st.rerun()