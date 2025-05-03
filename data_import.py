import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import random
from core.modules.data_connector import DataConnector

def show_data_import():
    """
    Display the Data Import interface - part of the Empire OS
    where external data is integrated and transformed.
    """
    st.title("Data Import & Integration - Empire OS")
    st.subheader("External Data Integration with Divine Alignment")
    
    # Initialize data connector
    connector = DataConnector()
    
    # Create sidebar for navigation
    st.sidebar.title("Empire OS Navigation")
    page = st.sidebar.selectbox(
        "Choose Function",
        ["Import Data", "Data Inventory", "Data Transformations", "Validation & Quality", "Integration Metrics"]
    )
    
    if page == "Import Data":
        show_data_import_form(connector)
    elif page == "Data Inventory":
        show_data_inventory(connector)
    elif page == "Data Transformations":
        show_data_transformations(connector)
    elif page == "Validation & Quality":
        show_data_validation(connector)
    elif page == "Integration Metrics":
        show_integration_metrics(connector)

def show_data_import_form(connector):
    """Display form for importing data from files"""
    st.header("Import External Data")
    
    # File uploader for Excel files
    st.subheader("Upload Excel File")
    uploaded_excel = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    
    if uploaded_excel is not None:
        # Save uploaded file temporarily
        with open(f"data/imported/{uploaded_excel.name}", "wb") as f:
            f.write(uploaded_excel.getbuffer())
        
        # Get sheet names for selection
        try:
            excel_file = pd.ExcelFile(f"data/imported/{uploaded_excel.name}")
            sheet_names = excel_file.sheet_names
            
            # Sheet selection
            selected_sheet = st.selectbox("Select Sheet", ["All Sheets"] + sheet_names)
            
            # Preview data
            if selected_sheet == "All Sheets":
                st.write("Preview first sheet:")
                df = pd.read_excel(f"data/imported/{uploaded_excel.name}", sheet_name=sheet_names[0])
            else:
                st.write(f"Preview of sheet: {selected_sheet}")
                df = pd.read_excel(f"data/imported/{uploaded_excel.name}", sheet_name=selected_sheet)
            
            st.dataframe(df.head())
            
            # Realm context for data attribution
            st.subheader("Data Attribution")
            realm = st.selectbox("Assign to Realm", ["RealmOne", "RealmTwo", "RealmThree"])
            purpose = st.text_input("Import Purpose")
            
            realm_context = {
                "realm": realm,
                "purpose": purpose,
                "import_time": datetime.now().isoformat()
            }
            
            # Import button
            if st.button("Import Data"):
                with st.spinner("Importing data..."):
                    if selected_sheet == "All Sheets":
                        result = connector.import_excel(
                            f"data/imported/{uploaded_excel.name}",
                            realm_context=realm_context
                        )
                    else:
                        result = connector.import_excel(
                            f"data/imported/{uploaded_excel.name}",
                            sheet_name=selected_sheet,
                            realm_context=realm_context
                        )
                
                if result["success"]:
                    st.success(result["message"])
                    
                    # Generate divine alignment score for import (mock)
                    alignment_score = random.randint(70, 95)
                    divine_principle = random.choice([
                        "Al-Adl (Justice)", "Ar-Rahman (Mercy)", "Al-Hakim (Wisdom)", 
                        "Al-Alim (Knowledge)", "Al-Muqsit (Equity)"
                    ])
                    
                    # Display alignment metrics
                    st.subheader("Divine Alignment Assessment")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Alignment Score", f"{alignment_score}%")
                        st.markdown(f"**Dominant Principle:** {divine_principle}")
                        
                        if alignment_score >= 90:
                            st.success("Excellent alignment with divine principles")
                        elif alignment_score >= 80:
                            st.info("Good alignment with divine principles")
                        elif alignment_score >= 70:
                            st.warning("Satisfactory alignment - consider transformation")
                        else:
                            st.error("Poor alignment - requires transformation")
                    
                    with col2:
                        # Create a gauge chart for alignment score
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=alignment_score,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Divine Alignment"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 60], 'color': "red"},
                                    {'range': [60, 70], 'color': "orange"},
                                    {'range': [70, 85], 'color': "yellow"},
                                    {'range': [85, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "black", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 85
                                }
                            }
                        ))
                        st.plotly_chart(fig)
                else:
                    st.error(result["message"])
        
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
    
    # File uploader for CSV files
    st.subheader("Upload CSV File")
    uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_csv is not None:
        # Save uploaded file temporarily
        with open(f"data/imported/{uploaded_csv.name}", "wb") as f:
            f.write(uploaded_csv.getbuffer())
        
        # Preview data
        try:
            df = pd.read_csv(f"data/imported/{uploaded_csv.name}")
            st.write("Preview:")
            st.dataframe(df.head())
            
            # Realm context for data attribution
            st.subheader("Data Attribution")
            realm = st.selectbox("Assign to Realm", ["RealmOne", "RealmTwo", "RealmThree"], key="csv_realm")
            purpose = st.text_input("Import Purpose", key="csv_purpose")
            
            realm_context = {
                "realm": realm,
                "purpose": purpose,
                "import_time": datetime.now().isoformat()
            }
            
            # Import button
            if st.button("Import CSV Data"):
                with st.spinner("Importing data..."):
                    result = connector.import_csv(
                        f"data/imported/{uploaded_csv.name}",
                        realm_context=realm_context
                    )
                
                if result["success"]:
                    st.success(result["message"])
                    
                    # Generate divine alignment score for import (mock)
                    alignment_score = random.randint(70, 95)
                    divine_principle = random.choice([
                        "Al-Adl (Justice)", "Ar-Rahman (Mercy)", "Al-Hakim (Wisdom)", 
                        "Al-Alim (Knowledge)", "Al-Muqsit (Equity)"
                    ])
                    
                    # Display alignment metrics
                    st.subheader("Divine Alignment Assessment")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Alignment Score", f"{alignment_score}%")
                        st.markdown(f"**Dominant Principle:** {divine_principle}")
                        
                        if alignment_score >= 90:
                            st.success("Excellent alignment with divine principles")
                        elif alignment_score >= 80:
                            st.info("Good alignment with divine principles")
                        elif alignment_score >= 70:
                            st.warning("Satisfactory alignment - consider transformation")
                        else:
                            st.error("Poor alignment - requires transformation")
                    
                    with col2:
                        # Create a gauge chart for alignment score
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=alignment_score,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Divine Alignment"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 60], 'color': "red"},
                                    {'range': [60, 70], 'color': "orange"},
                                    {'range': [70, 85], 'color': "yellow"},
                                    {'range': [85, 100], 'color': "green"}
                                ],
                                'threshold': {
                                    'line': {'color': "black", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 85
                                }
                            }
                        ))
                        st.plotly_chart(fig)
                else:
                    st.error(result["message"])
        
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
    
    # Using existing local files (from attached_assets)
    st.subheader("Import from Attached Assets")
    
    # Find Excel and CSV files in attached_assets
    asset_files = []
    
    if os.path.exists("attached_assets"):
        for file in os.listdir("attached_assets"):
            if file.endswith((".xlsx", ".xls", ".csv")):
                asset_files.append(file)
    
    if asset_files:
        selected_asset = st.selectbox("Select File", asset_files)
        file_path = f"attached_assets/{selected_asset}"
        
        if selected_asset.endswith((".xlsx", ".xls")):
            # Excel file
            try:
                excel_file = pd.ExcelFile(file_path)
                sheet_names = excel_file.sheet_names
                
                # Sheet selection
                selected_sheet = st.selectbox("Select Sheet", ["All Sheets"] + sheet_names, key="asset_sheet")
                
                # Preview data
                if selected_sheet == "All Sheets":
                    st.write("Preview first sheet:")
                    df = pd.read_excel(file_path, sheet_name=sheet_names[0])
                else:
                    st.write(f"Preview of sheet: {selected_sheet}")
                    df = pd.read_excel(file_path, sheet_name=selected_sheet)
                
                st.dataframe(df.head())
                
                # Realm context for data attribution
                st.subheader("Data Attribution")
                realm = st.selectbox("Assign to Realm", ["RealmOne", "RealmTwo", "RealmThree"], key="asset_realm")
                purpose = st.text_input("Import Purpose", key="asset_purpose")
                
                realm_context = {
                    "realm": realm,
                    "purpose": purpose,
                    "import_time": datetime.now().isoformat()
                }
                
                # Import button
                if st.button("Import Asset", key="import_asset"):
                    with st.spinner("Importing data..."):
                        if selected_sheet == "All Sheets":
                            result = connector.import_excel(
                                file_path,
                                realm_context=realm_context
                            )
                        else:
                            result = connector.import_excel(
                                file_path,
                                sheet_name=selected_sheet,
                                realm_context=realm_context
                            )
                    
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])
            
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
        
        elif selected_asset.endswith(".csv"):
            # CSV file
            try:
                df = pd.read_csv(file_path)
                st.write("Preview:")
                st.dataframe(df.head())
                
                # Realm context for data attribution
                st.subheader("Data Attribution")
                realm = st.selectbox("Assign to Realm", ["RealmOne", "RealmTwo", "RealmThree"], key="asset_csv_realm")
                purpose = st.text_input("Import Purpose", key="asset_csv_purpose")
                
                realm_context = {
                    "realm": realm,
                    "purpose": purpose,
                    "import_time": datetime.now().isoformat()
                }
                
                # Import button
                if st.button("Import Asset", key="import_csv_asset"):
                    with st.spinner("Importing data..."):
                        result = connector.import_csv(
                            file_path,
                            realm_context=realm_context
                        )
                    
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])
            
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
    else:
        st.info("No Excel or CSV files found in attached_assets directory")

