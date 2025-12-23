# C:\Users\USER\OneDrive\Desktop\developer\OpenSource\pip-package\winapp\main.py
# Main entry point for direct execution (not via pip package)

import sys
import os
from pathlib import Path

def launch_gui():
    """Launch the GUI interface"""
    try:
        # Try to import from the installed package first
        from amatak_winapp.gui.winapp_gui import gui_main
        gui_main()
    except ImportError:
        try:
            # Fallback to local import for development
            import sys
            project_root = Path(__file__).parent
            sys.path.insert(0, str(project_root))
            from amatak_winapp.gui.winapp_gui import gui_main
            gui_main()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("Make sure you have:")
            print("1. Installed the package: pip install -e .")
            print("2. tkinter installed (usually comes with Python)")
            print("\nFalling back to CLI...")
            launch_cli()

def launch_cli():
    """Launch CLI interface"""
    try:
        # Try to import from the installed package first
        from amatak_winapp.winapp import main as cli_main
        cli_main()
    except ImportError:
        try:
            # Fallback to local import for development
            import sys
            project_root = Path(__file__).parent
            sys.path.insert(0, str(project_root))
            from amatak_winapp.winapp import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"❌ Cannot launch CLI: {e}")
            print("\nPlease install the package first:")
            print("pip install -e .")
            print("\nOr run directly with:")
            print("python -m amatak_winapp.winapp")

def show_help():
    """Show help message"""
    help_text = """
Amatak WinApp - Windows Application Generator

Usage:
  python main.py [gui|cli|--help]

Options:
  gui       Launch graphical interface (default)
  cli       Launch command-line interface
  --help    Show this help message

Examples:
  python main.py          # Launch GUI
  python main.py gui      # Launch GUI
  python main.py cli      # Launch CLI
  python main.py --help   # Show help

Note: After installing via pip, use:
  winapp [command]       # Use the CLI command
  winapp gui             # Launch GUI via CLI
"""
    print(help_text)

def main():
    """Main entry point for direct execution"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ["--help", "-h", "help"]:
            show_help()
        elif command == "cli":
            launch_cli()
        elif command == "gui":
            launch_gui()
        else:
            print(f"❌ Unknown command: {command}")
            show_help()
    else:
        # Default to GUI
        launch_gui()

if __name__ == "__main__":
    main()