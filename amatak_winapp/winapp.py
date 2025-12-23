#!/usr/bin/env python3
import os
import sys
import json
import shutil
from pathlib import Path
import subprocess
import datetime



# Get package directory
PACKAGE_DIR = Path(__file__).parent

def get_package_root():
    """Get the root directory of the installed package"""
    return PACKAGE_DIR

class ProjectGenerator:
    """Main project generator for pip package"""
    
    def __init__(self, project_root=None):
        self.package_root = get_package_root()
        self.project_root = project_root or Path.cwd()
        self.setup_paths()
    
    def setup_paths(self):
        """Setup all necessary paths"""
        self.scripts_dir = self.package_root / "scripts"
        self.gui_dir = self.package_root / "gui"
        
        # Ensure directories exist in current project
        for dir_name in ["assets", "gui", "installer", "src", "tests"]:
            (self.project_root / dir_name).mkdir(parents=True, exist_ok=True)
    
    def run_script(self, script_name, cwd=None):
        """Run a Python script"""
        if cwd is None:
            cwd = self.project_root
        
        # Look for script in package
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            # Try in current directory
            script_path = Path(cwd) / script_name
        
        if script_path.exists():
            try:
                print(f"🔄 Running {script_name}...")
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"⚠️  {result.stderr}")
                
                return result.returncode == 0
                
            except Exception as e:
                print(f"❌ Error running {script_name}: {e}")
                return False
        else:
            print(f"⚠️  Script not found: {script_name}")
            return False
    
    def create_structure(self, project_name, category_data, location=None):
        """Create project structure - works from anywhere"""
        if location:
            base_path = Path(location) / project_name
        else:
            base_path = Path.cwd() / project_name
        
        # Use template from project root
        template_dir = self.project_root / "templates"
        
        print(f"\n🚀 Creating project: {project_name}")
        print(f"📍 Location: {base_path}")
        
        # Create project directory
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Copy template structure
        if template_dir.exists():
            self.copy_template(template_dir, base_path, category_data)
        else:
            self.create_default_structure(base_path, category_data)
        
        # Update main.py with project info
        self.update_main_file(base_path, project_name, category_data)
        
        # Generate initial files
        self.generate_initial_files(base_path)
        
        print(f"\n✅ Project created at: {base_path}")
        print(f"\nNext steps:")
        print(f"  cd {project_name}")
        print(f"  winapp init")
        print(f"  winapp build")
        
        return str(base_path)
    
    def copy_template(self, src, dst, category_data):
        """Copy template structure"""
        # Copy all files and directories
        if src.exists():
            for item in src.iterdir():
                dest_item = dst / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest_item)
        
        # Update category-specific files
        category_name = category_data.get('name', 'General')
        self.update_category_files(dst, category_name)
    
    def create_default_structure(self, base_path, category_data):
        """Create default project structure"""
        # Create basic structure
        directories = [
            "assets",
            "assets/brand",
            "assets/icons",
            "gui",
            "installer",
            "src",
            "tests"
        ]
        
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
        
        # Create basic files
        files = {
            "main.py": """#!/usr/bin/env python3
# {PROJECT_NAME} - {CATEGORY} Application

import sys

def main():
    print("Welcome to {PROJECT_NAME}!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
""",
            "requirements.txt": "# Project dependencies\n",
            "README.md": f"# {base_path.name}\n\nA {category_data.get('name', 'General')} application.\n"
        }
        
        for filename, content in files.items():
            (base_path / filename).write_text(content)
    
    def update_category_files(self, project_path, category_name):
        """Update files with category-specific content"""
        # This can be customized based on category
        category_file = project_path / "CATEGORY.txt"
        category_file.write_text(f"Category: {category_name}\n")
    
    def update_main_file(self, project_path, project_name, category_data):
        """Update main.py with project-specific info"""
        main_file = Path(project_path) / "main.py"
        
        if main_file.exists():
            content = main_file.read_text(encoding='utf-8')
            content = content.replace("{PROJECT_NAME}", project_name)
            content = content.replace("{CATEGORY}", category_data.get('name', 'General'))
            main_file.write_text(content, encoding='utf-8')
    
    def generate_initial_files(self, project_path):
        """Generate initial required files"""
        # Create requirements.txt if it doesn't exist
        req_file = Path(project_path) / "requirements.txt"
        if not req_file.exists():
            req_file.write_text("# Project dependencies\n")
        
        # Create config.json
        config_file = Path(project_path) / "config.json"
        if not config_file.exists():
            config = {
                "project_name": Path(project_path).name,
                "version": "1.0.0",
                "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
    
    def init_project(self, project_path=None):
        """Initialize project - works from anywhere"""
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        print(f"\n🔄 Initializing project at: {project_path}")
        
        # Check if this looks like a project directory
        if not (project_path / "main.py").exists():
            print(f"⚠️  Warning: {project_path} doesn't appear to be a project directory")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Initialization cancelled.")
                return
        
        # Run initialization scripts in correct order
        scripts = [
            "gen_brand.py",
            "gen_license.py", 
            "gen_readme.py",
            "gen_tree.py",
            "_init_scanner.py"
        ]
        
        for script in scripts:
            self.run_script(script, project_path)
        
        print("\n✅ Project initialization complete!")
    
    def build_project(self, project_path=None):
        """Build project - works from anywhere"""
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        print(f"\n🔨 Building project at: {project_path}")
        
        # Validate structure first
        if not self.validate_structure(project_path):
            print("❌ Build failed: Invalid project structure")
            return False
        
        # Run build scripts
        scripts = ["gen_nsi.py", "gen_win.py"]
        success = True
        
        for script in scripts:
            if not self.run_script(script, project_path):
                success = False
        
        if success:
            print("\n✅ Build successful!")
            print(f"📦 Installer generated in: {project_path}/installer/")
            return True
        else:
            print("\n❌ Build failed!")
            return False
    
    def validate_structure(self, project_path):
        """Validate project structure"""
        required = [
            "main.py",
            "requirements.txt",
            "assets/",
            "gui/",
        ]
        
        # These are nice to have but not strictly required
        recommended = [
            "README.md",
            "assets/brand/",
            "installer/"
        ]
        
        missing = []
        for item in required:
            if not (Path(project_path) / item).exists():
                missing.append(item)
        
        if missing:
            print("❌ Missing required items:")
            for item in missing:
                print(f"  - {item}")
            return False
        
        # Check recommended items
        missing_recommended = []
        for item in recommended:
            if not (Path(project_path) / item).exists():
                missing_recommended.append(item)
        
        if missing_recommended:
            print("⚠️  Missing recommended items:")
            for item in missing_recommended:
                print(f"  - {item}")
            print("You can add these with: winapp init")
        
        return True

def print_help():
    """Print help message"""
    help_text = """
Amatak WinApp Generator - Global CLI

Usage: winapp <command> [options]

Commands:
  create <name> [location]  Create new project
  init [path]              Initialize project
  build [path]             Build project/installer
  gui                      Launch GUI interface
  help                     Show this help

Examples:
  winapp create MyApp
  winapp create MyApp "C:/Projects"
  winapp init
  winapp build
  winapp gui

Notes:
  - Run without arguments in project directory
  - Specify path for operations elsewhere
  - Use 'winapp gui' for graphical interface
"""
    print(help_text)

def launch_gui():
    """Launch the GUI interface"""
    try:
        # Try to import GUI module
        gui_path = PROJECT_ROOT / "gui" / "winapp_gui.py"
        
        if gui_path.exists():
            # Use exec to run the GUI script
            with open(gui_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Create a module-like environment
            module_globals = {
                '__name__': '__main__',
                '__file__': str(gui_path),
                'PROJECT_ROOT': PROJECT_ROOT
            }
            
            # Execute the GUI code
            exec(code, module_globals)
            
        else:
            print(f"❌ GUI module not found at: {gui_path}")
            print("Please ensure the GUI files are installed")
            
    except Exception as e:
        print(f"❌ Failed to launch GUI: {e}")
        print("\nYou may need to:")
        print("1. Run the setup script: python setup.py")
        print("2. Install required dependencies")
        print("3. Run from project directory")

# Updated main function for global/local use
def main():
    """Main CLI entry point - works globally"""
    generator = ProjectGenerator()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        if len(sys.argv) < 3:
            print("❌ Please provide a project name")
            print("Usage: winapp create <ProjectName> [location]")
            return
        
        project_name = sys.argv[2]
        location = sys.argv[3] if len(sys.argv) > 3 else None
        
        # Get category
        categories = [
            "Productivity & Office Suites",
            "Development & Programming Tools",
            "Creative & Multimedia Software", 
            "Communication & Collaboration",
            "Utilities & Security",
            "Specialized Business & Enterprise"
        ]
        
        print("\n📋 Select Application Category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        try:
            choice = int(input("\nEnter choice (1-6): "))
            if 1 <= choice <= 6:
                category = categories[choice - 1]
                generator.create_structure(project_name, {"name": category}, location)
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
    
    elif command == "init":
        project_path = sys.argv[2] if len(sys.argv) > 2 else None
        generator.init_project(project_path)
    
    elif command == "build":
        project_path = sys.argv[2] if len(sys.argv) > 2 else None
        generator.build_project(project_path)
    
    elif command == "gui":
        launch_gui()
    
    elif command in ["-h", "--help", "help"]:
        print_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()

if __name__ == "__main__":
    main()