def show_data_inventory(connector):
    """Display inventory of imported data"""
    st.header("Data Inventory")
    
    # Get all imports
    imports = connector.get_all_imports()
    
    if not imports:
        st.info("No data has been imported yet")
        return
    
    # Display summary
    st.subheader("Import Summary")
    
    total_rows = sum(imp.get("row_count", 0) for imp in imports)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Imports", len(imports))
    with col2:
        st.metric("Total Records", total_rows)
    with col3:
        st.metric("Unique Sources", len(set(imp.get("source_file") for imp in imports)))
    
    # Create a DataFrame for visualization
    imports_df = pd.DataFrame(imports)
    
    # Convert import_time to datetime
    imports_df["import_time"] = pd.to_datetime(imports_df["import_time"])
    imports_df["date"] = imports_df["import_time"].dt.date
    
    # Import volume over time
    st.subheader("Import Volume Over Time")
    
    imports_by_date = imports_df.groupby("date").size().reset_index(name="count")
    imports_by_date["date"] = pd.to_datetime(imports_by_date["date"])
    
    fig = px.line(
        imports_by_date,
        x="date",
        y="count",
        title="Imports by Date"
    )
    st.plotly_chart(fig)
    
    # Data distribution by realm
    st.subheader("Data Distribution by Realm")
    
    # Extract realm from realm_context
    imports_df["realm"] = imports_df["realm_context"].apply(
        lambda x: x.get("realm") if isinstance(x, dict) else "Unknown"
    )
    
    realm_counts = imports_df["realm"].value_counts().reset_index()
    realm_counts.columns = ["Realm", "Count"]
    
    fig = px.pie(
        realm_counts,
        values="Count",
        names="Realm",
        title="Data Distribution by Realm"
    )
    st.plotly_chart(fig)
    
    # List of imports with details
    st.subheader("Import Details")
    
    # Enable sorting
    sorted_imports = sorted(imports, key=lambda x: x["import_time"], reverse=True)
    
    for i, imp in enumerate(sorted_imports):
        with st.expander(f"{imp['source_file']} - {imp['import_time']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Source:** {imp['source_file']}")
                st.markdown(f"**Import Time:** {imp['import_time']}")
                st.markdown(f"**Row Count:** {imp['row_count']}")
            
            with col2:
                if isinstance(imp.get("realm_context"), dict):
                    realm = imp["realm_context"].get("realm", "Unknown")
                    purpose = imp["realm_context"].get("purpose", "")
                    st.markdown(f"**Realm:** {realm}")
                    st.markdown(f"**Purpose:** {purpose}")
                
                # View data button
                if st.button("View Data", key=f"view_{i}"):
                    result = connector.get_imported_data(imp["import_id"])
                    if result["success"]:
                        st.json(result["data"], expanded=False)
                    else:
                        st.error(result["message"])
                
                # Transform data button
                if st.button("Transform Data", key=f"transform_{i}"):
                    st.session_state.selected_import_id = imp["import_id"]
                    st.session_state.current_page = "Data Transformations"
                    st.rerun()
                
                # Validate data button
                if st.button("Validate Data", key=f"validate_{i}"):
                    st.session_state.selected_import_id = imp["import_id"]
                    st.session_state.current_page = "Validation & Quality"
                    st.rerun()

