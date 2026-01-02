Copyright (c) 2026 Amatak Holdings Pty Ltd.

# winapp

This project is an automated AI utility suite. This README is auto-generated based on the project structure.

## Project Structure
```
winapp/
├── .gitignore
├── .pypirc
├── Anna
│   ├── LICENSE
│   ├── README.md
│   ├── VERSION.txt
│   ├── __init__.py
│   ├── assets
│   │   ├── brand
│   │   │   ├── brand.ico
│   │   │   ├── brand.png
│   │   │   ├── brand_installer.bmp
│   │   │   └── license_agreement.pdf
│   │   └── icons
│   ├── config.json
│   ├── gui
│   │   └── __init__.py
│   ├── installer
│   │   ├── Amatak_Anna_Setup_v1.0.0.exe
│   │   └── win_installer.nsi
│   ├── main.py
│   ├── requirements.txt
│   ├── src
│   │   └── __init__.py
│   └── tests
│       └── __init__.py
├── LICENSE
├── MANIFEST.in
├── README.md
├── VERSION.txt
├── amatak-winapp.bat
├── amatak-winapp.pyw
├── amatak_winapp
│   ├── __init__.py
│   ├── assets
│   │   └── brand
│   │       ├── brand.ico
│   │       ├── brand.png
│   │       ├── brand_installer.bmp
│   │       └── license_agreement.pdf
│   ├── data
│   │   ├── VERSION.txt
│   │   └── __init__.py
│   ├── gui
│   │   ├── __init__.py
│   │   └── winapp_gui.py
│   ├── installer
│   │   └── win_installer.nsi
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── _init_scanner.py
│   │   ├── gen_readme.py
│   │   ├── gen_win.py
│   │   └── winapp_init.py
│   ├── this_init.py
│   └── winapp.py
├── amatak_winapp.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── __init__.py
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── requires.txt
│   └── top_level.txt
├── assets
│   └── brand
│       ├── brand.ico
│       ├── brand.png
│       ├── brand_installer.bmp
│       └── license_agreement.pdf
├── buuuu
│   ├── LICENSE
│   ├── README.md
│   ├── VERSION.txt
│   ├── __init__.py
│   ├── assets
│   │   ├── brand
│   │   │   ├── brand.ico
│   │   │   ├── brand.png
│   │   │   ├── brand_installer.bmp
│   │   │   └── license_agreement.pdf
│   │   └── icons
│   ├── config.json
│   ├── gui
│   │   └── __init__.py
│   ├── installer
│   │   ├── Amatak_buuuu_Setup_v1.0.0.exe
│   │   └── win_installer.nsi
│   ├── main.py
│   ├── requirements.txt
│   ├── src
│   │   └── __init__.py
│   └── tests
│       └── __init__.py
├── cleanup_editable.py
├── dist
│   ├── __init__.py
│   ├── amatak_winapp-1.0.5-py3-none-any.whl
│   └── amatak_winapp-1.0.5.tar.gz
├── fdsfdsfdsf
│   ├── LICENSE
│   ├── README.md
│   ├── VERSION.txt
│   ├── __init__.py
│   ├── assets
│   │   ├── brand
│   │   │   ├── brand.ico
│   │   │   ├── brand.png
│   │   │   ├── brand_installer.bmp
│   │   │   └── license_agreement.pdf
│   │   └── icons
│   ├── config.json
│   ├── gui
│   │   └── __init__.py
│   ├── installer
│   │   ├── Amatak_fdsfdsfdsf_Setup_v1.0.0.exe
│   │   └── win_installer.nsi
│   ├── main.py
│   ├── requirements.txt
│   ├── src
│   │   └── __init__.py
│   └── tests
│       └── __init__.py
├── file.py
├── gen_nsi_main.py
├── gen_win_main.py
├── installer
│   ├── Amatak_WinApp_Generator_Setup_v1.0.2.exe
│   ├── Amatak_WinApp_Generator_Setup_v1.0.4.exe
│   └── win_installer.nsi
├── main.py
├── publish.py
├── requirements.txt
├── run_winapp.py
├── sample-app
│   ├── README.md
│   ├── VERSION.txt
│   ├── __init__.py
│   ├── assets
│   │   ├── brand
│   │   │   ├── brand.ico
│   │   │   ├── brand.png
│   │   │   └── brand_installer.bmp
│   │   └── icons
│   ├── config.json
│   ├── docs
│   │   └── __init__.py
│   ├── gui
│   │   └── __init__.py
│   ├── installer
│   │   └── win_installer.nsi
│   ├── main.py
│   ├── requirements.txt
│   ├── src
│   │   └── __init__.py
│   └── tests
│       └── __init__.py
├── setup.py
├── suhotest
│   ├── README.md
│   ├── VERSION.txt
│   ├── __init__.py
│   ├── assets
│   │   ├── brand
│   │   └── icons
│   ├── config.json
│   ├── gui
│   │   └── __init__.py
│   ├── installer
│   ├── main.py
│   ├── requirements.txt
│   ├── src
│   │   └── __init__.py
│   └── tests
│       └── __init__.py
├── sync_version.py
├── winapp.bat
└── youandme
    ├── LICENSE
    ├── README.md
    ├── VERSION.txt
    ├── __init__.py
    ├── assets
    │   ├── brand
    │   │   ├── brand.ico
    │   │   ├── brand.png
    │   │   ├── brand_installer.bmp
    │   │   └── license_agreement.pdf
    │   └── icons
    ├── config.json
    ├── gui
    │   └── __init__.py
    ├── installer
    │   ├── Amatak_youandme_Setup_v1.0.0.exe
    │   └── win_installer.nsi
    ├── main.py
    ├── requirements.txt
    ├── src
    │   └── __init__.py
    └── tests
        └── __init__.py
```
## Documentation & Modules
## Setup
```bash
pip install -r requirements.txt
python main.py
```
