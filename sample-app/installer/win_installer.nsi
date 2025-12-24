; ============================================
; Amatak WinApp Generator Installer (2025)
; Company: Amatak Holdings Pty Ltd
; ============================================
!include "MUI2.nsh"

Name "Amatak WinApp Generator v1.0.2"
OutFile "Amatak_WinApp_Generator_Setup_v1.0.2.exe"
InstallDir "$PROGRAMFILES\Amatak Holdings Pty Ltd\Amatak WinApp Generator"
InstallDirRegKey HKLM "Software\AmatakWinApp" "Install_Dir"
RequestExecutionLevel admin
ShowInstDetails show
BrandingText "Amatak Holdings Pty Ltd © 2025"

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
    CreateDirectory "$INSTDIR\assets\brand"
    SetOutPath "$INSTDIR"
    File "..\README.md"
    File "..\VERSION.txt"
    File "..\__init__.py"
    SetOutPath "$INSTDIR\assets\brand"
    File "..\assets\brand\brand.ico"
    File "..\assets\brand\brand.png"
    File "..\assets\brand\brand_installer.bmp"
    SetOutPath "$INSTDIR"
    File "..\config.json"
    File "..\main.py"
    File "..\requirements.txt"

    ; Install VERSION.txt if it exists
    SetOutPath "$INSTDIR"
    File "..\VERSION.txt"
    
    ; Create batch launcher
    FileOpen $0 "$INSTDIR\winapp.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "echo ========================================$\r$\n"
    FileWrite $0 "echo   Amatak WinApp Generator v1.0.2$\r$\n"
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
    
    ; Create Python GUI launcher script
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
    
    ; Write installation info
    WriteRegStr HKLM "Software\AmatakWinApp" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\AmatakWinApp" "Version" "1.0.2"
    
    ; Write uninstall info
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "DisplayName" "Amatak WinApp Generator"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "DisplayIcon" "$INSTDIR\assets\brand\brand.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "DisplayVersion" "1.0.2"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "Publisher" "Amatak Holdings Pty Ltd"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp" "URLInfoAbout" "https://github.com/amatak-org/amatak-winapp"
    
SectionEnd

Section "Shortcuts" SEC02
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    ; Create shortcut to VBS launcher (hidden console)
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp Generator.lnk" "$INSTDIR\launch.vbs" "" "$INSTDIR\assets\brand\brand.ico" 0
    ; Create shortcut to visible console
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp (Console).lnk" "$INSTDIR\run-visible.bat" "" "$INSTDIR\assets\brand\brand.ico" 0
    ; Create shortcut to Python GUI launcher
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Amatak WinApp GUI.lnk" "$INSTDIR\launch_gui.pyw" "" "$INSTDIR\assets\brand\brand.ico" 0
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
    DeleteRegKey HKLM "Software\AmatakWinApp"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AmatakWinApp"
    
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
    StrCpy $StartMenuFolder "AmatakWinApp"
FunctionEnd
