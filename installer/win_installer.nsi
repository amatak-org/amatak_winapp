; ============================================
; Amatak WinApp Generator Installer (2026)
; Company: Amatak Holdings Pty Ltd
; ============================================
!include "MUI2.nsh"

Name "Amatak WinApp Generator v1.0.4"
OutFile "Amatak_WinApp_Generator_Setup_v1.0.4.exe"
InstallDir "$PROGRAMFILES\Amatak Holdings Pty Ltd\Amatak WinApp Generator"
InstallDirRegKey HKLM "Software\AmatakWinAppGenerator" "Install_Dir"
RequestExecutionLevel admin
ShowInstDetails show
BrandingText "Amatak Holdings Pty Ltd © 2026"

!define MUI_ICON "..\assets\brand\brand.ico"
!define MUI_UNICON "..\assets\brand\brand.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "..\assets\brand\brand_installer.bmp"

Var StartMenuFolder

; --- PAGES ---
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

; =========== MAIN SECTION ===========
Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    ; Create directories and install files
    CreateDirectory "$INSTDIR\Anna"
    CreateDirectory "$INSTDIR\Anna\assets\brand"
    CreateDirectory "$INSTDIR\Anna\gui"
    CreateDirectory "$INSTDIR\Anna\src"
    CreateDirectory "$INSTDIR\Anna\tests"
    CreateDirectory "$INSTDIR\amatak_winapp.egg-info"
    CreateDirectory "$INSTDIR\amatak_winapp"
    CreateDirectory "$INSTDIR\amatak_winapp\assets\brand"
    CreateDirectory "$INSTDIR\amatak_winapp\data"
    CreateDirectory "$INSTDIR\amatak_winapp\gui"
    CreateDirectory "$INSTDIR\amatak_winapp\scripts"
    CreateDirectory "$INSTDIR\assets\brand"
    CreateDirectory "$INSTDIR\buuuu"
    CreateDirectory "$INSTDIR\buuuu\assets\brand"
    CreateDirectory "$INSTDIR\buuuu\gui"
    CreateDirectory "$INSTDIR\buuuu\src"
    CreateDirectory "$INSTDIR\buuuu\tests"
    CreateDirectory "$INSTDIR\fdsfdsfdsf"
    CreateDirectory "$INSTDIR\fdsfdsfdsf\assets\brand"
    CreateDirectory "$INSTDIR\fdsfdsfdsf\gui"
    CreateDirectory "$INSTDIR\fdsfdsfdsf\src"
    CreateDirectory "$INSTDIR\fdsfdsfdsf\tests"
    CreateDirectory "$INSTDIR\sample-app"
    CreateDirectory "$INSTDIR\sample-app\assets\brand"
    CreateDirectory "$INSTDIR\sample-app\docs"
    CreateDirectory "$INSTDIR\sample-app\gui"
    CreateDirectory "$INSTDIR\sample-app\src"
    CreateDirectory "$INSTDIR\sample-app\tests"
    CreateDirectory "$INSTDIR\suhotest"
    CreateDirectory "$INSTDIR\suhotest\gui"
    CreateDirectory "$INSTDIR\suhotest\src"
    CreateDirectory "$INSTDIR\suhotest\tests"
    CreateDirectory "$INSTDIR\youandme"
    CreateDirectory "$INSTDIR\youandme\assets\brand"
    CreateDirectory "$INSTDIR\youandme\gui"
    CreateDirectory "$INSTDIR\youandme\src"
    CreateDirectory "$INSTDIR\youandme\tests"
    SetOutPath "$INSTDIR"
    File "..\.pypirc"
    SetOutPath "$INSTDIR\Anna"
    File "..\Anna\LICENSE"
    File "..\Anna\README.md"
    File "..\Anna\VERSION.txt"
    File "..\Anna\__init__.py"
    SetOutPath "$INSTDIR\Anna\assets\brand"
    File "..\Anna\assets\brand\brand.ico"
    File "..\Anna\assets\brand\brand.png"
    File "..\Anna\assets\brand\brand_installer.bmp"
    File "..\Anna\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\Anna"
    File "..\Anna\config.json"
    SetOutPath "$INSTDIR\Anna\gui"
    File "..\Anna\gui\__init__.py"
    SetOutPath "$INSTDIR\Anna"
    File "..\Anna\main.py"
    File "..\Anna\requirements.txt"
    SetOutPath "$INSTDIR\Anna\src"
    File "..\Anna\src\__init__.py"
    SetOutPath "$INSTDIR\Anna\tests"
    File "..\Anna\tests\__init__.py"
    SetOutPath "$INSTDIR"
    File "..\LICENSE"
    File "..\MANIFEST.in"
    File "..\README.md"
    File "..\VERSION.txt"
    File "..\amatak-winapp.bat"
    File "..\amatak-winapp.pyw"
    SetOutPath "$INSTDIR\amatak_winapp.egg-info"
    File "..\amatak_winapp.egg-info\PKG-INFO"
    File "..\amatak_winapp.egg-info\SOURCES.txt"
    File "..\amatak_winapp.egg-info\__init__.py"
    File "..\amatak_winapp.egg-info\dependency_links.txt"
    File "..\amatak_winapp.egg-info\entry_points.txt"
    File "..\amatak_winapp.egg-info\requires.txt"
    File "..\amatak_winapp.egg-info\top_level.txt"
    SetOutPath "$INSTDIR\amatak_winapp"
    File "..\amatak_winapp\__init__.py"
    SetOutPath "$INSTDIR\amatak_winapp\assets\brand"
    File "..\amatak_winapp\assets\brand\brand.ico"
    File "..\amatak_winapp\assets\brand\brand.png"
    File "..\amatak_winapp\assets\brand\brand_installer.bmp"
    File "..\amatak_winapp\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\amatak_winapp\data"
    File "..\amatak_winapp\data\VERSION.txt"
    File "..\amatak_winapp\data\__init__.py"
    SetOutPath "$INSTDIR\amatak_winapp\gui"
    File "..\amatak_winapp\gui\__init__.py"
    File "..\amatak_winapp\gui\winapp_gui.py"
    SetOutPath "$INSTDIR\amatak_winapp\scripts"
    File "..\amatak_winapp\scripts\__init__.py"
    File "..\amatak_winapp\scripts\gen_brand.py"
    File "..\amatak_winapp\scripts\gen_license.py"
    File "..\amatak_winapp\scripts\gen_license_agreement.py"
    File "..\amatak_winapp\scripts\gen_tree.py"
    File "..\amatak_winapp\scripts\winapp_init.py"
    SetOutPath "$INSTDIR\amatak_winapp"
    File "..\amatak_winapp\this_init.py"
    File "..\amatak_winapp\winapp.py"
    SetOutPath "$INSTDIR\assets\brand"
    File "..\assets\brand\brand.ico"
    File "..\assets\brand\brand.png"
    File "..\assets\brand\brand_installer.bmp"
    File "..\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\buuuu"
    File "..\buuuu\LICENSE"
    File "..\buuuu\README.md"
    File "..\buuuu\VERSION.txt"
    File "..\buuuu\__init__.py"
    SetOutPath "$INSTDIR\buuuu\assets\brand"
    File "..\buuuu\assets\brand\brand.ico"
    File "..\buuuu\assets\brand\brand.png"
    File "..\buuuu\assets\brand\brand_installer.bmp"
    File "..\buuuu\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\buuuu"
    File "..\buuuu\config.json"
    SetOutPath "$INSTDIR\buuuu\gui"
    File "..\buuuu\gui\__init__.py"
    SetOutPath "$INSTDIR\buuuu"
    File "..\buuuu\main.py"
    File "..\buuuu\requirements.txt"
    SetOutPath "$INSTDIR\buuuu\src"
    File "..\buuuu\src\__init__.py"
    SetOutPath "$INSTDIR\buuuu\tests"
    File "..\buuuu\tests\__init__.py"
    SetOutPath "$INSTDIR"
    File "..\cleanup_editable.py"
    SetOutPath "$INSTDIR\fdsfdsfdsf"
    File "..\fdsfdsfdsf\LICENSE"
    File "..\fdsfdsfdsf\README.md"
    File "..\fdsfdsfdsf\VERSION.txt"
    File "..\fdsfdsfdsf\__init__.py"
    SetOutPath "$INSTDIR\fdsfdsfdsf\assets\brand"
    File "..\fdsfdsfdsf\assets\brand\brand.ico"
    File "..\fdsfdsfdsf\assets\brand\brand.png"
    File "..\fdsfdsfdsf\assets\brand\brand_installer.bmp"
    File "..\fdsfdsfdsf\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\fdsfdsfdsf"
    File "..\fdsfdsfdsf\config.json"
    SetOutPath "$INSTDIR\fdsfdsfdsf\gui"
    File "..\fdsfdsfdsf\gui\__init__.py"
    SetOutPath "$INSTDIR\fdsfdsfdsf"
    File "..\fdsfdsfdsf\main.py"
    File "..\fdsfdsfdsf\requirements.txt"
    SetOutPath "$INSTDIR\fdsfdsfdsf\src"
    File "..\fdsfdsfdsf\src\__init__.py"
    SetOutPath "$INSTDIR\fdsfdsfdsf\tests"
    File "..\fdsfdsfdsf\tests\__init__.py"
    SetOutPath "$INSTDIR"
    File "..\file.py"
    File "..\gen_brand.py"
    File "..\gen_nsi_main.py"
    File "..\gen_tree.py"
    File "..\gen_win_main.py"
    File "..\main.py"
    File "..\publish.py"
    File "..\requirements.txt"
    File "..\run_winapp.py"
    SetOutPath "$INSTDIR\sample-app"
    File "..\sample-app\README.md"
    File "..\sample-app\VERSION.txt"
    File "..\sample-app\__init__.py"
    SetOutPath "$INSTDIR\sample-app\assets\brand"
    File "..\sample-app\assets\brand\brand.ico"
    File "..\sample-app\assets\brand\brand.png"
    File "..\sample-app\assets\brand\brand_installer.bmp"
    SetOutPath "$INSTDIR\sample-app"
    File "..\sample-app\config.json"
    SetOutPath "$INSTDIR\sample-app\docs"
    File "..\sample-app\docs\__init__.py"
    SetOutPath "$INSTDIR\sample-app\gui"
    File "..\sample-app\gui\__init__.py"
    SetOutPath "$INSTDIR\sample-app"
    File "..\sample-app\main.py"
    File "..\sample-app\requirements.txt"
    SetOutPath "$INSTDIR\sample-app\src"
    File "..\sample-app\src\__init__.py"
    SetOutPath "$INSTDIR\sample-app\tests"
    File "..\sample-app\tests\__init__.py"
    SetOutPath "$INSTDIR"
    File "..\setup.py"
    SetOutPath "$INSTDIR\suhotest"
    File "..\suhotest\README.md"
    File "..\suhotest\VERSION.txt"
    File "..\suhotest\__init__.py"
    File "..\suhotest\config.json"
    SetOutPath "$INSTDIR\suhotest\gui"
    File "..\suhotest\gui\__init__.py"
    SetOutPath "$INSTDIR\suhotest"
    File "..\suhotest\main.py"
    File "..\suhotest\requirements.txt"
    SetOutPath "$INSTDIR\suhotest\src"
    File "..\suhotest\src\__init__.py"
    SetOutPath "$INSTDIR\suhotest\tests"
    File "..\suhotest\tests\__init__.py"
    SetOutPath "$INSTDIR"
    File "..\sync_version.py"
    File "..\use"
    File "..\winapp.bat"
    SetOutPath "$INSTDIR\youandme"
    File "..\youandme\LICENSE"
    File "..\youandme\README.md"
    File "..\youandme\VERSION.txt"
    File "..\youandme\__init__.py"
    SetOutPath "$INSTDIR\youandme\assets\brand"
    File "..\youandme\assets\brand\brand.ico"
    File "..\youandme\assets\brand\brand.png"
    File "..\youandme\assets\brand\brand_installer.bmp"
    File "..\youandme\assets\brand\license_agreement.pdf"
    SetOutPath "$INSTDIR\youandme"
    File "..\youandme\config.json"
    SetOutPath "$INSTDIR\youandme\gui"
    File "..\youandme\gui\__init__.py"
    SetOutPath "$INSTDIR\youandme"
    File "..\youandme\main.py"
    File "..\youandme\requirements.txt"
    SetOutPath "$INSTDIR\youandme\src"
    File "..\youandme\src\__init__.py"
    SetOutPath "$INSTDIR\youandme\tests"
    File "..\youandme\tests\__init__.py"

    ; Install VERSION.txt if it exists
    SetOutPath "$INSTDIR"
    File "..\VERSION.txt"
    
    ; Create batch launcher for builder
    FileOpen $0 "$INSTDIR\winapp.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "echo ========================================$\r$\n"
    FileWrite $0 "echo   Amatak WinApp Generator v1.0.4$\r$\n"
    FileWrite $0 "echo ========================================$\r$\n"
    FileWrite $0 "echo.$\r$\n"
    FileWrite $0 'cd /d "%~dp0"$\r$\n'
    FileWrite $0 "echo.$\r$\n"
    FileWrite $0 "echo Looking for Python...$\r$\n"
    FileWrite $0 "set FOUND=0$\r$\n"
    FileWrite $0 "py --version >nul 2>&1$\r$\n"
    FileWrite $0 "if not errorlevel 1 ($\r$\n"
    FileWrite $0 "  echo Found: Using py launcher$\r$\n"
    FileWrite $0 "  py -m amatak_winapp.winapp %*$\r$\n"
    FileWrite $0 "  set FOUND=1$\r$\n"
    FileWrite $0 "  goto :end$\r$\n"
    FileWrite $0 ")$\r$\n"
    FileWrite $0 "python --version >nul 2>&1$\r$\n"
    FileWrite $0 "if not errorlevel 1 ($\r$\n"
    FileWrite $0 "  echo Found: Using python command$\r$\n"
    FileWrite $0 "  python -m amatak_winapp.winapp %*$\r$\n"
    FileWrite $0 "  set FOUND=1$\r$\n"
    FileWrite $0 "  goto :end$\r$\n"
    FileWrite $0 ")$\r$\n"
    FileWrite $0 "python3 --version >nul 2>&1$\r$\n"
    FileWrite $0 "if not errorlevel 1 ($\r$\n"
    FileWrite $0 "  echo Found: Using python3 command$\r$\n"
    FileWrite $0 "  python3 -m amatak_winapp.winapp %*$\r$\n"
    FileWrite $0 "  set FOUND=1$\r$\n"
    FileWrite $0 "  goto :end$\r$\n"
    FileWrite $0 ")$\r$\n"
    FileWrite $0 "echo.$\r$\n"
    FileWrite $0 "echo ERROR: Python not found!$\r$\n"
    FileWrite $0 "echo Please install Python 3.7+ from https://www.python.org/downloads/$\r$\n"
    FileWrite $0 "echo.$\r$\n"
    FileWrite $0 "pause$\r$\n"
    FileWrite $0 ":end$\r$\n"
    FileWrite $0 "if %FOUND%==1 ($\r$\n"
    FileWrite $0 "  if errorlevel 1 ($\r$\n"
    FileWrite $0 "    echo.$\r$\n"
    FileWrite $0 "    echo Command failed with error code %ERRORLEVEL%$\r$\n"
    FileWrite $0 "    pause$\r$\n"
    FileWrite $0 "  )$\r$\n"
    FileWrite $0 ")$\r$\n"
    FileClose $0
    
    ; Create GUI launcher for builder
    FileOpen $0 "$INSTDIR\launch_gui.pyw" w
    FileWrite $0 'import sys$\r$\n'
    FileWrite $0 'import os$\r$\n'
    FileWrite $0 'sys.path.insert(0, os.path.dirname(__file__))$\r$\n'
    FileWrite $0 'try:$\r$\n'
    FileWrite $0 '    from amatak_winapp.gui.winapp_gui import gui_main$\r$\n'
    FileWrite $0 '    gui_main()$\r$\n'
    FileWrite $0 'except Exception as e:$\r$\n'
    FileWrite $0 '    import tkinter as tk$\r$\n'
    FileWrite $0 '    from tkinter import messagebox$\r$\n'
    FileWrite $0 '    tk.Tk().withdraw()$\r$\n'
    FileWrite $0 '    messagebox.showerror("Error", f"Failed to start: {e}")$\r$\n'
    FileWrite $0 '    sys.exit(1)$\r$\n'
    FileClose $0

    ; Create VBS wrapper - SIMPLIFIED AND CORRECT
    FileOpen $0 "$INSTDIR\launch.vbs" w
    FileWrite $0 'Set WshShell = CreateObject("WScript.Shell")$\r$\n'
    FileWrite $0 'Set fso = CreateObject("Scripting.FileSystemObject")$\r$\n'
    FileWrite $0 'scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)$\r$\n'
    FileWrite $0 'batFile = scriptDir & "\\winapp.bat"$\r$\n'
    FileWrite $0 'WshShell.Run Chr(34) & batFile & Chr(34), 0, False$\r$\n'
    FileWrite $0 'Set WshShell = Nothing$\r$\n'
    FileWrite $0 'Set fso = Nothing$\r$\n'
    FileClose $0
    
    ; Also create a direct shortcut batch file (visible console)
    FileOpen $0 "$INSTDIR\run-visible.bat" w
    FileWrite $0 '@echo off$\r$\n'
    FileWrite $0 'cd /d "%~dp0"$\r$\n'
    FileWrite $0 'call winapp.bat$\r$\n'
    FileWrite $0 'if errorlevel 1 pause$\r$\n'
    FileClose $0
    
    ; Write installation info
    WriteRegStr HKLM "Software\AmatakWinAppGenerator" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\AmatakWinAppGenerator" "Version" "1.0.4"
    
    ; Write uninstall info
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "DisplayName" "Amatak WinApp Generator"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "DisplayIcon" "$INSTDIR\assets\brand\brand.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "DisplayVersion" "1.0.4"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "Publisher" "Amatak Holdings Pty Ltd"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator" "URLInfoAbout" "https://github.com/amatak-org/amatak-winapp"
    
