@echo off
REM Activate local venv if exists, else use system Python
if exist venv\Scripts\activate (
    call venv\Scripts\activate
)
uvx nuke-mcp
pause
