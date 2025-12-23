# C:\Users\USER\OneDrive\Desktop\developer\OpenSource\pip-package\winapp\sync_version.py

#!/usr/bin/env python3
"""
Sync version between data/VERSION.txt and __init__.py
"""
import sys
from pathlib import Path

def sync_versions():
    """Sync version from data/VERSION.txt to __init__.py"""
    package_dir = Path(__file__).parent / "amatak_winapp"
    version_file = package_dir / "data" / "VERSION.txt"
    init_file = package_dir / "__init__.py"
    
    if not version_file.exists():
        print(f"❌ Version file not found: {version_file}")
        return False
    
    if not init_file.exists():
        print(f"❌ Init file not found: {init_file}")
        return False
    
    try:
        # Read version
        version = version_file.read_text(encoding='utf-8').strip()
        print(f"📦 Found version: {version}")
        
        # Read init file
        init_content = init_file.read_text(encoding='utf-8')
        
        # Update version in init file
        lines = init_content.split('\n')
        new_lines = []
        version_updated = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('__version__ = '):
                new_lines.append(f'__version__ = "{version}"')
                version_updated = True
            else:
                new_lines.append(line)
        
        # If version line wasn't found, add it after the docstring
        if not version_updated:
            # Find where to insert (after docstring)
            in_docstring = False
            for i, line in enumerate(lines):
                if line.strip().startswith('"""'):
                    in_docstring = not in_docstring
                elif not in_docstring and line.strip():
                    # Insert version here
                    lines.insert(i, f'__version__ = "{version}"')
                    break
            
            new_lines = lines
        
        # Write updated content
        init_file.write_text('\n'.join(new_lines), encoding='utf-8')
        print(f"✅ Updated {init_file} with version {version}")
        return True
        
    except Exception as e:
        print(f"❌ Error syncing versions: {e}")
        return False

if __name__ == "__main__":
    success = sync_versions()
    sys.exit(0 if success else 1)