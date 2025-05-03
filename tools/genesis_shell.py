#!/usr/bin/env python3
"""
Genesis Shell - Indexed Component Interface

This script provides an indexed shell interface for navigating and managing
all components (license types) within the Genesis Stack container.
It offers a paginated workflow for efficient license management across the system.
"""

import os
import sys
import json
import argparse
import curses
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

class GenesisShell:
    """Genesis Shell - Interactive command-line interface for Genesis Stack."""
    
    def __init__(self, screen):
        """Initialize the shell."""
        self.screen = screen
        self.current_page = 0
        self.items_per_page = 10
        self.selected_index = 0
        self.filter_text = ""
        self.filter_type = None
        self.components = []
        self.filtered_components = []
        self.command_history = []
        self.command_index = 0
        self.input_text = ""
        self.cursor_pos = 0
        self.status_message = ""
        self.status_timeout = 0
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected item
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Error
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Warning
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Info
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default
        
        # Initialize component data structure
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
        
        # Reset selection if needed
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(self.filtered_components))
        page_items = end_index - start_index
        
        if page_items > 0 and self.selected_index >= page_items:
            self.selected_index = page_items - 1
    
    def run(self):
        """Run the shell interface."""
        curses.curs_set(0)  # Hide cursor
        self.screen.timeout(100)  # Set non-blocking input with 100ms timeout
        
        while True:
            try:
                # Clear screen
                self.screen.clear()
                
                # Get screen dimensions
                max_y, max_x = self.screen.getmaxyx()
                
                # Draw UI
                self.draw_header(max_x)
                self.draw_component_list(max_y - 7, max_x)
                self.draw_status_bar(max_y - 4, max_x)
                self.draw_command_line(max_y - 3, max_x)
                self.draw_help_line(max_y - 1, max_x)
                
                # Refresh the screen
                self.screen.refresh()
                
                # Handle input
                ch = self.screen.getch()
                if ch == ord('q'):
                    break
                elif ch == curses.KEY_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif ch == curses.KEY_DOWN:
                    start_index = self.current_page * self.items_per_page
                    end_index = min(start_index + self.items_per_page, len(self.filtered_components))
                    page_items = end_index - start_index
                    self.selected_index = min(page_items - 1, self.selected_index + 1)
                elif ch == curses.KEY_LEFT:
                    self.current_page = max(0, self.current_page - 1)
                    self.selected_index = 0
                elif ch == curses.KEY_RIGHT:
                    total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
                    if total_pages > 0:
                        self.current_page = min(total_pages - 1, self.current_page + 1)
                        self.selected_index = 0
                elif ch == ord('/'):
                    # Show search prompt
                    self.input_text = "/"
                    self.cursor_pos = 1
                    curses.curs_set(1)  # Show cursor
                    self.handle_search_input()
                    curses.curs_set(0)  # Hide cursor
                elif ch == ord(':'):
                    # Show command prompt
                    self.input_text = ":"
                    self.cursor_pos = 1
                    curses.curs_set(1)  # Show cursor
                    self.handle_command_input()
                    curses.curs_set(0)  # Hide cursor
                elif ch == ord('r'):
                    # Reload components
                    self.load_components()
                    self.set_status("Components reloaded.", curses.color_pair(3))
                elif ch == ord('v'):
                    # View selected component
                    self.view_selected_component()
                elif ch == ord('f'):
                    # Toggle filter menu
                    self.show_filter_menu()
                elif ch == 10:  # Enter key
                    # View or edit selected component
                    self.view_selected_component()
                
            except KeyboardInterrupt:
                break
    
    def draw_header(self, max_x):
        """Draw the header."""
        self.screen.attron(curses.color_pair(1))
        self.screen.addstr(0, 0, " " * max_x)
        title = "GENESIS SHELL - Indexed Component Interface"
        self.screen.addstr(0, (max_x - len(title)) // 2, title)
        
        # Draw filter information
        filter_info = f"Filter: "
        if self.filter_type:
            filter_info += f"Type={self.filter_type} "
        if self.filter_text:
            filter_info += f"Text={self.filter_text} "
        if not self.filter_type and not self.filter_text:
            filter_info += "None"
        
        self.screen.addstr(0, max_x - len(filter_info) - 1, filter_info)
        self.screen.attroff(curses.color_pair(1))
    
    def draw_component_list(self, max_y, max_x):
        """Draw the component list."""
        self.screen.attron(curses.color_pair(7))
        self.screen.addstr(2, 0, "ID".ljust(20) + "Name".ljust(40) + "Type".ljust(15) + "Status".ljust(10) + "Created")
        self.screen.attroff(curses.color_pair(7))
        
        # Draw list header separator
        self.screen.addstr(3, 0, "─" * max_x)
        
        # Calculate pagination
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(self.filtered_components))
        
        # Draw items
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
                except ValueError:
                    created_str = component["created"]
            
            # Highlight selected item
            if index == self.selected_index:
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(4 + index, 0, f"{id_str}{name_str}{type_str}{status_str}{created_str}")
                self.screen.attroff(curses.color_pair(2))
            else:
                self.screen.addstr(4 + index, 0, f"{id_str}{name_str}{type_str}{status_str}{created_str}")
        
        # Draw pagination info
        total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
        if total_pages > 0:
            pagination_info = f"Page {self.current_page + 1}/{total_pages} - {len(self.filtered_components)} items"
        else:
            pagination_info = "No items"
        
        self.screen.addstr(4 + self.items_per_page + 1, 0, pagination_info)
    
    def draw_status_bar(self, y, max_x):
        """Draw the status bar."""
        if self.status_message:
            if self.status_timeout > 0:
                self.status_timeout -= 1
                self.screen.addstr(y, 0, self.status_message)
            else:
                self.status_message = ""
    
    def draw_command_line(self, y, max_x):
        """Draw the command line."""
        self.screen.addstr(y, 0, "> " + self.input_text)
        if self.input_text:
            # Draw cursor if input is active
            cursor_y, cursor_x = self.screen.getyx()
            self.screen.move(y, 2 + self.cursor_pos)
    
    def draw_help_line(self, y, max_x):
        """Draw the help line."""
        help_text = "q:Quit  r:Reload  v:View  f:Filter  /:Search  :Command  ←→:Pages  ↑↓:Select"
        self.screen.attron(curses.color_pair(6))
        self.screen.addstr(y, 0, help_text)
        self.screen.attroff(curses.color_pair(6))
    
    def set_status(self, message, color_pair=None):
        """Set a status message with color."""
        if color_pair is None:
            color_pair = curses.color_pair(7)
        self.screen.attron(color_pair)
        self.status_message = message
        self.status_timeout = 50  # About 5 seconds
        self.screen.attroff(color_pair)
    
    def handle_search_input(self):
        """Handle search input."""
        while True:
            # Get screen dimensions
            max_y, max_x = self.screen.getmaxyx()
            
            # Draw command line
            self.screen.move(max_y - 3, 0)
            self.screen.clrtoeol()
            self.screen.addstr(max_y - 3, 0, "> " + self.input_text)
            self.screen.move(max_y - 3, 2 + self.cursor_pos)
            
            # Refresh the screen
            self.screen.refresh()
            
            # Get input
            ch = self.screen.getch()
            
            if ch == 27:  # Escape
                self.input_text = ""
                break
            elif ch == 10:  # Enter
                if len(self.input_text) > 1:
                    self.filter_text = self.input_text[1:]  # Remove the '/' prefix
                    self.apply_filters()
                    self.set_status(f"Filter applied: '{self.filter_text}'", curses.color_pair(6))
                else:
                    self.filter_text = ""  # Clear filter
                    self.apply_filters()
                    self.set_status("Filter cleared.", curses.color_pair(6))
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if self.cursor_pos > 1:
                    self.input_text = self.input_text[:self.cursor_pos-1] + self.input_text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif ch == curses.KEY_LEFT:
                if self.cursor_pos > 1:
                    self.cursor_pos -= 1
            elif ch == curses.KEY_RIGHT:
                if self.cursor_pos < len(self.input_text):
                    self.cursor_pos += 1
            elif 32 <= ch <= 126:  # Printable ASCII
                self.input_text = self.input_text[:self.cursor_pos] + chr(ch) + self.input_text[self.cursor_pos:]
                self.cursor_pos += 1
    
    def handle_command_input(self):
        """Handle command input."""
        while True:
            # Get screen dimensions
            max_y, max_x = self.screen.getmaxyx()
            
            # Draw command line
            self.screen.move(max_y - 3, 0)
            self.screen.clrtoeol()
            self.screen.addstr(max_y - 3, 0, "> " + self.input_text)
            self.screen.move(max_y - 3, 2 + self.cursor_pos)
            
            # Refresh the screen
            self.screen.refresh()
            
            # Get input
            ch = self.screen.getch()
            
            if ch == 27:  # Escape
                self.input_text = ""
                break
            elif ch == 10:  # Enter
                if len(self.input_text) > 1:
                    command = self.input_text[1:]  # Remove the ':' prefix
                    self.execute_command(command)
                break
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                if self.cursor_pos > 1:
                    self.input_text = self.input_text[:self.cursor_pos-1] + self.input_text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif ch == curses.KEY_LEFT:
                if self.cursor_pos > 1:
                    self.cursor_pos -= 1
            elif ch == curses.KEY_RIGHT:
                if self.cursor_pos < len(self.input_text):
                    self.cursor_pos += 1
            elif 32 <= ch <= 126:  # Printable ASCII
                self.input_text = self.input_text[:self.cursor_pos] + chr(ch) + self.input_text[self.cursor_pos:]
                self.cursor_pos += 1
    
    def execute_command(self, command):
        """Execute a command."""
        command = command.strip()
        parts = command.split()
        
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == "filter" or cmd == "f":
            if len(args) > 0:
                filter_type = args[0].lower()
                if filter_type in COMPONENT_TYPES or filter_type == "clear":
                    if filter_type == "clear":
                        self.filter_type = None
                        self.filter_text = ""
                        self.set_status("Filters cleared.", curses.color_pair(6))
                    else:
                        self.filter_type = filter_type
                        self.set_status(f"Filter set to type: {filter_type}", curses.color_pair(6))
                    self.apply_filters()
                else:
                    self.set_status(f"Unknown component type: {filter_type}", curses.color_pair(4))
            else:
                self.set_status("Usage: filter <type|clear>", curses.color_pair(5))
        
        elif cmd == "search" or cmd == "s":
            if len(args) > 0:
                search_text = args[0]
                self.filter_text = search_text
                self.apply_filters()
                self.set_status(f"Search filter applied: '{search_text}'", curses.color_pair(6))
            else:
                self.filter_text = ""
                self.apply_filters()
                self.set_status("Search filter cleared.", curses.color_pair(6))
        
        elif cmd == "reload" or cmd == "r":
            self.load_components()
            self.set_status("Components reloaded.", curses.color_pair(3))
        
        elif cmd == "view" or cmd == "v":
            self.view_selected_component()
        
        elif cmd == "page" or cmd == "p":
            if len(args) > 0:
                try:
                    page = int(args[0]) - 1
                    total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
                    if 0 <= page < total_pages:
                        self.current_page = page
                        self.selected_index = 0
                        self.set_status(f"Navigated to page {page + 1}", curses.color_pair(6))
                    else:
                        self.set_status(f"Invalid page number. Valid range: 1-{total_pages}", curses.color_pair(4))
                except ValueError:
                    self.set_status("Invalid page number.", curses.color_pair(4))
            else:
                total_pages = (len(self.filtered_components) + self.items_per_page - 1) // self.items_per_page
                self.set_status(f"Current page: {self.current_page + 1}/{total_pages}", curses.color_pair(6))
        
        elif cmd == "help" or cmd == "h":
            self.show_help()
        
        else:
            self.set_status(f"Unknown command: {cmd}", curses.color_pair(4))
    
    def view_selected_component(self):
        """View the selected component details."""
        if not self.filtered_components:
            self.set_status("No components to view.", curses.color_pair(5))
            return
        
        start_index = self.current_page * self.items_per_page
        selected_component = self.filtered_components[start_index + self.selected_index]
        
        # Create a temporary file to view
        temp_file = f"data/temp_{selected_component['id']}.json"
        with open(temp_file, 'w') as f:
            json.dump(selected_component["data"], f, indent=2)
        
        # Save current terminal state
        curses.endwin()
        
        # Use less to view the file
        os.system(f"less -R {temp_file}")
        
        # Remove temporary file
        try:
            os.remove(temp_file)
        except:
            pass
        
        # Restore terminal state
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.keypad(True)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
    
    def show_filter_menu(self):
        """Show the filter menu."""
        # Get screen dimensions
        max_y, max_x = self.screen.getmaxyx()
        
        # Create a small window for the filter menu
        menu_height = len(COMPONENT_TYPES) + 4
        menu_width = 30
        menu_y = (max_y - menu_height) // 2
        menu_x = (max_x - menu_width) // 2
        
        # Create the menu window
        menu_win = curses.newwin(menu_height, menu_width, menu_y, menu_x)
        menu_win.box()
        menu_win.attron(curses.color_pair(1))
        menu_win.addstr(0, (menu_width - 12) // 2, " Filter Menu ")
        menu_win.attroff(curses.color_pair(1))
        
        # Add menu items
        menu_win.addstr(1, 2, "0. Clear filter")
        for i, (comp_type, info) in enumerate(COMPONENT_TYPES.items(), 1):
            menu_win.addstr(i + 1, 2, f"{i}. {info['icon']} {comp_type.capitalize()}")
        
        menu_win.addstr(menu_height - 2, 2, "ESC: Cancel")
        menu_win.refresh()
        
        # Handle menu input
        while True:
            ch = self.screen.getch()
            
            if ch == 27:  # Escape
                break
            elif ch == ord('0'):
                self.filter_type = None
                self.apply_filters()
                self.set_status("Type filter cleared.", curses.color_pair(6))
                break
            elif ord('1') <= ch <= ord('6'):
                index = ch - ord('1')
                if index < len(COMPONENT_TYPES):
                    self.filter_type = list(COMPONENT_TYPES.keys())[index]
                    self.apply_filters()
                    self.set_status(f"Filter set to type: {self.filter_type}", curses.color_pair(6))
                    break
    
    def show_help(self):
        """Show the help screen."""
        # Get screen dimensions
        max_y, max_x = self.screen.getmaxyx()
        
        # Create a window for the help screen
        help_height = 15
        help_width = 60
        help_y = (max_y - help_height) // 2
        help_x = (max_x - help_width) // 2
        
        # Create the help window
        help_win = curses.newwin(help_height, help_width, help_y, help_x)
        help_win.box()
        help_win.attron(curses.color_pair(1))
        help_win.addstr(0, (help_width - 16) // 2, " Genesis Shell Help ")
        help_win.attroff(curses.color_pair(1))
        
        # Add help content
        help_text = [
            "Navigation:",
            "  ↑/↓: Navigate items",
            "  ←/→: Change pages",
            "  Enter: View selected component",
            "",
            "Commands:",
            "  /text: Search components",
            "  :filter <type>: Filter by component type",
            "  :filter clear: Clear type filter",
            "  :search <text>: Search by text",
            "  :page <num>: Go to specific page",
            "  :reload: Reload components",
            "",
            "Press any key to close this help"
        ]
        
        for i, line in enumerate(help_text, 1):
            help_win.addstr(i, 2, line)
        
        help_win.refresh()
        
        # Wait for any key
        self.screen.getch()

def main():
    """Main function to run the Genesis Shell."""
    parser = argparse.ArgumentParser(
        description='Genesis Shell - Indexed Component Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            The Genesis Shell provides an indexed interface for navigating and managing 
            all components within the Genesis Stack container, with paginated workflow.
            
            Component types:
              🔑 License: Entity license for Genesis Stack operations
              🧠 NPU: Neural Processing Unit for computational governance
              ☁️ CloudShell: Cloud Shell fragment for entity operations
              ⚙️ Synergyze: SynergyzeOS license for entity distribution
              ⚖️ Governance: Governance rules for computational alignment
              ✨ Divine: Divine Alignment Layer filters
            
            For more information, use the in-app help by typing :help after launch.
        ''')
    )
    
    args = parser.parse_args()
    
    # Initialize directories if they don't exist
    os.makedirs("data/licenses", exist_ok=True)
    os.makedirs("data/npu_nodes", exist_ok=True)
    os.makedirs("data/governance_rules", exist_ok=True)
    os.makedirs("data/divine_filters", exist_ok=True)
    os.makedirs("data/license_assignments", exist_ok=True)
    
    # Run the curses application
    curses.wrapper(lambda screen: GenesisShell(screen).run())

if __name__ == "__main__":
    main()