SectionEnd

Section "Shortcuts" SEC02
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    ; Create shortcut to VBS launcher (hidden console)
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp Generator.lnk" "$INSTDIR\launch.vbs" "" "$INSTDIR\assets\brand\brand.ico" 0
    ; Create shortcut to visible console
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp Generator (Console).lnk" "$INSTDIR\run-visible.bat" "" "$INSTDIR\assets\brand\brand.ico" 0
    ; Create shortcut to Python GUI launcher
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp Generator GUI.lnk" "$INSTDIR\launch_gui.pyw" "" "$INSTDIR\assets\brand\brand.ico" 0
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    CreateShortcut "$DESKTOP\Amatak WinApp Generator.lnk" "$INSTDIR\launch.vbs" "" "$INSTDIR\assets\brand\brand.ico" 0
    !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -Post
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove shortcuts
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    Delete "$SMPROGRAMS\$StartMenuFolder\*.*"
    RMDir "$SMPROGRAMS\$StartMenuFolder"
    Delete "$DESKTOP\Amatak WinApp Generator.lnk"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\AmatakWinAppGenerator"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinAppGenerator"
    
    ; Remove files
    Delete "$INSTDIR\winapp.bat"
    Delete "$INSTDIR\launch.vbs"
    Delete "$INSTDIR\run-visible.bat"
    Delete "$INSTDIR\launch_gui.pyw"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Remove all other files
    RMDir /r "$INSTDIR"
SectionEnd

Function .onInit
    StrCpy $StartMenuFolder "AmatakWinAppGenerator"
FunctionEnd
