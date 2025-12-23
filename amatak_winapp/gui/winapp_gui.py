# gui/winapp_gui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
from pathlib import Path
import json
import os
from datetime import datetime

class WinAppGUI:
    def __init__(self, master=None):
        # Setup paths first
        self.setup_paths()
        
        if master:
            self.root = master
        else:
            self.root = tk.Tk()
            self.root.title("Amatak WinApp Generator - Dark Mode")
            self.root.geometry("1000x750")
            
            # Apply dark theme
            self.setup_dark_theme()
            
            # Set icon if available
            icon_path = self.assets_dir / "brand" / "brand.ico"
            if icon_path.exists():
                try:
                    self.root.iconbitmap(str(icon_path))
                except:
                    pass
            
            self.create_widgets()
            self.center_window()
            self.root.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_paths(self):
        """Setup paths for global/local operation"""
        # Try to get amatak root from environment
        amatak_root = os.environ.get('AMATAK_ROOT')
        
        if amatak_root and Path(amatak_root).exists():
            self.project_root = Path(amatak_root)
        else:
            # Try to find it
            possible_paths = [
                Path(__file__).parent.parent,  # gui/..
                Path.cwd(),
                Path.home() / ".amatak",
            ]
            
            for path in possible_paths:
                if (path / "bin" / "amatak" / "winapp.py").exists():
                    self.project_root = path
                    break
            else:
                self.project_root = Path.cwd()
        
        # Setup directories
        self.bin_dir = self.project_root / "bin" / "amatak"
        self.assets_dir = self.project_root / "assets"
        self.gui_dir = self.project_root / "gui"
        
        # Add to Python path
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))
    
    def setup_dark_theme(self):
        """Configure dark mode theme"""
        # Define dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.secondary_color = "#2d2d2d"
        self.widget_bg = "#252526"
        self.widget_fg = "#cccccc"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#F44336"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Create and configure style
        self.style = ttk.Style()
        
        # Try different themes
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        else:
            self.style.theme_use('default')
        
        # Configure colors for different widgets
        self.style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Segoe UI", 10)
        )
        
        self.style.configure(
            "TButton",
            background=self.widget_bg,
            foreground=self.fg_color,
            font=("Segoe UI", 10),
            borderwidth=1,
            relief="raised"
        )
        
        self.style.map(
            "TButton",
            background=[("active", self.accent_color)],
            foreground=[("active", self.fg_color)]
        )
        
        self.style.configure(
            "TFrame",
            background=self.bg_color
        )
        
        self.style.configure(
            "TNotebook",
            background=self.bg_color,
            borderwidth=0
        )
        
        self.style.configure(
            "TNotebook.Tab",
            background=self.secondary_color,
            foreground=self.widget_fg,
            padding=[10, 5]
        )
        
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.accent_color)],
            foreground=[("selected", self.fg_color)]
        )
        
        self.style.configure(
            "TLabelframe",
            background=self.bg_color,
            foreground=self.fg_color,
            relief="flat"
        )
        
        self.style.configure(
            "TLabelframe.Label",
            background=self.bg_color,
            foreground=self.accent_color,
            font=("Segoe UI", 11, "bold")
        )
        
        self.style.configure(
            "TEntry",
            fieldbackground=self.widget_bg,
            foreground=self.widget_fg,
            insertcolor=self.widget_fg,
            borderwidth=1
        )
        
        self.style.configure(
            "TScrollbar",
            background=self.secondary_color,
            troughcolor=self.bg_color,
            borderwidth=0
        )
        
        self.style.configure(
            "Treeview",
            background=self.widget_bg,
            foreground=self.widget_fg,
            fieldbackground=self.widget_bg,
            rowheight=25
        )
        
        self.style.map(
            "Treeview",
            background=[("selected", self.accent_color)],
            foreground=[("selected", self.fg_color)]
        )
        
        self.style.configure(
            "Treeview.Heading",
            background=self.secondary_color,
            foreground=self.widget_fg,
            relief="flat"
        )
        
        # Custom styles
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=self.accent_color
        )
        
        self.style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            background=self.accent_color
        )
        
        self.style.map(
            "Action.TButton",
            background=[("active", "#005a9e")]
        )
        
        self.style.configure(
            "Success.TButton",
            background=self.success_color
        )
        
        self.style.configure(
            "Warning.TButton",
            background=self.warning_color
        )
        
        self.style.configure(
            "Status.TLabel",
            font=("Segoe UI", 9),
            foreground="#888888"
        )
    
    def run_winapp_command(self, command, args=None, cwd=None):
        """Run winapp command with proper environment"""
        if args is None:
            args = []
        
        # Build command with category as argument
        cmd = [sys.executable, str(self.bin_dir / "winapp.py"), command] + args
        
        # Setup environment
        env = os.environ.copy()
        env['AMATAK_ROOT'] = str(self.project_root)
        
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{self.project_root}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = str(self.project_root)
        
        # Run command
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                env=env,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result
        except Exception as e:
            return type('Result', (), {
                'stdout': '',
                'stderr': str(e),
                'returncode': 1
            })()
    
    def create_widgets(self):
        """Create all GUI widgets with dark theme"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with icon
        title_container = ttk.Frame(header_frame)
        title_container.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(title_container, text="⚡", font=("Segoe UI", 24)
                 ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(title_container, text="Amatak WinApp Generator", 
                 style="Title.TLabel").pack(side=tk.LEFT)
        
        # Version info
        version_frame = ttk.Frame(header_frame)
        version_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Label(version_frame, text="Dark Mode",
                 foreground="#666666").pack(side=tk.RIGHT)
        ttk.Label(version_frame, text="v1.0.0",
                 foreground="#888888", font=("Segoe UI", 9)
                 ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Main content area (Notebook)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_project_tab()
        self.create_initialize_tab()
        self.create_build_tab()
        self.create_file_manager_tab()
        self.create_logs_tab()
        
        # Status bar
        self.status_bar = ttk.Frame(main_container)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_bar, text="🚀 Ready to create amazing applications!", 
                                      style='Status.TLabel')
        self.status_label.pack(fill=tk.X)
        
        # Add separator
        ttk.Separator(self.status_bar, orient=tk.HORIZONTAL
                     ).pack(fill=tk.X, pady=(0, 5))
    
    def create_project_tab(self):
        """Create project creation tab with dark theme"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 New Project")
        
        # Create a scrollable canvas
        canvas = tk.Canvas(tab, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Project name
        frame1 = ttk.LabelFrame(scrollable_frame, text="Project Details", padding=15)
        frame1.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame1, text="Project Name:", font=("Segoe UI", 10, "bold")
                 ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.project_name_var = tk.StringVar()
        name_entry = ttk.Entry(frame1, textvariable=self.project_name_var, 
                               font=("Segoe UI", 11), width=40)
        name_entry.grid(row=0, column=1, pady=(0, 10), padx=(10, 0))
        name_entry.focus_set()
        
        # Project location
        ttk.Label(frame1, text="Location:", font=("Segoe UI", 10, "bold")
                 ).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        loc_frame = ttk.Frame(frame1)
        loc_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10, padx=(10, 0))
        
        self.location_var = tk.StringVar(value=str(Path.cwd()))
        self.location_entry = ttk.Entry(loc_frame, textvariable=self.location_var,
                                        font=("Segoe UI", 10))
        self.location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(loc_frame, text="Browse", command=self.browse_location,
                  width=12).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Category selection
        category_frame = ttk.LabelFrame(scrollable_frame, text="Application Category", 
                                        padding=15)
        category_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.category_var = tk.StringVar()
        categories = [
            "Productivity & Office Suites",
            "Development & Programming Tools", 
            "Creative & Multimedia Software",
            "Communication & Collaboration",
            "Utilities & Security",
            "Specialized Business & Enterprise"
        ]
        
        # Create a grid for categories
        for i, category in enumerate(categories):
            row = i // 2
            col = (i % 2) * 2
            
            # Category frame
            cat_frame = ttk.Frame(category_frame)
            cat_frame.grid(row=row, column=col, columnspan=2, 
                          sticky=tk.W, padx=10, pady=8)
            
            # Radio button
            rb = ttk.Radiobutton(cat_frame, text=category, 
                                variable=self.category_var, value=category)
            rb.pack(anchor=tk.W)
            
            # Add description
            desc = self.get_category_description(category)
            desc_label = ttk.Label(cat_frame, text=desc, 
                                  foreground="#888888", 
                                  font=("Segoe UI", 9))
            desc_label.pack(anchor=tk.W, padx=(20, 0))
            
            # Add icon
            icons = ["📊", "💻", "🎨", "💬", "🔧", "🏢"]
            icon_label = ttk.Label(cat_frame, text=icons[i], 
                                  font=("Segoe UI", 14))
            icon_label.place(relx=1.0, rely=0.5, anchor=tk.E)
        
        # Spacer
        ttk.Frame(scrollable_frame, height=20).pack()
        
        # Create button
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        create_btn = ttk.Button(button_frame, text="🚀 Create Project", 
                               command=self.create_project,
                               style='Action.TButton', width=25)
        create_btn.pack(pady=10)
        
        # Help text
        help_label = ttk.Label(button_frame, 
                              text="Creates a new project with dark mode theme and Windows installer support",
                              foreground="#888888", font=("Segoe UI", 9))
        help_label.pack()
    
    def get_category_description(self, category):
        """Get description for each category"""
        descriptions = {
            "Productivity & Office Suites": "Office tools, document editors, planners, calendars",
            "Development & Programming Tools": "IDEs, code editors, version control, debuggers",
            "Creative & Multimedia Software": "Image/video editors, audio tools, 3D modeling",
            "Communication & Collaboration": "Chat apps, video conferencing, email clients",
            "Utilities & Security": "System tools, antivirus, backup, file management", 
            "Specialized Business & Enterprise": "ERP, CRM, accounting, inventory management"
        }
        return descriptions.get(category, "")
    
    def browse_location(self):
        """Browse for project location"""
        path = filedialog.askdirectory(title="Select Project Location")
        if path:
            self.location_var.set(path)
    
    def create_project(self):
        """Create new project - FIXED: Sends category as argument"""
        project_name = self.project_name_var.get().strip()
        location = self.location_var.get()
        category = self.category_var.get()
        
        if not project_name:
            messagebox.showerror("Error", "Please enter a project name", parent=self.root)
            return
        
        if not category:
            messagebox.showerror("Error", "Please select a category", parent=self.root)
            return
        
        # Map category to CLI argument
        # We'll modify the CLI to accept category as an argument
        # For now, we'll run the creation directly
        def run_create():
            try:
                # Import the ProjectGenerator from winapp.py
                sys.path.insert(0, str(self.bin_dir.parent.parent))
                
                # Create a modified version of ProjectGenerator that accepts category
                class DirectProjectGenerator:
                    def __init__(self, root_dir):
                        self.project_root = Path(root_dir)
                    
                    def create_structure(self, project_name, category_data, location=None):
                        """Direct project creation bypassing CLI input"""
                        from datetime import datetime
                        import json
                        
                        if location:
                            base_path = Path(location) / project_name
                        else:
                            base_path = Path.cwd() / project_name
                        
                        self.log_output(f"\n🚀 Creating project: {project_name}")
                        self.log_output(f"📍 Location: {base_path}")
                        self.log_output(f"📁 Category: {category_data.get('name', 'General')}")
                        
                        # Create directories
                        directories = [
                            "assets/brand",
                            "assets/icons",
                            "gui",
                            "src",
                            "tests",
                            "docs"
                        ]
                        
                        base_path.mkdir(parents=True, exist_ok=True)
                        
                        for directory in directories:
                            dir_path = base_path / directory
                            dir_path.mkdir(parents=True, exist_ok=True)
                            self.log_output(f"  Created: {directory}/")
                        
                        # Create main.py with dark theme
                        main_content = f'''#!/usr/bin/env python3
"""
{project_name} - {category_data.get('name', 'General')} Application
Created with Amatak WinApp Generator
"""

import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("{project_name}")
        self.geometry("800x600")
        
        # Setup dark theme
        self.setup_theme()
        self.create_widgets()
        
    def setup_theme(self):
        """Configure dark mode theme"""
        self.configure(bg="#1e1e1e")
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TButton", background="#007acc", foreground="#ffffff")
        style.configure("TFrame", background="#1e1e1e")
        
    def create_widgets(self):
        """Create UI widgets"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="{project_name}", 
                 font=("Segoe UI", 24, "bold"),
                 foreground="#007acc").pack(pady=20)
        
        ttk.Label(main_frame, text="{category_data.get('name', 'General')} Application",
                 font=("Segoe UI", 12)).pack(pady=10)
        
        ttk.Label(main_frame, 
                 text="Welcome to your new application!\\nThis app was created with Amatak WinApp Generator.",
                 justify="center").pack(pady=30)
        
        ttk.Button(main_frame, text="Get Started", width=20).pack(pady=10)
        
        ttk.Label(main_frame, text="© 2024 {project_name}",
                 foreground="#666666").pack(side=tk.BOTTOM, pady=20)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
'''
                        
                        main_file = base_path / "main.py"
                        main_file.write_text(main_content)
                        self.log_output(f"📝 Created: main.py with dark theme")
                        
                        # Create config.json
                        config = {
                            "project": {
                                "name": project_name,
                                "category": category_data.get('name', 'General'),
                                "version": "1.0.0",
                                "created": datetime.now().isoformat(),
                                "theme": "dark"
                            }
                        }
                        
                        config_file = base_path / "config.json"
                        config_file.write_text(json.dumps(config, indent=2))
                        self.log_output(f"📝 Created: config.json")
                        
                        # Create requirements.txt
                        req_file = base_path / "requirements.txt"
                        req_file.write_text("# Project dependencies\n")
                        self.log_output(f"📝 Created: requirements.txt")
                        
                        # Create README.md
                        readme_content = f"""# {project_name}

## {category_data.get('name', 'General')} Application

Created with Amatak WinApp Generator.

### Features
- Dark mode UI
- Windows installer ready
- Modern design
- Easy to customize

### Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
3. Build installer: `winapp build`

### Theme
This application uses a dark theme by default. Colors can be customized in `main.py`.
"""
                        
                        readme_file = base_path / "README.md"
                        readme_file.write_text(readme_content)
                        self.log_output(f"📝 Created: README.md")
                        
                        self.log_output(f"\n✅ Project created successfully at: {base_path}")
                        return str(base_path)
                    
                    def log_output(self, message):
                        self.root.after(0, lambda: self.update_log(message))
                    
                    def update_log(self, message):
                        self.console_text.insert(tk.END, message + "\n")
                        self.console_text.see(tk.END)
                
                # Run creation
                generator = DirectProjectGenerator(self.project_root)
                generator.root = self.root
                generator.console_text = self.console_text
                
                project_path = generator.create_structure(
                    project_name, 
                    {"name": category}, 
                    location
                )
                
                # Update GUI
                self.root.after(0, lambda: self.on_project_created(project_path, project_name))
                
            except Exception as e:
                error_msg = f"❌ Error creating project: {str(e)}"
                self.root.after(0, lambda: self.log_output(error_msg))
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    f"Failed to create project:\n{str(e)}",
                    parent=self.root
                ))
        
        # Clear logs and show progress
        self.console_text.delete(1.0, tk.END)
        self.log_output("="*60)
        self.log_output("🚀 Starting Project Creation")
        self.log_output("="*60)
        self.status_label.config(text=f"Creating project: {project_name}...")
        
        # Switch to logs tab
        self.notebook.select(4)  # Logs tab
        
        # Run in thread
        thread = threading.Thread(target=run_create, daemon=True)
        thread.start()
    
    def on_project_created(self, project_path, project_name):
        """Handle project creation success"""
        self.init_path_var.set(project_path)
        self.load_project_tree(project_path)
        
        self.status_label.config(text=f"✅ Project '{project_name}' created successfully!")
        
        # Switch to initialize tab
        self.notebook.select(1)
        
        messagebox.showinfo(
            "Success", 
            f"Project '{project_name}' created successfully!\n\nLocation: {project_path}",
            parent=self.root
        )
    
    def create_initialize_tab(self):
        """Create project initialization tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Initialize")
        
        # Project selection
        frame = ttk.LabelFrame(tab, text="Select Project", padding=15)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame, text="Project Path:", font=("Segoe UI", 10, "bold")
                 ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(frame)
        path_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        self.init_path_var = tk.StringVar()
        self.init_path_entry = ttk.Entry(path_frame, 
                                        textvariable=self.init_path_var,
                                        width=40, font=("Segoe UI", 10))
        self.init_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="Browse", command=self.browse_project,
                  width=12).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Generator scripts options
        scripts_frame = ttk.LabelFrame(tab, text="Generator Scripts", padding=15)
        scripts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.scripts_vars = {}
        scripts = [
            ("gen_brand.py", "Generate brand assets and icons", "🎨"),
            ("gen_license.py", "Generate license files", "📄"),
            ("gen_readme.py", "Generate README.md documentation", "📝"),
            ("_init_scanner.py", "Initialize project scanner", "🔍"),
            ("gen_tree.py", "Generate project tree structure", "📁"),
            ("gen_nsi.py", "Generate NSIS installer script", "⚙️"),
            ("gen_win.py", "Generate Windows build files", "🪟")
        ]
        
        for i, (script, desc, icon) in enumerate(scripts):
            var = tk.BooleanVar(value=True)
            self.scripts_vars[script] = var
            
            cb_frame = ttk.Frame(scripts_frame)
            cb_frame.grid(row=i, column=0, sticky=tk.W, pady=5)
            
            # Icon
            ttk.Label(cb_frame, text=icon, font=("Segoe UI", 12)
                     ).pack(side=tk.LEFT, padx=(0, 8))
            
            # Checkbox
            cb = ttk.Checkbutton(cb_frame, text=script, 
                                variable=var)
            cb.pack(side=tk.LEFT)
            
            # Description
            ttk.Label(scripts_frame, text=desc, 
                     foreground="#888888",
                     font=("Segoe UI", 9)).grid(row=i, column=1, 
                                               sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Button(button_frame, text="🔄 Run Selected", 
                  command=self.run_selected_scripts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⚡ Run All", 
                  command=self.run_all_scripts).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📁 Update Tree", 
                  command=self.update_tree).pack(side=tk.RIGHT, padx=5)
    
    def browse_project(self):
        """Browse for existing project"""
        path = filedialog.askdirectory(title="Select Project", parent=self.root)
        if path:
            self.init_path_var.set(path)
            self.load_project_tree(path)
    
    def run_selected_scripts(self):
        """Run selected generator scripts"""
        project_path = self.init_path_var.get()
        if not project_path or not Path(project_path).exists():
            messagebox.showerror("Error", "Please select a valid project path", parent=self.root)
            return
        
        selected_scripts = []
        for script, var in self.scripts_vars.items():
            if var.get():
                selected_scripts.append(script)
        
        if not selected_scripts:
            messagebox.showwarning("Warning", "No scripts selected", parent=self.root)
            return
        
        def run_scripts():
            self.log_output(f"\n🔄 Running scripts for: {project_path}\n")
            self.log_output("="*50 + "\n")
            
            for script in selected_scripts:
                script_path = Path(self.bin_dir) / script
                if not script_path.exists():
                    script_path = Path(project_path) / script
                
                if script_path.exists():
                    self.log_output(f"📦 Running {script}...\n")
                    
                    try:
                        # Run the script
                        cmd = [sys.executable, str(script_path)]
                        
                        proc = subprocess.run(
                            cmd,
                            cwd=project_path,
                            capture_output=True,
                            text=True,
                            encoding='utf-8'
                        )
                        
                        if proc.stdout:
                            self.log_output(proc.stdout)
                        if proc.stderr:
                            self.log_output(f"⚠️  {proc.stderr}\n")
                        
                        if proc.returncode == 0:
                            self.log_output(f"✅ {script} completed successfully\n")
                        else:
                            self.log_output(f"❌ {script} failed with code {proc.returncode}\n")
                        
                    except Exception as e:
                        self.log_output(f"❌ Error running {script}: {e}\n")
                else:
                    self.log_output(f"⚠️  Script not found: {script}\n")
            
            self.log_output("\n✅ All scripts executed!\n")
            self.root.after(0, lambda: self.status_label.config(
                text=f"Scripts executed for: {Path(project_path).name}"
            ))
        
        self.status_label.config(text="Running scripts...")
        self.log_output("="*60 + "\n")
        self.log_output("⚙️  Starting Script Execution\n")
        self.log_output("="*60 + "\n")
        
        thread = threading.Thread(target=run_scripts, daemon=True)
        thread.start()
    
    def run_all_scripts(self):
        """Run all generator scripts"""
        for var in self.scripts_vars.values():
            var.set(True)
        self.run_selected_scripts()
    
    def update_tree(self):
        """Update project tree"""
        project_path = self.init_path_var.get()
        if not project_path:
            messagebox.showerror("Error", "Please select a project path", parent=self.root)
            return
        
        # Run gen_tree.py
        tree_script = Path(self.bin_dir) / "gen_tree.py"
        if not tree_script.exists():
            tree_script = Path(project_path) / "gen_tree.py"
        
        if tree_script.exists():
            self.log_output(f"\n📁 Updating project tree...\n")
            
            try:
                proc = subprocess.run(
                    [sys.executable, str(tree_script)],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                
                self.log_output(proc.stdout)
                if proc.returncode == 0:
                    self.log_output("✅ Tree updated successfully!\n")
                    self.load_project_tree(project_path)
                else:
                    self.log_output(f"❌ Error: {proc.stderr}\n")
                    
            except Exception as e:
                self.log_output(f"❌ Exception: {e}\n")
        else:
            messagebox.showerror("Error", "gen_tree.py not found", parent=self.root)
    
    
    
    def create_build_tab(self):
        """Create build tab with dark theme"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔨 Build")
        
        # Validation section
        validate_frame = ttk.LabelFrame(tab, text="Project Validation", padding=15)
        validate_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create text widget with dark theme
        self.validation_text = tk.Text(validate_frame, 
                                      height=12,
                                      wrap=tk.WORD,
                                      bg=self.widget_bg,
                                      fg=self.widget_fg,
                                      insertbackground=self.widget_fg,
                                      font=("Consolas", 10),
                                      relief="flat")
        
        scrollbar = ttk.Scrollbar(validate_frame, command=self.validation_text.yview)
        self.validation_text.configure(yscrollcommand=scrollbar.set)
        
        self.validation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(validate_frame, text="🔍 Validate Structure", 
                  command=self.validate_structure).pack(pady=10)
        
        # Build options
        build_frame = ttk.LabelFrame(tab, text="Build Options", padding=15)
        build_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.clean_build_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(build_frame, text="Clean build directory before building", 
                       variable=self.clean_build_var).pack(anchor=tk.W, pady=5)
        
        self.generate_installer_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(build_frame, text="Generate Windows installer (NSIS)", 
                       variable=self.generate_installer_var).pack(anchor=tk.W, pady=5)
        
        self.include_debug_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(build_frame, text="Include debug symbols", 
                       variable=self.include_debug_var).pack(anchor=tk.W, pady=5)
        
        # Build button
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Button(button_frame, text="🚀 Build Project", 
                  command=self.build_project,
                  style='Action.TButton').pack(pady=10)
    
    def create_file_manager_tab(self):
        """Create file manager tab with dark theme"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📂 File Manager")
        
        # Top toolbar
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("📂 Open", self.open_file),
            ("✏️ Edit", self.edit_file),
            ("🗑️ Delete", self.delete_file),
            ("📝 Rename", self.rename_file),
        ]
        
        for text, command in buttons:
            btn = ttk.Button(toolbar, text=text, command=command, width=12)
            btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, 
                                                       padx=10, fill=tk.Y)
        
        archive_buttons = [
            ("📦 Zip", self.zip_files),
            ("📤 Unzip", self.unzip_file),
        ]
        
        for text, command in archive_buttons:
            btn = ttk.Button(toolbar, text=text, command=command, width=12)
            btn.pack(side=tk.LEFT, padx=2)
        
        # File tree and editor
        paned_window = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tree view frame
        tree_frame = ttk.Frame(paned_window)
        
        # Tree view with scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,
                                     show="tree headings")
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.file_tree.yview)
        
        # Configure tree columns
        self.file_tree['columns'] = ('Size', 'Modified', 'Type')
        self.file_tree.column('#0', width=300, minwidth=200)
        self.file_tree.column('Size', width=100, minwidth=80)
        self.file_tree.column('Modified', width=150, minwidth=100)
        self.file_tree.column('Type', width=100, minwidth=80)
        
        self.file_tree.heading('#0', text='Name')
        self.file_tree.heading('Size', text='Size')
        self.file_tree.heading('Modified', text='Modified')
        self.file_tree.heading('Type', text='Type')
        
        paned_window.add(tree_frame, weight=1)
        
        # Editor frame
        editor_frame = ttk.Frame(paned_window)
        
        # Text editor with scrollbars
        text_scroll_y = ttk.Scrollbar(editor_frame)
        text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_scroll_x = ttk.Scrollbar(editor_frame, orient=tk.HORIZONTAL)
        text_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.text_editor = tk.Text(editor_frame, 
                                  wrap=tk.NONE,
                                  bg=self.widget_bg,
                                  fg=self.widget_fg,
                                  insertbackground=self.widget_fg,
                                  font=("Consolas", 11),
                                  yscrollcommand=text_scroll_y.set,
                                  xscrollcommand=text_scroll_x.set)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        text_scroll_y.config(command=self.text_editor.yview)
        text_scroll_x.config(command=self.text_editor.xview)
        
        paned_window.add(editor_frame, weight=2)
        
        # Bind tree selection
        self.file_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.file_tree.bind('<Double-Button-1>', self.on_tree_double_click)
    
    def create_logs_tab(self):
        """Create logs/output tab with dark theme"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Output")
        
        # Console output
        self.console_text = tk.Text(tab, 
                                   height=20,
                                   wrap=tk.WORD,
                                   bg=self.widget_bg,
                                   fg=self.widget_fg,
                                   insertbackground=self.widget_fg,
                                   font=('Consolas', 10))
        
        text_scroll = ttk.Scrollbar(tab, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=text_scroll.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Control buttons
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(control_frame, text="🧹 Clear", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Save Log", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📋 Copy", 
                  command=self.copy_logs).pack(side=tk.RIGHT, padx=5)
    
    def validate_structure(self):
        """Validate project structure"""
        self.validation_text.delete(1.0, tk.END)
        
        project_path = self.init_path_var.get()
        if not project_path:
            self.validation_text.insert(tk.END, "❌ No project selected\n", "error")
            return
        
        # Check required files
        required_files = [
            "main.py",
            "config.json", 
            "README.md",
            "requirements.txt"
        ]
        
        self.validation_text.insert(tk.END, f"🔍 Validating: {project_path}\n", "info")
        self.validation_text.insert(tk.END, "="*50 + "\n")
        
        # Configure tags for colored text
        self.validation_text.tag_config("success", foreground="#4CAF50")
        self.validation_text.tag_config("error", foreground="#F44336")
        self.validation_text.tag_config("info", foreground="#2196F3")
        self.validation_text.tag_config("warning", foreground="#FF9800")
        
        all_ok = True
        for file in required_files:
            file_path = Path(project_path) / file
            if file_path.exists():
                self.validation_text.insert(tk.END, f"✅ {file}\n", "success")
            else:
                self.validation_text.insert(tk.END, f"❌ {file} (MISSING)\n", "error")
                all_ok = False
        
        # Check directories
        required_dirs = [
            "assets",
            "gui", 
            "src"
        ]
        
        self.validation_text.insert(tk.END, "\n📁 Directories:\n", "info")
        for directory in required_dirs:
            dir_path = Path(project_path) / directory
            if dir_path.exists():
                self.validation_text.insert(tk.END, f"✅ {directory}/\n", "success")
            else:
                self.validation_text.insert(tk.END, f"❌ {directory}/ (MISSING)\n", "error")
                all_ok = False
        
        if all_ok:
            self.validation_text.insert(tk.END, "\n🎉 All checks passed! Ready to build.\n", "success")
        else:
            self.validation_text.insert(tk.END, "\n⚠️  Some components are missing\n", "warning")
            self.validation_text.insert(tk.END, "Run 'Initialize' to generate missing files.\n", "info")
    
    def build_project(self):
        """Build project using CLI"""
        project_path = self.init_path_var.get()
        if not project_path:
            messagebox.showerror("Error", "Please select a project path", parent=self.root)
            return
        
        # Validate first
        if not self.validate_build_readiness(project_path):
            return
        
        def run_build():
            self.log_output(f"\n🔨 Building project: {project_path}\n")
            self.log_output("="*60 + "\n")
            
            try:
                # Use the winapp.py build command
                cmd = [sys.executable, str(self.bin_dir / "winapp.py"), "build"]
                
                proc = subprocess.run(
                    cmd,
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                self.log_output(proc.stdout)
                if proc.stderr:
                    self.log_output(f"\n⚠️  Warnings:\n{proc.stderr}\n")
                
                if proc.returncode == 0:
                    self.log_output("\n✅ Build successful!\n")
                    
                    # Check for installer
                    installer_dir = Path(project_path) / "installer"
                    if installer_dir.exists():
                        for file in installer_dir.iterdir():
                            if file.suffix in ['.exe', '.msi']:
                                self.log_output(f"📦 Installer created: {file.name}\n")
                    
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Success", 
                        "Project built successfully!",
                        parent=self.root
                    ))
                else:
                    self.log_output(f"\n❌ Build failed!\n")
                    self.root.after(0, lambda: messagebox.showerror(
                        "Error", 
                        "Build failed. Check output for details.",
                        parent=self.root
                    ))
                    
            except Exception as e:
                self.log_output(f"❌ Exception during build: {e}\n")
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    f"Build failed: {e}",
                    parent=self.root
                ))
        
        self.status_label.config(text="Building project...")
        self.log_output("="*60 + "\n")
        self.log_output("🔨 Starting Build Process\n")
        self.log_output("="*60 + "\n")
        
        thread = threading.Thread(target=run_build, daemon=True)
        thread.start()
    
    def validate_build_readiness(self, project_path):
        """Check if project is ready to build"""
        required = ["main.py", "config.json"]
        for file in required:
            if not (Path(project_path) / file).exists():
                messagebox.showerror(
                    "Not Ready", 
                    f"Cannot build: {file} is missing.\nPlease initialize the project first.",
                    parent=self.root
                )
                return False
        return True
    
    def load_project_tree(self, project_path):
        """Load project files into tree view"""
        self.file_tree.delete(*self.file_tree.get_children())
        self.current_project = project_path
        
        def add_tree_items(parent, path):
            try:
                items = sorted(Path(path).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for item in items:
                    # Skip hidden files and __pycache__
                    if item.name.startswith('.') or item.name == '__pycache__':
                        continue
                    
                    item_id = self.file_tree.insert(parent, 'end', 
                                                   text=item.name,
                                                   values=self.get_file_info(item),
                                                   tags=('dir' if item.is_dir() else 'file'))
                    
                    if item.is_dir():
                        # Add a dummy child to make it expandable
                        self.file_tree.insert(item_id, 'end', text='')
                        self.file_tree.item(item_id, open=False)
            except PermissionError:
                pass
        
        root_id = self.file_tree.insert('', 'end', 
                                       text=Path(project_path).name,
                                       values=['', '', 'Project'],
                                       tags=('project',),
                                       open=True)
        
        # Configure tags for different file types
        self.file_tree.tag_configure('project', foreground=self.accent_color, font=('Segoe UI', 10, 'bold'))
        self.file_tree.tag_configure('dir', foreground="#4FC3F7")
        self.file_tree.tag_configure('file', foreground=self.widget_fg)
        
        # Bind to load children on expand
        self.file_tree.bind('<<TreeviewOpen>>', self.on_tree_expand)
        
        add_tree_items(root_id, project_path)
    
    def on_tree_expand(self, event):
        """Load children when a directory is expanded"""
        item = self.file_tree.focus()
        if self.file_tree.get_children(item):
            # Check if it only has the dummy child
            children = self.file_tree.get_children(item)
            if len(children) == 1 and self.file_tree.item(children[0])['text'] == '':
                # Remove dummy and load real children
                self.file_tree.delete(children[0])
                path = self.get_full_path(item)
                if path:
                    self.add_tree_children(item, path)
    
    def add_tree_children(self, parent_id, path):
        """Add children to a tree item"""
        try:
            items = sorted(Path(path).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            for item in items:
                # Skip hidden files and __pycache__
                if item.name.startswith('.') or item.name == '__pycache__':
                    continue
                
                item_id = self.file_tree.insert(parent_id, 'end', 
                                               text=item.name,
                                               values=self.get_file_info(item),
                                               tags=('dir' if item.is_dir() else 'file'))
                
                if item.is_dir():
                    # Add a dummy child to make it expandable
                    self.file_tree.insert(item_id, 'end', text='')
                    self.file_tree.item(item_id, open=False)
        except PermissionError:
            pass
    
    def get_file_info(self, filepath):
        """Get file information for tree view"""
        path = Path(filepath)
        if path.is_file():
            size = path.stat().st_size
            size_str = self.format_size(size)
            modified = path.stat().st_mtime
            modified_str = datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M')
            file_type = path.suffix[1:] if path.suffix else 'File'
            return [size_str, modified_str, file_type]
        return ['', '', 'Folder']
    
    def format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            item_text = self.file_tree.item(item, 'text')
            self.status_label.config(text=f"Selected: {item_text}")
    
    def on_tree_double_click(self, event):
        """Handle tree double click to open file"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            file_path = self.get_full_path(item)
            
            if Path(file_path).is_file():
                self.open_file(file_path)
    
    def get_full_path(self, item_id):
        """Get full path from tree item"""
        path_parts = []
        while item_id:
            path_parts.insert(0, self.file_tree.item(item_id, 'text'))
            item_id = self.file_tree.parent(item_id)
        
        if self.current_project:
            # Handle case where current_project might be part of the path
            project_name = Path(self.current_project).name
            if path_parts and path_parts[0] == project_name:
                # Remove project name from parts since it's already in current_project
                path_parts.pop(0)
            
            return str(Path(self.current_project).joinpath(*path_parts))
        return str(Path.cwd().joinpath(*path_parts))
    
    def open_file(self, filepath=None):
        """Open file in editor"""
        if not filepath:
            selection = self.file_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "No file selected", parent=self.root)
                return
            filepath = self.get_full_path(selection[0])
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, content)
            
            # Switch to file manager tab
            self.notebook.select(3)  # File manager tab index
            self.status_label.config(text=f"Opened: {Path(filepath).name}")
            
            # Apply syntax highlighting based on file extension
            self.apply_syntax_highlighting(filepath)
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {e}", parent=self.root)
    
    def apply_syntax_highlighting(self, filepath):
        """Apply basic syntax highlighting based on file extension"""
        # Clear existing tags
        for tag in self.text_editor.tag_names():
            if tag not in ['sel', 'linenumber']:
                self.text_editor.tag_remove(tag, '1.0', tk.END)
        
        ext = Path(filepath).suffix.lower()
        
        # Configure tags for different file types
        if ext == '.py':
            # Python highlighting
            keywords = ['def', 'class', 'import', 'from', 'as', 'if', 'else', 
                       'elif', 'for', 'while', 'try', 'except', 'finally', 
                       'return', 'yield', 'pass', 'break', 'continue']
            
            self.text_editor.tag_config('keyword', foreground='#569CD6')
            self.text_editor.tag_config('string', foreground='#CE9178')
            self.text_editor.tag_config('comment', foreground='#6A9955')
            self.text_editor.tag_config('function', foreground='#DCDCAA')
            
            content = self.text_editor.get('1.0', tk.END)
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # Highlight comments
                if '#' in line:
                    start = line.find('#')
                    self.text_editor.tag_add('comment', 
                                           f'{i}.{start}', 
                                           f'{i}.{len(line)}')
                
                # Highlight strings
                import re
                string_pattern = r'(\".*?\")|(\'.*?\')'
                for match in re.finditer(string_pattern, line):
                    start, end = match.span()
                    self.text_editor.tag_add('string', 
                                           f'{i}.{start}', 
                                           f'{i}.{end}')
                
                # Highlight keywords
                words = line.split()
                for word in words:
                    if word in keywords:
                        start = line.find(word)
                        self.text_editor.tag_add('keyword', 
                                               f'{i}.{start}', 
                                               f'{i}.{start+len(word)}')
    
    def edit_file(self):
        """Edit selected file"""
        self.open_file()
    
    def delete_file(self):
        """Delete selected file/folder"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        filepath = self.get_full_path(item)
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete '{Path(filepath).name}'?",
                                     parent=self.root)
        if confirm:
            try:
                import shutil
                if Path(filepath).is_file():
                    Path(filepath).unlink()
                else:
                    shutil.rmtree(filepath)
                
                self.file_tree.delete(item)
                self.status_label.config(text=f"Deleted: {Path(filepath).name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete: {e}", parent=self.root)
    
    def rename_file(self):
        """Rename selected file/folder"""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        old_path = self.get_full_path(item)
        old_name = Path(old_path).name
        
        new_name = tk.simpledialog.askstring("Rename", 
                                            f"Rename '{old_name}' to:",
                                            initialvalue=old_name,
                                            parent=self.root)
        if new_name and new_name != old_name:
            try:
                new_path = Path(old_path).parent / new_name
                Path(old_path).rename(new_path)
                
                self.file_tree.item(item, text=new_name)
                self.status_label.config(text=f"Renamed to: {new_name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Cannot rename: {e}", parent=self.root)
    
    def zip_files(self):
        """Zip selected files"""
        import zipfile
        from datetime import datetime
        
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No files selected", parent=self.root)
            return
        
        files_to_zip = []
        for item in selection:
            filepath = self.get_full_path(item)
            files_to_zip.append(filepath)
        
        zip_name = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = filedialog.asksaveasfilename(
            title="Save Zip Archive",
            defaultextension=".zip",
            initialfile=zip_name,
            parent=self.root
        )
        
        if zip_path:
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in files_to_zip:
                        zipf.write(file, Path(file).name)
                
                messagebox.showinfo("Success", f"Created: {Path(zip_path).name}", parent=self.root)
                self.status_label.config(text=f"Created zip: {Path(zip_path).name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create zip: {e}", parent=self.root)
    
    def unzip_file(self):
        """Unzip selected archive"""
        import zipfile
        
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No file selected", parent=self.root)
            return
        
        zip_path = self.get_full_path(selection[0])
        if not zip_path.lower().endswith('.zip'):
            messagebox.showwarning("Warning", "Selected file is not a zip archive", parent=self.root)
            return
        
        extract_to = filedialog.askdirectory(title="Select Extraction Folder", parent=self.root)
        if extract_to:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(extract_to)
                
                messagebox.showinfo("Success", f"Extracted to: {extract_to}", parent=self.root)
                self.status_label.config(text=f"Extracted: {Path(zip_path).name}")
                
                # Reload tree if extracting to current project
                if self.current_project and extract_to == self.current_project:
                    self.load_project_tree(self.current_project)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Cannot extract: {e}", parent=self.root)
    
    def log_output(self, message):
        """Add message to console output"""
        # Configure tags for different message types
        if not hasattr(self, 'log_tags_configured'):
            self.console_text.tag_config("success", foreground="#4CAF50")
            self.console_text.tag_config("error", foreground="#F44336")
            self.console_text.tag_config("warning", foreground="#FF9800")
            self.console_text.tag_config("info", foreground="#2196F3")
            self.log_tags_configured = True
        
        # Determine message type
        tag = "info"
        if "✅" in message or "success" in message.lower():
            tag = "success"
        elif "❌" in message or "error" in message.lower():
            tag = "error"
        elif "⚠️" in message or "warning" in message.lower():
            tag = "warning"
        
        self.console_text.insert(tk.END, message, tag)
        self.console_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_logs(self):
        """Clear console output"""
        self.console_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Save console output to file"""
        content = self.console_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No logs to save", parent=self.root)
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save Log File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")],
            parent=self.root
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Log saved to: {filepath}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save log: {e}", parent=self.root)
    
    def copy_logs(self):
        """Copy console output to clipboard"""
        content = self.console_text.get(1.0, tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Copied", "Logs copied to clipboard", parent=self.root)


# Main entry point
def gui_main():
    """Launch the GUI interface"""
    try:
        app = WinAppGUI()
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    gui_main()