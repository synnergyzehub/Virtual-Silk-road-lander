"""
Data Connector Module for Empire OS

- Connects to external data sources (Excel, CSV, API endpoints)
- Transforms data into system-compatible format
- Applies divine principles to data validation
- Maintains data lineage tracking
"""

import os
import json
import pandas as pd
from datetime import datetime
import hashlib
import random

class DataConnector:
    def __init__(self):
        """Initialize the data connector"""
        # Ensure data directories exist
        os.makedirs('data/imported', exist_ok=True)
    
    def import_excel(self, file_path, sheet_name=None, realm_context=None):
        """
        Import data from Excel file
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str, optional): Specific sheet to import
            realm_context (dict, optional): Realm context for data attribution
            
        Returns:
            dict: Import results with data and metadata
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"File not found: {file_path}"
                }
            
            # Read Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                # If no sheet specified, read all sheets
                df = pd.read_excel(file_path, sheet_name=None)
            
            # Generate import ID
            import_id = self._generate_import_id(file_path)
            
            # Create import metadata
            import_time = datetime.now().isoformat()
            filename = os.path.basename(file_path)
            
            metadata = {
                "import_id": import_id,
                "source_file": filename,
                "import_time": import_time,
                "row_count": len(df) if not isinstance(df, dict) else sum(len(sheet) for sheet in df.values()),
                "sheet_name": sheet_name if sheet_name else "All Sheets",
                "columns": list(df.columns) if not isinstance(df, dict) else {name: list(sheet.columns) for name, sheet in df.items()},
                "realm_context": realm_context
            }
            
            # Save imported data 
            data_filename = f"imported_{import_id}.json"
            
            # Convert DataFrame to dict for JSON serialization
            if isinstance(df, dict):
                data_dict = {name: sheet.to_dict(orient='records') for name, sheet in df.items()}
            else:
                data_dict = df.to_dict(orient='records')
            
            with open(f"data/imported/{data_filename}", 'w') as f:
                json.dump(data_dict, f)
            
            # Save metadata
            with open(f"data/imported/{import_id}_metadata.json", 'w') as f:
                json.dump(metadata, f)
            
            # Log the import
            self._log_data_action("import", {
                "import_id": import_id,
                "source": filename,
                "time": import_time,
                "realm_context": realm_context,
                "row_count": metadata["row_count"]
            })
            
            return {
                "success": True,
                "message": f"Successfully imported {metadata['row_count']} rows from {filename}",
                "import_id": import_id,
                "metadata": metadata,
                "data": data_dict
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error importing file: {str(e)}"
            }
    
    def import_csv(self, file_path, realm_context=None):
        """
        Import data from CSV file
        
        Args:
            file_path (str): Path to the CSV file
            realm_context (dict, optional): Realm context for data attribution
            
        Returns:
            dict: Import results with data and metadata
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"File not found: {file_path}"
                }
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Generate import ID
            import_id = self._generate_import_id(file_path)
            
            # Create import metadata
            import_time = datetime.now().isoformat()
            filename = os.path.basename(file_path)
            
            metadata = {
                "import_id": import_id,
                "source_file": filename,
                "import_time": import_time,
                "row_count": len(df),
                "columns": list(df.columns),
                "realm_context": realm_context
            }
            
            # Save imported data 
            data_filename = f"imported_{import_id}.json"
            data_dict = df.to_dict(orient='records')
            
            with open(f"data/imported/{data_filename}", 'w') as f:
                json.dump(data_dict, f)
            
            # Save metadata
            with open(f"data/imported/{import_id}_metadata.json", 'w') as f:
                json.dump(metadata, f)
            
            # Log the import
            self._log_data_action("import", {
                "import_id": import_id,
                "source": filename,
                "time": import_time,
                "realm_context": realm_context,
                "row_count": len(df)
            })
            
            return {
                "success": True,
                "message": f"Successfully imported {len(df)} rows from {filename}",
                "import_id": import_id,
                "metadata": metadata,
                "data": data_dict
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error importing file: {str(e)}"
            }
    
    def get_imported_data(self, import_id):
        """
        Retrieve previously imported data
        
        Args:
            import_id (str): Import identifier
            
        Returns:
            dict: Retrieved data or error message
        """
        try:
            # Check if data file exists
            data_filename = f"data/imported/imported_{import_id}.json"
            metadata_filename = f"data/imported/{import_id}_metadata.json"
            
            if not os.path.exists(data_filename) or not os.path.exists(metadata_filename):
                return {
                    "success": False,
                    "message": f"Import ID not found: {import_id}"
                }
            
            # Read data and metadata
            with open(data_filename, 'r') as f:
                data = json.load(f)
            
            with open(metadata_filename, 'r') as f:
                metadata = json.load(f)
            
            # Log the retrieval
            self._log_data_action("retrieve", {
                "import_id": import_id,
                "time": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "message": f"Successfully retrieved data for import ID: {import_id}",
                "import_id": import_id,
                "metadata": metadata,
                "data": data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving data: {str(e)}"
            }
    
    def get_all_imports(self):
        """
        Get a list of all imported data files
        
        Returns:
            list: Information about all imports
        """
        imports = []
        
        # Find all metadata files
        metadata_files = [f for f in os.listdir("data/imported") if f.endswith("_metadata.json")]
        
        for metadata_file in metadata_files:
            with open(f"data/imported/{metadata_file}", 'r') as f:
                metadata = json.load(f)
                imports.append({
                    "import_id": metadata["import_id"],
                    "source_file": metadata["source_file"],
                    "import_time": metadata["import_time"],
                    "row_count": metadata["row_count"],
                    "realm_context": metadata.get("realm_context")
                })
        
        # Sort by import time (most recent first)
        imports.sort(key=lambda x: x["import_time"], reverse=True)
        
        return imports
    
    def transform_data(self, import_id, transformations):
        """
        Apply transformations to imported data
        
        Args:
            import_id (str): Import identifier
            transformations (list): List of transformation operations
            
        Returns:
            dict: Transformed data
        """
        # Get imported data
        import_result = self.get_imported_data(import_id)
        if not import_result["success"]:
            return import_result
        
        data = import_result["data"]
        
        # If data is multi-sheet, we need to know which sheet to transform
        if isinstance(data, dict) and len(data) > 1:
            # For simplicity, ask to specify the sheet in transformations
            if "sheet" not in transformations:
                return {
                    "success": False,
                    "message": "Multiple sheets found. Please specify the sheet to transform."
                }
            
            sheet = transformations["sheet"]
            if sheet not in data:
                return {
                    "success": False,
                    "message": f"Sheet not found: {sheet}"
                }
            
            # Get the specified sheet
            df = pd.DataFrame(data[sheet])
        else:
            # Single sheet or single-sheet dict
            if isinstance(data, dict) and len(data) == 1:
                df = pd.DataFrame(list(data.values())[0])
            else:
                df = pd.DataFrame(data)
        
        # Apply transformations
        try:
            for operation in transformations.get("operations", []):
                op_type = operation.get("type")
                
                if op_type == "filter":
                    column = operation.get("column")
                    condition = operation.get("condition")
                    value = operation.get("value")
                    
                    if column and condition and value is not None:
                        if condition == "equals":
                            df = df[df[column] == value]
                        elif condition == "not_equals":
                            df = df[df[column] != value]
                        elif condition == "greater_than":
                            df = df[df[column] > value]
                        elif condition == "less_than":
                            df = df[df[column] < value]
                        elif condition == "contains":
                            df = df[df[column].astype(str).str.contains(str(value))]
                
                elif op_type == "select":
                    columns = operation.get("columns", [])
                    if columns:
                        df = df[columns]
                
                elif op_type == "rename":
                    mapping = operation.get("mapping", {})
                    if mapping:
                        df = df.rename(columns=mapping)
                
                elif op_type == "sort":
                    column = operation.get("column")
                    ascending = operation.get("ascending", True)
                    if column:
                        df = df.sort_values(column, ascending=ascending)
                
                elif op_type == "group":
                    columns = operation.get("columns", [])
                    agg_func = operation.get("aggregation", "count")
                    if columns:
                        df = df.groupby(columns).agg(agg_func).reset_index()
            
            # Generate transformation ID
            transform_id = self._generate_transform_id(import_id)
            
            # Create transformed data
            transformed_data = df.to_dict(orient='records')
            
            # Create transformation metadata
            transform_time = datetime.now().isoformat()
            
            metadata = {
                "transform_id": transform_id,
                "import_id": import_id,
                "transform_time": transform_time,
                "transformations": transformations,
                "row_count_before": len(import_result["data"]) if not isinstance(import_result["data"], dict) else sum(len(sheet) for sheet in import_result["data"].values()),
                "row_count_after": len(transformed_data),
                "columns": list(df.columns)
            }
            
            # Save transformed data 
            data_filename = f"transformed_{transform_id}.json"
            
            with open(f"data/imported/{data_filename}", 'w') as f:
                json.dump(transformed_data, f)
            
            # Save metadata
            with open(f"data/imported/{transform_id}_metadata.json", 'w') as f:
                json.dump(metadata, f)
            
            # Log the transformation
            self._log_data_action("transform", {
                "transform_id": transform_id,
                "import_id": import_id,
                "time": transform_time,
                "row_count": len(transformed_data)
            })
            
            return {
                "success": True,
                "message": f"Successfully transformed data to {len(transformed_data)} rows",
                "transform_id": transform_id,
                "metadata": metadata,
                "data": transformed_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error transforming data: {str(e)}"
            }
    
    def validate_data(self, import_id, validation_rules):
        """
        Validate imported data against rules
        
        Args:
            import_id (str): Import identifier
            validation_rules (list): List of validation rules
            
        Returns:
            dict: Validation results
        """
        # Get imported data
        import_result = self.get_imported_data(import_id)
        if not import_result["success"]:
            return import_result
        
        data = import_result["data"]
        
        # Convert to DataFrame for validation
        if isinstance(data, dict) and len(data) > 1:
            # For simplicity, ask to specify the sheet in validation rules
            if "sheet" not in validation_rules:
                return {
                    "success": False,
                    "message": "Multiple sheets found. Please specify the sheet to validate."
                }
            
            sheet = validation_rules["sheet"]
            if sheet not in data:
                return {
                    "success": False,
                    "message": f"Sheet not found: {sheet}"
                }
            
            # Get the specified sheet
            df = pd.DataFrame(data[sheet])
        else:
            # Single sheet or single-sheet dict
            if isinstance(data, dict) and len(data) == 1:
                df = pd.DataFrame(list(data.values())[0])
            else:
                df = pd.DataFrame(data)
        
        # Apply validation rules
        validation_results = []
        passed_all = True
        
        try:
            for rule in validation_rules.get("rules", []):
                rule_type = rule.get("type")
                column = rule.get("column")
                rule_name = rule.get("name", f"Validate {column} - {rule_type}")
                
                if not column:
                    continue
                
                rule_result = {
                    "rule_name": rule_name,
                    "column": column,
                    "type": rule_type,
                    "passed": True,
                    "failures": []
                }
                
                if rule_type == "not_null":
                    null_rows = df[df[column].isnull()]
                    if not null_rows.empty:
                        rule_result["passed"] = False
                        rule_result["failures"] = null_rows.index.tolist()
                        rule_result["failure_count"] = len(null_rows)
                        rule_result["failure_message"] = f"Found {len(null_rows)} rows with null values in column '{column}'"
                
                elif rule_type == "unique":
                    duplicates = df[df.duplicated(subset=[column])]
                    if not duplicates.empty:
                        rule_result["passed"] = False
                        rule_result["failures"] = duplicates.index.tolist()
                        rule_result["failure_count"] = len(duplicates)
                        rule_result["failure_message"] = f"Found {len(duplicates)} duplicate values in column '{column}'"
                
                elif rule_type == "range":
                    min_val = rule.get("min")
                    max_val = rule.get("max")
                    
                    if min_val is not None:
                        below_min = df[df[column] < min_val]
                        if not below_min.empty:
                            rule_result["passed"] = False
                            rule_result["failures"].extend(below_min.index.tolist())
                            rule_result["failure_message"] = f"Found {len(below_min)} values below minimum {min_val} in column '{column}'"
                    
                    if max_val is not None:
                        above_max = df[df[column] > max_val]
                        if not above_max.empty:
                            rule_result["passed"] = False
                            rule_result["failures"].extend(above_max.index.tolist())
                            rule_result["failure_message"] = f"Found {len(above_max)} values above maximum {max_val} in column '{column}'"
                    
                    if not rule_result["passed"]:
                        rule_result["failure_count"] = len(rule_result["failures"])
                
                elif rule_type == "pattern":
                    pattern = rule.get("pattern")
                    if pattern:
                        non_matching = df[~df[column].astype(str).str.match(pattern)]
                        if not non_matching.empty:
                            rule_result["passed"] = False
                            rule_result["failures"] = non_matching.index.tolist()
                            rule_result["failure_count"] = len(non_matching)
                            rule_result["failure_message"] = f"Found {len(non_matching)} values not matching pattern in column '{column}'"
                
                validation_results.append(rule_result)
                
                if not rule_result["passed"]:
                    passed_all = False
            
            # Generate validation ID
            validation_id = self._generate_validation_id(import_id)
            
            # Create validation metadata
            validation_time = datetime.now().isoformat()
            
            metadata = {
                "validation_id": validation_id,
                "import_id": import_id,
                "validation_time": validation_time,
                "rules": validation_rules,
                "passed_all": passed_all,
                "total_rules": len(validation_results),
                "failed_rules": sum(1 for r in validation_results if not r["passed"])
            }
            
            # Save validation results 
            results_filename = f"validation_{validation_id}.json"
            
            with open(f"data/imported/{results_filename}", 'w') as f:
                json.dump({
                    "metadata": metadata,
                    "results": validation_results
                }, f)
            
            # Log the validation
            self._log_data_action("validate", {
                "validation_id": validation_id,
                "import_id": import_id,
                "time": validation_time,
                "passed_all": passed_all
            })
            
            return {
                "success": True,
                "message": "Validation complete",
                "validation_id": validation_id,
                "passed_all": passed_all,
                "metadata": metadata,
                "results": validation_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error validating data: {str(e)}"
            }
    
    def _generate_import_id(self, file_path):
        """Generate a unique import ID based on file path and timestamp"""
        seed = f"{file_path}-{datetime.now().isoformat()}"
        return "imp_" + hashlib.md5(seed.encode()).hexdigest()[:12]
    
    def _generate_transform_id(self, import_id):
        """Generate a unique transform ID based on import ID and timestamp"""
        seed = f"{import_id}-transform-{datetime.now().isoformat()}"
        return "trn_" + hashlib.md5(seed.encode()).hexdigest()[:12]
    
    def _generate_validation_id(self, import_id):
        """Generate a unique validation ID based on import ID and timestamp"""
        seed = f"{import_id}-validate-{datetime.now().isoformat()}"
        return "val_" + hashlib.md5(seed.encode()).hexdigest()[:12]
    
    def _log_data_action(self, action, data):
        """Log data actions to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            **data
        }
        
        # Ensure logs directory exists
        os.makedirs('data/ledger', exist_ok=True)
        
        # Append to log file
        with open('data/ledger/data_ledger.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# For testing
if __name__ == "__main__":
    connector = DataConnector()
    
    # Test with a local file
    file_path = "attached_assets/API_Mapping_Extract copy.xlsx"
    
    if os.path.exists(file_path):
        # Import example Excel file
        result = connector.import_excel(
            file_path,
            realm_context={"realm": "RealmOne", "purpose": "API Integration"}
        )
        
        print(f"Import result: {result['success']}")
        if result['success']:
            print(f"Imported {result['metadata']['row_count']} rows from {result['metadata']['source_file']}")
            
            # Get a list of all imports
            imports = connector.get_all_imports()
            print(f"Total imports: {len(imports)}")
            
            # Apply a transformation
            transform_result = connector.transform_data(
                result['import_id'],
                {
                    "operations": [
                        {"type": "select", "columns": ["API Name", "Endpoint", "Method", "Description"]},
                        {"type": "sort", "column": "API Name", "ascending": True}
                    ]
                }
            )
            
            print(f"Transform result: {transform_result['success']}")
            if transform_result['success']:
                print(f"Transformed to {transform_result['metadata']['row_count_after']} rows")
    else:
        print(f"Test file not found: {file_path}")