import streamlit as st
import pandas as pd
import os
import json
import sys

def show_diagnostic():
    """
    Display diagnostic information about the Empire OS installation
    """
    st.title("Empire OS Diagnostic Tool")
    st.subheader("System Information")
    
    # Python version
    st.markdown(f"**Python Version:** {sys.version}")
    
    # Installed packages
    st.subheader("Installed Packages")
    
    try:
        import pkg_resources
        packages = sorted([f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set])
        
        # Display in a dataframe for better visibility
        pkg_df = pd.DataFrame({"Package": packages})
        st.dataframe(pkg_df)
    except Exception as e:
        st.error(f"Error getting package information: {e}")
    
    # Directory structure
    st.subheader("Directory Structure")
    
    try:
        # Current working directory
        st.markdown(f"**Current Directory:** {os.getcwd()}")
        
        # List files in project directory
        files = sorted(os.listdir('.'))
        file_df = pd.DataFrame({"Files": files})
        st.dataframe(file_df)
        
        # Check important directories
        core_exists = os.path.exists('core')
        data_exists = os.path.exists('data')
        modules_exists = os.path.exists('core/modules')
        
        st.markdown(f"**Core Directory Exists:** {'✅' if core_exists else '❌'}")
        st.markdown(f"**Data Directory Exists:** {'✅' if data_exists else '❌'}")
        st.markdown(f"**Modules Directory Exists:** {'✅' if modules_exists else '❌'}")
    except Exception as e:
        st.error(f"Error checking directory structure: {e}")
    
    # Module imports test
    st.subheader("Module Import Test")
    
    modules = [
        "streamlit", "pandas", "plotly.express", "plotly.graph_objects",
        "emperor_timeline", "virtual_silk_road", "empire_os_dashboard", 
        "github_floors", "data_import",
        "core.modules.digital_me", "core.modules.license_gateway", 
        "core.modules.esg_validator", "core.modules.realm_scanner", 
        "core.modules.transformer", "core.modules.github_integration",
        "core.modules.data_connector"
    ]
    
    results = []
    for module in modules:
        try:
            __import__(module)
            results.append({"Module": module, "Status": "✅ Imported successfully"})
        except ImportError as e:
            results.append({"Module": module, "Status": f"❌ Import failed: {e}"})
    
    # Display results
    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
    
    # File content check
    st.subheader("File Content Check")
    
    files_to_check = [
        "app.py",
        "core/modules/digital_me.py", 
        "core/modules/license_gateway.py",
        "core/modules/esg_validator.py",
        "core/modules/realm_scanner.py",
        "core/modules/transformer.py",
        "core/modules/github_integration.py",
        "core/modules/data_connector.py",
        "emperor_timeline.py",
        "empire_os_dashboard.py",
        "virtual_silk_road.py",
        "github_floors.py",
        "data_import.py"
    ]
    
    file_results = []
    for file_path in files_to_check:
        try:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                file_results.append({"File": file_path, "Status": f"✅ Exists ({size} bytes)"})
            else:
                file_results.append({"File": file_path, "Status": "❌ Missing"})
        except Exception as e:
            file_results.append({"File": file_path, "Status": f"❌ Error: {e}"})
    
    # Display results
    file_df = pd.DataFrame(file_results)
    st.dataframe(file_df)
    
    # Streamlit configuration check
    st.subheader("Streamlit Configuration")
    
    try:
        if os.path.exists('.streamlit/config.toml'):
            with open('.streamlit/config.toml', 'r') as f:
                st.code(f.read(), language='toml')
        else:
            st.warning("Streamlit config.toml file not found")
    except Exception as e:
        st.error(f"Error reading Streamlit config: {e}")
    
    # Show system environment variables (excluding sensitive ones)
    st.subheader("Environment Variables")
    
    try:
        env_vars = {k: v for k, v in os.environ.items() 
                  if not any(sensitive in k.lower() for sensitive in ['key', 'token', 'secret', 'password', 'auth'])}
        
        # Convert to dataframe
        env_df = pd.DataFrame(list(env_vars.items()), columns=['Variable', 'Value'])
        st.dataframe(env_df)
    except Exception as e:
        st.error(f"Error reading environment variables: {e}")

if __name__ == "__main__":
    show_diagnostic()