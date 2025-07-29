#!/usr/bin/env python3
"""
Temperature Monitoring GUI Launcher

Simple launcher script for the Temperature Monitoring GUI application.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Temperature Monitoring GUI."""
    gui_script = Path(__file__).parent / "temperature_gui.py"
    
    if not gui_script.exists():
        print(f"Error: GUI script not found at {gui_script}")
        sys.exit(1)
    
    try:
        # Launch the GUI application
        subprocess.run([sys.executable, str(gui_script)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGUI application interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
