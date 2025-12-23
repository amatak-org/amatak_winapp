Copyright (c) 2025 Amatak Holdings Pty Ltd.

# Amatak WinApp

A comprehensive Python toolkit for creating professional Windows application installers.

## Installation

```bash
pip install amatak-winapp
# Create a new Windows application project
winapp create MyApp

# Navigate to project
cd MyApp

# Initialize with branding and documentation
winapp init

# Build the installer
winapp build
```

## Project Tree
```
winapp/
├── .pypirc
├── LICENSE
├── MANIFEST.in
├── README.md
├── VERSION.txt
├── _init_scanner.py
├── amatak-winapp.bat
├── amatak-winapp.pyw
├── amatak_winapp
│   ├── __init__.py
│   ├── _init_scanner.py
│   ├── data
│   │   ├── VERSION.txt
│   │   └── __init__.py
│   ├── gui
│   │   ├── __init__.py
│   │   └── winapp_gui.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── _init_scanner.py
│   │   ├── gen_readme.py
│   │   └── gen_win.py
│   └── winapp.py
├── amatak_winapp.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── __init__.py
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   └── top_level.txt
├── assets
│   └── brand
│       ├── brand.ico
│       ├── brand.png
│       └── brand_installer.bmp
├── bin
│   ├── __init__.py
│   └── amatak
│       └── __init__.py
├── dist
│   ├── __init__.py
│   ├── amatak_winapp-1.0.1-py3-none-any.whl
│   └── amatak_winapp-1.0.1.tar.gz
├── installer
│   └── win_installer.nsi
├── main.py
├── publish.py
├── pyproject.toml
├── requirements.txt
├── run_winapp.py
├── setup.py
└── winapp.bat
```

