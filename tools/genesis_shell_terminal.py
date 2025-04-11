#!/usr/bin/env python3
"""
Genesis Shell (Terminal Version) - Indexed Component Interface

This script provides a simple terminal-based implementation of the Genesis Shell
for navigating and managing all components within the Genesis Stack container.
It offers a paginated workflow for efficient license management across the system.
"""

import os
import sys
import json
import argparse
import textwrap
from datetime import datetime

# Component types with their icons and descriptions
COMPONENT_TYPES = {
    "license": {
        "icon": "🔑",
        "description": "Entity license for Genesis Stack operations"
    },
    "npu": {
        "icon": "🧠",
        "description": "Neural Processing Unit for computational governance"
    },
    "cloudshell": {
        "icon": "☁️",
        "description": "Cloud Shell fragment for entity operations"
    },
    "synergyze": {
        "icon": "⚙️",
        "description": "SynergyzeOS license for entity distribution"
    },
    "governance": {
        "icon": "⚖️",
        "description": "Governance rules for computational alignment"
    },
    "divine": {
        "icon": "✨",
        "description": "Divine Alignment Layer filters"
    }
}

class GenesisShellTerminal:
    """Genesis Shell Terminal - Simple terminal interface for Genesis Stack."""
    
    def __init__(self):
        """Initialize the shell."""
        self.current_page = 0
        self.items_per_page = 10
        self.filter_text = ""
        self.filter_type = None
        self.components = []
        self.filtered_components = []
        
        # Load component data
        self.load_components()
    
    def load_components(self):
        """Load all components from the data directories."""
        self.components = []
        
        # Load licenses
        license_dir = "data/licenses"
        if os.path.exists(license_dir):
            for filename in os.listdir(license_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(license_dir, filename), 'r') as f:
                            license_data = json.load(f)
                            self.components.append({
                                "id": license_data.get("license_id", filename.replace(".json", "")),
                                "name": license_data.get("entity_name", "Unknown Entity"),
                                "type": "license",
                                "status": license_data.get("status", "unknown"),
                                "created": license_data.get("created_at", ""),
                                "data": license_data
                            })
                    except Exception:
                        pass
        
        # Load NPU nodes
        npu_dir = "data/npu_nodes"
        if os.path.exists(npu_dir):
            for filename in os.listdir(npu_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(npu_dir, filename), 'r') as f:
                            npu_data = json.load(f)
                            self.components.append({
                                "id": npu_data.get("node_id", filename.replace(".json", "")),
                                "name": f"NPU Node {npu_data.get('node_id', '')}",
                                "type": "npu",
                                "status": npu_data.get("status", "unknown"),
                                "created": npu_data.get("created_at", ""),
                                "data": npu_data
                            })
                    except Exception:
                        pass
        
        # Load governance rules
        rules_dir = "data/governance_rules"
        if os.path.exists(rules_dir):
            for filename in os.listdir(rules_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(rules_dir, filename), 'r') as f:
                            rules_data = json.load(f)
                            self.components.append({
                                "id": rules_data.get("node_id", filename.replace("_governance.json", "")),
                                "name": f"Governance Rules for {rules_data.get('node_id', '')}",
                                "type": "governance",
                                "status": "active",
                                "created": rules_data.get("created_at", ""),
                                "data": rules_data
                            })
                    except Exception:
                        pass
        
        # Load divine filters
        filters_dir = "data/divine_filters"
        if os.path.exists(filters_dir):
            for filename in os.listdir(filters_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(filters_dir, filename), 'r') as f:
                            filters_data = json.load(f)
                            self.components.append({
                                "id": filters_data.get("node_id", filename.replace("_filters.json", "")),
                                "name": f"Divine Filters for {filters_data.get('node_id', '')}",
                                "type": "divine",
                                "status": "active",
                                "created": filters_data.get("created_at", ""),
                                "data": filters_data
                            })
                    except Exception:
                        pass
        
        # Load license assignments
        assignments_dir = "data/license_assignments"
        if os.path.exists(assignments_dir):
            for filename in os.listdir(assignments_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(assignments_dir, filename), 'r') as f:
                            assignment_data = json.load(f)
                            self.components.append({
                                "id": f"{assignment_data.get('license_id', '')}_{assignment_data.get('node_id', '')}",
                                "name": f"License Assignment: {assignment_data.get('entity_name', '')} to {assignment_data.get('node_id', '')}",
                                "type": "synergyze",
                                "status": assignment_data.get("status", "unknown"),
                                "created": assignment_data.get("assigned_at", ""),
                                "data": assignment_data
                            })
                    except Exception:
                        pass
        
        # Load entities from config directory as cloud shells
        config_dir = "config"
        if os.path.exists(config_dir):
            for dirname in os.listdir(config_dir):
                entity_dir = os.path.join(config_dir, dirname)
                if os.path.isdir(entity_dir) and dirname not in ["default", "entity-template"]:
                    entity_file = os.path.join(entity_dir, "entity.json")
                    if os.path.exists(entity_file):
                        try:
                            with open(entity_file, 'r') as f:
                                entity_data = json.load(f)
                                self.components.append({
                                    "id": entity_data.get("entity_id", dirname),
                                    "name": entity_data.get("entity_name", dirname),
                                    "type": "cloudshell",
                                    "status": "configured",
                                    "created": entity_data.get("created_at", ""),
                                    "data": entity_data
                                })
                        except Exception:
                            pass
        
        # Apply filtering
        self.apply_filters()
    
    def apply_filters(self):
        """Apply filters to the components list."""
        self.filtered_components = []
        
        for component in self.components:
            # Apply text filter
            if self.filter_text:
                # Search in ID, name, and type
                if (self.filter_text.lower() not in component["id"].lower() and
                    self.filter_text.lower() not in component["name"].lower() and
                    self.filter_text.lower() not in component["type"].lower()):
                    continue
            
            # Apply type filter
            if self.filter_type and component["type"] != self.filter_type:
                continue
            
            self.filtered_components.append(component)
        
        # Reset pagination if needed
        total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
        if total_pages > 0 and self.current_page >= total_pages:
            self.current_page = total_pages - 1
    
    def run(self):
        """Run the terminal shell interface."""
        while True:
            # Clear screen (works on both Windows and Unix-like systems)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Show header
            self.show_header()
            
            # Show component list
            self.show_component_list()
            
            # Show pagination info
            total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
            if total_pages > 0:
                pagination_info = f"Page {self.current_page + 1}/{total_pages} - {len(self.filtered_components)} items"
            else:
                pagination_info = "No items"
            
            print(f"\n{pagination_info}")
            
            # Show command prompt
            print("\nCommands:")
            print("  q: Quit         f: Filter by type    s: Search")
            print("  n: Next page    p: Previous page     v: View component")
            print("  r: Reload       h: Help              #: View component by number")
            
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'q':
                break
            elif command == 'n':
                total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
                if total_pages > 0:
                    self.current_page = min(total_pages - 1, self.current_page + 1)
            elif command == 'p':
                self.current_page = max(0, self.current_page - 1)
            elif command == 'r':
                self.load_components()
                print("Components reloaded.")
                input("Press Enter to continue...")
            elif command == 'f':
                self.filter_by_type()
            elif command == 's':
                self.search_components()
            elif command == 'v':
                self.view_component()
            elif command == 'h':
                self.show_help()
            elif command.isdigit():
                # View component by number
                index = int(command) - 1
                start_index = self.current_page * self.items_per_page
                if 0 <= index < min(self.items_per_page, len(self.filtered_components) - start_index):
                    self.view_component_by_index(start_index + index)
                else:
                    print(f"Invalid component number. Valid range: 1-{min(self.items_per_page, len(self.filtered_components) - start_index)}")
                    input("Press Enter to continue...")
    
    def show_header(self):
        """Show the header."""
        print("=" * 80)
        print(" GENESIS SHELL - Indexed Component Interface ".center(80))
        print("=" * 80)
        
        # Show filter information
        filter_info = "Filter: "
        if self.filter_type:
            filter_info += f"Type={self.filter_type} "
        if self.filter_text:
            filter_info += f"Text={self.filter_text} "
        if not self.filter_type and not self.filter_text:
            filter_info += "None"
        
        print(filter_info)
        print("-" * 80)
    
    def show_component_list(self):
        """Show the component list."""
        print(f"{'#':<3} {'ID':<20} {'Name':<40} {'Type':<15} {'Status':<10} {'Created'}")
        print("-" * 120)
        
        # Calculate pagination
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(self.filtered_components))
        
        if start_index >= len(self.filtered_components):
            print("No components found.")
            return
        
        # Show items
        for i in range(start_index, end_index):
            component = self.filtered_components[i]
            index = i - start_index
            
            # Format the row data
            type_icon = COMPONENT_TYPES.get(component["type"], {}).get("icon", "❓")
            type_display = f"{type_icon} {component['type'].capitalize()}"
            
            id_str = component["id"][:19].ljust(20)
            name_str = component["name"][:39].ljust(40)
            type_str = type_display.ljust(15)
            status_str = component["status"].capitalize().ljust(10)
            
            # Format created date if available
            created_str = ""
            if component["created"]:
                try:
                    created_date = datetime.fromisoformat(component["created"].replace("Z", "+00:00"))
                    created_str = created_date.strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    created_str = component["created"]
            
            print(f"{index+1:<3} {id_str} {name_str} {type_str} {status_str} {created_str}")
    
    def filter_by_type(self):
        """Filter components by type."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 80)
        print(" FILTER BY TYPE ".center(80))
        print("=" * 80)
        print("0. Clear filter")
        
        for i, (comp_type, info) in enumerate(COMPONENT_TYPES.items(), 1):
            print(f"{i}. {info['icon']} {comp_type.capitalize()} - {info['description']}")
        
        print("\nc. Cancel")
        
        choice = input("\nSelect type filter: ").strip().lower()
        
        if choice == '0':
            self.filter_type = None
            self.apply_filters()
        elif choice == 'c':
            pass  # Cancel
        elif choice.isdigit() and 1 <= int(choice) <= len(COMPONENT_TYPES):
            self.filter_type = list(COMPONENT_TYPES.keys())[int(choice) - 1]
            self.apply_filters()
    
    def search_components(self):
        """Search components by text."""
        search_text = input("Enter search text (empty to clear): ").strip()
        
        if search_text:
            self.filter_text = search_text
        else:
            self.filter_text = ""
        
        self.apply_filters()
    
    def view_component(self):
        """View a component by user selection."""
        component_num = input("Enter component number to view: ").strip()
        
        if not component_num.isdigit():
            print("Invalid input. Please enter a number.")
            input("Press Enter to continue...")
            return
        
        index = int(component_num) - 1
        start_index = self.current_page * self.items_per_page
        
        if 0 <= index < min(self.items_per_page, len(self.filtered_components) - start_index):
            self.view_component_by_index(start_index + index)
        else:
            print(f"Invalid component number. Valid range: 1-{min(self.items_per_page, len(self.filtered_components) - start_index)}")
            input("Press Enter to continue...")
    
    def view_component_by_index(self, index):
        """View component details by index."""
        if 0 <= index < len(self.filtered_components):
            component = self.filtered_components[index]
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=" * 80)
            print(f" COMPONENT DETAILS: {component['id']} ".center(80))
            print("=" * 80)
            
            print(f"ID:     {component['id']}")
            print(f"Name:   {component['name']}")
            print(f"Type:   {COMPONENT_TYPES.get(component['type'], {}).get('icon', '❓')} {component['type'].capitalize()}")
            print(f"Status: {component['status'].capitalize()}")
            
            if component["created"]:
                try:
                    created_date = datetime.fromisoformat(component["created"].replace("Z", "+00:00"))
                    created_str = created_date.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    created_str = component["created"]
                print(f"Created: {created_str}")
            
            print("\nFull Details:")
            print("-" * 80)
            
            # Format the JSON data
            formatted_json = json.dumps(component["data"], indent=2)
            print(formatted_json)
            
            print("\nPress Enter to return to component list...")
            input()
    
    def show_help(self):
        """Show help information."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 80)
        print(" GENESIS SHELL HELP ".center(80))
        print("=" * 80)
        
        help_text = """
Genesis Shell provides an indexed interface for navigating and managing all components
within the Genesis Stack container, with a paginated workflow.

Navigation Commands:
  n: Go to next page
  p: Go to previous page
  #: Enter a number to view the component at that position

Filter Commands:
  f: Filter by component type
  s: Search components by text

Other Commands:
  r: Reload components
  v: View component (prompts for component number)
  h: Show this help
  q: Quit Genesis Shell

Component Types:
  🔑 License: Entity license for Genesis Stack operations
  🧠 NPU: Neural Processing Unit for computational governance
  ☁️ CloudShell: Cloud Shell fragment for entity operations
  ⚙️ Synergyze: SynergyzeOS license for entity distribution
  ⚖️ Governance: Governance rules for computational alignment
  ✨ Divine: Divine Alignment Layer filters
"""
        print(help_text)
        
        print("\nPress Enter to return to component list...")
        input()

def main():
    """Main function to run the Genesis Shell Terminal."""
    parser = argparse.ArgumentParser(
        description='Genesis Shell Terminal - Indexed Component Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            The Genesis Shell provides an indexed interface for navigating and managing 
            all components within the Genesis Stack container, with paginated workflow.
            
            This terminal version is designed to work in environments where curses is not available.
        ''')
    )
    
    parser.parse_args()
    
    # Initialize directories if they don't exist
    os.makedirs("data/licenses", exist_ok=True)
    os.makedirs("data/npu_nodes", exist_ok=True)
    os.makedirs("data/governance_rules", exist_ok=True)
    os.makedirs("data/divine_filters", exist_ok=True)
    os.makedirs("data/license_assignments", exist_ok=True)
    
    # Run the terminal application
    try:
        GenesisShellTerminal().run()
    except KeyboardInterrupt:
        print("\nGenesis Shell terminated.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()