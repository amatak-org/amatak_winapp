# gen_nsi.py - Fixed version with correct NSIS syntax
import os
import sys
from datetime import datetime
from pathlib import Path

# Get the script's directory (winapp/)
PROJECT_ROOT = Path(__file__).resolve().parent

# Configuration - all paths relative to PROJECT_ROOT
VERSION_FILE = PROJECT_ROOT / "VERSION.txt"
NSIS_OUTPUT_PATH = PROJECT_ROOT / "installer" / "win_installer.nsi"

# Exclude patterns
EXCLUDE_DIRS = {".venv", ".git", "__pycache__", ".idea", ".vscode", "installer"}
EXCLUDE_FILES = {"gen_nsi.py", "gen_readme.py", "gen_win.py", "_init_scanner.py", ".gitignore", "tree.txt"}

def get_version():
    """Read version from VERSION.txt"""
    try:
        if VERSION_FILE.exists():
            return VERSION_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    return "1.0.1"

def scan_project_files():
    """Scan project files and return list of relative paths"""
    files_to_install = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            # Skip excluded files
            if file in EXCLUDE_FILES or file.endswith(".pyc"):
                continue
                
            # Get relative path from project root
            file_path = Path(root) / file
            rel_path = file_path.relative_to(PROJECT_ROOT)
            
            files_to_install.append(str(rel_path))
    
    return sorted(files_to_install)