def show_data_transformations(connector):
    """Display data transformation interface"""
    st.header("Data Transformations")
    
    # Get all imports
    imports = connector.get_all_imports()
    
    if not imports:
        st.info("No data has been imported yet")
        return
    
    # Import selection
    import_options = [f"{imp['source_file']} - {imp['import_id']}" for imp in imports]
    
    # Default selection from session state if available
    default_index = 0
    if hasattr(st.session_state, 'selected_import_id'):
        for i, imp in enumerate(imports):
            if imp["import_id"] == st.session_state.selected_import_id:
                default_index = i
                break
    
    selected_import = st.selectbox(
        "Select Import to Transform",
        import_options,
        index=default_index
    )
    
    selected_import_id = selected_import.split(" - ")[1]
    
    # Preview the selected import
    import_result = connector.get_imported_data(selected_import_id)
    
    if not import_result["success"]:
        st.error(import_result["message"])
        return
    
    # Check if data is multi-sheet
    is_multi_sheet = isinstance(import_result["data"], dict) and len(import_result["data"]) > 1
    
    if is_multi_sheet:
        # Sheet selection
        sheet_options = list(import_result["data"].keys())
        selected_sheet = st.selectbox("Select Sheet", sheet_options)
        
        # Preview the selected sheet
        preview_data = import_result["data"][selected_sheet]
        preview_df = pd.DataFrame(preview_data)
    else:
        # Single sheet data
        if isinstance(import_result["data"], dict) and len(import_result["data"]) == 1:
            # Single sheet in dict format
            preview_data = list(import_result["data"].values())[0]
        else:
            # Directly as list
            preview_data = import_result["data"]
        
        preview_df = pd.DataFrame(preview_data)
        selected_sheet = None
    
    # Show preview
    st.subheader("Data Preview")
    st.dataframe(preview_df.head())
    
    # Show available columns
    columns = list(preview_df.columns)
    st.subheader("Available Columns")
    st.write(", ".join(columns))
    
    # Transformation builder
    st.subheader("Build Transformation")
    
    # Initialize transformations if not in session state
    if "transformations" not in st.session_state:
        st.session_state.transformations = {
            "sheet": selected_sheet,
            "operations": []
        }
    
    # Update sheet selection if changed
    if selected_sheet != st.session_state.transformations.get("sheet"):
        st.session_state.transformations["sheet"] = selected_sheet
    
    # Add operation form
    with st.form("add_operation"):
        st.write("Add Transformation Operation")
        
        operation_type = st.selectbox(
            "Operation Type",
            ["filter", "select", "rename", "sort", "group"]
        )
        
        # Different inputs based on operation type
        if operation_type == "filter":
            column = st.selectbox("Column to Filter", columns)
            condition = st.selectbox(
                "Condition",
                ["equals", "not_equals", "greater_than", "less_than", "contains"]
            )
            value = st.text_input("Value")
            
            operation = {
                "type": "filter",
                "column": column,
                "condition": condition,
                "value": value
            }
        
        elif operation_type == "select":
            selected_columns = st.multiselect("Columns to Keep", columns)
            
            operation = {
                "type": "select",
                "columns": selected_columns
            }
        
        elif operation_type == "rename":
            col1, col2 = st.columns(2)
            rename_map = {}
            
            with col1:
                st.write("Original Column")
                original_col = st.selectbox("Original Column", columns)
            
            with col2:
                st.write("New Column Name")
                new_col = st.text_input("New Name")
                
                if original_col and new_col:
                    rename_map[original_col] = new_col
            
            operation = {
                "type": "rename",
                "mapping": rename_map
            }
        
        elif operation_type == "sort":
            column = st.selectbox("Column to Sort", columns)
            ascending = st.checkbox("Ascending Order", value=True)
            
            operation = {
                "type": "sort",
                "column": column,
                "ascending": ascending
            }
        
        elif operation_type == "group":
            group_columns = st.multiselect("Columns to Group By", columns)
            agg_func = st.selectbox(
                "Aggregation Function",
                ["count", "sum", "mean", "min", "max"]
            )
            
            operation = {
                "type": "group",
                "columns": group_columns,
                "aggregation": agg_func
            }
        
        # Submit button
        submitted = st.form_submit_button("Add Operation")
        if submitted:
            st.session_state.transformations["operations"].append(operation)
    
    # Show current transformation operations
    st.subheader("Current Transformation Pipeline")
    
    for i, op in enumerate(st.session_state.transformations["operations"]):
        op_type = op["type"]
        
        if op_type == "filter":
            st.write(f"{i+1}. Filter: {op['column']} {op['condition']} {op['value']}")
        elif op_type == "select":
            st.write(f"{i+1}. Select columns: {', '.join(op['columns'])}")
        elif op_type == "rename":
            renames = [f"{old} -> {new}" for old, new in op["mapping"].items()]
            st.write(f"{i+1}. Rename columns: {', '.join(renames)}")
        elif op_type == "sort":
            direction = "ascending" if op["ascending"] else "descending"
            st.write(f"{i+1}. Sort by {op['column']} ({direction})")
        elif op_type == "group":
            st.write(f"{i+1}. Group by {', '.join(op['columns'])} and {op['aggregation']}")
        
        # Remove button
        if st.button(f"Remove", key=f"remove_{i}"):
            st.session_state.transformations["operations"].pop(i)
            st.rerun()
    
    # Clear all button
    if st.button("Clear All Operations"):
        st.session_state.transformations["operations"] = []
        st.rerun()
    
    # Apply transformation button
    if st.button("Apply Transformation"):
        with st.spinner("Applying transformation..."):
            result = connector.transform_data(
                selected_import_id,
                st.session_state.transformations
            )
        
        if result["success"]:
            st.success(result["message"])
            
            # Show result preview
            st.subheader("Transformation Result")
            result_df = pd.DataFrame(result["data"])
            st.dataframe(result_df.head())
            
            # Reset operations
            st.session_state.transformations["operations"] = []
        else:
            st.error(result["message"])

