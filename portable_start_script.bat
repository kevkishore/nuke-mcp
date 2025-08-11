@echo off
setlocal enabledelayedexpansion

REM Get the directory where this script is located (setup folder)
set "SETUP_DIR=%~dp0"
set "SETUP_DIR=%SETUP_DIR:~0,-1%"

REM Get the root directory (parent of setup)
for %%I in ("%SETUP_DIR%\..") do set "SCRIPT_DIR=%%~fI"

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    echo.
    echo Setup directory: %SETUP_DIR%
    echo Root directory: %SCRIPT_DIR%
    echo Looking for: %SCRIPT_DIR%\venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo ===============================================
echo        Starting Nuke MCP Server
echo ===============================================
echo.
echo Package location: %SCRIPT_DIR%
echo Activating virtual environment...

REM Activate virtual environment
call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Set environment variables
set "NUKE_MCP_ROOT=%SCRIPT_DIR%"
set "PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%"

echo Starting Enhanced Nuke MCP Server...
echo Server will listen on localhost:9876
echo.
echo To use with Claude:
echo 1. Make sure Nuke is running with the addon loaded
echo 2. In Nuke, go to MCP menu ^> Start Server
echo 3. In Claude, try: "Create a blur node in Nuke"
echo.
echo Press Ctrl+C to stop the server
echo ===============================================

REM Start the server
python "%SCRIPT_DIR%\enhanced_nuke_mcp_server.py"

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Server stopped with error code: %errorlevel%
    pause
)