def generate_nsi():
    """Generate NSIS installer script - SIMPLIFIED VERSION"""
    version = get_version()
    year = datetime.now().year
    
    # Get list of files to install
    files_list = scan_project_files()
    
    # Get relative paths for NSIS (relative to installer/ folder)
    icon_relative = "..\\assets\\brand\\brand.ico"
    header_relative = "..\\assets\\brand\\brand_installer.bmp"
    
    # SIMPLIFIED NSIS TEMPLATE
    nsi_content = f"""; ============================================
; Amatak WinApp Generator Installer ({year})
; Company: Amatak Holdings Pty Ltd
; ============================================
!include "MUI2.nsh"

Name "Amatak WinApp Generator v{version}"
OutFile "Amatak_WinApp_Generator_Setup_v{version}.exe"
InstallDir "$PROGRAMFILES\\Amatak Holdings Pty Ltd\\Amatak WinApp Generator"
InstallDirRegKey HKLM "Software\\AmatakWinApp" "Install_Dir"
RequestExecutionLevel admin
ShowInstDetails show
BrandingText "Amatak Holdings Pty Ltd © {year}"

!define MUI_ICON "{icon_relative}"
!define MUI_UNICON "{icon_relative}"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "{header_relative}"

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
"""

    # Add file installation commands
    processed_dirs = set()
    current_dir = None
    
    for file_path in files_list:
        win_path = file_path.replace('/', '\\')
        
        # Create directory if needed
        if '\\' in win_path:
            dir_path = '\\'.join(win_path.split('\\')[:-1])
            if dir_path and dir_path not in processed_dirs:
                nsi_content += f'    CreateDirectory "$INSTDIR\\{dir_path}"\n'
                processed_dirs.add(dir_path)
    
    # Install files
    for file_path in files_list:
        win_path = file_path.replace('/', '\\')
        
        # Set output directory
        if '\\' in win_path:
            dir_path = '\\'.join(win_path.split('\\')[:-1])
            if dir_path != current_dir:
                nsi_content += f'    SetOutPath "$INSTDIR\\{dir_path}"\n'
                current_dir = dir_path
        else:
            if current_dir != "":
                nsi_content += f'    SetOutPath "$INSTDIR"\n'
                current_dir = ""
        
        # Install file
        nsi_relative = "..\\" + win_path
        nsi_content += f'    File "{nsi_relative}"\n'
    
    # Continue with the rest of the script - FIXED VBS SCRIPT
    nsi_content += f"""
    ; Install VERSION.txt
    SetOutPath "$INSTDIR"
    File "..\\VERSION.txt"
    
    ; Create batch launcher
    FileOpen $0 "$INSTDIR\\winapp.bat" w
    FileWrite $0 "@echo off$\\r$\\n"
    FileWrite $0 "echo ========================================$\\r$\\n"
    FileWrite $0 "echo   Amatak WinApp Generator$\\r$\\n"
    FileWrite $0 "echo ========================================$\\r$\\n"
    FileWrite $0 "echo.$\\r$\\n"
    FileWrite $0 'cd /d "%~dp0"$\\r$\\n'
    FileWrite $0 "echo Running from: %CD%$\\r$\\n"
    FileWrite $0 "echo.$\\r$\\n"
    FileWrite $0 "echo Looking for Python...$\\r$\\n"
    FileWrite $0 "set FOUND=0$\\r$\\n"
    FileWrite $0 "py --version >nul 2>&1$\\r$\\n"
    FileWrite $0 "if not errorlevel 1 ($\\r$\\n"
    FileWrite $0 "  echo Found: Using py launcher$\\r$\\n"
    FileWrite $0 "  py main.py %*$\\r$\\n"
    FileWrite $0 "  set FOUND=1$\\r$\\n"
    FileWrite $0 "  goto :end$\\r$\\n"
    FileWrite $0 ")$\\r$\\n"
    FileWrite $0 "python --version >nul 2>&1$\\r$\\n"
    FileWrite $0 "if not errorlevel 1 ($\\r$\\n"
    FileWrite $0 "  echo Found: Using python command$\\r$\\n"
    FileWrite $0 "  python main.py %*$\\r$\\n"
    FileWrite $0 "  set FOUND=1$\\r$\\n"
    FileWrite $0 "  goto :end$\\r$\\n"
    FileWrite $0 ")$\\r$\\n"
    FileWrite $0 "python3 --version >nul 2>&1$\\r$\\n"
    FileWrite $0 "if not errorlevel 1 ($\\r$\\n"
    FileWrite $0 "  echo Found: Using python3 command$\\r$\\n"
    FileWrite $0 "  python3 main.py %*$\\r$\\n"
    FileWrite $0 "  set FOUND=1$\\r$\\n"
    FileWrite $0 "  goto :end$\\r$\\n"
    FileWrite $0 ")$\\r$\\n"
    FileWrite $0 "echo ERROR: Python not found!$\\r$\\n"
    FileWrite $0 "echo.$\\r$\\n"
    FileWrite $0 "echo Please install Python 3.9+ from https://www.python.org/downloads/$\\r$\\n"
    FileWrite $0 "pause$\\r$\\n"
    FileWrite $0 ":end$\\r$\\n"
    FileWrite $0 "if %FOUND%==1 ( if errorlevel 1 pause )$\\r$\\n"
    FileClose $0
    
    ; Create VBS wrapper - SIMPLIFIED AND CORRECT
    FileOpen $0 "$INSTDIR\\launch.vbs" w
    FileWrite $0 'Set WshShell = CreateObject("WScript.Shell")$\\r$\\n'
    FileWrite $0 'Set fso = CreateObject("Scripting.FileSystemObject")$\\r$\\n'
    FileWrite $0 'scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)$\\r$\\n'
    FileWrite $0 'batFile = scriptDir & "\\\\winapp.bat"$\\r$\\n'
    FileWrite $0 'WshShell.Run Chr(34) & batFile & Chr(34), 0, False$\\r$\\n'
    FileWrite $0 'Set WshShell = Nothing$\\r$\\n'
    FileWrite $0 'Set fso = Nothing$\\r$\\n'
    FileClose $0
    
    ; Also create a direct shortcut batch file (visible console)
    FileOpen $0 "$INSTDIR\\run-visible.bat" w
    FileWrite $0 '@echo off$\\r$\\n'
    FileWrite $0 'cd /d "%~dp0"$\\r$\\n'
    FileWrite $0 'call winapp.bat$\\r$\\n'
    FileWrite $0 'if errorlevel 1 pause$\\r$\\n'
    FileClose $0
    
    ; Create Python GUI launcher script
    FileOpen $0 "$INSTDIR\\launch_gui.pyw" w
    FileWrite $0 'import sys$\\r$\\n'
    FileWrite $0 'import os$\\r$\\n'
    FileWrite $0 'sys.path.insert(0, os.path.dirname(__file__))$\\r$\\n'
    FileWrite $0 'try:$\\r$\\n'
    FileWrite $0 '    from gui.winapp_gui import WinAppGUI$\\r$\\n'
    FileWrite $0 '    app = WinAppGUI()$\\r$\\n'
    FileWrite $0 '    app.mainloop()$\\r$\\n'
    FileWrite $0 'except Exception as e:$\\r$\\n'
    FileWrite $0 '    import tkinter as tk$\\r$\\n'
    FileWrite $0 '    from tkinter import messagebox$\\r$\\n'
    FileWrite $0 '    tk.Tk().withdraw()$\\r$\\n'
    FileWrite $0 '    messagebox.showerror("Error", f"Failed to start: {{e}}")$\\r$\\n'
    FileWrite $0 '    sys.exit(1)$\\r$\\n'
    FileClose $0
    
    ; Write installation info
    WriteRegStr HKLM "Software\\AmatakWinApp" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\\AmatakWinApp" "Version" "{version}"
    
    ; Write uninstall info
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "DisplayName" "Amatak WinApp Generator"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "UninstallString" '"$INSTDIR\\uninstall.exe"'
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "DisplayIcon" "$INSTDIR\\assets\\brand\\brand.ico"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "DisplayVersion" "{version}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "Publisher" "Amatak Holdings Pty Ltd"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp" "URLInfoAbout" "www.uniqueedge.net"
    
SectionEnd

Section "Shortcuts" SEC02
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\\$StartMenuFolder"
    ; Create shortcut to VBS launcher (hidden console)
    CreateShortcut "$SMPROGRAMS\\$StartMenuFolder\\Amatak WinApp Generator.lnk" "$INSTDIR\\launch.vbs" "" "$INSTDIR\\assets\\brand\\brand.ico" 0
    ; Create shortcut to visible console
    CreateShortcut "$SMPROGRAMS\\$StartMenuFolder\\Amatak WinApp (Console).lnk" "$INSTDIR\\run-visible.bat" "" "$INSTDIR\\assets\\brand\\brand.ico" 0
    ; Create shortcut to Python GUI launcher
    CreateShortcut "$SMPROGRAMS\\$StartMenuFolder\\Amatak WinApp GUI.lnk" "$INSTDIR\\launch_gui.pyw" "" "$INSTDIR\\assets\\brand\\brand.ico" 0
    CreateShortcut "$SMPROGRAMS\\$StartMenuFolder\\Uninstall.lnk" "$INSTDIR\\uninstall.exe" "" "$INSTDIR\\uninstall.exe" 0
    CreateShortcut "$DESKTOP\\Amatak WinApp Generator.lnk" "$INSTDIR\\launch.vbs" "" "$INSTDIR\\assets\\brand\\brand.ico" 0
    !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -Post
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    ; Remove shortcuts
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    Delete "$SMPROGRAMS\\$StartMenuFolder\\*.*"
    RMDir "$SMPROGRAMS\\$StartMenuFolder"
    Delete "$DESKTOP\\Amatak WinApp Generator.lnk"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\\AmatakWinApp"
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AmatakWinApp"
    
    ; Remove files
    Delete "$INSTDIR\\winapp.bat"
    Delete "$INSTDIR\\launch.vbs"
    Delete "$INSTDIR\\run-visible.bat"
    Delete "$INSTDIR\\launch_gui.pyw"
    Delete "$INSTDIR\\uninstall.exe"
    
    ; Remove all other files
    RMDir /r "$INSTDIR"
SectionEnd

Function .onInit
    StrCpy $StartMenuFolder "AmatakWinApp"
FunctionEnd
"""
    
    try:
        # Create installer directory if it doesn't exist
        NSIS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(NSIS_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(nsi_content)
        
        print(f"\n[{year}] ✅ NSIS installer script generated successfully!")
        print(f"   Location: {NSIS_OUTPUT_PATH}")
        print(f"   Version: {version}")
        print(f"   Files to install: {len(files_list)}")
        
        # Show what will be created
        print(f"\n📋 Launcher files that will be created:")
        print(f"   1. winapp.bat - Main console launcher")
        print(f"   2. launch.vbs - Silent VBS launcher (for desktop shortcuts)")
        print(f"   3. run-visible.bat - Visible console launcher")
        print(f"   4. launch_gui.pyw - GUI launcher (.pyw = no console)")
        
        print(f"\n📋 Shortcuts that will be created:")
        print(f"   Desktop: Amatak WinApp Generator.lnk (silent)")
        print(f"   Start Menu:")
        print(f"     - Amatak WinApp Generator.lnk (silent)")
        print(f"     - Amatak WinApp (Console).lnk (visible)")
        print(f"     - Amatak WinApp GUI.lnk (GUI)")
        print(f"     - Uninstall.lnk")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating NSIS script: {e}")
        import traceback
        traceback.print_exc()
        return False

def compile_nsis():
    """Compile the NSIS script"""
    if not NSIS_OUTPUT_PATH.exists():
        print("❌ NSIS script not found. Generate it first.")
        return False
    
    # Try to find makensis.exe
    nsis_paths = [
        r"C:\Program Files (x86)\NSIS\makensis.exe",
        r"C:\Program Files\NSIS\makensis.exe",
        r"C:\NSIS\makensis.exe",
        r"makensis.exe"  # If in PATH
    ]
    
    makensis = None
    for path in nsis_paths:
        if Path(path).exists():
            makensis = path
            break
    
    if not makensis:
        # Try to find in PATH
        import shutil
        makensis = shutil.which("makensis")
    
    if not makensis:
        print("⚠️  NSIS compiler (makensis.exe) not found.")
        print("   Install NSIS from: https://nsis.sourceforge.io/Download")
        print("   Or download portable version and add to PATH.")
        return False
    
    try:
        import subprocess
        print(f"\n🔨 Compiling installer with {makensis}...")
        print(f"   NSIS script: {NSIS_OUTPUT_PATH}")
        print(f"   Working dir: {PROJECT_ROOT}")
        
        # First, let's test if the script has any obvious syntax errors
        print("\n🔍 Checking NSIS script for common issues...")
        
        # Read the NSIS script to check for issues
        with open(NSIS_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            nsis_content = f.read()
        
        # Common issues to check
        issues = []
        
        # Check for ${PRODUCT_NAME} instead of ${PRODUCT_NAME}
        if "${PRODUCT_NAME}" in nsis_content:
            issues.append("Found ${PRODUCT_NAME} - should be ${PRODUCT_NAME}")
        
        # Check for unclosed quotes
        quote_count = nsis_content.count('"')
        if quote_count % 2 != 0:
            issues.append(f"Unbalanced quotes (found {quote_count} quotes)")
        
        # Check for unclosed curly braces in macros
        lines = nsis_content.split('\n')
        for i, line in enumerate(lines, 1):
            if '${' in line and line.count('${') != line.count('}'):
                issues.append(f"Unbalanced curly braces on line {i}: {line[:50]}...")
        
        if issues:
            print("   Found potential issues:")
            for issue in issues:
                print(f"   ⚠️  {issue}")
        else:
            print("   ✓ No obvious syntax issues found")
        
        # Now try to compile with verbose output
        print("\n🔄 Starting NSIS compilation...")
        
        # Try different NSIS command line options to get more output
        cmd_options = [
            [makensis, "/V4", str(NSIS_OUTPUT_PATH)],  # Verbose level 4
            [makensis, "/V2", str(NSIS_OUTPUT_PATH)],  # Verbose level 2
            [makensis, str(NSIS_OUTPUT_PATH)]          # Default
        ]
        
        success = False
        last_error = ""
        
        for cmd in cmd_options:
            print(f"\n   Trying: {' '.join(cmd)}")
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    cwd=PROJECT_ROOT,
                    timeout=30  # 30 second timeout
                )
                
                if result.returncode == 0:
                    print("\n✅ Installer compiled successfully!")
                    
                    # Find the generated EXE
                    version = get_version()
                    exe_name = f"Amatak_WinApp_Generator_Setup_v{version}.exe"
                    exe_path = PROJECT_ROOT / exe_name
                    
                    if exe_path.exists():
                        size_mb = exe_path.stat().st_size / (1024 * 1024)
                        print(f"\n📦 Installer created: {exe_name}")
                        print(f"   Size: {size_mb:.2f} MB")
                        print(f"   Location: {exe_path}")
                        
                        # Show additional info
                        print(f"\n📋 Installer Details:")
                        print(f"   - Product: Amatak WinApp Generator")
                        print(f"   - Version: {version}")
                        print(f"   - Company: Amatak Holdings Pty Ltd")
                        print(f"   - Output: {exe_name}")
                    else:
                        print(f"⚠️  Installer EXE not found at expected location: {exe_path}")
                        print(f"   Check: {PROJECT_ROOT}\\*.exe")
                    
                    success = True
                    break
                else:
                    # Save error for analysis
                    last_error = result.stdout + "\n" + result.stderr
                    
                    # Try to extract meaningful error
                    error_lines = []
                    for line in (result.stdout + result.stderr).split('\n'):
                        line_lower = line.lower()
                        if any(keyword in line_lower for keyword in ['error', 'warning', 'failed', 'invalid', 'syntax']):
                            error_lines.append(line.strip())
                    
                    if error_lines:
                        print(f"\n❌ Compilation errors found:")
                        for err in error_lines[:10]:  # Show first 10 errors
                            print(f"   {err}")
                    else:
                        print(f"\n❌ Compilation failed (exit code: {result.returncode}) but no error details.")
                        
            except subprocess.TimeoutExpired:
                print(f"\n❌ NSIS compilation timed out after 30 seconds")
                last_error = "Compilation timed out"
                break
            except Exception as e:
                print(f"\n❌ Error running NSIS: {e}")
                last_error = str(e)
                break
        
        if not success:
            # Try one more approach - compile with a simple test script first
            print("\n🔧 Creating test script to verify NSIS installation...")
            test_script = PROJECT_ROOT / "installer" / "test_nsis.nsi"
            test_content = """!include "MUI2.nsh"

Name "Test Installer"
OutFile "test_installer.exe"
InstallDir "$PROGRAMFILES\\TestApp"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Section "Test"
    SetOutPath "$INSTDIR"
    FileOpen $0 "$INSTDIR\\test.txt" w
    FileWrite $0 "Test file"
    FileClose $0
SectionEnd
"""
            
            try:
                with open(test_script, 'w', encoding='utf-8') as f:
                    f.write(test_content)
                
                print(f"   Created test script: {test_script}")
                test_result = subprocess.run(
                    [makensis, str(test_script)],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    cwd=PROJECT_ROOT
                )
                
                if test_result.returncode == 0:
                    print("   ✅ Test compilation successful - NSIS is working")
                    print(f"   ❌ Your script has issues. Common problems:")
                    print("      - Missing or incorrect file paths")
                    print("      - Syntax errors in functions")
                    print("      - Unbalanced quotes or brackets")
                    print(f"\n   Try running manually: \"{makensis}\" \"{NSIS_OUTPUT_PATH}\"")
                else:
                    print(f"   ❌ Test compilation failed - NSIS may have issues")
                    if test_result.stderr:
                        print(f"   Error: {test_result.stderr[:200]}")
                        
                # Clean up test files
                if (PROJECT_ROOT / "test_installer.exe").exists():
                    (PROJECT_ROOT / "test_installer.exe").unlink()
                test_script.unlink()
                
            except Exception as e:
                print(f"   ❌ Could not run test: {e}")
        
        # Final error display
        if not success:
            print(f"\n❌ NSIS compilation failed!")
            print(f"\n💡 Troubleshooting tips:")
            print("   1. Check if all required files exist (brand.ico, brand_installer.bmp)")
            print("   2. Run NSIS manually to see full error:")
            print(f'      "{makensis}" "{NSIS_OUTPUT_PATH}"')
            print("   3. Check for syntax errors in the generated NSIS file")
            print("   4. Make sure you have write permissions in the output directory")
            
            # Suggest manual compilation
            print(f"\n🔧 Try manual compilation:")
            print(f'   cd "{PROJECT_ROOT}"')
            print(f'   "{makensis}" "installer\\win_installer.nsi"')
        
        return success
            
    except Exception as e:
        print(f"❌ Failed to compile NSIS: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate NSIS installer for Amatak WinApp')
    parser.add_argument('--compile', '-c', action='store_true', help='Compile after generation')
    parser.add_argument('--version', '-v', action='store_true', help='Show version only')
    parser.add_argument('--files', '-f', action='store_true', help='List files to be installed')
    parser.add_argument('--test', '-t', action='store_true', help='Test NSIS syntax only')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Version: {get_version()}")
        return
    
    print("=" * 60)
    print("📝 Amatak WinApp - NSIS Installer Generator")
    print("=" * 60)
    
    if args.files:
        files = scan_project_files()
        print(f"\n📁 Files to be installed ({len(files)}):")
        for file in files:
            print(f"  - {file}")
        return
    
    success = generate_nsi()
    
    if success and (args.compile or args.test):
        print("\n" + "=" * 60)
        print("🔨 Compiling NSIS Installer")
        print("=" * 60)
        success = compile_nsis()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Process completed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ Process failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()