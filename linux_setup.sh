#!/bin/bash

echo "==============================================="
echo "         Nuke MCP Portable Setup (Unix)"
echo "==============================================="
echo

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Package location: $SCRIPT_DIR"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10+ and add it to your PATH"
    exit 1
fi

echo "✓ Python found"
echo

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r "$SCRIPT_DIR/config/requirements.txt"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo

# Install the package in development mode
echo "Installing Nuke MCP package..."
pip install -e "$SCRIPT_DIR"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Nuke MCP package"
    exit 1
fi

echo "✓ Nuke MCP package installed"
echo

# Detect Nuke plugin directory
echo "Detecting Nuke plugin directory..."

USER_NUKE_DIR="$HOME/.nuke"

if [ -d "$USER_NUKE_DIR" ]; then
    echo "✓ Found Nuke user directory: $USER_NUKE_DIR"
else
    echo "Creating Nuke user directory: $USER_NUKE_DIR"
    mkdir -p "$USER_NUKE_DIR"
fi

echo

# Copy addon to Nuke plugins directory
echo "Installing Nuke addon..."
cp "$SCRIPT_DIR/src/enhanced_nuke_addon.py" "$USER_NUKE_DIR/"

# Also copy the server for reference
echo "Installing MCP server..."
cp "$SCRIPT_DIR/src/enhanced_nuke_mcp_server.py" "$SCRIPT_DIR/"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to copy addon to Nuke plugins directory"
    echo "Please manually copy enhanced_nuke_addon.py to: $USER_NUKE_DIR"
    exit 1
fi

echo "✓ Nuke addon installed to: $USER_NUKE_DIR"
echo

# Generate MCP configuration
echo "Generating MCP configuration..."

CONFIG_FILE="$SCRIPT_DIR/claude_mcp_config.json"

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "nuke": {
      "command": "bash",
      "args": [
        "$SCRIPT_DIR/start_nuke_mcp.sh"
      ],
      "env": {
        "NUKE_MCP_ROOT": "$SCRIPT_DIR"
      }
    }
  }
}
EOF

echo "✓ MCP configuration generated: $CONFIG_FILE"
echo

# Create menu.py for Nuke integration
echo "Creating Nuke menu integration..."

MENU_FILE="$USER_NUKE_DIR/menu.py"

cat > "$MENU_FILE" << 'EOF'
# Auto-generated Nuke MCP menu integration
import nuke
import os
import sys

# Add enhanced addon to path
addon_path = os.path.expanduser('~/.nuke')
if addon_path not in sys.path:
    sys.path.insert(0, addon_path)

try:
    import enhanced_nuke_addon
    print("Enhanced Nuke MCP addon loaded successfully")
except Exception as e:
    print(f"Failed to load Enhanced Nuke MCP addon: {e}")

# Create menu
def create_mcp_menu():
    menubar = nuke.menu('Nuke')
    mcp_menu = menubar.addMenu('MCP')
    mcp_menu.addCommand('Show Enhanced Panel', 'enhanced_nuke_addon.show_enhanced_panel()')
    mcp_menu.addCommand('Start Server (Port 9876)', 'enhanced_nuke_addon.start_enhanced_server(9876)')
    mcp_menu.addCommand('Stop Server', 'enhanced_nuke_addon.stop_enhanced_server()')

# Add menu when Nuke starts
nuke.addOnUserCreate(create_mcp_menu, nodeClass='Root')
EOF

echo "✓ Nuke menu integration created"
echo

# Create Unix start script
echo "Creating start script..."

START_SCRIPT="$SCRIPT_DIR/start_nuke_mcp.sh"

cat > "$START_SCRIPT" << EOF
#!/bin/bash

SCRIPT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "\$SCRIPT_DIR/venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first to install dependencies."
    exit 1
fi

echo "==============================================="
echo "        Starting Nuke MCP Server"
echo "==============================================="
echo
echo "Package location: \$SCRIPT_DIR"
echo "Activating virtual environment..."

# Activate virtual environment
source "\$SCRIPT_DIR/venv/bin/activate"
if [ \$? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo

# Set environment variables
export NUKE_MCP_ROOT="\$SCRIPT_DIR"
export PYTHONPATH="\$SCRIPT_DIR:\$PYTHONPATH"

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
python "\$SCRIPT_DIR/enhanced_nuke_mcp_server.py"
EOF

chmod +x "$START_SCRIPT"

echo "✓ Start script created and made executable"
echo

# Create quick start script
QUICK_START="$SCRIPT_DIR/quick_start.sh"

cat > "$QUICK_START" << EOF
#!/bin/bash
echo "Starting Nuke MCP Server..."
cd "\$(dirname "\$0")"
source "./venv/bin/activate"
python "./enhanced_nuke_mcp_server.py"
EOF

chmod +x "$QUICK_START"

echo "✓ Quick start script created"
echo

# Display completion message
echo "==============================================="
echo "            SETUP COMPLETED SUCCESSFULLY!"
echo "==============================================="
echo
echo "Next steps:"
echo
echo "1. CONFIGURE CLAUDE DESKTOP:"
echo "   - Open Claude Desktop"
echo "   - Go to Settings > MCP > Add Server"
echo "   - Copy and paste the content from:"
echo "     $CONFIG_FILE"
echo
echo "2. START NUKE:"
echo "   - Launch Nuke"
echo "   - You should see a new \"MCP\" menu"
echo "   - Click \"Start Server\" to begin"
echo
echo "3. TEST THE CONNECTION:"
echo "   - In Claude, try: \"Create a blur node in Nuke\""
echo "   - Or use the quick start: ./quick_start.sh"
echo
echo "4. NUKE ADDON LOCATION:"
echo "   - Installed to: $USER_NUKE_DIR"
echo
echo "Files generated:"
echo "✓ MCP Config: claude_mcp_config.json"
echo "✓ Nuke Addon: $USER_NUKE_DIR/enhanced_nuke_addon.py"
echo "✓ Menu Integration: $USER_NUKE_DIR/menu.py"
echo "✓ Start Script: start_nuke_mcp.sh"
echo "✓ Quick Start: quick_start.sh"
echo
echo "Setup complete! Enjoy your Nuke + Claude integration!"

# On macOS, try to open the config file
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Opening config file for easy copying..."
    open "$CONFIG_FILE"
fi