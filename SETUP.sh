#!/bin/bash

echo "==============================================="
echo "         Nuke MCP Setup Launcher"
echo "==============================================="
echo
echo "This will set up your Nuke MCP integration."
echo
read -p "Press Enter to continue..."

cd setup
chmod +x linux_setup.sh
./linux_setup.sh
cd ..

echo
echo "Setup completed! You can now use:"
echo "- setup/portable_start_script.sh to start the server"
echo "- enhanced_nuke_mcp_server.py (copied to root) for direct execution"
echo
read -p "Press Enter to exit..."
