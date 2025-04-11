#!/usr/bin/env python3
"""
Genesis Shell Runner

This script starts the Genesis Shell indexed component interface.
"""

import os
import sys
import subprocess


def main():
    """Main function to run the Genesis Shell."""
    print("Starting Genesis Shell - Indexed Component Interface...")

    # Ensure required directories exist
    os.makedirs("data/licenses", exist_ok=True)
    os.makedirs("data/npu_nodes", exist_ok=True)
    os.makedirs("data/governance_rules", exist_ok=True)
    os.makedirs("data/divine_filters", exist_ok=True)
    os.makedirs("data/license_assignments", exist_ok=True)

    # Run the Genesis Shell
    try:
        subprocess.run(["python", "tools/genesis_shell.py"])
    except KeyboardInterrupt:
        print("\nGenesis Shell terminated.")
    except Exception as e:
        print(f"\nError running Genesis Shell: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
