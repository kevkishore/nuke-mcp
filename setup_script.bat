@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo         Nuke MCP Portable Setup
echo ===============================================
echo.

REM Get the current directory (where this script is located)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo Package location: %SCRIPT_DIR%
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ and add it to your PATH
    echo Download from: https://python.org
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "%SCRIPT_DIR%\venv" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%\venv"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r "%SCRIPT_DIR%\config\requirements.txt"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Install the package in development mode
echo Installing Nuke MCP package...
pip install -e "%SCRIPT_DIR%"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Nuke MCP package
    pause
    exit /b 1
)

echo ✓ Nuke MCP package installed
echo.

REM Detect Nuke plugin directory
echo Detecting Nuke plugin directory...

set "NUKE_PLUGIN_DIR="
set "USER_NUKE_DIR=%USERPROFILE%\.nuke"

REM Check if .nuke directory exists
if exist "%USER_NUKE_DIR%" (
    set "NUKE_PLUGIN_DIR=%USER_NUKE_DIR%"
    echo ✓ Found Nuke user directory: !NUKE_PLUGIN_DIR!
) else (
    echo Creating Nuke user directory: %USER_NUKE_DIR%
    mkdir "%USER_NUKE_DIR%" 2>nul
    set "NUKE_PLUGIN_DIR=%USER_NUKE_DIR%"
)

echo.

REM Copy addon to Nuke plugins directory
echo Installing Nuke addon...
copy "%SCRIPT_DIR%\src\enhanced_nuke_addon.py" "%NUKE_PLUGIN_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy addon to Nuke plugins directory
    echo Please manually copy enhanced_nuke_addon.py to: %NUKE_PLUGIN_DIR%
    pause
    exit /b 1
)

echo ✓ Nuke addon installed to: %NUKE_PLUGIN_DIR%
echo.

REM Also copy the server for reference
echo Installing MCP server...
copy "%SCRIPT_DIR%\src\enhanced_nuke_mcp_server.py" "%SCRIPT_DIR%\" >nul
echo ✓ MCP server installed to root directory
echo.

REM Generate MCP configuration
echo Generating MCP configuration...

set "CONFIG_FILE=%SCRIPT_DIR%\claude_mcp_config.json"

(
echo {
echo   "mcpServers": {
echo     "nuke": {
echo       "command": "cmd",
echo       "args": [
echo         "/c",
echo         "\"%SCRIPT_DIR%\start_nuke_mcp.bat\""
echo       ],
echo       "env": {
echo         "NUKE_MCP_ROOT": "%SCRIPT_DIR%"
echo       }
echo     }
echo   }
echo }
) > "%CONFIG_FILE%"

echo ✓ MCP configuration generated: %CONFIG_FILE%
echo.

REM Create a menu.py file for easier Nuke integration
echo Creating Nuke menu integration...

set "MENU_FILE=%NUKE_PLUGIN_DIR%\menu.py"

(
echo # Auto-generated Nuke MCP menu integration
echo import nuke
echo import os
echo import sys
echo.
echo # Add enhanced addon to path
echo addon_path = r'%NUKE_PLUGIN_DIR%'
echo if addon_path not in sys.path:
echo     sys.path.insert^(0, addon_path^)
echo.
echo try:
echo     import enhanced_nuke_addon
echo     print^("Enhanced Nuke MCP addon loaded successfully"^)
echo except Exception as e:
echo     print^(f"Failed to load Enhanced Nuke MCP addon: {e}"^)
echo.
echo # Create menu
echo def create_mcp_menu^(^):
echo     menubar = nuke.menu^('Nuke'^)
echo     mcp_menu = menubar.addMenu^('MCP'^)
echo     mcp_menu.addCommand^('Show Enhanced Panel', 'enhanced_nuke_addon.show_enhanced_panel^(^)'^)
echo     mcp_menu.addCommand^('Start Server ^(Port 9876^)', 'enhanced_nuke_addon.start_enhanced_server^(9876^)'^)
echo     mcp_menu.addCommand^('Stop Server', 'enhanced_nuke_addon.stop_enhanced_server^(^)'^)
echo.
echo # Add menu when Nuke starts
echo nuke.addOnUserCreate^(create_mcp_menu, nodeClass='Root'^)
) > "%MENU_FILE%"

echo ✓ Nuke menu integration created
echo.

REM Create quick start scripts
echo Creating quick start scripts...

set "QUICK_START=%SCRIPT_DIR%\quick_start.bat"

(
echo @echo off
echo echo Starting Nuke MCP Server...
echo call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
echo python "%SCRIPT_DIR%\enhanced_nuke_mcp_server.py"
echo pause
) > "%QUICK_START%"

echo ✓ Quick start script created
echo.

REM Display completion message
echo ===============================================
echo            SETUP COMPLETED SUCCESSFULLY!
echo ===============================================
echo.
echo Next steps:
echo.
echo 1. CONFIGURE CLAUDE DESKTOP:
echo    - Open Claude Desktop
echo    - Go to Settings ^> MCP ^> Add Server
echo    - Copy and paste the content from:
echo      %CONFIG_FILE%
echo.
echo 2. START NUKE:
echo    - Launch Nuke
echo    - You should see a new "MCP" menu
echo    - Click "Start Server" to begin
echo.
echo 3. TEST THE CONNECTION:
echo    - In Claude, try: "Create a blur node in Nuke"
echo    - Or use the quick start: %QUICK_START%
echo.
echo 4. NUKE ADDON LOCATION:
echo    - Installed to: %NUKE_PLUGIN_DIR%
echo.
echo Files generated:
echo ✓ MCP Config: claude_mcp_config.json
echo ✓ Nuke Addon: %NUKE_PLUGIN_DIR%\enhanced_nuke_addon.py
echo ✓ Menu Integration: %NUKE_PLUGIN_DIR%\menu.py
echo ✓ Quick Start: quick_start.bat
echo.
echo Press any key to open the MCP config file...
pause >nul

REM Open the config file in notepad for easy copying
notepad "%CONFIG_FILE%"

echo.
echo Setup complete! Enjoy your Nuke + Claude integration!
pause