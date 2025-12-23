#!/usr/bin/env python3
"""
Publish amatak-winapp to PyPI
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"🚀 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"⚠️  {result.stderr}")
    if check and result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result.returncode

def main():
    print("📦 Publishing amatak-winapp to PyPI")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Run this from the project root.")
        sys.exit(1)
    
    # Step 1: Clean previous builds
    print("\n1. Cleaning previous builds...")
    for dir_name in ["dist", "build", "amatak_winapp.egg-info"]:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Step 2: Check if build tools are installed
    print("\n2. Checking build tools...")
    run_command(f"{sys.executable} -m pip install --upgrade build twine", check=False)
    
    # Step 3: Build the package
    print("\n3. Building package...")
    run_command(f"{sys.executable} -m build")
    
    # Step 4: Check the distribution
    print("\n4. Checking distribution...")
    dist_files = list(Path("dist").glob("*"))
    print(f"   Found {len(dist_files)} files in dist/:")
    for f in dist_files:
        print(f"   - {f.name}")
    
    # Step 5: Upload to PyPI
    print("\n5. Uploading to PyPI...")
    print("   Note: You need PyPI credentials to upload.")
    print("   Make sure you have a ~/.pypirc file or use API tokens.")
    
    response = input("\n   Upload to PyPI? (y/N): ")
    if response.lower() == 'y':
        run_command(f"{sys.executable} -m twine upload dist/*")
        print("\n✅ Successfully published to PyPI!")
        print("\n🎉 Users can now install with:")
        print("   pip install amatak-winapp")
    else:
        print("\n⏸️  Upload cancelled.")
        print("\nTo upload manually, run:")
        print("   python -m twine upload dist/*")
        print("\nTo upload to TestPyPI first:")
        print("   python -m twine upload --repository testpypi dist/*")
    
    print("\n" + "=" * 50)
    print("📦 Package ready for distribution!")
    return 0

if __name__ == "__main__":
    sys.exit(main())