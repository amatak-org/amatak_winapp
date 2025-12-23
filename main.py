# main.py - Updated to launch GUI

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def launch_gui():
    """Launch the GUI interface"""
    try:
        from gui.winapp_gui import WinAppGUI
        app = WinAppGUI()
    except ImportError as e:
        print(f"GUI not available: {e}")
        print("Make sure you have tkinter installed and gui.winapp_gui exists")
        print("Falling back to CLI...")
        launch_cli()

def launch_cli():
    """Launch CLI interface"""
    try:
        from bin.amatak.winapp import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"Cannot launch CLI: {e}")
        print("Please check your installation.")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        launch_cli()
    else:
        launch_gui()

if __name__ == "__main__":
    main()