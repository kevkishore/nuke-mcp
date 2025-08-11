#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$ROOT_DIR/venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run SETUP.sh first to install dependencies."
    exit 1
fi

echo "==============================================="
echo "        Starting Nuke MCP Server"
echo "==============================================="
echo
echo "Package location: $ROOT_DIR"
echo "Activating virtual environment..."

# Activate virtual environment
source "$ROOT_DIR/venv/bin/activate"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo

# Set environment variables
export NUKE_MCP_ROOT="$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"

echo "Starting Enhanced Nuke MCP Server..."
echo "Server will listen on localhost:9876"
echo
echo "To use with Claude:"
echo "1. Make sure Nuke is running with the addon loaded"
echo "2. In Nuke, go to MCP menu > Start Server"
echo "3. In Claude, try: \"Create a blur node in Nuke\""
echo
echo "Press Ctrl+C to stop the server"
echo "==============================================="

# Start the server
python "$ROOT_DIR/enhanced_nuke_mcp_server.py"
