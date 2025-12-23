#!/usr/bin/env python3
"""
Amatak WinApp - Main CLI
Windows Application Generator and Installer Creator
"""
import os
import sys
import json
import shutil
from pathlib import Path
import subprocess
import datetime
import importlib.util

# Get package directory
PACKAGE_DIR = Path(__file__).parent
PROJECT_ROOT = PACKAGE_DIR

class ProjectGenerator:
    """Main project generator for pip package"""
    
    def __init__(self, project_root=None):
        self.package_root = PROJECT_ROOT
        self.project_root = project_root or Path.cwd()
        self.setup_paths()
    
    def setup_paths(self):
        """Setup all necessary paths"""
        self.scripts_dir = self.package_root / "scripts"
        self.gui_dir = self.package_root / "gui"
        self.assets_dir = self.package_root / "assets"
        
        # Ensure scripts directory exists
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Print debug info
        if os.getenv('DEBUG'):
            print(f"📁 Package root: {self.package_root}")
            print(f"📁 Scripts dir: {self.scripts_dir}")
            print(f"📁 Project root: {self.project_root}")
    
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
                print(f"   Path: {script_path}")
                
                # Add package directory to Python path for the script
                env = os.environ.copy()
                python_path = env.get('PYTHONPATH', '')
                if str(self.package_root) not in python_path:
                    env['PYTHONPATH'] = f"{self.package_root}{os.pathsep}{python_path}"
                
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=str(cwd),
                    env=env,
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
                import traceback
                traceback.print_exc()
                return False
        else:
            print(f"⚠️  Script not found: {script_name}")
            print(f"   Searched in: {self.scripts_dir} and {cwd}")
            return False
    
    def run_winapp_init(self, project_path):
        """Run the winapp_init.py script with proper context"""
        init_script = self.scripts_dir / "winapp_init.py"
        
        if init_script.exists():
            print(f"🚀 Running winapp initialization...")
            print(f"   Script: {init_script}")
            
            try:
                # Import the module directly
                sys.path.insert(0, str(self.package_root))
                
                # Import and run the init script
                spec = importlib.util.spec_from_file_location("winapp_init", str(init_script))
                init_module = importlib.util.module_from_spec(spec)
                
                # Set up the module's namespace
                init_module.__dict__.update({
                    '__name__': '__main__',
                    '__file__': str(init_script),
                    'PROJECT_ROOT': str(project_path),
                    'PACKAGE_ROOT': str(self.package_root)
                })
                
                # Execute the module
                spec.loader.exec_module(init_module)
                
                # Check if it has a main function
                if hasattr(init_module, 'main'):
                    print("📝 Running winapp_init.main()...")
                    return init_module.main()
                else:
                    print("⚠️  winapp_init.py has no main() function")
                    return False
                    
            except Exception as e:
                print(f"❌ Error running winapp_init: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print(f"❌ winapp_init.py not found in: {self.scripts_dir}")
            return False
    
    def create_structure(self, project_name, category_data, location=None):
        """Create project structure"""
        if location:
            base_path = Path(location) / project_name
        else:
            base_path = Path.cwd() / project_name
        
        print(f"\n🚀 Creating project: {project_name}")
        print(f"📍 Location: {base_path}")
        
        # Create project directory
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Check if we have templates, otherwise create default
        if (self.package_root / "templates").exists():
            self.copy_template(self.package_root / "templates", base_path, category_data)
        else:
            self.create_default_structure(base_path, category_data)
        
        # Update main.py with project info
        self.update_main_file(base_path, project_name, category_data)
        
        # Generate initial files
        self.generate_initial_files(base_path)
        
        print(f"\n✅ Project created at: {base_path}")
        print(f"\n📋 Next steps:")
        print(f"  cd {project_name}")
        print(f"  winapp init      # Initialize with branding and docs")
        print(f"  winapp build     # Build the installer")
        
        return str(base_path)
    
    def copy_template(self, src, dst, category_data):
        """Copy template structure"""
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
            "main.py": f"""#!/usr/bin/env python3
# {base_path.name} - {category_data.get('name', 'General')} Application

import sys

def main():
    print("Welcome to {base_path.name}!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
""",
            "requirements.txt": "# Project dependencies\n",
            "README.md": f"# {base_path.name}\n\nA {category_data.get('name', 'General')} application.\n"
        }
        
        for filename, content in files.items():
            (base_path / filename).write_text(content, encoding='utf-8')
    
    def update_category_files(self, project_path, category_name):
        """Update files with category-specific content"""
        category_file = project_path / "CATEGORY.txt"
        category_file.write_text(f"Category: {category_name}\n", encoding='utf-8')
    
    def update_main_file(self, project_path, project_name, category_data):
        """Update main.py with project-specific info"""
        main_file = Path(project_path) / "main.py"
        
        if main_file.exists():
            try:
                content = main_file.read_text(encoding='utf-8')
                content = content.replace("{PROJECT_NAME}", project_name)
                content = content.replace("{CATEGORY}", category_data.get('name', 'General'))
                main_file.write_text(content, encoding='utf-8')
            except Exception as e:
                print(f"⚠️  Could not update main.py: {e}")
    
    def generate_initial_files(self, project_path):
        """Generate initial required files"""
        # Create requirements.txt if it doesn't exist
        req_file = Path(project_path) / "requirements.txt"
        if not req_file.exists():
            req_file.write_text("# Project dependencies\n", encoding='utf-8')
        
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
        """Initialize project - call winapp_init.py"""
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        print(f"\n🚀 Initializing project at: {project_path}")
        print("=" * 50)
        
        # Check if this looks like a project directory
        if not (project_path / "main.py").exists():
            print(f"⚠️  Warning: {project_path} doesn't appear to be a project directory")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Initialization cancelled.")
                return False
        
        print(f"📁 Project directory: {project_path}")
        print(f"📦 Package directory: {self.package_root}")
        
        # Run winapp_init.py script
        success = self.run_winapp_init(project_path)
        
        if success:
            print("\n" + "=" * 50)
            print("✅ Project initialization complete!")
            print("\n📋 Next steps:")
            print(f"  winapp build     # Build the installer")
            return True
        else:
            print("\n❌ Project initialization failed!")
            return False
    
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
        scripts = ["gen_win.py"]  # Only gen_win.py exists in your scripts
        success = True
        
        for script in scripts:
            if not self.run_script(script, project_path):
                success = False
        
        if success:
            print("\n✅ Build successful!")
            print(f"📦 Installer files in: {project_path}/installer/")
            return True
        else:
            print("\n❌ Build failed!")
            return False
    
    def validate_structure(self, project_path):
        """Validate project structure"""
        required = [
            "main.py",
            "requirements.txt",
        ]
        
        # These are nice to have but not strictly required
        recommended = [
            "assets/",
            "gui/",
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
Amatak WinApp Generator v1.0.0
──────────────────────────────

Usage: winapp <command> [options]

Commands:
  create <name> [location]  Create new Windows application project
  init [path]              Initialize project (branding, docs, etc.)
  build [path]             Build project installer
  gui                      Launch graphical interface
  help                     Show this help message

Examples:
  winapp create MyApp
  winapp create MyApp "C:/Projects"
  winapp init
  winapp build
  winapp gui

Debug mode: Set DEBUG=1 environment variable for detailed output
"""
    print(help_text)

def launch_gui():
    """Launch the GUI interface"""
    try:
        gui_path = PROJECT_ROOT / "gui" / "winapp_gui.py"
        
        if gui_path.exists():
            # Read and execute the GUI code
            with open(gui_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Create execution environment
            exec_globals = {
                '__name__': '__main__',
                '__file__': str(gui_path),
                'PROJECT_ROOT': PROJECT_ROOT,
                'ProjectGenerator': ProjectGenerator
            }
            
            exec(code, exec_globals)
        else:
            print(f"❌ GUI not found: {gui_path}")
            print("Make sure the GUI files are installed.")
            
    except Exception as e:
        print(f"❌ Failed to launch GUI: {e}")

def main():
    """Main CLI entry point"""
    # Enable debug mode
    if os.getenv('DEBUG'):
        print("🔍 DEBUG MODE ENABLED")
        print(f"Python executable: {sys.executable}")
        print(f"Python path: {sys.path}")
    
    if len(sys.argv) < 2:
        print_help()
        return 0
    
    command = sys.argv[1].lower()
    generator = ProjectGenerator()
    
    if command == "create":
        if len(sys.argv) < 3:
            print("❌ Please provide a project name")
            print("Usage: winapp create <ProjectName> [location]")
            return 1
        
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
            print(f"  {i}. {cat}")
        
        try:
            choice = input("\nEnter choice (1-6) or press Enter for General: ").strip()
            if choice and choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    category = categories[choice_num - 1]
                else:
                    category = "General"
            else:
                category = "General"
            
            generator.create_structure(project_name, {"name": category}, location)
            
        except (ValueError, KeyboardInterrupt) as e:
            print(f"\n⚠️  Using default category: General ({e})")
            generator.create_structure(project_name, {"name": "General"}, location)
    
    elif command == "init":
        project_path = sys.argv[2] if len(sys.argv) > 2 else None
        success = generator.init_project(project_path)
        return 0 if success else 1
    
    elif command == "build":
        project_path = sys.argv[2] if len(sys.argv) > 2 else None
        success = generator.build_project(project_path)
        return 0 if success else 1
    
    elif command == "gui":
        launch_gui()
    
    elif command in ["-h", "--help", "help"]:
        print_help()
    
    else:
        print(f"❌ Unknown command: {command}")
        print_help()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())