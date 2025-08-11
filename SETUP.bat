@echo off
echo ===============================================
echo         Nuke MCP Setup Launcher
echo ===============================================
echo.
echo This will set up your Nuke MCP integration.
echo.
pause

cd setup
call setup_script.bat
cd ..

echo.
echo Setup completed! You can now use:
echo - setup\portable_start_script.bat to start the server
echo - enhanced_nuke_mcp_server.py (copied to root) for direct execution
echo.
pause