def show_data_validation(connector):
    """Display data validation interface"""
    st.header("Data Validation & Quality")
    
    # Get all imports
    imports = connector.get_all_imports()
    
    if not imports:
        st.info("No data has been imported yet")
        return
    
    # Import selection
    import_options = [f"{imp['source_file']} - {imp['import_id']}" for imp in imports]
    
    # Default selection from session state if available
    default_index = 0
    if hasattr(st.session_state, 'selected_import_id'):
        for i, imp in enumerate(imports):
            if imp["import_id"] == st.session_state.selected_import_id:
                default_index = i
                break
    
    selected_import = st.selectbox(
        "Select Import to Validate",
        import_options,
        index=default_index
    )
    
    selected_import_id = selected_import.split(" - ")[1]
    
    # Preview the selected import
    import_result = connector.get_imported_data(selected_import_id)
    
    if not import_result["success"]:
        st.error(import_result["message"])
        return
    
    # Check if data is multi-sheet
    is_multi_sheet = isinstance(import_result["data"], dict) and len(import_result["data"]) > 1
    
    if is_multi_sheet:
        # Sheet selection
        sheet_options = list(import_result["data"].keys())
        selected_sheet = st.selectbox("Select Sheet", sheet_options)
        
        # Preview the selected sheet
        preview_data = import_result["data"][selected_sheet]
        preview_df = pd.DataFrame(preview_data)
    else:
        # Single sheet data
        if isinstance(import_result["data"], dict) and len(import_result["data"]) == 1:
            # Single sheet in dict format
            preview_data = list(import_result["data"].values())[0]
        else:
            # Directly as list
            preview_data = import_result["data"]
        
        preview_df = pd.DataFrame(preview_data)
        selected_sheet = None
    
    # Show preview
    st.subheader("Data Preview")
    st.dataframe(preview_df.head())
    
    # Show available columns
    columns = list(preview_df.columns)
    st.subheader("Available Columns")
    st.write(", ".join(columns))
    
    # Validation rule builder
    st.subheader("Build Validation Rules")
    
    # Initialize validation rules if not in session state
    if "validation_rules" not in st.session_state:
        st.session_state.validation_rules = {
            "sheet": selected_sheet,
            "rules": []
        }
    
    # Update sheet selection if changed
    if selected_sheet != st.session_state.validation_rules.get("sheet"):
        st.session_state.validation_rules["sheet"] = selected_sheet
    
    # Add rule form
    with st.form("add_rule"):
        st.write("Add Validation Rule")
        
        rule_type = st.selectbox(
            "Rule Type",
            ["not_null", "unique", "range", "pattern"]
        )
        
        rule_name = st.text_input("Rule Name (Optional)")
        column = st.selectbox("Column to Validate", columns)
        
        # Different inputs based on rule type
        if rule_type == "range":
            min_val = st.number_input("Minimum Value", value=0)
            max_val = st.number_input("Maximum Value", value=100)
            
            rule = {
                "type": "range",
                "name": rule_name,
                "column": column,
                "min": min_val,
                "max": max_val
            }
        
        elif rule_type == "pattern":
            pattern = st.text_input("Regex Pattern")
            
            rule = {
                "type": "pattern",
                "name": rule_name,
                "column": column,
                "pattern": pattern
            }
        
        else:  # not_null or unique
            rule = {
                "type": rule_type,
                "name": rule_name,
                "column": column
            }
        
        # Submit button
        submitted = st.form_submit_button("Add Rule")
        if submitted:
            st.session_state.validation_rules["rules"].append(rule)
    
    # Show current validation rules
    st.subheader("Current Validation Rules")
    
    for i, rule in enumerate(st.session_state.validation_rules["rules"]):
        rule_type = rule["type"]
        column = rule["column"]
        name = rule.get("name") or f"Rule {i+1}"
        
        if rule_type == "not_null":
            st.write(f"{i+1}. {name}: Column '{column}' must not contain nulls")
        elif rule_type == "unique":
            st.write(f"{i+1}. {name}: Column '{column}' must contain unique values")
        elif rule_type == "range":
            min_val = rule.get("min")
            max_val = rule.get("max")
            st.write(f"{i+1}. {name}: Column '{column}' values must be between {min_val} and {max_val}")
        elif rule_type == "pattern":
            pattern = rule.get("pattern")
            st.write(f"{i+1}. {name}: Column '{column}' values must match pattern '{pattern}'")
        
        # Remove button
        if st.button(f"Remove", key=f"remove_rule_{i}"):
            st.session_state.validation_rules["rules"].pop(i)
            st.rerun()
    
    # Clear all button
    if st.button("Clear All Rules"):
        st.session_state.validation_rules["rules"] = []
        st.rerun()
    
    # Run validation button
    if st.button("Run Validation"):
        with st.spinner("Running validation..."):
            result = connector.validate_data(
                selected_import_id,
                st.session_state.validation_rules
            )
        
        if result["success"]:
            st.success("Validation complete")
            
            # Show validation results
            st.subheader("Validation Results")
            
            # Overall result
            if result["passed_all"]:
                st.success("✅ All validation rules passed!")
            else:
                st.error(f"❌ {result['metadata']['failed_rules']} rule(s) failed")
            
            # Individual rule results
            for rule_result in result["results"]:
                with st.expander(f"{rule_result['rule_name']} - {rule_result['column']} ({rule_result['type']})"):
                    if rule_result["passed"]:
                        st.success("Rule passed!")
                    else:
                        st.error(f"Rule failed: {rule_result.get('failure_message', 'Validation failed')}")
                        st.markdown(f"**Failure Count:** {rule_result.get('failure_count', 0)}")
                        
                        # Show sample of failing rows
                        if rule_result.get("failures"):
                            st.markdown("**Sample of failing row indices:**")
                            st.write(rule_result["failures"][:10])  # Show first 10 failures
            
            # Reset rules
            st.session_state.validation_rules["rules"] = []
        else:
            st.error(result["message"])

