try:
    import streamlit
    print('Successfully imported streamlit')
except ImportError as e:
    print(f'Error importing streamlit: {e}')

try:
    import pandas
    print('Successfully imported pandas')
except ImportError as e:
    print(f'Error importing pandas: {e}')

try:
    import plotly
    print('Successfully imported plotly')
except ImportError as e:
    print(f'Error importing plotly: {e}')

try:
    import numpy
    print('Successfully imported numpy')
except ImportError as e:
    print(f'Error importing numpy: {e}')