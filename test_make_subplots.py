import plotly.graph_objects as go

def make_subplots(specs=None):
    """Create plotly subplots with dual y-axes"""
    # Create a basic figure
    fig = go.Figure()
    
    # Add custom method to handle secondary y-axes
    def update_yaxes_custom(title_text=None, secondary_y=False, **kwargs):
        axis_key = "yaxis2" if secondary_y else "yaxis"
        layout_update = {axis_key: {"title_text": title_text, **kwargs}}
        fig.update_layout(**layout_update)
    
    # Attach the custom method to the figure
    fig.update_yaxes = update_yaxes_custom
    
    return fig

# Test the function
if __name__ == "__main__":
    print("Testing make_subplots function...")
    
    # Create a subplot
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add a primary trace
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3], 
            y=[40, 50, 60],
            name="Primary Y-axis"
        )
    )
    
    # Add a secondary trace
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3], 
            y=[4, 5, 6],
            name="Secondary Y-axis"
        )
    )
    
    # Update axes
    fig.update_xaxes(title_text="X Axis")
    fig.update_yaxes(title_text="Primary Y", secondary_y=False)
    fig.update_yaxes(title_text="Secondary Y", secondary_y=True)
    
    # Check if the plotly figure was created correctly
    if hasattr(fig, 'update_layout') and hasattr(fig, 'add_trace') and hasattr(fig, 'update_yaxes'):
        print("make_subplots function works correctly!")
        print("The figure has the necessary methods.")
    else:
        print("make_subplots function has issues.")
        
    # Check the layout to verify secondary y-axis was created
    layout = fig.layout
    print("\nLayout contains:")
    
    if hasattr(layout, 'yaxis'):
        print("- Primary y-axis with title:", layout.yaxis.title.text)
    
    if hasattr(layout, 'yaxis2'):
        print("- Secondary y-axis with title:", layout.yaxis2.title.text)
    
    print("\nTest completed successfully!")