def show_integration_metrics(connector):
    """Display data integration metrics and statistics"""
    st.header("Data Integration Metrics")
    
    # Get all imports
    imports = connector.get_all_imports()
    
    if not imports:
        st.info("No data has been imported yet")
        return
    
    # Summary metrics
    st.subheader("Integration Summary")
    
    total_rows = sum(imp.get("row_count", 0) for imp in imports)
    total_sources = len(set(imp.get("source_file") for imp in imports))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Imports", len(imports))
    with col2:
        st.metric("Total Records", f"{total_rows:,}")
    with col3:
        st.metric("Unique Sources", total_sources)
    
    # Create a DataFrame for visualization
    imports_df = pd.DataFrame(imports)
    
    # Mock integration quality score (would come from actual validation in real system)
    quality_score = random.randint(70, 95)
    
    # Display quality score
    st.subheader("Data Quality Metrics")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=quality_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Data Quality"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "red"},
                {'range': [60, 70], 'color': "orange"},
                {'range': [70, 85], 'color': "yellow"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    st.plotly_chart(fig)
    
    # Divine principle alignment
    st.subheader("Divine Principle Alignment")
    
    # Mock divine principle metrics
    principles = [
        "Al-Adl (Justice)", "Ar-Rahman (Mercy)", "Al-Hakim (Wisdom)", 
        "Al-Alim (Knowledge)", "Al-Muqsit (Equity)"
    ]
    
    principle_scores = {
        principle: random.randint(60, 95) 
        for principle in principles
    }
    
    principle_df = pd.DataFrame({
        "Principle": list(principle_scores.keys()),
        "Score": list(principle_scores.values())
    })
    
    # Create bar chart for principle alignment
    principle_fig = px.bar(
        principle_df,
        x="Principle",
        y="Score",
        color="Score",
        color_continuous_scale=px.colors.sequential.Viridis,
        title="Divine Principle Alignment Scores"
    )
    st.plotly_chart(principle_fig)
    
    # Data distribution by realm
    st.subheader("Data Distribution by Realm")
    
    # Extract realm from realm_context
    imports_df["realm"] = imports_df["realm_context"].apply(
        lambda x: x.get("realm") if isinstance(x, dict) else "Unknown"
    )
    
    # Create treemap of data by realm and source
    if "source_file" in imports_df.columns and "realm" in imports_df.columns and "row_count" in imports_df.columns:
        fig = px.treemap(
            imports_df,
            path=['realm', 'source_file'],
            values='row_count',
            title="Data Volume by Realm and Source"
        )
        st.plotly_chart(fig)
    
    # Integration timeline
    st.subheader("Integration Timeline")
    
    # Convert import_time to datetime
    if "import_time" in imports_df.columns:
        imports_df["import_time"] = pd.to_datetime(imports_df["import_time"])
        imports_df["date"] = imports_df["import_time"].dt.date
        
        # Daily import counts
        daily_imports = imports_df.groupby("date").size().reset_index(name="count")
        daily_imports["date"] = pd.to_datetime(daily_imports["date"])
        
        # Daily record counts
        daily_records = imports_df.groupby("date")["row_count"].sum().reset_index()
        daily_records["date"] = pd.to_datetime(daily_records["date"])
        
        # Create dual-axis chart
        fig = go.Figure()
        
        # Add imports line
        fig.add_trace(go.Scatter(
            x=daily_imports["date"],
            y=daily_imports["count"],
            name="Import Count",
            line=dict(color='blue', width=2)
        ))
        
        # Add records line on secondary axis
        fig.add_trace(go.Scatter(
            x=daily_records["date"],
            y=daily_records["row_count"],
            name="Record Count",
            line=dict(color='red', width=2),
            yaxis='y2'
        ))
        
        # Update layout for dual y-axes
        fig.update_layout(
            title='Import and Record Counts Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(
                title='Import Count',
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title='Record Count',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        st.plotly_chart(fig)
    
    # Data integration health
    st.subheader("Integration Health")
    
    # Mock data for integration health
    health_metrics = {
        "Data Completeness": random.uniform(70, 95),
        "Data Accuracy": random.uniform(75, 98),
        "Schema Consistency": random.uniform(80, 99),
        "Reference Integrity": random.uniform(65, 90),
        "Divine Alignment": random.uniform(70, 90)
    }
    
    health_df = pd.DataFrame({
        "Metric": list(health_metrics.keys()),
        "Score": list(health_metrics.values())
    })
    
    # Create radar chart for health metrics
    fig = px.line_polar(
        health_df,
        r="Score",
        theta="Metric",
        line_close=True,
        range_r=[0, 100],
        title="Data Integration Health"
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    show_data_import()