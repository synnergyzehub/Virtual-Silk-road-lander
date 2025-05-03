#!/usr/bin/env python3
"""
Genesis Shell Terminal Runner

This script starts the Genesis Shell Terminal interface, which is a simplified
terminal-based version of the indexed component interface that doesn't require curses.
"""

import os
import sys
import subprocess

def main():
    """Main function to run the Genesis Shell Terminal."""
    print("Starting Genesis Shell Terminal - Indexed Component Interface...")
    
    # Ensure required directories exist
    os.makedirs("data/licenses", exist_ok=True)
    os.makedirs("data/npu_nodes", exist_ok=True)
    os.makedirs("data/governance_rules", exist_ok=True)
    os.makedirs("data/divine_filters", exist_ok=True)
    os.makedirs("data/license_assignments", exist_ok=True)
    
    # Make the terminal shell script executable
    try:
        os.chmod("tools/genesis_shell_terminal.py", 0o755)
    except Exception as e:
        print(f"Warning: Could not make genesis_shell_terminal.py executable: {e}")
    
    # Run the Genesis Shell Terminal
    try:
        if os.path.exists("tools/genesis_shell_terminal.py"):
            subprocess.run(["python", "tools/genesis_shell_terminal.py"])
        else:
            print("Error: Could not find tools/genesis_shell_terminal.py")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nGenesis Shell Terminal terminated.")
    except Exception as e:
        print(f"\nError running Genesis Shell Terminal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()