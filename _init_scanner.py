import os
from datetime import datetime

# Configuration
EXCLUDE_DIRS = {".venv", ".git", "__pycache__", ".idea", ".vscode", "installer", "assets"}
CURRENT_YEAR = datetime.now().year
VERSION_FILE = "VERSION.txt"
OWNER = "Amatak Holdings Pty Ltd"

def get_version():
    """Reads version from VERSION.txt or returns default."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "1.0.0"

def generate_inits():
    """Scans subdirectories and ensures they are valid Python packages with versioning."""
    project_root = os.getcwd()
    current_version = get_version()
    
    # Updated Header with Version
    copyright_header = (
        f'"""\n'
        f'Auto-generated package initialization.\n'
        f'Copyright (c) {CURRENT_YEAR} {OWNER}.\n'
        f'"""\n\n'
    )

    for root, dirs, files in os.walk(project_root):
        # Filter excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Skip project root
        if root == project_root:
            continue

        init_path = os.path.join(root, "__init__.py")
        
        # Find all .py modules (excluding __init__ and scripts)
        py_modules = sorted([
            f[:-3] for f in files 
            if f.endswith(".py") and f not in ["__init__.py", "_init_scanner.py"]
        ])

        # Generate the content components
        version_line = f'__version__ = "{current_version}"\n'
        import_lines = [f"from . import {module}" for module in py_modules]
        
        # Add modules + version variable to __all__
        export_list = py_modules + ["__version__"]
        all_line = f"__all__ = {export_list}"
        
        # Assemble file content
        full_content = copyright_header
        full_content += version_line
        full_content += "\n".join(import_lines) + "\n\n"
        full_content += all_line + "\n"

        # Write the file
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        
        rel_folder = os.path.relpath(root, project_root)
        print(f"[{CURRENT_YEAR}] Initialized: {rel_folder}/__init__.py (v{current_version})")

if __name__ == "__main__":
    generate_inits()