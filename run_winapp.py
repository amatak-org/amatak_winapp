# run_winapp.py

#!/usr/bin/env python3
"""
Global runner script for Amatak WinApp
Can be called from anywhere on the system
"""

import os
import sys
from pathlib import Path

def find_amatak_root():
    """Find the amatak installation directory"""
    # Check common installation locations
    possible_locations = [
        # Current directory
        Path.cwd(),
        # User home directory
        Path.home() / ".amatak",
        Path.home() / "amatak-winapp",
        # Windows Program Files
        Path("C:/Program Files/AmatakWinApp"),
        Path("C:/Program Files (x86)/AmatakWinApp"),
        # macOS/Linux
        Path("/usr/local/lib/amatak"),
        Path("/opt/amatak"),
        # Development locations
        Path(__file__).parent,  # This script's directory
    ]
    
    for location in possible_locations:
        # Check for winapp.py in bin/amatak/
        winapp_py = location / "bin" / "amatak" / "winapp.py"
        if winapp_py.exists():
            return location
        
        # Check for winapp.py directly
        if (location / "winapp.py").exists():
            return location
    
    # If not found, use current directory
    return Path.cwd()

def setup_environment():
    """Setup Python environment for amatak"""
    amatak_root = find_amatak_root()
    
    # Add amatak root to Python path
    if str(amatak_root) not in sys.path:
        sys.path.insert(0, str(amatak_root))
    
    # Add bin directory
    bin_dir = amatak_root / "bin"
    if str(bin_dir) not in sys.path:
        sys.path.insert(0, str(bin_dir))
    
    # Set environment variable for subprocesses
    os.environ['AMATAK_ROOT'] = str(amatak_root)
    
    return amatak_root

def main():
    """Main entry point"""
    # Setup environment
    amatak_root = setup_environment()
    
    print(f"📍 Amatak root: {amatak_root}")
    
    try:
        # Try to import and run the main CLI
        from bin.amatak.winapp import main as winapp_main
        winapp_main()
    except ImportError as e:
        print(f"❌ Failed to import amatak: {e}")
        print("\nTroubleshooting steps:")
        print(f"1. Check if amatak is installed at: {amatak_root}")
        print(f"2. Check if winapp.py exists at: {amatak_root}/bin/amatak/winapp.py")
        print("3. Try running the setup script: python setup.py")
        print("4. Run from the amatak project directory")
        
        # Offer to run setup
        if input("\nRun setup now? (y/n): ").lower() == 'y':
            setup_script = amatak_root / "setup.py"
            if setup_script.exists():
                import subprocess
                subprocess.run([sys.executable, str(setup_script)])
            else:
                print("Setup script not found")

if __name__ == "__main__":
    main()